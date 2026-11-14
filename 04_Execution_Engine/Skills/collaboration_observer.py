"""Assess team and role-interface health for bounded evolution proposals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Recommendation = Literal["KEEP_BASELINE", "PROPOSE_MICRO_TRIAL", "PROPOSE_MAJOR_REDESIGN", "CONTAIN_AND_STRICT_MODE"]


@dataclass(frozen=True)
class CollaborationObservation:
    """One independently reviewed, aggregated collaboration observation."""

    period_id: str
    interface_id: str
    task_class: str
    interface_acceptance_rate: float
    clarification_loop_rate: float
    coordination_rework_ratio: float
    decision_lead_time_hours: float
    defect_escape_rate: float
    sustainable_capacity_ratio: float
    critical_escape: bool
    independent_reviewer: bool


def recommend_collaboration_evolution(observations: list[CollaborationObservation]) -> tuple[Recommendation, str]:
    """Recommend only a reversible trial or human-reviewed redesign; never apply a change."""
    if not observations:
        return "KEEP_BASELINE", "No comparable collaboration evidence exists."
    if any(item.critical_escape for item in observations):
        return "CONTAIN_AND_STRICT_MODE", "A critical cross-role escape requires containment and stricter controls."
    comparable = [
        item for item in observations
        if item.task_class == observations[0].task_class and item.interface_id == observations[0].interface_id
    ]
    if len(comparable) < 3:
        return "KEEP_BASELINE", "Fewer than three comparable observations; continue measurement."
    quality = sum(item.defect_escape_rate > 0 or item.interface_acceptance_rate < 0.85 for item in comparable)
    flow = sum(item.clarification_loop_rate > 0.20 or item.decision_lead_time_hours > 48 for item in comparable)
    workload = sum(item.coordination_rework_ratio > 0.15 or item.sustainable_capacity_ratio > 1.0 for item in comparable)
    categories = sum(signal >= 3 for signal in (quality, flow, workload))
    independent_periods = {item.period_id for item in comparable if item.independent_reviewer}
    if categories >= 2 and len(independent_periods) >= 3:
        return "PROPOSE_MAJOR_REDESIGN", "Repeated independent quality, flow, and workload signals justify a human-reviewed redesign proposal."
    if any(signal >= 3 for signal in (quality, flow, workload)):
        return "PROPOSE_MICRO_TRIAL", "A repeated collaboration issue justifies one reversible micro-trial."
    return "KEEP_BASELINE", "No repeated collaboration signal exceeds the controlled trial threshold."
