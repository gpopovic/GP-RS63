"""Validate software release evidence manifests without authorising a release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DECISIONS = {"NEEDS_EVIDENCE", "BLOCKED", "READY_FOR_RELEASE_REVIEW"}
WORKFLOW_IDS = {"save_reopen", "undo_redo", "export_determinism", "ambiguity_safety"}


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(character in "0123456789abcdefABCDEF" for character in digest)


def _count_pair(block: object, field: str, errors: list[str]) -> tuple[int, int] | None:
    if not isinstance(block, dict):
        errors.append(f"{field} must be an object")
        return None
    total = block.get("total")
    passed = block.get("passed")
    if (
        isinstance(total, bool)
        or isinstance(passed, bool)
        or not isinstance(total, int)
        or not isinstance(passed, int)
        or total < 0
        or passed < 0
        or passed > total
    ):
        errors.append(f"{field}.total and {field}.passed must be non-negative integer counts with passed <= total")
        return None
    return total, passed


def validate_software_release_evidence(payload: object) -> list[str]:
    """Return evidence-contract errors; an empty result is not a release approval."""
    if not isinstance(payload, dict):
        return ["software release evidence must be a JSON object"]

    record: dict[str, Any] = payload
    errors: list[str] = []
    for field in (
        "workspace_id",
        "work_item_id",
        "candidate_version",
        "source_revision",
        "artifact_sha256",
        "executed_at_utc",
        "test_environment",
        "fixture_set",
        "requirements_p0",
        "blocking_tests",
        "protected_state",
        "workflow_checks",
        "clean_build",
        "live_observation",
        "claim_derivation",
        "evidence_references",
        "raw_log_references",
        "rollback_reference",
        "independent_reviewer",
        "limitations",
        "decision",
    ):
        if field not in record:
            errors.append(f"missing field: {field}")

    for field in (
        "workspace_id",
        "work_item_id",
        "candidate_version",
        "source_revision",
        "executed_at_utc",
        "test_environment",
        "fixture_set",
        "rollback_reference",
        "independent_reviewer",
    ):
        if field in record and not _non_empty(record[field]):
            errors.append(f"{field} must be a non-empty string")

    if not _valid_sha256(record.get("artifact_sha256")):
        errors.append("artifact_sha256 must use sha256:<64 hexadecimal characters>")

    decision = record.get("decision")
    if decision not in DECISIONS:
        errors.append(f"decision must be one of {sorted(DECISIONS)}")

    p0 = _count_pair(record.get("requirements_p0"), "requirements_p0", errors)
    blocking = _count_pair(record.get("blocking_tests"), "blocking_tests", errors)

    protected = record.get("protected_state")
    protected_counts: tuple[int, int, int] | None = None
    if not isinstance(protected, dict):
        errors.append("protected_state must be an object")
    else:
        values = tuple(protected.get(name) for name in ("checked", "unchanged", "unexpected_mutations"))
        if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in values):
            errors.append("protected_state counts must be non-negative integers")
        elif values[1] > values[0]:
            errors.append("protected_state.unchanged must not exceed protected_state.checked")
        else:
            protected_counts = values  # type: ignore[assignment]

    workflows = record.get("workflow_checks")
    workflow_results: dict[str, tuple[bool, int, int, bool]] = {}
    if not isinstance(workflows, list):
        errors.append("workflow_checks must be a list")
    else:
        for index, workflow in enumerate(workflows):
            if not isinstance(workflow, dict):
                errors.append(f"workflow_checks[{index}] must be an object")
                continue
            workflow_id = workflow.get("id")
            if workflow_id not in WORKFLOW_IDS:
                errors.append(f"workflow_checks[{index}].id must be one of {sorted(WORKFLOW_IDS)}")
                continue
            if workflow_id in workflow_results:
                errors.append(f"duplicate workflow check: {workflow_id}")
                continue
            applicable = workflow.get("applicable")
            if not isinstance(applicable, bool):
                errors.append(f"workflow_checks[{index}].applicable must be boolean")
                continue
            counts = _count_pair(workflow, f"workflow_checks[{index}]", errors)
            evidence_present = _non_empty(workflow.get("evidence_reference"))
            if applicable and not evidence_present:
                errors.append(f"workflow_checks[{index}].evidence_reference is required when applicable")
            if not applicable and not _non_empty(workflow.get("not_applicable_rationale")):
                errors.append(f"workflow_checks[{index}].not_applicable_rationale is required when not applicable")
            if counts:
                workflow_results[str(workflow_id)] = (applicable, counts[0], counts[1], evidence_present)
        missing_workflows = sorted(WORKFLOW_IDS - workflow_results.keys())
        errors.extend(f"missing workflow check: {workflow_id}" for workflow_id in missing_workflows)

    clean_build = _count_pair(record.get("clean_build"), "clean_build", errors)

    live_observation = record.get("live_observation")
    live_ready = False
    if not isinstance(live_observation, dict):
        errors.append("live_observation must be an object")
    else:
        required = live_observation.get("required")
        status = live_observation.get("status")
        if not isinstance(required, bool):
            errors.append("live_observation.required must be boolean")
        if status not in {"NOT_REQUIRED", "PENDING", "PASSED"}:
            errors.append("live_observation.status must be NOT_REQUIRED, PENDING, or PASSED")
        if required:
            live_ready = status == "PASSED" and _non_empty(live_observation.get("evidence_reference"))
        else:
            live_ready = status == "NOT_REQUIRED" and _non_empty(
                live_observation.get("not_required_rationale")
            )

    for field in ("evidence_references", "raw_log_references", "limitations"):
        value = record.get(field)
        if not isinstance(value, list) or not all(_non_empty(item) for item in value):
            errors.append(f"{field} must be a list of non-empty strings")

    if decision == "READY_FOR_RELEASE_REVIEW":
        if not p0 or p0[0] == 0 or p0[1] != p0[0]:
            errors.append("READY_FOR_RELEASE_REVIEW requires all P0 requirements to pass")
        if not blocking or blocking[0] == 0 or blocking[1] != blocking[0]:
            errors.append("READY_FOR_RELEASE_REVIEW requires all blocking tests to pass")
        if not protected_counts or protected_counts[0] == 0 or protected_counts[1] != protected_counts[0] or protected_counts[2] != 0:
            errors.append("READY_FOR_RELEASE_REVIEW requires complete protected-state preservation and zero unexpected mutations")
        for workflow_id, (applicable, total, passed, evidence_present) in workflow_results.items():
            if applicable and (total == 0 or passed != total or not evidence_present):
                errors.append(f"READY_FOR_RELEASE_REVIEW requires applicable workflow {workflow_id} to pass with evidence")
        if not clean_build or clean_build[0] == 0 or clean_build[1] != clean_build[0]:
            errors.append("READY_FOR_RELEASE_REVIEW requires reproducible clean builds")
        if not live_ready:
            errors.append("READY_FOR_RELEASE_REVIEW requires a resolved live-observation disposition")
        if record.get("claim_derivation") != "MACHINE_DERIVED":
            errors.append("READY_FOR_RELEASE_REVIEW requires MACHINE_DERIVED claim_derivation")
        if not record.get("evidence_references") or not record.get("raw_log_references"):
            errors.append("READY_FOR_RELEASE_REVIEW requires evidence and raw-log references")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a software release evidence manifest.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_software_release_evidence(json.loads(args.path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("Invalid software release evidence: " + "; ".join(errors))
    print("Software release evidence contract valid; release approval remains separate.")


if __name__ == "__main__":
    main()
