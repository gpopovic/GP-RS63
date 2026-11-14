"""Run bounded, catalog-defined virtual governance meetings with recorded challenge."""

from __future__ import annotations

import json
import argparse
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Literal, TypedDict

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import TRITON_ROOT, load_role_instructions

RoleRunner = Callable[[str, str, str], str]
MEETING_CATALOG_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "VIRTUAL_MEETING_CATALOG.json"
ENGAGEMENT_POLICY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "MEETING_ROLE_ENGAGEMENTS.json"
ENGAGEMENT_GUIDANCE_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "MEETING_ENGAGEMENT_GUIDANCE.md"
MeetingStatus = Literal["DECIDED", "ESCALATED"]
EngagementMode = Literal["CONTRIBUTOR", "EVALUATOR", "OPPOSITION", "OBSERVER"]
MAX_SHARED_CONTEXT_CHARS = 4_000


class GovernanceMeetingState(TypedDict):
    """Auditable state for one catalog-defined virtual governance meeting."""

    meeting_id: str
    situation: str
    chair: str
    participants: list[str]
    participant_modes: dict[str, EngagementMode]
    participant_index: int
    contributions: list[str]
    challenger_report: str
    minutes: str
    status: MeetingStatus
    model_call_cap: int | None


def load_participant_modes(meeting: dict[str, object]) -> dict[str, EngagementMode]:
    """Load controlled engagement modes and reject a mode for an absent participant."""
    policy = json.loads(ENGAGEMENT_POLICY_PATH.read_text(encoding="utf-8"))
    if policy.get("schema_version") != "1.0":
        raise ValueError("Meeting engagement policy has an invalid schema.")
    valid_modes = {"CONTRIBUTOR", "EVALUATOR", "OPPOSITION", "OBSERVER"}
    default_mode = policy.get("default_participant_mode")
    if default_mode not in valid_modes:
        raise ValueError("Meeting engagement policy has an invalid default mode.")
    overrides = policy.get("meetings", {}).get(meeting["id"], {})
    if not isinstance(overrides, dict):
        raise ValueError(f"Meeting engagement policy has an invalid override: {meeting['id']}")
    participants = list(meeting["participants"])
    unknown = set(overrides) - set(participants)
    if unknown:
        raise ValueError(f"Meeting engagement policy names absent participants: {', '.join(sorted(unknown))}")
    modes: dict[str, EngagementMode] = {}
    for role in participants:
        mode = overrides.get(role, default_mode)
        if mode not in valid_modes:
            raise ValueError(f"Meeting engagement policy has an invalid mode for {role}.")
        modes[role] = mode
    return modes


def load_engagement_guidance(mode: EngagementMode) -> str:
    """Read a mode-specific instruction from controlled Markdown rather than Python text."""
    text = ENGAGEMENT_GUIDANCE_PATH.read_text(encoding="utf-8")
    match = re.search(rf"^## {mode}\s*\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing Markdown engagement guidance for {mode}.")
    return match.group(1).strip()


def load_meeting_definition(meeting_id: str) -> dict[str, object]:
    """Load an approved meeting definition without hard-coding participants in Python."""
    payload = json.loads(MEETING_CATALOG_PATH.read_text(encoding="utf-8"))
    matches = [item for item in payload["meetings"] if item["id"] == meeting_id]
    if len(matches) != 1:
        raise KeyError(f"Unknown or ambiguous governance meeting: {meeting_id}")
    meeting = matches[0]
    for role in [meeting["chair"], *meeting["participants"]]:
        load_role_instructions(role)
    meeting["participant_modes"] = load_participant_modes(meeting)
    return meeting


def estimate_meeting_model_calls(meeting_id: str) -> int:
    """Count evidence contributors plus one challenger and one chair call."""
    meeting = load_meeting_definition(meeting_id)
    modes = meeting["participant_modes"]
    active_contributors = sum(mode != "OBSERVER" for mode in modes.values())
    return active_contributors + 2


def bounded_context(items: list[str]) -> str:
    """Keep role hand-offs useful without repeatedly sending the entire meeting history."""
    text = "\n\n".join(items)
    return text[-MAX_SHARED_CONTEXT_CHARS:]


def has_controlled_outcome(minutes: str) -> bool:
    """Accept only an explicit decision or recommendation marker, with light Markdown decoration."""
    return bool(re.match(r"^\s*(?:#+\s*)?(?:\*\*)?(?:DECISION|RECOMMENDATION)(?:\*\*)?\s*:", minutes, re.IGNORECASE))


def build_governance_meeting_graph(runner: RoleRunner):
    """Build evidence round -> bounded peer discussion -> challenge -> chair decision."""
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as error:
        raise RuntimeError("LangGraph is required. Install runtime dependencies.") from error

    def initialise(state: GovernanceMeetingState) -> dict[str, object]:
        meeting = load_meeting_definition(state["meeting_id"])
        call_cap = state.get("model_call_cap")
        estimated_calls = estimate_meeting_model_calls(state["meeting_id"])
        if call_cap is not None and estimated_calls > call_cap:
            raise ValueError(
                f"Meeting requires {estimated_calls} model calls but the approved cap is {call_cap}."
            )
        return {
            "chair": meeting["chair"],
            "participants": meeting["participants"],
            "participant_modes": meeting["participant_modes"],
            "participant_index": 0,
            "contributions": [],
            "challenger_report": "",
            "status": "ESCALATED",
        }

    def contribute(state: GovernanceMeetingState) -> dict[str, object]:
        role = state["participants"][state["participant_index"]]
        mode = state["participant_modes"][role]
        if mode == "OBSERVER":
            return {
                "contributions": [*state["contributions"], f"## {role}\n[OBSERVER] Receives minutes; no evidence-round model call."],
                "participant_index": state["participant_index"] + 1,
            }
        instructions = load_role_instructions(role)
        engagement_guidance = load_engagement_guidance(mode)
        prior_discussion = bounded_context(state["contributions"])
        work_item = (
            f"Meeting ID: {state['meeting_id']}\nSituation and evidence:\n{state['situation']}\n\n"
            f"Prior discussion (may be empty):\n{prior_discussion}\n\n"
            f"Engagement mode: {mode}\n{engagement_guidance}\n\n"
            "State role-specific evidence, assumptions, risks, and one decision recommendation. "
            "Where you disagree with a prior contribution, identify the claim and explain the evidence gap. "
            "Do not invent evidence or make a decision outside your role authority."
        )
        contribution = runner(f"Governance Participant | {role}", instructions, work_item)
        return {
            "contributions": [*state["contributions"], f"## {role}\n{contribution}"],
            "participant_index": state["participant_index"] + 1,
        }

    def next_after_contribution(state: GovernanceMeetingState) -> str:
        return "contribute" if state["participant_index"] < len(state["participants"]) else "challenge"

    def challenge(state: GovernanceMeetingState) -> dict[str, str]:
        instructions = load_role_instructions("ROLE_Korrektor")
        work_item = (
            f"Meeting ID: {state['meeting_id']}\nSituation and evidence:\n{state['situation']}\n\n"
            f"Participant discussion:\n{bounded_context(state['contributions'])}\n\n"
            "Independently challenge unsupported claims, missing inputs, conflicts of interest, risk omissions, "
            "and decisions that exceed the evidence. State whether the chair must escalate."
        )
        return {"challenger_report": runner("Governance Challenger | ROLE_Korrektor", instructions, work_item)}

    def close(state: GovernanceMeetingState) -> dict[str, str]:
        meeting = load_meeting_definition(state["meeting_id"])
        instructions = load_role_instructions(state["chair"])
        work_item = (
            f"Meeting purpose: {meeting['purpose']}\nRequired outputs: {', '.join(meeting['required_outputs'])}\n\n"
            f"Situation:\n{state['situation']}\n\nParticipant contributions:\n" + bounded_context(state["contributions"])
            + f"\n\nIndependent challenger report:\n{state['challenger_report']}\n\n"
            f"Engagement modes: {state['participant_modes']}\n\n"
            "Write concise meeting minutes with decisions, dissent, owners, dates, assumptions, and next gate. "
            "For the Corp Builder Control Board, start with `RECOMMENDATION:` followed only by REJECT, REWORK, TRIAL, or REQUEST_HUMAN_APPROVAL. "
            "For other meetings start with `DECISION:` only when evidence permits it; otherwise start with `ESCALATE:`."
        )
        minutes = runner(f"Governance Chair | {state['chair']}", instructions, work_item)
        status: MeetingStatus = "DECIDED" if has_controlled_outcome(minutes) else "ESCALATED"
        return {"minutes": minutes, "status": status}

    graph = StateGraph(GovernanceMeetingState)
    graph.add_node("initialise", initialise)
    graph.add_node("contribute", contribute)
    graph.add_node("challenge", challenge)
    graph.add_node("close", close)
    graph.add_edge(START, "initialise")
    graph.add_edge("initialise", "contribute")
    graph.add_conditional_edges("contribute", next_after_contribution, {"contribute": "contribute", "challenge": "challenge"})
    graph.add_edge("challenge", "close")
    graph.add_edge("close", END)
    return graph.compile()


def build_demo_runner() -> RoleRunner:
    """Return deterministic meeting evidence for smoke testing."""
    def run(role: str, _instructions: str, _item: str) -> str:
        if role.startswith("Governance Challenger"):
            return "[DEMO challenger] No material evidence gap."
        if role.startswith("Governance Chair"):
            return "DECISION: [DEMO chair] Decision record created."
        return f"[DEMO {role}] Evidence reviewed."

    return run


def main() -> None:
    """Run one catalog-defined meeting with a local-first model route or demo runner."""
    parser = argparse.ArgumentParser(description="Run a Triton governance meeting.")
    parser.add_argument("meeting_id", help="Approved meeting ID from VIRTUAL_MEETING_CATALOG.json.")
    parser.add_argument("situation", help="Bounded situation and evidence summary; never provide unrestricted production data.")
    parser.add_argument("--max-model-calls", type=int, default=7, help="Approved model-call ceiling for this meeting.")
    parser.add_argument("--demo", action="store_true", help="Run without an LLM or network call.")
    args = parser.parse_args()
    if args.demo:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
    if args.demo:
        runner = build_demo_runner()
    else:
        # Delay model-runner import so a demo never initialises tracing clients.
        from master_graph import build_openai_runner

        runner = build_openai_runner(max_model_calls=args.max_model_calls)
    final_state = build_governance_meeting_graph(runner).invoke(
        {
            "meeting_id": args.meeting_id,
            "situation": args.situation,
            "chair": "",
            "participants": [],
            "participant_modes": {},
            "participant_index": 0,
            "contributions": [],
            "challenger_report": "",
            "minutes": "",
            "status": "ESCALATED",
            "model_call_cap": None if args.demo else args.max_model_calls,
        }
    )
    print(f"Meeting status: {final_state['status']}")
    print(final_state["minutes"])


if __name__ == "__main__":
    main()
