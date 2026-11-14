"""Tests for built-environment capability admission and execution boundaries."""

from built_environment_capability import validate_capability_job


def valid_ifc_job() -> dict[str, object]:
    return {
        "job_id": "BIM-001",
        "capability": "IFC_IDS_VALIDATE",
        "lifecycle": "APPROVED",
        "environment": "PRODUCT",
        "action": "VALIDATE",
        "product_workspace_id": "EXTERNAL-PROJECT",
        "inputs": {
            "source_reference": "product-workspace evidence reference",
            "source_hash": "sha256:" + "a" * 64,
            "tool_name": "IfcOpenShell IDS validator",
            "tool_version": "controlled-version",
            "units": "SI",
            "assumptions": ["declared project assumptions"],
            "uncertainties": ["declared model limitations"],
            "ifc_schema": "IFC4.3",
            "ids_reference": "approved project IDS",
            "ifc_library": "IfcOpenShell controlled version",
            "validation_profile": "project delivery milestone",
            "issue_format": "BCF",
        },
        "output_reference": "external product workspace / Evidence",
        "data_classification": "CONFIDENTIAL",
        "accountable_owner": "BIM_Manager",
        "independent_reviewer": "Independent_BIM_Reviewer",
        "approval_reference": "GATE-BIM-001",
    }


def main() -> None:
    assert validate_capability_job(valid_ifc_job()) == []

    unapproved = valid_ifc_job()
    unapproved["lifecycle"] = "SANDBOX"
    assert "PRODUCT execution requires lifecycle APPROVED" in validate_capability_job(unapproved)

    regex_parser = valid_ifc_job()
    del regex_parser["inputs"]["ids_reference"]
    assert "inputs missing or empty: ids_reference" in validate_capability_job(regex_parser)

    same_reviewer = valid_ifc_job()
    same_reviewer["independent_reviewer"] = same_reviewer["accountable_owner"]
    assert "independent_reviewer must differ from accountable_owner" in validate_capability_job(same_reviewer)

    bad_classification = valid_ifc_job()
    bad_classification["data_classification"] = "SECRET"
    assert any(
        error.startswith("data_classification must be one of")
        for error in validate_capability_job(bad_classification)
    )

    for bad_hash in ("", "sha256:short", "sha256:" + "a" * 65, "sha256:" + "z" * 64, "md5:" + "a" * 64):
        invalid_hash = valid_ifc_job()
        invalid_hash["inputs"]["source_hash"] = bad_hash
        assert "inputs.source_hash must use sha256:<64 hexadecimal characters>" in validate_capability_job(
            invalid_hash
        )
    print("Built-environment capability contract tests passed.")


if __name__ == "__main__":
    main()
