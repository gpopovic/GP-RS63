# Regulatory Watch Register

## Use

This is the minimum source map for Triton's legal and regulatory watch. Each review produces an append-only record in `Regulatory_Watch_Records/` using the fields required by `LEGAL_AND_REGULATORY_CHANGE_CONTROL.md`. A listed source is a watch input, not a legal interpretation.

| Watch domain | Authoritative or primary source | Accountable watch owner | Review interval | Required counterweight |
| --- | --- | --- | --- | --- |
| EU binding legal acts and official notices | [EUR-Lex Official Journal](https://eur-lex.europa.eu/oj/direct-access.html) | Public Affairs and Policy Manager | Weekly | General Counsel and relevant domain owner |
| EU data-protection guidance and decisions | [European Data Protection Board](https://www.edpb.europa.eu/documents_en?type%5Bguidance%5D=guidance) | Privacy and Data Protection Officer | Biweekly; immediately after a data incident | General Counsel and Security Assurance Auditor |
| German data-protection authority updates | [BfDI notices](https://www.bfdi.bund.de/DE/BfDI/Presse/Kurzmeldungen/kurzmeldungen_node.html) and the competent state authority | Privacy and Data Protection Officer | Monthly; immediately for relevant enforcement | General Counsel |
| German and EU legal obligations relevant to contracts, entities, tax, labour, sanctions, and procurement | Official jurisdictional legal gazette or legislation portal selected for the active entity and country | General Counsel and Legal Department Lead | Monthly; weekly during country-entry or material transaction work | Corporate Governance, Finance, or Workforce Compliance owner |
| Security advisories and relevant technical obligations | Official vendor advisories, CERT/BSI, and approved vulnerability sources | Security Operations and Incident Response Engineer | Weekly; daily for actively exposed critical assets | Security Assurance Auditor |
| Licensed ISO, DIN, ASPICE, and sector standards | Official standard owner release and catalogue notices; licensed source retained under its terms | Safety and Compliance Engineer | Quarterly; before a regulated bid, release, or audit | Quality Manager and General Counsel |
| Country-specific legal, political, environmental, social, and humanitarian conditions | Activated country profile with official sources and qualified local-counsel route | Public Affairs and Policy Manager | Weekly during entry or active material delivery; monthly otherwise | General Counsel, Environmental and Sustainability Manager, and Social and Humanitarian Impact Officer |

## Country Profile Activation

No country is implicitly covered. Before Triton enters, hires in, contracts in, or makes a material policy commitment concerning a country, create a country profile that names: jurisdiction, legal entity, activity, official sources, local counsel or expert route, watch owner, review date, next review date, and current unresolved questions.

## Record Status

The register is structurally active, but a watch domain becomes operationally current only after its first dated review record exists. A missing or overdue record is a control exception and blocks affected binding decisions under the change-control policy.
