"""Validate sanitised project-to-Corp learning exports without importing project artefacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


COMMON_FIELDS = ("workspace_id", "period_start", "period_end", "data_classification", "owner", "aggregation_method", "evidence_references")
ALLOWED_DATA_CLASSES = {"PUBLIC", "SYNTHETIC", "ANONYMISED_AGGREGATE"}
METRIC_FIELDS = ("id", "definition", "value", "unit", "sample_size", "comparison_scope", "guardrail_status", "action")
LESSON_FIELDS = ("id", "harness_id", "context", "outcome", "contributing_factors", "recommendation", "confidence", "evidence_references")


def missing_fields(item: object, fields: tuple[str, ...]) -> list[str]:
    if not isinstance(item, dict):
        return ["entry is not an object"]
    return [field for field in fields if field not in item or item[field] in (None, "", [])]


def validate_learning_export(path: Path) -> list[str]:
    """Return structural privacy and completeness errors for one permitted export type."""
    if path.name not in {"KPI_Export.json", "Lessons_Learned.json"}:
        return ["export file must be named KPI_Export.json or Lessons_Learned.json"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["export is not valid JSON"]
    errors = [f"missing {field}" for field in missing_fields(payload, COMMON_FIELDS)]
    if isinstance(payload, dict) and payload.get("data_classification") not in ALLOWED_DATA_CLASSES:
        errors.append("data_classification is not permitted for Corp learning export")
    collection_name = "metrics" if path.name == "KPI_Export.json" else "lessons"
    fields = METRIC_FIELDS if collection_name == "metrics" else LESSON_FIELDS
    entries = payload.get(collection_name) if isinstance(payload, dict) else None
    if not isinstance(entries, list) or not entries:
        errors.append(f"missing {collection_name}")
    else:
        for index, entry in enumerate(entries, start=1):
            errors.extend(f"{collection_name}[{index}] missing {field}" for field in missing_fields(entry, fields))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a sanitised Triton project learning export.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_learning_export(args.path)
    if errors:
        raise SystemExit("Learning export failed: " + "; ".join(errors))
    print(f"Learning export valid: {args.path.name}")


if __name__ == "__main__":
    main()
