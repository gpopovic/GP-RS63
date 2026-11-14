"""Validate commercial changes, disputes, urgent containment and partial handovers."""

from __future__ import annotations

from typing import Any

CLASSIFICATIONS = {"DEFECT", "CHANGE", "UNCLEAR", "EMERGENCY_CONTAINMENT"}
STATUSES = {"NEEDS_CLARIFICATION", "READY_FOR_HUMAN_DECISION", "CONTAINMENT_ONLY", "BLOCKED"}
APPROVALS = {"NOT_DECIDED", "HUMAN_APPROVED", "HUMAN_REJECTED"}


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_commercial_change(record: object) -> list[str]:
    if not isinstance(record, dict):
        return ["commercial change must be an object"]
    payload: dict[str, Any] = record
    errors: list[str] = []
    for field in (
        "record_id", "baseline_reference", "requester", "requested_outcome", "scope_delta",
        "data_classification", "decision_owner", "reconciliation_obligation",
    ):
        if not _text(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if payload.get("classification") not in CLASSIFICATIONS:
        errors.append("classification is invalid")
    if payload.get("status") not in STATUSES:
        errors.append("status is invalid")
    if payload.get("approval_status") not in APPROVALS:
        errors.append("approval_status is invalid")
    sources = payload.get("source_references")
    if not isinstance(sources, list) or not sources or any(not _text(item) for item in sources):
        errors.append("source_references must be a non-empty string list")
    for name in ("cost_impact", "schedule_impact"):
        impact = payload.get(name)
        if not isinstance(impact, dict):
            errors.append(f"{name} must be an object")
            continue
        if not all(isinstance(impact.get(key), (int, float)) and not isinstance(impact.get(key), bool) for key in ("low", "high")):
            errors.append(f"{name} low/high must be numeric")
        elif impact["low"] > impact["high"]:
            errors.append(f"{name} low must not exceed high")
        if not _text(impact.get("source_reference")):
            errors.append(f"{name}.source_reference is required")
    protected = payload.get("protected_obligations_waived")
    if protected is not False:
        errors.append("protected_obligations_waived must be false")
    classification = payload.get("classification")
    if classification == "UNCLEAR" and payload.get("status") != "NEEDS_CLARIFICATION":
        errors.append("UNCLEAR classification must remain NEEDS_CLARIFICATION")
    if classification == "EMERGENCY_CONTAINMENT" and payload.get("status") != "CONTAINMENT_ONLY":
        errors.append("EMERGENCY_CONTAINMENT must remain CONTAINMENT_ONLY")
    if payload.get("approval_status") == "HUMAN_APPROVED" and not _text(payload.get("approval_reference")):
        errors.append("HUMAN_APPROVED requires approval_reference")
    if payload.get("automatic_execution") is not False:
        errors.append("automatic_execution must be false")
    return errors
