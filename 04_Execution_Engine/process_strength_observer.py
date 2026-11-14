"""Recommend bounded process-strength changes from an explicit task-class quality contract."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Literal

Recommendation = Literal[
    "KEEP_BASELINE",
    "CONTAIN_AND_STRENGTHEN",
    "TIGHTEN_ONE_CONTROL",
    "PROPOSE_BOUNDED_VARIATION",
    "PROPOSE_CONTROL_REDUCTION",
]


@dataclass(frozen=True)
class ProcessQualityContract:
    """Task-class limits selected by accountable humans; no universal thresholds."""

    task_class: str
    control_family: str
    minimum_first_pass_acceptance: float
    maximum_rework_ratio: float
    maximum_escaped_defect_rate: float
    minimum_satisfaction: float
    minimum_evidence_completeness: float
    maximum_cycle_time_hours: float
    maximum_process_wait_ratio: float
    maximum_assurance_cost_ratio: float


@dataclass(frozen=True)
class ProcessObservation:
    """One aggregated, independently reviewable process/output observation."""

    period_id: str
    task_class: str
    control_family: str
    first_pass_acceptance: float
    rework_ratio: float
    escaped_defect_rate: float
    satisfaction: float
    evidence_completeness: float
    cycle_time_hours: float
    process_wait_ratio: float
    assurance_cost_ratio: float
    critical_escape: bool
    mandatory_nonconformity: bool
    independent_reviewer: bool


def _rates_are_valid(contract: ProcessQualityContract, observations: list[ProcessObservation]) -> bool:
    rate_values = [
        contract.minimum_first_pass_acceptance,
        contract.maximum_rework_ratio,
        contract.maximum_escaped_defect_rate,
        contract.minimum_satisfaction,
        contract.minimum_evidence_completeness,
        contract.maximum_process_wait_ratio,
        contract.maximum_assurance_cost_ratio,
    ]
    for item in observations:
        rate_values.extend(
            [
                item.first_pass_acceptance,
                item.rework_ratio,
                item.escaped_defect_rate,
                item.satisfaction,
                item.evidence_completeness,
                item.process_wait_ratio,
                item.assurance_cost_ratio,
            ]
        )
    return all(0.0 <= value <= 1.0 for value in rate_values) and contract.maximum_cycle_time_hours > 0


def recommend_process_strength(
    contract: ProcessQualityContract,
    observations: list[ProcessObservation],
    *,
    exploration_authorised: bool,
) -> tuple[Recommendation, tuple[str, ...]]:
    """Recommend but never apply a process change."""
    if not _rates_are_valid(contract, observations):
        raise ValueError("Process quality contract and observation rates must be within valid ranges.")
    comparable = [
        item
        for item in observations
        if item.task_class == contract.task_class and item.control_family == contract.control_family
    ]
    if any(item.critical_escape or item.mandatory_nonconformity for item in comparable):
        return "CONTAIN_AND_STRENGTHEN", ("critical escape or mandatory nonconformity",)
    if len(comparable) < 3 or len({item.period_id for item in comparable if item.independent_reviewer}) < 3:
        return "KEEP_BASELINE", ("fewer than three comparable independently reviewed periods",)

    averages = {
        "first_pass_acceptance": mean(item.first_pass_acceptance for item in comparable),
        "rework_ratio": mean(item.rework_ratio for item in comparable),
        "escaped_defect_rate": mean(item.escaped_defect_rate for item in comparable),
        "satisfaction": mean(item.satisfaction for item in comparable),
        "evidence_completeness": mean(item.evidence_completeness for item in comparable),
        "cycle_time_hours": mean(item.cycle_time_hours for item in comparable),
        "process_wait_ratio": mean(item.process_wait_ratio for item in comparable),
        "assurance_cost_ratio": mean(item.assurance_cost_ratio for item in comparable),
    }
    quality_breaches = tuple(
        name
        for name, breached in (
            ("first_pass_acceptance", averages["first_pass_acceptance"] < contract.minimum_first_pass_acceptance),
            ("rework_ratio", averages["rework_ratio"] > contract.maximum_rework_ratio),
            ("escaped_defect_rate", averages["escaped_defect_rate"] > contract.maximum_escaped_defect_rate),
            ("satisfaction", averages["satisfaction"] < contract.minimum_satisfaction),
            ("evidence_completeness", averages["evidence_completeness"] < contract.minimum_evidence_completeness),
        )
        if breached
    )
    if quality_breaches:
        return "TIGHTEN_ONE_CONTROL", quality_breaches

    efficiency_breaches = tuple(
        name
        for name, breached in (
            ("cycle_time_hours", averages["cycle_time_hours"] > contract.maximum_cycle_time_hours),
            ("process_wait_ratio", averages["process_wait_ratio"] > contract.maximum_process_wait_ratio),
            ("assurance_cost_ratio", averages["assurance_cost_ratio"] > contract.maximum_assurance_cost_ratio),
        )
        if breached
    )
    if efficiency_breaches and exploration_authorised:
        return "PROPOSE_CONTROL_REDUCTION", efficiency_breaches
    if exploration_authorised:
        return "PROPOSE_BOUNDED_VARIATION", ("quality contract met with authorised exploration",)
    return "KEEP_BASELINE", ("quality contract met; no authorised experiment",)
