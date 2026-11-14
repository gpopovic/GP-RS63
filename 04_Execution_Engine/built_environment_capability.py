"""Validate built-environment capability jobs; never execute domain tools here."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LIFECYCLE = {"CANDIDATE", "SANDBOX", "VALIDATED", "APPROVED"}
ENVIRONMENTS = {"SANDBOX", "PRODUCT"}
ACTIONS = {"ANALYSE", "GENERATE", "VALIDATE", "PUBLISH"}
DATA_CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
COMMON_INPUTS = {
    "source_reference",
    "source_hash",
    "tool_name",
    "tool_version",
    "units",
    "assumptions",
    "uncertainties",
}
CAPABILITY_INPUTS = {
    "SH3D_INGEST": {"sh3d_version", "backup_reference", "level_convention", "evidence_layers", "missing_value_policy"},
    "IFC_IDS_VALIDATE": {"ifc_schema", "ids_reference", "ifc_library", "validation_profile", "issue_format"},
    "POINT_CLOUD_COMPARE": {"crs", "acquisition_method", "acquisition_date", "registration_method", "accuracy_evidence", "outlier_treatment", "reference_model"},
    "COST_PLAN": {"jurisdiction", "taxonomy", "taxonomy_version", "quantity_evidence", "currency", "price_date", "price_source", "tax_treatment", "contingency_method", "estimate_class"},
    "SCHEDULE_PLAN": {"project_context", "work_breakdown", "dependencies", "calendars", "resources", "constraints", "duration_sources"},
    "SITE_LOG": {"project_id", "log_date", "timezone", "weather_source", "observations", "evidence_attachments"},
    "SOLAR_SIMULATION": {"analysis_question", "location", "weather_reference", "geometry_reference", "orientation", "shading_context", "engine", "analysis_period", "timestep"},
    "MODEL_REVISION_DIFF": {"baseline_hash", "revision_hash", "stable_id_strategy", "geometry_tolerance", "semantic_fields", "duplicate_strategy"},
    "CONTROLLED_PUBLISH": {"template_reference", "template_version", "escaping_strategy", "source_manifest", "output_format", "output_validation"},
}


def _non_empty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def _valid_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(character in "0123456789abcdefABCDEF" for character in digest)


def validate_capability_job(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["capability job must be a JSON object"]
    job: dict[str, Any] = payload
    errors: list[str] = []
    for field in (
        "job_id",
        "capability",
        "lifecycle",
        "environment",
        "action",
        "product_workspace_id",
        "inputs",
        "output_reference",
        "data_classification",
        "accountable_owner",
        "independent_reviewer",
        "approval_reference",
    ):
        if not _non_empty(job.get(field)):
            errors.append(f"missing or empty field: {field}")

    capability = job.get("capability")
    if capability not in CAPABILITY_INPUTS:
        errors.append(f"capability must be one of {sorted(CAPABILITY_INPUTS)}")
    if job.get("lifecycle") not in LIFECYCLE:
        errors.append(f"lifecycle must be one of {sorted(LIFECYCLE)}")
    if job.get("environment") not in ENVIRONMENTS:
        errors.append(f"environment must be one of {sorted(ENVIRONMENTS)}")
    if job.get("action") not in ACTIONS:
        errors.append(f"action must be one of {sorted(ACTIONS)}")
    if job.get("data_classification") not in DATA_CLASSIFICATIONS:
        errors.append(f"data_classification must be one of {sorted(DATA_CLASSIFICATIONS)}")

    if job.get("environment") == "PRODUCT" and job.get("lifecycle") != "APPROVED":
        errors.append("PRODUCT execution requires lifecycle APPROVED")
    if job.get("environment") == "PRODUCT" and job.get("approval_reference") == "Pending":
        errors.append("PRODUCT execution requires a final approval_reference")
    if job.get("accountable_owner") == job.get("independent_reviewer"):
        errors.append("independent_reviewer must differ from accountable_owner")

    inputs = job.get("inputs")
    if not isinstance(inputs, dict):
        errors.append("inputs must be an object")
    elif capability in CAPABILITY_INPUTS:
        missing = sorted(
            field
            for field in COMMON_INPUTS | CAPABILITY_INPUTS[str(capability)]
            if not _non_empty(inputs.get(field))
        )
        errors.extend(f"inputs missing or empty: {field}" for field in missing)
        if not _valid_sha256(inputs.get("source_hash")):
            errors.append("inputs.source_hash must use sha256:<64 hexadecimal characters>")
        if capability == "SH3D_INGEST" and inputs.get("missing_value_policy") != "REJECT_OR_ESCALATE":
            errors.append("SH3D_INGEST missing_value_policy must be REJECT_OR_ESCALATE")
        if capability == "IFC_IDS_VALIDATE" and inputs.get("issue_format") != "BCF":
            errors.append("IFC_IDS_VALIDATE issue_format must be BCF")
        if capability == "SCHEDULE_PLAN" and inputs.get("project_context") not in {"EXISTING_BUILDING", "NEW_BUILD"}:
            errors.append("SCHEDULE_PLAN project_context must be EXISTING_BUILDING or NEW_BUILD")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a built-environment capability job manifest.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_capability_job(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid capability job: " + "; ".join(errors))
    print("Capability job contract valid; domain execution and approval remain separate.")


if __name__ == "__main__":
    main()
