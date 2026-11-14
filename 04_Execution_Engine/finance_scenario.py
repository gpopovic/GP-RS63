"""Route and validate finance scenarios without approving or executing finance actions."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from config import TRITON_ROOT

ENGAGEMENT_CATALOG_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "FINANCE_ENGAGEMENT_CATALOG.json"
DECISION_RIGHTS_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "FINANCE_DECISION_RIGHTS.json"
ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"

SCENARIOS = ("base", "bear", "worst")
DATA_CLASSES = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
INPUT_STATUSES = {"SYNTHETIC", "AUTHORISED_AGGREGATE"}
APPROVAL_STATUSES = {"NOT_APPROVED", "HUMAN_APPROVED"}
CONFIDENCE_LEVELS = {"LOW", "MEDIUM", "HIGH"}
RESERVE_TYPES = {"TAX", "VAT_GST", "PAYROLL", "DEBT_SERVICE", "CUSTOMER_FUNDS", "OTHER"}
PERIOD_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float))


def _non_negative(value: object) -> bool:
    return _number(value) and float(value) >= 0


def _canonical_roles() -> set[str]:
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {role for department in payload["departments"] for role in department["members"]}


def validate_finance_configuration() -> list[str]:
    """Check catalog and decision-right records against canonical roles."""
    errors: list[str] = []
    roles = _canonical_roles()
    catalog = json.loads(ENGAGEMENT_CATALOG_PATH.read_text(encoding="utf-8"))
    rights = json.loads(DECISION_RIGHTS_PATH.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != "1.0":
        errors.append("finance engagement catalog schema_version must be 1.0")
    engagement_ids: set[str] = set()
    for engagement in catalog.get("engagements", []):
        engagement_id = engagement.get("id")
        if not _non_empty(engagement_id) or engagement_id in engagement_ids:
            errors.append("finance engagement IDs must be unique non-empty strings")
        else:
            engagement_ids.add(str(engagement_id))
        triggers = engagement.get("trigger_flags")
        if not isinstance(triggers, list) or not triggers or any(not _non_empty(item) for item in triggers):
            errors.append(f"{engagement_id}.trigger_flags must be a non-empty string list")
        for field in ("preparers", "challengers"):
            assigned = engagement.get(field)
            if not isinstance(assigned, list) or any(role not in roles for role in assigned):
                errors.append(f"{engagement_id}.{field} must contain canonical roles")
        if set(engagement.get("preparers", [])) & set(engagement.get("challengers", [])):
            errors.append(f"{engagement_id} cannot assign one role as preparer and challenger")
        for field in ("outputs", "prohibited_actions"):
            values = engagement.get(field)
            if not isinstance(values, list) or not values or any(not _non_empty(item) for item in values):
                errors.append(f"{engagement_id}.{field} must be a non-empty string list")

    if rights.get("schema_version") != "1.0":
        errors.append("finance decision-rights schema_version must be 1.0")
    special = set(rights.get("special_authorities", []))
    allowed = roles | special
    decision_ids: set[str] = set()
    for decision in rights.get("decisions", []):
        decision_id = decision.get("id")
        if not _non_empty(decision_id) or decision_id in decision_ids:
            errors.append("finance decision IDs must be unique non-empty strings")
        else:
            decision_ids.add(str(decision_id))
        for field in ("prepare", "challenge", "approve", "execute", "reconcile"):
            assigned = decision.get(field)
            if not isinstance(assigned, list) or any(actor not in allowed for actor in assigned):
                errors.append(f"{decision_id}.{field} contains an unknown actor")
        if not decision.get("approve"):
            errors.append(f"{decision_id}.approve must name a human or qualified authority")
        if not _non_empty(decision.get("independence_rule")):
            errors.append(f"{decision_id}.independence_rule must be explicit")
    return errors


def route_finance_engagements(trigger_flags: set[str]) -> tuple[str, ...]:
    """Return catalog-ordered finance cells for declared flags; this is not approval."""
    catalog = json.loads(ENGAGEMENT_CATALOG_PATH.read_text(encoding="utf-8"))
    known_flags = {
        flag
        for engagement in catalog["engagements"]
        for flag in engagement["trigger_flags"]
    }
    unknown = trigger_flags - known_flags
    if unknown:
        raise ValueError(f"Unknown finance trigger flags: {sorted(unknown)}")
    selected: list[str] = []
    for engagement in catalog["engagements"]:
        if engagement["id"] == "finance_intake_and_routing" or trigger_flags.intersection(engagement["trigger_flags"]):
            selected.append(str(engagement["id"]))
    return tuple(selected)


def validate_finance_scenario(payload: object) -> list[str]:
    """Return structural and consistency errors without accepting financial facts."""
    if not isinstance(payload, dict):
        return ["finance scenario must be a JSON object"]
    errors: list[str] = []
    roles = _canonical_roles()
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in ("record_id", "workspace_reference", "decision_question"):
        if not _non_empty(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    try:
        date.fromisoformat(str(payload.get("as_of_date")))
    except ValueError:
        errors.append("as_of_date must be an ISO date")
    currency = payload.get("reporting_currency")
    if not isinstance(currency, str) or not CURRENCY_PATTERN.fullmatch(currency):
        errors.append("reporting_currency must be a three-letter uppercase code")
    if payload.get("data_classification") not in DATA_CLASSES:
        errors.append("data_classification is invalid")
    if payload.get("input_status") not in INPUT_STATUSES:
        errors.append("input_status must be SYNTHETIC or AUTHORISED_AGGREGATE")
    for field in ("prepared_by", "independent_reviewer"):
        if payload.get(field) not in roles:
            errors.append(f"{field} must be a canonical role")
    if payload.get("prepared_by") == payload.get("independent_reviewer"):
        errors.append("prepared_by and independent_reviewer must be distinct")
    sources = payload.get("source_references")
    if not isinstance(sources, list) or not sources or any(not _non_empty(item) for item in sources):
        errors.append("source_references must be a non-empty string list")
    if not _non_negative(payload.get("opening_cash")):
        errors.append("opening_cash must be non-negative")

    reserves = payload.get("protected_reserves")
    reserve_ids: set[str] = set()
    if not isinstance(reserves, list):
        errors.append("protected_reserves must be a list")
    else:
        for index, reserve in enumerate(reserves):
            if not isinstance(reserve, dict):
                errors.append(f"protected_reserves[{index}] must be an object")
                continue
            reserve_id = reserve.get("reserve_id")
            if not _non_empty(reserve_id) or reserve_id in reserve_ids:
                errors.append("reserve_id values must be unique non-empty strings")
            else:
                reserve_ids.add(str(reserve_id))
            if reserve.get("reserve_type") not in RESERVE_TYPES:
                errors.append(f"protected_reserves[{index}].reserve_type is invalid")
            if not _non_negative(reserve.get("amount")):
                errors.append(f"protected_reserves[{index}].amount must be non-negative")
            if not _non_empty(reserve.get("source_reference")):
                errors.append(f"protected_reserves[{index}].source_reference is required")
            if reserve.get("approval_status") not in APPROVAL_STATUSES:
                errors.append(f"protected_reserves[{index}].approval_status is invalid")

    liquidity = payload.get("minimum_operating_liquidity")
    if not isinstance(liquidity, dict):
        errors.append("minimum_operating_liquidity must be an object")
    else:
        if not _non_negative(liquidity.get("amount")):
            errors.append("minimum_operating_liquidity.amount must be non-negative")
        if not _non_empty(liquidity.get("policy_reference")):
            errors.append("minimum_operating_liquidity.policy_reference is required")
        approval_status = liquidity.get("approval_status")
        if approval_status not in APPROVAL_STATUSES:
            errors.append("minimum_operating_liquidity.approval_status is invalid")
        if approval_status == "HUMAN_APPROVED" and str(liquidity.get("approval_reference", "")).upper() in {"", "NOT_APPROVED", "NOT_DECIDED"}:
            errors.append("approved minimum liquidity requires human approval evidence")

    periods = payload.get("periods")
    observed_periods: list[str] = []
    if not isinstance(periods, list) or not 1 <= len(periods) <= 36:
        errors.append("periods must contain 1-36 monthly entries")
    else:
        for index, period in enumerate(periods):
            if not isinstance(period, dict):
                errors.append(f"periods[{index}] must be an object")
                continue
            period_id = period.get("period")
            if not isinstance(period_id, str) or not PERIOD_PATTERN.fullmatch(period_id):
                errors.append(f"periods[{index}].period must be YYYY-MM")
            else:
                observed_periods.append(period_id)
            values: dict[str, dict[str, object]] = {}
            for flow in ("inflows", "outflows"):
                scenario_values = period.get(flow)
                if not isinstance(scenario_values, dict):
                    errors.append(f"periods[{index}].{flow} must be an object")
                    continue
                values[flow] = scenario_values
                for scenario in SCENARIOS:
                    if not _non_negative(scenario_values.get(scenario)):
                        errors.append(f"periods[{index}].{flow}.{scenario} must be non-negative")
            if "inflows" in values and all(_non_negative(values["inflows"].get(scenario)) for scenario in SCENARIOS):
                if not float(values["inflows"]["worst"]) <= float(values["inflows"]["bear"]) <= float(values["inflows"]["base"]):
                    errors.append(f"periods[{index}] inflows must satisfy worst <= bear <= base")
            if "outflows" in values and all(_non_negative(values["outflows"].get(scenario)) for scenario in SCENARIOS):
                if not float(values["outflows"]["base"]) <= float(values["outflows"]["bear"]) <= float(values["outflows"]["worst"]):
                    errors.append(f"periods[{index}] outflows must satisfy base <= bear <= worst")
        if observed_periods != sorted(set(observed_periods)):
            errors.append("periods must be unique and ascending")

    assumptions = payload.get("assumptions")
    if not isinstance(assumptions, list) or not assumptions:
        errors.append("assumptions must be a non-empty list")
    else:
        assumption_ids: set[str] = set()
        for index, assumption in enumerate(assumptions):
            if not isinstance(assumption, dict):
                errors.append(f"assumptions[{index}] must be an object")
                continue
            assumption_id = assumption.get("assumption_id")
            if not _non_empty(assumption_id) or assumption_id in assumption_ids:
                errors.append("assumption_id values must be unique non-empty strings")
            else:
                assumption_ids.add(str(assumption_id))
            for field in ("description", "effect_reference", "validation_reference"):
                if not _non_empty(assumption.get(field)):
                    errors.append(f"assumptions[{index}].{field} is required")
            if assumption.get("owner") not in roles:
                errors.append(f"assumptions[{index}].owner must be a canonical role")
            try:
                date.fromisoformat(str(assumption.get("expiry_date")))
            except ValueError:
                errors.append(f"assumptions[{index}].expiry_date must be an ISO date")

    stress_refs = payload.get("stress_event_references")
    if not isinstance(stress_refs, list) or not stress_refs or any(not _non_empty(item) for item in stress_refs):
        errors.append("stress_event_references must be a non-empty string list")
    if payload.get("data_confidence") not in CONFIDENCE_LEVELS:
        errors.append("data_confidence is invalid")
    decision_status = payload.get("decision_status")
    if decision_status not in APPROVAL_STATUSES:
        errors.append("decision_status is invalid")
    if decision_status == "HUMAN_APPROVED" and str(payload.get("decision_reference", "")).upper() in {"", "NOT_APPROVED", "NOT_DECIDED"}:
        errors.append("HUMAN_APPROVED requires decision_reference evidence")
    return errors


def calculate_cash_scenarios(payload: dict[str, Any]) -> dict[str, Any]:
    """Calculate declared cash scenarios after validation; return no approval or transaction."""
    errors = validate_finance_scenario(payload)
    if errors:
        raise ValueError("Invalid finance scenario: " + "; ".join(errors))
    reserve_total = sum(float(item["amount"]) for item in payload["protected_reserves"])
    opening_available = float(payload["opening_cash"]) - reserve_total
    minimum = float(payload["minimum_operating_liquidity"]["amount"])
    results: dict[str, list[dict[str, float | str]]] = {}
    first_breaches: dict[str, str | None] = {}
    for scenario in SCENARIOS:
        cash = opening_available
        entries: list[dict[str, float | str]] = []
        first_breach: str | None = None
        for period in payload["periods"]:
            cash += float(period["inflows"][scenario]) - float(period["outflows"][scenario])
            headroom = cash - minimum
            if headroom < 0 and first_breach is None:
                first_breach = str(period["period"])
            entries.append({
                "period": str(period["period"]),
                "closing_available_cash": round(cash, 2),
                "liquidity_headroom": round(headroom, 2),
            })
        results[scenario] = entries
        first_breaches[scenario] = first_breach
    return {
        "record_id": payload["record_id"],
        "reporting_currency": payload["reporting_currency"],
        "opening_cash": round(float(payload["opening_cash"]), 2),
        "protected_reserve_total": round(reserve_total, 2),
        "opening_available_cash": round(opening_available, 2),
        "minimum_operating_liquidity": round(minimum, 2),
        "minimum_liquidity_approval_status": payload["minimum_operating_liquidity"]["approval_status"],
        "scenario_results": results,
        "first_liquidity_breach": first_breaches,
        "decision_support_only": True,
        "approval_granted": False,
        "transaction_executed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and calculate a controlled finance scenario.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--triggers", nargs="*", default=[])
    args = parser.parse_args()
    configuration_errors = validate_finance_configuration()
    if configuration_errors:
        raise SystemExit("Invalid finance configuration: " + "; ".join(configuration_errors))
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    result = calculate_cash_scenarios(payload)
    result["selected_engagements"] = route_finance_engagements(set(args.triggers))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
