# Antigravity Gemba Intake — Non-Authoritative Remediation Annex — 2026-08-29

## Status and Use

This annex supports findings F-01 through F-04 in `ANTIGRAVITY_REMEDIATION_FOLLOWUP_DECISION_BRIEF_2026-08-29.md`. It is implementation guidance, not an approved patch, release decision or instruction to modify the read-only Antigravity repository. The target observed was commit `7bcc99583f2c6a1dff97b2d41314ab6a5d014953`.

## Minimal Change Sequence

### 1. Fail before serving when validation is unavailable

Do not maintain a `PYDANTIC_AVAILABLE = False` operating path. Import failure must stop startup with a short operator-facing error and no queue write. Add a test that removes or mocks the dependency and proves the server cannot start.

### 2. Replace lexical path-prefix checks

Use resolved `pathlib.Path` containment and an allow-list. The essential pattern is:

```python
base = BASE_DIR.resolve()
target = (base / requested_name).resolve()
try:
    target.relative_to(base)
except ValueError:
    deny_request()
if target.name not in APPROVED_DASHBOARD_FILES or not target.is_file():
    deny_request()
```

Do not use `str(target).startswith(str(base))`. Test traversal, encoded traversal, a sibling directory whose name begins with `Dashboards`, symlinks and alternate separators.

### 3. Move persistence to the project boundary

Accept the queue location only from a controlled project configuration. Resolve it, verify that it is inside the authorised Ralja workspace and outside the Company OS root, and fail closed otherwise. The configuration record must identify data owner, classification, retention, backup, access and deletion route.

For a pilot, prefer a transactional local store such as SQLite over whole-file JSON replacement. Store proposal ID, type, payload, submitter identity reference, timestamp, review state and immutable event history. Never replace corrupted storage with an empty queue.

### 4. Establish request authority

Loopback is transport containment, not identity. Before pilot use, add:

- authenticated local user or admitted identity provider;
- server-generated anti-CSRF token tied to the session;
- strict `Host`, `Origin` and content-type validation;
- role checks for project observation and financial proposal creation;
- generic external error messages and detailed restricted logs;
- expiry, logout and token rotation behaviour.

A typed `submitted_by` value may remain a display label but cannot be the identity or approval evidence.

### 5. Make persistence and response atomic

Return success only after a validated transaction commits. On validation, storage or audit-log failure, return a non-success status and preserve the prior state. Do not expose raw exception details in the browser response. Use a stable full-length identifier or a collision-checked database key.

### 6. Keep observation, review and action separate

Maintain distinct states and authorities for:

```text
OBSERVED -> PROPOSAL_PENDING -> ACCEPTED or REJECTED
```

Technical observation does not approve contractual acceptance, invoice validity, payment or project completion. Photographic evidence requires an actual controlled reference and integrity metadata; a checkbox is only a claim that evidence may exist.

## Minimum Negative-Test Set

| Test | Expected result |
| --- | --- |
| Missing validation dependency | Server refuses startup; no file is created or changed |
| Empty or excessive request | `4xx`; no proposal written |
| Invalid decimal, excessive precision or unsupported currency | `4xx`; no proposal written |
| Missing/invalid CSRF token or disallowed origin | `403`; no proposal written |
| Unauthenticated or unauthorised role | `401/403`; no proposal written |
| Traversal and prefix-sibling path | `404/403`; no external file read |
| Corrupt or unavailable storage | non-success response; prior evidence retained |
| Interrupted transaction | no partial proposal; recovery check passes |
| Duplicate identifier | rejected or deterministically de-duplicated with evidence |
| Submitted invoice or site status | remains `PROPOSAL_PENDING`; no payment or acceptance side effect |

## Exit Criteria

The spike may request controlled-pilot review only when all tests pass in an isolated environment, the project data route is approved, rollback and recovery are demonstrated, and an independent reviewer confirms that the UI cannot create operational approval by itself.
