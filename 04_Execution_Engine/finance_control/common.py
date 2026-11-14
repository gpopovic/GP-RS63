"""Shared validation primitives for controlled finance calculations."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

PERIOD_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")
IBAN_PATTERN = re.compile(r"^[A-Z]{2}\d{2}[A-Z0-9]{10,30}$")
DATA_CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "STRICTLY_CONFIDENTIAL"}
INPUT_STATUSES = {"SYNTHETIC", "AUTHORISED_AGGREGATE"}


@dataclass(frozen=True)
class FinanceControlContext:
    record_id: str
    as_of_date: str
    data_classification: str
    input_status: str
    prepared_by: str
    independent_reviewer: str
    source_references: tuple[str, ...]


def validate_context(context: FinanceControlContext) -> date:
    """Enforce provenance, permitted data routes and reviewer separation."""
    require_reference(context.record_id, "context.record_id")
    as_of = require_iso_date(context.as_of_date, "context.as_of_date")
    if context.data_classification not in DATA_CLASSIFICATIONS:
        raise ValueError("context.data_classification is invalid")
    if context.input_status not in INPUT_STATUSES:
        raise ValueError("context.input_status must be SYNTHETIC or AUTHORISED_AGGREGATE")
    require_reference(context.prepared_by, "context.prepared_by")
    require_reference(context.independent_reviewer, "context.independent_reviewer")
    if context.prepared_by == context.independent_reviewer:
        raise ValueError("context preparer and independent reviewer must be distinct")
    if not context.source_references:
        raise ValueError("context.source_references must not be empty")
    for source in context.source_references:
        require_reference(source, "context.source_reference")
    return as_of


def money(value: object, field: str) -> Decimal:
    """Convert a non-negative declared amount without introducing float arithmetic."""
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a non-negative number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a non-negative number") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be a non-negative finite number")
    return result


def require_reference(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty controlled reference")


def require_period(value: str, field: str) -> None:
    if not isinstance(value, str) or PERIOD_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{field} must use YYYY-MM")


def require_iso_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an ISO date") from exc


def require_currency(value: str) -> None:
    if not isinstance(value, str) or CURRENCY_PATTERN.fullmatch(value) is None:
        raise ValueError("currency must be a three-letter uppercase code")


def serialise_decimal(value: Decimal) -> str:
    """Return an exact, JSON-safe decimal representation."""
    return format(value.quantize(Decimal("0.01")), "f")
