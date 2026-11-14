# Feature Investment Review Template

## Record

- **Feature / option ID:**
- **Decision date:**
- **Chair:** Product Owner
- **Status:** Draft / Discovery approved / MVP approved / Deferred / Stopped
- **Decision requested:** Approve discovery (A) / Approve MVP (B) / Defer (C)

## Binding Data Constraint

State the processing boundary before discussing scope or cost. For a customer-local deployment, record the approved customer-local runtime: device or server, operating system, network rule, allowed processes, permitted storage locations, update path, and support-access boundary.

- Production customer data may not leave the approved customer-local runtime.
- Production customer data may not enter the Triton Company OS, AI chats, development or test fixtures, telemetry, or an external provider unless a specifically approved and documented data-transfer route exists.
- Development and automated testing use synthetic fixtures only.
- A Data Capsule is only a minimised, sanitised input for one approved online escalation. It is not a general authorisation to transfer production customer data.

If the constraint is infeasible, stop the review or reframe the option; do not treat it as a delivery-time detail.

## Problem and Evidence

- Affected users and their outcome:
- Source evidence and confidence:
- Alternatives considered:
- Demand evidence (pilot intent, discovery mandate, purchase signal, or equivalent):
- Expected benefit and how it will be measured:

## Scope and Assumptions

- Included outcome and explicit exclusions:
- Customer-specific variants and commercial treatment:
- Data classification and data-flow summary:
- Dependencies and target environment:
- Acceptance and timing protocol: start/end event, representative input profile, hardware/runtime, cold/warm state, tolerance, and evidence:

## Options

| Option | Meaning | Decision conditions |
| --- | --- | --- |
| A - Approve discovery | Bounded discovery only; no full delivery capacity commitment | State timebox, budget, artifacts, stop conditions, and re-baseline date |
| B - Approve MVP | Commit bounded feature-team capacity | Requires frozen requirements, data-flow/architecture evidence, approved acceptance protocol, and refreshed estimate |
| C - Defer | Do not commit discovery or delivery capacity | State revisit trigger and owner |

## Cost, Time, and Risk

- Discovery timebox, budget, and expected artifacts:
- MVP cost/time hypothesis and confidence:
- Re-estimation trigger:
- Top risks, mitigations, and residual risk:
- Licensing, installation/update, retention/deletion, backup, local-permission, and support-access considerations:

## Stop Conditions

List objective conditions that halt spend or require a new review. Include at least: data-boundary violation or infeasibility; requirements or acceptance protocol not frozen; estimate beyond approved range; material customer variant; and unresolvable security/privacy finding.

## Required Sign-Offs and Evidence

| Gate | Owner | Required evidence |
| --- | --- | --- |
| FIR decision | Chair and panel | Decision, rationale, dissent, owners |
| Data classification and transfer boundary | Privacy and Data Protection Officer | Data-flow and control register |
| Egress and toolchain challenge | Security Assurance Auditor | Local-runtime allow/deny evidence and toolchain review |
| Value and scope | Product Owner and customer/domain owner | Baseline and variant decision |
| Architecture fitness | Software Architect | Design and data-flow note |
| Cost/time | Proposal and Solution Estimator | Baseline estimate and confidence |
| Release later | Quality Manager / independent validator | Test, inspection, and release evidence |

## Decision and Follow-up

- **Decision:**
- **Rationale and dissent:**
- **Owners and due dates:**
- **Next review / re-baseline trigger:**
- **Manual Quality Gate record ID:**
