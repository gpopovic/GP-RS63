"""Behavior and guardrail tests for the scalable finance operating model."""

from __future__ import annotations

import json
from copy import deepcopy

from config import TRITON_ROOT
from finance_scenario import (
    calculate_cash_scenarios,
    route_finance_engagements,
    validate_finance_configuration,
    validate_finance_scenario,
)


def example() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Finance_Control" / "FINANCE_SCENARIO_RECORD.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_finance_configuration() == []

    assert route_finance_engagements(set()) == ("finance_intake_and_routing",)
    assert route_finance_engagements({"offer_or_project"}) == (
        "finance_intake_and_routing",
        "forecast_project_economics",
    )
    assert route_finance_engagements({"surplus_or_capital_commitment", "material_financial_decision"}) == (
        "finance_intake_and_routing",
        "capital_allocation",
        "independent_finance_assurance",
    )
    try:
        route_finance_engagements({"invented_trigger"})
    except ValueError as exc:
        assert "Unknown finance trigger" in str(exc)
    else:
        raise AssertionError("Unknown finance triggers must fail closed")

    payload = example()
    assert validate_finance_scenario(payload) == []
    result = calculate_cash_scenarios(payload)
    assert result["opening_available_cash"] == 70000.0
    assert result["scenario_results"]["base"][-1]["closing_available_cash"] == 85000.0
    assert result["first_liquidity_breach"]["base"] is None
    assert result["first_liquidity_breach"]["worst"] == "2026-09"
    assert result["decision_support_only"] is True
    assert result["approval_granted"] is False
    assert result["transaction_executed"] is False

    conflicted = deepcopy(payload)
    conflicted["independent_reviewer"] = conflicted["prepared_by"]
    assert any("must be distinct" in error for error in validate_finance_scenario(conflicted))

    false_range = deepcopy(payload)
    false_range["periods"][0]["inflows"]["worst"] = 90000.0
    assert any("worst <= bear <= base" in error for error in validate_finance_scenario(false_range))

    false_approval = deepcopy(payload)
    false_approval["decision_status"] = "HUMAN_APPROVED"
    assert any("requires decision_reference" in error for error in validate_finance_scenario(false_approval))

    raw_production = deepcopy(payload)
    raw_production["input_status"] = "PRODUCTION_RAW"
    assert any("SYNTHETIC or AUTHORISED_AGGREGATE" in error for error in validate_finance_scenario(raw_production))
    print("Finance operating-model and scenario-control tests passed.")


if __name__ == "__main__":
    main()
