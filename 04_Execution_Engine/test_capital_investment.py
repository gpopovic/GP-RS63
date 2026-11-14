"""Tests for controlled corporate investment calculations."""

from decimal import Decimal

from capital_investment import CashFlow, InvestmentAlternative, compare_investments, review_realised_outcome


def alternative(identifier: str, outlay: str, returns: tuple[str, ...]) -> InvestmentAlternative:
    return InvestmentAlternative(
        alternative_id=identifier,
        initial_outlay=Decimal(outlay),
        cash_flows=tuple(
            CashFlow(index, Decimal(amount), f"source://{identifier}/period/{index}")
            for index, amount in enumerate(returns, start=1)
        ),
        evidence_references=(f"source://{identifier}/estimate",),
    )


def main() -> None:
    comparison = compare_investments(
        (alternative("MAKE", "1000", ("500", "700")), alternative("BUY", "800", ("450", "500"))),
        discount_rate=Decimal("0.08"),
        discount_rate_source="approval://capital-policy/2026-08-28",
    )
    assert comparison.net_present_values == (("MAKE", Decimal("63.10")), ("BUY", Decimal("45.34")))
    assert comparison.human_decision_required is True
    assert comparison.approval_granted is False

    review = review_realised_outcome(
        alternative_id="MAKE",
        forecast_npv=Decimal("63.10"),
        realised_npv=Decimal("10.00"),
        maximum_adverse_variance=Decimal("40.00"),
    )
    assert review.breached_declared_limit is True
    assert review.automatic_action_taken is False
    print("Corporate capital-investment tests passed.")


if __name__ == "__main__":
    main()
