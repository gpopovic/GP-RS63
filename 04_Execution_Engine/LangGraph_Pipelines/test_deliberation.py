"""Deterministic test for Triton's bounded agent deliberation graph."""

from __future__ import annotations

from deliberation_graph import build_deliberation_graph, build_demo_runner, parse_deliberation_status


def main() -> None:
    result = build_deliberation_graph(build_demo_runner()).invoke(
        {
            "topic": "Should a new model become the approved validator baseline?",
            "producer_role": "Model_Quality_Observer",
            "reviewer_role": "ROLE_Korrektor",
            "position": "",
            "critique": "",
            "defense": "",
            "decision": "",
            "status": "ESCALATED",
            "rounds": 0,
        }
    )
    assert result["status"] == "RESOLVED"
    assert result["rounds"] == 1
    assert parse_deliberation_status("**RESULT: RESOLVED**\nEvidence accepted.") == "RESOLVED"
    assert parse_deliberation_status("- RESULT: ESCALATED\nOpen conflict.") == "ESCALATED"
    assert parse_deliberation_status("Discussion mentions RESULT: RESOLVED but is not a decision.") == "ESCALATED"
    print("Deliberation graph smoke test passed.")


if __name__ == "__main__":
    main()
