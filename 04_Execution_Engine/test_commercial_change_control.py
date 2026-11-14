"""Tests for commercial change and exception validation."""

from copy import deepcopy

from commercial_change_control import validate_commercial_change


def example() -> dict[str, object]:
    return {
        "record_id": "SYNTHETIC-CHANGE-001",
        "baseline_reference": "contract://synthetic/baseline/1",
        "requester": "Synthetic customer",
        "requested_outcome": "Add an optional report",
        "scope_delta": "One report outside baseline acceptance criteria",
        "classification": "CHANGE",
        "source_references": ["evidence://synthetic/request", "evidence://synthetic/baseline"],
        "cost_impact": {"low": 100.0, "high": 200.0, "source_reference": "estimate://synthetic/cost"},
        "schedule_impact": {"low": 1.0, "high": 2.0, "source_reference": "estimate://synthetic/days"},
        "data_classification": "INTERNAL",
        "decision_owner": "Commercial_and_Pricing_Manager",
        "reconciliation_obligation": "Update the approved baseline after human decision.",
        "protected_obligations_waived": False,
        "status": "READY_FOR_HUMAN_DECISION",
        "approval_status": "NOT_DECIDED",
        "automatic_execution": False,
    }


def main() -> None:
    assert validate_commercial_change(example()) == []
    unclear = deepcopy(example())
    unclear["classification"] = "UNCLEAR"
    assert any("NEEDS_CLARIFICATION" in item for item in validate_commercial_change(unclear))
    waiver = deepcopy(example())
    waiver["protected_obligations_waived"] = True
    assert any("must be false" in item for item in validate_commercial_change(waiver))
    emergency = deepcopy(example())
    emergency["classification"] = "EMERGENCY_CONTAINMENT"
    emergency["status"] = "CONTAINMENT_ONLY"
    assert validate_commercial_change(emergency) == []
    print("Commercial change-control tests passed.")


if __name__ == "__main__":
    main()
