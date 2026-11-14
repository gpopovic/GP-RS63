"""Run the controlled multi-model review path for Triton_AI_Corp configuration changes."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from governance_meeting_graph import build_governance_meeting_graph, build_demo_runner
from master_graph import build_openai_runner
from Local_Model_Operations.gpu_relief import release_configured_models

CONTROL_MEETING_ID = "event_triggered_corp_builder_control_board"
ALLOWED_RECOMMENDATIONS = ("REJECT", "REWORK", "TRIAL", "REQUEST_HUMAN_APPROVAL")


def validate_control_board_minutes(minutes: str) -> str | None:
    """Return the controlled recommendation or None for an unusable free-text brief."""
    match = re.search(r"^RECOMMENDATION:\s*(REJECT|REWORK|TRIAL|REQUEST_HUMAN_APPROVAL)\b", minutes, re.MULTILINE)
    return match.group(1) if match else None


def run_control_board(
    change_packet: str, *, demo: bool = False, max_model_calls: int = 9
) -> dict[str, object]:
    """Return a review brief; this function never applies the proposed change."""
    if demo:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"

    if demo:
        base_runner = build_demo_runner()
        def runner(role_name: str, instructions: str, work_item: str) -> str:
            if role_name.startswith("Governance Chair"):
                return "RECOMMENDATION: TRIAL\n[DEMO chair] Decision record created."
            return base_runner(role_name, instructions, work_item)
    else:
        runner = build_openai_runner(max_model_calls=max_model_calls)
    result = build_governance_meeting_graph(runner).invoke(
        {
            "meeting_id": CONTROL_MEETING_ID,
            "situation": change_packet,
            "chair": "",
            "participants": [],
            "participant_modes": {},
            "participant_index": 0,
            "contributions": [],
            "challenger_report": "",
            "minutes": "",
            "status": "ESCALATED",
            "model_call_cap": None if demo else max_model_calls,
        }
    )
    recommendation = validate_control_board_minutes(str(result["minutes"]))
    result["recommendation"] = recommendation or "REQUEST_HUMAN_APPROVAL"
    result["status"] = "DECIDED" if recommendation else "ESCALATED"
    return result


def main() -> None:
    """Run a data-safe Corp Builder change-control board meeting."""
    parser = argparse.ArgumentParser(description="Review a Triton_AI_Corp configuration change without applying it.")
    parser.add_argument("change_packet", type=Path, help="Markdown change packet; never use unrestricted production data.")
    parser.add_argument("--demo", action="store_true", help="Run deterministic control-board validation.")
    args = parser.parse_args()

    packet = args.change_packet.resolve()
    if packet.suffix.lower() != ".md" or not packet.is_file():
        raise FileNotFoundError("Provide an existing Markdown change packet.")

    try:
        result = run_control_board(packet.read_text(encoding="utf-8"), demo=args.demo)
    finally:
        if not args.demo:
            release_configured_models()
    print(f"Control-board status: {result['status']}")
    print(result["minutes"])


if __name__ == "__main__":
    main()
