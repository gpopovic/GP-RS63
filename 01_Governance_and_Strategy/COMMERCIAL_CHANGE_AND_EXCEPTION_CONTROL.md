# Commercial Change and Exception Control

## Purpose

Turn a customer change, disputed scope item, urgent exception or partial handover request into a traceable decision without inventing universal surcharges, waiving protected obligations or allowing an AI to create a commercial commitment.

## Required Record

Every material request records the existing contract or approved baseline, requester, requested outcome, observed delta, classification (`DEFECT`, `CHANGE`, `UNCLEAR` or `EMERGENCY_CONTAINMENT`), source evidence, affected deliverables, cost and schedule ranges with sources, quality and risk impact, data classification, proposed containment, approval status and reconciliation obligation.

Ambiguity remains `UNCLEAR` until examples, acceptance evidence or competent contract interpretation resolves it. A keyword scan, customer urgency or internal opinion does not decide whether work is a defect or paid change.

## Decision Rules

- An emergency may receive bounded containment while the commercial and technical decision remains open. Containment does not become release, acceptance or a permanent waiver.
- Applicable safety, legal, regulatory, privacy, security, professional and contractual obligations cannot be waived by a customer request or converted into a price term.
- Expedite capacity, price adjustment, deposit, tax handling, warranty and time-extension terms come from the applicable contract, current quote and qualified review. Triton has no universal rush-fee percentage, invoice threshold or legal entitlement.
- Partial handover identifies exact artefacts, maturity, exclusions, prohibited uses, expiry/reconciliation point and the competent approver. It never describes an incomplete package as approved for its final use.
- The output is `NEEDS_CLARIFICATION`, `READY_FOR_HUMAN_DECISION`, `CONTAINMENT_ONLY` or `BLOCKED`. Only an authorised human may commit price, scope, liability, delivery date, waiver or acceptance.

The controlled validator is `04_Execution_Engine/commercial_change_control.py`.
