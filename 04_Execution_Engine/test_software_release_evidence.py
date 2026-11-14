"""Tests for candidate-specific, evidence-backed software release review."""

from copy import deepcopy

from software_release_evidence import validate_software_release_evidence


def valid_manifest() -> dict[str, object]:
    return {
        "workspace_id": "EXTERNAL-SOFTWARE-WORKSPACE",
        "work_item_id": "PLUGIN-VAL-001",
        "candidate_version": "2.0.0",
        "source_revision": "0123456789abcdef",
        "artifact_sha256": "sha256:" + "a" * 64,
        "executed_at_utc": "2099-01-01T10:00:00Z",
        "test_environment": "isolated controlled workstation",
        "fixture_set": "fixture-set-v1",
        "requirements_p0": {"total": 4, "passed": 4},
        "blocking_tests": {"total": 8, "passed": 8},
        "protected_state": {"checked": 5, "unchanged": 5, "unexpected_mutations": 0},
        "workflow_checks": [
            {"id": "save_reopen", "applicable": True, "total": 2, "passed": 2, "evidence_reference": "EV-SAVE"},
            {"id": "undo_redo", "applicable": True, "total": 2, "passed": 2, "evidence_reference": "EV-UNDO"},
            {"id": "export_determinism", "applicable": True, "total": 2, "passed": 2, "evidence_reference": "EV-EXPORT"},
            {"id": "ambiguity_safety", "applicable": False, "total": 0, "passed": 0, "not_applicable_rationale": "No ambiguous-input path in this bounded candidate."},
        ],
        "clean_build": {"total": 2, "passed": 2},
        "live_observation": {"required": True, "status": "PASSED", "evidence_reference": "EV-LIVE"},
        "claim_derivation": "MACHINE_DERIVED",
        "evidence_references": ["EV-MANIFEST", "EV-LIVE"],
        "raw_log_references": ["LOG-COMPILE", "LOG-TEST"],
        "rollback_reference": "BACKUP-001",
        "independent_reviewer": "Code_Validator",
        "limitations": ["Approval applies only to this candidate hash and environment."],
        "decision": "READY_FOR_RELEASE_REVIEW",
    }


def main() -> None:
    assert validate_software_release_evidence(valid_manifest()) == []

    cases = (
        ("artifact_sha256", "sha256:short", "artifact_sha256 must use"),
        ("claim_derivation", "MANUAL_CONFIRMATION", "MACHINE_DERIVED claim_derivation"),
    )
    for field, value, expected in cases:
        candidate = valid_manifest()
        candidate[field] = value
        assert any(expected in error for error in validate_software_release_evidence(candidate))

    p0_gap = valid_manifest()
    p0_gap["requirements_p0"]["passed"] = 3
    assert any("all P0 requirements" in error for error in validate_software_release_evidence(p0_gap))

    mutation = valid_manifest()
    mutation["protected_state"]["unexpected_mutations"] = 1
    assert any("zero unexpected mutations" in error for error in validate_software_release_evidence(mutation))

    workflow_gap = valid_manifest()
    workflow_gap["workflow_checks"][0]["passed"] = 1
    assert any("workflow save_reopen" in error for error in validate_software_release_evidence(workflow_gap))

    pending_live = valid_manifest()
    pending_live["live_observation"] = {"required": True, "status": "PENDING", "evidence_reference": "Pending"}
    assert any("live-observation disposition" in error for error in validate_software_release_evidence(pending_live))

    needs_evidence = deepcopy(valid_manifest())
    needs_evidence["decision"] = "NEEDS_EVIDENCE"
    needs_evidence["requirements_p0"] = {"total": 4, "passed": 2}
    needs_evidence["claim_derivation"] = "MANUAL_DRAFT"
    assert validate_software_release_evidence(needs_evidence) == []
    print("Software release evidence contract tests passed.")


if __name__ == "__main__":
    main()
