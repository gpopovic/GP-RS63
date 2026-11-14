# Process Strength Observation and Evolution Policy

## Purpose

Adjust process strength from observed quality, rework, satisfaction, evidence and flow without allowing an algorithm or agent to mutate production controls autonomously. Lean tailoring and quality protection form one closed loop: simplification is permitted only while the declared quality contract remains satisfied.

This policy uses the existing adaptive harness and roles. It creates no new standing meeting, department or universal process score.

## Process-Strength States

| State | Meaning | Typical response |
| --- | --- | --- |
| `LEAN` | minimum sufficient controls for low-consequence reversible work | acceptance check, versioned result and rollback where applicable |
| `STANDARD` | normal productive engineering controls | peer or independent review, deterministic tests, change impact and release decision |
| `ENHANCED` | one or more quality or risk signals require stronger targeted control | increase only the control family linked to the failure mode |
| `CONTAINMENT` | critical escape, mandatory nonconformity or uncontrolled high-consequence risk | stop propagation, preserve evidence, correct and independently re-evaluate |

Process strength is a vector, not one global number. Review depth, test depth, evidence capture, independence, sampling, approval, parallelism and meeting cadence may have different strengths. Do not increase all controls because one metric deteriorates.

## Task-Class Quality Contract

Before observing a process variant, the Product Owner and Quality Manager define task-class-specific guardrails. Use only relevant measures and record formula, data source, baseline, target/limit, confidence and manipulation risk.

Protected quality measures include:

| Measure | Example formula | Interpretation |
| --- | --- | --- |
| first-pass acceptance | accepted without material correction / reviewed packages | higher is normally better; segment by task class and reviewer |
| rework ratio | correction effort / total package effort | distinguish defect correction from legitimate learning and scope change |
| escaped-defect rate and severity | accepted defects found downstream / accepted packages | a critical escape triggers containment regardless of average |
| evidence completeness | required evidence items accepted / required evidence items | measure applicable evidence only, not document volume |
| stakeholder or customer satisfaction | source-backed rating for the delivered outcome | never infer sentiment from messages; pair with acceptance and defect evidence |
| control adherence | applicable controls completed with valid evidence / applicable controls | a missed optional step is not nonconformity |

Flow and cost counterweights include cycle time, decision wait, process-wait ratio, handoffs, review effort, assurance cost, model/tool cost and duplicate evidence effort. A speed or cost improvement is invalid when a protected quality, safety, security, privacy, legal or customer guardrail regresses.

No universal thresholds apply across task classes. A grammar correction, code change, architecture decision, structural calculation and safety requirement require different contracts.

## Observation Loop

```text
quality contract and current process vector
  -> comparable work packages
  -> independent output and adherence observations
  -> quality, rework, satisfaction, evidence, flow and cost evaluation
  -> containment, targeted strengthening, keep, or one bounded variant proposal
  -> named human decision
  -> time/cost/work-scope-bounded trial
  -> compare against the same contract and baseline
  -> promote, revert or refine with preserved evidence
```

Use at least three comparable accepted observations before recommending a normal micro-trial. A critical escape, mandatory nonconformity or uncontrolled safety/security/privacy event bypasses experimentation and enters containment immediately.

## Strengthening Rules

Strengthen only the control family that addresses a supported cause:

- unclear acceptance -> improve requirement and acceptance contract;
- defects not detected -> improve the relevant deterministic test or independent review;
- evidence missing -> generate evidence at source or strengthen the evidence gate;
- interface rework -> tighten the handoff contract or integration ownership;
- blind approval -> strengthen competence, independence, review scope or sampling;
- excessive parallel conflicts -> reduce lanes or sequence shared-baseline work;
- repeated external nonconformity -> strengthen applicability and compliance evidence;
- unstable tool or model -> restrict the admitted configuration or route.

Do not respond to poor quality by adding unrelated meetings, documents, roles or universal approval steps. Perform root-cause analysis and preserve a rollback path.

## Controlled Evolutionary Optimisation

An evolutionary or search algorithm may rank candidate process vectors only after sufficient comparable evidence exists. It operates as a constrained champion/challenger experiment:

1. the current approved process vector is the champion;
2. one challenger mutates one reversible control at a time;
3. hard obligation and protected-quality constraints cannot mutate;
4. the trial has a declared task class, sample boundary, time/cost cap, stop condition and rollback;
5. work is randomly or otherwise fairly assigned where practical; no unsafe work enters an experimental reduction;
6. fitness is multi-objective: accepted quality, defect/rework, satisfaction, evidence, flow and total cost;
7. a Pareto improvement is a proposal, not proof or activation;
8. independent review checks confounding, sample comparability, data quality, gaming and unintended human workload;
9. the configuration owner and named human authority promote or reject the challenger;
10. every promoted variant remains reversible and is re-observed for regression.

Do not optimise a single scalar productivity score. Do not use individuals as experimental units for employment evaluation. Do not combine several process mutations before the responsible effect can be identified.

For Engineering Flow Logistics, one mutable control family may be WIP capacity, buffer target, non-protected queue weights, batch size or controlled cache prefetch. The objective vector may add delay exposure, blocked capacity, lifecycle TCO, rework/recovery, compute/tool/energy, human attention/context switching, opportunity, supplier/exit, resilience and sustainability cost where each has a controlled formula, unit, source, horizon and confidence. Protected obligations and quality limits remain constraints, never weighted cost terms. Use the controlled Logistics Evolution Experiment record and independent logistics audit before promotion.

## Recommendations

The process-strength observer may return only:

- `KEEP_BASELINE`;
- `CONTAIN_AND_STRENGTHEN`;
- `TIGHTEN_ONE_CONTROL`;
- `PROPOSE_BOUNDED_VARIATION`;
- `PROPOSE_CONTROL_REDUCTION`.

It never changes the catalog, ALM, role prompt, approval rule or production routing. Recommendations contain breached guardrails, evidence periods, uncertainty, proposed control family, experiment cap, owner and rollback.

## Roles and Independence

- Continuous Improvement Architect owns aggregated process observation and proposes one reversible variant.
- Process and Quality Auditor independently checks adherence, KPI integrity, comparability and effectiveness.
- Operational Quality Inspector supplies independent output-quality and nonconformity signals.
- Quality Manager owns protected-quality guardrails and the strengthen/keep/reduce recommendation gate.
- Product Owner owns the value and task-class quality contract.
- Role and Skill Evolution Manager coordinates any durable role or harness change.
- Pepper reports material quality/process drift and decision needs to the founder.
- Jarvis checks technical automation, data provenance and safe implementation of measurement.
- The configuration owner and named human authority approve a trial or process change. No algorithm self-promotes a variant.

## Anti-Gaming and Data Protection

Report sample size, missing data and confidence. Segment by task class, complexity, domain, route, tool/model configuration and reviewer independence. Satisfaction is collected through an authorised source and is not inferred from private communications. Activity volume, lines of code, ticket count, model calls and process-step completion are not quality proxies.

Retire or redesign a KPI when it causes gaming, excessive observation cost, privacy risk or work displacement. Process observation evaluates the system and interfaces; it is not covert employee surveillance.
