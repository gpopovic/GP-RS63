# Industrial Automation Assurance Adapter

Status: `CANDIDATE_NOT_ACTIVATED`

## Scope and Architecture Boundary

OPC UA, AutomationML, IEC 61131-3, IEC 61499 and PLCopen artefacts may support the same project, but they do not form a single AUTOSAR-equivalent platform:

- OPC UA supplies communication services and extensible AddressSpace information models;
- OPC UA NodeSets exchange information-model definitions, not a complete plant or controller assurance case;
- AutomationML exchanges engineering information and can reference complementary formats for topology, geometry, kinematics and control logic;
- IEC 61131-3 defines programmable-controller languages and execution concepts;
- IEC 61499 addresses distributed function-block systems and is not automatically the selected plant runtime;
- PLCopen specifications and libraries are applied only when the project and toolchain adopt the relevant profile.

The project shall identify plant type, controller and safety-controller architecture, field networks, machinery or process-safety scope, cybersecurity zones/conduits, operating modes, vendor tools, target hardware and applicable regulatory regime before selecting any of these candidates.

## Controlled Artefact Intake

1. Distinguish offline engineering files, exported NodeSets, live OPC UA endpoints, controller source, compiled artefacts, recipes, historian data and network captures.
2. Record source, exact release/schema, namespace URIs, vendor extensions, configuration baseline, hash, classification and authorisation.
3. Parse XML with external entities and network resolution disabled; use official or admitted libraries for binary/protocol encodings.
4. Validate schema, namespace ownership, references, data types, engineering units, access levels, method signatures, state models and project constraints.
5. Treat live endpoint discovery and read access as a separately approved connector capability. Default to no write, method call, subscription or control action.
6. Preserve source identifiers and provenance in an authorised graph view. AI-proposed relationships remain candidates until reviewed.

## Information Protection

Private IP addresses are network topology information, not automatically personal data. OPC UA NodeIds, browse paths, asset names, serial numbers, recipes, setpoints, credentials and network layouts receive project classifications. External routing uses stable local tokens only when meaning and traceability survive the transformation.

Credentials, private keys, certificates with private material, controller passwords, safety bypasses, production recipes classified as restricted, and exploit-enabling configuration are prohibited prompt content. They require hard blocking and controlled security operations.

## AI Output Boundary

AI may draft a quarantined function-block or Structured Text candidate, test idea, mapping or review finding. Syntax validation and successful compilation are insufficient for release. The relevant validation ladder includes:

1. response schema and allowed-action validation;
2. exact language/profile syntax and admitted compiler checks;
3. type, unit, range, state, concurrency and scan-cycle analysis;
4. hardware I/O mapping, retained state, startup/shutdown and fail-safe-state review;
5. safety-function/library provenance and change-impact assessment;
6. cybersecurity zone, identity, certificate and least-privilege review;
7. simulation, static analysis and representative unit/integration tests;
8. hardware-in-the-loop, factory/site acceptance and abnormal-condition tests as applicable;
9. independent safety/security/quality review;
10. named human approval and controlled download or deployment.

No AI route may directly download code, write setpoints, invoke control methods, modify a safety function or alter a production endpoint.

## Required Activation Evidence

- approved industrial project assurance profile and applicability record;
- exact standards, profiles, licences and vendor-tool compatibility matrix;
- plant and safety boundary, operating modes, hazards and security zones/conduits;
- admitted parsers, protocol clients, compilers and test tools with negative fixtures;
- data classification and external-route tokenisation tests;
- write-disabled connector admission and rollback evidence;
- independent review and named human engineering, safety and operations authorities.
