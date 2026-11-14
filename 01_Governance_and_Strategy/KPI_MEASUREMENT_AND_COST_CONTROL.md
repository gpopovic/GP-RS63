# KPI Measurement and Cost Control

## Decision Principle

Every Triton role has a small scorecard for self-review and independent review. A KPI is actionable only if its definition, data source, calculation, owner, cadence, limitations, and decision consequence are stated. Do not rank people or agents by tokens, prompts, messages, online time, ticket count, or hours alone.

## Common Integrity Scorecard: Every Role

| Metric | Calculation | What it says | Guardrail / action |
| --- | --- | --- | --- |
| Evidence completeness | accepted work items with required evidence / reviewed accepted work items | Whether a result can be traced and audited | Missing evidence blocks a material gate. |
| Independent acceptance rate | independently accepted outcomes / independently evaluated outcomes | Reliability for a defined task class | Report sample size, severity and task/model/data scope. |
| Escaped-defect rate | material defects found after the role's defined gate / accepted outputs | Quality leakage, not merely rework | A critical escape pauses delegation or triggers corrective action. |
| Rework ratio | corrective effort / total effort for the same work package | Waste and requirement/process quality | Do not lower by hiding defects. |
| Handoff completeness | handoffs with owner, input, decision, evidence and next action / reviewed handoffs | Collaboration and flow quality | Missing owner or evidence is incomplete. |
| Forecast accuracy | 1 - abs(actual - forecast) / max(forecast, small positive floor) | Planning calibration for time, cost or risk | Segment by task class; do not punish novel work. |
| Control adherence | required gates passed or explicitly waived / applicable gates | Respect for quality, security, privacy and approval boundaries | A waiver needs an accountable human decision. |

## Functional Scorecards

| Capability | Primary KPI | Drivers | Guardrails |
| --- | --- | --- | --- |
| Business growth and offers | risk-adjusted contribution margin | qualified demand, win rate, proposal cycle time, forecast accuracy | claim accuracy, contract risk, customer concentration |
| Product and requirements | validated outcome / investment | discovery evidence, requirement stability, acceptance-criteria completeness | unpriced scope growth, customer harm, privacy/security impact |
| Engineering and architecture | accepted increment flow | lead time, build/test pass rate, dependency age | escaped defects, maintainability findings, security issues |
| Quality, safety and security | defect containment effectiveness | coverage of critical controls, defect detection before release, remediation time | independent release status, critical escapes, audit finding age |
| Agile, communication and ALM | decision flow effectiveness | decision latency, handoff completeness, ALM data completeness | meeting load, communication interruption, administrative burden |
| Legal, privacy and governance | timely compliant decision quality | obligation traceability, contract/change review latency | unapproved data route, overdue material obligation, conflict of interest |
| Finance, treasury and procurement | cash- and risk-adjusted value | forecast accuracy, collection cycle, purchase variance, supplier conformance | liquidity limit, concentration, sanctions/control finding |
| Research, impact and workforce | validated improvement effect | experiment learning rate, capability coverage, intervention effectiveness | ethics/privacy harm, safety, unfair or non-comparable assessment |
| AI systems and embodied intelligence | reproducible quality improvement for the declared use | validated learning, independent benchmark reproduction, quality-constrained compute and memory change | dataset contamination, unsafe physical transfer, licence/provenance gaps, hidden quality regression |
| Built environment delivery | accepted work package progress | inspection conformity, rework, schedule predictability | structural/safety non-conformance, unapproved change |

### AI Systems and Embodied Intelligence Definitions

| Metric ID | Calculation or record | Decision use | Guardrail |
| --- | --- | --- | --- |
| `validated_learning_rate` | independently accepted decision-relevant learnings / completed bounded experiments | Whether research reduces material uncertainty | A well-evidenced negative result is a learning; do not reward only positive claims or high experiment volume. |
| `benchmark_reproducibility` | independent reruns within the declared metric tolerance / eligible benchmark reruns | Whether the reported result survives the recorded model, data, software and hardware configuration | Report sample size, tolerance and configuration; a benchmark does not establish real-world or safety fitness. |
| `quality_constrained_resource_efficiency` | report the quality delta together with compute time, peak memory, energy/cost and latency ratios against the same accepted baseline | Whether an optimisation reduces resource use without hiding quality loss | Keep this as a vector; no efficiency gain is valid when a protected quality or safety limit regresses. |

## Cost and Time Forecasting

Every work package provides a base estimate and a risk reserve. The initial default reserve is 20% and is shown separately:

`forecast at completion = base forecast × (1 + reserve rate)`

For human work:

`human forecast = planned hours × fully loaded hourly cost × 1.20`

For local AI work:

`local AI forecast = planned runtime hours × allocated compute hourly cost × 1.20 + approved fixed tool cost`

For paid cloud AI work:

`cloud AI forecast = ((planned input tokens × input rate) + (planned output tokens × output rate)) × 1.20 + approved fixed tool cost`

The **fully loaded hourly cost** includes compensation, employer costs, equipment, software, management/admin allocation, training, and other agreed overhead. The founder's rate is entered as a normal human cost profile; it is neither omitted nor guessed.

Project control uses EVM-style measures only where work packages have an approved budget and objective completion evidence: `CPI = earned value / actual cost`; `SPI = earned value / planned value`. Values below 1 indicate adverse cost or schedule performance. Do not assign earned value simply because an agent produced text; objective acceptance evidence is required.

## Preventing Metric Gaming

- Every cost, time, throughput, or margin KPI has an explicit quality, risk, and customer-value guardrail.
- Compare like with like: segment by task class, complexity band, data class, customer criticality, and delivery mode before judging movement.
- Use random and risk-based samples, blinded counter-review where feasible, and held-out cases for model/role changes.
- Recalibrate only through a documented experiment: preserve the old definition, sample, comparison result, intended effect, unintended effect, owner, effective date, and rollback condition.
- A favorable margin is invalid if quality, safety, legality, security, privacy, traceability, or customer commitments regress.

## Visualisation Readiness

The future dashboard must show per role and in aggregate: forecast versus actual cost and hours, reserve consumption, acceptance/rework/escape trends, CPI/SPI where applicable, quality guardrails, confidence/sample size, and drill-down to evidence. It must never show a synthetic individual-performance score without task-class comparability and human review.

A decision-facing dashboard is an evidence projection, not a substitute for the underlying record. Every shown value, target and status requires its controlled source, as-of time, population or task class, formula, owner, confidence or data-quality state, and declared decision use. A static or synthetic value must be visibly labelled `DEMONSTRATION` or `NOT_ASSESSED`; a tooltip, framework label, colour, or favourable trend never proves compliance, maturity, current status, or an approved release. Targets are task-class and decision-specific, not imported as universal benchmarks.
