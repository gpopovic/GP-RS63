# Role Engagement Model

## One Canonical Role, Several Controlled Engagements

A role defines competence, authority, boundaries, and expected results. It does not limit a person or agent to one narrow activity. The same canonical role may be assigned to different engagements when the assignment is explicit and its independence constraints are met.

| Engagement | Purpose | Typical examples |
| --- | --- | --- |
| **Actor** | Creates or operates a work product or service | Requirements Engineer specifies; Developer implements; Procurement sources |
| **Advisor** | Supplies independent expertise or options | Legal Counsel advises a feature team; Structural Engineer reviews an option |
| **Challenger** | Tests reasoning, assumptions, risks, or alternatives | Strategic Red Team, Security Auditor, Commercial Strategy Auditor |
| **Validator** | Checks defined acceptance criteria and records a pass/fail or exception decision | Code Validator, Test Engineer, Receiving Inspector |
| **Auditor** | Independently assesses process, evidence, controls, or conformance | Process and Quality Auditor, Internal Control Inspector |
| **Panel member** | Contributes evidence and dissent to a bounded collective decision | Feature Investment Review, Legal Risk Review, Treasury Review |
| **Chair / integrator** | Runs a defined decision forum and produces an accountable record | Product Owner, Scrum Master, department lead |

## Assignment Contract

Every non-trivial assignment records: role, engagement type, scope, work item or meeting identifier, decision rights, input evidence, expected output, time boundary, conflicts of interest, and escalation owner. The ALM system links this assignment to the relevant evidence and decision record.

## Independence Guardrails

- An Actor cannot be the sole Validator, Auditor, or release authority for the same work product.
- An Auditor cannot audit a control that the same assignment designed or operated.
- A Panel member may advocate a position and must disclose relevant interest; the chair records dissent and decision rationale.
- A Scrum Master facilitates the system; the role does not own product priority or technical acceptance.
- An ALM administrator can operate data and workflow configuration but does not close independent quality or audit findings.
- Where a small company cannot separate people, separation is achieved by separate assignments, independent evidence review, recorded conflict, and proportionate external review.

## Conflict and Escalation

Roles may challenge each other and defend evidence-backed work. A material unresolved conflict moves through the bounded deliberation graph and then to the smallest competent governance forum. The record must retain the competing positions, evidence, decision, owner, and re-evaluation trigger.
