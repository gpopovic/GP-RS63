"""Validate AI processing envelopes without granting access or executing a model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
CONSEQUENCES = {"LOW", "MATERIAL", "HIGH_CONSEQUENCE"}
MODEL_CLASSES = {"FLAGSHIP", "STANDARD", "WORKER"}
RETRIEVAL_BOUNDARIES = {"LOCAL_APPROVED", "CUSTOMER_APPROVED", "NO_RETRIEVAL"}
ROUTES = {"LOCAL_DEVICE_ONLY", "PRIVATE_SERVER_APPROVED", "EU_EEA_APPROVED", "US_EXCEPTION", "CN_EXCEPTION"}
EXTERNAL_ROUTES = {"EU_EEA_APPROVED", "US_EXCEPTION", "CN_EXCEPTION"}
DECISIONS = {"DRAFT", "BLOCKED", "READY_FOR_EXECUTION_REVIEW"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(character in "0123456789abcdefABCDEF" for character in digest)


def validate_ai_processing_envelope(payload: object) -> list[str]:
    """Return contract errors; a valid record is still not execution approval."""
    if not isinstance(payload, dict):
        return ["AI processing envelope must be a JSON object"]
    record: dict[str, Any] = payload
    errors: list[str] = []
    required = (
        "request_id", "workspace_id", "domain_profile_id", "purpose", "task_class", "consequence",
        "data_classification", "source_references", "retrieval_boundary", "applicability_record_reference",
        "sanitisation", "permitted_routes", "selected_route", "route_approval_reference", "model_class",
        "model_identifier", "provider", "logging", "output_schema_reference", "deterministic_validators",
        "human_gate", "access_decision_reference", "cost_cap_reference", "stop_conditions", "decision_status",
    )
    for field in required:
        if field not in record:
            errors.append(f"missing field: {field}")
    for field in (
        "request_id", "workspace_id", "domain_profile_id", "purpose", "task_class",
        "applicability_record_reference", "route_approval_reference", "model_identifier", "provider",
        "output_schema_reference", "access_decision_reference", "cost_cap_reference",
    ):
        if field in record and not _non_empty(record[field]):
            errors.append(f"{field} must be a non-empty string")

    classification = record.get("data_classification")
    if classification not in CLASSIFICATIONS:
        errors.append(f"data_classification must be one of {sorted(CLASSIFICATIONS)}")
    if record.get("consequence") not in CONSEQUENCES:
        errors.append(f"consequence must be one of {sorted(CONSEQUENCES)}")
    if record.get("model_class") not in MODEL_CLASSES:
        errors.append(f"model_class must be one of {sorted(MODEL_CLASSES)}")
    if record.get("retrieval_boundary") not in RETRIEVAL_BOUNDARIES:
        errors.append(f"retrieval_boundary must be one of {sorted(RETRIEVAL_BOUNDARIES)}")
    if record.get("decision_status") not in DECISIONS:
        errors.append(f"decision_status must be one of {sorted(DECISIONS)}")

    sources = record.get("source_references")
    if not isinstance(sources, list) or not sources:
        errors.append("source_references must be a non-empty list")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"source_references[{index}] must be an object")
                continue
            for field in ("source_id", "classification", "authorisation_reference"):
                if not _non_empty(source.get(field)):
                    errors.append(f"source_references[{index}].{field} must be a non-empty string")
            if source.get("classification") not in CLASSIFICATIONS:
                errors.append(f"source_references[{index}].classification is invalid")
            if not _valid_sha256(source.get("sha256")):
                errors.append(f"source_references[{index}].sha256 must use sha256:<64 hexadecimal characters>")

    permitted = record.get("permitted_routes")
    selected = record.get("selected_route")
    if not isinstance(permitted, list) or not permitted or not all(route in ROUTES for route in permitted):
        errors.append("permitted_routes must be a non-empty list of controlled routes")
    if selected not in ROUTES:
        errors.append(f"selected_route must be one of {sorted(ROUTES)}")
    elif isinstance(permitted, list) and selected not in permitted:
        errors.append("selected_route must be included in permitted_routes")

    sanitisation = record.get("sanitisation")
    sanitisation_ready = False
    if not isinstance(sanitisation, dict):
        errors.append("sanitisation must be an object")
    else:
        required_sanitisation = sanitisation.get("required")
        if not isinstance(required_sanitisation, bool):
            errors.append("sanitisation.required must be boolean")
        if sanitisation.get("status") not in {"NOT_REQUIRED", "PENDING", "PASSED", "FAILED"}:
            errors.append("sanitisation.status is invalid")
        sanitisation_ready = (
            required_sanitisation is True
            and sanitisation.get("status") == "PASSED"
            and _non_empty(sanitisation.get("profile_reference"))
            and sanitisation.get("token_map_location") == "LOCAL_CONTROLLED"
        )
        if selected in EXTERNAL_ROUTES and not sanitisation_ready:
            errors.append("external routes require passed sanitisation and a LOCAL_CONTROLLED token map")

    logging = record.get("logging")
    if not isinstance(logging, dict):
        errors.append("logging must be an object")
    else:
        if logging.get("mode") not in {"METADATA_ONLY", "CONTENT_APPROVED", "DISABLED"}:
            errors.append("logging.mode is invalid")
        if not isinstance(logging.get("content_logging"), bool):
            errors.append("logging.content_logging must be boolean")
        if not _non_empty(logging.get("retention_reference")):
            errors.append("logging.retention_reference must be a non-empty string")
        if classification != "PUBLIC" and logging.get("content_logging") is True:
            errors.append("non-public processing must not enable content logging in the standard envelope")

    validators = record.get("deterministic_validators")
    if not isinstance(validators, list) or not validators or not all(_non_empty(item) for item in validators):
        errors.append("deterministic_validators must be a non-empty string list")
    stops = record.get("stop_conditions")
    if not isinstance(stops, list) or not stops or not all(_non_empty(item) for item in stops):
        errors.append("stop_conditions must be a non-empty string list")

    human_gate = record.get("human_gate")
    gate_ready = False
    if not isinstance(human_gate, dict):
        errors.append("human_gate must be an object")
    else:
        if not isinstance(human_gate.get("required"), bool):
            errors.append("human_gate.required must be boolean")
        if human_gate.get("status") not in {"NOT_REQUIRED", "PENDING", "APPROVED", "DENIED"}:
            errors.append("human_gate.status is invalid")
        gate_ready = human_gate.get("required") is True and _non_empty(human_gate.get("owner"))
        if classification in {"CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"} or record.get("consequence") != "LOW":
            if not gate_ready:
                errors.append("sensitive or consequential processing requires a named human gate")

    if record.get("decision_status") == "READY_FOR_EXECUTION_REVIEW":
        for field in ("route_approval_reference", "access_decision_reference", "cost_cap_reference"):
            if str(record.get(field, "")).strip().lower() in {"", "pending", "unverified"}:
                errors.append(f"READY_FOR_EXECUTION_REVIEW requires final {field}")
        if selected in EXTERNAL_ROUTES and not sanitisation_ready:
            errors.append("READY_FOR_EXECUTION_REVIEW cannot use an unprotected external route")
        if not gate_ready and (classification != "PUBLIC" or record.get("consequence") != "LOW"):
            errors.append("READY_FOR_EXECUTION_REVIEW requires a configured human gate")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an AI processing envelope.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_ai_processing_envelope(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid AI processing envelope: " + "; ".join(errors))
    print("AI processing envelope valid; access and execution approval remain separate.")


if __name__ == "__main__":
    main()
