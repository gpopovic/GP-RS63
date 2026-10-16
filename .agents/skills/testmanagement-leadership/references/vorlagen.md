# Operational Templates

Use only the sections needed for the task. Placeholders are not collected evidence. Mark outputs as drafts and give existing company templates priority.

## Common document header

- Product/system boundary, hardware/firmware/software baseline, relevant configuration:
- Purpose, reporting period, and data as-of time:
- Author, document version, and review status:
- Sources with document version/location:
- Facts / assumptions / missing information:

## Test strategy and test plan

1. Objectives, scope, and justified exclusions, including their effects.
2. Priorities from requirements, product changes, risk analysis, and defect history.
3. Test levels and methods: reviews, static checks, manual/automated testing, regression, verification/validation according to the applicable process.
4. Versioned test basis, traceability, and configuration management.
5. Test objects, environments, simulators, equipment status, test data, and reproducibility.
6. Resources, competencies, effort, dependencies, and milestones.
7. Entry, suspension, resumption, and exit criteria with verifiable evidence; identify proposed criteria as proposals.
8. Defect process, reporting cadence, review roles, and decision authority.

| Work package | Risk/priority and source | Deliverable/evidence | Effort and uncertainty | Owner | Due date | Dependency |
|---|---|---|---|---|---|---|
| open | open | open | open | open | open | open |

## Test status and decision brief

Lead with the assessment and rationale. Without agreed traffic-light criteria, label status as a reasoned assessment.

| Field | Content |
|---|---|
| Product/version, data as-of time, source | common header |
| Test scope | unique planned cases for this baseline; changes since the previous report |
| Results | passed / failed / blocked / not executed |
| Coverage | evidenced requirements and risk controls; missing or outdated evidence |
| Critical deviations | ID, impact, sourced severity, status, missing evidence |
| Plan and capacity | milestones, bottlenecks, forecast and assumptions |
| Decision | recommendation, open criteria, responsible decision role |
| Next actions | action, owner, due date, completion evidence |

Metrics require a suitable data basis:

- Total = passed + failed + blocked + not executed.
- Executed = passed + failed. A started test without an assessable result remains blocked.
- Execution rate = executed / total.
- Pass rate among executed cases = passed / executed.
- Passed as a proportion of total = passed / total.
- For a zero denominator, report “not calculable.” Result ratios do not establish requirements/risk coverage.

**Fictional example:** 100 cases: 95 passed, 1 failed, 0 blocked, and 4 not executed. Execution rate: 96/100 = 96%; pass rate among executed cases: 95/96 ≈ 99.0%; passed as a proportion of total: 95/100 = 95%. A failed lid-locking test requires investigation and evidence before a positive recommendation; the percentage does not decide release.

## Capacity and effort

| Role/person | Working days in period | Availability fraction | Absence in PD | Other commitments in PD | Reserve in PD | Net capacity for planned tests in PD |
|---|---|---|---|---|---|---|
| open | open | open | open | open | open | open |

Gross = sum(working days × availability fraction). Net = gross − absences − other commitments − reserve. Apply deductions to the same available time basis; do not count part-time availability or leave twice. Account for public holidays in the relevant location.

**Fictional example:** 3 full-time people × 10 working days = 30 PD gross; 3 PD leave, 5 PD other commitments, and 4 PD reserve leave 18 PD for planned tests. Here the reserve covers retests/unplanned work; do not deduct these activities again.

Compare net capacity with estimated effort as a range. Without estimates, achievable scope and completion remain open. Record equipment, specialist knowledge, and delivery-baseline bottlenecks separately.

## Traceability

| Requirement ID/version | Risk/control ID, if available | Test case ID/version | Test object/configuration | Result and evidence | Defect/retest | Gap, owner, due date |
|---|---|---|---|---|---|---|
| open | open | open | open | open | open | open |

## Defect management and triage

Record ID, observed and expected behavior with requirement source, reproduction steps, test object/configuration, evidence, and affected variants. Severity describes impact; priority describes treatment order. Justify both using internal definitions.

Triage records the assessment, owner, due date, next decision, and affected test scope. Closure requires the correction reference, retest, and justified regression. Escalate safety-related findings through the existing process to development/QA/risk management. Risk acceptance remains with authorized roles.
