# OneBinary Platform Contract

Status: `DRAFT_NOT_APPROVED`

## Invariant

One released BZS platform binary is reused across admitted centrifuge products. Product variation is supplied by controlled parameter and production-data packages. A product-specific source fork is an exception requiring change-impact analysis and explicit approval.

## Configuration Identity

A deployable configuration is identified by:

1. source revision;
2. reproducible binary SHA-256;
3. compiler, linker and generator toolchain baseline;
4. parameter-schema version;
5. product parameter-package ID and hash;
6. target hardware and bootloader compatibility class.

## Separation of Evidence

- BZS proves reusable software behavior and the permitted parameter envelope.
- Each system workspace proves its selected values, hardware compatibility, integration behavior, hazards, verification and intended-use validation.
- Evidence from one product is not automatically transferable to another product without a recorded equivalence decision.

## Medical Acceptance Boundary

- Automotive SPICE structures development and reusable evidence; it does not constitute medical product acceptance.
- A shared binary never transfers final approval automatically. Each product variant requires risk-based verification and intended-use validation of its exact binary, parameter package, production data, hardware and interfaces.
- A parameter or production-data change is a controlled configuration change. Its safety, performance and regulatory impact must be assessed before release even when the binary is unchanged.
- Final risk acceptance, applicability decisions, waivers and release approval require named human medical, quality and product authorities.

## Stop Conditions

Create a new binary baseline when a requested variation exceeds the approved parameter envelope, changes interfaces or resources, invalidates a safety/security assumption, or is incompatible with the admitted target class.
