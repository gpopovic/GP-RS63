"""Project economics with deliberately separated profit, contribution, cash and tax views."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .common import FinanceControlContext, money, require_currency, require_reference, serialise_decimal, validate_context


@dataclass(frozen=True)
class ProjectEconomicsInput:
    context: FinanceControlContext
    project_reference: str
    currency: str
    recognised_revenue: object
    direct_delivery_cost: object
    variable_commercial_cost: object
    allocated_overhead: object
    cash_receipts: object
    cash_payments: object
    tax_provision: object
    tax_basis_reference: str


def _ratio(numerator: Decimal, denominator: Decimal) -> str | None:
    if denominator == 0:
        return None
    return format((numerator / denominator * Decimal("100")).quantize(Decimal("0.01")), "f")


def calculate_project_economics(inputs: ProjectEconomicsInput) -> dict[str, object]:
    """Calculate declared metrics without deriving a tax rate or margin policy."""
    validate_context(inputs.context)
    require_reference(inputs.project_reference, "project_reference")
    require_currency(inputs.currency)
    require_reference(inputs.tax_basis_reference, "tax_basis_reference")
    revenue = money(inputs.recognised_revenue, "recognised_revenue")
    direct = money(inputs.direct_delivery_cost, "direct_delivery_cost")
    variable = money(inputs.variable_commercial_cost, "variable_commercial_cost")
    overhead = money(inputs.allocated_overhead, "allocated_overhead")
    receipts = money(inputs.cash_receipts, "cash_receipts")
    payments = money(inputs.cash_payments, "cash_payments")
    tax = money(inputs.tax_provision, "tax_provision")

    gross_profit = revenue - direct
    contribution = gross_profit - variable
    operating_result = contribution - overhead
    cash_before_tax = receipts - payments
    cash_after_declared_tax = cash_before_tax - tax
    return {
        "record_id": inputs.context.record_id,
        "as_of_date": inputs.context.as_of_date,
        "input_status": inputs.context.input_status,
        "project_reference": inputs.project_reference,
        "currency": inputs.currency,
        "gross_profit": serialise_decimal(gross_profit),
        "gross_margin_percent": _ratio(gross_profit, revenue),
        "contribution": serialise_decimal(contribution),
        "contribution_margin_percent": _ratio(contribution, revenue),
        "operating_result_after_allocated_overhead": serialise_decimal(operating_result),
        "cash_surplus_before_declared_tax": serialise_decimal(cash_before_tax),
        "declared_tax_provision": serialise_decimal(tax),
        "cash_surplus_after_declared_tax": serialise_decimal(cash_after_declared_tax),
        "tax_basis_reference": inputs.tax_basis_reference,
        "policy_threshold_assessment": "NOT_ASSESSED",
        "decision_status": "NEEDS_HUMAN_REVIEW",
        "decision_support_only": True,
        "approval_granted": False,
    }
