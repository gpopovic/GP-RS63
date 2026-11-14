"""Tests for evidence-backed creative option analysis."""

from creative_option_analysis import (
    ConstraintEvidence,
    Objective,
    OptionCandidate,
    analyse_options,
)


def candidate(
    option_id: str,
    cost: str,
    carbon: str,
    usefulness: str,
    *,
    safe: bool = True,
) -> OptionCandidate:
    return OptionCandidate(
        option_id=option_id,
        name=f"Option {option_id}",
        measurements=(("cost", cost), ("carbon", carbon), ("usefulness", usefulness)),
        constraints=(ConstraintEvidence("declared-safety", safe, f"evidence://{option_id}/safety"),),
        evidence_references=(f"evidence://{option_id}/input",),
    )


def main() -> None:
    objectives = (
        Objective("cost", "MINIMISE", "EUR", "source://estimate/2026-08-28"),
        Objective("carbon", "MINIMISE", "kgCO2e", "source://carbon/2026-08-28"),
        Objective("usefulness", "MAXIMISE", "review-points", "source://review-method/1.0"),
    )
    result = analyse_options(
        decision_question="Which option should receive further evidence?",
        human_decision_owner="Product_Owner",
        objectives=objectives,
        required_constraint_ids=("declared-safety",),
        candidates=(
            candidate("A", "100", "100", "8"),
            candidate("B", "120", "80", "9"),
            candidate("C", "130", "130", "7"),
            candidate("D", "90", "60", "10", safe=False),
        ),
    )
    assert result.admissible_option_ids == ("A", "B", "C")
    assert result.pareto_front_option_ids == ("A", "B")
    assert result.rejected_options[0].option_id == "D"
    assert "failed required constraint" in result.rejected_options[0].reasons[0]
    assert result.human_decision_required is True
    assert not hasattr(result, "recommended_option")

    try:
        analyse_options(
            decision_question="test",
            human_decision_owner="owner",
            objectives=objectives,
            required_constraint_ids=("declared-safety",),
            candidates=(OptionCandidate("X", "X", (("cost", "1"),), (), ("evidence://x",)),),
        )
    except ValueError as error:
        assert "exactly match" in str(error)
    else:
        raise AssertionError("missing objective measurements must fail closed")
    print("Creative option analysis tests passed.")


if __name__ == "__main__":
    main()
