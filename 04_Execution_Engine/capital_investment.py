"""Controlled corporate capital-investment calculations and review signals."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CashFlow:
    period: int
    amount: Decimal
    source_reference: str


@dataclass(frozen=True)
class InvestmentAlternative:
    alternative_id: str
    initial_outlay: Decimal
    cash_flows: tuple[CashFlow, ...]
    evidence_references: tuple[str, ...]


@dataclass(frozen=True)
class InvestmentComparison:
    discount_rate: Decimal
    discount_rate_source: str
    net_present_values: tuple[tuple[str, Decimal], ...]
    human_decision_required: bool = True
    approval_granted: bool = False


@dataclass(frozen=True)
class RealisedOutcomeReview:
    alternative_id: str
    forecast_npv: Decimal
    realised_npv: Decimal
    variance: Decimal
    breached_declared_limit: bool
    human_review_required: bool = True
    automatic_action_taken: bool = False


def _required(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must be non-empty")
    return cleaned


def calculate_npv(alternative: InvestmentAlternative, discount_rate: Decimal) -> Decimal:
    """Calculate NPV from explicitly sourced period cash flows."""
    _required(alternative.alternative_id, "alternative_id")
    if alternative.initial_outlay < 0:
        raise ValueError("initial_outlay must be non-negative")
    if discount_rate <= Decimal("-1"):
        raise ValueError("discount_rate must be greater than -1")
    if not alternative.cash_flows:
        raise ValueError("at least one cash flow is required")
    if not alternative.evidence_references or any(not item.strip() for item in alternative.evidence_references):
        raise ValueError("alternative evidence references are required")
    periods: set[int] = set()
    result = -alternative.initial_outlay
    for flow in alternative.cash_flows:
        if flow.period <= 0 or flow.period in periods:
            raise ValueError("cash-flow periods must be unique positive integers")
        periods.add(flow.period)
        _required(flow.source_reference, "cash_flow.source_reference")
        result += flow.amount / ((Decimal("1") + discount_rate) ** flow.period)
    return result.quantize(Decimal("0.01"))


def compare_investments(
    alternatives: tuple[InvestmentAlternative, ...],
    *,
    discount_rate: Decimal,
    discount_rate_source: str,
) -> InvestmentComparison:
    if len(alternatives) < 2:
        raise ValueError("at least two alternatives are required")
    source = _required(discount_rate_source, "discount_rate_source")
    identifiers = [item.alternative_id for item in alternatives]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("alternative IDs must be unique")
    values = tuple((item.alternative_id, calculate_npv(item, discount_rate)) for item in alternatives)
    return InvestmentComparison(discount_rate, source, values)


def review_realised_outcome(
    *,
    alternative_id: str,
    forecast_npv: Decimal,
    realised_npv: Decimal,
    maximum_adverse_variance: Decimal,
) -> RealisedOutcomeReview:
    _required(alternative_id, "alternative_id")
    if maximum_adverse_variance < 0:
        raise ValueError("maximum_adverse_variance must be non-negative")
    variance = (realised_npv - forecast_npv).quantize(Decimal("0.01"))
    return RealisedOutcomeReview(
        alternative_id=alternative_id,
        forecast_npv=forecast_npv,
        realised_npv=realised_npv,
        variance=variance,
        breached_declared_limit=variance < -maximum_adverse_variance,
    )
