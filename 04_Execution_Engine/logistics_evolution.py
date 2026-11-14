"""Validate non-activating logistics evolution experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import TRITON_ROOT

ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"
MUTABLE_FAMILIES = {"wip_capacity", "buffer_target_work_items", "queue_weights", "batch_size", "cache_prefetch"}
VECTOR_KEYS = MUTABLE_FAMILIES
QUEUE_WEIGHT_KEYS = {"delay_exposure", "dependency_unlock", "aging", "readiness", "setup_efficiency"}
REQUIRED_COST_ASPECTS = {
    "delay_exposure", "lifecycle_tco", "rework_recovery", "compute_tool_energy",
    "human_attention", "opportunity_resilience_exit",
}
DIRECTIONS = {"MINIMISE", "MAXIMISE"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and value > 0


def _roles() -> set[str]:
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {role for department in payload.get("departments", []) for role in department.get("members", [])}


def _validate_vector(vector: object, label: str) -> list[str]:
    if not isinstance(vector, dict) or set(vector) != VECTOR_KEYS:
        return [f"{label} must contain exactly the controlled logistics families"]
    errors: list[str] = []
    for field, maximum in (("wip_capacity", 64), ("buffer_target_work_items", 1000), ("batch_size", 64)):
        value = vector.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
            errors.append(f"{label}.{field} must be 1-{maximum}")
    if not isinstance(vector.get("cache_prefetch"), bool):
        errors.append(f"{label}.cache_prefetch must be boolean")
    weights = vector.get("queue_weights")
    if not isinstance(weights, dict) or set(weights) != QUEUE_WEIGHT_KEYS:
        errors.append(f"{label}.queue_weights must contain exactly the controlled non-protected factors")
    else:
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 for value in weights.values()):
            errors.append(f"{label}.queue_weights must be non-negative numbers")
        elif abs(sum(float(value) for value in weights.values()) - 1.0) > 0.000001:
            errors.append(f"{label}.queue_weights must sum to 1.0")
    return errors


def validate_logistics_evolution_experiment(payload: object) -> list[str]:
    """Return contract errors; a valid experiment remains proposal-only."""
    if not isinstance(payload, dict):
        return ["logistics evolution experiment must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in (
        "experiment_id", "project_workspace_reference", "task_class", "human_decision_reference",
        "trial_scope", "cost_cap_currency", "rollback_reference", "status_note",
    ):
        if not _non_empty(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    roles = _roles()
    role_fields = (
        "process_owner", "experiment_owner", "independent_auditor",
        "quality_guardrail_owner", "economic_reviewer",
    )
    for field in role_fields:
        if payload.get(field) not in roles:
            errors.append(f"{field} must be a canonical role")
    if payload.get("independent_auditor") in {payload.get("process_owner"), payload.get("experiment_owner")}:
        errors.append("independent_auditor must be separate from process and experiment ownership")
    periods = payload.get("minimum_comparable_periods")
    references = payload.get("comparable_period_references")
    if isinstance(periods, bool) or not isinstance(periods, int) or periods < 3:
        errors.append("minimum_comparable_periods must be at least 3")
    if not isinstance(references, list) or any(not _non_empty(item) for item in references) or (isinstance(periods, int) and len(set(references)) < periods):
        errors.append("comparable_period_references must provide the declared distinct periods")
    if payload.get("uncontrolled_high_consequence_work") is not False:
        errors.append("uncontrolled high-consequence work cannot enter a logistics experiment")
    for field in ("time_cap_hours", "cost_cap_amount"):
        if not _positive_number(payload.get(field)):
            errors.append(f"{field} must be positive")

    family = payload.get("mutated_control_family")
    if family not in MUTABLE_FAMILIES:
        errors.append("mutated_control_family is invalid")
    champion = payload.get("champion_vector")
    challenger = payload.get("challenger_vector")
    errors.extend(_validate_vector(champion, "champion_vector"))
    errors.extend(_validate_vector(challenger, "challenger_vector"))
    if isinstance(champion, dict) and isinstance(challenger, dict) and set(champion) == VECTOR_KEYS and set(challenger) == VECTOR_KEYS:
        changed = {key for key in VECTOR_KEYS if champion.get(key) != challenger.get(key)}
        if changed != {family}:
            errors.append("challenger must mutate exactly the declared one control family")

    objectives = payload.get("objective_vector")
    if not isinstance(objectives, list) or len(objectives) < 3:
        errors.append("objective_vector must contain at least three objectives")
    else:
        names: set[str] = set()
        protected_count = 0
        for index, objective in enumerate(objectives):
            if not isinstance(objective, dict):
                errors.append(f"objective_vector[{index}] must be an object")
                continue
            name = objective.get("name")
            if not _non_empty(name) or name in names:
                errors.append(f"objective_vector[{index}].name must be unique and non-empty")
            else:
                names.add(str(name))
            if objective.get("direction") not in DIRECTIONS:
                errors.append(f"objective_vector[{index}].direction is invalid")
            if not isinstance(objective.get("protected_guardrail"), bool):
                errors.append(f"objective_vector[{index}].protected_guardrail must be boolean")
            elif objective.get("protected_guardrail") is True:
                protected_count += 1
            for field in ("formula_reference", "unit", "source_reference"):
                if not _non_empty(objective.get(field)):
                    errors.append(f"objective_vector[{index}].{field} must be non-empty")
        if protected_count == 0:
            errors.append("objective_vector requires at least one protected guardrail")

    aspects = payload.get("cost_aspects")
    if not isinstance(aspects, list) or set(aspects) != REQUIRED_COST_ASPECTS:
        errors.append("cost_aspects must contain the controlled multi-cost taxonomy")
    stops = payload.get("stop_conditions")
    if not isinstance(stops, list) or len(stops) < 3 or any(not _non_empty(item) for item in stops):
        errors.append("stop_conditions must contain at least three explicit conditions")
    if payload.get("status") != "PROPOSED":
        errors.append("logistics evolution status must remain PROPOSED")
    if payload.get("automatic_activation") is not False:
        errors.append("automatic_activation must be false")
    if str(payload.get("human_decision_reference", "")).upper() != "NOT_APPROVED":
        errors.append("template contract accepts proposals only; approval remains external")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a proposal-only logistics evolution experiment.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_logistics_evolution_experiment(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid logistics evolution experiment: " + "; ".join(errors))
    print("Logistics evolution experiment valid; champion remains active and no control was changed.")


if __name__ == "__main__":
    main()
