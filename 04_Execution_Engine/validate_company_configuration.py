"""Validate the configuration-management index and its declared local sources."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from config import TRITON_ROOT

INDEX_PATH = TRITON_ROOT / "01_Governance_and_Strategy" / "COMPANY_CONFIGURATION_INDEX.json"
PATH_FIELDS = {
    "source", "derived_document", "runtime", "validation", "catalog", "registry", "matrix",
    "watch_register", "cost_rate_card_template", "model_lanes", "alm_strategy", "role_matrix",
    "engagement_policy", "engagement_guidance", "template", "import_mapping", "governance",
    "runtime_rules", "assurance_pilot", "source_manifest", "operational_runtime",
    "authorised_source_manifest",
}


def main() -> None:
    """Fail when an indexed configuration item lacks an authoritative source."""
    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    identifiers: set[str] = set()
    missing: list[str] = []
    for item in payload["configuration_items"]:
        item_id = item["id"]
        if item_id in identifiers:
            raise SystemExit(f"Duplicate configuration item: {item_id}")
        identifiers.add(item_id)
        for field in PATH_FIELDS.intersection(item):
            declared_paths = (part.strip() for part in str(item[field]).split(";"))
            for declared_path in declared_paths:
                # Some legacy validation entries also document a CLI invocation.
                # Only a plain repository-relative path is a configuration dependency.
                if not declared_path or " " in declared_path:
                    continue
                if not (TRITON_ROOT / declared_path).exists():
                    missing.append(f"{item_id}.{field}: {declared_path}")
    if missing:
        raise SystemExit("Missing configuration sources: " + "; ".join(missing))
    print(f"Company configuration index valid: {len(identifiers)} configuration items.")


if __name__ == "__main__":
    main()
