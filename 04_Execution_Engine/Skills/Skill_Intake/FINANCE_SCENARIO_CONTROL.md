# Skill Intake: Finance Scenario Control

- **Source:** Triton-owned implementation derived from controlled finance roles and governance policies.
- **Source version:** Repository commit candidate dated 2026-08-27; exact commit assigned when published.
- **Licence:** Internal Triton configuration; no third-party code or financial model incorporated.
- **Purpose:** Select the smallest applicable finance engagement and validate/calculate source-linked base, bear and worst cash scenarios.
- **Trigger:** A declared liquidity, forecast, project-economics, reserve, accounting/tax-readiness, capital-allocation, payment-integrity or counterparty decision question.
- **Tools:** Python standard library and repository-local JSON/Markdown configuration only.
- **Data classification:** Synthetic or explicitly authorised aggregate finance inputs. Raw bank, accounting, customer, employee, tax or private-wealth data is prohibited in Company OS.
- **External network access:** None.
- **Write access:** None during validation/calculation; result is returned to the caller. No bank, accounting, ALM or source-record mutation.
- **Owner:** Finance and Risk Controller.
- **Independent review:** Investment and Counterparty Risk Auditor for material investment/counterparty use; Quality Manager for configuration evidence.
- **Tests:** Catalog and role integrity, routing selectivity, unknown-trigger fail-closed behavior, base/bear/worst calculation, liquidity-breach detection, independence conflict, scenario-order validation, false approval and raw-production-data rejection.
- **Decision:** `trial`.
- **Sign-off:** Not approved for live financial reliance or transaction use. Promotion requires representative authorised fixtures, source-system reconciliation, security/privacy review, accounting/tax applicability review where relevant, and a named human activation decision.
