# Project-to-Corp Learning KPI Framework

## Purpose and Boundary

This framework measures whether a project-specific harness improves Triton_AI_Corp roles, controls, and information flows. It does not evaluate a person, contractor, customer, or model in isolation. Project artefacts remain in the external project workspace; only aggregated KPI observations and sanitised lessons may enter Triton_AI_Corp through the Product Workspace Contract.

Start with three accepted, comparable work packages as a baseline. Do not set pass/fail targets before that baseline exists. Segment every result by harness version, work-package type, complexity, data class, and reviewer independence.

## Core Learning KPIs

| KPI ID | Calculation | Ralja application | Improvement decision | Guardrail |
| --- | --- | --- | --- | --- |
| `evidence_to_decision_completeness` | decisions with source, uncertainty, owner, gate, and evidence reference / reviewed decisions | CAD-baseline and design decisions | Improve evidence register or gate prompt when incomplete | Missing evidence blocks a material decision |
| `baseline_stability_after_approval` | approved CAD elements not materially revised due to pre-existing uncertainty / reviewed approved elements | Sweet Home 3D/CAD baseline | Improve survey, geometry reconciliation, or status labels | Do not treat a necessary owner change as a defect |
| `early_constraint_discovery_rate` | material constraints found before downstream commitment / all material constraints found | moisture, structure, permit, utilities, access | Improve opposition/review harness or project intake | A late critical safety issue triggers containment, not KPI optimisation |
| `first_pass_independent_acceptance` | outputs accepted at independent review without material rework / independently reviewed outputs | drawings, quantity drafts, decision records, work packages | Improve the originating role/harness only after comparable samples | Report severity and sample size; never conceal findings |
| `construction_rework_ratio` | corrective effort caused by an avoidable planning/information defect / total effort for the work package | only for executed construction work | Improve information hand-off or construction readiness criteria | Separate changed requirements and unforeseen existing conditions |
| `decision_lead_time` | median elapsed time from complete evidence package to recorded decision | baseline approvals and change decisions | Reduce waiting or unclear ownership | Do not accelerate by skipping an applicable gate |
| `harness_usefulness_rating` | independent human rating of usefulness, 1–5, with reason / reviewed uses | whether the staged workflow helped practical planning | Keep, trial, adjust, or retire a harness step | A high rating never overrides quality/safety evidence |

## Supporting Diagnostics

- `role_handoff_completeness`: hand-offs containing input, owner, decision, evidence, next action, and due date / reviewed hand-offs.
- `reviewer_disagreement_rate`: material review disagreements / reviewed outputs; classify as productive evidence gap, ambiguous requirement, or process defect.
- `forecast_accuracy`: `1 - abs(actual - forecast) / max(forecast, small positive floor)` for time/cost/risk estimates, reported by comparable work-package type.
- `model_or_tool_failure_rate`: failed or unusable tool-assisted outputs / assessed tool uses, reported per exact version and task class. It never becomes an individual-performance metric.

## Ralja Feedback Cadence

| Trigger | Minimum export | Review and action |
| --- | --- | --- |
| CAD baseline approved | completeness, baseline uncertainty count, usefulness rating | Decide whether the CAD/baseline harness is ready for variants |
| Each material design or investigation package | all applicable core metrics and one lesson | Quality + domain reviewer propose `keep`, `adjust`, or `strict mode` |
| Construction work-package completion | rework, constraint discovery, forecast accuracy | Update ready-to-build criteria; do not alter static/permit decisions without competent review |
| Three comparable completed packages | trend and confidence note | Corp review may authorise a micro-trial of one role, prompt, template, or gate |

## Closed Learning Loop

1. Record project evidence and the project decision in Ralja_House.
2. Export only `KPI_Export.json` and `Lessons_Learned.json` from `06_Learning_Exports`.
3. Validate the export in the project workspace.
4. Corp reviewers assess data quality, comparability, and guardrails.
5. Create a non-mutating improvement hypothesis: `keep`, `trial`, `promote`, `rollback`, or `retire`.
6. A human approves a material Triton_AI_Corp configuration change through the existing control board.
7. Compare the trial to the preserved baseline; retain or roll back the change.

No feedback export authorises a product change, construction action, model activation, provider transfer, or modification of the source Sweet Home 3D/CAD model.

Markdown reports, audit folders, and manually copied scorecards may inform a review hypothesis, but they are not admitted as official Corp KPI observations. Automated admission requires the two sanctioned, validated export files named above; absence of those files must be recorded as `NEEDS_EVIDENCE`, not silently substituted.
