"""End-to-end negative and recovery tests for the synthetic P0 assurance pilot."""

from __future__ import annotations

import json
import tempfile
from dataclasses import replace
from pathlib import Path

from p0_assurance_pilot import (
    AccessRule,
    BoundedRagIndex,
    EvidenceLedger,
    IdentityClaims,
    RagDocument,
    authorise,
    sign_identity,
)

EVALUATION_TIME = "2026-08-28T10:00:00Z"
SIGNING_KEY = b"synthetic-ephemeral-test-key-only-0001"


def identity() -> IdentityClaims:
    return sign_identity(
        IdentityClaims(
            assertion_id="SYNTHETIC-ASSERTION-001",
            issuer="SYNTHETIC-LOCAL-IDP",
            subject="svc-triton-rag-pilot",
            tenant="triton-synthetic",
            service_identity="rag-pilot",
            purpose="synthetic-assurance-test",
            scopes=("rag:read", "evidence:write", "evidence:delete"),
            attributes=(("environment", "synthetic"), ("workspace", "p0-pilot"), ("clearance", "INTERNAL")),
            expires_at_utc="2026-08-28T12:00:00Z",
        ),
        SIGNING_KEY,
    )


def rule(action: str, scope: str, resource: str = "rag://synthetic/controls") -> AccessRule:
    return AccessRule(
        resource_id=resource,
        action=action,
        tenant="triton-synthetic",
        purpose="synthetic-assurance-test",
        classification="INTERNAL",
        required_scope=scope,
        required_attributes=(("environment", "synthetic"), ("workspace", "p0-pilot")),
    )


def main() -> None:
    claims = identity()
    granted = authorise(claims, rule("rag:read", "rag:read"), SIGNING_KEY, EVALUATION_TIME)
    assert granted.granted

    assert not authorise(replace(claims, signature="0" * 64), rule("rag:read", "rag:read"), SIGNING_KEY, EVALUATION_TIME).granted
    assert "identity_expired" in authorise(claims, rule("rag:read", "rag:read"), SIGNING_KEY, "2026-08-28T12:00:00Z").reasons
    assert "tenant_mismatch" in authorise(claims, replace(rule("rag:read", "rag:read"), tenant="other"), SIGNING_KEY, EVALUATION_TIME).reasons
    assert "scope_missing" in authorise(claims, rule("admin", "admin"), SIGNING_KEY, EVALUATION_TIME).reasons
    assert "clearance_insufficient" in authorise(
        claims, replace(rule("rag:read", "rag:read"), classification="CONFIDENTIAL"), SIGNING_KEY, EVALUATION_TIME
    ).reasons

    allowed = RagDocument.controlled(
        source_id="SYNTHETIC-CONTROL-001", source_version="1.0", resource_id="rag://synthetic/controls",
        tenant="triton-synthetic", purpose="synthetic-assurance-test", classification="INTERNAL",
        required_scope="rag:read", required_attributes=(("environment", "synthetic"), ("workspace", "p0-pilot")),
        valid_from="2026-08-01", valid_until="2026-12-31", applicability="APPLICABLE",
        content="Payment preflight requires current evidence and human review.",
    )
    stale = RagDocument.controlled(
        source_id="SYNTHETIC-STALE", source_version="0.1", resource_id="rag://synthetic/controls",
        tenant="triton-synthetic", purpose="synthetic-assurance-test", classification="INTERNAL",
        required_scope="rag:read", required_attributes=(("environment", "synthetic"),),
        valid_from="2025-01-01", valid_until="2025-12-31", applicability="APPLICABLE",
        content="Payment preflight stale rule.",
    )
    restricted = RagDocument.controlled(
        source_id="SYNTHETIC-OTHER-TENANT", source_version="1.0", resource_id="rag://other/customer",
        tenant="other-tenant", purpose="synthetic-assurance-test", classification="STRICTLY_CONFIDENTIAL",
        required_scope="rag:read", required_attributes=(("environment", "synthetic"),),
        valid_from="2026-08-01", valid_until="2026-12-31", applicability="APPLICABLE",
        content="Payment preflight customer secret.",
    )
    results = BoundedRagIndex((allowed, stale, restricted)).query("payment preflight", claims, SIGNING_KEY, EVALUATION_TIME)
    assert len(results) == 1
    assert results[0]["source_id"] == "SYNTHETIC-CONTROL-001"
    assert results[0]["source_version"] == "1.0"
    assert len(str(results[0]["source_sha256"])) == 64
    assert "customer secret" not in json.dumps(results)

    poisoned = replace(allowed, content="Poisoned replacement content")
    try:
        BoundedRagIndex((poisoned,)).query("poisoned", claims, SIGNING_KEY, EVALUATION_TIME)
    except ValueError as exc:
        assert "source integrity failure" in str(exc)
    else:
        raise AssertionError("Poisoned source must fail closed")

    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        ledger = EvidenceLedger(root / "evidence")
        write_decision = authorise(claims, rule("evidence:write", "evidence:write", "evidence://synthetic/pilot"), SIGNING_KEY, EVALUATION_TIME)
        record = ledger.append(
            write_decision, "RAG_QUERY", json.dumps(results, sort_keys=True).encode("utf-8"),
            EVALUATION_TIME, "2026-08-29", {"query_id": "SYNTHETIC-QUERY-001"},
        )
        retained_record = ledger.append(
            write_decision, "RAG_QUERY_RECHECK", json.dumps(results, sort_keys=True).encode("utf-8"),
            "2026-08-28T10:02:00Z", "2026-09-30", {"query_id": "SYNTHETIC-QUERY-002"},
        )
        assert retained_record["record_id"] != record["record_id"]
        assert ledger.verify() == []
        backup = ledger.backup_to(root / "backup")
        assert EvidenceLedger(backup).verify() == []

        # Retention is enforced only after expiry and requires a separately scoped decision.
        delete_decision = authorise(claims, rule("evidence:delete", "evidence:delete", "evidence://synthetic/pilot"), SIGNING_KEY, EVALUATION_TIME)
        assert ledger.purge_expired(delete_decision, "2026-08-29") == ()
        assert ledger.purge_expired(delete_decision, "2026-08-30") == (record["record_id"],)
        assert ledger.verify() == []
        assert (ledger.blob_dir / str(retained_record["payload_sha256"])).exists()

        # A ledger mutation is detected even when the JSON remains parseable.
        lines = ledger.ledger_path.read_text(encoding="utf-8").splitlines()
        first = json.loads(lines[0])
        first["metadata"]["query_id"] = "TAMPERED"
        lines[0] = json.dumps(first, sort_keys=True)
        ledger.ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        assert any("content hash mismatch" in error for error in ledger.verify())

        # The ephemeral signing key must never be written to evidence or backup.
        for path in root.rglob("*"):
            if path.is_file():
                assert SIGNING_KEY not in path.read_bytes()

    print("Synthetic P0 access, evidence, and bounded-RAG pilot passed.")


if __name__ == "__main__":
    main()
