"""Regression checks for the controlled 2026-08-29 Antigravity adaptation."""

from __future__ import annotations

import json

from config import TRITON_ROOT
from external_review_disposition import validate_external_review_disposition


def _read(relative_path: str) -> str:
    return (TRITON_ROOT / relative_path).read_text(encoding="utf-8")


def main() -> None:
    onboarding = _read("01_Governance_and_Strategy/CUSTOMER_ONBOARDING_AND_VALUE_REALISATION_PLAYBOOK.md")
    incident = _read("01_Governance_and_Strategy/SECURITY_INCIDENT_RESPONSE_CONTROL.md")
    insurance = _read("01_Governance_and_Strategy/ENTERPRISE_RISK_TRANSFER_AND_INSURANCE_CONTROL.md")
    pulse = _read("01_Governance_and_Strategy/EVIDENCE_BACKED_CORPORATE_PULSE.md")
    pricing = _read("01_Governance_and_Strategy/COMMERCIAL_PRICING_POLICY.md")
    built_environment = _read("01_Governance_and_Strategy/BUILT_ENVIRONMENT_DELIVERY_FRAMEWORK.md")

    assert "No universal two-hour welcome" in onboarding
    assert "A checksum proves identity of bytes" in incident
    assert "Missing policy wording is `NOT_ASSESSED`" in insurance
    assert "schema-valid request" in incident
    assert "Invalid input fails closed" in pulse
    assert "does not establish scope" in insurance
    assert "may not compress safety" in pricing
    assert "Payment and contractual acceptance remain separate" in built_environment

    register_path = (
        TRITON_ROOT
        / "05_Human_Interface_and_Ops"
        / "External_Review_Intake"
        / "ANTIGRAVITY_INCREMENTAL_CAPABILITY_DISPOSITION_REGISTER_2026-08-29.json"
    )
    register = json.loads(register_path.read_text(encoding="utf-8"))
    assert validate_external_review_disposition(register) == []
    paths = [path for item in register["items"] for path in item["changed_paths"]]
    assert len(paths) == register["reviewed_path_count"] == 24
    assert len(paths) == len(set(paths))

    manifest_path = register_path.with_name("ANTIGRAVITY_INCREMENT_MANIFEST_2026-08-29.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_paths = [item["path"] for item in manifest["files"]]
    assert manifest["head_commit_inclusive"] == "be4ffdb5e5ed92c738141bca829da9ceea7e803b"
    assert manifest["commit_count"] == len(manifest["commits"]) == 10
    assert manifest["changed_path_count"] == len(manifest_paths) == 24
    assert sorted(manifest_paths) == sorted(paths)
    assert all(len(item["sha256"]) == 64 for item in manifest["files"])
    print("Antigravity incremental adaptation checks passed.")


if __name__ == "__main__":
    main()
