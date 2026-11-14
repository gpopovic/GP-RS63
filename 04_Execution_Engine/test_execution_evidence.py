"""Tests for product-workspace execution evidence validation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import execution_evidence
import project_workspace


with tempfile.TemporaryDirectory() as temporary_directory:
    temporary_root = Path(temporary_directory)
    with (
        patch.object(project_workspace, "TRITON_ROOT", temporary_root / "triton-corp"),
        patch.object(project_workspace, "PRODUCT_WORKSPACES_ROOT", temporary_root / "product-workspaces"),
        patch.object(execution_evidence, "workspace_path", project_workspace.workspace_path),
    ):
        workspace = project_workspace.create_workspace("pilot", "Controlled pilot")
        evidence = workspace / "04_Evidence" / "execution_evidence.json"
        evidence.write_text(json.dumps({
            "workspace_id": "pilot", "executed_at": "2026-08-15T12:00:00Z",
            "command": "pytest", "exit_code": 0, "test_output_reference": "test-output.txt",
            "reviewer": "Code Validator",
        }), encoding="utf-8")
        assert execution_evidence.validate_execution_evidence("pilot", evidence) == []

print("Execution evidence validator passed.")
