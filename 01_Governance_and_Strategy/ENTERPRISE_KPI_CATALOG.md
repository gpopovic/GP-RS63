# Triton Enterprise KPI Catalog

## Measurement Principle

Use a balanced scorecard, not a single productivity number. Every KPI must state its owner, formula, data source, reporting cadence, baseline, target range, confidence, and possible manipulation risk. Compare AI, human, and hybrid work only on equivalent work classes and the same acceptance criteria.

## Enterprise and Portfolio KPIs

| Dimension | KPIs | Decision use |
| --- | --- | --- |
| Business outcomes | Qualified-pipeline coverage, win rate, recurring-revenue share, renewal rate, customer concentration | Grow, redesign, or retire offers |
| Profit and cash | Gross margin, contribution margin, cost-to-serve, cash conversion, days sales outstanding, unbilled work | Price, capacity, payment, and capital decisions |
| Customer trust | Acceptance first-pass rate, complaint rate, claim exposure, time to resolve a complaint | Account and delivery intervention |
| Risk and compliance | Gate-miss rate, severe finding rate, open high-risk age, audit-action closure effectiveness | Control investment and escalation |

## Delivery and Process KPIs

| Dimension | KPIs | Decision use |
| --- | --- | --- |
| Outcome | Requirement acceptance rate, defect escape rate, realised customer outcome | Confirm value and quality |
| Flow | Lead time, cycle time, work in progress, blocked-work age, hand-off count, forecast accuracy | Remove bottlenecks |
| Stability | Change failure rate, recovery time, release success rate, integration rework | Protect service and release reliability |
| Competency | Traceability coverage, test evidence coverage, review quality, corrective-action effectiveness | Target process improvement |

### Task Investment and Capacity Allocation

Material portfolio decisions use three decision KPIs: evidenced delay exposure addressed, accepted constrained-resource time allocated to ready critical/near-critical or dependency-unlocking work, and realised investment-decision accuracy after the outcome matures. Diagnostic drivers include readiness failure, dependency age, WIP, blocked time, estimate range, first-pass acceptance and rework.

These measures never form one autonomous productivity score. Relative WSJF remains within one comparable portfolio and scoring session; monetary Cost of Delay remains a separately sourced range. Protected legal, contractual, safety, security and professional work cannot be traded away by a feature score. Before targets are set, record the task-class baseline, sample size, period and data quality. See `TASK_INVESTMENT_AND_SOURCING_POLICY.md`.

### Process-Strength Feedback Scorecard

Process-strength decisions combine protected quality measures (first-pass acceptance, rework, escaped-defect severity, applicable evidence completeness, source-backed satisfaction and control adherence) with counterweights (cycle time, process wait, handoffs, review effort, assurance/model/tool cost and duplicate evidence effort). Each task class owns its quality contract and limits; no universal target applies across grammar work, coding, architecture, construction or safety engineering.

A critical escape or mandatory nonconformity triggers containment. Normal tightening or simplification requires at least three comparable independently reviewed periods. The observer may recommend only one targeted control change or bounded variant and may never mutate production routing. See `PROCESS_STRENGTH_OBSERVATION_AND_EVOLUTION_POLICY.md`.

For logistics evolution, compare a champion and one-family challenger across at least three comparable independently audited periods. Report a multi-objective vector covering protected quality, flow, delay/blocked-capacity exposure, lifecycle and recovery cost, compute/tool/energy, human attention, opportunity/resilience/exit and applicable sustainability impact. Do not collapse this vector into one fitness score. The Release and Integration Manager owns the flow; the Process and Quality Auditor independently audits it; Finance reviews cost lineage; Quality owns protected guardrails; the Continuous Improvement Architect proposes but cannot activate a challenger.

Software and plugin candidates use the blocking and diagnostic evidence defined in `SOFTWARE_CHANGE_RELEASE_EVIDENCE_PROFILE.md`. Candidate readiness is hash-specific and remains distinct from human release approval.

## Role-Level KPIs

Measure a role against the outcomes it owns, not activity volume alone. Use quality pass rate, traceability, rework cycles, unresolved disagreement, decision latency, stakeholder usefulness, and control effectiveness. Report sample size and uncertainty; small samples may trigger learning, never a punitive conclusion.

## Human, AI, and Hybrid Work KPIs

| Dimension | Measures | Guardrail |
| --- | --- | --- |
| Performance | Accepted outcome rate, escaped defects, decision quality, customer impact | Do not replace with output count |
| Flow and efficiency | Lead time, active effort, hand-offs, automation time, model latency | Compare equivalent work only |
| Activity | Completed work items, reviewed artifacts, validated tests | Activity is diagnostic, not a target by itself |
| Collaboration | Clarification loops, hand-off quality, unresolved conflicts, knowledge transfer | High collaboration is not automatically waste |
| Sustainability | Human workload signal, AI token/energy/cost consumption, recurring rework | Optimise sustained capacity, not short bursts |

## Communication and Agile-System KPIs

Measure communication and Scrum-system effectiveness at team or process level: decision latency, meeting decision yield, clarification-loop rate, hand-off completeness, focus interruption load, sprint-goal attainment, blocked-work age, and retrospective-action effectiveness. Treat message count, attendance, tickets, and individual online time as diagnostics at most, never as individual performance targets. See `ALM_AND_COMMUNICATION_GOVERNANCE.md` for definitions and privacy guardrails.

## Loss and Gate-Risk Indicators

Track missed gates, late acceptance evidence, customer complaints, claims, security/privacy incidents, contractual deviations, and estimated loss exposure. For every material incident capture prevention cost, actual recovery cost, revenue at risk, and the corrective action's measured effectiveness.

## KPI Anti-Gaming Rules

- No individual ranking from one metric, token volume, lines of code, ticket count, or raw hours.
- A speed or cost gain is invalid if a protected quality, traceability, safety, legal, customer, or financial-risk metric regresses.
- Publish both leading indicators (e.g. open high-risk age) and lagging indicators (e.g. customer claims).
- Review metric relevance quarterly and retire measures that create harmful incentives.
- Evolutionary process optimisation must use hard protected-quality constraints and multiple objectives; it may not optimise one scalar productivity score or self-promote a process variant.
