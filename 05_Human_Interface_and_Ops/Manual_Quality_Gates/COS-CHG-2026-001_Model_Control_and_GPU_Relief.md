# COS-CHG-2026-001 — Model Control, Baseline Verification, and GPU Relief

## Decision Record

| Field | Record |
| --- | --- |
| Requester | Founder direction, 2026-08-15 |
| Scope | Company OS only; no product workspace or customer data |
| Trigger | Control-board output/evidence gaps and local GPU responsiveness concern |
| Proposed effective mode | `TRITON_GPU_RELIEF_MODE=on_demand` after human activation review |
| Rollback | Set `TRITON_GPU_RELIEF_MODE=performance`; revert this change as one baseline |

## Controls Added

- Fixed baseline runner; it executes an allow-listed set of local checks rather than commands stored in configuration data.
- Local GPU relief helper; it asks the local Ollama service to release configured model allocations after a completed live command. Failure to release is non-destructive and does not change routing.
- Activation remains subject to `COMPANY_OS_ACTIVATION_GATE.md`; model IDs, data routes, ALM, and MCP admissions are not approved by this record.

## Required Human Review Before Activation

Confirm local model identifiers, evaluate each lane on synthetic cases, record latency/quality evidence, and approve or reject the operating mode. Do not use a Company OS review as approval for product data processing.
