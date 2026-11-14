# Human–Agent Stewardship and Reliability Policy

## Purpose

Triton is a hybrid operating model: people retain accountability and agents provide bounded, traceable work. A human may lead several AI agents as an **AI Pod Steward**, but leadership is not a rubber-stamp role. The steward must understand the decision, inspect the evidence appropriate to its risk, and escalate uncertainty.

## Operating Pod

| Responsibility | Purpose | May approve alone? |
| --- | --- | --- |
| Human accountable owner | Owns the business decision, customer commitment, and escalation | Only inside delegated authority |
| AI producer | Drafts, analyses, implements, or prepares evidence | No |
| AI challenger or independent reviewer | Searches for gaps, contradictory evidence, and unsafe assumptions | No |
| Deterministic validator | Runs defined checks, tests, schemas, or policy rules | No; reports evidence |
| Human quality or domain approver | Evaluates evidence and grants the defined gate | Yes, if authorised and independent |

The initial pod size is deliberately small. Expand only after the steward can demonstrate timely review, clear hand-offs, and stable independent evidence. No human should be assigned so many active agents that meaningful review becomes impossible.

## Reliability Is Measured, Not Assumed

Triton must not claim a blanket 95% accuracy figure. Reliability is reported by **role, task class, model/tool configuration, data boundary, and measurement period**:

`independently accepted outcomes / independently evaluated outcomes`

Every result records sample size, task definition, severity weighting, reviewer independence, known failure modes, and confidence interval where statistically meaningful. A 95% result for summarising internal notes does not transfer to pricing, safety, security, legal advice, production release, or customer commitments.

## Delegation Levels

| Level | Permitted use | Control |
| --- | --- | --- |
| Observe | Agent runs on synthetic or low-risk examples | Human compares result against expected outcome |
| Supervised | Agent prepares a bounded work item | Human reviews every output before use |
| Bounded delegation | Repetitive, reversible, low-impact steps with proven evidence | Sampling, automated guardrails, stop threshold, named owner |
| Pause and escalate | Material errors, drift, conflicts, new data class, or missing evidence | Disable delegation; investigate and re-authorise only through change control |

Contracts, prices, legal positions, privacy/security exceptions, financial transfers, production releases, personnel actions, and safety-relevant decisions always require the authorised human decision path. A KPI can inform that decision but cannot replace it.

## Quality Thresholds and Stop Rules

The Quality Manager defines acceptance tests and severity classes with the domain owner. The Model Quality Observer maintains the evaluation record. A proposed 95% operating threshold is admissible only when the task is homogeneous, the evaluation set is representative and independently reviewed, and no critical defect appears. One critical defect, unexplained drift, evidence tampering, or repeated human correction triggers a pause and review regardless of the aggregate rate.

## Training and Evidence

Before leading a pod, a human completes the relevant Academy path, demonstrates a supervised scenario, and knows the applicable data boundary, decision rights, quality gate, and escalation route. Training success is assessed by an observed task and evidence review—not prompt volume, online time, or ticket count.

## Ownership

Learning and Transfer Coach owns learning design. Quality Manager owns gate design. Model Quality Observer owns model-evaluation evidence. Organizational Psychology and Human Factors Advisor reviews workload and human-factors risks. Employment and Workforce Compliance Officer ensures workforce use is lawful and fair. Material changes follow Company Configuration Management.

## User-Initiated Low-Energy Support

When a person explicitly reports low energy, overload or decision fatigue, the agent may offer one small reversible next step, reduce nonessential choices, preserve context and make stopping easy. It must not diagnose health, infer a psychological state from activity data, impose universal sprint caps, exploit streak-loss pressure, create monetary self-reward schemes or lower a required safety, legal, privacy, security or quality control. Persistent or serious wellbeing concerns belong with the person and an appropriate qualified human, not an automated productivity mechanism.
