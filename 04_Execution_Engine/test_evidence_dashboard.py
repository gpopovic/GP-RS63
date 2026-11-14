"""Tests for accessible evidence dashboard rendering."""

from copy import deepcopy

from evidence_dashboard import render_dashboard, validate_dashboard


def example() -> dict[str, object]:
    return {
        "dashboard_id": "synthetic-option-review",
        "title": "Synthetic <Option> Review",
        "evidence_state": "DEMONSTRATION",
        "as_of": "2026-08-28T21:00:00+02:00",
        "owner": "Continuous_Improvement_Architect",
        "decision_use": "Demonstrate evidence-bound KPI explanations.",
        "metrics": [
            {
                "metric_id": "admissible-options",
                "label": "Admissible options",
                "value": "3",
                "unit": "options",
                "formula": "count(options satisfying every required constraint)",
                "source_reference": "synthetic://creative-option-test",
                "owner": "Product_Owner",
                "population": "four synthetic options",
                "confidence": "deterministic fixture",
                "data_quality_state": "SYNTHETIC",
                "decision_use": "Verify the dashboard contract only.",
            }
        ],
    }


def main() -> None:
    payload = example()
    assert validate_dashboard(payload) == []
    html = render_dashboard(payload)
    assert "Synthetic &lt;Option&gt; Review" in html
    assert "<details>" in html and "<summary>" in html
    assert "https://" not in html and "<script" not in html

    missing_source = deepcopy(payload)
    missing_source["metrics"][0]["source_reference"] = ""  # type: ignore[index]
    assert any("source_reference" in error for error in validate_dashboard(missing_source))

    unsupported_target = deepcopy(payload)
    unsupported_target["metrics"][0]["target"] = "95%"  # type: ignore[index]
    assert any("target_source_reference" in error for error in validate_dashboard(unsupported_target))
    print("Evidence dashboard tests passed.")


if __name__ == "__main__":
    main()
