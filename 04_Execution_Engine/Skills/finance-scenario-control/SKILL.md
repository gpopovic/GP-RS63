---
name: finance-scenario-control
description: Route a Triton finance question to the smallest applicable finance cell and validate source-linked base, bear, and worst cash scenarios. Use for liquidity, project economics, reserve, payment-control, capital-allocation, tax-readiness, or counterparty decision support; never for executing or approving a transaction.
---

# Finance Scenario Control

## Use

1. Define the decision question, reporting currency, as-of date, authorised source references and accountable human decision owner.
2. Route only the declared trigger flags through `04_Execution_Engine/finance_scenario.py`; do not activate every finance role.
3. For cash analysis, populate the controlled example contract under `05_Human_Interface_and_Ops/Finance_Control/` with synthetic or authorised aggregate inputs.
4. Validate before calculating. Preserve observed facts, management assumptions, scenario stresses and decisions as separate fields.
5. Return the cash range, liquidity-headroom range, first indicated breach, evidence gaps and roles needed. Label the result as decision support, not approval.

## Guardrails

- Bank and accounting systems remain authoritative. Never create a shadow ledger from chat or scenario output.
- Never infer a balance, exchange rate, tax amount, payment date, market value or legal/accounting treatment.
- Base, bear and worst are scenarios, not probabilities. Do not add Monte Carlo, VaR or CVaR unless the declared decision and evidence justify them.
- A minimum-liquidity value or reserve is a controlled input with source and approval status, not a universal Triton threshold.
- Never expose private wealth to corporate analysis beyond the minimum approved related-party record.
- Never approve or execute payments, investments, filings, journal entries, recipient changes or bank-account changes.

## Controlled References

- `01_Governance_and_Strategy/FINANCE_OPERATING_MODEL.md`
- `01_Governance_and_Strategy/FINANCE_ENGAGEMENT_CATALOG.json`
- `01_Governance_and_Strategy/FINANCE_DECISION_RIGHTS.json`
- `05_Human_Interface_and_Ops/Finance_Control/FINANCE_SCENARIO_RECORD.example.json`
