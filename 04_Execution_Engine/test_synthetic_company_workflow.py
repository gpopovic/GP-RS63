"""Hermetic end-to-end test from option evidence to an accessible dashboard."""

from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from creative_option_analysis import ConstraintEvidence, Objective, OptionCandidate, analyse_options
from evidence_dashboard import render_dashboard


def main() -> None:
    objectives = (
        Objective("effort", "MINIMISE", "hours", "synthetic://source/effort"),
        Objective("evidence", "MAXIMISE", "accepted-items", "synthetic://source/evidence"),
    )
    candidates = (
        OptionCandidate("LEAN", "Lean route", (("effort", "4"), ("evidence", "4")), (ConstraintEvidence("privacy", True, "synthetic://privacy/lean"),), ("synthetic://lean",)),
        OptionCandidate("STANDARD", "Standard route", (("effort", "6"), ("evidence", "8")), (ConstraintEvidence("privacy", True, "synthetic://privacy/standard"),), ("synthetic://standard",)),
        OptionCandidate("UNSAFE", "Unsafe shortcut", (("effort", "1"), ("evidence", "9")), (ConstraintEvidence("privacy", False, "synthetic://privacy/unsafe"),), ("synthetic://unsafe",)),
    )
    analysis = analyse_options(
        decision_question="Which synthetic route remains eligible for human review?",
        human_decision_owner="Product_Owner",
        objectives=objectives,
        required_constraint_ids=("privacy",),
        candidates=candidates,
    )
    assert analysis.pareto_front_option_ids == ("LEAN", "STANDARD")
    assert analysis.rejected_options[0].option_id == "UNSAFE"

    dashboard = {
        "dashboard_id": "synthetic-company-workflow",
        "title": "Synthetic Company Workflow",
        "evidence_state": "DEMONSTRATION",
        "as_of": "2026-08-28T21:00:00+02:00",
        "owner": "Product_Owner",
        "decision_use": "Verify option-analysis to dashboard integration without a release decision.",
        "metrics": [
            {
                "metric_id": "pareto-options",
                "label": "Non-dominated admissible options",
                "value": str(len(analysis.pareto_front_option_ids)),
                "unit": "options",
                "formula": "count(non-dominated options after hard constraints)",
                "source_reference": "synthetic://creative-option-analysis/result",
                "owner": analysis.human_decision_owner,
                "population": f"{len(candidates)} synthetic route options",
                "confidence": "deterministic synthetic fixture",
                "data_quality_state": "SYNTHETIC",
                "decision_use": "Confirm interface and preserve the human decision boundary.",
            }
        ],
    }
    with TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "dashboard.html"
        output.write_text(render_dashboard(dashboard), encoding="utf-8")
        rendered = output.read_text(encoding="utf-8")
        assert "DEMONSTRATION" in rendered
        assert "Product_Owner" in rendered
        assert "<details>" in rendered
    assert not output.exists()
    print("Synthetic option-to-dashboard workflow passed in an isolated temporary directory.")


if __name__ == "__main__":
    main()
