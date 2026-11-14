"""Tests for fail-closed information-access records."""

from information_access import validate_access_request


def valid_request() -> dict[str, object]:
    return {
        "request_id": "ACCESS-2099-001",
        "resource_scope": "External workspace / approved evidence capsule",
        "data_classification": "STRICTLY_CONFIDENTIAL",
        "requester": "Named service identity",
        "purpose": "Perform the approved bounded analysis",
        "processing_context": "Approved local workspace",
        "minimum_fields": ["redacted_measurement_set"],
        "data_owner": "Named Data Owner",
        "requested_at_utc": "2099-01-01T09:00:00Z",
        "expires_at_utc": "2099-01-01T12:00:00Z",
        "status": "APPROVED",
        "approvals": [
            {
                "approver": "Named Data Owner",
                "capacity": "DATA_OWNER",
                "decision": "APPROVE",
                "decided_at_utc": "2099-01-01T09:05:00Z",
                "evidence_reference": "DEC-001",
            },
            {
                "approver": "Named Privacy Reviewer",
                "capacity": "PRIVACY_CONTROL",
                "decision": "APPROVE",
                "decided_at_utc": "2099-01-01T09:10:00Z",
                "evidence_reference": "DEC-002",
            },
        ],
        "decision_reference": "GATE-2099-001",
        "revocation_owner": "Named Data Owner",
    }


def main() -> None:
    evaluation_time = "2099-01-01T10:00:00Z"
    assert validate_access_request(valid_request(), evaluation_time) == []

    title_only = valid_request()
    title_only["approvals"] = []
    assert "APPROVED requests require approval by the named data_owner" in validate_access_request(
        title_only, evaluation_time
    )

    one_approver = valid_request()
    one_approver["approvals"] = [valid_request()["approvals"][0]]
    assert (
        "STRICTLY_CONFIDENTIAL approval requires the data_owner and a distinct control approver"
        in validate_access_request(one_approver, evaluation_time)
    )

    executive_title_only = valid_request()
    executive_title_only["approvals"][1]["capacity"] = "EXECUTIVE"
    assert (
        "STRICTLY_CONFIDENTIAL approval requires the data_owner and a distinct control approver"
        in validate_access_request(executive_title_only, evaluation_time)
    )

    contradictory = valid_request()
    contradictory["approvals"].append(
        {
            "approver": "Named Security Reviewer",
            "capacity": "SECURITY_CONTROL",
            "decision": "DENY",
            "decided_at_utc": "2099-01-01T09:11:00Z",
            "evidence_reference": "DEC-003",
        }
    )
    assert "APPROVED requests must not contain an unresolved DENY decision" in validate_access_request(
        contradictory, evaluation_time
    )

    bad_window = valid_request()
    bad_window["expires_at_utc"] = bad_window["requested_at_utc"]
    assert "expires_at_utc must be later than requested_at_utc" in validate_access_request(
        bad_window, evaluation_time
    )

    expired = valid_request()
    assert "APPROVED request is expired at evaluation_time_utc" in validate_access_request(
        expired, "2099-01-01T12:00:00Z"
    )

    decision_before_request = valid_request()
    decision_before_request["approvals"][0]["decided_at_utc"] = "2099-01-01T08:59:00Z"
    assert (
        "approvals[0].decided_at_utc must not precede requested_at_utc"
        in validate_access_request(decision_before_request, evaluation_time)
    )

    decision_after_expiry = valid_request()
    decision_after_expiry["approvals"][0]["decided_at_utc"] = "2099-01-01T12:01:00Z"
    assert (
        "approvals[0].decided_at_utc must not exceed expires_at_utc"
        in validate_access_request(decision_after_expiry, evaluation_time)
    )

    naive_time = valid_request()
    assert "evaluation_time_utc must include a UTC offset" in validate_access_request(
        naive_time, __import__("datetime").datetime(2099, 1, 1, 10, 0)
    )

    # With no trusted historical evaluation time, an old approval must fail closed.
    old_request = valid_request()
    old_request["requested_at_utc"] = "2020-01-01T09:00:00Z"
    old_request["expires_at_utc"] = "2020-01-01T12:00:00Z"
    old_request["approvals"][0]["decided_at_utc"] = "2020-01-01T09:05:00Z"
    old_request["approvals"][1]["decided_at_utc"] = "2020-01-01T09:10:00Z"
    assert "APPROVED request is expired at evaluation_time_utc" in validate_access_request(old_request)

    assert validate_access_request([]) == ["access request must be a JSON object"]
    print("Information access contract tests passed.")


if __name__ == "__main__":
    main()
