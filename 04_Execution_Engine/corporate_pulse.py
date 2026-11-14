"""Validate and render a sourced corporate pulse without inventing state."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import TRITON_ROOT

CATEGORIES = {"FACT", "ASSUMPTION", "RECOMMENDATION", "DECISION_NEEDED", "QUESTION"}
SOURCE_TYPES = {"CONTROLLED_CORP_RECORD", "SANITISED_PROJECT_EXPORT"}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
REQUIRED_FIELDS = (
    "statement_id",
    "category",
    "statement",
    "evidence_reference",
    "source_type",
    "observed_at_utc",
    "owner",
    "confidence",
    "data_classification",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _timestamp(value: object) -> bool:
    if not _text(value):
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _valid_corp_reference(reference: str) -> bool:
    candidate = (TRITON_ROOT / reference).resolve()
    try:
        candidate.relative_to(TRITON_ROOT.resolve())
    except ValueError:
        return False
    return candidate.is_file()


def validate_statement(statement: object) -> list[str]:
    if not isinstance(statement, dict):
        return ["statement must be an object"]
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in statement:
            errors.append(f"missing field: {field}")
    for field in ("statement_id", "statement", "evidence_reference", "owner"):
        if field in statement and not _text(statement[field]):
            errors.append(f"{field} must be a non-empty string")
    if statement.get("category") not in CATEGORIES:
        errors.append(f"category must be one of {sorted(CATEGORIES)}")
    if statement.get("source_type") not in SOURCE_TYPES:
        errors.append(f"source_type must be one of {sorted(SOURCE_TYPES)}")
    if statement.get("confidence") not in CONFIDENCE:
        errors.append(f"confidence must be one of {sorted(CONFIDENCE)}")
    if statement.get("data_classification") not in CLASSIFICATIONS:
        errors.append(f"data_classification must be one of {sorted(CLASSIFICATIONS)}")
    if not _timestamp(statement.get("observed_at_utc")):
        errors.append("observed_at_utc must be a timezone-aware ISO 8601 timestamp")
    if (
        statement.get("source_type") == "CONTROLLED_CORP_RECORD"
        and _text(statement.get("evidence_reference"))
        and not _valid_corp_reference(str(statement["evidence_reference"]))
    ):
        errors.append("CONTROLLED_CORP_RECORD evidence_reference must identify an existing Corp file")
    if statement.get("source_type") == "SANITISED_PROJECT_EXPORT" and not _text(
        statement.get("export_validation_reference")
    ):
        errors.append("SANITISED_PROJECT_EXPORT requires export_validation_reference")
    return errors


def build_pulse(statements: object) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    """Return valid statements grouped by category and indexed validation errors."""
    if not isinstance(statements, list):
        return {}, ["pulse input must be a list"]
    grouped = {category: [] for category in sorted(CATEGORIES)}
    errors: list[str] = []
    seen: set[str] = set()
    for index, statement in enumerate(statements):
        item_errors = validate_statement(statement)
        if isinstance(statement, dict) and statement.get("statement_id") in seen:
            item_errors.append("duplicate statement_id")
        if item_errors:
            errors.extend(f"statements[{index}]: {error}" for error in item_errors)
            continue
        assert isinstance(statement, dict)
        seen.add(str(statement["statement_id"]))
        grouped[str(statement["category"])].append(dict(statement))
    for items in grouped.values():
        items.sort(key=lambda item: (item["observed_at_utc"], item["statement_id"]), reverse=True)
    return grouped, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a sourced, non-authoritative corporate pulse.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    grouped, errors = build_pulse(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid pulse input: " + "; ".join(errors))
    print(json.dumps(grouped, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
