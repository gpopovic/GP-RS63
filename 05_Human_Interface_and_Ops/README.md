# Human Interface and Operations

Humans retain approval authority for requirements, architecture, risk decisions, online data escalation, and releases. Record every manual sign-off in `Manual_Quality_Gates/` with artifact ID, version, review scope, decision (`approved`, `rejected`, or `approved with conditions`), rationale, name/role, and timestamp.

Recommended gates:

1. Requirements baseline before architecture starts.
2. Architecture review before implementation.
3. Quality and compliance review after automated validation.
4. A minimised, sanitised Data Capsule and provider approval before any online escalation. A Data Capsule is not a general approval for production-customer-data transfer; such a transfer requires its own documented data route.
5. Release sign-off before delivery.

An automated `FAIL` is never silently bypassed. A human decision is required after three executor attempts or an unresolved material agent conflict.
