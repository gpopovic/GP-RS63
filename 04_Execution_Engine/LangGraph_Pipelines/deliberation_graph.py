"""A bounded evidence-first debate graph for two Triton roles and a quality arbiter."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import re
import sys
from typing import Literal, TypedDict

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import load_role_instructions

RoleRunner = Callable[[str, str, str], str]
DeliberationStatus = Literal["RESOLVED", "ESCALATED"]

DELIBERATION_MARKER = re.compile(
    r"^\s*(?:#{1,6}\s+|[-*+]\s+)?(?:\*\*|__|`)?RESULT:\s*(RESOLVED|ESCALATED)(?:\*\*|__|`)?\s*(?:\r?\n|$)",
    re.IGNORECASE,
)


def parse_deliberation_status(decision: str) -> DeliberationStatus:
    """Accept a controlled first-line result marker, including light Markdown formatting."""
    match = DELIBERATION_MARKER.match(decision)
    return "RESOLVED" if match and match.group(1).upper() == "RESOLVED" else "ESCALATED"


class DeliberationState(TypedDict):
    """Auditable state for a bounded role disagreement."""

    topic: str
    producer_role: str
    reviewer_role: str
    position: str
    critique: str
    defense: str
    decision: str
    status: DeliberationStatus
    rounds: int


def build_deliberation_graph(runner: RoleRunner, max_rounds: int = 3):
    """Build Position -> Challenge -> Defense -> Resolution with bounded escalation."""
    if max_rounds < 1:
        raise ValueError("max_rounds must be at least 1")
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as error:
        raise RuntimeError("LangGraph is required. Install runtime dependencies.") from error

    def position(state: DeliberationState) -> dict[str, str]:
        prompt = load_role_instructions(state["producer_role"])
        return {"position": runner(state["producer_role"], prompt, state["topic"])}

    def challenge(state: DeliberationState) -> dict[str, object]:
        prompt = load_role_instructions(state["reviewer_role"])
        current_position = state["defense"] or state["position"]
        prior_critique = state["critique"] or "None; this is the first review round."
        work_item = (
            f"Topic:\n{state['topic']}\n\nCurrent producer position or response:\n{current_position}\n\n"
            f"Prior critique:\n{prior_critique}"
        )
        return {
            "critique": runner(state["reviewer_role"], prompt, work_item),
            "rounds": state["rounds"] + 1,
        }

    def defense(state: DeliberationState) -> dict[str, str]:
        prompt = load_role_instructions(state["producer_role"])
        work_item = (
            f"Topic:\n{state['topic']}\n\nYour position:\n{state['position']}\n\n"
            f"Independent critique:\n{state['critique']}"
        )
        return {"defense": runner(state["producer_role"], prompt, work_item)}

    def resolution(state: DeliberationState) -> dict[str, str]:
        prompt = load_role_instructions("Quality_Manager")
        work_item = (
            f"Topic:\n{state['topic']}\n\nPosition:\n{state['position']}\n\n"
            f"Critique:\n{state['critique']}\n\nDefense or correction:\n{state['defense']}\n\n"
            "Start with `RESULT: RESOLVED` only when evidence establishes an acceptable path; otherwise start with `RESULT: ESCALATED`."
        )
        decision = runner("Quality Manager", prompt, work_item)
        status = parse_deliberation_status(decision)
        return {"decision": decision, "status": status}

    def next_after_resolution(state: DeliberationState) -> Literal["challenge", "end"]:
        return "end" if state["status"] == "RESOLVED" or state["rounds"] >= max_rounds else "challenge"

    graph = StateGraph(DeliberationState)
    graph.add_node("position", position)
    graph.add_node("challenge", challenge)
    graph.add_node("defense", defense)
    graph.add_node("resolution", resolution)
    graph.add_edge(START, "position")
    graph.add_edge("position", "challenge")
    graph.add_edge("challenge", "defense")
    graph.add_edge("defense", "resolution")
    graph.add_conditional_edges("resolution", next_after_resolution, {"challenge": "challenge", "end": END})
    return graph.compile()


def build_demo_runner() -> RoleRunner:
    """Deterministic runner for local debate-flow verification."""
    def run(role_name: str, _prompt: str, _work_item: str) -> str:
        return "RESULT: RESOLVED\nDeterministic deliberation test." if role_name == "Quality Manager" else f"[DEMO {role_name}]"

    return run
