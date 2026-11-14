"""Smoke test for the catalog-driven virtual governance meeting graph."""

from __future__ import annotations

import json

from governance_meeting_graph import (
    MEETING_CATALOG_PATH,
    build_governance_meeting_graph,
    estimate_meeting_model_calls,
    load_meeting_definition,
)


def main() -> None:
    definition = load_meeting_definition("monthly_treasury_capital_review")
    assert definition["chair"] == "Banking_and_Treasury_Manager"
    calls: list[str] = []

    def runner(role: str, _instructions: str, _work_item: str) -> str:
        calls.append(role)
        if role.startswith("Governance Challenger"):
            return "[DEMO challenger] No material evidence gap."
        if role.startswith("Governance Chair"):
            return "DECISION: [DEMO chair] Decision record created."
        return f"[DEMO {role}] Evidence reviewed."

    final_state = build_governance_meeting_graph(runner).invoke(
        {
            "meeting_id": "monthly_treasury_capital_review",
            "situation": "Cash forecast changed; compare two capital-allocation cases.",
            "chair": "",
            "participants": [],
            "participant_index": 0,
            "contributions": [],
            "challenger_report": "",
            "minutes": "",
            "status": "ESCALATED",
        }
    )
    assert len(final_state["contributions"]) == len(definition["participants"])
    assert "DECISION:" in final_state["minutes"]
    assert "DEMO challenger" in final_state["challenger_report"]
    assert final_state["status"] == "DECIDED"
    assert len(calls) == estimate_meeting_model_calls("monthly_treasury_capital_review")
    assert all("OBSERVER" not in call for call in calls)

    catalog = json.loads(MEETING_CATALOG_PATH.read_text(encoding="utf-8"))
    for meeting in catalog["meetings"]:
        modes = load_meeting_definition(meeting["id"])["participant_modes"]
        assert set(modes) == set(meeting["participants"])
    print("Governance meeting graph smoke test passed.")


if __name__ == "__main__":
    main()
