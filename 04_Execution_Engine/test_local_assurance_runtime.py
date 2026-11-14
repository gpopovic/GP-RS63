"""Regression tests for the operational local assurance vertical slice."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import local_assurance_runtime as runtime


def main() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "secure-runtime"
        root.mkdir(parents=True)
        fake_key = b"k" * 32
        fake_identity = runtime.LocalIdentity("test\\founder", "S-1-5-21-test", "test-token")
        with (
            patch.object(runtime, "load_or_create_signing_key", return_value=fake_key),
            patch.object(runtime, "current_os_identity", return_value=fake_identity),
            patch.object(runtime, "secure_runtime_directory", side_effect=lambda path=root: Path(path).resolve()),
        ):
            index = runtime.build_authorised_index(root=root)
            indexed = json.loads(index.read_text(encoding="utf-8"))
            assert len(indexed["documents"]) >= 3
            result = runtime.run_local_assurance(
                "access approval classification", "2030-01-01", root=root
            )
            assert result["citations"]
            assert len(result["citations"]) <= 5
            assert all(item["section"] and item["source_path"] for item in result["citations"])
            assert result["identity_sid"] == "S-1-5-21-test"
            backup = runtime.verified_backup(root=root)
            assert runtime.verify_sealed_ledger(runtime.EvidenceLedger(backup), fake_key) == []

            source = runtime._safe_repository_source(indexed["documents"][0]["source_path"])
            expected_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            assert indexed["documents"][0]["source_file_sha256"] == expected_hash
            altered_manifest = root / "altered-manifest.json"
            altered_manifest.write_text("{}\n", encoding="utf-8")
            try:
                runtime._load_verified_index(index, altered_manifest)
            except ValueError as error:
                assert "manifest changed" in str(error)
            else:
                raise AssertionError("A changed source manifest must invalidate the index")
            ledger = runtime.EvidenceLedger(root / runtime.EVIDENCE_DIR)
            original = ledger.ledger_path.read_text(encoding="utf-8")
            ledger.ledger_path.write_text(original.replace("AUTHORISED", "ALTERED", 1), encoding="utf-8")
            assert runtime.verify_sealed_ledger(ledger, fake_key)
            try:
                runtime.run_local_assurance("access approval", "2030-01-01", root=root)
            except ValueError as error:
                assert "pre-write verification" in str(error)
            else:
                raise AssertionError("Tampered evidence must be rejected before append and reseal")

            files = list(root.rglob("*"))
            assert all(fake_key not in path.read_bytes() for path in files if path.is_file())

    print("Operational local identity, authorised RAG, sealed evidence, and restore tests passed.")


if __name__ == "__main__":
    main()
