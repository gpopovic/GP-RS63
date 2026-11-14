"""Choose Triton's minimum adequate model class without selecting a provider."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from config import TRITON_ROOT

ModelClass = Literal["FLAGSHIP", "STANDARD", "WORKER"]
TaskType = Literal["ROUTINE", "COMPLEX", "FINAL_REVIEW"]
REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "MODEL_CLASS_REGISTRY.json"


@dataclass(frozen=True)
class ModelClassRoute:
    """A class recommendation; provider and data-route selection stay separate."""

    model_class: ModelClass
    requires_approved_data_route: bool
    requires_human_gate: bool
    reason: str


def load_model_class_registry() -> dict[str, object]:
    """Load the controlled classification criteria and reject incomplete classes."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    classes = registry.get("classes")
    if registry.get("schema_version") != "1.0" or not isinstance(classes, dict):
        raise ValueError("Model class registry has an invalid schema.")
    if set(classes) != {"FLAGSHIP", "STANDARD", "WORKER"}:
        raise ValueError("Model class registry must define exactly three classes.")
    for model_class, definition in classes.items():
        if not isinstance(definition, dict) or not definition.get("permitted_work") or not definition.get("triton_acceptance"):
            raise ValueError(f"Model class registry has an incomplete class: {model_class}")
    candidates = registry.get("candidate_models")
    if not isinstance(candidates, list):
        raise ValueError("Model class registry must contain a candidate-model list.")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Model class registry has an invalid candidate.")
        required = {"id", "model_identifier", "processing_route", "proposed_class", "admission_status", "declared_strengths", "declared_limits"}
        if not required <= set(candidate) or candidate["proposed_class"] not in classes:
            raise ValueError("Model class registry has an incomplete candidate.")
    return registry


def require_admitted_model(model_identifier: str, required_class: ModelClass) -> dict[str, object]:
    """Return one explicitly admitted candidate or fail before an unapproved live call."""
    registry = load_model_class_registry()
    candidates = registry["candidate_models"]
    matches = [
        candidate for candidate in candidates
        if candidate["model_identifier"] == model_identifier
    ]
    if len(matches) != 1:
        raise ValueError(f"Model is not registered for live routing: {model_identifier}")
    candidate = matches[0]
    if candidate["admission_status"] != "ADMITTED":
        raise ValueError(f"Model is not admitted for live routing: {model_identifier}")
    if candidate.get("assigned_class") != required_class:
        raise ValueError(
            f"Model {model_identifier} is not admitted as required class {required_class}."
        )
    return candidate


def select_model_class(
    task_type: TaskType,
    *,
    material_risk: bool,
    sensitive_data: bool,
) -> ModelClassRoute:
    """Return the lowest adequate class and make risk-driven gates explicit."""
    load_model_class_registry()
    if material_risk or task_type == "FINAL_REVIEW":
        model_class: ModelClass = "FLAGSHIP"
        reason = "Material consequence or final review requires the flagship evidence threshold."
    elif task_type == "COMPLEX":
        model_class = "STANDARD"
        reason = "Complex work needs the standard evidence threshold and independent review path."
    elif task_type == "ROUTINE":
        model_class = "WORKER"
        reason = "Routine bounded work may use the worker class with its deterministic checks."
    else:
        raise ValueError(f"Unknown model task type: {task_type}")
    return ModelClassRoute(
        model_class=model_class,
        requires_approved_data_route=sensitive_data,
        requires_human_gate=material_risk or sensitive_data,
        reason=reason,
    )
