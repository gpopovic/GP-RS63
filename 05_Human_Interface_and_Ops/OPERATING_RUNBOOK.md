# Triton Operating Runbook

## 1. Start an Opportunity

Give Triton a short evidence-based brief: customer or market, problem, desired outcome, budget or timing, constraints, data class, and decision requested. The Business Model, Market Intelligence, Marketing, Business Development, Proposal, Pricing, Legal, and Finance roles turn it into a qualified opportunity, offer decision, and risk-aware commercial path.

Use the `monthly_marketing_sales_review` when the evidence spans campaigns, pipeline, offer claims, or a launch.

## 2. Create a Product Workspace Only After the Work Is Approved

From the Company OS root, create a separate work area:

```powershell
python 04_Execution_Engine/project_workspace.py create acme-reporting-mvp --purpose "AI-supported reporting MVP"
```

It creates the configured external workspace with exact `Inputs`, `Work`, `Outputs`, `Evidence`, `Operations`, and `Learning Exports` boundaries. Put the approved brief, requirements, data classification, constraints, and acceptance criteria in `01_Inputs/`; never put product source, customer artefacts, or operational records inside the Company OS.

Validate the boundary at any time:

```powershell
python 04_Execution_Engine/project_workspace.py validate acme-reporting-mvp
```

## 3. Run Delivery

For a safe deterministic pipeline check:

```powershell
python 04_Execution_Engine/LangGraph_Pipelines/master_graph.py "Create a typed reporting service with acceptance tests." --demo
```

For real local-model execution, omit `--demo`. The graph loads all system instructions dynamically and runs Requirements → Architecture → Execution → independent review → Validation. A failed validation returns to execution, capped at three attempts.

## 4. Operate Departments and Meetings

Supply each meeting with its named required inputs from `01_Governance_and_Strategy/VIRTUAL_MEETING_CATALOG.json`. The meeting graph gathers independent positions and has its chair issue minutes with decisions, owners, dates, risks, assumptions, and escalations.

```powershell
python 04_Execution_Engine/LangGraph_Pipelines/test_governance_meeting.py
```

Use the monthly procurement/product-operations meeting for sourcing, supplier, inspection, stock, fulfilment, and payment exceptions. Inspectors may challenge or reject evidence but do not select suppliers or approve their own work.

For a proposed feature or product improvement, prepare the seven required inputs of `biweekly_feature_investment_review` before allocating material capacity. Once it enters delivery, the feature team uses one lean ALM source of truth, a Sprint Goal, explicit acceptance criteria, and an evidence-linked Definition of Done. The Scrum Master facilitates effectiveness; the ALM and Jira Product Administrator controls the system, workflow pilots, and dashboards.

## 5. Feed Learning Back Without Moving Product Work

At the end of a delivery period, export aggregate `KPI_Export.json` and `Lessons_Learned.json` from `06_Learning_Exports/`. They are the only product-to-Company-OS interface. The Company uses them for KPI review and controlled role, process, skill, MCP, and model trials under `OPERATING_UPDATE_CADENCE.md`.
