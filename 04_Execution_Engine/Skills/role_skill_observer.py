"""Observe role and skill KPIs and make bounded evolution recommendations."""

from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import sys
from typing import Literal

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import TRITON_ROOT, load_role_instructions

ArtifactKind = Literal["role", "skill"]
Recommendation = Literal["INSUFFICIENT_EVIDENCE", "KEEP_BASELINE", "RECOMMEND_PROMOTION", "REJECT_CANDIDATE"]
ActorType = Literal["AI", "HUMAN", "HYBRID"]
OperatingMode = Literal["EXPLORATORY", "GUIDED", "STRICT"]

OBSERVATIONS_DIR = TRITON_ROOT / "04_Execution_Engine" / "Skills" / "observations"
OBSERVATION_PATH = OBSERVATIONS_DIR / "role_skill_quality_history.jsonl"


@dataclass(frozen=True)
class RoleSkillObservation:
    """One reviewed KPI observation for an AI, human, or hybrid work result."""

    timestamp: str
    artifact_kind: ArtifactKind
    artifact_id: str
    version: str
    benchmark_id: str
    quality_passed: bool
    traceability_score: float
    rework_cycles: int
    latency_seconds: float
    estimated_cost: float
    unresolved_disagreement: bool
    severe_failure: bool
    evidence: str
    actor_type: ActorType = "AI"
    human_effort_hours: float = 0.0
    gate_missed: bool = False
    customer_claim_risk: float = 0.0
    estimated_loss_exposure: float = 0.0
    role_boundary_pressure: float = 0.0


@dataclass(frozen=True)
class ArtifactAssessment:
    """A baseline/candidate comparison that cannot apply a change by itself."""

    artifact_kind: ArtifactKind
    artifact_id: str
    baseline_version: str
    candidate_version: str
    compared_samples: int
    recommendation: Recommendation
    baseline_quality_pass_rate: float
    candidate_quality_pass_rate: float
    baseline_traceability: float
    candidate_traceability: float
    baseline_median_latency_seconds: float
    candidate_median_latency_seconds: float
    reason: str


@dataclass(frozen=True)
class AutonomyAssessment:
    """A recommended operating mode based on evidence; it cannot edit an artifact."""

    artifact_kind: ArtifactKind
    artifact_id: str
    version: str
    sample_count: int
    operating_mode: OperatingMode
    quality_pass_rate: float
    mean_traceability: float
    gate_miss_rate: float
    severe_failure_count: int
    reason: str


def _load_observations() -> list[RoleSkillObservation]:
    if not OBSERVATION_PATH.is_file():
        return []
    return [
        RoleSkillObservation(**json.loads(line))
        for line in OBSERVATION_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def record_observation(observation: RoleSkillObservation) -> None:
    """Append one independently reviewed, bounded KPI observation."""
    bounded_scores = (
        observation.traceability_score,
        observation.customer_claim_risk,
        observation.role_boundary_pressure,
    )
    if any(not 0.0 <= score <= 1.0 for score in bounded_scores):
        raise ValueError("traceability, claim risk, and boundary pressure must be between 0.0 and 1.0")
    non_negative = (
        observation.rework_cycles,
        observation.latency_seconds,
        observation.estimated_cost,
        observation.human_effort_hours,
        observation.estimated_loss_exposure,
    )
    if any(value < 0 for value in non_negative):
        raise ValueError("rework, time, effort, cost, and loss exposure must be non-negative")
    OBSERVATIONS_DIR.mkdir(parents=True, exist_ok=True)
    with OBSERVATION_PATH.open("a", encoding="utf-8") as history:
        history.write(json.dumps(asdict(observation), ensure_ascii=False) + "\n")


def _matching(
    observations: list[RoleSkillObservation], artifact_kind: ArtifactKind, artifact_id: str, version: str
) -> dict[str, RoleSkillObservation]:
    return {
        item.benchmark_id: item
        for item in observations
        if item.artifact_kind == artifact_kind and item.artifact_id == artifact_id and item.version == version
    }


def assess_candidate(
    *, artifact_kind: ArtifactKind, artifact_id: str, baseline_version: str, candidate_version: str
) -> ArtifactAssessment:
    """Compare equivalent benchmark results under the governance policy."""
    load_role_instructions("Role_Skill_Evolution_Manager")
    all_observations = _load_observations()
    baseline = _matching(all_observations, artifact_kind, artifact_id, baseline_version)
    candidate = _matching(all_observations, artifact_kind, artifact_id, candidate_version)
    benchmark_ids = sorted(set(baseline) & set(candidate))
    if len(benchmark_ids) < 10:
        return ArtifactAssessment(
            artifact_kind, artifact_id, baseline_version, candidate_version, len(benchmark_ids),
            "INSUFFICIENT_EVIDENCE", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            "Fewer than 10 comparable benchmark observations are available.",
        )
    base = [baseline[key] for key in benchmark_ids]
    trial = [candidate[key] for key in benchmark_ids]
    base_quality = sum(item.quality_passed for item in base) / len(base)
    trial_quality = sum(item.quality_passed for item in trial) / len(trial)
    base_traceability = statistics.mean(item.traceability_score for item in base)
    trial_traceability = statistics.mean(item.traceability_score for item in trial)
    base_latency = statistics.median(item.latency_seconds for item in base)
    trial_latency = statistics.median(item.latency_seconds for item in trial)
    protected_regression = (
        any(item.severe_failure or item.gate_missed for item in trial)
        or trial_quality < base_quality
        or trial_traceability < base_traceability
        or sum(item.unresolved_disagreement for item in trial) > sum(item.unresolved_disagreement for item in base)
        or statistics.mean(item.rework_cycles for item in trial) > statistics.mean(item.rework_cycles for item in base)
    )
    improved = (
        trial_quality > base_quality
        or trial_traceability > base_traceability
        or trial_latency < base_latency
        or statistics.mean(item.estimated_cost for item in trial) < statistics.mean(item.estimated_cost for item in base)
    )
    recommendation: Recommendation = "REJECT_CANDIDATE" if protected_regression else (
        "RECOMMEND_PROMOTION" if improved else "KEEP_BASELINE"
    )
    reasons = {
        "REJECT_CANDIDATE": "Candidate regressed a protected KPI or produced a severe failure/gate miss.",
        "RECOMMEND_PROMOTION": "Candidate improved at least one KPI without protected regression; prepare a promotion decision record.",
        "KEEP_BASELINE": "No protected regression, but no measurable improvement over the baseline.",
    }
    return ArtifactAssessment(
        artifact_kind, artifact_id, baseline_version, candidate_version, len(benchmark_ids), recommendation,
        base_quality, trial_quality, base_traceability, trial_traceability, base_latency, trial_latency,
        reasons[recommendation],
    )


def assess_operating_mode(*, artifact_kind: ArtifactKind, artifact_id: str, version: str) -> AutonomyAssessment:
    """Grant or withdraw creative latitude based on reviewed evidence."""
    load_role_instructions("Role_Skill_Evolution_Manager")
    observations = [
        item for item in _load_observations()
        if item.artifact_kind == artifact_kind and item.artifact_id == artifact_id and item.version == version
    ]
    if not observations:
        return AutonomyAssessment(
            artifact_kind, artifact_id, version, 0, "GUIDED", 0.0, 0.0, 0.0, 0,
            "No reviewed evidence exists; use the normal guided workflow.",
        )
    quality_rate = sum(item.quality_passed for item in observations) / len(observations)
    traceability = statistics.mean(item.traceability_score for item in observations)
    gate_miss_rate = sum(item.gate_missed for item in observations) / len(observations)
    severe_failures = sum(item.severe_failure for item in observations)
    strict = severe_failures > 0 or gate_miss_rate >= 0.10 or (len(observations) >= 3 and quality_rate < 0.80)
    exploratory = (
        len(observations) >= 10
        and quality_rate >= 0.90
        and traceability >= 0.90
        and statistics.mean(item.rework_cycles for item in observations) <= 0.20
        and not any(item.unresolved_disagreement for item in observations)
    )
    if strict:
        mode: OperatingMode = "STRICT"
        reason = "Severe failure, gate miss, or repeated low quality requires a bounded checklist-driven workflow."
    elif exploratory:
        mode = "EXPLORATORY"
        reason = "High quality, traceability, and low rework justify wider creative latitude."
    else:
        mode = "GUIDED"
        reason = "Mixed or insufficient evidence requires normal workflow controls."
    return AutonomyAssessment(
        artifact_kind, artifact_id, version, len(observations), mode, quality_rate, traceability,
        gate_miss_rate, severe_failures, reason,
    )


def propose_mutation(*, artifact_kind: ArtifactKind, artifact_id: str, baseline_version: str, gap: str) -> dict[str, str]:
    """Create one bounded proposal; it deliberately does not edit a role or skill."""
    return {
        "artifact_kind": artifact_kind,
        "artifact_id": artifact_id,
        "baseline_version": baseline_version,
        "observed_gap": gap,
        "allowed_mutations": "; ".join((
            "clarify one workflow step", "tighten one output schema", "add one guardrail",
            "add one negative test", "remove redundant wording",
        )),
        "next_state": "trial",
        "instruction": "Create exactly one variant, evaluate it against the held-out local benchmark set, and record the comparison.",
    }


def propose_role_split(*, role_id: str, functions: list[str], pressure_observations: int) -> dict[str, object]:
    """Propose a trial split only after recurring evidence of overloaded boundaries."""
    unique_functions = sorted({item.strip() for item in functions if item.strip()})
    ready = pressure_observations >= 3 and len(unique_functions) >= 2
    return {
        "role_id": role_id,
        "observed_functions": unique_functions,
        "pressure_observations": pressure_observations,
        "recommendation": "CREATE_TRIAL_SPLIT" if ready else "KEEP_ROLE_AND_MEASURE",
        "required_next_step": (
            "Create separate trial role candidates with distinct missions, interfaces, KPIs, and held-out evaluations."
            if ready else "Collect at least three comparable pressure observations and identify at least two distinct functions."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Record and assess Triton role/skill KPI evidence.")
    commands = parser.add_subparsers(dest="command", required=True)
    record = commands.add_parser("record")
    record.add_argument("--kind", required=True, choices=("role", "skill"))
    record.add_argument("--id", required=True)
    record.add_argument("--version", required=True)
    record.add_argument("--benchmark", required=True)
    record.add_argument("--quality-passed", action="store_true")
    record.add_argument("--traceability", required=True, type=float)
    record.add_argument("--rework", required=True, type=int)
    record.add_argument("--latency", required=True, type=float)
    record.add_argument("--cost", required=True, type=float)
    record.add_argument("--unresolved-disagreement", action="store_true")
    record.add_argument("--severe-failure", action="store_true")
    record.add_argument("--evidence", required=True)
    record.add_argument("--actor-type", choices=("AI", "HUMAN", "HYBRID"), default="AI")
    record.add_argument("--human-effort-hours", type=float, default=0.0)
    record.add_argument("--gate-missed", action="store_true")
    record.add_argument("--customer-claim-risk", type=float, default=0.0)
    record.add_argument("--loss-exposure", type=float, default=0.0)
    record.add_argument("--boundary-pressure", type=float, default=0.0)
    assess = commands.add_parser("assess")
    assess.add_argument("--kind", required=True, choices=("role", "skill"))
    assess.add_argument("--id", required=True)
    assess.add_argument("--baseline", required=True)
    assess.add_argument("--candidate", required=True)
    propose = commands.add_parser("propose")
    propose.add_argument("--kind", required=True, choices=("role", "skill"))
    propose.add_argument("--id", required=True)
    propose.add_argument("--baseline", required=True)
    propose.add_argument("--gap", required=True)
    autonomy = commands.add_parser("operating-mode")
    autonomy.add_argument("--kind", required=True, choices=("role", "skill"))
    autonomy.add_argument("--id", required=True)
    autonomy.add_argument("--version", required=True)
    split = commands.add_parser("propose-split")
    split.add_argument("--role-id", required=True)
    split.add_argument("--functions", required=True, help="Semicolon-separated distinct functions.")
    split.add_argument("--pressure-observations", required=True, type=int)
    args = parser.parse_args()

    if args.command == "record":
        record_observation(RoleSkillObservation(
            timestamp=datetime.now(UTC).isoformat(), artifact_kind=args.kind, artifact_id=args.id,
            version=args.version, benchmark_id=args.benchmark, quality_passed=args.quality_passed,
            traceability_score=args.traceability, rework_cycles=args.rework, latency_seconds=args.latency,
            estimated_cost=args.cost, unresolved_disagreement=args.unresolved_disagreement,
            severe_failure=args.severe_failure, evidence=args.evidence, actor_type=args.actor_type,
            human_effort_hours=args.human_effort_hours, gate_missed=args.gate_missed,
            customer_claim_risk=args.customer_claim_risk, estimated_loss_exposure=args.loss_exposure,
            role_boundary_pressure=args.boundary_pressure,
        ))
        print("Recorded.")
    elif args.command == "assess":
        result = assess_candidate(
            artifact_kind=args.kind, artifact_id=args.id, baseline_version=args.baseline, candidate_version=args.candidate,
        )
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    elif args.command == "operating-mode":
        result = assess_operating_mode(artifact_kind=args.kind, artifact_id=args.id, version=args.version)
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    elif args.command == "propose-split":
        result = propose_role_split(
            role_id=args.role_id, functions=args.functions.split(";"), pressure_observations=args.pressure_observations,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = propose_mutation(
            artifact_kind=args.kind, artifact_id=args.id, baseline_version=args.baseline, gap=args.gap,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
