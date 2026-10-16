# RS63 Product Workspaces

These document and evidence workspaces were imported from the user-supplied `TriCorp-Product-Workspaces.zip` on 2026-10-16. They remain separate from the TriCorp Company OS and from the source-code checkouts under `/workspace`.

| Workspace | Scope | Source-code relationship |
|---|---|---|
| BZS | Reusable software platform and OneBinary records | Existing checkout: `/workspace/BZS` |
| HBI-High-Premium | Proposed system-level workspace | Existing checkout: `/workspace/HBI-High-Premium`; the system-level classification remains an open source decision |
| Systemverbund-Roto-Silenta-6-3 | RS63 system integration and assurance records | The uploaded portfolio names `Hettichlab/Systemverbund-Roto-Silenta-6.3`; the existing checkout is `/workspace/BZS-ROTO-SILENTA-6.3-Robotic`. Their relationship is unconfirmed. |

`Systemverbund-RU320` is excluded from this repository at the user's request because it concerns another product. The local portfolio manifest contains only the three selected workspaces. The original archive remains in the intake area.

## Status and language

The imported charters, applicability records, assurance profiles, and evidence indexes retain their original contents and draft status. Source assertions about standard editions, official verification, repository permissions, and applicability have not been independently verified by importing the archive. Do not treat draft profiles or empty evidence folders as approval or completed verification.

Documentation, code identifiers, comments, and docstrings use English. Conversational explanations may be in German.

## Layout

Each workspace uses `01_Inputs`, `02_Work`, `03_Outputs`, `04_Evidence`, `05_Operations`, and `06_Learning_Exports`. Keep platform and system evidence in their respective workspaces. The existing source-code repositories remain in their current locations; no product source code was copied into these documentation folders. Empty leaf directories contain `.gitkeep` placeholders so Git preserves the complete evidence structure.

Configure TriCorp operations with:

```bash
export TRITON_PRODUCT_WORKSPACES_ROOT=/workspace/GP-RS63/Product-Workspaces
/workspace/tricorp-runtime/venv/bin/python /workspace/TriCorp/04_Execution_Engine/project_workspace.py validate Systemverbund-Roto-Silenta-6-3
```

The workspace validator checks the manifest and required folder structure. It does not establish regulatory compliance, requirement completeness, or release readiness.
