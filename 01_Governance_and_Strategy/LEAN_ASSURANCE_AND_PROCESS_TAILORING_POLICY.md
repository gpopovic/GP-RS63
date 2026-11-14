# Lean Assurance and Process Tailoring Policy

## Purpose

Achieve the declared quality outcome with the smallest sufficient set of controls, evidence and coordination. Process is a means of producing quality and assurance, not a measure of quality by its volume.

This policy does not permit Triton or a project to waive applicable law, regulation, permit conditions, contractual duties, certification commitments, customer-mandated evidence or required professional approval. It prevents optional, duplicated, legacy or speculative process from being mistaken for a mandatory obligation.

## Operating Principle

> Use only the process needed to satisfy applicable obligations, control the real risk and demonstrate the agreed quality standard. Generate reusable evidence during the work so the project does not later repeat the work merely to reconstruct compliance.

The goal is `compliance-ready by design`, not premature certification theatre. A team should structure requirements, decisions, baselines, tests and reviews so that likely applicable evidence exists naturally. It must not execute a complete external assessment process before applicability, scope and business intent are confirmed.

## Step 1 — Classify the Process Demand

Every material process demand belongs to one class:

| Class | Meaning | Tailoring rule |
| --- | --- | --- |
| `MANDATORY_EXTERNAL` | applicable law, regulation, permit, authority condition or required professional duty | cannot be removed; implementation may be simplified only when the authority permits it |
| `BINDING_COMMITMENT` | contract, approved certification basis, customer requirement or accepted supplier obligation | change only through the authorised contractual or governance route |
| `QUALITY_CRITICAL` | necessary to meet an explicit quality attribute or acceptance criterion | keep the smallest control that provides objective evidence |
| `RISK_TRIGGERED` | added because consequence, uncertainty, novelty, data sensitivity, irreversibility or blast radius crosses a declared trigger | remove when the trigger no longer applies and evidence supports removal |
| `OPTIONAL_IMPROVEMENT` | useful optimisation, coaching or experiment | time-box; continue only with measured benefit |
| `LEGACY_OR_DUPLICATE` | has no current obligation, quality outcome, risk control or unique evidence consumer | remove or merge after confirming that no downstream dependency remains |

The applicability owner records the source and exact scope for external or binding demands. “This is best practice”, “an auditor might want it” or “another industry does it” is not sufficient to classify a process as mandatory.

## Step 2 — Define the Quality Contract Before the Process

For each material work package, define only the relevant quality attributes and acceptance evidence. Candidate attributes include:

- functional correctness and completeness;
- safety or structural integrity;
- security and privacy;
- reliability, recoverability and operability;
- performance and resource use;
- maintainability, portability and compatibility;
- usability and human factors;
- traceability, configuration integrity and reproducibility limits;
- legal, contractual or professional acceptance.

State the consequence of failure, evidence needed to decide, named decision owner and stop condition. Do not select every attribute by default. An internal grammar correction, a reversible prototype, production code, a structural calculation and a medical safety requirement need different quality contracts.

## Step 3 — Select the Minimum Sufficient Assurance Route

Use one of three routes through the existing adaptive harness; do not create a second workflow:

| Route | Typical use | Minimum control set |
| --- | --- | --- |
| `LEAN` | low-consequence, reversible, no sensitive data, no external obligation | clear outcome and owner, acceptance check, versioned result and rollback where applicable |
| `STANDARD` | material product or business effect | LEAN plus independent or peer review, deterministic tests, change impact, evidence references and release decision |
| `ASSURANCE` | safety/security/privacy/high-consequence or externally governed work | STANDARD plus applicability, traceability, independence, qualified-human authority and domain-specific evidence |

Start with the least intensive route that can meet the quality contract. Add a control only when it has a named obligation, risk, failure mode, evidence consumer or measured improvement purpose. A higher route does not mean every conceivable ceremony, role or document is required.

For an operational capability, the normal implementation unit is a thin vertical slice: controlled input, the minimum business logic, an inspectable output and an acceptance check. Add architecture, policy or evidence records only where the quality contract or a named consumer requires them. Do not substitute a collection of schemas, policies and validators for the requested capability, and do not require executable code when the requested deliverable is genuinely a policy, decision record or assessment.

## Progressive Assurance Triggers

Increase the route only when evidence shows one or more of:

- an applicable external or binding requirement;
- safety, security, privacy, structural, legal, financial or release-critical consequence;
- irreversible or high-blast-radius change;
- novel technology or tool reliance without adequate independent error detection;
- sensitive cross-boundary data movement;
- repeated escaped defects, review bounce or ambiguous acceptance;
- supplier, authority or professional-sign-off dependency;
- missing provenance, configuration baseline, rollback or verification evidence.

Decrease the route when the trigger is removed, the work is reversible and comparable evidence shows the smaller control set maintains the quality contract.

## Evidence Once, Reuse Many Times

Normal engineering activity should create its evidence as a by-product:

- the ALM item or controlled outage fallback holds the outcome, owner, acceptance and status;
- version control holds the exact change and review history;
- automated tests and deterministic tools produce machine-readable evidence;
- architecture and risk decisions identify rationale, assumptions and affected baselines;
- the approved evidence store retains controlled references, integrity and retention metadata;
- the release or professional decision points to the same evidence rather than requesting a duplicate report.

Do not maintain the same status, requirement, risk, test result or approval manually in several systems. Create a presentation or regulator-specific package from controlled source evidence when required; do not recreate the underlying engineering history.

## Tailoring Decision Rule

The configured default route needs no separate tailoring ceremony. Add a short decision record only when:

- an applicable external or binding process is interpreted, simplified or changed;
- a normally required control is omitted, substituted or sampled;
- a work package moves to or from the ASSURANCE route;
- evidence will serve more than one authority, customer or lifecycle purpose;
- residual uncertainty is accepted instead of resolved.

The record contains the demand class, quality contract, selected route, included and omitted controls, rationale, evidence, owner, independent reviewer where required, expiry or reconsideration trigger and affected baseline. One ALM record or approved template is sufficient; no meeting is required unless a real decision cannot be resolved asynchronously.

## Anti-Perfectionism and Stop Rules

Stop adding process when every applicable obligation, declared quality attribute and material risk has objective acceptance evidence. Additional review, documentation or roles require a named incremental benefit.

Do not pursue undocumented “maximum quality”. If the desired quality level changes, update the quality contract, cost/time forecast and decision owner. Do not hide time, cost or uncertainty behind ceremonial completeness.

Contain and correct a critical defect, but do not answer every defect by permanently adding another gate. First determine whether the cause was missing knowledge, unclear acceptance, poor automation, excessive handoff, inadequate control or non-adherence to an adequate existing process.

## Process Removal and Consolidation

A process is a removal or consolidation candidate when it:

- has no current obligation source or accountable evidence consumer;
- duplicates information already controlled elsewhere;
- produces no decision, risk reduction or measurable quality evidence;
- creates more queueing, handoff or rework than the failure mode it controls;
- persists after its original risk trigger expired;
- can be replaced by an automated check or evidence generated at source.
- has remained dormant beyond its declared review trigger, has no observed consumer, or validates only structure already enforced by another controlled component.

Removal requires a dependency check, owner decision, rollback route and bounded observation. Safety, legal, contractual or professional controls require the applicable independent authority before removal.

Review consolidation through the existing configuration-management lifecycle; do not create a separate cleanup board or standing meeting. At a normal baseline review, configuration owners may flag an item as active, triggered-dormant, consolidation-candidate or retirement-candidate, with the consumer and dependency evidence needed for a decision. Absence of recent use alone does not justify removing a contingency, legal or high-consequence control.

## Improvement Measures

Measure process effectiveness rather than process volume:

- accepted first-pass rate and escaped defects;
- rework caused by missing evidence versus rework caused by unnecessary process;
- decision and review wait time;
- duplicate data-entry and evidence-reconstruction effort;
- automated evidence reuse;
- review findings that changed the outcome;
- assurance cost and model/tool cost by task class;
- recovery time and rollback success;
- contributor cognitive load and work-in-progress age.
- accepted operational outcome effort compared with control, handoff and evidence-reconstruction effort, segmented by task class;
- configuration items with no observed consumer, duplicated source data or expired activation purpose, treated as review signals rather than automatic deletion criteria.

Do not set universal numeric targets from theory. Compare at least three genuinely comparable accepted work packages before proposing a reversible routing or control-set trial. No agent may silently reduce a mandatory control or mutate the default route.

Process-strength feedback, quality guardrails and bounded evolutionary trials follow `PROCESS_STRENGTH_OBSERVATION_AND_EVOLUTION_POLICY.md`.

## Roles

- Product Owner defines the quality contract and value/time boundary.
- Safety and Compliance Engineer and General Counsel determine applicable external obligations with the relevant domain authority.
- Quality Manager checks whether evidence is sufficient and whether tailoring creates false assurance.
- Continuous Improvement Architect measures flow, duplication, rework and proposes bounded simplification trials.
- Pepper protects founder visibility, business priorities and organisational simplicity.
- Jarvis maintains technical consistency, automation and evidence-at-source integration.
- The named human authority approves material tailoring. AI may recommend but never waive an obligation or self-approve a reduced control set.
