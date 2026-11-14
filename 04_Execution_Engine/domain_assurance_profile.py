"""Validate domain-profile configuration without activating a regulated scope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from config import TRITON_ROOT

CATALOG_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "DOMAIN_ASSURANCE_PROFILE_CATALOG.json"
PROFILE_IDS = {
    "AUTOMOTIVE",
    "INDUSTRIAL_AUTOMATION",
    "MEDICAL_DEVICE",
    "AEROSPACE",
    "RAIL",
    "MARINE",
    "BUILT_ENVIRONMENT",
}
CATALOG_STATUSES = {"TEMPLATE_NOT_ACTIVATED", "CANDIDATE", "APPROVED"}
PROJECT_STATUSES = {"DRAFT_NOT_APPROVED", "REVIEW_REQUIRED", "APPROVED"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_domain_catalog(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["domain assurance catalog must be a JSON object"]
    errors: list[str] = []
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    activation = payload.get("activation_requires")
    if not isinstance(activation, list) or len(activation) < 5 or not all(_non_empty(item) for item in activation):
        errors.append("activation_requires must contain at least five non-empty controls")
    profiles = payload.get("profiles")
    if not isinstance(profiles, list):
        return errors + ["profiles must be a list"]
    seen: set[str] = set()
    for index, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            errors.append(f"profiles[{index}] must be an object")
            continue
        profile_id = profile.get("id")
        if profile_id not in PROFILE_IDS:
            errors.append(f"profiles[{index}].id must be a controlled profile ID")
        elif profile_id in seen:
            errors.append(f"duplicate domain profile: {profile_id}")
        else:
            seen.add(str(profile_id))
        if profile.get("status") not in CATALOG_STATUSES:
            errors.append(f"profiles[{index}].status is invalid")
        for field in ("accountable_role",):
            if not _non_empty(profile.get(field)):
                errors.append(f"profiles[{index}].{field} must be a non-empty string")
        for field in ("candidate_source_families", "special_controls"):
            value = profile.get(field)
            if not isinstance(value, list) or not value or not all(_non_empty(item) for item in value):
                errors.append(f"profiles[{index}].{field} must be a non-empty string list")
    if seen != PROFILE_IDS:
        errors.append(f"catalog profile coverage mismatch: {sorted(PROFILE_IDS - seen)}")
    return errors


def validate_project_assurance_profile(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["project assurance profile must be a JSON object"]
    record: dict[str, Any] = payload
    errors: list[str] = []
    string_fields = (
        "workspace_id", "profile_version", "domain_profile_id", "profile_status", "intended_use",
        "product_boundary", "applicability_record_reference", "toolchain_and_qualification_reference",
        "data_flow_reference", "configuration_baseline_reference", "quality_manager_review",
        "domain_human_approval",
    )
    for field in string_fields:
        if not _non_empty(record.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if record.get("domain_profile_id") not in PROFILE_IDS:
        errors.append(f"domain_profile_id must be one of {sorted(PROFILE_IDS)}")
    if record.get("profile_status") not in PROJECT_STATUSES:
        errors.append(f"profile_status must be one of {sorted(PROJECT_STATUSES)}")
    for field in ("jurisdictions_and_markets", "source_register_references", "required_independence", "human_approval_authorities", "prohibited_ai_decisions"):
        value = record.get(field)
        if not isinstance(value, list) or not value or not all(_non_empty(item) for item in value):
            errors.append(f"{field} must be a non-empty string list")
    classification = record.get("assurance_classification")
    if not isinstance(classification, dict) or not all(
        _non_empty(classification.get(field)) for field in ("scheme", "level", "rationale_reference")
    ):
        errors.append("assurance_classification must define scheme, level, and rationale_reference")
    if record.get("profile_status") == "APPROVED":
        pending_values = {
            "toolchain_and_qualification_reference": record.get("toolchain_and_qualification_reference"),
            "configuration_baseline_reference": record.get("configuration_baseline_reference"),
            "quality_manager_review": record.get("quality_manager_review"),
            "domain_human_approval": record.get("domain_human_approval"),
        }
        for field, value in pending_values.items():
            if str(value).strip().lower() in {"pending", "unverified"}:
                errors.append(f"APPROVED profile requires final {field}")
        if any("VERIFY" in item.upper() for item in record.get("jurisdictions_and_markets", [])):
            errors.append("APPROVED profile requires verified jurisdictions_and_markets")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate domain assurance configuration.")
    parser.add_argument("path", nargs="?", type=Path, default=CATALOG_PATH)
    parser.add_argument("--project-profile", action="store_true")
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_project_assurance_profile(payload) if args.project_profile else validate_domain_catalog(payload)
    if errors:
        raise SystemExit("Invalid domain assurance configuration: " + "; ".join(errors))
    print("Domain assurance configuration valid; activation and applicability approval remain separate.")


if __name__ == "__main__":
    main()
