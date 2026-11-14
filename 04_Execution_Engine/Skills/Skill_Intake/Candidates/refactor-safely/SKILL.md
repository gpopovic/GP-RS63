---
name: refactor-safely
description: Plan or perform small, behavior-preserving code improvements protected by tests. Use when resolving a verified maintainability issue, reducing duplication or coupling, improving names or module boundaries, or preparing code for a functional change without altering intended behavior.
---

# Safe Refactoring

## Workflow

1. Identify the concrete maintainability symptom and confirm it is not merely a stylistic preference.
2. State the behavior that must remain unchanged and the tests or observations that protect it.
3. Propose the smallest reversible transformation. Keep functional changes separate.
4. Apply one transformation at a time, then run the relevant checks.
5. Report structural benefit, changed files, evidence of preserved behavior, and residual debt.

## Guardrails

Treat a code smell as a hypothesis, not a verdict. Do not combine refactoring with feature work, broad formatting, dependency replacement, or unverified performance claims.

## Reference

Read [refactoring source notes](references/source-notes.md) when selecting a transformation.
