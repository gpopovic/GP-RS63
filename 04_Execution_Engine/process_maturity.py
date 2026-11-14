"""Validate evidence-backed process maturity reviews without manufacturing levels."""

from __future__ import annotations

from typing import Any

FINDINGS = {"NOT_ASSESSED", "INSUFFICIENT_EVIDENCE", "PARTIALLY_EVIDENCED", "EVIDENCED", "NOT_APPLICABLE"}


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_maturity_review(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["maturity review must be a JSON object"]
    review: dict[str, Any] = payload
    errors: list[str] = []
    text_fields = (
        "assessment_id", "scope", "framework_name", "framework_version",
        "rating_method_reference", "process_owner", "independent_reviewer",
        "evidence_cutoff_date", "claimed_level", "limitations", "decision_reference",
    )
    for field in text_fields:
        if field not in review:
            errors.append(f"missing field: {field}")
        elif not _text(review[field]):
            errors.append(f"{field} must be a non-empty string")
    if "criteria" not in review:
        errors.append("missing field: criteria")
    if review.get("process_owner") == review.get("independent_reviewer"):
        errors.append("independent_reviewer must differ from process_owner")

    criteria = review.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("criteria must be a non-empty list")
        criteria = []
    seen: set[str] = set()
    applicable_findings: list[str] = []
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict):
            errors.append(f"criteria[{index}] must be an object")
            continue
        criterion_id = criterion.get("criterion_id")
        if not _text(criterion_id):
            errors.append(f"criteria[{index}].criterion_id must be a non-empty string")
        elif str(criterion_id) in seen:
            errors.append(f"criteria[{index}].criterion_id must be unique")
        else:
            seen.add(str(criterion_id))
        finding = criterion.get("finding")
        if finding not in FINDINGS:
            errors.append(f"criteria[{index}].finding must be one of {sorted(FINDINGS)}")
        if finding != "NOT_APPLICABLE":
            applicable_findings.append(str(finding))
        evidence = criterion.get("evidence_references")
        if finding == "EVIDENCED" and (
            not isinstance(evidence, list) or not evidence or not all(_text(item) for item in evidence)
        ):
            errors.append(f"criteria[{index}] marked EVIDENCED requires evidence_references")
        if finding == "NOT_APPLICABLE" and not _text(criterion.get("applicability_rationale")):
            errors.append(f"criteria[{index}] marked NOT_APPLICABLE requires applicability_rationale")

    if review.get("claimed_level") != "NOT_ASSESSED":
        if not applicable_findings or any(finding != "EVIDENCED" for finding in applicable_findings):
            errors.append("a claimed level requires every applicable criterion to be EVIDENCED")
        if review.get("rating_method_reference") == "Pending":
            errors.append("a claimed level requires a final rating_method_reference")
        if review.get("decision_reference") == "Pending":
            errors.append("a claimed level requires a final decision_reference")
    return errors
