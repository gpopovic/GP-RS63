# Task Granularity and Parallelisation Policy

## Purpose

Select the smallest work package that can produce independently reviewable evidence without creating administrative waste. This policy controls task sizing; it does not automatically rewrite a backlog or change a production harness.

## Sizing Modes

| Mode | Use when | Required exit evidence |
| --- | --- | --- |
| `FINE_ATOMIC` | risk, uncertainty, interface ambiguity, repeated review bounce, or failed quality gate is material | one narrow output, named owner, explicit acceptance check |
| `STANDARD_SLICE` | dependencies and acceptance are understood and the slice can be reviewed end to end | accepted outcome plus evidence reference |
| `MACRO_BATCH` | several low-risk slices are genuinely repeatable and have comparable clean evidence | batch-level reconciliation and sampled independent review |

## Split Triggers

Split or sequence a work package when any of the following applies:

- a safety, privacy, security, legal, structural, financial, or release-critical uncertainty cannot be isolated;
- two material clarification or review loops show that the input/output contract is unclear;
- one failed gate reveals separable remediation, verification, or dependency work;
- a package contains more than one accountable decision or cannot be rolled back as one unit; or
- parallel lanes would modify the same baseline, assumption, or decision record.

A critical escaped defect triggers containment and independent review. It is not merely a task-sizing signal.

## Merge Triggers

Merge repeatable low-risk slices only after at least three comparable accepted packages show:

- no material escaped defect;
- no unresolved review bounce;
- stable input and acceptance contracts;
- no loss of traceability or rollback; and
- a measured reduction in cycle time or coordination cost.

Macro batching is prohibited for high-blast-radius decisions and for work requiring qualified human sign-off.

## Parallelisation Gate

Use at most three lanes and only when their inputs, outputs, tools, write scopes, and acceptance checks are independent. Each lane needs an owner, cap, stop condition, and evidence location. One named integration owner resolves contradictions and produces the single accepted record.

Do not parallelise dependent construction sequencing, changes to one CAD/BIM baseline, final legal or structural decisions, shared configuration writes, or tasks whose evidence must be observed in chronological order.

## Learning and Change Control

Flow measures are diagnostic, not universal thresholds. Segment observations by task class, risk, toolchain, and workspace. After three comparable observations, the Continuous Improvement Architect may propose one reversible trial. The configuration owner records the decision; no script or agent may silently mutate task-sizing thresholds, harness routing, or ALM records.

Product task records remain in their external product workspace. Only sanitised KPI and lesson exports may enter Triton_AI_Corp under the product-workspace contract.
