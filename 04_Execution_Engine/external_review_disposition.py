"""Validate external-review dispositions and prohibit silent proposal loss."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DISPOSITIONS = {
    "ACCEPTED", "ADAPTED", "SUPERSEDED", "DUPLICATE", "DEFERRED",
    "REJECTED_HARMFUL", "NEEDS_EVIDENCE", "REFERENCE_ONLY",
}
COMPLETENESS = {"COMPLETE", "NEEDS_EVIDENCE"}
TARGET_DISPOSITIONS = {"ACCEPTED", "ADAPTED", "SUPERSEDED", "DUPLICATE"}
OPEN_DISPOSITIONS = {"DEFERRED", "NEEDS_EVIDENCE"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_external_review_disposition(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["external review disposition must be a JSON object"]
    record: dict[str, Any] = payload
    errors: list[str] = []
    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in (
        "review_id", "source_type", "source_reference", "source_manifest_reference",
        "review_owner", "independent_reviewer", "review_date",
    ):
        if not _non_empty(record.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if record.get("review_owner") == record.get("independent_reviewer"):
        errors.append("independent_reviewer must differ from review_owner")
    completeness = record.get("intake_completeness")
    if completeness not in COMPLETENESS:
        errors.append(f"intake_completeness must be one of {sorted(COMPLETENESS)}")
    items = record.get("items")
    if not isinstance(items, list) or not items:
        return errors + ["items must be a non-empty list"]
    declared_count = record.get("declared_item_count")
    if isinstance(declared_count, bool) or not isinstance(declared_count, int) or declared_count != len(items):
        errors.append("declared_item_count must equal the number of disposition items")

    seen_ids: set[str] = set()
    needs_evidence_count = 0
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] must be an object")
            continue
        for field in (
            "id", "source_item", "intent", "disposition", "rationale", "protected_outcome",
            "capability_coverage", "authoritative_target", "verification_reference", "owner",
            "follow_up_trigger",
        ):
            if not _non_empty(item.get(field)):
                errors.append(f"items[{index}].{field} must be a non-empty string")
        item_id = item.get("id")
        if _non_empty(item_id):
            if item_id in seen_ids:
                errors.append(f"duplicate disposition ID: {item_id}")
            seen_ids.add(str(item_id))
        disposition = item.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"items[{index}].disposition must be one of {sorted(DISPOSITIONS)}")
            continue
        if disposition == "NEEDS_EVIDENCE":
            needs_evidence_count += 1
        if disposition in TARGET_DISPOSITIONS:
            if str(item.get("capability_coverage", "")).upper() in {"OPEN", "NONE", "UNKNOWN"}:
                errors.append(f"items[{index}] cannot close with open capability coverage")
        if disposition == "REJECTED_HARMFUL":
            coverage = str(item.get("capability_coverage", "")).upper()
            target = str(item.get("authoritative_target", "")).strip()
            if not target and coverage != "NOT_REQUIRED_WITH_REASON":
                errors.append(f"items[{index}] harmful rejection requires a safer target or NOT_REQUIRED_WITH_REASON")
        if disposition in OPEN_DISPOSITIONS and str(item.get("follow_up_trigger", "")).strip().lower() in {
            "", "pending", "none", "not applicable",
        }:
            errors.append(f"items[{index}] open disposition requires a concrete follow_up_trigger")

    if completeness == "COMPLETE" and needs_evidence_count:
        errors.append("COMPLETE intake must not contain NEEDS_EVIDENCE dispositions")
    if completeness == "NEEDS_EVIDENCE" and needs_evidence_count == 0:
        errors.append("NEEDS_EVIDENCE intake requires at least one matching disposition")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an external-review disposition register.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_external_review_disposition(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid external review disposition: " + "; ".join(errors))
    print("External review disposition valid; unresolved items remain open until their evidence closes.")


if __name__ == "__main__":
    main()
