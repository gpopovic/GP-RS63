# ALM Shadow Backlog Protocol

## Purpose

Use this temporary, controlled record when a Jira sandbox or approved ALM tenant is unavailable. It supports planning and review; it does not replace a future operational system of record.

## Storage and Ownership

- Store the CSV in the external product workspace, never in this Triton_AI_Corp configuration repository. Start from `ALM_Shadow_Backlog_Template.csv` and validate it with `04_Execution_Engine/shadow_backlog.py` before any hand-off or import.
- The Product Owner owns priority and acceptance; the ALM and Jira Product Administrator owns structure, identifiers, traceability checks, and later migration.
- Use one stable identifier per work item. Do not rename or reuse identifiers.

## Minimum Fields

| Field | Requirement |
| --- | --- |
| ID | Stable, unique identifier |
| Type | Epic, Feature, Story, Task, Defect, Test, Evidence, Risk, or Decision |
| Title and outcome | Concise and testable |
| Owner | Named accountable role/person |
| Status | Proposed, Ready, In Progress, Blocked, In Review, Done, or Cancelled |
| Parent and links | Parent, requirement, test, defect, evidence, risk, or decision links as applicable |
| Acceptance / DoD | Required for work that may be completed |
| Source and date | Origin and last confirmed date |

## Framework Rule

SAFe governs cross-team flow and escalation. Nexus may be used only for shared-product integration. If they conflict, apply the precedence recorded in `01_Governance_and_Strategy/ALM_AND_COMMUNICATION_GOVERNANCE.md` and log the decision.

## Migration to an Approved ALM

Before import, freeze the Shadow Backlog version, validate required fields and links, apply `ALM_SHADOW_BACKLOG_IMPORT_MAPPING.example.json` to the selected ALM, import into a sandbox first, reconcile counts and spot-check traceability, then declare the approved ALM the operational source of truth. Archive the final Shadow Backlog export as read-only evidence.
