"""Recommend task sizing from evidence without mutating harnesses or backlogs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Mode = Literal["FINE_ATOMIC", "STANDARD_SLICE", "MACRO_BATCH"]
Action = Literal["CONTAIN_AND_SPLIT", "SPLIT", "KEEP", "PROPOSE_MERGE_TRIAL"]


@dataclass(frozen=True)
class GranularityRecommendation:
    action: Action
    recommended_mode: Mode
    reasons: tuple[str, ...]
    requires_human_decision: bool
    may_parallelise: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def recommend_granularity(
    *,
    current_mode: Mode,
    comparable_outcomes: list[str],
    material_review_loops: int,
    failed_gate: bool,
    critical_escape: bool,
    high_blast_radius: bool,
    stable_contract: bool,
    independent_lanes: bool,
    write_scope_collision: bool,
) -> GranularityRecommendation:
    """Produce a non-binding recommendation based on controlled policy signals."""
    if material_review_loops < 0:
        raise ValueError("material_review_loops must not be negative")
    allowed_outcomes = {"ACCEPTED", "REWORK", "DEFECT_ESCAPE"}
    if any(outcome not in allowed_outcomes for outcome in comparable_outcomes):
        raise ValueError(f"comparable_outcomes must use {sorted(allowed_outcomes)}")

    parallel = independent_lanes and not write_scope_collision and not high_blast_radius
    if critical_escape:
        return GranularityRecommendation(
            action="CONTAIN_AND_SPLIT",
            recommended_mode="FINE_ATOMIC",
            reasons=("critical escaped defect requires containment and independent review",),
            requires_human_decision=True,
            may_parallelise=False,
        )

    split_reasons: list[str] = []
    if high_blast_radius:
        split_reasons.append("high blast radius")
    if failed_gate:
        split_reasons.append("failed gate")
    if material_review_loops >= 2:
        split_reasons.append("repeated material review loops")
    if write_scope_collision:
        split_reasons.append("parallel lanes would share a write scope")
    if split_reasons:
        return GranularityRecommendation(
            action="SPLIT",
            recommended_mode="FINE_ATOMIC",
            reasons=tuple(split_reasons),
            requires_human_decision=True,
            may_parallelise=False,
        )

    last_three = comparable_outcomes[-3:]
    if (
        len(last_three) == 3
        and all(outcome == "ACCEPTED" for outcome in last_three)
        and stable_contract
        and current_mode != "MACRO_BATCH"
    ):
        return GranularityRecommendation(
            action="PROPOSE_MERGE_TRIAL",
            recommended_mode="MACRO_BATCH",
            reasons=("three comparable accepted packages with a stable contract",),
            requires_human_decision=True,
            may_parallelise=parallel,
        )

    return GranularityRecommendation(
        action="KEEP",
        recommended_mode=current_mode,
        reasons=("insufficient evidence for a controlled sizing change",),
        requires_human_decision=False,
        may_parallelise=parallel,
    )
