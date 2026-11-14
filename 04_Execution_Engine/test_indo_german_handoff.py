"""Tests for mandatory Germany–India handoff data."""
from indo_german_handoff import validate_handoff


def valid_handoff() -> dict[str, object]:
    return {
        "work_item_id": "TRI-1", "version": "1", "outcome": "Reviewed increment",
        "acceptance_criteria": ["tests pass"], "data_classification": "internal",
        "baseline_reference": "abc123", "dependencies": ["TRI-0"],
        "germany_owner": "DE lead", "india_owner": "IN lead", "handoff_utc": "2026-08-15T09:00:00Z",
        "decision_window_hours": 3, "evidence_plan": "test link", "status": "READY_FOR_HANDOFF",
        "escalation_owner": "Cross-Border Delivery Manager",
    }


def main() -> None:
    assert validate_handoff(valid_handoff()) == []
    blocked = valid_handoff()
    blocked["status"] = "BLOCKED"
    blocked["dependencies"] = []
    assert "BLOCKED handoff requires dependencies" in validate_handoff(blocked)
    assert "missing or empty escalation_owner" in validate_handoff({})
    print("Indo-German handoff tests passed.")


if __name__ == "__main__":
    main()
