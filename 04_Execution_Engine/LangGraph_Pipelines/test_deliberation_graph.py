"""Smoke test for Triton's bounded role-disagreement graph."""

from __future__ import annotations

from deliberation_graph import build_deliberation_graph, build_demo_runner


def main() -> None:
    """Verify a deterministic position, challenge, defence, and resolution flow."""
    final_state = build_deliberation_graph(build_demo_runner()).invoke(
        {
            "topic": "Synthetic requirement ambiguity with no customer data.",
            "producer_role": "Requirements_Engineer",
            "reviewer_role": "Software_Architect",
            "position": "",
            "critique": "",
            "defense": "",
            "decision": "",
            "status": "ESCALATED",
            "rounds": 0,
        }
    )
    assert final_state["status"] == "RESOLVED"
    assert final_state["rounds"] == 1
    print("Deliberation graph smoke test passed.")


if __name__ == "__main__":
    main()
