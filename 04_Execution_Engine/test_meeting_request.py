"""Tests for controlled role meeting requests and founder-notification inputs."""

import json
from copy import deepcopy

from config import TRITON_ROOT
from meeting_request import validate_meeting_request_register


def register() -> dict[str, object]:
    path = TRITON_ROOT / "05_Human_Interface_and_Ops" / "Meeting_Requests" / "MEETING_REQUEST_REGISTER.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assert validate_meeting_request_register(register()) == []

    unknown_role = register()
    unknown_role["requests"][0]["requested_by_role"] = "Invented_Role"
    assert any("not canonical" in error for error in validate_meeting_request_register(unknown_role))

    no_async_reason = register()
    no_async_reason["requests"][0]["reason_async_insufficient"] = ""
    assert any("reason_async_insufficient" in error for error in validate_meeting_request_register(no_async_reason))

    urgent = register()
    urgent["requests"][0]["urgency"] = "TODAY"
    assert any("requires founder attention" in error for error in validate_meeting_request_register(urgent))

    false_schedule = deepcopy(register())
    false_schedule["requests"][0]["status"] = "SCHEDULED"
    assert any("requires a calendar reference" in error for error in validate_meeting_request_register(false_schedule))

    too_many = register()
    too_many["requests"][0]["minimum_participants"] = ["System_Architect"] * 9
    assert any("1-8 canonical roles" in error for error in validate_meeting_request_register(too_many))
    print("Meeting request and founder-notification input tests passed.")


if __name__ == "__main__":
    main()
