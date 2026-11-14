"""Smoke test for the non-mutating Corp Builder control-board entry point."""

from corp_builder_control import run_control_board


def main() -> None:
    result = run_control_board(
        "Change ID: DEMO-001\nProposal: add a non-production Academy reference.\nRollback: revert the reference.",
        demo=True,
    )
    assert result["status"] == "DECIDED"
    assert result["recommendation"] == "TRIAL"
    assert len(result["contributions"]) == 7
    assert "DEMO challenger" in result["challenger_report"]
    print("Corp Builder control-board smoke test passed.")


if __name__ == "__main__":
    main()
