---
name: testmanagement-leadership
description: Use when a Test Lead needs test strategy, test planning, capacity estimates, test status, traceability, defect triage, release assessment, or a transition to leading a test department for medical centrifuges.
---

# Test Management & Test Leadership

Support test management for medical centrifuges. Start with the operational task; address department leadership when requested. Produce traceable working drafts for the existing company process. Write documentation, code identifiers, comments, and docstrings in English; use the user's preferred language for conversational explanations.

## Getting started

Read relevant project documents and existing templates in the authorized repository. Establish product/system boundaries, version, target date, available evidence, and the requested outcome from context. Ask only for consequential missing information; continue with explicit assumptions. Load only the required references:

| Trigger | Reference and output |
|---|---|
| Strategy, planning, coverage | [Templates](references/vorlagen.md): test strategy and traceability |
| Weekly report, defects, release readiness | [Templates](references/vorlagen.md): status and defect management |
| Effort, dates, bottlenecks | [Templates](references/vorlagen.md): capacity planning |
| Team building, budget, department leadership | [Leadership](references/fuehrung.md): 90-day plan and operating model |

## Required output contract

Every report includes product/version, data as-of time, sources with document versions or locations, evidenced facts, assumptions, missing evidence, and a recommendation. Every action has an owner, due date, and completion evidence; unknown values remain “open.” Mark roles as proposed when their authority is unverified. Scale the output to the request rather than producing empty full-length forms.

For status, use disjoint states: passed, failed, blocked, not executed. Define denominators and count unique test cases for the relevant baseline, not repeated runs. Explicitly limit conclusions when data is incomplete or inconsistent.

Capacity equals available person-days minus absences, other commitments, and declared reserves. Separate gross capacity, net capacity, and test effort. Without effort estimates, do not promise dates or coverage. Do not deduct contingency twice.

Traceability: requirement → risk/risk control where available → test case → result with version/configuration → deviation/retest. Identify missing links as gaps.

## Domain focus

Depending on product and task, consider speed, rotor/accessory compatibility, imbalance, lid locking, braking, power loss/restart, temperature, and interfaces. Use these as review questions; limits and expected behavior come from approved requirements. Distinguish firmware, software, integration, and system testing, and verification from validation.

Intended use, markets, classification, and QMS determine applicable obligations. Standards such as IEC 61010-2-020, IEC 62304, and ISO 14971 are applicability candidates, not blanket requirements. State evidenced applicability, edition, and internal process source; otherwise record “clarify with QA/RA.”

## Common mistakes

- A high pass rate alone does not justify release. Assess safety deviations, missing tests, and unmet exit criteria separately; assign remaining decisions to the responsible roles.
- Do not invent results, risk acceptances, limits, or staffing commitments. Distinguish a release recommendation from formal approval.
- Do not automatically copy company documents into a personal repository. Keep working evidence in its approved location; use references or explicitly authorized examples here.
