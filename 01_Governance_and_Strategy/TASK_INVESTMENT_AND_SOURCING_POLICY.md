# Task Investment and Sourcing Policy

## Purpose

Direct scarce founder, engineering, review, test-bench, GPU and supplier capacity toward the work that best protects obligations, unlocks flow and creates risk-adjusted value. This policy adds economic and network-planning evidence to Engineering Flow Logistics without turning one score into an automatic backlog decision.

The reusable decision contract belongs to Triton_AI_Corp. Task estimates, customer economics, dependency graphs, source code and supplier quotations remain in the authorised external product or project workspace.

## Decision order

Apply the following order before committing material capacity:

1. **Protected work:** binding law, contract, safety/security containment, professional hold points and critical defect correction cannot be displaced by a lower-scored commercial feature. Confirm applicability and authority rather than assigning arbitrary score bonuses.
2. **Readiness:** do not load a constrained resource with work lacking its required inputs, acceptance condition, owner or decision boundary. Use bounded discovery to close a material unknown.
3. **Network effect:** identify real predecessors, successors, critical and near-critical paths, float, dependency unlocks and resource contention.
4. **Economic comparison:** compare Cost of Delay, job size, uncertainty, option value and consequence of not doing the work within a declared comparable portfolio.
5. **Sourcing:** compare feasible `MAKE`, `BUY` and `HYBRID` alternatives over the relevant lifecycle and data/assurance boundary.
6. **Portfolio balance:** retain capacity for defects, maintenance, learning and aging work so that a high score cannot starve essential but less visible work.
7. **Human decision:** record `COMMIT`, `DISCOVERY`, `DEFER` or `STOP`, rationale, evidence, owner, review point and invalidation trigger.

## Cost-of-delay and WSJF use

Two forms must remain separate:

- **Monetary Cost of Delay:** an evidenced low/base/high loss or foregone-value rate over a declared time horizon and currency. Include contractual exposure, blocked-capacity cost, missed revenue/value, risk exposure and customer impact only where they are supportable. Do not convert safety or legal duties into a price that permits trading them away.
- **Relative WSJF proxy:** `(business value + time criticality + risk reduction or opportunity enablement) / relative job size`. Use a consistent scale and the same scoring session for comparable items. It is a discussion aid, not money, schedule proof or approval.

Never mix monetary values and relative scores in one numerator. Report ranges and confidence. Split work when a large job hides an independently valuable smaller outcome. A score may order otherwise eligible tasks but cannot override a protected obligation, missing readiness, data boundary, quality gate or competent authority.

## Little's Law and flow cost

For a sufficiently stable observed flow over a declared boundary and period:

`average WIP = average throughput × average lead time`

Equivalently, `average lead time = average WIP / average throughput` when units and sampling are consistent. This is a diagnostic relationship, not a promise for a single heterogeneous task. Arrival-rate changes, priority classes, rework loops, batching, blocked work and unstable throughput must be reported. Little's Law does not establish exponential cost growth.

Use it to test whether excessive WIP is associated with waiting and to size bounded experiments. Do not reduce WIP below the safe level needed to keep a constraint supplied or to handle protected incident work.

## Critical path, PERT and resource constraints

The project network records activities, dependency edges, duration ranges, calendars, resources and acceptance conditions. CPM identifies zero- or low-float paths for a stated baseline. PERT three-point estimates may expose uncertainty, but their assumptions, correlations and data basis remain visible.

Capacity outside the current critical path is not automatically waste. Near-critical work can become critical after variance; independent work can reduce risk, create an option, satisfy a protected obligation or avoid future resource conflict. Use resource-constrained scheduling when multiple activities need the same person, bench, licence or environment. Recalculate after material scope, duration, dependency or capacity change.

## Make, buy or hybrid

Classifying work as core or commodity starts the analysis but does not decide it. Compare each feasible alternative over an explicit horizon using a Total Cost of Ownership range:

- acquisition, development and integration;
- migration, validation, qualification and regulatory impact;
- licences, hosting, compute and support;
- operations, monitoring, security and incident response;
- maintenance, upgrades, compatibility and obsolescence;
- data sovereignty, privacy, IP exposure and permitted processing region;
- supplier viability, concentration, lock-in, service limits and roadmap control;
- skills retention, opportunity cost and switching/exit cost;
- performance, quality, availability and recovery evidence.

Open source is not zero-cost, and a vendor community does not automatically carry Triton's integration or assurance responsibility. Core IP may still use bought infrastructure behind controlled interfaces. A commodity may be made internally when sovereignty, assurance, lifecycle or exit evidence makes that safer and cheaper. Prefer a reversible adapter boundary and retain an exit route.

## Decision-support KPIs

Use a small scorecard by comparable task class and planning cadence:

| Metric | Definition | Decision use | Guardrail |
| --- | --- | --- | --- |
| Delay exposure addressed | evidenced low/base/high delay exposure avoided or reduced by the selected capacity allocation | compares allocation scenarios | never monetise away protected duties; show confidence and source |
| Critical/near-critical constraint allocation | accepted hours spent on ready critical, near-critical or dependency-unlocking work / available constrained-resource hours | detects capacity spent on low-leverage work | reserve incident, maintenance, learning and risk-reduction capacity |
| Investment decision accuracy | decisions whose realised value, duration and TCO remain within the approved range / reviewed mature decisions | recalibrates estimates and sourcing | segment by task class; do not punish discovery or hide stopped work |

Diagnostic drivers are readiness failure, dependency age, WIP, blocked time, estimate range, first-pass acceptance and rework. Guardrails are escaped-defect severity, mandatory-control adherence, customer harm, technical-debt trend, starvation/aging exceptions, supplier concentration and exit readiness.

Do not set universal numeric targets before comparable historical data exists. Establish a baseline, sample size, task classification and measurement period first. A favorable score is invalid if quality, safety, security, privacy, law, contract, traceability or professional authority regresses.

## Roles

| Role | Responsibility |
| --- | --- |
| Product Owner | Owns the capacity decision, comparable portfolio and relative value evidence. |
| Finance and Risk Controller | Challenges monetary Cost of Delay, TCO range, cash/risk exposure and false precision. |
| Proposal and Solution Estimator | Maintains effort, duration, option and sourcing assumptions with confidence ranges. |
| Release and Integration Manager | Maintains dependency, critical/near-critical and constrained-resource evidence. |
| System Architect and Security/Privacy roles | Determine core boundaries, interfaces, sovereignty and assurance constraints. |
| Procurement and Sourcing Manager | Obtains comparable supplier, licence, service and exit evidence. |
| Quality Manager | Independently checks evidence quality, protected controls and realised-outcome review. |
| Continuous Improvement Architect | Recommends one bounded recalibration experiment without automatically changing priority rules. |
| Pepper | Reports material allocation conflicts, aging, decisions and missing evidence in the founder operating view. |

No AI role may commit spend, sign a supplier contract, waive an obligation, alter a production backlog or approve a release.

## Required record and boundary

The controlled example and validator define the minimum record. Structural validation does not verify the supplied economics, prove a critical path, purchase a tool or commit project capacity. Material inputs require their named human review in the external workspace.

## Ownership

The Product Owner owns this policy. The Finance and Risk Controller independently challenges economic inputs. The Release and Integration Manager owns dependency evidence, and the Quality Manager reviews decision integrity.
