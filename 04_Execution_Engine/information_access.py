"""Validate bounded information-access decision records without granting access."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
STATUSES = {"REQUESTED", "APPROVED", "DENIED", "REVOKED", "EXPIRED"}
CONTROL_CAPACITIES = {
    "PRIVACY_CONTROL",
    "LEGAL_CONTROL",
    "SECURITY_CONTROL",
    "FINANCE_CONTROL",
    "CUSTOMER_CONTROL",
}
REQUIRED_FIELDS = (
    "request_id",
    "resource_scope",
    "data_classification",
    "requester",
    "purpose",
    "processing_context",
    "minimum_fields",
    "data_owner",
    "requested_at_utc",
    "expires_at_utc",
    "status",
    "approvals",
    "decision_reference",
    "revocation_owner",
)


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_timestamp(value: object, field: str, errors: list[str]) -> datetime | None:
    if not _non_empty_string(value):
        errors.append(f"{field} must be a non-empty ISO 8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} must be a valid ISO 8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{field} must include a UTC offset")
        return None
    return parsed


def validate_access_request(
    payload: object, evaluation_time_utc: datetime | str | None = None
) -> list[str]:
    """Return all contract errors; an empty list is not an access grant."""
    if not isinstance(payload, dict):
        return ["access request must be a JSON object"]

    record: dict[str, Any] = payload
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing field: {field}")

    for field in (
        "request_id",
        "resource_scope",
        "requester",
        "purpose",
        "processing_context",
        "data_owner",
        "decision_reference",
        "revocation_owner",
    ):
        if field in record and not _non_empty_string(record[field]):
            errors.append(f"{field} must be a non-empty string")

    classification = record.get("data_classification")
    if classification not in CLASSIFICATIONS:
        errors.append(f"data_classification must be one of {sorted(CLASSIFICATIONS)}")

    status = record.get("status")
    if status not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    minimum_fields = record.get("minimum_fields")
    if not isinstance(minimum_fields, list) or not minimum_fields or not all(
        _non_empty_string(item) for item in minimum_fields
    ):
        errors.append("minimum_fields must contain at least one exact non-empty scope item")

    requested_at = _parse_timestamp(record.get("requested_at_utc"), "requested_at_utc", errors)
    expires_at = _parse_timestamp(record.get("expires_at_utc"), "expires_at_utc", errors)
    if requested_at and expires_at and expires_at <= requested_at:
        errors.append("expires_at_utc must be later than requested_at_utc")

    if evaluation_time_utc is None:
        evaluation_time = datetime.now(timezone.utc)
    elif isinstance(evaluation_time_utc, datetime):
        if evaluation_time_utc.tzinfo is None:
            errors.append("evaluation_time_utc must include a UTC offset")
            evaluation_time = None
        else:
            evaluation_time = evaluation_time_utc
    else:
        evaluation_time = _parse_timestamp(
            evaluation_time_utc, "evaluation_time_utc", errors
        )

    approvals = record.get("approvals")
    if not isinstance(approvals, list):
        errors.append("approvals must be a list")
        approvals = []

    approved_by: set[str] = set()
    control_approvers: set[str] = set()
    has_denial = False
    for index, approval in enumerate(approvals):
        if not isinstance(approval, dict):
            errors.append(f"approvals[{index}] must be an object")
            continue
        for field in ("approver", "capacity", "decision", "decided_at_utc", "evidence_reference"):
            if not _non_empty_string(approval.get(field)):
                errors.append(f"approvals[{index}].{field} must be a non-empty string")
        if approval.get("decision") not in {"APPROVE", "DENY"}:
            errors.append(f"approvals[{index}].decision must be APPROVE or DENY")
        if approval.get("decision") == "DENY":
            has_denial = True
        decided_at = _parse_timestamp(
            approval.get("decided_at_utc"), f"approvals[{index}].decided_at_utc", errors
        )
        if decided_at and requested_at and decided_at < requested_at:
            errors.append(f"approvals[{index}].decided_at_utc must not precede requested_at_utc")
        if decided_at and expires_at and decided_at > expires_at:
            errors.append(f"approvals[{index}].decided_at_utc must not exceed expires_at_utc")
        if approval.get("decision") == "APPROVE" and _non_empty_string(approval.get("approver")):
            approver = str(approval["approver"]).strip()
            approved_by.add(approver)
            if approval.get("capacity") in CONTROL_CAPACITIES:
                control_approvers.add(approver)

    if status == "APPROVED":
        owner = str(record.get("data_owner", "")).strip()
        if has_denial:
            errors.append("APPROVED requests must not contain an unresolved DENY decision")
        if owner not in approved_by:
            errors.append("APPROVED requests require approval by the named data_owner")
        if classification == "STRICTLY_CONFIDENTIAL" and not (control_approvers - {owner}):
            errors.append(
                "STRICTLY_CONFIDENTIAL approval requires the data_owner and a distinct control approver"
            )
        if record.get("decision_reference") == "Pending":
            errors.append("APPROVED requests require a final decision_reference")
        if evaluation_time and expires_at and evaluation_time >= expires_at:
            errors.append("APPROVED request is expired at evaluation_time_utc")

    if status in {"DENIED", "REVOKED"} and any(
        approval.get("decision") == "APPROVE" for approval in approvals if isinstance(approval, dict)
    ):
        # Prior approvals may exist, but the final decision record must explain the terminal state.
        if record.get("decision_reference") == "Pending":
            errors.append(f"{status} requests require a final decision_reference")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an information-access JSON record.")
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--eval-time",
        dest="evaluation_time_utc",
        help="Trusted ISO 8601 evaluation time; defaults to the current UTC time.",
    )
    args = parser.parse_args()
    errors = validate_access_request(
        json.loads(args.path.read_text(encoding="utf-8")), args.evaluation_time_utc
    )
    if errors:
        raise SystemExit("Invalid access request: " + "; ".join(errors))
    print("Access request contract valid; this result does not grant access.")


if __name__ == "__main__":
    main()
