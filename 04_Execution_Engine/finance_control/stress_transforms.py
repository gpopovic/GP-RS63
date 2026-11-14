"""Explicit and traceable stress transformations for scheduled cash items."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal

from .cash_flow_schedule import CashFlowItem, Scenario
from .common import FinanceControlContext, money, require_iso_date, require_reference, validate_context


@dataclass(frozen=True)
class CashStressEvent:
    event_id: str
    target_item_ids: tuple[str, ...]
    scenario: Scenario
    amount_factor: object
    delay_months: int
    assumption_reference: str
    owner_role: str
    expiry_date: str


def _shift_period(period: str, months: int) -> str:
    year, month = (int(part) for part in period.split("-"))
    index = year * 12 + month - 1 + months
    return f"{index // 12:04d}-{index % 12 + 1:02d}"


def apply_cash_stress_events(
    items: tuple[CashFlowItem, ...],
    events: tuple[CashStressEvent, ...],
    context: FinanceControlContext,
) -> tuple[tuple[CashFlowItem, ...], tuple[dict[str, object], ...]]:
    """Create scenario-specific item copies from declared, unexpired assumptions."""
    as_of = validate_context(context)
    by_id = {item.item_id: item for item in items}
    if len(by_id) != len(items):
        raise ValueError("cash-flow item IDs must be unique before stress transformation")
    transformed = list(items)
    lineage: list[dict[str, object]] = []
    event_ids: set[str] = set()
    transformed_targets: set[tuple[str, Scenario]] = set()
    for event in events:
        require_reference(event.event_id, "event_id")
        if event.event_id in event_ids:
            raise ValueError(f"duplicate stress event_id: {event.event_id}")
        event_ids.add(event.event_id)
        if event.scenario not in {"base", "bear", "worst"}:
            raise ValueError(f"{event.event_id}.scenario is invalid")
        if not isinstance(event.delay_months, int) or isinstance(event.delay_months, bool) or event.delay_months < 0:
            raise ValueError(f"{event.event_id}.delay_months must be a non-negative integer")
        factor = money(event.amount_factor, f"{event.event_id}.amount_factor")
        require_reference(event.assumption_reference, f"{event.event_id}.assumption_reference")
        require_reference(event.owner_role, f"{event.event_id}.owner_role")
        expiry = require_iso_date(event.expiry_date, f"{event.event_id}.expiry_date")
        if expiry < as_of:
            raise ValueError(f"{event.event_id} uses an expired assumption")
        if not event.target_item_ids:
            raise ValueError(f"{event.event_id}.target_item_ids must not be empty")
        for target_id in event.target_item_ids:
            if target_id not in by_id:
                raise ValueError(f"{event.event_id} targets unknown item {target_id}")
            target_key = (target_id, event.scenario)
            if target_key in transformed_targets:
                raise ValueError(f"multiple stress events target {target_id} in {event.scenario}")
            transformed_targets.add(target_key)
            source = by_id[target_id]
            stressed_id = f"{target_id}__{event.event_id}__{event.scenario}"
            stressed = replace(
                source,
                item_id=stressed_id,
                due_period=_shift_period(source.due_period, event.delay_months),
                amount=money(source.amount, f"{target_id}.amount") * factor,
                source_reference=event.assumption_reference,
                evidence_status="CONTROLLED_ASSUMPTION",
                included_scenarios=(event.scenario,),
            )
            transformed.append(stressed)
            original_index = transformed.index(source)
            original_scenarios = tuple(value for value in source.included_scenarios if value != event.scenario)
            transformed[original_index] = replace(source, included_scenarios=original_scenarios)
            by_id[target_id] = transformed[original_index]
            lineage.append({
                "event_id": event.event_id,
                "source_item_id": target_id,
                "stressed_item_id": stressed_id,
                "scenario": event.scenario,
                "amount_factor": str(factor),
                "delay_months": event.delay_months,
                "assumption_reference": event.assumption_reference,
                "owner_role": event.owner_role,
                "expiry_date": event.expiry_date,
            })
    return tuple(transformed), tuple(lineage)
