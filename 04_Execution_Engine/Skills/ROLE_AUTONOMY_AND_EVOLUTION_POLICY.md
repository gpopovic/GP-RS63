# Role Autonomy and Evolution Policy

## Operating Modes

| Mode | Permitted freedom | When to use |
| --- | --- | --- |
| `EXPLORATORY` | May explore alternatives, propose novel workflows, and use wider reasoning latitude within existing tools and data boundaries | Repeated high quality, high traceability, low rework, and no severe failure |
| `GUIDED` | Follow role workflow, approved templates, and normal independent review | Default mode or mixed evidence |
| `STRICT` | Follow an approved checklist/schema, use bounded inputs, require explicit evidence at each gate, and prohibit unvalidated variation | Severe failure, repeated gate miss, low quality, or material risk regression |

## Adaptive Rule

The Role and Skill Evolution Manager may recommend a mode change from append-only observations. It grants more freedom only after sufficient comparable evidence. It recommends stricter operation immediately for a severe failure and after repeated quality or gate failures. It cannot edit a canonical role instruction, activate a candidate, or weaken a protected gate.

## Role Split Rule

Propose a split only when at least three comparable observations show sustained boundary pressure, conflicting goals, materially different competence needs, or a hand-off that cannot be made reliable inside one role. The output is two or more `trial` role candidates with separate missions, interfaces, KPIs, and evaluation cases. The original role remains the baseline until a configuration decision activates a replacement.

## Lean Process Rule

Add a gate only when its expected reduction in defect, claim, loss, or rework exposure exceeds its measured time and cost. Remove, automate, merge, or sample controls that do not improve a protected KPI. Preserve a small number of strong evidence gates rather than many ceremonial checks.

## Collaboration Safeguard

Role and skill evidence is insufficient for a major profile or process redesign. Consult `01_Governance_and_Strategy/COLLABORATION_HEALTH_AND_EVOLUTION_POLICY.md`: large changes require repeated independent signals across quality, flow, workload, cost, or risk. Apply only a single reversible micro-trial for an isolated recurring collaboration issue. A critical cross-role failure triggers containment and strict mode, never automatic redesign.
