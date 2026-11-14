"""Guard the project-local Codex profile against known unsafe process claims."""

from __future__ import annotations

from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
TRITON_ROOT = ENGINE_DIR.parent
PROFILE_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "CODEX_SELF_CORRECTION_AND_EXECUTION_PROFILE.md"
LEAN_POLICY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "LEAN_ASSURANCE_AND_PROCESS_TAILORING_POLICY.md"
CONFIGURATION_POLICY_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "COMPANY_CONFIGURATION_MANAGEMENT.md"
MANUAL_PATH = TRITON_ROOT / "00_Corp_DNA" / "TRITON_AI_CORP_MASTER_OPERATING_MANUAL.md"
AGENT_RULES_PATH = TRITON_ROOT / "AGENTS.md"
ROLE_DIR = TRITON_ROOT / "02_Organization_and_Roles" / "Roles_Descriptions"


def main() -> None:
    profile = PROFILE_PATH.read_text(encoding="utf-8")
    lean_policy = LEAN_POLICY_PATH.read_text(encoding="utf-8")
    configuration_policy = CONFIGURATION_POLICY_PATH.read_text(encoding="utf-8")
    manual = MANUAL_PATH.read_text(encoding="utf-8")
    agent_rules = AGENT_RULES_PATH.read_text(encoding="utf-8")

    required_profile_rules = (
        "smallest sufficient quality contract",
        "Do not invent universal percentages",
        "Do not equate test success",
        "Never infer access or approval from a role title",
        "Treat external review packages as evidence candidates",
        "smallest useful vertical slice",
        "Every new control must name the specific failure mode or obligation",
        "control volume is not delivered business value",
        "not restricted to a permanent auditor role",
        "Do not call a weighted ranking",
        "Treat decision-facing dashboards as evidence projections",
        "Keep tests hermetic unless a named integration environment is explicitly admitted",
        "Select `RULE_BOUND` or `EXPLORATORY` work explicitly",
        "When the user explicitly reports low energy",
        "Audit Communication Contract",
        "bottom-line-up-front triage",
        "Severity describes supported consequence and exploitability",
        "Use CVSS only for a technically scoped vulnerability",
        "EXPLORATORY_SPIKE",
        "PARTIALLY_REMEDIATED",
        "non-authoritative remediation annex",
    )
    for rule in required_profile_rules:
        assert rule in profile, f"Missing Codex execution guardrail: {rule}"

    required_lean_rules = (
        "thin vertical slice",
        "do not create a separate cleanup board",
        "no observed consumer",
        "operational outcome effort",
    )
    for rule in required_lean_rules:
        assert rule in lean_policy, f"Missing lean anti-bureaucracy rule: {rule}"

    required_kpi_visualisation_rules = (
        "evidence projection, not a substitute for the underlying record",
        "`DEMONSTRATION` or `NOT_ASSESSED`",
        "not imported as universal benchmarks",
    )
    for rule in required_kpi_visualisation_rules:
        assert rule in (TRITON_ROOT / "01_Governance_and_Strategy" / "KPI_MEASUREMENT_AND_COST_CONTROL.md").read_text(encoding="utf-8"), (
            f"Missing dashboard-evidence rule: {rule}"
        )

    assurance_flow = (TRITON_ROOT / "01_Governance_and_Strategy" / "AI_PROCESSING_AND_ASSURANCE_FLOW.md").read_text(
        encoding="utf-8"
    )
    for rule in (
        "controlled and versioned, not immutable",
        "No MCP, model, second agent, or named tool is mandatory",
        "Fixed loop counts and telemetry thresholds are not universal company rules",
        "does not by itself establish maturity, fitness for use",
    ):
        assert rule in assurance_flow, f"Missing producer-verifier safeguard: {rule}"

    mcp_policy = (TRITON_ROOT / "04_Execution_Engine" / "MCP_Registry" / "MCP_ADMISSION_AND_CAPABILITY_POLICY.md").read_text(
        encoding="utf-8"
    )
    for rule in (
        "Tool selection is a constrained decision",
        "do not invent universal scores or timings",
        "may not silently change permissions, data boundary, provider, jurisdiction, cost authority, or mutation scope",
        "invoking a tool does not make its output true or complete",
    ):
        assert rule in mcp_policy, f"Missing tool-orchestration safeguard: {rule}"

    required_configuration_rules = (
        "unique failure mode or obligation",
        "TRIGGERED_DORMANT",
        "do not maintain a second inventory",
    )
    for rule in required_configuration_rules:
        assert rule in configuration_policy, f"Missing configuration consolidation rule: {rule}"

    assert PROFILE_PATH.name in agent_rules

    prohibited_manual_claims = (
        "ASPICE Level 5",
        "absolute zero-error",
        "CORPORATE_PULSE_STATE.json",
        "85/15",
        "universal 3-level",
    )
    for claim in prohibited_manual_claims:
        assert claim.casefold() not in manual.casefold(), f"Unsafe manual claim returned: {claim}"

    role_claims = {
        "Lead_AI_Research_Scientist.md": "zero hallucination",
        "Embodied_AI_and_Robotics_Engineer.md": "guarantee collision avoidance",
        "Model_Training_and_Optimization_Engineer.md": "production-grade model artifacts",
    }
    for role_name, claim in role_claims.items():
        role_text = (ROLE_DIR / role_name).read_text(encoding="utf-8")
        assert claim.casefold() not in role_text.casefold(), f"Unsafe role claim returned: {role_name}"

    print("Codex self-correction and execution profile tests passed.")


if __name__ == "__main__":
    main()
