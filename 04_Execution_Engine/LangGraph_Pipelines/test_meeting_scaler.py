"""Smoke test for deterministic governance-scaling recommendations."""

from meeting_scaler import recommend_meetings


def main() -> None:
    result = recommend_meetings(
        {
            "sprint_length_days": 10,
            "feature_team_count": 2,
            "active_customers": 3,
            "external_parties": 4,
            "delivery_state": "AMBER",
            "available_capacity_fraction": 0.76,
            "material_investment_decision": True,
            "sow_decision_required": True,
            "material_change_required": True,
        }
    )
    assert result["capacity_mode"] == "REDUCED_SCOPE"
    assert result["coordination_mode"] == "EVIDENCE_ROUND_THEN_DECISION"
    assert "nexus_integration_review" in result["meeting_ids"]
    assert "event_triggered_sow_review" in result["meeting_ids"]
    assert "event_triggered_change_control_board" in result["meeting_ids"]
    print("Meeting scaler smoke test passed.")


if __name__ == "__main__":
    main()
