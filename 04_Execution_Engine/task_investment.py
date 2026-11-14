"""Validate task-investment and sourcing records without committing capacity or spend."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from config import TRITON_ROOT

ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"
OBLIGATION_CLASSES = {"MANDATORY_EXTERNAL", "BINDING_COMMITMENT", "QUALITY_CRITICAL", "RISK_TRIGGERED", "OPTIONAL_IMPROVEMENT"}
READINESS_STATES = {"NOT_READY", "DISCOVERY_READY", "READY", "BLOCKED"}
PRIORITY_METHODS = {"RELATIVE_WSJF", "MONETARY_COST_OF_DELAY", "PROTECTED_OBLIGATION"}
CRITICALITY = {"CRITICAL_PATH", "NEAR_CRITICAL_PATH", "OFF_CRITICAL_PATH", "UNKNOWN"}
CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
SOURCING_MODES = {"MAKE", "BUY", "HYBRID", "UNDECIDED"}
DECISIONS = {"COMMIT", "DISCOVERY", "DEFER", "STOP"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_non_empty(item) for item in value)


def _roles() -> set[str]:
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {role for department in payload.get("departments", []) for role in department.get("members", [])}


def _positive_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and value > 0


def _ordered_positive_range(values: list[object]) -> bool:
    return all(_positive_number(value) for value in values) and float(values[0]) <= float(values[1]) <= float(values[2])


def calculate_relative_wsjf(relative_wsjf: dict[str, object]) -> float:
    """Calculate a relative discussion proxy; callers must retain all guardrails."""
    numerator = sum(float(relative_wsjf[field]) for field in ("business_value", "time_criticality", "risk_reduction_or_opportunity"))
    return numerator / float(relative_wsjf["relative_job_size"])


def validate_task_investment_record(payload: object) -> list[str]:
    """Return structural errors; a valid record is not a capacity or sourcing decision."""
    if not isinstance(payload, dict):
        return ["task investment record must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in (
        "record_id", "project_workspace_reference", "task_reference", "flow_plan_reference", "comparison_scope",
        "decision_rationale", "status_note",
    ):
        if not _non_empty(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    roles = _roles()
    for field in ("decision_owner", "independent_reviewer"):
        if payload.get(field) not in roles:
            errors.append(f"{field} must be a canonical role")
    if payload.get("decision_owner") == payload.get("independent_reviewer"):
        errors.append("decision_owner and independent_reviewer must be distinct")
    obligation = payload.get("obligation_class")
    if obligation not in OBLIGATION_CLASSES:
        errors.append("obligation_class is invalid")
    if not isinstance(payload.get("protected_priority"), bool):
        errors.append("protected_priority must be boolean")
    if payload.get("protected_priority") is True and obligation == "OPTIONAL_IMPROVEMENT":
        errors.append("optional improvement cannot claim protected priority")
    if obligation in {"MANDATORY_EXTERNAL", "BINDING_COMMITMENT", "QUALITY_CRITICAL"} and payload.get("protected_priority") is not True:
        errors.append("mandatory, binding or quality-critical work requires protected priority")
    readiness = payload.get("readiness_status")
    if readiness not in READINESS_STATES:
        errors.append("readiness_status is invalid")
    method = payload.get("priority_method")
    if method not in PRIORITY_METHODS:
        errors.append("priority_method is invalid")
    if payload.get("protected_priority") is True and method != "PROTECTED_OBLIGATION":
        errors.append("protected priority must use PROTECTED_OBLIGATION rather than an economic score")

    relative = payload.get("relative_wsjf")
    monetary = payload.get("monetary_cost_of_delay")
    if method == "RELATIVE_WSJF":
        if not isinstance(relative, dict):
            errors.append("RELATIVE_WSJF requires relative_wsjf inputs")
        else:
            scale = relative.get("scale_max")
            if isinstance(scale, bool) or not isinstance(scale, int) or not 1 <= scale <= 100:
                errors.append("relative_wsjf.scale_max must be 1-100")
            for field in ("business_value", "time_criticality", "risk_reduction_or_opportunity", "relative_job_size"):
                value = relative.get(field)
                if not _positive_number(value) or (isinstance(scale, int) and float(value) > scale):
                    errors.append(f"relative_wsjf.{field} must be positive and within scale_max")
            for field in ("scoring_session_reference", "evidence_reference"):
                if not _non_empty(relative.get(field)):
                    errors.append(f"relative_wsjf.{field} must be a non-empty string")
        if monetary is not None:
            errors.append("RELATIVE_WSJF must not mix monetary_cost_of_delay")
    elif method == "MONETARY_COST_OF_DELAY":
        if relative is not None:
            errors.append("MONETARY_COST_OF_DELAY must not mix relative_wsjf")
        if not isinstance(monetary, dict):
            errors.append("MONETARY_COST_OF_DELAY requires monetary inputs")
        else:
            if not _ordered_positive_range([monetary.get("low_per_day"), monetary.get("base_per_day"), monetary.get("high_per_day")]):
                errors.append("monetary Cost of Delay needs an ordered positive low/base/high range")
            for field in ("currency", "horizon", "evidence_reference"):
                if not _non_empty(monetary.get(field)):
                    errors.append(f"monetary_cost_of_delay.{field} must be a non-empty string")
    elif method == "PROTECTED_OBLIGATION" and payload.get("protected_priority") is not True:
        errors.append("PROTECTED_OBLIGATION requires protected_priority")

    network = payload.get("network_position")
    if not isinstance(network, dict):
        errors.append("network_position must be an object")
    else:
        if network.get("criticality") not in CRITICALITY:
            errors.append("network_position.criticality is invalid")
        total_float = network.get("total_float_working_days")
        if isinstance(total_float, bool) or not isinstance(total_float, (int, float)) or total_float < 0:
            errors.append("network_position.total_float_working_days must be non-negative")
        if not _non_empty(network.get("calculation_reference")):
            errors.append("network_position.calculation_reference must be a non-empty string")
        for field in ("dependency_unlock_references", "resource_constraint_references"):
            if not isinstance(network.get(field), list) or any(not _non_empty(item) for item in network.get(field, [])):
                errors.append(f"network_position.{field} must be a string list")

    estimate = payload.get("estimate")
    if not isinstance(estimate, dict):
        errors.append("estimate must be an object")
    else:
        if not _ordered_positive_range([estimate.get("effort_low_person_days"), estimate.get("effort_base_person_days"), estimate.get("effort_high_person_days")]):
            errors.append("estimate effort range must be ordered and positive")
        if not _ordered_positive_range([estimate.get("duration_low_working_days"), estimate.get("duration_base_working_days"), estimate.get("duration_high_working_days")]):
            errors.append("estimate duration range must be ordered and positive")
        if estimate.get("confidence") not in CONFIDENCE:
            errors.append("estimate.confidence is invalid")
        if not _non_empty(estimate.get("basis_reference")):
            errors.append("estimate.basis_reference must be a non-empty string")

    sourcing = payload.get("sourcing")
    if not isinstance(sourcing, dict):
        errors.append("sourcing must be an object")
    else:
        required = sourcing.get("analysis_required")
        if not isinstance(required, bool):
            errors.append("sourcing.analysis_required must be boolean")
        selected = sourcing.get("selected_mode")
        if selected not in SOURCING_MODES:
            errors.append("sourcing.selected_mode is invalid")
        horizon = sourcing.get("horizon_months")
        if isinstance(horizon, bool) or not isinstance(horizon, int) or not 1 <= horizon <= 360:
            errors.append("sourcing.horizon_months must be 1-360")
        alternatives = sourcing.get("alternatives")
        if not isinstance(alternatives, list) or (required is True and len(alternatives) < 2):
            errors.append("required sourcing analysis needs at least two alternatives")
        else:
            modes: set[str] = set()
            currencies: set[str] = set()
            for index, alternative in enumerate(alternatives):
                if not isinstance(alternative, dict):
                    errors.append(f"sourcing.alternatives[{index}] must be an object")
                    continue
                mode = alternative.get("mode")
                if mode not in {"MAKE", "BUY", "HYBRID"}:
                    errors.append(f"sourcing.alternatives[{index}].mode is invalid")
                elif mode in modes:
                    errors.append(f"duplicate sourcing alternative: {mode}")
                else:
                    modes.add(str(mode))
                low, high = alternative.get("tco_low"), alternative.get("tco_high")
                if not _positive_number(low) or not _positive_number(high) or float(low) > float(high):
                    errors.append(f"sourcing.alternatives[{index}] TCO range must be positive and ordered")
                currency = alternative.get("currency")
                if not _non_empty(currency):
                    errors.append(f"sourcing.alternatives[{index}].currency must be non-empty")
                else:
                    currencies.add(str(currency))
                if not _string_list(alternative.get("included_cost_families")):
                    errors.append(f"sourcing.alternatives[{index}].included_cost_families must be non-empty")
                for field in ("evidence_reference", "exit_reference"):
                    if not _non_empty(alternative.get(field)):
                        errors.append(f"sourcing.alternatives[{index}].{field} must be non-empty")
            if len(currencies) > 1:
                errors.append("sourcing alternatives must use one comparable currency")
            if required is True and selected not in modes and selected != "UNDECIDED":
                errors.append("selected sourcing mode must have a compared alternative")
        for field in ("selection_rationale", "approval_reference"):
            if not _non_empty(sourcing.get(field)):
                errors.append(f"sourcing.{field} must be a non-empty string")

    decision = payload.get("decision")
    if decision not in DECISIONS:
        errors.append("decision is invalid")
    if decision == "COMMIT" and readiness != "READY":
        errors.append("COMMIT requires READY status")
    if decision == "COMMIT" and isinstance(sourcing, dict) and sourcing.get("analysis_required") is True and str(sourcing.get("approval_reference", "")).upper() == "NOT_APPROVED":
        errors.append("COMMIT with required sourcing analysis needs approval evidence")
    if not _string_list(payload.get("guardrail_references")):
        errors.append("guardrail_references must be a non-empty string list")
    if not _string_list(payload.get("evidence_references")):
        errors.append("evidence_references must be a non-empty string list")
    if not _string_list(payload.get("invalidation_triggers")):
        errors.append("invalidation_triggers must be a non-empty string list")
    try:
        date.fromisoformat(str(payload.get("review_date")))
    except ValueError:
        errors.append("review_date must be an ISO date")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a task investment and sourcing decision record.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_task_investment_record(payload)
    if errors:
        raise SystemExit("Invalid task investment record: " + "; ".join(errors))
    relative = payload.get("relative_wsjf")
    indicator = f" Relative WSJF proxy: {calculate_relative_wsjf(relative):.2f}." if isinstance(relative, dict) else ""
    print("Task investment record valid; no capacity, sourcing or spend was approved." + indicator)


if __name__ == "__main__":
    main()
