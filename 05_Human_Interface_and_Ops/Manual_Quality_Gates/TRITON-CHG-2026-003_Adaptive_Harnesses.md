# TRITON-CHG-2026-003 — Adaptive Harnesses and Information Flow

## Change

Adds a controlled catalog and validator for discovery, coding, architecture, built-environment, and service-operation harnesses. The catalog permits only bounded independent fan-out, then requires accountable synthesis and a gate.

## Basis

The design adapts documented patterns from AWS Working Backwards, GitLab asynchronous single-source-of-truth communication, Toyota pull/jidoka, Google DORA small-batch/WIP practices, and Google SRE error-budget control. Sources and adaptation limits are recorded in `01_Governance_and_Strategy/ADAPTIVE_HARNESS_AND_INFORMATION_FLOW.md`.

## Safeguards

- At most three parallel lanes, two model calls per lane, and one synthesis call before a gate.
- External-model use requires approved provider, data class, cap, and stop condition in the work item.
- Sensitive or material work requires the controlled route and human accountable approval.
- Triton_AI_Corp remains configuration-only; product and client work stays in separate product workspaces.

## Verification

- `python 04_Execution_Engine/test_adaptive_harness.py` passes.
- `python 04_Execution_Engine/run_company_baseline.py` passes.

## Activation Decision

Prepared for controlled trial. The Founder Operating System Advisor and Continuous Improvement Architect must record the first comparable-work trial, including first-pass acceptance, latency, rework, cost-cap consumption, and any stop event, before a broader routing change.
