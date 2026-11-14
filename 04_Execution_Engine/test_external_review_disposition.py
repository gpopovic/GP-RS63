"""Tests for no-silent-drop external review intake."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from external_review_disposition import validate_external_review_disposition


def register() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "External_Review_Intake" / "ANTIGRAVITY_DISPOSITION_REGISTER_2026-08-21.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    register_dir = TRITON_ROOT / "05_Human_Interface_and_Ops" / "External_Review_Intake"
    controlled_registers = sorted(register_dir.glob("*_DISPOSITION_REGISTER_*.json"))
    assert len(controlled_registers) >= 2
    for path in controlled_registers:
        controlled = json.loads(path.read_text(encoding="utf-8"))
        assert validate_external_review_disposition(controlled) == []
        if "reviewed_path_count" in controlled:
            reviewed_paths = [
                changed_path
                for item in controlled["items"]
                for changed_path in item.get("changed_paths", [])
            ]
            assert len(reviewed_paths) == controlled["reviewed_path_count"]
            assert len(set(reviewed_paths)) == len(reviewed_paths)

    assert validate_external_review_disposition(register()) == []

    missing_item = register()
    missing_item["items"] = missing_item["items"][:-1]
    assert "declared_item_count must equal the number of disposition items" in validate_external_review_disposition(missing_item)

    generic_rejection = deepcopy(register())
    generic_rejection["items"][0]["disposition"] = "REJECTED"
    assert any("disposition must be one of" in error for error in validate_external_review_disposition(generic_rejection))

    false_closure = deepcopy(register())
    false_closure["intake_completeness"] = "COMPLETE"
    assert "COMPLETE intake must not contain NEEDS_EVIDENCE dispositions" in validate_external_review_disposition(false_closure)

    missing_trigger = deepcopy(register())
    missing_trigger["items"][-1]["follow_up_trigger"] = "Pending"
    assert any("open disposition requires a concrete" in error for error in validate_external_review_disposition(missing_trigger))
    print("External review disposition tests passed.")


if __name__ == "__main__":
    main()
