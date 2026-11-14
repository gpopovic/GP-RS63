"""Due-period-aware cash scheduling for declared finance scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from .common import FinanceControlContext, money, require_currency, require_period, require_reference, serialise_decimal, validate_context

Scenario = Literal["base", "bear", "worst"]
FlowDirection = Literal["INFLOW", "OUTFLOW"]
EvidenceStatus = Literal["OBSERVED", "CONTROLLED_ASSUMPTION"]
SCENARIOS: tuple[Scenario, ...] = ("base", "bear", "worst")


@dataclass(frozen=True)
class CashFlowItem:
    item_id: str
    direction: FlowDirection
    due_period: str
    amount: object
    source_reference: str
    evidence_status: EvidenceStatus
    included_scenarios: tuple[Scenario, ...] = SCENARIOS


@dataclass(frozen=True)
class CashSchedulePolicy:
    context: FinanceControlContext
    currency: str
    opening_cash: object
    protected_reserve: object
    minimum_operating_liquidity: object
    liquidity_policy_reference: str
    liquidity_policy_approval_status: Literal["NOT_APPROVED", "HUMAN_APPROVED"]


def calculate_cash_schedule(
    periods: tuple[str, ...],
    items: tuple[CashFlowItem, ...],
    policy: CashSchedulePolicy,
) -> dict[str, object]:
    """Calculate only declared due-period flows; never infer collection timing."""
    validate_context(policy.context)
    require_currency(policy.currency)
    require_reference(policy.liquidity_policy_reference, "liquidity_policy_reference")
    if policy.liquidity_policy_approval_status not in {"NOT_APPROVED", "HUMAN_APPROVED"}:
        raise ValueError("liquidity_policy_approval_status is invalid")
    if not periods:
        raise ValueError("periods must not be empty")
    for period in periods:
        require_period(period, "period")
    if list(periods) != sorted(set(periods)):
        raise ValueError("periods must be unique and ascending")

    opening = money(policy.opening_cash, "opening_cash")
    reserve = money(policy.protected_reserve, "protected_reserve")
    minimum = money(policy.minimum_operating_liquidity, "minimum_operating_liquidity")
    if reserve > opening:
        raise ValueError("protected_reserve cannot exceed opening_cash")

    item_ids: set[str] = set()
    normalised: list[tuple[CashFlowItem, Decimal]] = []
    for item in items:
        require_reference(item.item_id, "item_id")
        if item.item_id in item_ids:
            raise ValueError(f"duplicate cash-flow item_id: {item.item_id}")
        item_ids.add(item.item_id)
        if item.direction not in {"INFLOW", "OUTFLOW"}:
            raise ValueError(f"{item.item_id}.direction is invalid")
        require_period(item.due_period, f"{item.item_id}.due_period")
        if item.due_period not in periods:
            raise ValueError(f"{item.item_id}.due_period is outside the declared horizon")
        require_reference(item.source_reference, f"{item.item_id}.source_reference")
        if item.evidence_status not in {"OBSERVED", "CONTROLLED_ASSUMPTION"}:
            raise ValueError(f"{item.item_id}.evidence_status is invalid")
        if not item.included_scenarios or any(value not in SCENARIOS for value in item.included_scenarios):
            raise ValueError(f"{item.item_id}.included_scenarios is invalid")
        normalised.append((item, money(item.amount, f"{item.item_id}.amount")))

    results: dict[str, list[dict[str, str]]] = {}
    breaches: dict[str, str | None] = {}
    for scenario in SCENARIOS:
        available = opening - reserve
        rows: list[dict[str, str]] = []
        breach: str | None = None
        for period in periods:
            inflow = sum(
                (amount for item, amount in normalised if item.due_period == period and item.direction == "INFLOW" and scenario in item.included_scenarios),
                Decimal("0"),
            )
            outflow = sum(
                (amount for item, amount in normalised if item.due_period == period and item.direction == "OUTFLOW" and scenario in item.included_scenarios),
                Decimal("0"),
            )
            available += inflow - outflow
            headroom = available - minimum
            if headroom < 0 and breach is None:
                breach = period
            rows.append({
                "period": period,
                "declared_inflow": serialise_decimal(inflow),
                "declared_outflow": serialise_decimal(outflow),
                "closing_available_cash": serialise_decimal(available),
                "liquidity_headroom": serialise_decimal(headroom),
            })
        results[scenario] = rows
        breaches[scenario] = breach

    return {
        "record_id": policy.context.record_id,
        "as_of_date": policy.context.as_of_date,
        "input_status": policy.context.input_status,
        "currency": policy.currency,
        "scenario_results": results,
        "first_liquidity_breach": breaches,
        "policy_approval_status": policy.liquidity_policy_approval_status,
        "decision_status": "NEEDS_HUMAN_REVIEW",
        "decision_support_only": True,
        "approval_granted": False,
        "transaction_executed": False,
    }
