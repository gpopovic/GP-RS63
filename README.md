# GP-RS63

Personal version control and working files for the RS63 project.

## Product workspaces

[Product-Workspaces](Product-Workspaces/README.md) contains the imported BZS, HBI-High-Premium, and RS63 system documentation structures. Systemverbund-RU320 is excluded. Imported records retain their draft status; the relationship between the named RS63 system repository and the existing robotic-controller checkout remains unconfirmed.

## Test Management & Test Leadership

A Codex skill for everyday test management of medical centrifuges and a later transition to leading a test department.

- [Skill](.agents/skills/testmanagement-leadership/SKILL.md)
- [Templates for strategy, status, capacity, traceability, and defect triage](.agents/skills/testmanagement-leadership/references/vorlagen.md)
- [90-day plan, team development, and resource planning](.agents/skills/testmanagement-leadership/references/fuehrung.md)
- [Skill verification record](docs/skill-pruefung.md)

## Language

Documentation, code identifiers, comments, and docstrings use English. Conversational explanations may remain in German. Preserve source quotations and established technical identifiers when exact wording matters.

## Usage

Open this repository as the working directory in Codex. The skill is under `.agents/skills/`; `AGENTS.md` also directs relevant tasks to it. Restarting Codex may be necessary for discovery. If automatic discovery is unavailable, explicitly request that Codex read the skill file.

Example requests:

> Use testmanagement-leadership to prepare a weekly test status from these results. Identify open decisions and next actions.

> Plan test capacity for next month. Separate known availability, assumptions, and missing effort estimates.

> Use testmanagement-leadership to prepare my 90-day transition plan for leading the test department.

The templates are working drafts, not approved company procedures. Adapt them using evidence of product purpose, applicable obligations, and internal responsibilities. Numerical examples are fictional. Project evidence stays in its approved location.
