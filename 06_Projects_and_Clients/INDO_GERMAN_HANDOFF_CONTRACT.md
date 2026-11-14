# Indo-German Delivery Handoff Contract

Every cross-border work package uses one stable ALM identifier and a versioned handoff record. The record is created in the external product workspace and is never a reason to copy product data into Triton_AI_Corp.

Required fields: `work_item_id`, `version`, `outcome`, `acceptance_criteria`, `data_classification`, `baseline_reference`, `dependencies`, `germany_owner`, `india_owner`, `handoff_utc`, `decision_window_hours`, `evidence_plan`, `status`, and `escalation_owner`.

Allowed statuses are `READY_FOR_HANDOFF`, `IN_PROGRESS`, `BLOCKED`, `READY_FOR_REVIEW`, `ACCEPTED`, and `REJECTED`. A `BLOCKED` record requires a named dependency or decision and an escalation owner. Both sides preserve the same identifier, version, evidence links, and decision history.

Validate JSON handoff records with `04_Execution_Engine/indo_german_handoff.py validate <path>` before a handoff is declared ready for review.
