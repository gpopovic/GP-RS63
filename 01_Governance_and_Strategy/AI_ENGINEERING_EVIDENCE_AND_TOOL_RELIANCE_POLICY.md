# AI Engineering Evidence and Tool-Reliance Policy

## Purpose

Define proportionate evidence for AI-assisted engineering and determine whether the declared use is advisory, independently verified, qualification-relevant or prohibited. This policy does not claim that every AI use requires tool qualification or that retaining every prompt and output is lawful, necessary or sufficient.

The active external product workspace owns the engineering decision record and evidence. Triton_AI_Corp stores only the reusable contract, validator and sanitised learning outcomes.

## Tool-Reliance Decision

For every AI use that can affect a requirement, risk analysis, architecture, model, source code, test, verification result or release argument, record:

1. the exact intended use and affected lifecycle process;
2. whether the AI can introduce an error or fail to detect an error;
3. whether a downstream activity independently detects the error with adequate coverage;
4. whether AI use eliminates, reduces or automates an otherwise required activity;
5. consequence, assurance classification, active standard/profile and authority expectations;
6. the resulting reliance decision and accountable human owner.

Controlled decisions are:

- `NO_QUALIFICATION_ADVISORY`: no engineering artefact or assurance conclusion relies on the output;
- `NO_QUALIFICATION_INDEPENDENT_VERIFICATION`: the output is a quarantined candidate and complete independent verification remains effective;
- `QUALIFICATION_REQUIRED`: the declared use relies on the tool or removes an otherwise required error-detection activity; a domain-specific qualification plan is required before use;
- `USE_PROHIBITED`: the use cannot provide adequate assurance, violates a boundary or would permit an autonomous consequential decision.

The active domain profile maps this decision to its own standard terminology. ISO 26262 tool-confidence logic, DO-330 TQL, medical software validation and rail tool-assessment concepts must not be collapsed into one universal rating.

## Evidence Profiles

| Profile | Use | Minimum evidence |
| --- | --- | --- |
| `E0_ADVISORY` | brainstorming, explanation or non-authoritative drafting | request ID, purpose, source references, model/provider version reference, declared limitations and confirmation that no artefact relies on the output |
| `E1_TRACEABLE_CANDIDATE` | AI produces a quarantined candidate that is independently verified | E0 plus controlled prompt/instruction references, retrieval manifest, inference configuration, raw-output reference, transformations, deterministic verification, final diff and competent human review |
| `E2_ASSURANCE_RELIANCE` | a lifecycle or assurance activity relies on AI or an error may escape because another activity is removed or reduced | E1 plus domain-specific qualification/validation plan, tool operational requirements, qualified configuration, representative and negative tests, problem reporting, change control, authority/assessor agreement where required and approved use limitations |

`E2_ASSURANCE_RELIANCE` is not automatically approvable. If exact model behaviour, configuration control, validation evidence or authority expectations cannot be satisfied, use an independently verified E1 candidate route or prohibit the use.

## Capture Without Creating a Data Leak

Evidence records store hashes and controlled references, not unrestricted raw content. Capture categories may include:

- controlled system-prompt version;
- user-instruction version;
- retrieval manifest containing source IDs, editions, clause or element references, source hashes, query/retrieval configuration and applicability status;
- execution identity and provider request/response IDs;
- raw model-output reference before transformation;
- validator, retry and transformation event logs;
- final candidate-to-approved-artifact diff;
- human review and decision evidence.

Do not automatically duplicate licensed standards, personal data, customer IP, secrets or complete prompt bodies into a general audit store. A retrieval manifest normally records exact source identity and selected element references; verbatim chunks are retained only when lawful, necessary, classified, access-controlled and covered by retention rules.

Pseudonymisation events may record token identifiers and rule outcomes. The reversible token map remains in a separate protected vault and is never embedded in the general inference log. Credentials, cryptographic keys, safety bypasses and production secrets are hard-blocked.

## Model Identity and Reproducibility

For a locally controlled model, record the exact model artefact and weight hash, quantisation, runtime, tokenizer and relevant dependencies. For a hosted model whose weights are unavailable, record the provider, exact exposed model/version identifier, request/response ID, region and contractual retention/configuration evidence. Do not invent a weight hash.

Record exposed inference parameters, embedding model and retrieval configuration. `temperature: 0` does not prove deterministic reproduction. Hosted service updates, kernels, hardware, batching, floating-point behaviour, retrieval-index changes and unavailable seeds may alter results. State reproducibility limits explicitly and preserve the original evidence needed to review the actual decision.

## Human Review Evidence

A timestamp and reviewer ID alone do not prove meaningful review. Record:

- reviewer competence and independence required by the active profile;
- declared review scope, criteria and source baseline;
- deterministic checks and exceptions reviewed;
- candidate-to-final diff and rationale for material changes;
- anomalies, limitations and residual risk;
- signed decision for the exact artefact and configuration baseline.

Blind approval indicators, unusually short reviews, repeated unchanged approvals or missing source access trigger escalation; they do not create an automatic accusation or rejection.

## Retention and Disclosure

Retention follows product liability, regulatory, contractual, privacy, security, IP/licence, litigation-hold and project-record requirements. More data is not automatically better evidence. The project shall document why each content category is retained, where it is stored, who can access it, how integrity is protected, when it is deleted and what an auditor can lawfully inspect.

The general audit trail must remain usable if a model, provider, embedding index or tool version changes. It demonstrates the actual execution and decision; it does not promise bit-identical re-execution where the technology cannot provide it.

## Authority Correction

Authority and assessor lists are project-specific. TÜV and DEKRA are assessment organisations, FDA is a United States medical-device authority, EASA is an aviation authority, and the European Union Agency for Railways is ERA. EBA is the European Banking Authority and must not be used as the rail authority.
