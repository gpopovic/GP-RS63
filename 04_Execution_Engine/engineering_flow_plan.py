"""Validate engineering flow logistics plans without executing project work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import TRITON_ROOT

ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"
PROCESS_STRENGTHS = {"LEAN", "STANDARD", "ASSURANCE"}
FLOW_STATES = {"INCOMING", "READY", "ACTIVE", "VERIFYING", "QUARANTINED", "ACCEPTED", "RELEASED", "BLOCKED", "SUPERSEDED"}
READINESS_STATES = {"PENDING", "ACCEPTED", "REJECTED", "QUARANTINED"}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
QUEUE_POLICIES = {"RISK_VALUE_WEIGHTED_PULL", "FIFO_WITH_EXPEDITE_CONTROL", "DEADLINE_AWARE_PULL"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _roles() -> set[str]:
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {role for department in payload.get("departments", []) for role in department.get("members", [])}


def _string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_non_empty(item) for item in value)


def validate_engineering_flow_plan(payload: object) -> list[str]:
    """Return structural errors; validation does not reserve, execute or release."""
    if not isinstance(payload, dict):
        return ["engineering flow plan must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in ("plan_id", "project_workspace_reference", "task_class", "candidate_area_reference", "release_manifest_reference", "status_note"):
        if not _non_empty(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if payload.get("process_strength") not in PROCESS_STRENGTHS:
        errors.append("process_strength is invalid")
    if payload.get("current_state") not in FLOW_STATES:
        errors.append("current_state is invalid")
    roles = _roles()
    for field in ("decision_owner", "flow_owner"):
        if payload.get(field) not in roles:
            errors.append(f"{field} must be a canonical role")
    if not isinstance(payload.get("quarantine_required"), bool):
        errors.append("quarantine_required must be boolean")

    artifact_ids: set[str] = set()
    artifacts = payload.get("artifact_inputs")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifact_inputs must be a non-empty list")
    else:
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"artifact_inputs[{index}] must be an object")
                continue
            for field in ("artifact_id", "version_or_baseline", "source_reference", "integrity_reference", "acceptance_condition"):
                if not _non_empty(artifact.get(field)):
                    errors.append(f"artifact_inputs[{index}].{field} must be a non-empty string")
            artifact_id = artifact.get("artifact_id")
            if _non_empty(artifact_id):
                if artifact_id in artifact_ids:
                    errors.append(f"duplicate artifact_id: {artifact_id}")
                artifact_ids.add(str(artifact_id))
            if artifact.get("classification") not in CLASSIFICATIONS:
                errors.append(f"artifact_inputs[{index}].classification is invalid")
            if artifact.get("readiness_status") not in READINESS_STATES:
                errors.append(f"artifact_inputs[{index}].readiness_status is invalid")
            if artifact.get("owner") not in roles:
                errors.append(f"artifact_inputs[{index}].owner must be a canonical role")

    edges = payload.get("dependency_edges")
    if not isinstance(edges, list):
        errors.append("dependency_edges must be a list")
    else:
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict) or not all(_non_empty(edge.get(field)) for field in ("predecessor", "successor", "acceptance_reference")):
                errors.append(f"dependency_edges[{index}] must identify predecessor, successor and acceptance_reference")
            elif edge.get("predecessor") == edge.get("successor"):
                errors.append(f"dependency_edges[{index}] cannot be a self-dependency")

    resources = payload.get("constrained_resources")
    if not isinstance(resources, list):
        errors.append("constrained_resources must be a list")
    else:
        for index, resource in enumerate(resources):
            if not isinstance(resource, dict):
                errors.append(f"constrained_resources[{index}] must be an object")
                continue
            for field in ("resource_id", "reservation_reference"):
                if not _non_empty(resource.get(field)):
                    errors.append(f"constrained_resources[{index}].{field} must be a non-empty string")
            if resource.get("resource_owner") not in roles:
                errors.append(f"constrained_resources[{index}].resource_owner must be a canonical role")
            capacity = resource.get("wip_capacity")
            if isinstance(capacity, bool) or not isinstance(capacity, int) or not 1 <= capacity <= 64:
                errors.append(f"constrained_resources[{index}].wip_capacity must be 1-64")
            if resource.get("queue_policy") not in QUEUE_POLICIES:
                errors.append(f"constrained_resources[{index}].queue_policy is invalid")
            if not _string_list(resource.get("priority_factors")):
                errors.append(f"constrained_resources[{index}].priority_factors must be a non-empty string list")

    if not _string_list(payload.get("early_checks")):
        errors.append("early_checks must be a non-empty string list")
    if not _string_list(payload.get("flow_metrics")):
        errors.append("flow_metrics must be a non-empty string list")
    if not _string_list(payload.get("evidence_references")):
        errors.append("evidence_references must be a non-empty string list")

    strategy = payload.get("failure_strategy")
    if not isinstance(strategy, dict):
        errors.append("failure_strategy must be an object")
    else:
        for field in ("containment_reference", "prevalidated_rollback_reference"):
            if not _non_empty(strategy.get(field)):
                errors.append(f"failure_strategy.{field} must be a non-empty string")
        if not isinstance(strategy.get("forward_recovery_allowed"), bool):
            errors.append("failure_strategy.forward_recovery_allowed must be boolean")
        if strategy.get("recovery_authority") not in roles:
            errors.append("failure_strategy.recovery_authority must be a canonical role")

    if payload.get("current_state") == "RELEASED" and str(payload.get("release_manifest_reference", "")).upper() == "NOT_RELEASED":
        errors.append("RELEASED state requires a release manifest reference")
    if payload.get("quarantine_required") is True and str(payload.get("candidate_area_reference", "")).upper() in {"NONE", "NOT_APPLICABLE"}:
        errors.append("quarantine_required needs a controlled candidate area")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an engineering flow logistics plan.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_engineering_flow_plan(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid engineering flow plan: " + "; ".join(errors))
    print("Engineering flow plan valid; no resource was reserved, executed or released.")


if __name__ == "__main__":
    main()
