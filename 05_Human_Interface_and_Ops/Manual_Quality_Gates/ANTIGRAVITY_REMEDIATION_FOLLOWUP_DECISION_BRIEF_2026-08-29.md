# Antigravity Remediation Follow-up — Decision Brief — 2026-08-29

## BLUF

Antigravity has responded constructively to the prior audit. Commit `7bcc99583f2c6a1dff97b2d41314ab6a5d014953` changes 13 files and materially improves the Gemba intake, portability, voluntary interaction, onboarding, site guidance, insurance wording and assurance language. The commit was inspected read-only and was locally one commit ahead of Antigravity's `origin/main` at the observation time.

The result is suitable as an **isolated synthetic exploratory spike**, but the Gemba intake remains a **production blocker**. It still writes restricted Ralja and financial proposals inside the generic Company OS, has no authenticated identity or CSRF defence, succeeds with an empty proposal list when Pydantic is unavailable, uses a string-prefix path boundary, silently discards a damaged queue and has no submitted negative test suite. The static dashboards also remain demonstration material rather than live operational evidence.

This is a builder-side follow-up review, not independent release certification.

## Decision Triage

| Priority | Severity | Finding | Current status | Spike | Controlled pilot | Production | Required decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P0` | `HIGH` | Restricted project and financial proposals are written inside the Company OS | `OPEN` | Synthetic data only | Blocked | Blocked | Move the queue to an authorised external project workspace before real data use |
| `P0` | `HIGH` | Local intake lacks authenticated identity and CSRF/origin protection | `PARTIALLY_REMEDIATED` | Isolated manual use only | Blocked | Blocked | Add an admitted identity/session boundary and request-origin control |
| `P1` | `HIGH` | Missing validator dependency and damaged queue can still produce loss or misleading success | `OPEN` | Must fail visibly | Blocked | Blocked | Fail at startup; use transactional or atomic persistence and recovery evidence |
| `P1` | `MEDIUM` | Path boundary uses string-prefix comparison instead of path containment | `PARTIALLY_REMEDIATED` | Contain before reuse | Blocked | Blocked | Replace with resolved `Path.relative_to` containment and negative traversal tests |
| `P1` | `MEDIUM` | Dashboards still contain static live-looking values and a remote runtime script | `OPEN` | Demonstration label required | Blocked for decisions | Blocked | Bind every value to controlled evidence or label the entire suite demonstration-only |
| `P2` | `MEDIUM` | Security, insurance and operational documents retain unsupported positive states and universal numbers | `PARTIALLY_REMEDIATED` | Reference only | Evidence needed | Evidence needed | Remove remaining unverified `CHECK_PASSED`, zero-defect, 100-percent and fixed-time claims |
| `P2` | `MEDIUM` | Voluntary low-bandwidth and commercial rules still contain universal interaction or negotiation mechanics | `PARTIALLY_REMEDIATED` | Usable as optional heuristic | Tailor first | Tailor first | Make daily prompting, WIP=1, binary decisions, 15-minute work and proportional scope reduction contextual |
| `P3` | `LOW` | No automated tests accompanied the remediation commit | `OPEN` | Manual review possible | Blocked | Blocked | Add hermetic negative tests tied to the declared phase and failure modes |

`P0` is an action priority, not a CVSS score. `HIGH` reflects the supported consequence of unauthorised or misplaced project/financial state; no formal CVSS vector is asserted because deployment reachability and asset impact have not been established.

## Material Findings

### F-01 — Project-data boundary violation

- **Observed evidence:** `AUDIT_QUEUE_FILE` resolves beside the Company OS dashboard server and stores Ralja project observations plus restricted financial proposals.
- **Root cause:** The interface was converted from direct state mutation to proposal intake, but the storage boundary was not moved with the project capability.
- **Risk and phase:** Real project, personal or financial data would enter the wrong system of record. This blocks pilot and production use.
- **Immediate containment:** Run only with synthetic fixtures in a disposable copy; do not enter real names, invoices, photos or site status.
- **Corrective action:** Require an explicitly configured, authorised external project workspace and prevent any queue path inside the Company OS root.
- **Acceptance evidence:** Negative tests reject Corp-root, traversal and unapproved paths; a project data-flow approval identifies owner, retention, access and deletion route.
- **Owner/status:** Configuration Manager plus Ralja project owner — `OPEN`.

### F-02 — Localhost is not authentication

- **Observed evidence:** Binding was corrected to `127.0.0.1`, remote clients are rejected and remote CSS was removed from the form. No authenticated user, CSRF token, trusted `Origin`/`Host` rule or session authority is present.
- **Root cause:** Network locality is being used as the identity and request-authority boundary.
- **Risk and phase:** A local process or browser-origin attack can submit proposals under a typed name that is only a claim. Pilot and production remain blocked.
- **Immediate containment:** Explicit manual start, synthetic data only, no unattended service and no port forwarding.
- **Corrective action:** Add an admitted identity/session mechanism, CSRF defence, strict host/origin handling and role-based proposal permissions.
- **Acceptance evidence:** Negative tests for cross-origin POST, missing/invalid token, spoofed name, non-loopback request and unauthorised role.
- **Owner/status:** Security Operations Engineer — `PARTIALLY_REMEDIATED`.

### F-03 — Fail-closed and persistence are incomplete

- **Observed evidence:** If Pydantic import fails, the server writes an empty list extension and returns success. Invalid existing JSON is silently replaced with an empty queue. Persistence is a direct whole-file rewrite.
- **Root cause:** Dependency absence and storage corruption are treated as recoverable presentation conditions instead of integrity failures.
- **Risk and phase:** Proposals can be lost while the operator receives a success page. This is a high-impact integrity failure for site or finance records.
- **Immediate containment:** Preserve the queue file and stop on any dependency or parse failure.
- **Corrective action:** Fail at startup when validation is unavailable; use transactional project-owned storage, atomic commit, backup/recovery and stable full-length identifiers.
- **Acceptance evidence:** Tests prove no write and no success response on missing dependency, malformed amount, corrupt queue, interrupted write, duplicate ID and persistence failure.
- **Owner/status:** Chief Engineer and Configuration Manager — `OPEN`.

### F-04 — Path containment is improved but not proven

- **Observed evidence:** Paths are resolved, but containment is tested with `str(target).startswith(str(BASE_DIR.resolve()))`.
- **Root cause:** Lexical string prefix is used as a filesystem boundary.
- **Risk and phase:** A sibling path sharing the directory prefix can satisfy the string check. Actual exploitability depends on reachable filesystem names, so no `CRITICAL` label or CVSS value is asserted.
- **Immediate containment:** Do not serve arbitrary requested files during the spike; use an explicit allow-list.
- **Corrective action:** Use resolved path containment with `relative_to` and serve only declared dashboard filenames.
- **Acceptance evidence:** Negative tests cover `..`, encoded traversal, prefix-sibling directories, mixed separators, query strings, symlinks and non-HTML files.
- **Owner/status:** Software Architect — `PARTIALLY_REMEDIATED`.

### F-05 — Dashboard evidence remains incomplete

- **Observed evidence:** The hard-coded destination was corrected, but the builder still emits static KPI values, fixed exchange rates and live-looking readiness/compliance text and loads a remote runtime script.
- **Root cause:** Portability was fixed without separating presentation templates from controlled data.
- **Risk and phase:** Decision makers can mistake demonstration output for current operational truth.
- **Immediate containment:** Label the suite `DEMONSTRATION / NOT FOR OPERATIONAL DECISIONS`.
- **Corrective action:** Require source, as-of time, formula, population, owner, confidence, data-quality state and decision use for every value; remove unadmitted runtime dependencies.
- **Acceptance evidence:** Rendering fails closed on missing evidence fields and escapes hostile content; a negative fixture cannot display green operational state.
- **Owner/status:** Continuous Improvement Architect — `OPEN`.

### F-06 — Governance wording improved, residual overclaim remains

- **Observed evidence:** Universal onboarding times, many compliance footers, fixed site tolerances, psychological sensing and several pricing numbers were corrected. Remaining examples include hermetic scans on every commit, unverified `CHECK_PASSED` risk states, 100-percent strictness, zero-defect language, fixed high-severity response windows, daily mode prompting, WIP=1, one binary decision, a 15-minute fast lane and mandatory proportional scope adjustment.
- **Root cause:** Useful heuristics remain written as organisation-wide requirements without the necessary baseline, task class, activation condition or evidence.
- **Risk and phase:** Teams may optimise to invented numbers, suppress necessary work or report assurance not demonstrated.
- **Immediate containment:** Treat these statements as candidates or examples, not binding readiness evidence.
- **Corrective action:** Attach source, scope, owner, measurement window, applicability and exception route, or replace the number with risk-based tailoring.
- **Acceptance evidence:** Text and configuration regression tests prohibit the named universal claims unless a controlled context record supplies them.
- **Owner/status:** Quality Manager and relevant domain owners — `PARTIALLY_REMEDIATED`.

## Phase Decision

### Exploratory spike

Permitted only with synthetic data, explicit manual launch, loopback, a disposable queue, no dashboard truth claim, no approval/payment effect and an easy delete/rollback route. The objective is operator-flow learning, not security or production evidence.

### Controlled pilot

Blocked until project-owned storage, authenticated identity, CSRF/origin protection, fail-closed dependency handling, atomic persistence, path containment, data-flow approval and negative tests are present.

### Production release

Not assessed. In addition to the pilot controls, it would require an approved deployment architecture, threat model, access/retention controls, monitoring, backup/restore evidence, dependency admission, incident route, representative load/recovery tests and independent release approval.

## Recommended Next Action

Do not broaden the dashboard suite yet. Close F-01 through F-04 as one bounded intake slice, demonstrate the negative tests, and then request a controlled-pilot review. Keep the current visual form as the spike front end; replace its authority and persistence boundary before adding features.
