"""Tests for Triton's benchmark-qualified model class routing."""

from model_class_router import load_model_class_registry, require_admitted_model, select_model_class


def main() -> None:
    registry = load_model_class_registry()
    assert set(registry["classes"]) == {"FLAGSHIP", "STANDARD", "WORKER"}
    candidates = {candidate["id"]: candidate for candidate in registry["candidate_models"]}
    assert candidates["local_gemma3_4b"]["processing_route"] == "LOCAL_DEVICE_ONLY"
    assert candidates["local_qwen3_4b"]["proposed_class"] == "WORKER"
    assert all(candidate["admission_status"] == "CANDIDATE_NOT_ADMITTED" for candidate in candidates.values())
    try:
        require_admitted_model("gemma3:4b", "WORKER")
    except ValueError as error:
        assert "not admitted" in str(error)
    else:
        raise AssertionError("Unadmitted candidates must fail closed for live routing.")

    worker = select_model_class("ROUTINE", material_risk=False, sensitive_data=False)
    assert worker.model_class == "WORKER"
    assert not worker.requires_human_gate

    standard = select_model_class("COMPLEX", material_risk=False, sensitive_data=False)
    assert standard.model_class == "STANDARD"

    flagship = select_model_class("FINAL_REVIEW", material_risk=True, sensitive_data=True)
    assert flagship.model_class == "FLAGSHIP"
    assert flagship.requires_approved_data_route
    assert flagship.requires_human_gate
    print("Model class router tests passed.")


if __name__ == "__main__":
    main()
