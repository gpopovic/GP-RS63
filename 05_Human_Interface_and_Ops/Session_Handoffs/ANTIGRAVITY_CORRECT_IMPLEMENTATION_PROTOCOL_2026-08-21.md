# Antigravity Correct-Implementation Protocol — 2026-08-21

## Objective

Review and improve Triton_AI_Corp by understanding the intent behind rejected candidates and implementing that intent through controlled, evidence-backed abstractions. Rejection of an unsafe implementation is not rejection of the underlying capability.

Before using this protocol, read `ANTIGRAVITY_FULL_SYNCHRONISATION_DIRECTIVE_2026-08-21.md`. The full synchronisation directive contains later regulated-engineering, external-review, AUTOSAR, cross-domain adapter and TREM decisions that this earlier protocol does not enumerate.

## Authoritative Starting Set

Read these files before proposing or changing anything:

1. `05_Human_Interface_and_Ops/Manual_Quality_Gates/ANTIGRAVITY_PROGRESS_REVIEW_2026-08-21.md`
2. `01_Governance_and_Strategy/INFORMATION_ACCESS_AND_MINIMISATION_POLICY.md`
3. `01_Governance_and_Strategy/EVIDENCE_BACKED_CORPORATE_PULSE.md`
4. `01_Governance_and_Strategy/TASK_GRANULARITY_AND_PARALLELISATION_POLICY.md`
5. `01_Governance_and_Strategy/BUILT_ENVIRONMENT_AUTOMATION_CAPABILITY_CONTRACT.md`
6. `05_Human_Interface_and_Ops/Manual_Quality_Gates/PROCESS_MATURITY_EVIDENCE_TEMPLATE.md`
7. `06_Projects_and_Clients/PRODUCT_WORKSPACE_CONTRACT.md`
8. `01_Governance_and_Strategy/COMPANY_CONFIGURATION_INDEX.json`
9. `01_Governance_and_Strategy/EXTERNAL_REVIEW_CHANGE_INTAKE_POLICY.md`
10. `05_Human_Interface_and_Ops/External_Review_Intake/ANTIGRAVITY_DISPOSITION_REGISTER_2026-08-21.json`
11. `05_Human_Interface_and_Ops/Manual_Quality_Gates/OPEN_CONTROL_GAPS_REGISTER.json`

## Required Interpretation

| Original intent | Required Triton implementation |
| --- | --- |
| Information barriers | Explicit purpose, minimum scope, named data owner, applicable independent approval, expiry, revocation, and enforcement boundary. Never grant by title. |
| Corporate pulse | Read-only projection of controlled evidence. Every statement retains source, timestamp, owner, confidence, and classification. No self-authored company state. |
| Dynamic task sizing | Non-mutating recommendation from comparable evidence. Critical failures cause containment. Merge trials need at least three comparable accepted packages and human approval. |
| Process maturity | Framework/version-specific evidence matrix with independent review. Default is `NOT_ASSESSED`; no automatic certification or capability level. |
| BIM/construction automation | Capability contract plus separately admitted implementation. Use domain libraries and project inputs; never regex IFC, silent SH3D defaults, universal schedules, or source-free simulations. |
| Project learning | Accept only validated, sanitised exports from the external product workspace. Never invent or directly copy project status into Corp. |

## Implementation Sequence

1. State the capability, user decision, project class, jurisdiction, source standard/version, data class, and accountable owner.
2. Map the capability to an existing Triton contract before creating a new module.
3. Keep product data and generated deliverables in the external product workspace.
4. Add the smallest deterministic validator or adapter. Fail closed on missing provenance, units, schema, CRS, source version, uncertainty, approval, or review evidence.
5. Add positive, negative, boundary, malformed-input, duplicate, and regression tests. Synthetic fixtures prove software behaviour only, not domain readiness.
6. Record dependencies, licences, versions, permissions, network behaviour, rollback, and threat/data review through skill intake.
7. Run the fixed Corp baseline. Report exactly which checks ran and distinguish baseline success from project acceptance.
8. Append a change manifest containing changed files, reason, evidence, tests, unresolved limitations, and rollback. Do not overwrite earlier review history.
9. Reconcile every proposal or materially changed file group to one controlled disposition. Generic rejection or silent omission is prohibited; an unsafe implementation needs a documented harm and a safer target, justified non-requirement, or open follow-up route.

## Built-Environment Tool Rules

- IFC/IDS: use an IFC-aware library and declared schema; use IDS for machine-readable requirements and BCF for issues where supported.
- SH3D: back up and hash first; preserve user geometry, materials, elevations, and evidence layers; reject or escalate missing values.
- Point clouds: require CRS, units, acquisition and registration metadata, accuracy evidence, and outlier handling.
- Cost: require jurisdiction, taxonomy/version, quantity evidence, price source/date, currency, tax, reserve method, and estimate class.
- Schedule: distinguish existing building from new build and require dependencies, calendars, resources, constraints, duration sources, and uncertainty.
- Solar/environment: require location/weather, geometry, orientation, shading, engine/version, time basis, and relevant building assumptions.
- Revision diff: use stable IDs, hashes, geometry and semantic comparison, declared tolerances, and duplicate handling.
- Publishing: escape input, pin template/tool versions, retain a source manifest, validate output, and separate generation from approval/publication.

## Prohibited Claims and Actions

Do not claim completion, project status, model/provider availability, test counts, maturity, compliance, cost accuracy, structural safety, permit readiness, or production approval without a controlled evidence reference. Do not activate models, providers, MCPs, plugins, project writes, network transmission, or autonomous fixes merely because code exists.

## Required Result Format

The first line must be exactly one of `AUDIT_RESULT: PASS`, `AUDIT_RESULT: FAIL`, or `AUDIT_RESULT: NEEDS_EVIDENCE`.

Then provide: scope reviewed, intent understood, findings by severity, accepted changes, rejected alternatives, exact files changed, tests executed, evidence references, remaining limitations, and recommended next bounded step.
