# Candidate Skill Intake Register

All entries below are `trial`: they are quarantined under `Candidates/`, have no write or external-transmission permission, and must pass local evaluation before promotion to the active registry.

| Candidate | Purpose | Source basis | Evaluation cases | Current decision |
| --- | --- | --- | --- | --- |
| `security-audit` | Evidence-led read-only secure code review | OWASP Code Review Guide and Cheat Sheet | Detect seeded access-control, secret-handling, and input-validation defects; avoid unsupported findings | trial |
| `testing-specialist` | Trace requirements to deterministic tests | pytest documentation | Create positive, negative, boundary, and flaky-test cases from a representative feature | trial |
| `refactor-safely` | Plan small behavior-preserving improvements | Fowler refactoring guidance | Reject mixed feature/refactor changes; preserve a supplied test suite; explain a justified small transformation | trial |
| `data-analysis` | Reproducible analysis with quality checks | UK Government Analysis Function and ONS principles | Identify missing values, duplicate keys, invalid joins, and uncertainty in a synthetic KPI dataset | trial |
| `decision-records` | Create durable evidence-led decision records | ADR and MADR guidance | Capture alternatives, consequences, owner, and review trigger from a model-routing decision | trial |

Before promotion, each candidate needs a versioned test artifact, pass criteria, named evaluator, evaluation result, and an approved transfer into `04_Execution_Engine/Skills/Active/`.
