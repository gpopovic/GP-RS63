"""Structural test for the regulatory watch record contract."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import regulatory_watch


content = """# Regulatory Watch Record
| Field | Required value |
| --- | --- |
| Record ID | REG-2026-001 |
| Watch domain | EU data protection |
| Source URL or reference | https://example.invalid |
| Jurisdiction | EU |
| Publication date | Unknown |
| Retrieval date | 2026-08-15 |
| Reviewer | Privacy Officer |
| Classification | MONITOR |
| Affected configuration items | None |
| Affected product workspaces | None |
| Interpretation owner | General Counsel |
| Decision | ESCALATE |
| Due date | N/A |
| Verification evidence | Pending |
| Next review date | 2026-08-22 |
"""
with tempfile.TemporaryDirectory() as temporary_directory:
    folder = Path(temporary_directory)
    record = folder / "REG-2026-001.md"
    record.write_text(content, encoding="utf-8")
    with patch.object(regulatory_watch, "RECORDS_DIR", folder.resolve()):
        assert regulatory_watch.validate_watch_record(record.resolve()) == []

print("Regulatory watch record validator passed.")
