# Role and Skill Evolution Governance

## Objective

Continuously improve Triton roles and skills through evidence-led evaluation and bounded variation. The system may create proposals and trial candidates; it may not replace an active artifact by itself.

See `ROLE_AUTONOMY_AND_EVOLUTION_POLICY.md` for adaptive operating modes, role-split criteria, and lean-process rules. See `01_Governance_and_Strategy/ENTERPRISE_KPI_CATALOG.md` for the enterprise KPI hierarchy.

## KPI Set

| KPI | Direction | Definition |
| --- | --- | --- |
| Quality pass rate | higher | Share of evaluation cases meeting all stated acceptance criteria |
| Traceability coverage | higher | Share of material claims linked to an input, test, or evidence artifact |
| Rework rate | lower | Mean correction cycles required after independent review |
| Median latency | lower | Median seconds to a completed, valid artifact for comparable cases |
| Estimated cost | lower | Estimated local or approved-provider cost per valid artifact |
| Reviewer disagreement rate | lower | Material challenges not resolved in the first review cycle |
| Severe failure rate | lower | Security, privacy, integrity, or critical-quality failures per evaluated case |

## Non-negotiable Guardrails

- Compare a candidate with its baseline on the same versioned, held-out local evaluation set.
- Require at least 10 observations per comparable baseline/candidate pair before a promotion recommendation.
- Reject a candidate with any severe failure, lower quality pass rate, lower traceability coverage, or a material regression in another protected KPI.
- Treat latency and cost as secondary optimisation targets; they cannot compensate for a quality or safety regression.
- Store observations append-only. Preserve the source artifact, candidate mutation, evaluator, benchmark version, and result.
- Permit only one bounded mutation per candidate: clarify a workflow step, tighten an output schema, add a guardrail, add a negative test, or remove redundant wording.

## Promotion States

`baseline` -> `trial` -> `recommended` -> `active` -> `retired`

The Evolution Manager may move an artifact to `recommended` only. The Configuration Manager applies a versioned activation after the defined quality gate has accepted the recommendation.

## Capability Discovery

Propose a new role or skill only when a recurring capability gap is evidenced by at least three comparable observations, cannot be resolved by an existing role or skill, and has a defined owner, boundary, KPI, and evaluation set.
