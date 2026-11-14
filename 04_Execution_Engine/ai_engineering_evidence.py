"""Validate AI engineering decision evidence without granting tool qualification or approval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EVIDENCE_PROFILES = {"E0_ADVISORY", "E1_TRACEABLE_CANDIDATE", "E2_ASSURANCE_RELIANCE"}
RECORD_STATUSES = {"DRAFT", "READY_FOR_REVIEW", "APPROVED_FOR_DECLARED_USE", "REJECTED"}
RELIANCE_DECISIONS = {
    "NO_QUALIFICATION_ADVISORY",
    "NO_QUALIFICATION_INDEPENDENT_VERIFICATION",
    "QUALIFICATION_REQUIRED",
    "USE_PROHIBITED",
}
DETECTION = {"COMPLETE", "PARTIAL", "NONE", "NOT_APPLICABLE"}
WEIGHT_IDENTITY_MODES = {"LOCAL_SHA256", "PROVIDER_VERSION", "NOT_AVAILABLE_WITH_RESTRICTION"}
CAPTURE_MODES = {
    "HASH_AND_CONTROLLED_REFERENCE",
    "ENCRYPTED_CONTROLLED_REFERENCE",
    "NOT_RETAINED_WITH_RATIONALE",
}
CAPTURE_CATEGORIES = {
    "SYSTEM_PROMPT",
    "USER_INSTRUCTION",
    "RETRIEVAL_MANIFEST",
    "RAW_MODEL_OUTPUT",
    "VALIDATION_LOG",
    "TRANSFORMATION_LOG",
    "FINAL_DIFF",
    "PSEUDONYMISATION_EVENT_LOG",
}
CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
REQUIRED_E1_CATEGORIES = {
    "SYSTEM_PROMPT",
    "USER_INSTRUCTION",
    "RETRIEVAL_MANIFEST",
    "RAW_MODEL_OUTPUT",
    "VALIDATION_LOG",
    "FINAL_DIFF",
}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(character in "0123456789abcdefABCDEF" for character in digest)


def validate_ai_engineering_evidence(payload: object) -> list[str]:
    """Return structural and fail-closed approval errors; an empty result is not qualification."""
    if not isinstance(payload, dict):
        return ["AI engineering decision record must be a JSON object"]
    record: dict[str, Any] = payload
    errors: list[str] = []
    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in (
        "record_id", "workspace_id", "work_item_id", "intended_use", "affected_process",
        "domain_profile_reference", "assurance_classification_reference", "record_owner",
    ):
        if not _non_empty(record.get(field)):
            errors.append(f"{field} must be a non-empty string")
    profile = record.get("evidence_profile")
    status = record.get("record_status")
    if profile not in EVIDENCE_PROFILES:
        errors.append(f"evidence_profile must be one of {sorted(EVIDENCE_PROFILES)}")
    if status not in RECORD_STATUSES:
        errors.append(f"record_status must be one of {sorted(RECORD_STATUSES)}")

    reliance = record.get("tool_reliance")
    decision = None
    detection = None
    if not isinstance(reliance, dict):
        errors.append("tool_reliance must be an object")
    else:
        for field in ("can_introduce_or_miss_error", "reduces_or_replaces_required_process"):
            if not isinstance(reliance.get(field), bool):
                errors.append(f"tool_reliance.{field} must be boolean")
        detection = reliance.get("independent_error_detection")
        decision = reliance.get("decision")
        if detection not in DETECTION:
            errors.append(f"tool_reliance.independent_error_detection must be one of {sorted(DETECTION)}")
        if decision not in RELIANCE_DECISIONS:
            errors.append(f"tool_reliance.decision must be one of {sorted(RELIANCE_DECISIONS)}")
        for field in ("assessment_reference", "qualification_or_validation_reference"):
            if not _non_empty(reliance.get(field)):
                errors.append(f"tool_reliance.{field} must be a non-empty string")

    identity = record.get("execution_identity")
    if not isinstance(identity, dict):
        errors.append("execution_identity must be an object")
    else:
        for field in (
            "execution_id", "provider", "model_identifier", "model_version_reference",
            "weights_identity_value", "runtime_reference", "tokenizer_reference",
            "embedding_model_reference", "provider_request_reference",
        ):
            if not _non_empty(identity.get(field)):
                errors.append(f"execution_identity.{field} must be a non-empty string")
        identity_mode = identity.get("weights_identity_mode")
        if identity_mode not in WEIGHT_IDENTITY_MODES:
            errors.append(f"execution_identity.weights_identity_mode must be one of {sorted(WEIGHT_IDENTITY_MODES)}")
        elif identity_mode == "LOCAL_SHA256" and not _valid_sha256(identity.get("weights_identity_value")):
            errors.append("LOCAL_SHA256 weights identity requires a valid sha256 value")

    inference = record.get("inference_configuration")
    if not isinstance(inference, dict):
        errors.append("inference_configuration must be an object")
    else:
        for field in (
            "temperature", "top_p", "seed", "context_window", "retrieval_configuration_reference",
            "reproducibility_limitations",
        ):
            if not _non_empty(inference.get(field)):
                errors.append(f"inference_configuration.{field} must be a non-empty string")

    captures = record.get("capture_records")
    captured_categories: set[str] = set()
    if not isinstance(captures, list):
        errors.append("capture_records must be a list")
    else:
        for index, capture in enumerate(captures):
            if not isinstance(capture, dict):
                errors.append(f"capture_records[{index}] must be an object")
                continue
            if "content" in capture:
                errors.append(f"capture_records[{index}] must not embed raw content")
            category = capture.get("category")
            mode = capture.get("capture_mode")
            if category not in CAPTURE_CATEGORIES:
                errors.append(f"capture_records[{index}].category is invalid")
            elif category in captured_categories:
                errors.append(f"duplicate capture category: {category}")
            else:
                captured_categories.add(str(category))
            if mode not in CAPTURE_MODES:
                errors.append(f"capture_records[{index}].capture_mode is invalid")
            for field in ("classification", "retention_reference", "rationale"):
                if not _non_empty(capture.get(field)):
                    errors.append(f"capture_records[{index}].{field} must be a non-empty string")
            if capture.get("classification") not in CLASSIFICATIONS:
                errors.append(f"capture_records[{index}].classification is invalid")
            if mode == "NOT_RETAINED_WITH_RATIONALE":
                if not _non_empty(capture.get("reference")):
                    errors.append(f"capture_records[{index}] not-retained decision requires a decision reference")
            else:
                if not _non_empty(capture.get("reference")) or not _valid_sha256(capture.get("sha256")):
                    errors.append(f"capture_records[{index}] retained evidence requires reference and sha256")

    if not _non_empty(record.get("token_map_reference")) or not str(record.get("token_map_reference", "")).startswith(
        "SEPARATE_PROTECTED_VAULT:"
    ):
        errors.append("token_map_reference must point to a SEPARATE_PROTECTED_VAULT")
    verification = record.get("deterministic_verification_references")
    if not isinstance(verification, list) or not all(_non_empty(item) for item in verification):
        errors.append("deterministic_verification_references must be a string list")
    limitations = record.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(_non_empty(item) for item in limitations):
        errors.append("limitations must be a non-empty string list")

    human = record.get("human_review")
    if not isinstance(human, dict):
        errors.append("human_review must be an object")
    else:
        if not isinstance(human.get("required"), bool):
            errors.append("human_review.required must be boolean")
        if human.get("status") not in {"NOT_REQUIRED", "PENDING", "APPROVED", "REJECTED"}:
            errors.append("human_review.status is invalid")
        for field in (
            "reviewer_id", "competence_reference", "independence_reference", "review_scope_reference",
            "decision_reference", "reviewed_artifact_reference",
        ):
            if not _non_empty(human.get(field)):
                errors.append(f"human_review.{field} must be a non-empty string")

    if profile in {"E1_TRACEABLE_CANDIDATE", "E2_ASSURANCE_RELIANCE"}:
        missing = sorted(REQUIRED_E1_CATEGORIES - captured_categories)
        errors.extend(f"{profile} requires capture category {category}" for category in missing)
        if not verification:
            errors.append(f"{profile} requires deterministic verification references")
        if not isinstance(human, dict) or human.get("required") is not True:
            errors.append(f"{profile} requires human review")
    if decision == "NO_QUALIFICATION_INDEPENDENT_VERIFICATION" and detection != "COMPLETE":
        errors.append("independent-verification decision requires COMPLETE independent error detection")
    if decision == "QUALIFICATION_REQUIRED" and profile != "E2_ASSURANCE_RELIANCE":
        errors.append("QUALIFICATION_REQUIRED requires E2_ASSURANCE_RELIANCE")
    if status == "APPROVED_FOR_DECLARED_USE":
        if decision in {"QUALIFICATION_REQUIRED", "USE_PROHIBITED"}:
            errors.append("unresolved qualification-required or prohibited use cannot be approved")
        if profile != "E0_ADVISORY" and (
            not isinstance(human, dict)
            or human.get("status") != "APPROVED"
            or str(human.get("decision_reference", "")).strip().lower() in {"", "pending", "unverified"}
        ):
            errors.append("approved consequential record requires completed human review evidence")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate AI engineering decision evidence.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_ai_engineering_evidence(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid AI engineering decision evidence: " + "; ".join(errors))
    print("AI engineering evidence valid; tool qualification and engineering approval remain separate.")


if __name__ == "__main__":
    main()
