"""Render accessible, source-backed KPI dashboards without remote assets."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Any

EVIDENCE_STATES = {"DEMONSTRATION", "NOT_ASSESSED", "OBSERVED"}
DATA_QUALITY_STATES = {"SYNTHETIC", "MISSING", "ACCEPTED", "LIMITED"}


def _text(record: dict[str, Any], field: str, context: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}.{field} must be a non-empty string")
    return value.strip()


def validate_dashboard(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["dashboard must be a JSON object"]
    errors: list[str] = []
    for field in ("dashboard_id", "title", "as_of", "owner", "decision_use"):
        try:
            _text(payload, field, "dashboard")
        except ValueError as error:
            errors.append(str(error))
    evidence_state = payload.get("evidence_state")
    if evidence_state not in EVIDENCE_STATES:
        errors.append(f"dashboard.evidence_state must be one of {sorted(EVIDENCE_STATES)}")
    metrics = payload.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        return errors + ["dashboard.metrics must be a non-empty list"]
    seen: set[str] = set()
    for index, metric in enumerate(metrics):
        context = f"metrics[{index}]"
        if not isinstance(metric, dict):
            errors.append(f"{context} must be an object")
            continue
        for field in (
            "metric_id", "label", "value", "unit", "formula", "source_reference",
            "owner", "population", "confidence", "data_quality_state", "decision_use",
        ):
            try:
                _text(metric, field, context)
            except ValueError as error:
                errors.append(str(error))
        metric_id = metric.get("metric_id")
        if isinstance(metric_id, str):
            if metric_id in seen:
                errors.append(f"duplicate metric_id: {metric_id}")
            seen.add(metric_id)
        if metric.get("data_quality_state") not in DATA_QUALITY_STATES:
            errors.append(f"{context}.data_quality_state must be one of {sorted(DATA_QUALITY_STATES)}")
        target = metric.get("target")
        if target is not None:
            if not isinstance(target, str) or not target.strip():
                errors.append(f"{context}.target must be a non-empty string when present")
            try:
                _text(metric, "target_source_reference", context)
            except ValueError as error:
                errors.append(str(error))
    return errors


def render_dashboard(payload: object) -> str:
    errors = validate_dashboard(payload)
    if errors:
        raise ValueError("invalid dashboard: " + "; ".join(errors))
    assert isinstance(payload, dict)
    metrics = payload["metrics"]
    cards: list[str] = []
    for metric in metrics:
        target = ""
        if metric.get("target"):
            target = (
                f'<dt>Target</dt><dd>{escape(metric["target"])}</dd>'
                f'<dt>Target source</dt><dd>{escape(metric["target_source_reference"])}</dd>'
            )
        cards.append(
            '<article class="card">'
            f'<p class="state">{escape(metric["data_quality_state"])}</p>'
            f'<h2>{escape(metric["label"])}</h2>'
            f'<p class="value">{escape(metric["value"])} <small>{escape(metric["unit"])}</small></p>'
            '<details><summary>Definition and evidence</summary><dl>'
            f'<dt>Formula</dt><dd>{escape(metric["formula"])}</dd>'
            f'<dt>Source</dt><dd>{escape(metric["source_reference"])}</dd>'
            f'<dt>Owner</dt><dd>{escape(metric["owner"])}</dd>'
            f'<dt>Population</dt><dd>{escape(metric["population"])}</dd>'
            f'<dt>Confidence</dt><dd>{escape(metric["confidence"])}</dd>'
            f'<dt>Decision use</dt><dd>{escape(metric["decision_use"])}</dd>'
            f'{target}</dl></details></article>'
        )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(payload["title"])}</title>
<style>
:root{{--bg:#0b1020;--card:#151d31;--text:#eef4ff;--muted:#a9b7d0;--line:#33415f;--accent:#71d5ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,sans-serif}}
main{{max-width:1100px;margin:auto;padding:2rem}}.banner{{border:1px solid var(--line);padding:1rem;border-radius:.8rem;background:#11192a}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;margin-top:1rem}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:.8rem;padding:1rem}}h1,h2{{line-height:1.2}}
.state{{color:var(--accent);font-weight:700;letter-spacing:.05em}}.value{{font-size:1.7rem;font-weight:700}}small{{color:var(--muted)}}
summary{{cursor:pointer;color:var(--accent);padding:.35rem 0}}dt{{font-weight:700;margin-top:.5rem}}dd{{margin:0;color:var(--muted);overflow-wrap:anywhere}}
summary:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
</style></head><body><main>
<header><h1>{escape(payload["title"])}</h1><div class="banner"><strong>{escape(payload["evidence_state"])}</strong> · as of {escape(payload["as_of"])} · owner {escape(payload["owner"])}<br>{escape(payload["decision_use"])}</div></header>
<section class="grid">{''.join(cards)}</section>
</main></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an evidence-bound dashboard from JSON.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.write_text(render_dashboard(payload), encoding="utf-8", newline="\n")
    print(f"Dashboard rendered: {args.output}")


if __name__ == "__main__":
    main()
