# Feature-Team Operating Model

## Principle

Triton forms durable, cross-functional feature teams around a customer or product outcome, not departmental queues. Each team owns discovery through usable increment, evidence, and learning for a bounded feature area. Departments provide capability standards, coaching, assurance, and capacity—not sequential hand-offs.

## Team Composition

| Capability | Default team accountability |
| --- | --- |
| Value | Product Owner, Business Manager, Cost-Benefit / Solution Estimator |
| Understanding | Requirements Engineer and relevant domain expert |
| Design | System/Software Architect plus domain architects where applicable |
| Delivery | Developers, engineers, or other delivery specialists |
| Evidence | Tester / Quality specialist and independent gate access |
| Effectiveness | Scrum Master from the Communication and Collaboration capability |

For construction or built-environment work, activate the relevant Civil Engineer, Structural Engineer, Built Environment Architect, Interior/Exterior Design Manager, and Construction Site Quality Inspector. Specialists may serve more than one small team, but every responsibility must have a named accountable owner.

## Feature Flow

```text
Signal or idea
  -> Evidence, risk, cost, and benefit triage
  -> Product Owner orders validated option
  -> Feature-team discovery and acceptance criteria
  -> Timeboxed delivery with continuous quality evidence
  -> Usable increment and independent gate
  -> Release / operation
  -> KPI and lesson export -> future improvement portfolio
```

## Before Capacity Is Committed

The Feature Investment Review evaluates material ideas as an option, not a promise. It requires: problem and affected users, source evidence, alternatives, expected benefit, cost range, risk and compliance impact, data classification, feasibility, dependencies, measurable success criterion, and a stop condition. Use `FEATURE_INVESTMENT_REVIEW_TEMPLATE.md` for the controlled record. The Product Owner retains backlog ordering; the review gives evidence and challenge, not committee-controlled micromanagement.

## Lean Coordination Rules

- Default to a team decision record and asynchronous update; schedule a meeting only for a decision, conflict, risk, or design session that cannot be resolved asynchronously.
- A work item has one source of truth in the ALM system, a small required-field set, a visible definition of ready/done, and evidence links rather than duplicated status reporting.
- Cross-team dependencies are explicit, owned, dated, and reviewed through the smallest relevant coordination forum.
- Every team reviews flow, quality, outcome, and communication-load indicators. High workload alone is a signal for investigation, not a performance score.
