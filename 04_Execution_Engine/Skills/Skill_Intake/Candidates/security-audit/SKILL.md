---
name: security-audit
description: Conduct an evidence-led, read-only security review of source code, configuration, infrastructure definitions, or change sets. Use for security-sensitive changes, pre-merge reviews, suspected vulnerabilities, secrets exposure, access control, input handling, dependency, logging, or deployment concerns.
---

# Security Audit

## Workflow

1. Establish the asset, trust boundary, data classification, change scope, and threat-relevant assumptions.
2. Inspect the smallest relevant diff and its configuration; do not change code or execute untrusted programs.
3. Check authentication, authorization, input/output handling, secrets, dependencies, logging, error paths, and deployment configuration as applicable.
4. Report only reproducible findings. State severity, affected location, evidence, likely impact, and a bounded remediation.
5. Separate confirmed defects, plausible risks, and missing evidence. Do not claim a system is secure because no issue was found.

## Output

Return findings ordered by risk, then residual risks and checks not performed. Use `Security finding`, `Evidence`, `Impact`, `Recommendation`, and `Verification` headings.

## Reference

Read [OWASP secure review guidance](references/source-notes.md) before a broad application-security review.
