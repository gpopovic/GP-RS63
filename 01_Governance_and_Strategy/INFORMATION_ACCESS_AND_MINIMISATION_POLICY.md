# Information Access and Minimisation Policy

## Purpose and Scope

This policy governs non-public information when it crosses a role, tool, provider, legal entity, or product-workspace boundary. It supplements normal repository permissions; it does not turn an access-request record into technical access.

Product data remains in its external product workspace. Triton_AI_Corp stores reusable configuration and approved, minimised learning exports only.

## Classification

| Class | Typical handling |
| --- | --- |
| `PUBLIC` | Approved for public disclosure. Publication approval is separate from access. |
| `INTERNAL` | Limited to the authorised Triton or product-workspace population. |
| `CONFIDENTIAL` | Named business need, named data owner, minimum necessary scope, bounded duration. |
| `STRICTLY_CONFIDENTIAL` | Named data owner plus an independent applicable control approver, exact field scope, shortest practical duration, and recorded decision evidence. |

Role title, agent persona, seniority, founder proximity, meeting attendance, or technical administrator status never grants access by itself. Pepper and Jarvis coordinate and advise within their mandates; neither inherits access to protected information.

## Required Decision Record

Use the controlled access-request contract when non-public information crosses a boundary. The record must identify:

1. the requester and exact resource scope;
2. the purpose and processing context;
3. the minimum fields or artefacts required;
4. the data classification and named data owner;
5. the requested and expiry timestamps;
6. each human approval or denial and its decision evidence; and
7. the final status and revocation route.

The applicable independent approver depends on the risk, for example Privacy and Data Protection, Legal, Security, Finance, or the accountable customer representative. A generic executive approval is not a substitute.

## Fail-Closed Rules

- Missing, ambiguous, expired, denied, or revoked records do not authorise processing.
- `STRICTLY_CONFIDENTIAL` approval requires the named data owner and at least one distinct applicable control approver.
- Approval is limited to the declared purpose, processing context, resource scope, fields, and time window.
- A model, MCP, plugin, subprocess, export, or cross-border route requires its own approved processing context; access to the source does not imply permission to send it elsewhere.
- Logs, prompts, embeddings, caches, screenshots, and generated files inherit the source classification unless an accountable owner approves a lower classification based on documented sanitisation.
- Emergency access must be time-bounded, logged, independently reviewed after use, and revoked when the emergency ends.

## Validation and Enforcement Boundary

`04_Execution_Engine/information_access.py` validates the completeness and internal consistency of a decision record. A passing result means only that the record is structurally acceptable. Technical enforcement remains with the relevant repository, identity provider, product workspace, MCP, or service owner.

## Review

The Privacy and Data Protection Officer owns this policy. The Security Operations and Incident Response Engineer reviews technical enforcement. The Quality Manager samples records for evidence quality. Material changes require a manual quality-gate record and rollback path.
