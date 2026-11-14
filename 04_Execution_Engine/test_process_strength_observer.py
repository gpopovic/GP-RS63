"""Tests for non-mutating process-strength observation and bounded evolution."""

from process_strength_observer import (
    ProcessObservation,
    ProcessQualityContract,
    recommend_process_strength,
)


def contract() -> ProcessQualityContract:
    return ProcessQualityContract(
        task_class="coding-standard",
        control_family="code-review",
        minimum_first_pass_acceptance=0.80,
        maximum_rework_ratio=0.20,
        maximum_escaped_defect_rate=0.05,
        minimum_satisfaction=0.80,
        minimum_evidence_completeness=0.95,
        maximum_cycle_time_hours=48.0,
        maximum_process_wait_ratio=0.25,
        maximum_assurance_cost_ratio=0.25,
    )


def observations(**overrides: object) -> list[ProcessObservation]:
    result = []
    for index in range(3):
        values = {
            "period_id": f"P{index + 1}",
            "task_class": "coding-standard",
            "control_family": "code-review",
            "first_pass_acceptance": 0.90,
            "rework_ratio": 0.10,
            "escaped_defect_rate": 0.01,
            "satisfaction": 0.90,
            "evidence_completeness": 1.0,
            "cycle_time_hours": 30.0,
            "process_wait_ratio": 0.10,
            "assurance_cost_ratio": 0.15,
            "critical_escape": False,
            "mandatory_nonconformity": False,
            "independent_reviewer": True,
        }
        values.update(overrides)
        result.append(ProcessObservation(**values))
    return result


def main() -> None:
    recommendation, _ = recommend_process_strength(contract(), observations(), exploration_authorised=False)
    assert recommendation == "KEEP_BASELINE"

    recommendation, _ = recommend_process_strength(contract(), observations(), exploration_authorised=True)
    assert recommendation == "PROPOSE_BOUNDED_VARIATION"

    recommendation, reasons = recommend_process_strength(
        contract(), observations(rework_ratio=0.35), exploration_authorised=True
    )
    assert recommendation == "TIGHTEN_ONE_CONTROL"
    assert "rework_ratio" in reasons

    recommendation, _ = recommend_process_strength(
        contract(), observations(process_wait_ratio=0.40), exploration_authorised=True
    )
    assert recommendation == "PROPOSE_CONTROL_REDUCTION"

    recommendation, _ = recommend_process_strength(
        contract(), observations(critical_escape=True), exploration_authorised=True
    )
    assert recommendation == "CONTAIN_AND_STRENGTHEN"

    recommendation, _ = recommend_process_strength(
        contract(), observations()[:2], exploration_authorised=True
    )
    assert recommendation == "KEEP_BASELINE"
    print("Process-strength observer tests passed.")


if __name__ == "__main__":
    main()
