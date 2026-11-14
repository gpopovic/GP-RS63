"""Validate the frozen Antigravity snapshot and its disposition reconciliation."""

from __future__ import annotations

import json

from config import TRITON_ROOT
from external_review_disposition import validate_external_review_disposition
from external_snapshot_manifest import validate_snapshot_manifest


def main() -> None:
    intake = TRITON_ROOT / "05_Human_Interface_and_Ops" / "External_Review_Intake"
    manifest = json.loads((intake / "ANTIGRAVITY_SOURCE_SNAPSHOT_MANIFEST_2026-08-28.json").read_text(encoding="utf-8"))
    disposition = json.loads((intake / "ANTIGRAVITY_SNAPSHOT_DISPOSITION_REGISTER_2026-08-28.json").read_text(encoding="utf-8"))
    assert validate_snapshot_manifest(manifest) == []
    assert validate_external_review_disposition(disposition) == []
    manifest_ids = set(manifest["disposition_counts"])
    register_ids = {item["id"] for item in disposition["items"]}
    assert manifest_ids == register_ids
    assert sum(manifest["comparison_counts"].values()) == manifest["tracked_file_count"]
    assert sum(manifest["disposition_counts"].values()) == manifest["tracked_file_count"]
    assert disposition["declared_item_count"] == len(register_ids)
    assert manifest["source_commit_time_after_observation"] is True
    assert manifest["comparison_counts"] == {
        "DIVERGENT": 82,
        "EXTERNAL_ONLY": 110,
        "IDENTICAL": 171,
    }
    assert manifest["disposition_counts"] == {
        "AG28-0D0C9276": 1,
        "AG28-2E6D5724": 1,
        "AG28-483D6C31": 1,
        "AG28-86D803A9": 7,
        "AG28-976B9EE4": 3,
        "AG28-A225E298": 67,
        "AG28-AE260432": 92,
        "AG28-AF74947A": 13,
        "AG28-B0338619": 3,
        "AG28-CB0E5689": 4,
        "AG28-IDENTICAL": 171,
    }
    by_id = {item["id"]: item for item in disposition["items"]}
    assert "171 source files" in by_id["AG28-IDENTICAL"]["source_item"]
    assert "Ninety-two" in by_id["AG28-AE260432"]["source_item"]
    print("Antigravity frozen snapshot and disposition reconciliation passed.")


if __name__ == "__main__":
    main()
