"""Tests for the two permitted project-to-Corp learning exports."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from project_learning_export import validate_learning_export


common = {
    "workspace_id": "Ralja_House", "period_start": "2026-08-16", "period_end": "2026-08-16",
    "data_classification": "ANONYMISED_AGGREGATE", "owner": "Project Lead",
    "aggregation_method": "One reviewed package", "evidence_references": ["RALJA-001"],
}
with tempfile.TemporaryDirectory() as temporary_directory:
    folder = Path(temporary_directory)
    kpi = folder / "KPI_Export.json"
    kpi.write_text(json.dumps({**common, "metrics": [{
        "id": "evidence_to_decision_completeness", "definition": "complete decisions / reviewed decisions",
        "value": 1.0, "unit": "ratio", "sample_size": 1, "comparison_scope": "CAD baseline",
        "guardrail_status": "PASS", "action": "Collect baseline",
    }]}), encoding="utf-8")
    assert validate_learning_export(kpi) == []
    lessons = folder / "Lessons_Learned.json"
    lessons.write_text(json.dumps({**common, "lessons": [{
        "id": "RALJA-LL-001", "harness_id": "ralja_existing_house_renovation", "context": "CAD baseline",
        "outcome": "Useful", "contributing_factors": ["evidence register"], "recommendation": "keep",
        "confidence": "MEDIUM", "evidence_references": ["RALJA-001"],
    }]}), encoding="utf-8")
    assert validate_learning_export(lessons) == []

print("Project learning export validator passed.")
