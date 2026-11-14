"""Regression checks for decision-ready, phase-aware audit reporting."""

from __future__ import annotations

from config import TRITON_ROOT

BRIEF = (
    TRITON_ROOT
    / "05_Human_Interface_and_Ops"
    / "Manual_Quality_Gates"
    / "ANTIGRAVITY_REMEDIATION_FOLLOWUP_DECISION_BRIEF_2026-08-29.md"
)
ANNEX = BRIEF.with_name("ANTIGRAVITY_GEMBA_REMEDIATION_ANNEX_2026-08-29.md")


def main() -> None:
    brief = BRIEF.read_text(encoding="utf-8")
    annex = ANNEX.read_text(encoding="utf-8")

    for required in (
        "## BLUF",
        "## Decision Triage",
        "Priority | Severity",
        "Exploratory spike",
        "Controlled pilot",
        "Production release",
        "PARTIALLY_REMEDIATED",
        "Observed evidence",
        "Acceptance evidence",
        "no formal CVSS vector is asserted",
    ):
        assert required in brief, f"Missing audit decision element: {required}"

    for required in (
        "Non-Authoritative Remediation Annex",
        "Do not use `str(target).startswith(str(base))`",
        "Minimum Negative-Test Set",
        "Loopback is transport containment, not identity",
    ):
        assert required in annex, f"Missing remediation-annex element: {required}"

    assert "| `CRITICAL` |" not in brief.split("## Decision Triage", 1)[1].split("## Material Findings", 1)[0]
    print("Audit decision brief and remediation annex checks passed.")


if __name__ == "__main__":
    main()
