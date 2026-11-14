"""Synthetic end-to-end pilot for access, evidence integrity, and bounded RAG.

The module proves a local control path with synthetic data. It does not activate
production SSO, a secrets manager, customer data, or a production RAG service.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a UTC offset")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class IdentityClaims:
    assertion_id: str
    issuer: str
    subject: str
    tenant: str
    service_identity: str
    purpose: str
    scopes: tuple[str, ...]
    attributes: tuple[tuple[str, str], ...]
    expires_at_utc: str
    signature: str = ""

    def unsigned(self) -> dict[str, object]:
        payload = asdict(self)
        payload.pop("signature")
        return payload


@dataclass(frozen=True)
class AccessRule:
    resource_id: str
    action: str
    tenant: str
    purpose: str
    classification: str
    required_scope: str
    required_attributes: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class AccessDecision:
    decision_id: str
    granted: bool
    subject: str
    resource_id: str
    action: str
    reasons: tuple[str, ...]


def sign_identity(claims: IdentityClaims, signing_key: bytes) -> IdentityClaims:
    """Sign synthetic identity claims with an ephemeral caller-owned key."""
    if len(signing_key) < 32:
        raise ValueError("signing key must contain at least 32 bytes")
    signature = hmac.new(signing_key, _canonical_json(claims.unsigned()), hashlib.sha256).hexdigest()
    return IdentityClaims(**{**claims.unsigned(), "signature": signature})


def authorise(
    claims: IdentityClaims,
    rule: AccessRule,
    signing_key: bytes,
    evaluation_time_utc: str,
) -> AccessDecision:
    """Fail closed on signature, expiry, tenant, purpose, scope, or attributes."""
    reasons: list[str] = []
    expected = hmac.new(signing_key, _canonical_json(claims.unsigned()), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, claims.signature):
        reasons.append("identity_signature_invalid")
    if _timestamp(evaluation_time_utc) >= _timestamp(claims.expires_at_utc):
        reasons.append("identity_expired")
    if claims.tenant != rule.tenant:
        reasons.append("tenant_mismatch")
    if claims.purpose != rule.purpose:
        reasons.append("purpose_mismatch")
    if rule.required_scope not in claims.scopes:
        reasons.append("scope_missing")
    attributes = dict(claims.attributes)
    classification_rank = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "STRICTLY_CONFIDENTIAL": 3}
    clearance = attributes.get("clearance")
    if rule.classification not in classification_rank or clearance not in classification_rank:
        reasons.append("classification_or_clearance_invalid")
    elif classification_rank[clearance] < classification_rank[rule.classification]:
        reasons.append("clearance_insufficient")
    for key, expected_value in rule.required_attributes:
        if attributes.get(key) != expected_value:
            reasons.append(f"attribute_mismatch:{key}")
    decision_payload = {
        "assertion_id": claims.assertion_id,
        "resource_id": rule.resource_id,
        "action": rule.action,
        "evaluation_time_utc": evaluation_time_utc,
        "reasons": reasons,
    }
    return AccessDecision(
        decision_id=f"sha256:{_sha256(_canonical_json(decision_payload))}",
        granted=not reasons,
        subject=claims.subject,
        resource_id=rule.resource_id,
        action=rule.action,
        reasons=tuple(reasons),
    )


class EvidenceLedger:
    """Hash-chained metadata ledger with separate retained payload blobs."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.ledger_path = self.root / "ledger.jsonl"
        self.blob_dir = self.root / "blobs"
        self.blob_dir.mkdir(parents=True, exist_ok=True)

    def _records(self) -> list[dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        return [json.loads(line) for line in self.ledger_path.read_text(encoding="utf-8").splitlines() if line]

    def _append_record(self, body: dict[str, object]) -> dict[str, object]:
        records = self._records()
        previous_hash = str(records[-1]["record_hash"]) if records else "GENESIS"
        record = {**body, "previous_hash": previous_hash}
        record["record_hash"] = _sha256(_canonical_json(record))
        with self.ledger_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
        return record

    def append(
        self,
        decision: AccessDecision,
        event_type: str,
        payload: bytes,
        occurred_at_utc: str,
        retention_until: str,
        metadata: dict[str, str],
    ) -> dict[str, object]:
        if not decision.granted or decision.action != "evidence:write":
            raise PermissionError("granted evidence:write decision required")
        _timestamp(occurred_at_utc)
        date.fromisoformat(retention_until)
        payload_hash = _sha256(payload)
        blob_path = self.blob_dir / payload_hash
        blob_path.write_bytes(payload)
        record_identity = {
            "payload_sha256": payload_hash,
            "event_type": event_type,
            "occurred_at_utc": occurred_at_utc,
            "access_decision_id": decision.decision_id,
        }
        record_id = f"EV-{_sha256(_canonical_json(record_identity))[:24]}"
        return self._append_record({
            "record_id": record_id,
            "record_type": "EVIDENCE",
            "event_type": event_type,
            "subject": decision.subject,
            "access_decision_id": decision.decision_id,
            "occurred_at_utc": occurred_at_utc,
            "retention_until": retention_until,
            "payload_sha256": payload_hash,
            "metadata": metadata,
        })

    def purge_expired(self, decision: AccessDecision, as_of_date: str) -> tuple[str, ...]:
        if not decision.granted or decision.action != "evidence:delete":
            raise PermissionError("granted evidence:delete decision required")
        as_of = date.fromisoformat(as_of_date)
        existing_tombstones = {
            str(record["target_record_id"])
            for record in self._records()
            if record.get("record_type") == "DELETION_TOMBSTONE"
        }
        records = self._records()
        removed: list[str] = []
        removed_payloads: set[str] = set()
        for record in records:
            if record.get("record_type") != "EVIDENCE" or record["record_id"] in existing_tombstones:
                continue
            if date.fromisoformat(str(record["retention_until"])) >= as_of:
                continue
            self._append_record({
                "record_id": f"DEL-{record['record_id']}",
                "record_type": "DELETION_TOMBSTONE",
                "target_record_id": record["record_id"],
                "subject": decision.subject,
                "access_decision_id": decision.decision_id,
                "occurred_at_utc": f"{as_of_date}T00:00:00Z",
            })
            removed.append(str(record["record_id"]))
            removed_payloads.add(str(record["payload_sha256"]))
            existing_tombstones.add(str(record["record_id"]))
        live_payloads = {
            str(record["payload_sha256"])
            for record in records
            if record.get("record_type") == "EVIDENCE"
            and str(record["record_id"]) not in existing_tombstones
        }
        for payload_hash in removed_payloads - live_payloads:
            blob_path = self.blob_dir / payload_hash
            if blob_path.exists():
                blob_path.unlink()
        return tuple(removed)

    def verify(self) -> list[str]:
        errors: list[str] = []
        records = self._records()
        expected_previous = "GENESIS"
        seen_record_ids: set[str] = set()
        tombstones = {
            str(record["target_record_id"])
            for record in records
            if record.get("record_type") == "DELETION_TOMBSTONE"
        }
        for index, record in enumerate(records):
            record_id = str(record.get("record_id", ""))
            if not record_id:
                errors.append(f"record[{index}] record ID missing")
            elif record_id in seen_record_ids:
                errors.append(f"record[{index}] duplicate record ID")
            seen_record_ids.add(record_id)
            if record.get("previous_hash") != expected_previous:
                errors.append(f"record[{index}] previous hash mismatch")
            stored_hash = str(record.get("record_hash", ""))
            body = dict(record)
            body.pop("record_hash", None)
            if _sha256(_canonical_json(body)) != stored_hash:
                errors.append(f"record[{index}] content hash mismatch")
            expected_previous = stored_hash
            if record.get("record_type") == "EVIDENCE":
                blob = self.blob_dir / str(record.get("payload_sha256", ""))
                if not blob.exists() and record.get("record_id") not in tombstones:
                    errors.append(f"record[{index}] payload missing without tombstone")
                elif blob.exists() and _sha256(blob.read_bytes()) != record.get("payload_sha256"):
                    errors.append(f"record[{index}] payload hash mismatch")
        return errors

    def backup_to(self, target: Path) -> Path:
        resolved = target.resolve()
        if resolved.exists():
            raise FileExistsError(resolved)
        shutil.copytree(self.root, resolved)
        if EvidenceLedger(resolved).verify():
            raise ValueError("backup verification failed")
        return resolved


@dataclass(frozen=True)
class RagDocument:
    source_id: str
    source_version: str
    resource_id: str
    tenant: str
    purpose: str
    classification: str
    required_scope: str
    required_attributes: tuple[tuple[str, str], ...]
    valid_from: str
    valid_until: str
    applicability: str
    content: str
    content_sha256: str

    @classmethod
    def controlled(cls, **values: object) -> "RagDocument":
        content = str(values["content"])
        return cls(**values, content_sha256=_sha256(content.encode("utf-8")))  # type: ignore[arg-type]


class BoundedRagIndex:
    def __init__(self, documents: Iterable[RagDocument]) -> None:
        self.documents = tuple(documents)

    def query(
        self,
        query: str,
        claims: IdentityClaims,
        signing_key: bytes,
        evaluation_time_utc: str,
    ) -> tuple[dict[str, object], ...]:
        query_terms = {term.casefold() for term in query.split() if term.strip()}
        results: list[dict[str, object]] = []
        evaluation_date = _timestamp(evaluation_time_utc).date()
        for document in self.documents:
            if document.applicability != "APPLICABLE":
                continue
            if not date.fromisoformat(document.valid_from) <= evaluation_date <= date.fromisoformat(document.valid_until):
                continue
            if _sha256(document.content.encode("utf-8")) != document.content_sha256:
                raise ValueError(f"source integrity failure: {document.source_id}")
            decision = authorise(
                claims,
                AccessRule(
                    document.resource_id,
                    "rag:read",
                    document.tenant,
                    document.purpose,
                    document.classification,
                    document.required_scope,
                    document.required_attributes,
                ),
                signing_key,
                evaluation_time_utc,
            )
            if not decision.granted:
                continue
            content_terms = {term.casefold().strip(".,:;()") for term in document.content.split()}
            score = len(query_terms & content_terms)
            if score == 0:
                continue
            results.append({
                "source_id": document.source_id,
                "source_version": document.source_version,
                "source_sha256": document.content_sha256,
                "classification": document.classification,
                "score": score,
                "excerpt": document.content,
                "access_decision_id": decision.decision_id,
            })
        return tuple(sorted(results, key=lambda item: (-int(item["score"]), str(item["source_id"]))))
