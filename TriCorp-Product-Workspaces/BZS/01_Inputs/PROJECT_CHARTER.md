# BZS Project Charter

Status: `DRAFT_NOT_APPROVED`

## Classification

- Engineering abstraction level: `SOFTWARE`
- Project role: `ONE_BINARY_PLATFORM_SOFTWARE_SUBSYSTEM`
- Primary process scope candidate: `SWE.1` through `SWE.6`
- Supporting process candidates: `SUP.1`, `SUP.8`, `SUP.9`, `SUP.10`, `MAN.3`, `MAN.5`, `REU.2`
- Process capability level: `NOT_ASSESSED`

## Governance and Acceptance

Automotive SPICE 4.1 structures the engineering organization, roles, processes, work products and evidence. Medical and life-science requirements govern intended-use classification, risk acceptability, verification, validation and final product release. Automotive SPICE assessment results are not medical product approvals.

## Intended Outcome

Develop and release one controlled BZS platform binary for reuse across centrifuge system products. Product behavior is adapted through validated parameter and production-data packages rather than product-specific source forks by default.

## Boundary

This workspace owns platform requirements, software architecture, implementation, build configuration, binary releases, parameter-schema contracts, software verification and reusable release evidence. Product-specific system requirements, parameter values, system integration and product validation remain in the consuming system workspace.

## Open Decisions

- Confirm supported hardware, bootloader, memory and interface compatibility classes.
- Define which variation points may be parameters and which require a new binary baseline.
- Name parameter-data approval authorities and production provisioning controls.
- Confirm classification, intended use, claims, markets, applicable medical/laboratory-equipment sources, safety class and required reviewer independence for every consuming product.
