# Company OS Activation Gate

## Purpose and Scope

Use this gate before treating Triton's Company Operating System as an active operating environment. This record governs Company OS configuration only. It does **not** approve an opportunity, product, client delivery, data processing activity, external tool, model, MCP, expenditure, or product workspace.

Product work remains in an external workspace under `06_Projects_and_Clients/PRODUCT_WORKSPACE_CONTRACT.md`. Do not attach customer data, credentials, source code, delivery artefacts, invoices, or operational records to this gate.

## Gate Record

| Field | Required entry |
| --- | --- |
| Gate ID | `COS-ACT-YYYY-NNN` |
| Requested by | Name and role |
| Configuration baseline | Git commit or approved baseline identifier |
| Review date | ISO 8601 date |
| Scope | Company OS configuration being activated |
| Decision | `APPROVE`, `APPROVE WITH CONDITIONS`, or `DO NOT APPROVE` |
| Conditions and due dates | Explicit owner and date for every condition |
| Next review date | ISO 8601 date |

## Required Evidence Checks

Record the command result, reviewer, date, and evidence reference for each applicable item.

| Check | Minimum acceptance evidence | Owner / independent review |
| --- | --- | --- |
| Configuration baseline | `validate_company_configuration.py` passes; all intended changes are traceable | Configuration Manager / Process and Quality Auditor |
| Role baseline | `validate_role_registry.py` passes; role prompts are loaded from controlled Markdown sources | Role Skill Evolution Manager / Quality Manager |
| Product-workspace boundary | `test_project_workspace.py` passes; no product workspace is located in the Company OS | Product and Inventory Operations Manager / Privacy Officer |
| KPI and cost controls | `test_kpi_cost_engine.py` passes; illustrative rates are not used as an approved rate card | Continuous Improvement Architect / Finance and Risk Controller |
| ALM source of truth | Selected ALM sandbox or approved Shadow Backlog mode, named owner, migration/rollback route, and dashboard data definitions | ALM and Jira Product Administrator / Quality Manager |
| Data routing | Approved data-flow decision for Company OS, external product workspace, customer-local processing, AI chats, telemetry, and external providers | Privacy and Data Protection Officer / Security Assurance Auditor |
| Models and MCPs | Each enabled lane or MCP has a separate admission/approval record, data boundary, monitoring owner, and rollback route | Model Quality Observer / Security and Privacy |
| Manual operations | Named incident, escalation, change-control, and human decision contacts are reachable | Founder Operating System Advisor / General Counsel as relevant |

## Explicit Human Decisions Still Required

The activation reviewer must select and record one outcome for every item below. An empty field is not approval.

| Decision | Outcome / rationale | Accountable human | Date | Evidence reference |
| --- | --- | --- | --- | --- |
| ALM sandbox or continued controlled Shadow Backlog mode |  |  |  |  |
| Operational source of truth and dashboard connector |  |  |  |  |
| Permitted Company OS data classes and routing |  |  |  |  |
| Initial model lanes and permitted external providers |  |  |  |  |
| Initial MCP admissions, if any |  |  |  |  |
| Exception or risk acceptance, if any |  |  |  |  |

## Decision and Follow-up

| Role | Name | Decision / signature reference | Date |
| --- | --- | --- | --- |
| Accountable founder or delegated authority |  |  |  |
| Configuration Manager |  |  |  |
| Quality Manager (independent recommendation) |  |  |  |
| Privacy and Data Protection Officer (as applicable) |  |  |  |
| Security Assurance Auditor (as applicable) |  |  |  |
| ALM and Jira Product Administrator (as applicable) |  |  |  |

If the decision is conditional or negative, record each corrective action in the approved decision/change record. Do not silently reinterpret this gate as an approval for a particular product workspace or delivery package.
