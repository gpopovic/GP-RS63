# Corp Builder Control Board

## Purpose

The Corp Builder may draft and test improvements to Triton's Company OS, but it may not silently promote its own work. The Control Board provides independent, multi-model review before an accountable human accepts a material configuration change.

## Separation of Duties

| Lane | Roles | Intended contribution |
| --- | --- | --- |
| Builder | Founder Operating System Advisor, Role Skill Evolution Manager, Continuous Improvement Architect | Explain the problem, propose the smallest viable change, provide evidence, test plan, expected benefit, and rollback route. |
| Controller | ROLE Korrektor, Quality Manager, Model Quality Observer, Security Assurance Auditor, Privacy and Data Protection Officer, Process and Quality Auditor | Challenge assumptions, check evidence and measurement design, assess model/data/control impact, and identify stop conditions. |
| Human authority | Founder or explicitly delegated accountable leader | Accept, reject, request a trial, approve the applicable gate, and own any material risk acceptance. |

Each lane is configured with an independently selectable model route in `CORP_BUILDER_CONTROL_BOARD.json`. Using different local models improves diversity of review; it is not proof of independence or correctness. Evidence, separation of duties, deterministic checks, and human approval remain required.

## Required Change Packet

Every request contains: identifier, proposed configuration item(s), problem and trigger, current baseline, evidence, desired outcome, affected roles/processes/data, risk and privacy/security/legal impact, KPI or acceptance test, cost/latency impact, proposed change, trial plan, rollback route, and requested decision.

The board must return: a recommendation, dissent, evidence gaps, required tests, owner, review date, and one of `REJECT`, `REWORK`, `TRIAL`, or `REQUEST_HUMAN_APPROVAL`.

## Non-Negotiable Control

The board output is a decision brief, not an automatic mutation command. The runtime must not write, install, connect, publish, change credentials, alter a production model route, or contact an external provider from this process. Controlled implementation occurs only after the human decision and applicable configuration-management record.

## Invocation

Use `corp_builder_control.py` with a bounded, data-safe change packet. It calls the approved `event_triggered_corp_builder_control_board` meeting definition and preserves the independent challenge round. Use `--demo` to validate the control path without calling a model.
