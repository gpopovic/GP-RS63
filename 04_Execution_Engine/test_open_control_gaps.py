"""Tests for durable open findings and evidence-backed closure."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from open_control_gaps import validate_open_control_gaps


def register() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Manual_Quality_Gates" / "OPEN_CONTROL_GAPS_REGISTER.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_open_control_gaps(register()) == []

    false_close = deepcopy(register())
    false_close["findings"][0]["status"] = "CLOSED"
    assert any("CLOSED requires closure_evidence" in error for error in validate_open_control_gaps(false_close))

    active_without_alm = deepcopy(register())
    active_without_alm["findings"][0]["status"] = "IN_PROGRESS"
    active_without_alm["findings"][0]["alm_reference"] = "Not started"
    assert any("active work requires an ALM" in error for error in validate_open_control_gaps(active_without_alm))

    duplicate = deepcopy(register())
    duplicate["findings"][1]["id"] = duplicate["findings"][0]["id"]
    assert any("duplicate finding ID" in error for error in validate_open_control_gaps(duplicate))

    deferred_without_trigger = deepcopy(register())
    deferred_without_trigger["findings"][0].pop("activation_trigger")
    assert any(
        "DEFERRED_UNTIL_TRIGGER requires activation_trigger" in error
        for error in validate_open_control_gaps(deferred_without_trigger)
    )
    print("Open control gap tests passed.")


if __name__ == "__main__":
    main()
