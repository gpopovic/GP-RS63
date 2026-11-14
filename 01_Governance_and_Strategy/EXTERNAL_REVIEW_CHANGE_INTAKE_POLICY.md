# External Review Change Intake and Disposition Policy

## Purpose

Preserve useful changes, criticisms, and capability intent from Antigravity and any other external reviewer without copying unsafe implementations into the authoritative Triton baseline. No proposal may disappear merely because its submitted implementation is rejected.

## No-Silent-Drop Rule

Every atomic proposal, changed capability, criticism, or materially changed file group receives a stable intake ID and exactly one controlled disposition:

- `ACCEPTED`: incorporated without changing its material intent;
- `ADAPTED`: useful intent incorporated through a safer or more effective implementation;
- `SUPERSEDED`: a later controlled decision or implementation covers the same intent better;
- `DUPLICATE`: an authoritative existing control already covers the complete intent;
- `DEFERRED`: useful intent retained with a named trigger, owner, and evidence requirement;
- `REJECTED_HARMFUL`: the proposed intent or implementation would damage a protected process, control, product boundary, safety, security, privacy, quality, legality, cost control, traceability, or maintainability;
- `NEEDS_EVIDENCE`: the proposal or source inventory is too incomplete to decide;
- `REFERENCE_ONLY`: contextual snapshot material that makes no change proposal.

Generic `REJECTED`, omission, deletion without a disposition, or silence is prohibited.

## Rejection and Replacement Test

`REJECTED_HARMFUL` is valid only when the record identifies:

1. the protected outcome or control that would be harmed;
2. evidence or a reproducible reasoning chain for that harm;
3. whether the underlying capability remains required; and
4. either the authoritative safer replacement or an explicit, justified `NOT_REQUIRED` decision by the accountable owner.

`ADAPTED`, `SUPERSEDED`, and `DUPLICATE` require an authoritative target and evidence that it covers the original capability intent. A different filename or architectural preference is not sufficient.

`DEFERRED` and `NEEDS_EVIDENCE` remain open. They require an owner, a concrete follow-up trigger, required evidence, and a review date. They may not be reported as rejected or complete.

## Intake Completeness

Each external delivery should provide a machine-readable change manifest containing stable item IDs, changed paths, hashes, capability intent, dependencies, tests, limitations, and proposed acceptance criteria. The Configuration Manager compares the new manifest with the prior accepted snapshot.

When a source package lacks a complete manifest, record `intake_completeness: NEEDS_EVIDENCE`, create an open reconciliation finding, and review the known proposals without claiming package-complete coverage. File timestamps, test presence, or a narrative summary are not a substitute for an inventory.

## Review Workflow

1. Freeze or identify the external review snapshot and record its source reference.
2. Inventory atomic proposals and changed file groups; compare with the previous source manifest.
3. Map every item to its capability intent and affected Triton configuration items.
4. Assess benefit, harm, duplication, alternatives, boundary impact, evidence, and rollback.
5. Assign one controlled disposition and the accountable owner.
6. For accepted or adapted items, implement the smallest controlled change and verify it independently.
7. For deferred or evidence-deficient items, retain an open finding with trigger and acceptance evidence.
8. Reconcile intake count, disposition count, unresolved count, changed paths, and verification before closing the review.
9. Append history. Never rewrite a prior disposition; a later decision uses `SUPERSEDED` and links the earlier item.

## Roles

- Configuration Manager owns snapshot identity, manifest comparison, configuration targets, and baseline evidence.
- Role and Skill Evolution Manager owns capability-intent preservation and role/skill alternatives.
- Quality Manager checks completeness, protected outcomes, verification, and false closure.
- Chief Engineer and Systems Architect coordinates cross-cutting technical alternatives.
- Privacy, Security, Legal, Finance, Safety, and domain owners assess their protected boundaries.
- The named human authority approves material activation. Neither the external reviewer nor Triton self-approves production use.

## System-of-Record Boundary

The disposition register is audit evidence, not a delivery backlog. Open implementation work must be represented in the approved ALM or its controlled outage fallback. The Corp open-control-gap register tracks unresolved control findings and links the ALM item when work begins.
