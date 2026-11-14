"""Validate a portable CSV shadow backlog before hand-off or ALM import."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = (
    "ID", "Type", "Title", "Outcome", "Owner", "Status", "Parent", "Links",
    "Acceptance_DoD", "Source", "Last_Confirmed_Date",
)
ALLOWED_TYPES = {"Epic", "Feature", "Story", "Task", "Defect", "Test", "Evidence", "Risk", "Decision"}
ALLOWED_STATUSES = {"Proposed", "Ready", "In Progress", "Blocked", "In Review", "Done", "Cancelled"}


@dataclass(frozen=True)
class ShadowBacklogValidation:
    """Validation result that can be printed or asserted without side effects."""

    row_count: int
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def validate_shadow_backlog(path: Path) -> ShadowBacklogValidation:
    """Validate the portable contract; does not modify the CSV or an ALM system."""
    errors: list[str] = []
    identifiers: set[str] = set()
    if path.suffix.lower() != ".csv" or not path.is_file():
        return ShadowBacklogValidation(0, ("Provide an existing CSV shadow backlog.",))
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != list(REQUIRED_COLUMNS):
            return ShadowBacklogValidation(0, ("CSV columns must exactly match the approved template.",))
        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            row_count += 1
            identifier = row["ID"].strip()
            if not identifier:
                errors.append(f"Row {line_number}: ID is required.")
            elif identifier in identifiers:
                errors.append(f"Row {line_number}: duplicate ID {identifier}.")
            identifiers.add(identifier)
            if row["Type"].strip() not in ALLOWED_TYPES:
                errors.append(f"Row {line_number}: Type is not approved.")
            if row["Status"].strip() not in ALLOWED_STATUSES:
                errors.append(f"Row {line_number}: Status is not approved.")
            for field in ("Title", "Outcome", "Owner", "Source", "Last_Confirmed_Date"):
                if not row[field].strip():
                    errors.append(f"Row {line_number}: {field} is required.")
            if row["Status"].strip() == "Done" and not row["Acceptance_DoD"].strip():
                errors.append(f"Row {line_number}: Done work requires Acceptance_DoD.")
    return ShadowBacklogValidation(row_count, tuple(errors))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Triton portable ALM shadow-backlog CSV.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    result = validate_shadow_backlog(args.csv_path)
    if not result.valid:
        raise SystemExit("\n".join(result.errors))
    print(f"Shadow backlog valid: {result.row_count} work items.")


if __name__ == "__main__":
    main()
