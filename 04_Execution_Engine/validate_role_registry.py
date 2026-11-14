"""Validate that Triton's organisation registry covers every canonical instruction."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import COACHES_DIR, CORE_ASSISTANTS_DIR, ROLES_DIR, TRITON_ROOT

ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"


def registered_members() -> set[str]:
    """Return every unique member indexed by the organisation registry."""
    payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    members = [member for department in payload["departments"] for member in department["members"]]
    if len(members) != len(set(members)):
        raise ValueError("A registry member is assigned to more than one department.")
    return set(members)


def canonical_members() -> set[str]:
    """Return every canonical role, core assistant, and coach filename stem."""
    directories = (ROLES_DIR, CORE_ASSISTANTS_DIR, COACHES_DIR)
    return {path.stem for directory in directories for path in directory.glob("*.md")}


def main() -> None:
    expected = canonical_members()
    registered = registered_members()
    missing = sorted(expected - registered)
    unknown = sorted(registered - expected)
    if missing or unknown:
        if missing:
            print(f"Unregistered canonical members: {', '.join(missing)}")
        if unknown:
            print(f"Registry members without an instruction file: {', '.join(unknown)}")
        raise SystemExit(1)
    print(f"Role registry valid: {len(registered)} canonical members across all departments.")


if __name__ == "__main__":
    main()
