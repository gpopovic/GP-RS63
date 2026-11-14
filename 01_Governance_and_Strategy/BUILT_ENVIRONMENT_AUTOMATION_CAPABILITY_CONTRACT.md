# Built-Environment Automation Capability Contract

## Purpose and Placement

Convert reusable SH3D, IFC, IDS/BCF, point-cloud, cost, schedule, site-log, solar, revision-diff, and publishing ideas into controlled capabilities. Triton_AI_Corp owns the contracts, admission rules, routing, and tests. Project models, measurements, prices, schedules, documents, and generated deliverables remain in the external project workspace.

## Lifecycle

`CANDIDATE` → `SANDBOX` → `VALIDATED` → `APPROVED`

- `CANDIDATE`: documented concept only.
- `SANDBOX`: synthetic or explicitly approved fixtures; no project write or external transmission.
- `VALIDATED`: representative positive, negative, boundary, malformed-input, and regression cases have evidence.
- `APPROVED`: named owner and independent reviewer authorise a specific tool/version, project class, jurisdiction, input contract, and action scope.

Passing unit tests does not promote a capability automatically.

## Capability Requirements

| Capability | Correct implementation boundary |
| --- | --- |
| `SH3D_INGEST` | Back up and hash the source; record SH3D/app version, units, levels, coordinate convention, evidence-layer status, and missing-value policy. Never invent wall, level, material, or foundation defaults. Preserve user-selected geometry and finishes. |
| `IFC_IDS_VALIDATE` | Use an IFC-aware library such as IfcOpenShell and a declared IFC schema. Validate information requirements against a versioned IDS; report issues through BCF where supported. Never parse STEP with regular expressions or infer cost classes from entity counts. |
| `POINT_CLOUD_COMPARE` | Require CRS, units, acquisition method/date, registration method, accuracy/quality evidence, outlier treatment, and reference model. Separate survey observations from engineering interpretation. |
| `COST_PLAN` | Require jurisdiction, cost taxonomy and version, quantity evidence, currency, price date/source, tax treatment, contingency method, and estimate class. Keep reserve and tax explicit; never silently impose DIN 276 on Serbia or greenfield assumptions on renovation. |
| `SCHEDULE_PLAN` | Require existing/new-build context, work-breakdown structure, dependencies, calendars, resources, constraints, duration sources, uncertainty, and approval state. Do not publish hard-coded universal durations. |
| `SITE_LOG` | Record dated observations, weather source, labour/trades, deliveries, tests, photos/evidence, blockers, instructions, and signatures. Do not generate legal notices, suitability rulings, payment withholding, or acceptance without the accountable professional. |
| `SOLAR_SIMULATION` | Define the question and require location, weather/EPW, geometry, orientation, shading, engine/version, analysis period, timestep, and relevant constructions/schedules/HVAC assumptions. Label early studies as non-compliance evidence. |
| `MODEL_REVISION_DIFF` | Use stable object identifiers plus geometry and semantic comparison, declared tolerances, baseline/revision hashes, duplicate handling, and human-classified impact. Name matching alone is advisory at best. |
| `CONTROLLED_PUBLISH` | Use versioned templates, escaped input, source manifest, reproducible tool/version, output validation, and a no-shell-injection boundary. Publication and project approval remain separate gates. |

## Execution Manifest

Before execution, validate the product-workspace job manifest with `04_Execution_Engine/built_environment_capability.py`. The validator checks lifecycle, environment, required input declarations, evidence, output location, and qualified review. It does not run the domain tool and does not certify the result.

## Required Validation Evidence

Every implementation needs representative real files or approved redacted fixtures, expected results, failure cases, unit/CRS handling, uncertainty behaviour, provenance, dependency and licence records, security review, rollback, and independent domain acceptance. Regulatory or normative values remain versioned project inputs unless the exact controlled source is included.
