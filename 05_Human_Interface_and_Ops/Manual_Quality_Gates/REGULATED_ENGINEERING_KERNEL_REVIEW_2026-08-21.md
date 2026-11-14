# Regulated Engineering Kernel Review — 2026-08-21

## Decision

Status: `IMPLEMENTED_CONFIGURATION / NOT_ACTIVATED`

Gemini's proposed gateway-to-output pattern was accepted only as a technical subflow. The corrected Triton design places project identity, purpose, domain applicability, data classification, authorised retrieval, source validity, and routing approval before any model gateway or external boundary. It separates schema conformance from deterministic engineering verification and human approval.

## Coverage Assessment

The following assessment counts controlled capability areas, not documents or lines of code.

| # | Capability area | Status after this change | Evidence or remaining issue |
| --- | --- | --- | --- |
| 1 | Company OS versus product-workspace boundary | `VERIFIED_BASELINE` | Product Workspace Contract and validator |
| 2 | Controlled roles, identities and communication signatures | `VERIFIED_BASELINE` | Role registry and baseline tests |
| 3 | Cost-bounded LangGraph harnesses and convergence gates | `VERIFIED_BASELINE` | Adaptive harness catalog; regulated workflow added |
| 4 | Three model capability classes separated from processing route | `VERIFIED_BASELINE` | Model class policy and router |
| 5 | Time-bounded information-access decision records | `VERIFIED_BASELINE` | Information-access validator |
| 6 | ALM outage CSV fallback and reconciliation | `VERIFIED_BASELINE` | Shadow backlog protocol and validator |
| 7 | Candidate-specific software release evidence | `VERIFIED_BASELINE` | Software release evidence profile and validator |
| 8 | Configuration management and fixed local baseline | `VERIFIED_BASELINE` | Configuration index and baseline runner |
| 9 | Cross-sector assurance lifecycle and traceability spine | `CONFIGURED_NOT_ACTIVATED` | Regulated Engineering Assurance Kernel |
| 10 | Domain profile catalog for automotive, medical, aerospace, rail, marine and built environment | `CONFIGURED_NOT_ACTIVATED` | Candidate catalog; no profile is an applicability approval |
| 11 | AI processing request envelope | `CONFIGURED_NOT_ACTIVATED` | Structural validator exists; no gateway enforcement yet |
| 12 | RAG source, edition, section, licence and applicability rules | `CONFIGURED_NOT_ACTIVATED` | Policy exists; no production index or populated domain source set |
| 13 | Regulatory watch and change control | `CONFIGURED_NOT_ACTIVATED` | Register exists; operational currency requires dated review records |
| 14 | On-demand local model lifecycle | `CONFIGURED_NOT_ACTIVATED` | Ollama helper exists; local candidates are not admitted models |
| 15 | LiteLLM gateway | `MISSING_LIVE_CAPABILITY` | Not installed, pinned, isolated, integrated or approved |
| 16 | Presidio PII detection | `MISSING_LIVE_CAPABILITY` | No admitted service or representative multilingual evaluation |
| 17 | IP recognisers and controlled token vault | `MISSING_LIVE_CAPABILITY` | Project-specific identifier rules and re-identification store absent |
| 18 | Technical ABAC, SSO, scoped service identity and secrets vault | `MISSING_LIVE_CAPABILITY` | Policy records do not enforce repository, RAG or gateway access |
| 19 | Live authorised RAG/GraphRAG implementation | `MISSING_LIVE_CAPABILITY` | No operational index, poisoning controls or retrieval evaluation |
| 20 | Tamper-evident evidence store and retention enforcement | `MISSING_LIVE_CAPABILITY` | Git, Jira or a database alone is insufficient |
| 21 | Active project-specific domain profiles and current licensed source packs | `MISSING_LIVE_CAPABILITY` | Must be created per real project, market and product |
| 22 | Domain tool qualification and deterministic adapters | `MISSING_LIVE_CAPABILITY` | No common qualification route for simulation, ALM, CAD/BIM or safety tools |
| 23 | Live ALM/Git/CI/provider integration and end-to-end security test | `MISSING_LIVE_CAPABILITY` | Current validators are local structural controls |

Summary: eight capability areas are part of the verified local baseline, six are controlled designs that are not operationally activated, and nine live or project-specific capabilities remain missing. This is strong Company OS configuration coverage, but it is not yet a production regulated-engineering platform.

## Corrected Gemini Claims

- LiteLLM is a model gateway candidate, not Triton's role/process orchestrator or policy authority.
- Authorised local retrieval occurs before external-context masking; only the minimum selected context may cross an approved external boundary.
- Presidio is a PII candidate and cannot guarantee detection of intellectual property or all identifiers.
- RAG retrieves source candidates; it is not a neutral or approving reviewer.
- Pydantic, Instructor, or Guardrails can validate structure and configured rules but cannot prove factual, safety, regulatory, or engineering correctness.
- Structured output is not deterministic content. Deterministic tools and qualified human review remain separate.
- Local inference does not itself prove GDPR, IP, security, sovereignty, availability, or model capability.
- Jira, Git, and ordinary databases are not automatically revision-safe or regulator-ready.
- Sector norms cannot be swapped as labels. Exact market, jurisdiction, product classification, current edition, tailoring, independence, and authority must be approved.

## Folder and Document Decision

The existing six product-workspace boundaries remain authoritative. Regulated work uses the assurance overlay defined by the kernel, avoiding another competing top-level hierarchy. The maintained minimum records are:

1. Project Assurance Profile and Applicability Record.
2. Data Flow and AI Processing Register with one envelope per material request.
3. Requirements and acceptance baseline.
4. Risk, hazard, safety, security and privacy analyses as applicable.
5. Architecture/interface decisions and verification/validation plan.
6. Configuration baselines and change-impact records.
7. Bidirectional traceability, verification results and anomaly/deviation records.
8. Assurance Case Index, release evidence and named human approvals.
9. Operational configuration, monitoring, incidents, corrective actions and retention evidence.

## Next Controlled Trials

Do not install the entire proposed stack at once. The next safe sequence is:

1. Use the project assurance profile and processing envelope on one non-sensitive automotive-style synthetic work package.
2. Measure missing fields, review effort, latency, rework and traceability usefulness.
3. Trial LiteLLM with metadata-only logging, pinned dependencies, no customer data, no automatic fallback, and a rollback route.
4. Trial Presidio separately against held-out German, English and project-specific identifiers; record false negatives and false positives.
5. Add one real domain profile only when a named project, market, qualified domain human and lawful current sources exist.

No item in this review activates a provider, model, gateway, masking service, regulated project, certification position, construction action, or release authority.

Owner: `Chief_Engineer_and_Systems_Architect`

Independent controls: `Quality_Manager`, `Privacy_and_Data_Protection_Officer`, `Security_Assurance_Auditor`, `General_Counsel_and_Legal_Department_Lead`
