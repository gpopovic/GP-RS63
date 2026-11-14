"""Validate the open Company OS control-finding register without acting as an ALM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PRIORITIES = {"P0", "P1", "P2", "P3"}
STATUSES = {
    "OPEN", "IN_PROGRESS", "BLOCKED", "CLOSED", "ACCEPTED_RISK",
    "DEFERRED_UNTIL_TRIGGER",
}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_open_control_gaps(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["open control gaps register must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not _non_empty(payload.get("purpose")) or not _non_empty(payload.get("last_reviewed")):
        errors.append("purpose and last_reviewed must be non-empty strings")
    findings = payload.get("findings")
    if not isinstance(findings, list) or not findings:
        return errors + ["findings must be a non-empty list"]
    seen: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        for field in ("id", "area", "finding", "owner", "acceptance", "alm_reference", "source"):
            if not _non_empty(finding.get(field)):
                errors.append(f"findings[{index}].{field} must be a non-empty string")
        finding_id = finding.get("id")
        if _non_empty(finding_id):
            if finding_id in seen:
                errors.append(f"duplicate finding ID: {finding_id}")
            seen.add(str(finding_id))
        if finding.get("priority") not in PRIORITIES:
            errors.append(f"findings[{index}].priority must be one of {sorted(PRIORITIES)}")
        status = finding.get("status")
        if status not in STATUSES:
            errors.append(f"findings[{index}].status must be one of {sorted(STATUSES)}")
        if status in {"CLOSED", "ACCEPTED_RISK"} and not _non_empty(finding.get("closure_evidence")):
            errors.append(f"findings[{index}] {status} requires closure_evidence")
        if status == "DEFERRED_UNTIL_TRIGGER" and not _non_empty(finding.get("activation_trigger")):
            errors.append(f"findings[{index}] DEFERRED_UNTIL_TRIGGER requires activation_trigger")
        if status in {"IN_PROGRESS", "BLOCKED"} and str(finding.get("alm_reference", "")).strip().lower() == "not started":
            errors.append(f"findings[{index}] active work requires an ALM or outage-fallback reference")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Company OS open-control-gap register.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_open_control_gaps(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid open control gaps register: " + "; ".join(errors))
    print("Open control gaps register valid; open findings are not completion claims.")


if __name__ == "__main__":
    main()
