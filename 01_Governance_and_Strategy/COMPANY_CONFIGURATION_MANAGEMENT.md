# Company Configuration Management

## Purpose

Triton's Company OS is a controlled configuration, not an informal prompt collection. Roles, organisational structure, meetings, KPIs, process models, skills, MCP configurations, model routing, ALM configurations, and policy documents are configuration items. Their authoritative sources, relationships, versions, changes, and verification evidence must remain traceable.

## Configuration Baseline

`COMPANY_CONFIGURATION_INDEX.json` is the machine-readable entry point. It identifies the current authoritative configuration items and the validator or review required for each. A configuration baseline is valid only when all referenced files exist and their stated checks pass.

## Change Lifecycle

1. **Propose** — state purpose, trigger, evidence, affected configuration items, expected benefit, risk, cost, privacy/security/legal impact, and rollback route.
2. **Assess** — the relevant Actor, Quality, Security, Privacy, Legal, Finance, and ALM owners assess proportionate impacts.
3. **Trial** — place a changed role, skill, MCP, model, workflow, KPI, or process in a controlled trial if material uncertainty remains.
4. **Decide and baseline** — record version, owner, decision, rationale, verification evidence, effective date, and rollback condition.
5. **Monitor** — use KPIs, incidents, feedback, audits, and lessons learned to validate the expected benefit.
6. **Revise, retire, or rollback** — preserve traceable history; do not silently overwrite a released configuration.

The lifecycle also prevents configuration accumulation. Prefer extending or consolidating an existing item when ownership, traceability and rollback remain clear. A proposed new role, register, validator, gate or policy identifies its unique failure mode or obligation, accountable consumer, activation trigger, expected operational or assurance benefit, and condition for consolidation or retirement. If those cannot be named, use the existing source of truth or do not add the item.

External reviews follow `EXTERNAL_REVIEW_CHANGE_INTAKE_POLICY.md`. Every proposal or changed capability receives an explicit disposition. Rejecting unsafe code does not permit Triton to discard the useful capability intent; the review must identify the harm, the complete existing control, a safer replacement, or an open evidence/deferment route.

## Required Change Record

Every material change record includes an identifier, title, requester, owner, affected items, reason, evidence, risk assessment, approvals or decisions, test/trial result, effective date, version, review date, and rollback decision. Product work remains outside the Company OS under the Product Workspace Contract.

## Configuration Ownership

| Configuration item | Accountable owner | Independent counterweight |
| --- | --- | --- |
| Role instructions and engagement policies | Role Skill Evolution Manager | Process and Quality Auditor |
| Organisation and meeting catalog | Founder Operating System Advisor | General Counsel / Process Auditor as relevant |
| KPI catalog and metric contracts | Continuous Improvement Architect | Finance and Risk Controller / Quality Manager |
| ALM/Jira workflow, reports, dashboards | ALM and Jira Product Administrator | Quality Manager; Privacy as relevant |
| Skills, MCPs, models, routing | Role Skill Evolution Manager / Model Quality Observer | Security, Privacy, Quality |
| Product improvement portfolio | Product Improvement and Insights Manager / Product Owner | Commercial Strategy Auditor |

## Lean-Control Principle

Control is proportional to risk. A wording correction can be versioned and reviewed lightly. A change to data sharing, financial approvals, customer commitments, audit independence, model routing, security controls, workflow evidence, or regulatory logic needs a formal impact assessment and rollback plan.

Configuration reviews distinguish `ACTIVE`, `TRIGGERED_DORMANT`, `CONSOLIDATION_CANDIDATE` and `RETIREMENT_CANDIDATE` as review states, not automatic decisions. Use the existing change record or ALM item; do not maintain a second inventory. A dormant control may remain justified by a named contingency or obligation. A candidate is consolidated or retired only after dependency, evidence-consumer, authority and rollback checks.
