"""Tests for the Engineering Flow Logistics plan contract."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from engineering_flow_plan import validate_engineering_flow_plan


def example() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "ENGINEERING_FLOW_PLAN.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_engineering_flow_plan(example()) == []

    assurance = deepcopy(example())
    assurance["process_strength"] = "ASSURANCE"
    assert validate_engineering_flow_plan(assurance) == []

    invented_strength = deepcopy(example())
    invented_strength["process_strength"] = "ENHANCED"
    assert "process_strength is invalid" in validate_engineering_flow_plan(invented_strength)

    unknown_owner = deepcopy(example())
    unknown_owner["flow_owner"] = "Warehouse_Wizard"
    assert any("flow_owner" in error for error in validate_engineering_flow_plan(unknown_owner))

    blind_fifo = deepcopy(example())
    blind_fifo["constrained_resources"][0]["queue_policy"] = "BLIND_FIFO"
    assert any("queue_policy" in error for error in validate_engineering_flow_plan(blind_fifo))

    unsafe_capacity = deepcopy(example())
    unsafe_capacity["constrained_resources"][0]["wip_capacity"] = 0
    assert any("wip_capacity" in error for error in validate_engineering_flow_plan(unsafe_capacity))

    self_dependency = deepcopy(example())
    self_dependency["dependency_edges"][0]["successor"] = "INTERFACE-CONTRACT-001"
    assert any("self-dependency" in error for error in validate_engineering_flow_plan(self_dependency))

    false_release = deepcopy(example())
    false_release["current_state"] = "RELEASED"
    assert any("release manifest" in error for error in validate_engineering_flow_plan(false_release))

    missing_recovery = deepcopy(example())
    missing_recovery["failure_strategy"]["prevalidated_rollback_reference"] = ""
    assert any("prevalidated_rollback_reference" in error for error in validate_engineering_flow_plan(missing_recovery))
    print("Engineering flow logistics plan tests passed.")


if __name__ == "__main__":
    main()
