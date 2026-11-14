# Sweet Home 3D Project KPI Learning Review — 2026-08-21

## Decision

**Disposition:** `PARTIAL_ACCEPTANCE / NEEDS_EVIDENCE`

The review accepts reusable control improvements and rejects the transfer of project-specific status, raw evidence, or uncalibrated KPI targets into Triton_AI_Corp. No Sweet Home 3D source, model, binary, customer artefact, or project execution record was copied into the Corp repository.

## Reviewed Boundaries

- External product workspace: `C:\Projects\Eclipse_WS\sweethome3D_SRC`
- External audit workspace: `C:\git\Triton_AI_Corp_Antigravity_Audit_Package_2026-08-15`
- Corp configuration workspace: `C:\git\Triton_AI_Corp`

The product workspace contained Markdown KPI and validation reports for multiple candidate states. No conforming `06_Learning_Exports/KPI_Export.json` and `06_Learning_Exports/Lessons_Learned.json` pair was available. Therefore the reviewed project values are not admitted as official Corp KPI observations or baselines.

## Data-Quality Assessment

| Dimension | Assessment | Consequence |
| --- | --- | --- |
| Grain | Mixed package, candidate, source-recovery, synthetic, and live-observation evidence | Results are not pooled into one score |
| Candidate identity | Later evidence is artifact/hash-specific; earlier reports contain broader claims | Only the general hash-specific control is adopted |
| Completeness | Early reports lacked live behaviour and protected-state coverage; later reports improved this | Missing evidence remains explicit, never inferred from compilation or unit tests |
| Comparability | Too few comparable work packages for stable universal timing or closure targets | Proposed numeric diagnostic targets are not adopted |
| Lineage | Useful paths and reports exist externally, but the sanctioned export interface is absent | Manual review informs hypotheses only |
| Decision readiness | Sufficient for Corp control improvements, insufficient for project KPI ingestion | Partial acceptance |

## Accepted Improvements

1. A reusable software/plugin release-evidence profile now separates P0 requirements, blocking tests, protected-state preservation, workflow behaviour, clean-build reproducibility, live observation, raw logs, rollback, and independent review.
2. Release evidence is bound to the exact source revision and artifact SHA-256. Synthetic or package-level evidence cannot silently stand in for live GUI or installation evidence.
3. `READY_FOR_RELEASE_REVIEW` requires machine-derived claims and remains a review state, not self-approval.
4. Diagnostic measures such as review latency, recovery time, preflight performance, and technical-debt closure remain target-free until at least three comparable work packages exist.
5. Information-access decisions are checked against a trusted evaluation time and their approval window.
6. Built-environment capability manifests now validate exact SHA-256 syntax and controlled data classifications.
7. Role loading is tested end-to-end for controlled Markdown, fictional work identity, and communication signature injection.

## Rejected or Deferred Inputs

- Raw Sweet Home 3D KPI values as an official Corp baseline: rejected because the controlled learning exports are absent.
- Universal timing, recovery, or technical-debt targets: deferred pending three comparable packages.
- Hard-coded GUI confirmation strings as evidence: rejected.
- Package inspection, compilation, or synthetic tests as proof of live UI behaviour: rejected.
- Product-specific operating instructions, status claims, models, binaries, or Ralja decisions inside the Corp configuration repository: rejected by workspace boundary.
- Role-title-based permissions, regex parsing of IFC STEP geometry, bounding-box terrain validation, universal DIN 276 use, and maturity certification inferred from unit tests: remain rejected.

## Verification and Approval Boundary

The Corp baseline must pass after these changes. This record does not approve a Sweet Home 3D installation, release, Ralja model mutation, construction action, or production activation. Those decisions require evidence and named human approval in the external product workspace.

Owner: `Role_Skill_Evolution_Manager`

Independent control: `Quality_Manager`

Configuration control: `Configuration_Manager`
