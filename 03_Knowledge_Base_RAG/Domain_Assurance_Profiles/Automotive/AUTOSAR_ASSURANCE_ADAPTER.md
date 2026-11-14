# AUTOSAR Assurance Adapter

Status: `CANDIDATE_NOT_ACTIVATED`

## Purpose and Boundary

This adapter maps AUTOSAR engineering artefacts into Triton's Regulated Engineering Assurance Kernel. It does not activate an AUTOSAR release, vendor toolchain, licence, safety classification, project model, generator, or external AI route.

AUTOSAR Classic Platform, Adaptive Platform, and Foundation are separate but related standards. A project must record the exact AUTOSAR release, platform scope, schema, vendor extensions, tool versions, compatibility constraints, commercial-use rights, and project baseline. “Latest” is not automatically compatible with the customer toolchain or released vehicle baseline.

Classic and Adaptive are architecture/platform choices, not automatic ASIL or consequence classifications. Classic addresses deeply embedded systems with hard real-time and safety constraints through application, RTE, and BSW layers. Adaptive addresses high-performance ECUs and supports service/API-oriented software, updates and reconfiguration. Both still require project-specific safety, security, timing, performance, availability, and certification evidence.

## Controlled Artefact Intake

ARXML is an XML representation and exchange format for AUTOSAR models. It is not an unstructured document collection and must not be ingested as arbitrary text chunks.

Use this sequence:

1. identify the source file, exact release/schema, project baseline, variant, supplier, classification, hash and authorisation;
2. parse with a namespace-aware XML parser with external entities and network resolution disabled;
3. validate every fragment against the exact approved AUTOSAR XML schema;
4. resolve references, paths, UUIDs, multiplicities, package ownership, duplicates and cross-file dependencies;
5. apply AUTOSAR metamodel semantics, project constraints, vendor-tool validation and compatibility rules;
6. normalise only approved entities and relationships into a provenance-preserving graph;
7. expose only authorised graph views to RAG or AI, retaining source release, file hash, element path and baseline;
8. keep the original ARXML and authoritative model in the external product workspace and approved AUTOSAR toolchain.

DBC, FIBEX, A2L/ASAP2, traces and generated source are distinct artefact types. They require their own parser, version, provenance and validation route; they must not be treated as generic ARXML or merged merely because they describe related vehicle communication or calibration concepts.

## Traceability Mapping

AI or GraphRAG may propose candidate links, but the controlled trace graph stores explicit reviewed mappings:

```text
stakeholder/system requirement
  -> safety goal, technical safety requirement, cybersecurity goal or constraint
  -> AUTOSAR system/software requirement
  -> model element and interface
  -> ECU or execution allocation and configuration baseline
  -> generated or implemented software item
  -> static analysis, unit, integration, network, SIL/HIL or vehicle test
  -> anomaly, deviation, residual risk and release evidence
```

Every link retains link type, direction, source and target stable IDs, baseline, evidence, author, reviewer and status. Similar names or an LLM inference do not create an approved trace link.

## Information Protection

Do not classify every AUTOSAR identifier as personal data or automatically mask every engineering ID. Project classification determines whether signal names, PDU/frame IDs, service/interface names, ECU names, memory addresses, calibration labels, diagnostic identifiers, supplier extensions and topology are public, internal, confidential or strictly confidential.

For an approved external route, preserve traceability with stable opaque tokens and a separately protected local token map. Masking must not change numeric meaning, units, bit layout, timing, addressing, reference identity or variant relationships.

Cryptographic keys, private key material, seed/key algorithms, credentials, unlock material and production secrets are prohibited prompt content. They require hard blocking, secret scanning, access-controlled key management or HSM-backed processes, and incident escalation. Redaction is not an acceptable reason to expose the original secret to an AI gateway.

## Output Validation Ladder

Instructor, Pydantic or Guardrails may validate the AI response envelope. They do not validate AUTOSAR correctness. Apply the relevant deterministic ladder:

1. response schema and allowed action validation;
2. XML well-formedness and secure parser checks;
3. exact-release AUTOSAR XSD validation;
4. metamodel, reference-integrity and semantic validation;
5. project and vendor-tool consistency checks;
6. generator/build reproducibility and configuration-diff review;
7. language/compiler, MISRA or other project coding rules, SAST and unit tests where source is involved;
8. communication, timing, resource, diagnostics, safety and cybersecurity integration tests as applicable;
9. independent traceability, anomaly and change-impact review;
10. named human import, merge, release or safety decision.

An LLM must not authoritatively generate or directly import an RTE, BSW configuration, Adaptive manifest, service deployment, safety mechanism, production calibration, or security configuration. It may create a candidate change or test proposal in quarantine. Approved AUTOSAR authoring/generation tools produce controlled artefacts from an approved model baseline.

## Required Project Records

- project assurance profile and AUTOSAR applicability decision;
- exact CP/AP/FO release and schema set;
- tool/vendor/version and compatibility matrix;
- licence and permitted RAG/indexing/use record;
- artefact-type and data-classification register;
- parser/schema/metamodel validation configuration;
- explicit requirement-risk-model-test traceability rules;
- generator and tool-qualification or confidence assessment as applicable;
- AI processing envelopes and prohibited-secret rules;
- representative positive, negative, malformed, duplicate, missing-reference, cross-version and security test fixtures;
- independent reviewers, human approval authorities and rollback route.

## Primary Watch Source

Use the official AUTOSAR standards and release pages as watch inputs. At the 2026-08-21 review, the official site displayed R25-11 as the current Classic release, but each project must verify and deliberately select its compatible baseline rather than automatically adopting it. AUTOSAR materials carry intellectual-property and commercial-exploitation conditions that must be reviewed before storage, indexing or generation use.
