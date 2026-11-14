"""Focused checks for bounded role and skill evolution recommendations."""

from __future__ import annotations

import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent
if str(SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILLS_DIR))

import role_skill_observer as observer


def test_requires_comparable_evidence(tmp_path: Path) -> None:
    original_path = observer.OBSERVATION_PATH
    original_dir = observer.OBSERVATIONS_DIR
    try:
        observer.OBSERVATIONS_DIR = tmp_path
        observer.OBSERVATION_PATH = tmp_path / "history.jsonl"
        result = observer.assess_candidate(
            artifact_kind="skill", artifact_id="testing-specialist", baseline_version="v1", candidate_version="v2"
        )
        assert result.recommendation == "INSUFFICIENT_EVIDENCE"
    finally:
        observer.OBSERVATION_PATH = original_path
        observer.OBSERVATIONS_DIR = original_dir


def test_mutation_is_only_a_proposal() -> None:
    proposal = observer.propose_mutation(
        artifact_kind="role", artifact_id="Code_Validator", baseline_version="v1", gap="rework is high"
    )
    assert proposal["next_state"] == "trial"
    assert "exactly one variant" in proposal["instruction"]


def test_no_evidence_starts_guided() -> None:
    assessment = observer.assess_operating_mode(
        artifact_kind="role", artifact_id="Code_Validator", version="v1"
    )
    assert assessment.operating_mode == "GUIDED"


def test_role_split_requires_repeated_boundary_evidence() -> None:
    proposal = observer.propose_role_split(
        role_id="Cross_Border_Delivery_Manager",
        functions=["customer escalation", "supplier capacity"],
        pressure_observations=3,
    )
    assert proposal["recommendation"] == "CREATE_TRIAL_SPLIT"
