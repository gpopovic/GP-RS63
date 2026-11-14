"""Contract tests for isolated Triton product workspaces."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import project_workspace


class ProductWorkspaceTests(unittest.TestCase):
    """Verify that the Company OS cannot silently host product work."""

    def test_normalise_workspace_id_is_portable(self) -> None:
        self.assertEqual(project_workspace.normalise_workspace_id(" Pilot / One "), "Pilot-One")
        with self.assertRaises(ValueError):
            project_workspace.normalise_workspace_id("///")

    def test_create_and_validate_external_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            product_root = temporary_root / "product-workspaces"
            with (
                patch.object(project_workspace, "TRITON_ROOT", temporary_root / "company-os"),
                patch.object(project_workspace, "PRODUCT_WORKSPACES_ROOT", product_root),
            ):
                workspace = project_workspace.create_workspace("Pilot / One", "Controlled pilot")
                self.assertEqual(workspace.parent, product_root.resolve())
                self.assertEqual(project_workspace.validate_workspace("Pilot / One"), [])
                manifest = json.loads((workspace / project_workspace.MANIFEST_NAME).read_text(encoding="utf-8"))
                self.assertEqual(manifest["workspace_id"], "Pilot-One")
                self.assertEqual(manifest["required_learning_exports"], list(project_workspace.REQUIRED_LEARNING_EXPORTS))

    def test_validate_reports_manifest_contract_violations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            product_root = temporary_root / "product-workspaces"
            with (
                patch.object(project_workspace, "TRITON_ROOT", temporary_root / "company-os"),
                patch.object(project_workspace, "PRODUCT_WORKSPACES_ROOT", product_root),
            ):
                workspace = project_workspace.create_workspace("pilot", "Controlled pilot")
                manifest_path = workspace / project_workspace.MANIFEST_NAME
                manifest_path.write_text("{}", encoding="utf-8")
                violations = project_workspace.validate_workspace("pilot")
                self.assertIn("unsupported manifest schema_version", violations)
                self.assertIn("manifest workspace_id does not match folder", violations)
                self.assertIn("manifest purpose is missing", violations)
                self.assertIn("manifest company_os_boundary is invalid", violations)
                self.assertIn("manifest required_learning_exports is invalid", violations)

    def test_workspace_root_inside_company_os_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            company_root = Path(temporary_directory) / "company-os"
            with (
                patch.object(project_workspace, "TRITON_ROOT", company_root),
                patch.object(project_workspace, "PRODUCT_WORKSPACES_ROOT", company_root / "workspaces"),
            ):
                with self.assertRaisesRegex(ValueError, "outside the Triton Company OS"):
                    project_workspace.workspace_path("pilot")


if __name__ == "__main__":
    unittest.main()
