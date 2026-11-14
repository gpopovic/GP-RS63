"""Tests for the AI processing and assurance boundary."""

import json
from copy import deepcopy

from ai_processing_envelope import validate_ai_processing_envelope
from config import TRITON_ROOT


def envelope() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "AI_PROCESSING_ENVELOPE.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_ai_processing_envelope(envelope()) == []

    unpermitted = envelope()
    unpermitted["selected_route"] = "US_EXCEPTION"
    assert "selected_route must be included in permitted_routes" in validate_ai_processing_envelope(unpermitted)

    unmasked = deepcopy(envelope())
    unmasked["sanitisation"]["status"] = "PENDING"
    assert any("external routes require passed sanitisation" in error for error in validate_ai_processing_envelope(unmasked))

    content_log = deepcopy(envelope())
    content_log["logging"]["content_logging"] = True
    assert "non-public processing must not enable content logging in the standard envelope" in validate_ai_processing_envelope(content_log)

    invalid_hash = deepcopy(envelope())
    invalid_hash["source_references"][0]["sha256"] = "sha256:short"
    assert any("sha256 must use" in error for error in validate_ai_processing_envelope(invalid_hash))

    no_gate = deepcopy(envelope())
    no_gate["human_gate"] = {"required": False, "owner": "", "status": "NOT_REQUIRED"}
    assert any("requires a named human gate" in error for error in validate_ai_processing_envelope(no_gate))
    print("AI processing envelope tests passed.")


if __name__ == "__main__":
    main()
