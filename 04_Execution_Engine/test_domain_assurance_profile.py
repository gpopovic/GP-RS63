"""Tests for fail-closed domain profile activation."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from domain_assurance_profile import validate_domain_catalog, validate_project_assurance_profile


def project_profile() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Project_Assurance_Templates" / "PROJECT_ASSURANCE_PROFILE.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    catalog_path = TRITON_ROOT / "01_Governance_and_Strategy" / "DOMAIN_ASSURANCE_PROFILE_CATALOG.json"
    assert validate_domain_catalog(json.loads(catalog_path.read_text(encoding="utf-8"))) == []
    assert validate_project_assurance_profile(project_profile()) == []

    invalid_domain = project_profile()
    invalid_domain["domain_profile_id"] = "UNIVERSAL"
    assert any("domain_profile_id must be one of" in error for error in validate_project_assurance_profile(invalid_domain))

    premature = deepcopy(project_profile())
    premature["profile_status"] = "APPROVED"
    errors = validate_project_assurance_profile(premature)
    assert any("requires final quality_manager_review" in error for error in errors)
    assert "APPROVED profile requires verified jurisdictions_and_markets" in errors
    print("Domain assurance profile tests passed.")


if __name__ == "__main__":
    main()
