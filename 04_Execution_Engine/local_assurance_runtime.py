"""Operational local assurance path for the single-user Triton workstation.

This module binds access assertions to the current operating-system identity,
keeps the signing key outside Git using Windows DPAPI, restricts local runtime
state with OS permissions, builds a hash-bound index from an authorised source
manifest, and seals the evidence ledger. It is intentionally not a multi-user
enterprise SSO implementation and never authorises customer data.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import hmac
import json
import os
import secrets
import shutil
import subprocess
from contextlib import contextmanager
from ctypes import wintypes
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from config import AUTHORISED_RAG_MANIFESTS_DIR, SECURE_RUNTIME_DIR, TRITON_ROOT
from p0_assurance_pilot import (
    AccessRule,
    BoundedRagIndex,
    EvidenceLedger,
    IdentityClaims,
    RagDocument,
    authorise,
    sign_identity,
)

DEFAULT_MANIFEST = AUTHORISED_RAG_MANIFESTS_DIR / "COMPANY_OS_LOCAL_ASSURANCE_SOURCES.json"
KEY_FILE = "identity-signing-key.dpapi"
INDEX_FILE = "authorised-rag-index.json"
EVIDENCE_DIR = "evidence"
BACKUP_DIR = "evidence-backup"
SEAL_FILE = "ledger.hmac"
LOCK_FILE = "runtime.lock"


class _DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


@dataclass(frozen=True)
class LocalIdentity:
    principal: str
    stable_id: str
    source: str


def _blob(data: bytes) -> tuple[_DataBlob, ctypes.Array[Any]]:
    buffer = ctypes.create_string_buffer(data)
    value = _DataBlob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    return value, buffer


def _protect_for_current_windows_user(data: bytes) -> bytes:
    if os.name != "nt":
        raise RuntimeError("The admitted local secret store currently requires Windows DPAPI")
    source, source_buffer = _blob(data)
    output = _DataBlob()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    description = ctypes.c_wchar_p("Triton local assurance key")
    if not crypt32.CryptProtectData(
        ctypes.byref(source), description, None, None, None, 0, ctypes.byref(output)
    ):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        kernel32.LocalFree(output.pbData)
        del source_buffer


def _unprotect_for_current_windows_user(data: bytes) -> bytes:
    if os.name != "nt":
        raise RuntimeError("The admitted local secret store currently requires Windows DPAPI")
    source, source_buffer = _blob(data)
    output = _DataBlob()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    if not crypt32.CryptUnprotectData(
        ctypes.byref(source), None, None, None, None, 0, ctypes.byref(output)
    ):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        kernel32.LocalFree(output.pbData)
        del source_buffer


def current_os_identity() -> LocalIdentity:
    """Read the authenticated OS token identity, not an environment alias."""
    if os.name != "nt":
        uid = str(os.getuid())
        return LocalIdentity(principal=f"uid:{uid}", stable_id=uid, source="posix-process-uid")
    completed = subprocess.run(
        ["whoami", "/user", "/fo", "csv", "/nh"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    row = next(csv.reader([completed.stdout.strip()]))
    if len(row) != 2 or not row[1].startswith("S-"):
        raise RuntimeError("Unable to resolve the current Windows logon token")
    return LocalIdentity(principal=row[0], stable_id=row[1], source="windows-logon-token")


def secure_runtime_directory(root: Path = SECURE_RUNTIME_DIR) -> Path:
    """Create private local state and fail if its OS permissions cannot be set."""
    resolved = root.expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        identity = current_os_identity()
        completed = subprocess.run(
            [
                "icacls", str(resolved), "/inheritance:r", "/grant:r",
                f"{identity.principal}:(OI)(CI)F", "/grant:r", "*S-1-5-18:(OI)(CI)F",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if completed.returncode != 0:
            raise PermissionError(f"Unable to apply the secure runtime ACL: {completed.stderr.strip()}")
    else:
        resolved.chmod(0o700)
    return resolved


@contextmanager
def _exclusive_runtime_lock(root: Path) -> Iterable[None]:
    """Serialise key, index, ledger, seal, and backup mutations across processes."""
    lock_path = root / LOCK_FILE
    with lock_path.open("a+b") as handle:
        handle.seek(0)
        if handle.read(1) == b"":
            handle.seek(0)
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_or_create_signing_key(root: Path = SECURE_RUNTIME_DIR) -> bytes:
    """Load a current-user-bound key without writing plaintext key material."""
    secured = secure_runtime_directory(root)
    key_path = secured / KEY_FILE
    if key_path.exists():
        key = _unprotect_for_current_windows_user(key_path.read_bytes())
    else:
        key = secrets.token_bytes(32)
        key_path.write_bytes(_protect_for_current_windows_user(key))
    if len(key) != 32:
        raise ValueError("Invalid local signing key length")
    return key


def _safe_repository_source(relative_path: str) -> Path:
    candidate = (TRITON_ROOT / relative_path).resolve()
    if TRITON_ROOT not in candidate.parents or not candidate.is_file():
        raise ValueError(f"Manifest source is missing or outside TRITON_ROOT: {relative_path}")
    return candidate


def _sections(markdown: str) -> Iterable[tuple[str, str]]:
    heading = "Document"
    lines: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("#") and line.lstrip("#").startswith(" "):
            if lines and any(item.strip() for item in lines):
                yield heading, "\n".join(lines).strip()
            heading = line.lstrip("#").strip()
            lines = [line]
        else:
            lines.append(line)
    if lines and any(item.strip() for item in lines):
        yield heading, "\n".join(lines).strip()


def build_authorised_index(
    manifest_path: Path = DEFAULT_MANIFEST, root: Path = SECURE_RUNTIME_DIR
) -> Path:
    """Build a local JSON index whose contents are bound to repository hashes."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("classification") != "INTERNAL":
        raise ValueError("The workstation runtime admits only the INTERNAL source manifest")
    documents: list[dict[str, Any]] = []
    for source in manifest.get("sources", []):
        if source.get("applicability") != "APPLICABLE":
            continue
        path = _safe_repository_source(str(source["path"]))
        content = path.read_text(encoding="utf-8")
        source_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if source.get("sha256") != source_hash:
            raise ValueError(f"Source hash is not admitted by manifest: {source['source_id']}")
        for ordinal, (heading, section) in enumerate(_sections(content), start=1):
            documents.append({
                "source_id": source["source_id"],
                "source_version": f"{source['edition']}@sha256:{source_hash}",
                "resource_id": f"rag://triton-company-os/{source['source_id']}#{ordinal}",
                "tenant": manifest["tenant"],
                "purpose": manifest["purpose"],
                "classification": manifest["classification"],
                "required_scope": "rag:read",
                "required_attributes": [["runtime", "founder-workstation"]],
                "valid_from": "2000-01-01",
                "valid_until": "9999-12-31",
                "applicability": "APPLICABLE",
                "heading": heading,
                "content": section,
                "content_sha256": hashlib.sha256(section.encode("utf-8")).hexdigest(),
                "source_path": source["path"],
                "source_file_sha256": source_hash,
            })
    if not documents:
        raise ValueError("The authorised source manifest produced no documents")
    target = secure_runtime_directory(root) / INDEX_FILE
    payload = {
        "manifest_id": manifest["manifest_id"],
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "declared_use": manifest["declared_use"],
        "documents": documents,
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def _load_verified_index(
    index_path: Path, manifest_path: Path = DEFAULT_MANIFEST
) -> tuple[dict[str, Any], tuple[RagDocument, ...]]:
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    current_manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if payload.get("manifest_sha256") != current_manifest_hash:
        raise ValueError("Authorised source manifest changed since indexing")
    documents: list[RagDocument] = []
    for item in payload.get("documents", []):
        source_path = _safe_repository_source(str(item["source_path"]))
        current_file_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if current_file_hash != item["source_file_sha256"]:
            raise ValueError(f"Source changed since indexing: {item['source_id']}")
        values = {key: item[key] for key in (
            "source_id", "source_version", "resource_id", "tenant", "purpose",
            "classification", "required_scope", "valid_from", "valid_until",
            "applicability", "content", "content_sha256",
        )}
        values["required_attributes"] = tuple(tuple(pair) for pair in item["required_attributes"])
        documents.append(RagDocument(**values))
    if not documents:
        raise ValueError("The local authorised index is empty")
    return payload, tuple(documents)


def _claims(key: bytes, now: datetime) -> IdentityClaims:
    identity = current_os_identity()
    return sign_identity(
        IdentityClaims(
            assertion_id=f"local-{secrets.token_hex(16)}",
            issuer=identity.source,
            subject=identity.stable_id,
            tenant="triton-company-os",
            service_identity=identity.principal,
            purpose="company-os-assurance",
            scopes=("rag:read", "evidence:write"),
            attributes=(("runtime", "founder-workstation"), ("clearance", "INTERNAL")),
            expires_at_utc=(now + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
        ),
        key,
    )


def _seal(ledger: EvidenceLedger, key: bytes) -> Path:
    ledger_bytes = ledger.ledger_path.read_bytes() if ledger.ledger_path.exists() else b""
    target = ledger.root / SEAL_FILE
    target.write_text(hmac.new(key, ledger_bytes, hashlib.sha256).hexdigest() + "\n", encoding="ascii")
    return target


def verify_sealed_ledger(ledger: EvidenceLedger, key: bytes) -> list[str]:
    errors = ledger.verify()
    seal_path = ledger.root / SEAL_FILE
    if not seal_path.is_file():
        errors.append("ledger seal missing")
        return errors
    content = ledger.ledger_path.read_bytes() if ledger.ledger_path.exists() else b""
    expected = hmac.new(key, content, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, seal_path.read_text(encoding="ascii").strip()):
        errors.append("ledger seal mismatch")
    return errors


def run_local_assurance(
    query: str, retention_until: str, root: Path = SECURE_RUNTIME_DIR
) -> dict[str, Any]:
    """Execute a local retrieval and record only its citation metadata."""
    secured = secure_runtime_directory(root)
    with _exclusive_runtime_lock(secured):
        key = load_or_create_signing_key(secured)
        index_path = secured / INDEX_FILE
        if not index_path.exists():
            build_authorised_index(root=secured)
        index_payload, documents = _load_verified_index(index_path)
        now = datetime.now(timezone.utc)
        claims = _claims(key, now)
        evaluation_time = now.isoformat().replace("+00:00", "Z")
        results = BoundedRagIndex(documents).query(query, claims, key, evaluation_time)[:5]
        if not results:
            raise LookupError("No authorised local source matched the query")
        document_metadata = {
            item["content_sha256"]: item for item in index_payload["documents"]
        }
        citations = []
        for item in results:
            metadata = document_metadata[item["source_sha256"]]
            citations.append({
                **{key: item[key] for key in (
                    "source_id", "source_version", "source_sha256", "classification", "score"
                )},
                "source_path": metadata["source_path"],
                "section": metadata["heading"],
            })
        decision = authorise(
            claims,
            AccessRule(
                resource_id="evidence://triton-company-os/local-assurance",
                action="evidence:write",
                tenant="triton-company-os",
                purpose="company-os-assurance",
                classification="INTERNAL",
                required_scope="evidence:write",
                required_attributes=(("runtime", "founder-workstation"),),
            ),
            key,
            evaluation_time,
        )
        ledger = EvidenceLedger(secured / EVIDENCE_DIR)
        if ledger.ledger_path.exists():
            errors = verify_sealed_ledger(ledger, key)
            if errors:
                raise ValueError("Existing evidence failed pre-write verification: " + "; ".join(errors))
        record = ledger.append(
            decision,
            "AUTHORISED_LOCAL_RAG_QUERY",
            json.dumps(citations, sort_keys=True).encode("utf-8"),
            evaluation_time,
            retention_until,
            {
                "manifest_id": str(index_payload["manifest_id"]),
                "query_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
            },
        )
        _seal(ledger, key)
        errors = verify_sealed_ledger(ledger, key)
        if errors:
            raise ValueError("Operational evidence verification failed: " + "; ".join(errors))
        return {"identity_sid": claims.subject, "record_id": record["record_id"], "citations": citations}


def verified_backup(root: Path = SECURE_RUNTIME_DIR) -> Path:
    secured = secure_runtime_directory(root)
    with _exclusive_runtime_lock(secured):
        key = load_or_create_signing_key(secured)
        source = EvidenceLedger(secured / EVIDENCE_DIR)
        errors = verify_sealed_ledger(source, key)
        if errors:
            raise ValueError("Source evidence is not verifiable: " + "; ".join(errors))
        target = secured / BACKUP_DIR
        if target.exists():
            shutil.rmtree(target)
        source.backup_to(target)
        errors = verify_sealed_ledger(EvidenceLedger(target), key)
        if errors:
            raise ValueError("Restored backup is not verifiable: " + "; ".join(errors))
        return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Operate Triton's local assurance runtime.")
    parser.add_argument("command", choices=("setup", "query", "self-test"))
    parser.add_argument("--query", default="access evidence retrieval")
    parser.add_argument(
        "--retention-until",
        help="ISO date from the applicable evidence-retention decision; required for query.",
    )
    args = parser.parse_args()
    if args.command == "setup":
        root = secure_runtime_directory()
        with _exclusive_runtime_lock(root):
            load_or_create_signing_key(root)
            index = build_authorised_index(root=root)
        print(json.dumps({"status": "READY", "runtime": str(root), "index": str(index)}))
        return
    if args.command == "query" and not args.retention_until:
        parser.error("query requires --retention-until from the applicable retention decision")
    retention_until = args.retention_until or datetime.now(timezone.utc).date().isoformat()
    result = run_local_assurance(args.query, retention_until)
    if args.command == "self-test":
        result["verified_backup"] = str(verified_backup())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
