# BIM Information Management Harness

## Purpose

Provide a reusable, openBIM-oriented delivery pattern for built-environment projects. The harness separates **information governance** from **model production** while linking both through versioned requirements, validation evidence, and accountable human decisions.

It applies to renovation, single-family, multi-family, and multi-building projects. A product project instantiates this harness in its own workspace; the Triton repository contains only the reusable process pattern and never the project's CAD, IFC, photographs, measurements, or customer data.

## Workflow 1 — Information governance

**Accountable lead:** Built Environment Architect.  
**Independent gate:** Quality Manager or a project-appointed accountable reviewer.  
**Configuration control:** Configuration Manager.

1. Frame the project: jurisdiction, contract, intended uses, exchange parties, scale, accountable humans, data boundary, and decision deadline.
2. Define a small, versioned information-requirements register. It states the object scope, property/information, unit or allowed values, evidence/source-status rule, delivery point, acceptance test, and reviewer.
3. Keep the human-readable register as the explanatory source. Derive machine-readable IDS only for the review-ready, testable subset.
4. Baseline the approved register and the applicable IFC schema/profile. A change identifies impact, owner, review, and rollback.
5. Review delivery evidence independently: model revision/hash, IDS profile/revision, validator/version, result, exceptions, evidence links, and decision.

**Stop conditions:** missing source for a compliance-relevant requirement; unclear accountable reviewer; an unbaselined requirement/schema change; an exception without an explicit decision; or a model claim that exceeds its evidence status.

## Workflow 2 — Model production and resolution

**Accountable lead:** Built Environment Architect for design coordination; discipline professionals retain their own professional accountability.  
**Contributors:** Civil Engineer, Structural Engineer, Interior and Exterior Design Manager, relevant services/procurement roles.  
**Quality role:** Construction Site Quality Inspector for work-package/field evidence; Quality Manager for process conformance where engaged.

1. Receive the baselined information requirements and perform a feasibility/mapping review before authoring.
2. Model and enrich only evidenced information. Use suitable standard IFC classes and established bSDD/IFC terms where available; do not invent a private property where an applicable, versioned term exists.
3. Mark every uncertain fact using the project source-status vocabulary; do not convert assumptions into properties that look verified.
4. Run internal IDS/schema/identifier and geometry-sanity checks before export.
5. Export the agreed open format. Select IFC4, IFC4.3, or another agreed profile from the exchange purpose and demonstrated tool compatibility; do not prescribe IFC4.3 by default.
6. Record issues in BCF where all participants can exchange it. Each issue references the affected model object(s), view, issue state, owner, due point, and resolution evidence. A controlled issue register is the fallback when BCF is unavailable.
7. Correct, revalidate, and submit the named model revision to Workflow 1 for independent delivery validation.

## Shared contracts

| Contract | Minimum content |
| --- | --- |
| Information requirement | purpose, object/property scope, data type/unit, source status, delivery point, test, reviewer |
| Model exchange | model ID/revision/hash, schema/profile, coordinate/unit convention, exchange purpose, accepted tool route |
| Validation report | IDS version, validator/version, pass/fail result, exceptions, source links, reviewer decision |
| BCF/issue record | issue ID, model revision, element GUID(s), viewpoint/reference, severity, owner, due point, state, resolution evidence |
| Change record | reason, impacted requirement/model/work package, decision, approval, rollback or revalidation route |

## Cadence and scaling

Use a short planning/authoring loop of two to six weeks, sized to the work package and evidence risk. Review the effectiveness of the harness periodically (for example quarterly) using first-pass acceptance, rework, blocked-work age, hand-off completeness, decision latency, and validation-exception trends. A six-month improvement horizon is not a delivery sprint.

## Boundaries

- IDS validates structured information against an IFC model; it is not a legal, permit, structural, fire, energy, utility, or geometric-correctness proof.
- ISO 12911 supports the structure of BIM implementation specifications; it does not supply project content.
- HOAI may be a planning reference for a German project but is not a default legal process for projects in other jurisdictions.
- BIM/GIS organisational integration is optional. Establish a defined interface when geospatial data is actually relevant.
- Qualified human professionals and authorities keep all mandated approvals.
