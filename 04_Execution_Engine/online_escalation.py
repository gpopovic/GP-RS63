"""Validate the narrow data capsule required before an online model escalation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from config import APPROVED_DATA_CAPSULES_DIR


REQUIRED_FIELDS = ("Capsule ID", "Purpose", "Target Provider", "Processing Region", "Allowed Data Class", "Expires On")
PERMITTED_DATA_CLASSES = {"PUBLIC", "SYNTHETIC", "ANONYMISED_AGGREGATE"}


@dataclass(frozen=True)
class ApprovedDataCapsule:
    """A validated capsule with only the content approved for a single route."""

    capsule_id: str
    purpose: str
    target_provider: str
    processing_region: str
    allowed_data_class: str
    expires_on: date
    content: str


def _metadata(text: str, field: str) -> str:
    match = re.search(rf"^- {re.escape(field)}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Data capsule is missing {field}.")
    return match.group(1).strip()


def load_approved_data_capsule(
    capsule_id: str,
    configured_path: str,
    *,
    provider: str,
    region: str,
    today: date | None = None,
) -> ApprovedDataCapsule:
    """Load a matching, unexpired capsule for exactly one approved provider route."""
    candidate = Path(configured_path).resolve()
    approved_root = APPROVED_DATA_CAPSULES_DIR.resolve()
    if candidate.parent != approved_root or candidate.suffix.lower() != ".md" or candidate.stem != capsule_id:
        raise ValueError("Data capsule path or identifier is outside the approved capsule directory.")
    if not candidate.is_file():
        raise FileNotFoundError(f"Approved data capsule not found: {candidate.name}")
    text = candidate.read_text(encoding="utf-8")
    values = {field: _metadata(text, field) for field in REQUIRED_FIELDS}
    if values["Capsule ID"] != capsule_id:
        raise ValueError("Data capsule ID does not match its configured identifier.")
    if values["Target Provider"] != provider:
        raise ValueError("Data capsule target provider does not match the approved route.")
    if values["Processing Region"] != region:
        raise ValueError("Data capsule processing region does not match the approved route.")
    if values["Allowed Data Class"] not in PERMITTED_DATA_CLASSES:
        raise ValueError("Data capsule data class is not permitted for online escalation.")
    try:
        expires_on = date.fromisoformat(values["Expires On"])
    except ValueError as error:
        raise ValueError("Data capsule Expires On must be an ISO-8601 date.") from error
    if expires_on < (today or date.today()):
        raise ValueError("Data capsule has expired.")
    content_marker = "## Sanitised Content\n"
    if content_marker not in text:
        raise ValueError("Data capsule is missing the Sanitised Content section.")
    content = text.split(content_marker, maxsplit=1)[1].strip()
    if not content:
        raise ValueError("Data capsule has no approved sanitised content.")
    return ApprovedDataCapsule(
        capsule_id=capsule_id,
        purpose=values["Purpose"],
        target_provider=provider,
        processing_region=region,
        allowed_data_class=values["Allowed Data Class"],
        expires_on=expires_on,
        content=content,
    )
