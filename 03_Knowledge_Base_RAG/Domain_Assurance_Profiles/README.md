# Domain Assurance Profiles

This directory stores reviewed domain-source mappings and reusable terminology mappings. It must not store customer or product evidence.

The catalog in `01_Governance_and_Strategy/DOMAIN_ASSURANCE_PROFILE_CATALOG.json` contains candidate domain families only. A profile becomes usable for a product workspace only when that workspace creates and approves its own `PROJECT_ASSURANCE_PROFILE.json` and `APPLICABILITY_RECORD.md` from the controlled templates.

## Source-Record Requirements

For every relied-upon law, regulation, standard, rule, authority guidance, customer requirement, or approved interpretation, record:

- stable source ID and title;
- issuing organisation and authoritative retrieval location;
- edition, revision, publication date, effective date, and supersession status;
- jurisdiction, market, product and lifecycle applicability;
- licence and permitted RAG/indexing use;
- controlled local reference or evidence link;
- relevant clauses or sections without copying restricted text unlawfully;
- review owner, independent reviewer, review date, next review date, and open questions.

Do not infer current applicability from filenames, an AI answer, a search result, or the existence of a PDF. Country, market, product classification, contract, certification authority, class society, infrastructure manager, and customer requirements may alter the applicable set.

## Intended Substructure

A sector subfolder may contain reviewed, non-activated adapter guidance. A real project activates none of it here: the external product workspace must still approve its own applicability and assurance profile before use.

```text
Domain_Assurance_Profiles/
  Automotive/
  Industrial_Automation/
  Medical_Device/
  Aerospace/
  Rail/
  Marine/
  Built_Environment/
```

Each subfolder may contain candidate guidance, source metadata and reusable approved mappings, not customer evidence or licensed standards unless storage and indexing rights are confirmed. Candidate guidance must state `CANDIDATE_NOT_ACTIVATED` explicitly.
