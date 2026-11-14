# TRITON-CHG-2026-004 — Model Classes and Benchmark Admission

## Change

Adds three benchmark-led model classes: `FLAGSHIP`, `STANDARD`, and `WORKER`. The classes replace an ambiguous capability assumption with explicit permitted work, evidence thresholds, routing constraints, and a controlled registry.

## Evidence Basis

Public screening uses current, version-specific evidence from Artificial Analysis, LMArena, and Hugging Face evaluation resources. Triton acceptance uses at least ten data-safe representative cases and records quality, deterministic checks, latency, actual cost, and critical failures. No single public leaderboard is treated as sufficient.

## Safeguards

- A class is assigned to an exact model version and provider route, never a brand name alone.
- Benchmark status does not approve data processing, a provider, or a model change.
- The lowest adequate class is selected; Worker outputs cannot make final consequential decisions.
- Sensitive or material work still requires an approved data route and human gate.
- The existing `phi4-mini:3.8b` reference is obsolete and is removed from the tracked template; the live unversioned environment must be updated only after an admitted replacement is selected.
- `gemma3:4b` and `qwen3:4b` are labelled only as local Worker candidates. Their origin is recorded separately from their local processing route; neither is an admitted replacement or a cloud data route.

## Verification

- `python 04_Execution_Engine/test_model_class_router.py` passes.
- `python 04_Execution_Engine/run_company_baseline.py` passes.

## Activation Decision

Prepared for candidate admission. No model is automatically assigned to a class, downloaded, started, or routed online. The Model Quality Observer, Privacy and Data Protection Officer, and accountable human owner approve each specific candidate route.
