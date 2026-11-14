"""Validate structured, external Germany–India delivery handoff records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FIELDS = ("work_item_id", "version", "outcome", "acceptance_criteria", "data_classification", "baseline_reference", "dependencies", "germany_owner", "india_owner", "handoff_utc", "decision_window_hours", "evidence_plan", "status", "escalation_owner")
ALLOWED_STATUSES = {"READY_FOR_HANDOFF", "IN_PROGRESS", "BLOCKED", "READY_FOR_REVIEW", "ACCEPTED", "REJECTED"}


def validate_handoff(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["handoff must be a JSON object"]
    errors = [f"missing or empty {field}" for field in REQUIRED_FIELDS if not payload.get(field)]
    if payload.get("status") not in ALLOWED_STATUSES:
        errors.append("invalid status")
    if payload.get("status") == "BLOCKED" and not payload.get("dependencies"):
        errors.append("BLOCKED handoff requires dependencies")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate one structured Indo-German handoff JSON file.")
    parser.add_argument("command", choices=("validate",))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_handoff(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Handoff validation failed: " + "; ".join(errors))
    print(f"Handoff valid: {args.path.name}")


if __name__ == "__main__":
    main()
