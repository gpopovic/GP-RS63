# Local Assurance Runtime Acceptance Evidence — 2026-08-28

## Declared Use and Outcome

The operational slice is enabled for `INTERNAL` Triton Company OS policy retrieval on the founder's single-user Windows workstation. It does not admit customer data, licensed standards, shared users, remote services, external providers, or a customer/product workspace.

Observed status: `CHECK_PASSED` for the declared local use. This closes the missing-implementation findings for that exact scope; it is not enterprise SSO, WORM storage, security certification, or customer-production approval.

## Implemented Path

1. `local_assurance_runtime.py` obtains the authenticated Windows logon SID rather than trusting a role name or environment alias.
2. A random signing key is generated outside the repository and stored only as a current-user DPAPI ciphertext.
3. The runtime directory is restricted to the current Windows principal and `SYSTEM`; ACL setup fails closed.
4. The authorised-source manifest admits only three controlled, `INTERNAL`, Triton-owned policy files and pins each exact SHA-256.
5. Index load verifies both manifest identity and current source-file identity before retrieval. Results are limited to five cited sections with source path, section, edition/hash, classification and score.
6. The ABAC decision checks signed identity, expiry, tenant, purpose, scope, runtime attribute and classification clearance before retrieval or evidence write.
7. Citation metadata is written to a separate-blob, hash-chained evidence ledger. The ledger is HMAC-sealed; existing evidence is verified before every append, preventing a later write from silently resealing prior manipulation.
8. A cross-process lock serialises key, index, evidence, seal and backup mutations. Backup is restored to a separate directory and fully reverified.

## Threat and Negative-Test Evidence

| Failure mode | Control and observed evidence |
| --- | --- |
| Environment-variable identity spoofing | Windows token SID is obtained through `whoami /user`; real run recorded the current SID. |
| Plaintext signing-key persistence | DPAPI current-user ciphertext plus secret-absence regression test. |
| Other local-account access | Runtime ACL contains only the current Windows principal and `SYSTEM`. |
| Cross-tenant, wrong-purpose, over-scope or expired assertion | Synthetic end-to-end negative tests fail closed. |
| Manifest substitution or source drift | Manifest SHA and explicitly admitted source SHA values invalidate the index. |
| Poisoned index section | Per-section SHA verification aborts retrieval. |
| Excessive context | Operational retrieval returns no more than five authorised cited sections. |
| Existing-ledger tampering | Pre-write verification rejects the append; the ledger cannot be silently resealed by a normal later operation. |
| Concurrent local writers | OS-level cross-process lock serialises mutations. |
| Broken or incomplete backup | Backup creation is followed by full chain, blob and HMAC verification. |

## Operational Observation

- Real runtime root: `C:\Users\gamma\.triton_ai\secure-runtime`
- Real source count: 3 controlled policy files, split into cited Markdown sections
- Real query: passed with five bounded citations
- Real evidence write: passed
- Real sealed-ledger verification: passed
- Real backup and restore verification: passed
- Docker Desktop engine: available, server `29.7.2`
- Containerised deterministic LangGraph smoke run: quality gate `PASS`, executor attempt `1/3`

Secrets, evidence payloads and the generated local index are not configuration items in Git and are intentionally excluded from this record.

## Limits and Activation Triggers

- Compromise of the logged-on Windows account or `SYSTEM` is outside this local control boundary; such a principal can invoke DPAPI and alter local state.
- A shared workstation, service account, remote gateway, customer data route, external model, licensed-standard corpus, or regulated-project source requires a new processing envelope, identity/storage design, source admission, representative tests and independent review before activation.
- Retention is not hard-coded. Normal queries require the caller to provide the applicable `--retention-until` date. The self-test retains its synthetic record only through the test date.
- Rebuilding the index does not admit changed sources unless their new hashes are deliberately entered into the controlled source manifest.

## Rollback

Disable callers of `local_assurance_runtime.py`, preserve any evidence still subject to retention, remove the runtime and its tests from the fixed baseline and configuration index, and revoke the local runtime state only after the retention owner authorises disposal. A future shared implementation must not reuse the workstation DPAPI key as a server secret.
