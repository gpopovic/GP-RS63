# BZS Applicability Record

Status: `DRAFT_NOT_APPROVED`

## Boundary

- Workspace: `BZS`
- Level: software platform subsystem
- Intended use: reusable OneBinary BZS software across centrifuge systems
- Markets, device classification and safety classification: `NEEDS_EVIDENCE`

## Source Applicability

| Source | Edition | Status | Intended use | Decision |
| --- | --- | --- | --- | --- |
| VDA QMC Automotive SPICE PAM | 4.1, 2026-08-24 | Official release verified | Organization, engineering lifecycle and evidence model | `PENDING_HUMAN_APPROVAL` |
| TriCorp Medical Device profile | Current workspace baseline | Template only | Medical and life-science product acceptance | `PENDING_ACTIVATION` |
| MDR 2017/745 or IVDR 2017/746 | Current consolidated law for target market | Official source identified | Candidate legal route determined by intended use and claims | `NEEDS_APPLICABILITY_DECISION` |
| ISO 13485 and ISO 14971 | Current controlled editions | Official sources identified | Candidate quality and risk-management basis | `NEEDS_APPLICABILITY_DECISION` |
| IEC 62304 | Current controlled edition | Official source identified | Candidate software lifecycle source when applicable; not final device validation/release | `NEEDS_APPLICABILITY_DECISION` |
| IEC 61010 series | Product-specific edition | Official source identified | Candidate laboratory-equipment safety basis | `NEEDS_PRODUCT_SPECIFIC_SELECTION` |

## Terminology Rule

`SOFTWARE` is the engineering abstraction level. It is not a SPICE process capability level. Capability remains `NOT_ASSESSED` until assessment scope, evidence and assessor authority are defined.

## Acceptance Rule

Automotive SPICE capability and process evidence support development assurance but cannot approve a medical or life-science product. Named human medical, quality and product authorities must accept the exact released configuration against its intended use, risks, target market and approved source matrix.

## Open Questions

- Confirm intended use, claims, applicable legal route, markets, device or laboratory-equipment classification, safety classification and standards for each consuming product.
- Approve the project-specific Automotive SPICE 4.1 process scope.
