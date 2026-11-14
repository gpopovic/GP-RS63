"""Focused tests for controlled collaboration-evolution recommendations."""

from collaboration_observer import CollaborationObservation, recommend_collaboration_evolution


def test_major_redesign_requires_cross_category_evidence() -> None:
    observations = [CollaborationObservation(f"P{index}", "requirements_to_architecture", "embedded", 0.80, 0.25, 0.18, 60, 0.03, 1.05, False, True) for index in range(1, 4)]
    assert recommend_collaboration_evolution(observations)[0] == "PROPOSE_MAJOR_REDESIGN"


def test_critical_escape_containment_overrides_evolution() -> None:
    observation = CollaborationObservation("P1", "architecture_to_delivery", "embedded", 0.9, 0.1, 0.1, 12, 0.0, 0.8, True, True)
    assert recommend_collaboration_evolution([observation])[0] == "CONTAIN_AND_STRICT_MODE"
