"""Backward-compatible local smoke-test entry point for the master graph."""

from __future__ import annotations

import os

from master_graph import build_demo_runner, build_graph, parse_validation_status


def main() -> None:
    """Run without model credentials or LangSmith trace submission."""
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    result = build_graph(build_demo_runner()).invoke(
        {
            "task": "Validate the portable Triton master graph smoke test.",
            "requirements": "",
            "architecture": "",
            "implementation": "",
            "independent_review": "",
            "validation": "",
            "validation_status": "FAIL",
            "attempts": 0,
        }
    )
    assert result["validation_status"] == "PASS"
    assert result["attempts"] == 1
    assert parse_validation_status("**RESULT: PASS**\nReviewed.") == "PASS"
    assert parse_validation_status("## RESULT: PASS\nReviewed.") == "PASS"
    assert parse_validation_status("Discussion mentions RESULT: PASS but is not a decision.") == "FAIL"
    print("Master graph smoke test passed.")


if __name__ == "__main__":
    main()
