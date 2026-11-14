# Built Environment Delivery Framework

## Purpose

This is Triton_AI_Corp's reusable operating framework for residential renovation, single-family homes, bungalows, multi-family buildings, and multi-building developments. It is a process and information-management framework; it never substitutes for a licensed architect, engineer, site manager, fire-safety specialist, surveyor, authority, contractor, or the accountable client.

Ralja is one project profile under this framework, not the framework itself.

## Phase Reference and Jurisdiction Rule

Use the nine HOAI phases as a familiar planning reference: `LPH 1` Basic Evaluation, `LPH 2` Preliminary Planning, `LPH 3` Design Planning, `LPH 4` Approval Planning, `LPH 5` Detailed Design, `LPH 6` Tender Preparation, `LPH 7` Tender Support, `LPH 8` Construction Supervision and Documentation, and `LPH 9` Post-Completion Support. The phase logic applies to new build, conversion, modernisation, repair, and maintenance work.

HOAI, DIN, VOB, German building law, or any other national standard applies only when the project jurisdiction, contract, and qualified reviewer establish that it applies. Every project profile must name its jurisdiction, governing contract, permit route, and required competent professionals before a binding decision.

## Universal Stage Gates

| Stage | Main purpose | Minimum evidence before exit | Default engagement |
| --- | --- | --- | --- |
| `BE-0` Project profile and scope | Establish jurisdiction, building type, delivery strategy, budget boundary, data boundary, and accountable humans | approved project profile and decision rights | Client/owner designs; quality evaluates |
| `BE-1` Existing condition / site baseline | Establish reliable geometry, condition, utilities, constraints, and uncertainty | versioned CAD/BIM baseline, source register, measured versus assumed status | Architect/CAD role designs; independent reviewer evaluates |
| `BE-2` Preliminary and design planning | Develop options that reconcile use, cost, structure, envelope, services, planning, and buildability | selected option, assumption register, cost/time range, specialist needs | domain lanes contribute; opposition challenges |
| `BE-3` Permit and technical coordination | Prepare only the approvals and technical evidence applicable to the project | permit/authority decision path, coordinated technical inputs, unresolved-risk list | qualified human specialists evaluate/approve |
| `BE-4` Detailed design and procurement readiness | Make a package buildable and measurable | drawings/details, `predmer`/quantities where applicable, hold points, acceptance criteria | design and cost lanes contribute; quality evaluates |
| `BE-5` Tender, award, and mobilisation | Select scope-compatible suppliers and confirm readiness | bid comparison, exclusions, programme, insurance/safety/contract checks as applicable | procurement contributes; technical and commercial evaluators assess |
| `BE-6` Construction integration | Coordinate work fronts, dependencies, inspections, changes, and records | short look-ahead plan, constraint log, inspection/hold-point evidence | site lead coordinates; active trades contribute; quality observes/evaluates |
| `BE-7` Acceptance and close-out | Separate technical readiness, contractual acceptance, defects, and handover | protocol, defects/reservations, test evidence, handover records | accountable client and competent professionals decide |
| `BE-8` Operation and learning | Verify defect follow-up, maintainability, costs, and harness learning | maintenance/defect plan and sanitised learning export | owner operates; Corp reviews aggregate learning |

## Scalable Coordination Pattern

| Project complexity | Minimum coordination pattern | Add when evidence requires it |
| --- | --- | --- |
| Single-family house / bungalow | Stage-gated design review plus event-driven discipline review; weekly look-ahead only during active works | survey, structural, services, permit, moisture, energy, or procurement specialists |
| Multi-family building | Formal discipline coordination, change register, recurring look-ahead, independent quality sampling, structured handovers by system/area | fire safety, acoustics, accessibility, energy, multiple service disciplines, tenancy/use and authority interfaces |
| Multi-building / block development | Area/system breakdown, programme board, cross-building dependency management, formal change-control board, package-level quality and cost reporting | multiple delivery teams, shared utilities/infrastructure, phased approvals, central information management, client programme governance |

Use Lean/Last-Planner-style look-ahead and constraint removal during active construction. Borrow the useful SAFe ideas of visible dependencies, capacity-aware planning, and retrospective learning, but do not relabel contractual or statutory construction responsibilities as software roles.

## Active-Site Planning and Handover Controls

During active work, the project profile may use milestone pull planning, a rolling look-ahead, a commitment plan, and short site coordination. The horizon and cadence follow current work fronts, trade interfaces, access, material lead times, weather, permits, inspections, and contractual duties; they are not universal six-week, weekly, or daily requirements. A task may be committed only when its declared prerequisites are ready or an accountable person accepts the recorded exception.

Before work is concealed or handed to the next trade, the project defines the applicable self-check, independent or successor check, hold point, measurement method, evidence, nonconformity route, and release authority. Visual controls, bilingual job aids, photographs, and physical error-proofing may support the check, but do not replace calibrated measurement, contract evidence, privacy controls, or a competent inspection. A discrepancy stops only the affected unsafe or nonconforming work scope; response time follows severity, exposure, site conditions, and the approved escalation route rather than a universal service level.

Project-specific terminology, dimensional tolerances, reinforcement details, colour conventions, payment conditions, geolocation, and contractor ratings belong in the controlled external project workspace. They must not be inferred from a generic Corp playbook or written into the role registry. Payment and contractual acceptance remain separate from technical observation and require the applicable human authority.

## Required Project Profile Fields

- project type: `new_build`, `renovation`, `conversion`, or `mixed`;
- scale and delivery boundaries: building(s), areas, packages, and active trades;
- jurisdiction, governing contract, authority/permit route, and applicable standards;
- source-of-truth location, CAD/BIM status, revision/issue convention, and information-exchange requirements;
- accountable client, named qualified professionals, decision rights, and escalation route;
- stage gates, hold points, acceptance protocol, change-control route, and learning-export cadence.

## AI Boundaries

AI may prepare a source-linked register, compare alternatives, identify conflicts, draft a `predmer`, organise evidence, and track constraints. AI may not make a binding design, structural, fire-safety, permit, procurement, site-safety, acceptance, or payment decision; claim a measurement it did not verify; or overwrite a controlled CAD/BIM baseline.
