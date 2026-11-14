"""Validate reproducible test evidence stored in an external product workspace."""

from __future__ import annotations

import json
from pathlib import Path

from project_workspace import workspace_path


REQUIRED_FIELDS = ("workspace_id", "executed_at", "command", "exit_code", "test_output_reference", "reviewer")


def validate_execution_evidence(workspace_id: str, evidence_path: Path) -> list[str]:
    """Return evidence-contract violations; never run an arbitrary command."""
    workspace = workspace_path(workspace_id)
    expected_directory = (workspace / "04_Evidence").resolve()
    candidate = evidence_path.resolve()
    if candidate.parent != expected_directory or candidate.suffix.lower() != ".json":
        return ["evidence must be a JSON file in the workspace 04_Evidence directory"]
    if not candidate.is_file():
        return ["execution evidence does not exist"]
    try:
        evidence = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["execution evidence is not valid JSON"]
    if not isinstance(evidence, dict):
        return ["execution evidence root must be an object"]
    errors = [
        f"missing {field}"
        for field in REQUIRED_FIELDS
        if field not in evidence or evidence[field] in (None, "")
    ]
    if evidence.get("workspace_id") != workspace.name:
        errors.append("workspace_id does not match the external workspace")
    if evidence.get("exit_code") != 0:
        errors.append("test execution did not succeed")
    return errors
