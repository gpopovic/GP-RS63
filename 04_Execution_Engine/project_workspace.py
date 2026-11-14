"""Create and validate external product workspaces without contaminating the Company OS."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Final

from config import PRODUCT_WORKSPACES_ROOT, TRITON_ROOT

WORKSPACE_FOLDERS: Final[tuple[str, ...]] = (
    "01_Inputs",
    "02_Work",
    "03_Outputs",
    "04_Evidence",
    "05_Operations",
    "06_Learning_Exports",
)
MANIFEST_NAME: Final[str] = "workspace_manifest.json"
MANIFEST_SCHEMA_VERSION: Final[str] = "1.0"
REQUIRED_LEARNING_EXPORTS: Final[tuple[str, str]] = (
    "KPI_Export.json",
    "Lessons_Learned.json",
)
COMPANY_OS_BOUNDARY: Final[str] = (
    "Product work remains outside TRITON_ROOT; only approved aggregate KPI and lessons exports return."
)


def normalise_workspace_id(workspace_id: str) -> str:
    """Return a safe, portable workspace identifier."""
    candidate = re.sub(r"[^A-Za-z0-9_-]+", "-", workspace_id.strip()).strip("-")
    if not candidate:
        raise ValueError("Workspace ID must contain letters or digits.")
    return candidate


def workspace_path(workspace_id: str) -> Path:
    """Resolve one workspace below the configured external root."""
    candidate = (PRODUCT_WORKSPACES_ROOT / normalise_workspace_id(workspace_id)).resolve()
    if candidate.parent != PRODUCT_WORKSPACES_ROOT.resolve():
        raise ValueError("Workspace path escapes the configured product-workspace root.")
    if TRITON_ROOT.resolve() in candidate.parents or candidate == TRITON_ROOT.resolve():
        raise ValueError("Product workspaces must remain outside the Triton Company OS.")
    return candidate


def create_workspace(workspace_id: str, purpose: str) -> Path:
    """Create the governed skeleton only when the target does not yet exist."""
    target = workspace_path(workspace_id)
    if target.exists():
        raise FileExistsError(f"Workspace already exists: {target.name}")

    target.mkdir(parents=True)
    for folder in WORKSPACE_FOLDERS:
        (target / folder).mkdir()
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "workspace_id": target.name,
        "purpose": purpose,
        "company_os_boundary": COMPANY_OS_BOUNDARY,
        "required_learning_exports": list(REQUIRED_LEARNING_EXPORTS),
    }
    (target / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return target


def validate_workspace(workspace_id: str) -> list[str]:
    """Return contract violations for a single product workspace."""
    target = workspace_path(workspace_id)
    violations: list[str] = []
    if not target.is_dir():
        return ["workspace does not exist"]
    manifest_path = target / MANIFEST_NAME
    if not manifest_path.is_file():
        violations.append(f"missing {MANIFEST_NAME}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            violations.append(f"invalid {MANIFEST_NAME}")
        else:
            if not isinstance(manifest, dict):
                violations.append(f"invalid {MANIFEST_NAME} root")
            else:
                if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
                    violations.append("unsupported manifest schema_version")
                if manifest.get("workspace_id") != target.name:
                    violations.append("manifest workspace_id does not match folder")
                if not isinstance(manifest.get("purpose"), str) or not manifest["purpose"].strip():
                    violations.append("manifest purpose is missing")
                if manifest.get("company_os_boundary") != COMPANY_OS_BOUNDARY:
                    violations.append("manifest company_os_boundary is invalid")
                if manifest.get("required_learning_exports") != list(REQUIRED_LEARNING_EXPORTS):
                    violations.append("manifest required_learning_exports is invalid")
    for folder in WORKSPACE_FOLDERS:
        if not (target / folder).is_dir():
            violations.append(f"missing folder: {folder}")
    return violations


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage Triton's external product-workspace contract.")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("workspace_id")
    create.add_argument("--purpose", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("workspace_id")
    args = parser.parse_args()

    if args.command == "create":
        print(f"Created external product workspace: {create_workspace(args.workspace_id, args.purpose)}")
        return

    violations = validate_workspace(args.workspace_id)
    if violations:
        raise SystemExit("Workspace contract failed: " + "; ".join(violations))
    print(f"Workspace contract valid: {workspace_path(args.workspace_id)}")


if __name__ == "__main__":
    main()
