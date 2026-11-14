"""Tests for configured adaptive workflow selection and spend containment."""

from adaptive_harness import load_catalog, select_adaptive_harness


def main() -> None:
    catalog = load_catalog()
    assert catalog["global_controls"]["max_parallel_lanes"] == 3
    assert "Engineering Flow Plan" in catalog["global_controls"]["engineering_flow_logistics"]
    assert "relative score never commits" in catalog["global_controls"]["task_investment"]
    for workflow_id in catalog["workflows"]:
        plan = select_adaptive_harness(workflow_id, material_risk=False, sensitive_data=False)
        assert plan.maximum_parallel_lanes <= 3

    coding = select_adaptive_harness("coding", material_risk=False, sensitive_data=False)
    assert coding.role_profile == "standard_delivery"
    assert coding.maximum_parallel_lanes == 3
    assert coding.maximum_model_calls_before_gate == 7
    assert coding.requires_cost_preflight
    assert not coding.requires_human_approval
    assert any("artifact readiness" in output for output in coding.stages[0]["outputs"])

    regulated = select_adaptive_harness(
        "regulated_engineering", material_risk=True, sensitive_data=True
    )
    assert regulated.role_profile == "architecture_delivery"
    assert regulated.maximum_parallel_lanes == 3
    assert regulated.requires_human_approval

    building = select_adaptive_harness("built_environment", material_risk=True, sensitive_data=False)
    assert building.role_profile == "built_environment_delivery"
    assert building.maximum_parallel_lanes == 3
    assert building.requires_human_approval

    try:
        select_adaptive_harness("unknown", material_risk=False, sensitive_data=False)  # type: ignore[arg-type]
    except ValueError as error:
        assert "Unknown adaptive workflow" in str(error)
    else:
        raise AssertionError("Unknown workflows must fail closed.")
    print("Adaptive harness tests passed.")


if __name__ == "__main__":
    main()
