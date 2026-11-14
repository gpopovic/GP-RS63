"""Tests for non-mutating task-granularity recommendations."""

from task_granularity import recommend_granularity


def call(**overrides: object):
    values = {
        "current_mode": "STANDARD_SLICE",
        "comparable_outcomes": [],
        "material_review_loops": 0,
        "failed_gate": False,
        "critical_escape": False,
        "high_blast_radius": False,
        "stable_contract": True,
        "independent_lanes": True,
        "write_scope_collision": False,
    }
    values.update(overrides)
    return recommend_granularity(**values)


def main() -> None:
    assert call(critical_escape=True).action == "CONTAIN_AND_SPLIT"
    assert call(material_review_loops=2).action == "SPLIT"
    assert call(write_scope_collision=True).may_parallelise is False
    trial = call(comparable_outcomes=["ACCEPTED", "ACCEPTED", "ACCEPTED"])
    assert trial.action == "PROPOSE_MERGE_TRIAL"
    assert trial.requires_human_decision is True
    assert call(comparable_outcomes=["ACCEPTED", "ACCEPTED"]).action == "KEEP"
    print("Task granularity tests passed.")


if __name__ == "__main__":
    main()
