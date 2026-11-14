"""Regression checks for the bounded 2026-09-06 Antigravity adaptation."""

from __future__ import annotations

import json

from config import TRITON_ROOT
from external_review_disposition import validate_external_review_disposition


REVIEW_DIR = TRITON_ROOT / "05_Human_Interface_and_Ops" / "External_Review_Intake"
MANIFEST = REVIEW_DIR / "ANTIGRAVITY_INCREMENT_MANIFEST_2026-09-06.json"
REGISTER = REVIEW_DIR / "ANTIGRAVITY_INCREMENTAL_CAPABILITY_DISPOSITION_REGISTER_2026-09-06.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))

    assert manifest["source_repository_kind"] == "GIT_REPOSITORY"
    assert manifest["source_head_at_review"] == "6321998e18ddd2069791b9471089b8560f5849ce"
    assert manifest["source_worktree_status"] == "DIRTY_UNCOMMITTED_INCREMENT"
    assert manifest["changed_path_count"] == len(manifest["files"]) == 4
    assert all(len(item["sha256"]) == 64 for item in manifest["files"])

    assert validate_external_review_disposition(register) == []
    registered_paths = [path for item in register["items"] for path in item["changed_paths"]]
    manifest_paths = [item["path"] for item in manifest["files"]]
    assert register["reviewed_path_count"] == len(registered_paths) == 4
    assert sorted(registered_paths) == sorted(manifest_paths)

    dispositions = {item["id"]: item["disposition"] for item in register["items"]}
    assert dispositions == {
        "AG0906-001": "ADAPTED",
        "AG0906-002": "ADAPTED",
        "AG0906-003": "REFERENCE_ONLY",
        "AG0906-004": "REJECTED_HARMFUL",
    }
    print("Antigravity 2026-09-06 adaptation checks passed.")


if __name__ == "__main__":
    main()
