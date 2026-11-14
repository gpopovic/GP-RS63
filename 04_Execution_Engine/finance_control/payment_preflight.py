"""Fail-closed payment evidence preflight with no payment or approval capability."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .common import FinanceControlContext, IBAN_PATTERN, SHA256_PATTERN, money, require_currency, require_iso_date, require_reference, validate_context

EvidenceState = str


@dataclass(frozen=True)
class PaymentPreflight:
    context: FinanceControlContext
    payment_reference: str
    recipient_reference: str
    payment_instruction_fingerprint: str
    invoice_reference: str
    amount: object
    currency: str
    counterparty_status: EvidenceState
    counterparty_evidence_reference: str
    counterparty_evidence_valid_through: str
    sanctions_status: EvidenceState
    sanctions_evidence_reference: str
    sanctions_evidence_valid_through: str
    duplicate_check_status: EvidenceState
    duplicate_check_reference: str
    prepared_by: str
    independent_verifier: str
    accountable_human_approver: str


def assess_payment_preflight(record: PaymentPreflight) -> dict[str, object]:
    """Assess evidence completeness; never declare a payment approved or executable."""
    as_of = validate_context(record.context)
    for field, value in (
        ("payment_reference", record.payment_reference),
        ("recipient_reference", record.recipient_reference),
        ("invoice_reference", record.invoice_reference),
        ("counterparty_evidence_reference", record.counterparty_evidence_reference),
        ("sanctions_evidence_reference", record.sanctions_evidence_reference),
        ("duplicate_check_reference", record.duplicate_check_reference),
        ("prepared_by", record.prepared_by),
        ("independent_verifier", record.independent_verifier),
        ("accountable_human_approver", record.accountable_human_approver),
    ):
        require_reference(value, field)
    compact_recipient = record.recipient_reference.replace(" ", "").upper()
    if IBAN_PATTERN.fullmatch(compact_recipient):
        raise ValueError("recipient_reference must not contain a raw IBAN")
    if SHA256_PATTERN.fullmatch(record.payment_instruction_fingerprint) is None:
        raise ValueError("payment_instruction_fingerprint must be a lowercase SHA-256 reference")
    require_currency(record.currency)
    money(record.amount, "amount")
    if len({record.prepared_by, record.independent_verifier, record.accountable_human_approver}) != 3:
        raise ValueError("preparer, verifier and accountable approver must be distinct")

    gaps: list[str] = []
    blocks: list[str] = []
    counterparty_expiry = require_iso_date(record.counterparty_evidence_valid_through, "counterparty_evidence_valid_through")
    sanctions_expiry = require_iso_date(record.sanctions_evidence_valid_through, "sanctions_evidence_valid_through")
    if record.counterparty_status == "BLOCKED":
        blocks.append("counterparty_blocked")
    elif record.counterparty_status != "CURRENTLY_VERIFIED" or counterparty_expiry < as_of:
        gaps.append("counterparty_evidence_missing_or_expired")
    if record.sanctions_status == "BLOCKED":
        blocks.append("sanctions_blocked")
    elif record.sanctions_status != "CURRENTLY_VERIFIED" or sanctions_expiry < as_of:
        gaps.append("sanctions_evidence_missing_or_expired")
    if record.duplicate_check_status == "DUPLICATE_FOUND":
        blocks.append("duplicate_payment_indicator")
    elif record.duplicate_check_status != "NO_DUPLICATE_FOUND":
        gaps.append("duplicate_check_missing")

    status = "BLOCKED" if blocks else "NEEDS_EVIDENCE" if gaps else "NEEDS_HUMAN_REVIEW"
    return {
        "record_id": record.context.record_id,
        "as_of_date": record.context.as_of_date,
        "input_status": record.context.input_status,
        "payment_reference": record.payment_reference,
        "recipient_reference": record.recipient_reference,
        "assessment_status": status,
        "evidence_gaps": gaps,
        "blocking_findings": blocks,
        "decision_support_only": True,
        "approval_granted": False,
        "transaction_executed": False,
    }
