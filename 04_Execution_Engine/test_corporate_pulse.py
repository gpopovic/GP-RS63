"""Tests for evidence-backed corporate pulse generation."""

from corporate_pulse import build_pulse


def valid_statement() -> dict[str, str]:
    return {
        "statement_id": "PULSE-001",
        "category": "FACT",
        "statement": "The controlled configuration index exists.",
        "evidence_reference": "01_Governance_and_Strategy/COMPANY_CONFIGURATION_INDEX.json",
        "source_type": "CONTROLLED_CORP_RECORD",
        "observed_at_utc": "2026-08-21T10:00:00Z",
        "owner": "Configuration_Manager",
        "confidence": "HIGH",
        "data_classification": "INTERNAL",
    }


def main() -> None:
    grouped, errors = build_pulse([valid_statement()])
    assert errors == []
    assert grouped["FACT"][0]["statement_id"] == "PULSE-001"

    unsupported = valid_statement()
    unsupported["evidence_reference"] = "missing/status.json"
    grouped, errors = build_pulse([unsupported])
    assert grouped["FACT"] == []
    assert any("existing Corp file" in error for error in errors)

    project_claim = valid_statement()
    project_claim["source_type"] = "SANITISED_PROJECT_EXPORT"
    grouped, errors = build_pulse([project_claim])
    assert any("export_validation_reference" in error for error in errors)

    duplicate = valid_statement()
    grouped, errors = build_pulse([valid_statement(), duplicate])
    assert len(grouped["FACT"]) == 1
    assert any("duplicate statement_id" in error for error in errors)
    print("Corporate pulse tests passed.")


if __name__ == "__main__":
    main()
