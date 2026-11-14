"""Select Triton's smallest adequate execution harness from explicit task risk."""

from __future__ import annotations

from typing import Literal, TypedDict

TaskClass = Literal["ADMIN", "DELIVERY", "CROSS_BORDER_DELIVERY", "CONTROLLED_CHANGE"]
Harness = Literal["LEAN", "STANDARD", "CONTROLLED"]


class HarnessSelection(TypedDict):
    harness: Harness
    role_profile: str
    required_gate: str


def select_harness(task_class: TaskClass, *, material_risk: bool, sensitive_data: bool) -> HarnessSelection:
    """Route high-impact work to controls and ordinary work to the leanest safe path."""
    if material_risk or sensitive_data or task_class == "CONTROLLED_CHANGE":
        return {"harness": "CONTROLLED", "role_profile": "controlled_change", "required_gate": "human accountable approval"}
    if task_class == "ADMIN":
        return {"harness": "LEAN", "role_profile": "lean_delivery", "required_gate": "deterministic validation"}
    if task_class == "CROSS_BORDER_DELIVERY":
        return {"harness": "STANDARD", "role_profile": "indo_german_delivery_cell", "required_gate": "quality and release evidence"}
    return {"harness": "STANDARD", "role_profile": "standard_delivery", "required_gate": "independent quality validation"}
