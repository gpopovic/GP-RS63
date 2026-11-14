# Model-Driven Engineering Adapter Taxonomy

Status: `CANDIDATE_NOT_ACTIVATED`

## Purpose

Provide a reusable comparison frame for structured engineering standards without claiming that standards from different sectors are equivalent. AUTOSAR is not a universal blueprint that can be replaced by another schema name. Each candidate below covers one or more distinct layers and remains subject to a project-specific applicability decision, current authoritative sources, licence rights, toolchain evidence and human approval.

## Comparison Layers

| Layer | Question | Typical evidence |
| --- | --- | --- |
| L1 lifecycle and assurance | Which lifecycle, risk classification and independent approval rules apply? | applicability record, assurance plan, authority or assessor acceptance |
| L2 architecture and component model | How are system elements, responsibilities and interfaces decomposed? | architecture model, allocation, interface contract |
| L3 runtime and platform abstraction | How are execution, partitioning, resources and hardware access controlled? | platform configuration, timing and resource evidence |
| L4 communication and interoperability | How do systems exchange messages or services? | protocol profile, compatibility and cybersecurity tests |
| L5 engineering information model and exchange | Which machine-readable artefacts describe engineering data? | exact schema/release, parser and semantic validation evidence |
| L6 implementation and toolchain | How are models transformed, compiled, configured and deployed? | qualified or confidence-assessed tools, reproducible build, controlled import |
| L7 verification, certification and operational evidence | What proves suitability for release and continued operation? | tests, independent review, anomaly closure, approval and monitoring records |

A comparison is valid only within an identified layer. Similar use of XML, components or services does not establish cross-domain equivalence.

## Candidate Mapping and Limits

| Domain | Candidate standards or initiatives | Primary layers | Important limit |
| --- | --- | --- | --- |
| Automotive | AUTOSAR Classic, Adaptive and Foundation; ARXML | L2-L6 | Platform architecture does not replace functional-safety, cybersecurity or homologation evidence. |
| Industrial automation | OPC UA information models and communication; AutomationML; IEC 61131-3, IEC 61499 and PLCopen profiles where applicable | L2-L6 | These are complementary standards, not one combined platform. Vendor runtime, safety PLC and plant constraints remain decisive. |
| Medical devices and health information | IEEE 11073 SDC/BICEPS where applicable; HL7 FHIR; DICOM | L4-L5 | FHIR is healthcare information exchange, DICOM covers imaging-related data, and SDC covers connected medical-device interoperability; none is a complete medical-device software architecture or assurance lifecycle. |
| Aerospace and defence avionics | FACE; ARINC 653; project-selected ARINC interfaces | L2-L6 | FACE scope and conformance are not universal to civil aviation or space. ARINC 653 covers partitioned operating environments, not the complete aircraft assurance case. |
| Rail control-command and signalling | EULYNX architecture/interfaces; current EULYNX Data Preparation where maintained; OCORA or RaSTA only when applicable | L2-L5 | EULYNX is signalling-focused and infrastructure-manager applicability matters. Its former DataPrep model is explicitly no longer maintained, so release status must be checked. |
| Marine | IEC 61162 family where applicable; IHO S-100 product specifications; NMEA interfaces; OpenBridge | L4-L5 and HMI guidance | S-100 is a hydrographic data framework and OpenBridge is an evolving HMI design system without a formal approval process; neither is a ship-control platform. Flag, class, ship type and operational profile govern applicability. |
| Built environment | IFC, IDS, BCF and bSDD; KNX or BACnet only for relevant building automation | L4-L5 | BIM is an information-management method. IFC models built assets, IDS states information requirements and BCF exchanges issues; they do not replace design responsibility, structural verification, permits or construction acceptance. |

## Controlled Adapter Contract

Every activated domain adapter shall define:

1. intended use, project boundary, jurisdiction, market and accountable human authorities;
2. exact standard, edition, schema, maturity, supersession and licence/indexing rights;
3. supported artefact types, secure parsers and prohibited generic parsing shortcuts;
4. syntactic, referential, semantic, project and toolchain validation ladders;
5. stable IDs, provenance, configuration baselines and reviewed graph mappings;
6. information classification, secret hard blocks and meaning-preserving tokenisation rules;
7. AI action limits, quarantine, write permissions, rollback and independent review;
8. safety, security, timing, performance, human-factors and operational evidence appropriate to the domain;
9. tool qualification or tool-confidence expectations and representative positive/negative fixtures;
10. activation, release, certification and post-release monitoring gates.

## Safe Processing Sequence

```text
authorised source or live endpoint
  -> exact-version secure parser or protocol client
  -> schema, reference and semantic validation
  -> immutable provenance and approved graph view
  -> access-controlled retrieval inside the project boundary
  -> minimise or tokenise only for an explicitly approved external route
  -> model inference in a bounded action envelope
  -> response-schema validation
  -> deterministic domain and toolchain validation
  -> independent review and named human decision
  -> controlled import, release and audit evidence
```

PII detection is only one control. Proprietary engineering identifiers require classification and semantic-preserving handling. Credentials, cryptographic material, safety bypasses and production secrets are hard-blocked rather than merely redacted. RAG retrieval must itself be authorised; sanitisation after retrieval cannot repair an unauthorised access.

## Activation Boundary

This taxonomy records candidate mappings only. It does not activate a standard, certify a tool, admit a connector, authorise a cloud route or permit AI-generated engineering output to enter a product toolchain. Activation occurs only in an external product workspace through an approved project assurance profile and applicability record.
