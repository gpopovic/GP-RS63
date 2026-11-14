"""Validate role meeting requests without scheduling or notifying externally."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import TRITON_ROOT

ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"
MEETING_CATALOG_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "VIRTUAL_MEETING_CATALOG.json"
URGENCIES = {"IMMEDIATE", "TODAY", "NEXT_7_DAYS", "ROUTINE"}
STATUSES = {"PROPOSED", "ASYNC_REDIRECTED", "APPROVED_TO_SCHEDULE", "SCHEDULED", "DECLINED", "CLOSED"}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _timestamp(value: object) -> bool:
    if not _non_empty(value):
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _controlled_roles() -> set[str]:
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {role for department in payload.get("departments", []) for role in department.get("members", [])}


def _controlled_meetings() -> set[str]:
    payload = json.loads(MEETING_CATALOG_PATH.read_text(encoding="utf-8"))
    return {str(item["id"]) for item in payload.get("meetings", [])}


def validate_meeting_request_register(payload: object) -> list[str]:
    """Return contract errors; a valid request is not calendar or founder approval."""
    if not isinstance(payload, dict):
        return ["meeting request register must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in ("register_id", "source_of_truth"):
        if not _non_empty(payload.get(field)):
            errors.append(f"{field} must be a non-empty string")
    requests = payload.get("requests")
    if not isinstance(requests, list):
        return errors + ["requests must be a list"]
    roles = _controlled_roles()
    meetings = _controlled_meetings()
    seen: set[str] = set()
    for index, item in enumerate(requests):
        if not isinstance(item, dict):
            errors.append(f"requests[{index}] must be an object")
            continue
        for field in (
            "request_id", "decision_question", "reason_async_insufficient", "consequence_if_deferred",
            "calendar_reference", "alm_reference",
        ):
            if not _non_empty(item.get(field)):
                errors.append(f"requests[{index}].{field} must be a non-empty string")
        request_id = item.get("request_id")
        if _non_empty(request_id):
            if request_id in seen:
                errors.append(f"duplicate request_id: {request_id}")
            seen.add(str(request_id))
        for field in ("created_at_utc", "decision_deadline_utc"):
            if not _timestamp(item.get(field)):
                errors.append(f"requests[{index}].{field} must be a timezone-aware ISO timestamp")
        requester = item.get("requested_by_role")
        chair = item.get("proposed_chair")
        if requester not in roles:
            errors.append(f"requests[{index}].requested_by_role is not canonical")
        if chair not in roles:
            errors.append(f"requests[{index}].proposed_chair is not canonical")
        meeting_id = item.get("proposed_meeting_id")
        if meeting_id not in meetings:
            errors.append(f"requests[{index}].proposed_meeting_id is not controlled")
        participants = item.get("minimum_participants")
        observers = item.get("observers")
        if not isinstance(participants, list) or not participants or len(participants) > 8 or any(role not in roles for role in participants):
            errors.append(f"requests[{index}].minimum_participants must contain 1-8 canonical roles")
        if not isinstance(observers, list) or any(role not in roles for role in observers):
            errors.append(f"requests[{index}].observers must be a canonical-role list")
        if isinstance(participants, list) and isinstance(observers, list) and set(participants) & set(observers):
            errors.append(f"requests[{index}] active participants and observers must be distinct")
        evidence = item.get("evidence_references")
        if not isinstance(evidence, list) or not evidence or not all(_non_empty(value) for value in evidence):
            errors.append(f"requests[{index}].evidence_references must be a non-empty string list")
        duration = item.get("duration_minutes_cap")
        calls = item.get("model_call_cap")
        if isinstance(duration, bool) or not isinstance(duration, int) or not 5 <= duration <= 120:
            errors.append(f"requests[{index}].duration_minutes_cap must be 5-120")
        if isinstance(calls, bool) or not isinstance(calls, int) or not 0 <= calls <= 7:
            errors.append(f"requests[{index}].model_call_cap must be 0-7")
        urgency = item.get("urgency")
        status = item.get("status")
        if urgency not in URGENCIES:
            errors.append(f"requests[{index}].urgency is invalid")
        if status not in STATUSES:
            errors.append(f"requests[{index}].status is invalid")
        if not isinstance(item.get("founder_attention_required"), bool):
            errors.append(f"requests[{index}].founder_attention_required must be boolean")
        if urgency in {"IMMEDIATE", "TODAY"} and item.get("founder_attention_required") is not True:
            errors.append(f"requests[{index}] immediate or today urgency requires founder attention")
        if status == "SCHEDULED" and str(item.get("calendar_reference", "")).upper() == "NOT_SCHEDULED":
            errors.append(f"requests[{index}] scheduled status requires a calendar reference")
        if item.get("data_classification") not in CLASSIFICATIONS:
            errors.append(f"requests[{index}].data_classification is invalid")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a meeting request register.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_meeting_request_register(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid meeting request register: " + "; ".join(errors))
    print("Meeting request register valid; scheduling and notification remain separate human-authorised actions.")


if __name__ == "__main__":
    main()
