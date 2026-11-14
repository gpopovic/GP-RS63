"""Run the fixed, local Triton_AI_Corp baseline checks without executing index strings."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
CHECKS = (
    ENGINE_DIR / "validate_company_configuration.py",
    ENGINE_DIR / "test_codex_execution_profile.py",
    ENGINE_DIR / "validate_role_registry.py",
    ENGINE_DIR / "validate_role_human_names.py",
    ENGINE_DIR / "validate_role_communication_signatures.py",
    ENGINE_DIR / "test_role_loader.py",
    ENGINE_DIR / "test_kpi_cost_engine.py",
    ENGINE_DIR / "test_project_workspace.py",
    ENGINE_DIR / "test_harness_router.py",
    ENGINE_DIR / "test_adaptive_harness.py",
    ENGINE_DIR / "test_model_class_router.py",
    ENGINE_DIR / "test_shadow_backlog.py",
    ENGINE_DIR / "test_online_escalation.py",
    ENGINE_DIR / "test_information_access.py",
    ENGINE_DIR / "test_ai_processing_envelope.py",
    ENGINE_DIR / "test_p0_assurance_pilot.py",
    ENGINE_DIR / "test_local_assurance_runtime.py",
    ENGINE_DIR / "test_ai_engineering_evidence.py",
    ENGINE_DIR / "test_corporate_pulse.py",
    ENGINE_DIR / "test_task_granularity.py",
    ENGINE_DIR / "test_process_maturity.py",
    ENGINE_DIR / "test_process_strength_observer.py",
    ENGINE_DIR / "test_meeting_request.py",
    ENGINE_DIR / "test_engineering_flow_plan.py",
    ENGINE_DIR / "test_task_investment.py",
    ENGINE_DIR / "test_finance_scenario.py",
    ENGINE_DIR / "test_finance_control.py",
    ENGINE_DIR / "test_logistics_evolution.py",
    ENGINE_DIR / "test_built_environment_capability.py",
    ENGINE_DIR / "test_regulatory_watch.py",
    ENGINE_DIR / "test_execution_evidence.py",
    ENGINE_DIR / "test_software_release_evidence.py",
    ENGINE_DIR / "test_domain_assurance_profile.py",
    ENGINE_DIR / "test_external_review_disposition.py",
    ENGINE_DIR / "test_external_snapshot_manifest.py",
    ENGINE_DIR / "test_open_control_gaps.py",
    ENGINE_DIR / "test_project_learning_export.py",
    ENGINE_DIR / "test_indo_german_handoff.py",
    ENGINE_DIR / "test_creative_option_analysis.py",
    ENGINE_DIR / "test_evidence_dashboard.py",
    ENGINE_DIR / "test_synthetic_company_workflow.py",
    ENGINE_DIR / "test_capital_investment.py",
    ENGINE_DIR / "test_admitted_tool_router.py",
    ENGINE_DIR / "test_commercial_change_control.py",
    ENGINE_DIR / "test_antigravity_incremental_adaptation.py",
    ENGINE_DIR / "test_antigravity_2026_09_06_adaptation.py",
    ENGINE_DIR / "test_audit_decision_brief.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_graph.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_corp_builder_control.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_deliberation.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_deliberation_graph.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_governance_meeting.py",
    ENGINE_DIR / "LangGraph_Pipelines" / "test_meeting_scaler.py",
    ENGINE_DIR / "Skills" / "test_collaboration_observer.py",
    ENGINE_DIR / "Skills" / "test_role_skill_observer.py",
)


def main() -> None:
    for check in CHECKS:
        subprocess.run([sys.executable, str(check)], check=True)
    print(f"Triton_AI_Corp baseline passed: {len(CHECKS)} fixed checks.")


if __name__ == "__main__":
    main()
