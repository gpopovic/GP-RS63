"""Run identical, non-destructive Triton prompts against one local OpenAI-compatible model."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EVALUATION_CASES: tuple[str, ...] = (
    "Turn this idea into three atomic, testable software requirements: a health endpoint reports service status.",
    "Propose a small typed Python design for a service health endpoint, including one failure case.",
    "Review this defect claim critically: unit tests pass, therefore the API is production ready.",
    "Write one focused unit-test scenario for an unavailable downstream dependency.",
    "State the most important open question before releasing a health endpoint.",
)


def request_completion(base_url: str, model: str, prompt: str) -> tuple[float, str]:
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
    ).encode("utf-8")
    request = Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urlopen(request, timeout=180) as response:
        body = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    return elapsed, str(body["choices"][0]["message"]["content"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate one local model with Triton-relevant prompts.")
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible base URL, including /v1.")
    parser.add_argument("--model", required=True, help="Exact loaded model ID.")
    parser.add_argument("--output", type=Path, default=Path("local_model_evaluation.json"))
    args = parser.parse_args()

    results: list[dict[str, object]] = []
    for case in EVALUATION_CASES:
        try:
            elapsed, response = request_completion(args.base_url, args.model, case)
            results.append({"prompt": case, "seconds": round(elapsed, 2), "response": response})
            print(f"PASS {elapsed:.2f}s: {case[:56]}...")
        except (HTTPError, URLError, KeyError, TimeoutError) as error:
            results.append({"prompt": case, "error": str(error)})
            print(f"FAIL: {case[:56]}... ({error})")

    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved evaluation evidence to {args.output.resolve()}")


if __name__ == "__main__":
    main()
