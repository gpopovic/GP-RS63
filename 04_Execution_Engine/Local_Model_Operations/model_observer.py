"""Evidence-led model-health observation and safe routing recommendations."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import sys
from typing import Literal

from dotenv import load_dotenv

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import MODEL_OBSERVATIONS_DIR, TRITON_ROOT, load_role_instructions

load_dotenv(TRITON_ROOT / ".env")
load_dotenv(TRITON_ROOT / "04_Execution_Engine" / "LangGraph_Pipelines" / ".env", override=False)

HealthDecision = Literal["KEEP", "ROUTE_TO_LOCAL_BACKUP", "ESCALATE_FOR_HUMAN_SIGN_OFF"]


@dataclass(frozen=True)
class ModelObservation:
    """One objective quality signal, stored append-only as JSONL."""

    timestamp: str
    model: str
    role: str
    quality_score: float
    critical_failure: bool
    evidence: str


@dataclass(frozen=True)
class ModelHealth:
    """A routing recommendation; it never directly installs or replaces models."""

    model: str
    role: str
    decision: HealthDecision
    sample_count: int
    mean_quality_score: float
    consecutive_critical_failures: int
    recommended_model: str | None
    online_escalation_ready: bool
    reason: str


def _observation_path() -> Path:
    return MODEL_OBSERVATIONS_DIR / "model_quality_history.jsonl"


def _load_observations() -> list[ModelObservation]:
    path = _observation_path()
    if not path.is_file():
        return []

    observations: list[ModelObservation] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        observations.append(ModelObservation(**data))
    return observations


def record_observation(
    *,
    model: str,
    role: str,
    quality_score: float,
    critical_failure: bool,
    evidence: str,
) -> ModelObservation:
    """Record a bounded quality score together with human-readable evidence."""
    if not 0.0 <= quality_score <= 1.0:
        raise ValueError("quality_score must be between 0.0 and 1.0")

    observation = ModelObservation(
        timestamp=datetime.now(UTC).isoformat(),
        model=model,
        role=role,
        quality_score=quality_score,
        critical_failure=critical_failure,
        evidence=evidence,
    )
    path = _observation_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as history:
        history.write(json.dumps(asdict(observation), ensure_ascii=False) + "\n")
    return observation


def assess_model(model: str, role: str) -> ModelHealth:
    """Assess repeated evidence and recommend only approved, local alternatives."""
    # Loading the role keeps the governing policy external to Python.
    load_role_instructions("Model_Quality_Observer")
    minimum_score = float(os.getenv("TRITON_MIN_QUALITY_SCORE", "0.80"))
    minimum_samples = int(os.getenv("TRITON_MIN_QUALITY_SAMPLES", "5"))
    max_critical_failures = int(os.getenv("TRITON_MAX_CONSECUTIVE_CRITICAL_FAILURES", "3"))
    relevant = [item for item in _load_observations() if item.model == model and item.role == role]
    sample = relevant[-minimum_samples:]
    scores = [item.quality_score for item in sample]
    mean_score = sum(scores) / len(scores) if scores else 0.0
    failures = 0
    for item in reversed(relevant):
        if not item.critical_failure:
            break
        failures += 1

    backup_name = os.getenv(f"TRITON_{role.upper()}_BACKUP_MODEL", "").strip() or None
    remote_ready = all(
        os.getenv(name, "").strip()
        for name in (
            "TRITON_EU_FALLBACK_BASE_URL",
            "TRITON_EU_FALLBACK_MODEL",
            "TRITON_ONLINE_DATA_CAPSULE_ID",
        )
    ) and all(
        os.getenv(name, "false").lower() == "true"
        for name in (
            "TRITON_EU_FALLBACK_ENABLED",
            "TRITON_EU_FALLBACK_APPROVED",
            "TRITON_ONLINE_DATA_CAPSULE_APPROVED",
            "TRITON_ONLINE_EXECUTION_APPROVED",
        )
    )

    insufficient = len(sample) >= minimum_samples and mean_score < minimum_score
    repeated_critical_failure = failures >= max_critical_failures
    if insufficient or repeated_critical_failure:
        if backup_name and backup_name != model:
            return ModelHealth(
                model, role, "ROUTE_TO_LOCAL_BACKUP", len(sample), mean_score, failures,
                backup_name, remote_ready,
                "Repeated evidence is below the configured local quality threshold.",
            )
        return ModelHealth(
            model, role, "ESCALATE_FOR_HUMAN_SIGN_OFF", len(sample), mean_score, failures,
            None, remote_ready,
            "No approved local backup is configured; prepare a human escalation decision.",
        )

    return ModelHealth(
        model, role, "KEEP", len(sample), mean_score, failures, None, remote_ready,
        "Insufficient negative evidence to change the approved model baseline.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Record and assess Triton model quality evidence.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    record = subparsers.add_parser("record", help="Append one reviewed quality observation.")
    record.add_argument("--model", required=True)
    record.add_argument("--role", required=True, choices=("primary", "validator", "specialist"))
    record.add_argument("--score", type=float, required=True)
    record.add_argument("--critical-failure", action="store_true")
    record.add_argument("--evidence", required=True)
    status = subparsers.add_parser("status", help="Print the current health recommendation.")
    status.add_argument("--model", required=True)
    status.add_argument("--role", required=True, choices=("primary", "validator", "specialist"))
    args = parser.parse_args()

    if args.command == "record":
        result = record_observation(
            model=args.model, role=args.role, quality_score=args.score,
            critical_failure=args.critical_failure, evidence=args.evidence,
        )
        print(json.dumps(asdict(result), ensure_ascii=False))
        return

    print(json.dumps(asdict(assess_model(args.model, args.role)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
