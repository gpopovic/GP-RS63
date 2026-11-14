# Project Governance Scaling Policy

## Purpose

Scale project coordination to the decision load, not to a calendar ritual. A meeting is added only when it resolves a named decision, risk, dependency, or evidence gap that cannot be handled asynchronously.

Apply `LEAN_ASSURANCE_AND_PROCESS_TAILORING_POLICY.md`: a ceremony without a named obligation, decision, risk-control purpose, unique evidence output or measured improvement experiment is optional and should be removed, merged or handled asynchronously.

## Inputs for Each Planning Cycle

- sprint length and number of active feature teams;
- active customers, material external parties, and contractual decision dates;
- delivery state: `GREEN`, `AMBER`, or `RED` based on evidence, not sentiment;
- planned capacity after approved leave, training, public holidays, and named backup coverage;
- material investment, Statement of Work (SOW), change, release, security, privacy, legal, or financial decision requests; and
- dependency and quality-evidence status.

## Cadence Rules

| Situation | Minimum coordination | Escalation or reduction rule |
| --- | --- | --- |
| One team, 1-week sprint, GREEN | Planning, short Daily Scrum, Review, Retrospective; asynchronous quality evidence | Add delivery-quality review only for a decision or risk. |
| One team, 2-week sprint, GREEN | Planning, Daily Scrum, Review, Retrospective; weekly asynchronous status | This is the normal default. |
| Two or more teams on one product | Above plus Nexus Integration Review per integrated increment | SAFe portfolio and dependency decisions prevail over Nexus. |
| Multiple active customers | Customer Delivery Steering per material customer cadence; portfolio view monthly | Avoid duplicating internal status; use one evidence pack. |
| AMBER | Weekly Delivery Quality Review and explicitly owned recovery actions | Stop adding low-value meetings; focus on blockers and evidence gaps. |
| RED / incident | Event-Triggered Crisis Command or relevant specialist board | Pause non-critical ceremonies, establish containment and next decision time. |
| Material new offer or SOW | Feature Investment Review and SOW Review before commitment | No delivery commitment or external promise without the authorised commercial path. |
| Material Company OS or project baseline change | Appropriate Change Control Board | A board output never implements the change automatically. |

## Participant Scaling

The smallest authorised set attends. A board with more than eight decision participants is split into an evidence round and an accountable decision round unless law, contract, or incident handling requires otherwise. Observers read minutes; they do not join merely for information.

Use written pre-reads and a structured evidence template where external parties or customers exceed three. The chair records one decision, dissent, owner, due date, and next gate; this avoids a large forum becoming a status-reporting room.

## Leave and Continuity

Maintain a capacity and coverage register with planned leave, customer-critical dates, named deputy, competence boundary, hand-over evidence, and availability status. Do not infer availability from calendar silence.

| Available planned capacity | Planning response |
| --- | --- |
| At least 85% | Normal commitment, with named backup for critical roles. |
| 70% to under 85% | Reduce planned scope, protect integration/test work, confirm deputy coverage before accepting new work. |
| Under 70% | Commit only to critical contractual, safety, security, quality, and recovery work until leadership accepts a revised plan. |

These starting bands are operational controls to be calibrated through observed forecast accuracy, quality, wellbeing, and customer outcomes. They are not a people-performance target.

## FROP Definition Needed

`FROP` is not expanded in Triton's current controlled vocabulary. Do not create a board with an invented mandate. The requester must define its full name, decision rights, inputs, outputs, and relationship to existing Feature Investment, SOW, Release, and Change boards before it becomes canonical.
