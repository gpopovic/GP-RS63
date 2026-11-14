# Product Workspace Contract

## Purpose

Triton_AI_Corp is a governance, role, process, knowledge, and improvement repository. It is **not** a product-delivery repository. Each client project, internal product, prototype, or manufactured item has its own workspace outside `TRITON_ROOT`.

The default external workspace root is derived from configuration as the sibling directory `Triton_Product_Workspaces`; it can be overridden with `TRITON_PRODUCT_WORKSPACES_ROOT`. No Windows-specific path is embedded in runtime code.

## Required Product Workspace Contract

Every product workspace contains an explicit `workspace_manifest.json` and these logical boundaries:

| Boundary | Required contents | Owner |
| --- | --- | --- |
| `01_Inputs/` | approved brief, requirements, data classification, constraints, acceptance criteria | Requirements / Product Owner |
| `02_Work/` | implementation, models, designs, source, build configuration | Delivery team |
| `03_Outputs/` | versioned deliverables, releases, customer-facing results | Release / Product Operations |
| `04_Evidence/` | tests, reviews, inspection results, approvals, traceability | Quality / independent inspectors |
| `05_Operations/` | runbooks, fulfilment, support, inventory or service evidence | Product Operations |
| `06_Learning_Exports/` | aggregate `KPI_Export.json` and `Lessons_Learned.json` only | Project lead |

No unclassified customer data, credentials, source code, product artefacts, invoices, or customer deliverables are copied into the Company OS as a shortcut.

## Regulated Engineering Assurance Overlay

When a project is regulated, safety-relevant, permit-dependent, certification-dependent, or otherwise high consequence, retain the same six top-level boundaries and add the logical assurance records defined in `01_Governance_and_Strategy/REGULATED_ENGINEERING_ASSURANCE_KERNEL.md`. At minimum, activate a reviewed project assurance profile and applicability record under `01_Inputs/Assurance/`; keep risk, architecture, verification planning, and change impact under `02_Work/Assurance/`; keep traceability, results, anomalies, the assurance-case index, and human approvals under `04_Evidence/Assurance/`; and keep monitoring, incidents, corrective actions, operational configuration, and retention under `05_Operations/Assurance/`.

The overlay does not make a domain profile active by copying a template. Applicability, current source editions, jurisdiction or market, required independence, toolchain expectations, and named human approval authorities must be reviewed for the exact product workspace.

## Controlled Learning Interface

Only the two export files may feed the Company OS. They must contain the workspace identifier, period, metric definition, aggregation method, evidence reference, data classification, and owner. Lessons must describe context, outcome, contributing factors, recommendation, and confidence; they cannot contain secrets or personal data unless specifically governed through an approved data capsule.

The Role Skill Evolution Manager, Quality Manager, and relevant department leads may use these exports to improve roles, skills, KPIs, and process models. They may not write product deliverables back into the Company OS.
