"""Evidence-backed creative option exploration and Pareto analysis."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable, Literal

Direction = Literal["MINIMISE", "MAXIMISE"]


@dataclass(frozen=True)
class Objective:
    objective_id: str
    direction: Direction
    unit: str
    source_reference: str


@dataclass(frozen=True)
class ConstraintEvidence:
    constraint_id: str
    satisfied: bool
    evidence_reference: str


@dataclass(frozen=True)
class OptionCandidate:
    option_id: str
    name: str
    measurements: tuple[tuple[str, str], ...]
    constraints: tuple[ConstraintEvidence, ...]
    evidence_references: tuple[str, ...]


@dataclass(frozen=True)
class RejectedOption:
    option_id: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class OptionAnalysis:
    decision_question: str
    human_decision_owner: str
    admissible_option_ids: tuple[str, ...]
    rejected_options: tuple[RejectedOption, ...]
    pareto_front_option_ids: tuple[str, ...]
    human_decision_required: bool = True


def _required_text(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must be a non-empty string")
    return cleaned


def _measurement_map(candidate: OptionCandidate, objectives: tuple[Objective, ...]) -> dict[str, Decimal]:
    raw = dict(candidate.measurements)
    if len(raw) != len(candidate.measurements):
        raise ValueError(f"option {candidate.option_id} has duplicate measurement IDs")
    required = {objective.objective_id for objective in objectives}
    if set(raw) != required:
        raise ValueError(f"option {candidate.option_id} measurements must exactly match declared objectives")
    values: dict[str, Decimal] = {}
    for objective_id, value in raw.items():
        try:
            decimal_value = Decimal(value)
        except (InvalidOperation, ValueError) as error:
            raise ValueError(f"option {candidate.option_id} has invalid value for {objective_id}") from error
        if not decimal_value.is_finite():
            raise ValueError(f"option {candidate.option_id} has non-finite value for {objective_id}")
        values[objective_id] = decimal_value
    return values


def _dominates(
    left: dict[str, Decimal],
    right: dict[str, Decimal],
    objectives: tuple[Objective, ...],
) -> bool:
    no_worse = True
    strictly_better = False
    for objective in objectives:
        left_value = left[objective.objective_id]
        right_value = right[objective.objective_id]
        if objective.direction == "MINIMISE":
            no_worse = no_worse and left_value <= right_value
            strictly_better = strictly_better or left_value < right_value
        else:
            no_worse = no_worse and left_value >= right_value
            strictly_better = strictly_better or left_value > right_value
    return no_worse and strictly_better


def analyse_options(
    *,
    decision_question: str,
    human_decision_owner: str,
    objectives: Iterable[Objective],
    required_constraint_ids: Iterable[str],
    candidates: Iterable[OptionCandidate],
) -> OptionAnalysis:
    """Return admissibility and the genuine non-dominated option set."""
    question = _required_text(decision_question, "decision_question")
    owner = _required_text(human_decision_owner, "human_decision_owner")
    objective_list = tuple(objectives)
    candidate_list = tuple(candidates)
    constraint_ids = tuple(_required_text(item, "required_constraint_id") for item in required_constraint_ids)
    if not objective_list:
        raise ValueError("at least one objective is required")
    if not candidate_list:
        raise ValueError("at least one option candidate is required")
    if len(set(constraint_ids)) != len(constraint_ids):
        raise ValueError("required constraint IDs must be unique")

    objective_ids: set[str] = set()
    for objective in objective_list:
        objective_id = _required_text(objective.objective_id, "objective_id")
        if objective_id in objective_ids:
            raise ValueError(f"duplicate objective ID: {objective_id}")
        objective_ids.add(objective_id)
        if objective.direction not in {"MINIMISE", "MAXIMISE"}:
            raise ValueError(f"invalid direction for objective {objective_id}")
        _required_text(objective.unit, f"objective {objective_id} unit")
        _required_text(objective.source_reference, f"objective {objective_id} source_reference")

    seen_options: set[str] = set()
    admissible: list[OptionCandidate] = []
    rejected: list[RejectedOption] = []
    values: dict[str, dict[str, Decimal]] = {}
    for candidate in candidate_list:
        option_id = _required_text(candidate.option_id, "option_id")
        if option_id in seen_options:
            raise ValueError(f"duplicate option ID: {option_id}")
        seen_options.add(option_id)
        _required_text(candidate.name, f"option {option_id} name")
        if not candidate.evidence_references or any(not ref.strip() for ref in candidate.evidence_references):
            raise ValueError(f"option {option_id} requires evidence references")
        values[option_id] = _measurement_map(candidate, objective_list)

        constraint_map = {item.constraint_id: item for item in candidate.constraints}
        if len(constraint_map) != len(candidate.constraints):
            raise ValueError(f"option {option_id} has duplicate constraint evidence")
        reasons: list[str] = []
        for constraint_id in constraint_ids:
            evidence = constraint_map.get(constraint_id)
            if evidence is None:
                reasons.append(f"missing required constraint: {constraint_id}")
            elif not evidence.evidence_reference.strip():
                reasons.append(f"missing evidence for constraint: {constraint_id}")
            elif not evidence.satisfied:
                reasons.append(f"failed required constraint: {constraint_id}")
        if reasons:
            rejected.append(RejectedOption(option_id, tuple(reasons)))
        else:
            admissible.append(candidate)

    front: list[str] = []
    for candidate in admissible:
        dominated = any(
            other.option_id != candidate.option_id
            and _dominates(values[other.option_id], values[candidate.option_id], objective_list)
            for other in admissible
        )
        if not dominated:
            front.append(candidate.option_id)

    return OptionAnalysis(
        decision_question=question,
        human_decision_owner=owner,
        admissible_option_ids=tuple(item.option_id for item in admissible),
        rejected_options=tuple(rejected),
        pareto_front_option_ids=tuple(front),
    )
