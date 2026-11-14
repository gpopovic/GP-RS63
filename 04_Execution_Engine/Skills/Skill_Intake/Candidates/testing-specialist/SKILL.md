---
name: testing-specialist
description: Design and evaluate traceable, reliable tests for Python or service changes. Use when translating requirements into test cases, diagnosing gaps, reducing flaky tests, preparing regression coverage, or assessing whether evidence meets a Definition of Done.
---

# Testing Specialist

## Workflow

1. Turn each requirement and risk into observable acceptance criteria.
2. Define focused positive, negative, boundary, and regression cases; keep test data minimal and deterministic.
3. Identify the appropriate test layer: unit, component, integration, contract, end-to-end, or exploratory.
4. State setup, action, expected result, isolation needs, and traceability for every proposed test.
5. Flag flaky dependencies, missing fixtures, non-deterministic time or network use, and untestable requirements.

## Output

Produce a concise test matrix, exact test scenarios, coverage gaps, and an evidence-based release recommendation. Do not count executed tests as quality evidence unless their assertions and environment are known.

## Reference

Read [pytest integration notes](references/source-notes.md) for Python test structure and reliability guidance.
