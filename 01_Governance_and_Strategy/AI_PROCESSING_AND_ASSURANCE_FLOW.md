# AI Processing and Assurance Flow

## Corrected Control Sequence

LiteLLM, Presidio, Guardrails, Instructor, Ollama, and vLLM are candidate implementation components, not the governance system. Triton controls the sequence:

```text
request and project identity
  -> purpose, domain, task and consequence classification
  -> human/service identity plus ABAC decision
  -> source classification and authorised local retrieval
  -> source validity, version and applicability check
  -> minimum-context selection
  -> local pseudonymisation or redaction before an external boundary
  -> approved model class, provider, region and cost route
  -> isolated inference with bounded retries
  -> schema validation
  -> deterministic domain, code, calculation and traceability checks
  -> output DLP and authorised local re-identification where needed
  -> independent review and human gate
  -> controlled write to ALM, Git, evidence store or delivery system
  -> retention, monitoring, incident and learning loop
```

## Separation of Responsibilities

| Concern | Triton control | Candidate implementation |
| --- | --- | --- |
| Process and role orchestration | LangGraph harness and controlled role prompts | LangGraph runtime |
| Model gateway | Provider abstraction, keys, rate limits, spend and technical routing | LiteLLM Proxy candidate |
| Policy decision | Project, purpose, classification, route, time window, owner and approval | Triton processing envelope plus external technical enforcement |
| PII detection | Tested entity detection and pseudonymisation | Presidio candidate with language and project-specific recognisers |
| IP and engineering identifiers | Explicit project dictionaries, patterns and source classifications | Custom recognisers and deterministic rules; not Presidio alone |
| Structured output | Typed response and bounded correction | Pydantic/Instructor candidate |
| Content risk checks | Explicitly selected, tested validators | Guardrails AI candidate where justified |
| Code and engineering verification | Reproducible deterministic tools | Linters, type checkers, SAST, tests, simulation, CAD/BIM/requirements tools |
| Local inference | On-demand laptop worker route | Ollama |
| Server inference | High-throughput controlled GPU service | vLLM candidate for a suitable server, not the current laptop baseline |

No tool is compliant, secure, sovereign, or suitable because of its name or local deployment alone. Host controls, network egress, software supply chain, telemetry, logging, access, licence, model evidence, jurisdiction, retention, incident response, and human approval remain necessary.

## Retrieval and Masking Rule

Authorised retrieval may use original identifiers inside the approved local or customer trust boundary. Before any selected context crosses an external provider boundary, minimise it and replace sensitive identifiers with stable opaque tokens. Keep the token map in a separate local controlled store. Do not mask away requirement, risk, test, configuration, or evidence relationships.

RAG is a source-selection mechanism, not a neutral reviewer. Every material RAG claim must retain source ID, edition, section, retrieval date, applicability status, and evidence reference. A missing or overdue applicability record blocks binding use.

## Validation and Logging Rule

Schema conformance proves shape, not truth. Every consequential output needs the configured deterministic and human checks. Narrative rationale may be required alongside structured data for safety cases, deviations, assumptions, and residual risk.

For non-public data, default logs contain metadata rather than prompt or response bodies. Logs, embeddings, caches, token maps, screenshots, and generated files inherit the source classification unless an approved sanitisation decision states otherwise. Jira, Git, or a database is not revision-safe by default; evidence requires controlled identity, timestamps, hashes, permissions, history, retention, and backup or tamper-evidence appropriate to risk.

When AI can affect an engineering artefact or assurance conclusion, apply `AI_ENGINEERING_EVIDENCE_AND_TOOL_RELIANCE_POLICY.md`. The project decision record uses hashes and controlled references for prompts, retrieval manifests, raw outputs, transformations, verification and final diffs. It does not override the standard prohibition on non-public content logging or place a reversible pseudonymisation map in the general audit trail.

## Activation Rule

The current architecture is a controlled design, not proof that LiteLLM, Presidio, Guardrails, Instructor, or vLLM is installed or admitted. Each candidate requires dependency review, pinned version, isolated trial, data-flow assessment, representative tests, observability policy, rollback evidence, independent review, and explicit activation approval.

## Evidence-Grounded Producer-Verifier Loop

Consequential work uses a producer-verifier loop sized to the declared consequence, uncertainty, reversibility, and available evidence. This is an assurance pattern, not a mandatory multi-agent hierarchy.

1. Record the smallest sufficient acceptance baseline before implementation. The baseline is controlled and versioned, not immutable: a justified change records who changed it, why, and the impact on completed work.
2. Select direct execution or bounded decomposition. Parallel work is used only for genuinely independent slices with explicit inputs, outputs, ownership, and an integration owner.
3. Run suitable deterministic checks as early as practical. They still consume compute, elapsed time, licences, equipment, and human attention; they are not described as zero-cost.
4. Give the verifier enough bounded evidence to test the claim: the objective, current acceptance baseline, applicable authoritative sources, changed artefact or diff, provenance, execution environment, check results, known limitations, and unresolved assumptions. The verifier may request missing evidence rather than infer it.
5. Use the most direct admitted verification method that can establish or refute the claim. No MCP, model, second agent, or named tool is mandatory merely to make a finding valid. Tool execution is required only where the acceptance baseline or risk-specific verification plan requires it.
6. Record each material finding with evidence and consequence. A reasoned architecture or operational finding may rely on direct inspection; an incompletely evidenced concern remains a labelled hypothesis. Style comments are retained only when tied to an acceptance criterion, maintainability risk, or observable user outcome.
7. Apply task-specific stop conditions and correction budgets. An exhausted budget, unavailable evidence, or unresolved material finding causes an explicit escalation or bounded partial result; it never becomes a silent pass. Fixed loop counts and telemetry thresholds are not universal company rules.

A passed check establishes only the claim covered by that check. It does not by itself establish maturity, fitness for use, regulatory acceptance, or release approval.
