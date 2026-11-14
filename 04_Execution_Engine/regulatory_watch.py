"""Validate append-only regulatory watch records without interpreting the law."""

from __future__ import annotations

import re
from pathlib import Path

from config import TRITON_ROOT


RECORDS_DIR = TRITON_ROOT / "03_Knowledge_Base_RAG" / "Regulatory_Watch_Records"
REQUIRED_FIELDS = (
    "Record ID", "Watch domain", "Source URL or reference", "Jurisdiction", "Publication date",
    "Retrieval date", "Reviewer", "Classification", "Affected configuration items",
    "Affected product workspaces", "Interpretation owner", "Decision", "Due date",
    "Verification evidence", "Next review date",
)
ALLOWED_CLASSIFICATIONS = {"NO_CHANGE", "MONITOR", "ASSESS", "ACTION_REQUIRED"}


def validate_watch_record(path: Path) -> list[str]:
    """Return structural errors; source interpretation remains a human/legal responsibility."""
    if path.parent != RECORDS_DIR.resolve() or path.suffix.lower() != ".md":
        return ["record must be a Markdown file in Regulatory_Watch_Records"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    values: dict[str, str] = {}
    for field in REQUIRED_FIELDS:
        match = re.search(rf"\| {re.escape(field)} \|\s*(.*?)\s*\|", text)
        if not match or not match.group(1) or match.group(1).startswith("`"):
            errors.append(f"missing {field}")
        else:
            values[field] = match.group(1)
    if values.get("Classification") not in ALLOWED_CLASSIFICATIONS:
        errors.append("invalid Classification")
    for field in ("Retrieval date", "Next review date"):
        value = values.get(field, "")
        if value and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            errors.append(f"invalid {field}")
    return errors
