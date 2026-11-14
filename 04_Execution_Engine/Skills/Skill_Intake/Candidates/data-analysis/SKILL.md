---
name: data-analysis
description: Produce reproducible, decision-oriented analysis from structured data with explicit quality and uncertainty checks. Use when cleaning, joining, summarising, visualising, interpreting, or reporting operational, product, quality, or model-performance data.
---

# Data Analysis

## Workflow

1. Define the decision, metric, population, time window, and acceptable uncertainty before calculating.
2. Profile provenance, completeness, types, duplicates, outliers, and join assumptions.
3. Use transparent transformations and retain enough detail to reproduce every material result.
4. Distinguish observed facts, assumptions, inference, and recommendations.
5. Present the smallest table or chart that answers the decision question and state limitations.

## Guardrails

Never infer causation from correlation alone, hide data-quality failures, or silently discard inconvenient records. Apply the assigned data classification before using external tools.

## Reference

Read [data analysis source notes](references/source-notes.md) before handling a new dataset.
