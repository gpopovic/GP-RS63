"""Tests for evidence-backed process maturity review records."""

from process_maturity import validate_maturity_review


def valid_unassessed() -> dict[str, object]:
    return {
        "assessment_id": "MAT-001", "scope": "One declared process and assessment boundary",
        "framework_name": "Declared framework", "framework_version": "Exact controlled version",
        "rating_method_reference": "Pending", "process_owner": "Named Process Owner",
        "independent_reviewer": "Named Independent Reviewer", "evidence_cutoff_date": "2026-08-21",
        "criteria": [{"criterion_id": "CRIT-1", "finding": "NOT_ASSESSED", "evidence_references": [], "applicability_rationale": "Applicable; evidence not yet reviewed"}],
        "claimed_level": "NOT_ASSESSED", "limitations": "No assessment evidence collected yet",
        "decision_reference": "Pending",
    }


def main() -> None:
    assert validate_maturity_review(valid_unassessed()) == []
    fabricated = valid_unassessed()
    fabricated["claimed_level"] = "LEVEL_5"
    errors = validate_maturity_review(fabricated)
    assert "a claimed level requires every applicable criterion to be EVIDENCED" in errors
    assert "a claimed level requires a final rating_method_reference" in errors
    evidenced = valid_unassessed()
    criterion = evidenced["criteria"][0]
    criterion["finding"] = "EVIDENCED"
    criterion["evidence_references"] = ["EV-001"]
    evidenced["claimed_level"] = "FRAMEWORK_DEFINED_LEVEL"
    evidenced["rating_method_reference"] = "METHOD-001"
    evidenced["decision_reference"] = "DEC-001"
    assert validate_maturity_review(evidenced) == []
    print("Process maturity tests passed.")


if __name__ == "__main__":
    main()
