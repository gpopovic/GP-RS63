# Online Escalation Policy

The mandatory order is:

1. An admitted local Triton model.
2. An approved EEA/EU provider with contractually and technically confirmed European data processing.
3. A stronger US or Chinese provider only as a documented case-by-case escalation.

## Data Capsule

An online escalation never receives the entire graph state. Before transmission, a human creates a data capsule with ID, purpose, exact target provider, processing region, permitted data class, expiry date, and sanitised content. The runtime rejects a provider or region mismatch, an expired capsule, or any data class other than `PUBLIC`, `SYNTHETIC`, or `ANONYMISED_AGGREGATE`.

Credentials, personal or customer data, full internal repositories, unapproved standards text, unreviewed log extracts, and secrets are prohibited. The capsule resides as `<capsule-ID>.md` under `05_Human_Interface_and_Ops/Approved_Data_Capsules/`; the graph reads only that file for an online route.

## Configuration Gates

The following variables remain `false` or empty by default:

- `TRITON_EU_FALLBACK_*` for the preferred EU/EEA provider.
- `TRITON_US_FALLBACK_*` and `TRITON_CN_FALLBACK_*` for separately approved third-country exceptions. They are never a shared non-EU route.
- `TRITON_ONLINE_DATA_CAPSULE_ID`, `TRITON_ONLINE_DATA_CAPSULE_PATH`, and `TRITON_ONLINE_DATA_CAPSULE_APPROVED`.
- `TRITON_ONLINE_EXECUTION_APPROVED` as the final technical gate.

Only when every relevant gate is set may a separate, approved escalation run take place. The regular master graph never transfers a complete work context online.
