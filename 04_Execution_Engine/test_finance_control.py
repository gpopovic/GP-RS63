"""Regression checks for the deterministic finance-control modules."""

from __future__ import annotations

from finance_control import (
    CashFlowItem,
    CashSchedulePolicy,
    CashStressEvent,
    FinanceControlContext,
    PaymentPreflight,
    ProjectEconomicsInput,
    apply_cash_stress_events,
    assess_payment_preflight,
    calculate_cash_schedule,
    calculate_project_economics,
)


def expect_error(action: object, text: str) -> None:
    try:
        action()  # type: ignore[operator]
    except ValueError as exc:
        assert text in str(exc)
    else:
        raise AssertionError(f"Expected ValueError containing {text!r}")


def main() -> None:
    context = FinanceControlContext(
        "SYNTHETIC-FIN-CONTROL", "2026-08-27", "INTERNAL", "SYNTHETIC",
        "Unit_Economics_and_Financial_Planning_Analyst", "Finance_and_Risk_Controller",
        ("SYNTHETIC-FINANCE-SOURCE",),
    )
    items = (
        CashFlowItem("INV-SEP", "INFLOW", "2026-09", "10000", "SYNTHETIC-INV-SEP", "OBSERVED"),
        CashFlowItem("INV-OCT", "INFLOW", "2026-10", "20000", "SYNTHETIC-INV-OCT", "OBSERVED"),
        CashFlowItem("PAY-SEP", "OUTFLOW", "2026-09", "15000", "SYNTHETIC-PAY-SEP", "OBSERVED"),
    )
    policy = CashSchedulePolicy(context, "EUR", "50000", "10000", "20000", "SYNTHETIC-LIQUIDITY-POLICY", "NOT_APPROVED")
    schedule = calculate_cash_schedule(("2026-09", "2026-10"), items, policy)
    assert schedule["scenario_results"]["base"][0]["closing_available_cash"] == "35000.00"  # type: ignore[index]
    assert schedule["scenario_results"]["base"][1]["closing_available_cash"] == "55000.00"  # type: ignore[index]
    assert schedule["policy_approval_status"] == "NOT_APPROVED"
    assert schedule["approval_granted"] is False

    stressed_items, lineage = apply_cash_stress_events(
        items,
        (CashStressEvent("CLIENT-DELAY", ("INV-SEP",), "worst", "0.5", 1, "SYNTHETIC-STRESS-001", "Unit_Economics_and_Financial_Planning_Analyst", "2026-12-31"),),
        context,
    )
    stressed = calculate_cash_schedule(("2026-09", "2026-10"), stressed_items, policy)
    assert stressed["scenario_results"]["worst"][0]["declared_inflow"] == "0.00"  # type: ignore[index]
    assert stressed["scenario_results"]["worst"][1]["declared_inflow"] == "25000.00"  # type: ignore[index]
    assert lineage[0]["amount_factor"] == "0.5"
    expect_error(
        lambda: apply_cash_stress_events(items, (CashStressEvent("OLD", ("INV-SEP",), "bear", "1", 0, "SYNTHETIC-OLD", "Unit_Economics_and_Financial_Planning_Analyst", "2026-01-01"),), context),
        "expired assumption",
    )

    economics = calculate_project_economics(ProjectEconomicsInput(
        context, "SYNTHETIC-PROJECT", "EUR", "100000", "50000", "10000", "15000", "80000", "62000", "5000",
        "SYNTHETIC-TAX-ADVISER-ESTIMATE",
    ))
    assert economics["gross_profit"] == "50000.00"
    assert economics["contribution"] == "40000.00"
    assert economics["operating_result_after_allocated_overhead"] == "25000.00"
    assert economics["cash_surplus_after_declared_tax"] == "13000.00"
    assert economics["policy_threshold_assessment"] == "NOT_ASSESSED"

    payment = PaymentPreflight(
        context, "SYNTHETIC-PAYMENT", "COUNTERPARTY-42", "a" * 64, "SYNTHETIC-INVOICE", "1200", "EUR",
        "CURRENTLY_VERIFIED", "SYNTHETIC-KYC", "2026-12-31",
        "CURRENTLY_VERIFIED", "SYNTHETIC-SANCTIONS", "2026-09-30",
        "NO_DUPLICATE_FOUND", "SYNTHETIC-DUPLICATE-CHECK",
        "Bookkeeping_and_Financial_Operations_Manager", "Financial_Crime_and_Sanctions_Compliance_Officer", "FOUNDER-HUMAN",
    )
    assessment = assess_payment_preflight(payment)
    assert assessment["assessment_status"] == "NEEDS_HUMAN_REVIEW"
    assert assessment["approval_granted"] is False
    expired = PaymentPreflight(**{**payment.__dict__, "sanctions_evidence_valid_through": "2026-01-01"})
    assert assess_payment_preflight(expired)["assessment_status"] == "NEEDS_EVIDENCE"
    blocked = PaymentPreflight(**{**payment.__dict__, "duplicate_check_status": "DUPLICATE_FOUND"})
    assert assess_payment_preflight(blocked)["assessment_status"] == "BLOCKED"
    raw_iban = PaymentPreflight(**{**payment.__dict__, "recipient_reference": "DE89370400440532013000"})
    expect_error(lambda: assess_payment_preflight(raw_iban), "raw IBAN")
    conflict = PaymentPreflight(**{**payment.__dict__, "independent_verifier": payment.prepared_by})
    expect_error(lambda: assess_payment_preflight(conflict), "must be distinct")
    raw_context = FinanceControlContext(**{**context.__dict__, "input_status": "PRODUCTION_RAW"})
    expect_error(lambda: calculate_cash_schedule(("2026-09", "2026-10"), items, CashSchedulePolicy(**{**policy.__dict__, "context": raw_context})), "SYNTHETIC or AUTHORISED_AGGREGATE")
    print("Finance-control module tests passed.")


if __name__ == "__main__":
    main()
