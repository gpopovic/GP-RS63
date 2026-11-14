"""Freeze a read-only Git review snapshot and reconcile every tracked file."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _git(repository: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), *args], text=True, encoding="utf-8", errors="strict"
    ).strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _last_commit_map(repository: Path) -> tuple[dict[str, tuple[str, str]], dict[str, str]]:
    log = _git(repository, "log", "--format=@@COMMIT@@%H%x09%s", "--name-only")
    by_path: dict[str, tuple[str, str]] = {}
    subjects: dict[str, str] = {}
    current_hash = ""
    current_subject = ""
    for line in log.splitlines():
        if line.startswith("@@COMMIT@@"):
            current_hash, current_subject = line.removeprefix("@@COMMIT@@").split("\t", 1)
            subjects[current_hash] = current_subject
        elif line and current_hash and line not in by_path:
            by_path[line] = (current_hash, current_subject)
    return by_path, subjects


def build_snapshot_manifest(
    source_repository: Path,
    authoritative_root: Path,
    generated_at_utc: str | None = None,
) -> dict[str, object]:
    """Inventory every tracked source file without modifying the source repository."""
    source = source_repository.resolve()
    authoritative = authoritative_root.resolve()
    if not (source / ".git").exists():
        raise ValueError("source_repository must be a Git working tree")
    if _git(source, "status", "--porcelain"):
        raise ValueError("source review repository must be clean before freezing")
    source_commit = _git(source, "rev-parse", "HEAD")
    source_commit_time = _git(source, "show", "-s", "--format=%cI", source_commit)
    generated_time = generated_at_utc or datetime.now(timezone.utc).isoformat()
    tracked = [item for item in _git(source, "ls-files").splitlines() if item]
    commit_by_path, subjects = _last_commit_map(source)
    files: list[dict[str, object]] = []
    for relative in sorted(tracked):
        source_path = source / relative
        target_path = authoritative / relative
        source_hash = _sha256(source_path)
        target_hash = _sha256(target_path) if target_path.is_file() else None
        comparison = "IDENTICAL" if target_hash == source_hash else "DIVERGENT" if target_hash else "EXTERNAL_ONLY"
        last_commit, subject = commit_by_path.get(relative, (source_commit, subjects.get(source_commit, "HEAD snapshot")))
        disposition_id = "AG28-IDENTICAL" if comparison == "IDENTICAL" else f"AG28-{last_commit[:8].upper()}"
        files.append({
            "path": relative,
            "size_bytes": source_path.stat().st_size,
            "source_sha256": source_hash,
            "authoritative_sha256": target_hash,
            "comparison": comparison,
            "last_source_commit": last_commit,
            "last_source_commit_subject": subject,
            "disposition_id": disposition_id,
        })
    comparison_counts = Counter(str(item["comparison"]) for item in files)
    disposition_counts = Counter(str(item["disposition_id"]) for item in files)
    return {
        "schema_version": "1.0",
        "manifest_id": f"ANTIGRAVITY-SNAPSHOT-{source_commit[:12].upper()}",
        "generated_at_utc": generated_time,
        "source_repository": source.name,
        "source_commit": source_commit,
        "source_commit_time": source_commit_time,
        "source_commit_time_after_observation": _timestamp_after(source_commit_time, generated_time),
        "source_worktree_status": "CLEAN",
        "exclusions": [".git metadata", "untracked and ignored files"],
        "tracked_file_count": len(files),
        "comparison_counts": dict(sorted(comparison_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "files": files,
    }


def _timestamp_after(first: str, second: str) -> bool:
    return datetime.fromisoformat(first.replace("Z", "+00:00")) > datetime.fromisoformat(second.replace("Z", "+00:00"))


def validate_snapshot_manifest(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["snapshot manifest must be an object"]
    record: dict[str, Any] = payload
    errors: list[str] = []
    files = record.get("files")
    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not isinstance(files, list) or not files:
        return errors + ["files must be a non-empty list"]
    if record.get("tracked_file_count") != len(files):
        errors.append("tracked_file_count must equal files length")
    paths: set[str] = set()
    counts: Counter[str] = Counter()
    dispositions: Counter[str] = Counter()
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            errors.append(f"files[{index}] must be an object")
            continue
        path = item.get("path")
        if not isinstance(path, str) or not path or path in paths:
            errors.append(f"files[{index}].path must be unique and non-empty")
        else:
            paths.add(path)
        if item.get("comparison") not in {"IDENTICAL", "DIVERGENT", "EXTERNAL_ONLY"}:
            errors.append(f"files[{index}].comparison is invalid")
        source_hash = item.get("source_sha256")
        if not isinstance(source_hash, str) or len(source_hash) != 64 or any(char not in "0123456789abcdef" for char in source_hash):
            errors.append(f"files[{index}].source_sha256 must be lowercase hexadecimal SHA-256")
        commit_hash = item.get("last_source_commit")
        if not isinstance(commit_hash, str) or len(commit_hash) != 40 or any(char not in "0123456789abcdef" for char in commit_hash):
            errors.append(f"files[{index}].last_source_commit must be a full lowercase Git SHA-1")
        disposition = item.get("disposition_id")
        if not isinstance(disposition, str) or not disposition:
            errors.append(f"files[{index}].disposition_id is required")
        else:
            dispositions[disposition] += 1
        counts[str(item.get("comparison"))] += 1
    if record.get("comparison_counts") != dict(sorted(counts.items())):
        errors.append("comparison_counts do not reconcile")
    if record.get("disposition_counts") != dict(sorted(dispositions.items())):
        errors.append("disposition_counts do not reconcile")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Freeze an external Git snapshot without modifying it.")
    parser.add_argument("source_repository", type=Path)
    parser.add_argument("authoritative_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--generated-at-utc")
    args = parser.parse_args()
    manifest = build_snapshot_manifest(args.source_repository, args.authoritative_root, args.generated_at_utc)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Frozen {manifest['tracked_file_count']} tracked files at {manifest['source_commit']}.")


if __name__ == "__main__":
    main()
