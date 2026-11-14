"""Tests for proportionate AI engineering evidence and tool-reliance decisions."""

import json
from copy import deepcopy

from ai_engineering_evidence import validate_ai_engineering_evidence
from config import TRITON_ROOT


def record() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "AI_ENGINEERING_DECISION_RECORD.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_ai_engineering_evidence(record()) == []

    leaked = record()
    leaked["capture_records"][0]["content"] = "raw prompt must not be embedded"
    assert any("must not embed raw content" in error for error in validate_ai_engineering_evidence(leaked))

    false_hash = record()
    false_hash["execution_identity"]["weights_identity_mode"] = "LOCAL_SHA256"
    false_hash["execution_identity"]["weights_identity_value"] = "invented"
    assert any("LOCAL_SHA256" in error for error in validate_ai_engineering_evidence(false_hash))

    incomplete_detection = record()
    incomplete_detection["tool_reliance"]["independent_error_detection"] = "PARTIAL"
    assert any("requires COMPLETE" in error for error in validate_ai_engineering_evidence(incomplete_detection))

    qualification = record()
    qualification["tool_reliance"]["decision"] = "QUALIFICATION_REQUIRED"
    assert any("requires E2_ASSURANCE_RELIANCE" in error for error in validate_ai_engineering_evidence(qualification))

    premature = deepcopy(record())
    premature["record_status"] = "APPROVED_FOR_DECLARED_USE"
    assert any("completed human review" in error for error in validate_ai_engineering_evidence(premature))

    token_map = record()
    token_map["token_map_reference"] = "GENERAL-AUDIT-LOG"
    assert any("SEPARATE_PROTECTED_VAULT" in error for error in validate_ai_engineering_evidence(token_map))
    print("AI engineering evidence and tool-reliance tests passed.")


if __name__ == "__main__":
    main()
