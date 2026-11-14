# Finance Operating Model

## Purpose

Give Triton reliable financial decision support without creating a single authoritative "Finance Bot", duplicating the existing finance roles, or granting an AI control over money. The model starts small: capabilities remain dormant until a real decision or control trigger needs them, and additional assurance is added only when value, exposure, jurisdiction or complexity justifies it.

## Operating Principles

- Bank, accounting and approved project-control systems remain the systems of record. Agent memory, chat, dashboards and scenario files are not ledgers.
- A deterministic router may select an engagement; it may not interpret financial law, approve a recommendation, execute a transaction or alter a source record.
- Every recommendation identifies currency, valuation or reporting date, source references, assumptions, uncertainty, owner, reviewer and invalidation triggers.
- Separate corporate and personal assets, liabilities, data and decisions. Any legitimate related-party payment, loan, compensation or distribution follows its accounting, tax, legal and approval route using the minimum necessary data.
- Finance roles prepare, challenge, reconcile and report. Only a named human acting within recorded authority may approve or execute a payment, investment, filing, contract, account change or risk acceptance.
- Deterministic calculations reduce arithmetic error but do not validate inputs, tax treatment, market data, accounting classification or commercial assumptions by themselves.

## Scalable Engagement Model

Triton uses the controlled `FINANCE_ENGAGEMENT_CATALOG.json`; it does not activate all finance roles for every question.

### Foundation stage

Use the smallest applicable combination of bookkeeping, unit economics, treasury and controller capabilities. Capital allocation, investment audit, sanctions, tax assurance and crisis analysis remain event-triggered. A small company may combine operational functions only when the decision-rights record documents a compensating independent review; no person or agent may control preparation, approval, execution and reconciliation end to end.

### Growth stage

Increase forecast depth, counterparty monitoring and capital-allocation review when evidence shows material surplus cash, multiple banks/currencies, recurring subcontracting, material receivables, financing, or increased customer and supplier concentration. Growth is an observed condition, not a revenue number hard-coded in Company OS.

### Complex or cross-border stage

Activate the relevant Legal, Tax, Privacy, Sanctions, FX and independent assurance participants when the actual transaction, entity, country, data route or reporting duty triggers them. A country label alone does not determine tax, permanent-establishment, withholding, VAT/GST, sanctions or accounting treatment.

## Engagement Cells

| Cell | Typical purpose | Lead preparation | Independent challenge | Activation principle |
| --- | --- | --- | --- | --- |
| Finance intake and routing | Classify the decision and select only the needed cells | deterministic router with catalog owner | Finance and Risk Controller checks material misrouting | invoked for a declared finance question; produces no financial conclusion |
| Liquidity, treasury and FX | Cash visibility, obligations, banking continuity, currency exposure | Banking and Treasury Manager | Finance and Risk Controller; risk auditor when material | cash, bank, funding, reserve or foreign-currency trigger |
| Forecast and project economics | Offer/project margin, cash timing and scenario range | Unit Economics and Financial Planning Analyst | Finance and Risk Controller | offer, project, forecast or material variance trigger |
| Accounting and tax readiness | Reconciliation, evidence, tax/accounting handoff | Bookkeeping and Financial Operations Manager; Tax Readiness Officer | qualified external adviser where required | close, filing, tax, accounting exception or related-party trigger |
| Capital allocation | Compare business reinvestment, resilience and permitted financial alternatives | Capital Allocation and Investment Analyst | Treasury plus Investment and Counterparty Risk Auditor | evidenced surplus or material capital commitment |
| Payment integrity and counterparty control | New/changed payment route, bank details, fraud/sanctions indicators | Bookkeeping operations and Financial Crime Officer | independent verifier and accountable payment approver | every new or changed recipient plus anomaly- and risk-triggered sampling; not every routine payment |
| Independent finance assurance | Challenge evidence, separation, limits and realised outcome | Investment and Counterparty Risk Auditor or other assigned independent reviewer | accountable human receives the finding | material exposure, exception, conflict, repeated error or assurance trigger |

## Decision Rights and Separation

`FINANCE_DECISION_RIGHTS.json` defines the preparation, challenge, approval, execution and reconciliation functions for material decision classes. Role assignment is engagement-specific. If staffing cannot provide full separation, record the conflict, reduce permissions, use a second human or qualified external reviewer, and perform a prompt post-transaction review. Compensating control is not permission for one actor to self-approve.

## Data and Calculation Contract

Financial analysis must distinguish:

- observed source facts;
- controlled accounting classifications;
- management assumptions;
- scenarios and stress conditions;
- recommendations; and
- approved decisions.

Never infer missing balances, taxes, exchange rates, customer payment dates or investment values. Report missing evidence as `NEEDS_EVIDENCE`. Market, FX, bank, tax and legal inputs carry source and as-of dates. Calculations retain precision internally but present uncertainty appropriate to the evidence.

The finance scenario runtime validates and calculates a synthetic or authorised scenario record. Its output is decision support only and cannot post a journal, change a bank account, reserve funds, send a payment, place an order or submit a filing.

For a declared corporate capital-allocation question, `capital_investment.py` may calculate source-backed NPV scenarios and compare alternatives using an explicitly approved discount or hurdle rate. It has no universal MARR, does not recommend private wealth allocations, and cannot approve, execute or terminate an investment. A realised-outcome review reports forecast variance and breached decision criteria to the accountable human; it does not automatically expand or shut down a capability.

The controlled `finance_control` package adds four narrow deterministic capabilities:

- a due-period cash schedule that counts a receivable only in its declared collection period;
- project economics that keeps gross profit, contribution, allocated-overhead result, cash result and externally supplied tax provision separate;
- explicit stress transformations whose factor, delay, owner, source and expiry remain visible; and
- a payment evidence preflight that accepts only controlled counterparty references and payment-instruction fingerprints, never raw bank details.

No module contains a default margin, tax rate, liquidity duration, reserve amount or approval threshold. Such a parameter is valid only when supplied with a controlled policy or evidence reference and its approval status. A complete payment preflight reaches only `NEEDS_HUMAN_REVIEW`; missing or expired evidence produces `NEEDS_EVIDENCE`, and an adverse finding produces `BLOCKED`. None of these states approves or executes a transaction.

## Scenario and Crisis Use

Scenario analysis is a reusable skill, not a standing role. Select only events relevant to the current decision, such as delayed receivables, customer loss, cost increase, bank unavailability, currency movement or loss of delivery capacity. The scenario owner states the causal assumption and avoids counting the same impact twice.

Base, bear and worst cases are not probabilities unless an evidence-backed probability model is separately declared. Monte Carlo, VaR or CVaR may support a suitable investment question but are not default proof of operating-liquidity safety.

## Outputs

Normal outputs are a source-linked cash range, liquidity headroom, project or portfolio margin range, reserve coverage, counterparty exposure, exceptions, decision options and the smallest next evidence request. Board reporting is a read-only view produced from these records; it is not a separate decision-making role.

## Review and Evolution

Begin with synthetic fixtures and manual source references. Admit live integrations separately through security, privacy, tool and MCP controls. Measure forecast error, evidence completeness, reconciliation breaks, decision latency, control exceptions, review effort and escaped financial errors by comparable task class. Add a role, integration, calculation or recurring review only when a supported failure mode or measured benefit justifies it.
