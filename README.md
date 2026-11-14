# Triton_AI_Corp

Triton_AI_Corp is a governed configuration repository for a hybrid AI-enabled company. It contains controlled roles, governance, model-routing safeguards, quality gates, and reusable operating patterns.

It is not a customer-product repository. Product code, customer data, delivery artefacts, operational records, and ALM backlogs remain in separate external product workspaces under the [Product Workspace Contract](06_Projects_and_Clients/PRODUCT_WORKSPACE_CONTRACT.md).

## Start Here

- [Operating runbook](05_Human_Interface_and_Ops/OPERATING_RUNBOOK.md)
- [Current handoff](05_Human_Interface_and_Ops/Session_Handoffs/2026-08-15_Triton_Operating_System_Setup.md)
- [Configuration index](01_Governance_and_Strategy/COMPANY_CONFIGURATION_INDEX.json)
- [Manual quality gates](05_Human_Interface_and_Ops/Manual_Quality_Gates/)

## Verification

Run the controlled local baseline from the repository root:

```powershell
python 04_Execution_Engine/run_company_baseline.py
```

The baseline is deterministic and must not start a local model, transmit project data, or approve a product release.

## Safety Boundaries

- Local and online models require version-specific admission; candidates fail closed.
- Online escalation requires a human-approved, unexpired data capsule that matches the exact provider and processing region.
- A portable CSV Shadow Backlog is available only as an ALM outage bridge; import into an approved ALM sandbox before making it the source of truth.
- Material configuration changes require the applicable human quality gate and change record.
