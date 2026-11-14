# Antigravity Review Disposition — 2026-08-17

## Scope

Independent review of changes made in `C:\git\Triton_AI_Corp_Antigravity_Audit_Package_2026-08-15`. The audit package is not the authoritative Triton configuration; no change is adopted by copying it wholesale.

## Accepted correction

| Finding | Disposition | Evidence required |
| --- | --- | --- |
| Result parsers accepted only literal, unformatted first-line `RESULT:` markers and could reject a valid Markdown-wrapped decision marker. | Accepted with a constrained implementation. `master_graph.py` and `deliberation_graph.py` now accept only a first-line controlled marker with limited Markdown formatting. They do not accept a marker merely mentioned later in narrative text. | Focused positive and false-positive tests, plus the fixed baseline. |

## Rejected changes and reason

| Proposed change | Disposition | Reason |
| --- | --- | --- |
| Add `Executive_Steward_and_Operations_Guard` and `Chief_Engineer_and_Systems_Architect` as permanent activation-profile and registry roles. | Rejected. | Their responsibilities overlap existing accountable roles and would increase default active-team size. Persona/call-sign concepts do not establish a needed independent control boundary, role source mapping, KPI profile, or evidence of recurring work. |
| Replace central `config.py` with simplified role/model loading. | Rejected. | It removes persona/KPI loading, central paths, approved capsule location, and fail-closed lane resolution; it adds a broad heuristic default model route. |
| Replace workspace contract/validator with simpler create/validate logic. | Rejected. | It weakens workspace-ID normalisation, external-root containment, manifest invariants, learning-export requirements, and command-line validation. |
| Replace KPI/cost engine and its coverage test. | Rejected. | It removes visible reserve forecasting and complete role-KPI coverage in favour of an unrelated simple cost sum. |
| Replace company/role validation and current smoke tests. | Rejected. | It reduces declared-path validation and removes important observer/call-cap/profile-coverage assertions. Additive test cases may be useful; replacement is not. |
| Replace evidence-led model observation with an in-memory/override implementation. | Rejected. | It removes append-only observations, evidence thresholds, route safeguards, and human escalation evidence. |
| Add a second handoff validator and JSON schema. | Deferred. | The existing handoff contract already has an executable validator and baseline test. A schema can be considered later only if it becomes the single declared contract, validates dates/owners/data classes consistently, and receives its own tests and configuration-index entry. |

## Verification

The accepted correction is not a release claim until `04_Execution_Engine/run_company_baseline.py` passes in the authoritative Triton workspace.
