"""Tests for provider-, region-, expiry-, and data-class-bound data capsules."""

from __future__ import annotations

import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch

import online_escalation


def capsule(path: Path, *, provider: str = "EU Provider", region: str = "EU/EEA", expires_on: str = "2026-12-31") -> None:
    path.write_text(
        "# Approved Data Capsule\n\n"
        "- Capsule ID: TEST-001\n"
        "- Purpose: Synthetic architecture question\n"
        f"- Target Provider: {provider}\n"
        f"- Processing Region: {region}\n"
        "- Allowed Data Class: SYNTHETIC\n"
        f"- Expires On: {expires_on}\n\n"
        "## Sanitised Content\n\nA synthetic, bounded question.\n",
        encoding="utf-8",
    )


with tempfile.TemporaryDirectory() as temporary_directory:
    root = Path(temporary_directory)
    path = root / "TEST-001.md"
    capsule(path)
    with patch.object(online_escalation, "APPROVED_DATA_CAPSULES_DIR", root):
        loaded = online_escalation.load_approved_data_capsule(
            "TEST-001", str(path), provider="EU Provider", region="EU/EEA", today=date(2026, 8, 15)
        )
        assert loaded.allowed_data_class == "SYNTHETIC"
        try:
            online_escalation.load_approved_data_capsule(
                "TEST-001", str(path), provider="Other", region="EU/EEA", today=date(2026, 8, 15)
            )
        except ValueError as error:
            assert "provider" in str(error)
        else:
            raise AssertionError("Provider mismatch must fail.")

print("Online escalation capsule tests passed.")
