"""Focused tests for the portable ALM shadow-backlog validator."""

from __future__ import annotations

import tempfile
from pathlib import Path

from shadow_backlog import REQUIRED_COLUMNS, validate_shadow_backlog


def write_csv(path: Path, rows: list[str]) -> None:
    path.write_text(",".join(REQUIRED_COLUMNS) + "\n" + "\n".join(rows) + "\n", encoding="utf-8")


with tempfile.TemporaryDirectory() as temporary_directory:
    csv_path = Path(temporary_directory) / "backlog.csv"
    good_row = "TRI-1,Story,Title,Outcome,Product Owner,Ready,,,Acceptance,Workshop,2026-08-15"
    write_csv(csv_path, [good_row])
    assert validate_shadow_backlog(csv_path).valid

    invalid_row = "TRI-1,Story,Title,Outcome,Product Owner,Done,,,,Workshop,2026-08-15"
    write_csv(csv_path, [invalid_row, invalid_row])
    errors = validate_shadow_backlog(csv_path).errors
    assert any("duplicate ID" in error for error in errors)
    assert any("Acceptance_DoD" in error for error in errors)

print("Shadow backlog validator passed.")
