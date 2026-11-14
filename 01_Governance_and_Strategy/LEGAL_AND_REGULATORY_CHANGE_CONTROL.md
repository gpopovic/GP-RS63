# Legal and Regulatory Change Control

## Purpose

Keep legal, regulatory, supervisory, standards, and security-rule assumptions current without treating an unreviewed alert or AI summary as a binding interpretation.

## Scope

This control applies to every Triton role that relies on law, regulation, regulatory guidance, standards, supervisory expectations, export or sanctions rules, data-protection rules, tax or employment obligations, or security advisories. A role may use a current, approved interpretation; it must not independently invent one.

## Source and Review Rule

The authoritative watch sources, accountable watch owners, review intervals, and scope are listed in `03_Knowledge_Base_RAG/REGULATORY_WATCH_REGISTER.md`. Country-specific work is prohibited from relying on a generic EU or Germany source set: the Public Affairs and Policy Manager and General Counsel must activate and verify a country profile before a country-entry, employment, contracting, or regulated delivery decision.

## Change Workflow

1. The watch owner records the source, publication or effective date, retrieval date, jurisdiction, subject, and confidence that the source is authoritative.
2. The owner classifies the signal as `NO_MATERIAL_CHANGE`, `MINOR_SELF_IMPLEMENTED`, `INTERPRETATION_NEEDED`, `FUTURE_EFFECTIVE`, `MATERIAL_CHANGE`, or `URGENT_INCIDENT`.
3. For any classification other than `NO_MATERIAL_CHANGE`, the owner identifies affected customers, products, roles, contracts, data flows, controls, policies, and evidence.
4. Record every classification and outcome in the append-only `REGULATORY_CHANGE_LOG.csv`; link supporting evidence rather than copying restricted legal text into the log.
5. General Counsel coordinates legal interpretation; the accountable domain owner proposes implementation; Privacy, Security, Quality, Finance, and Public Affairs join where their boundary is affected.
6. Material changes create a versioned configuration-change record, due date, verification method, and rollback or contingency route. Urgent incident handling starts immediately under the relevant incident procedure.
7. The Process and Quality Auditor samples the register and change records quarterly for completeness, timeliness, and evidence quality.

## Minor Self-Implementation

The accountable watch owner may implement and baseline a `MINOR_SELF_IMPLEMENTED` change without a cross-functional meeting only when **all** conditions hold:

- the change is limited to an internal source reference, taxonomy, explanatory wording, or already-approved control mapping;
- it does not change Triton's legal obligation, interpretation, customer promise, product behaviour, release evidence, contract, pricing, data flow, access right, security control, employment condition, tax treatment, sanctions exposure, or country-entry position;
- no shipped, in-progress, or planned customer product needs correction or rework;
- it is reversible, passes the declared local validation, and has a clear owner; and
- the CSV log records the source, rationale, affected configuration item, validation result, owner, and rollback reference.

If any condition is uncertain, classify the item at least as `INTERPRETATION_NEEDED` and do not self-implement it.

## Material Change Review

`MATERIAL_CHANGE` is mandatory when a rule change or its interpretation can affect an already delivered, in-development, or planned product; a customer commitment; a contract; personal or sensitive data; security; safety; sanctions; tax; employment; financial reporting; a country-entry plan; or a material environmental or social commitment.

The General Counsel convenes `event_triggered_regulatory_change_review`. The core group is General Counsel, the accountable domain owner, Product Owner, Configuration Manager, Quality Manager, Ethics and Responsible Business Officer, and Founder Operating System Advisor. Privacy, Security Operations, Finance, Public Affairs, Safety and Compliance, Environmental, Social, workforce, delivery, and customer roles join when their boundary is affected. The meeting records competing positions, impact options, cost and timing, owner, verification, customer communication need, and the decision requested from company leadership. The resulting leadership decision and implementation evidence are entered in the CSV log.

## Timing and Escalation

- A due or failed source review is a visible control exception, not a silent assumption that the prior interpretation remains valid.
- `URGENT_INCIDENT` and credible imminent legal, privacy, security, or sanctions exposure escalate immediately to the applicable control owner and General Counsel.
- `MATERIAL_CHANGE` requires an impact assessment within five working days unless an earlier effective date or risk requires faster action.
- A binding external commitment may not proceed when its applicable country or rule profile is unreviewed, overdue, or materially unresolved.

## Evidence and KPIs

Required evidence: source reference, review date, reviewer, conclusion, effectivity date, impact assessment, decisions, implementation proof, and re-test where applicable.

KPIs: source-review completion, overdue critical sources, time from signal to triage, time to impact assessment, material-change closure, recurrence of noncompliance, and audit sampling pass rate. Activity volume is not a substitute for relevance or legal quality.
