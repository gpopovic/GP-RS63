# Software Change Release Evidence Profile

## Purpose and Boundary

This profile defines reusable evidence for software, plugin, automation, and toolchain changes. It was refined from external project experience, but it does not import project files, project status, or customer data into Triton_AI_Corp. A valid evidence manifest makes a candidate eligible for human release review; it never approves installation, production use, or a product change.

Evidence is candidate-specific. Every claim must identify the source revision, built artifact SHA-256, controlled environment, fixture set, execution time, raw logs, and independent reviewer. Results from another artifact hash, synthetic harness, machine, or workspace are not transferable without a recorded equivalence decision.

## Blocking Release Evidence

For `READY_FOR_RELEASE_REVIEW`, the candidate must demonstrate:

- all P0 requirements passed against explicit acceptance criteria;
- all blocking automated tests passed;
- all declared protected-state fields were checked and remained unchanged, with zero unexpected mutations;
- save/reopen, undo/redo, export determinism, and ambiguity-safety checks were either passed with evidence or explicitly not applicable with a reason;
- clean-build reproduction succeeded for every declared attempt;
- required live observation was passed, or non-applicability was justified;
- claims were derived from machine-readable results rather than hard-coded confirmations;
- raw logs, evidence references, rollback evidence, limitations, and an independent reviewer are recorded.

The protected-state list must be explicit for each work item. A generic statement such as “the model was preserved” is insufficient. Package inspection, compilation, and synthetic tests do not prove live GUI behaviour, installation, save/reopen behaviour, or production suitability.

## Diagnostic Measures

Track review latency, recovery time, read-only preflight performance, defect-regression coverage, escaped defects, and technical-debt closure as diagnostics. Do not assign universal numeric targets until at least three comparable work packages exist. Segment results by work type, candidate version, environment, complexity, fixture set, and reviewer independence.

## Evidence and Decision States

- `NEEDS_EVIDENCE`: the record may be structurally valid while blocking evidence is incomplete.
- `BLOCKED`: a known finding prevents progression.
- `READY_FOR_RELEASE_REVIEW`: the automated contract passes; a named human still decides release or installation.

The validator is `04_Execution_Engine/software_release_evidence.py`. Project-specific evidence remains in its external product workspace. Corp learning enters only through the sanctioned `KPI_Export.json` and `Lessons_Learned.json` interface defined by the Project-to-Corp Learning KPI Framework.
