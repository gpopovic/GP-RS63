"""Load and validate Triton's configured, cost-bounded workflow harnesses."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from config import TRITON_ROOT

WorkflowId = Literal[
    "discovery", "coding", "architecture", "regulated_engineering", "built_environment", "service_operation"
]
CATALOG_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ADAPTIVE_HARNESS_CATALOG.json"
ROLE_PROFILES_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ACTIVE_ROLE_PROFILES.json"
ROLE_REGISTRY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "ROLE_REGISTRY.json"


@dataclass(frozen=True)
class AdaptiveHarnessPlan:
    """A validated execution plan without provider-specific pricing assumptions."""

    workflow_id: WorkflowId
    role_profile: str
    maximum_parallel_lanes: int
    maximum_model_calls_before_gate: int
    requires_cost_preflight: bool
    requires_human_approval: bool
    stages: tuple[dict[str, Any], ...]


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    """Load the controlled catalog and reject malformed operational configuration."""
    catalog = json.loads(path.read_text(encoding="utf-8"))
    controls = catalog.get("global_controls")
    workflows = catalog.get("workflows")
    if catalog.get("schema_version") != "1.0" or not isinstance(controls, dict) or not isinstance(workflows, dict):
        raise ValueError("Adaptive harness catalog has an invalid schema.")
    if not isinstance(controls.get("max_parallel_lanes"), int) or controls["max_parallel_lanes"] < 1:
        raise ValueError("Adaptive harness catalog needs a positive parallel-lane limit.")
    if not isinstance(controls.get("max_model_calls_per_lane"), int) or controls["max_model_calls_per_lane"] < 0:
        raise ValueError("Adaptive harness catalog needs a non-negative lane model-call limit.")
    if not isinstance(controls.get("synthesis_model_calls"), int) or controls["synthesis_model_calls"] < 0:
        raise ValueError("Adaptive harness catalog needs a non-negative synthesis model-call limit.")
    role_profiles = json.loads(ROLE_PROFILES_PATH.read_text(encoding="utf-8")).get("profiles", {})
    role_registry = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
    canonical_roles = {
        role
        for department in role_registry.get("departments", [])
        for role in department.get("members", [])
    }
    for workflow_id, workflow in workflows.items():
        if not isinstance(workflow, dict) or workflow.get("role_profile") not in role_profiles:
            raise ValueError(f"Adaptive harness has an unknown role profile: {workflow_id}")
        stages = workflow.get("stages")
        if not isinstance(stages, list) or not stages:
            raise ValueError(f"Adaptive harness has no stages: {workflow_id}")
        for stage in stages:
            if not isinstance(stage, dict) or stage.get("mode") not in {"sequential", "parallel", "gate"}:
                raise ValueError(f"Adaptive harness has an invalid stage: {workflow_id}")
            accountable_role = stage.get("accountable_role")
            if accountable_role is not None and accountable_role not in canonical_roles:
                raise ValueError(f"Adaptive harness has an unknown accountable role: {workflow_id}.{stage.get('id')}")
            if stage["mode"] == "parallel":
                lanes = stage.get("lanes")
                if not isinstance(lanes, list) or not lanes or len(lanes) > controls["max_parallel_lanes"]:
                    raise ValueError(f"Adaptive harness exceeds the parallel-lane limit: {workflow_id}")
                for lane in lanes:
                    roles = lane.get("roles") if isinstance(lane, dict) else None
                    if not isinstance(roles, list) or not roles or any(role not in canonical_roles for role in roles):
                        raise ValueError(f"Adaptive harness has an unknown lane role: {workflow_id}.{stage.get('id')}")
    return catalog


def select_adaptive_harness(
    workflow_id: WorkflowId,
    *,
    material_risk: bool,
    sensitive_data: bool,
) -> AdaptiveHarnessPlan:
    """Select one configured workflow and strengthen its approval route when needed."""
    catalog = load_catalog()
    workflow = catalog["workflows"].get(workflow_id)
    if not isinstance(workflow, dict):
        raise ValueError(f"Unknown adaptive workflow: {workflow_id}")
    stages = workflow.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError(f"Adaptive workflow has no stages: {workflow_id}")
    controls = catalog["global_controls"]
    lanes = max(
        (len(stage.get("lanes", [])) for stage in stages if stage.get("mode") == "parallel"),
        default=0,
    )
    maximum_parallel_lanes = min(lanes, controls["max_parallel_lanes"])
    maximum_model_calls = maximum_parallel_lanes * controls["max_model_calls_per_lane"] + controls["synthesis_model_calls"]
    return AdaptiveHarnessPlan(
        workflow_id=workflow_id,
        role_profile=str(workflow["role_profile"]),
        maximum_parallel_lanes=maximum_parallel_lanes,
        maximum_model_calls_before_gate=maximum_model_calls,
        requires_cost_preflight=maximum_model_calls > 0,
        requires_human_approval=material_risk or sensitive_data,
        stages=tuple(stages),
    )
