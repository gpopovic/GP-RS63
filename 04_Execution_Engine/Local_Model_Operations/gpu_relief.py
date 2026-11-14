"""Release local Ollama models after a bounded Triton run."""

from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


MODEL_ENVIRONMENT_KEYS = (
    "TRITON_DEFAULT_MODEL", "TRITON_SPECIALIST_MODEL", "TRITON_VALIDATOR_MODEL",
    "TRITON_CORP_BUILDER_MODEL", "TRITON_CORP_BUILDER_CONTROLLER_MODEL",
)


def gpu_relief_enabled() -> bool:
    """Return whether completed local runs should release their VRAM allocation."""
    return os.getenv("TRITON_GPU_RELIEF_MODE", "on_demand").lower() == "on_demand"


def unload_model(model: str, *, host: str = "http://localhost:11434") -> None:
    """Ask Ollama to unload one local model without starting another model."""
    payload = json.dumps({"model": model, "keep_alive": 0}).encode("utf-8")
    request = Request(f"{host.rstrip('/')}/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=15):
        pass


def release_configured_models() -> list[str]:
    """Best-effort release of configured local models; never changes configuration."""
    if not gpu_relief_enabled():
        return []
    released: list[str] = []
    for model in sorted({os.getenv(key, "").strip() for key in MODEL_ENVIRONMENT_KEYS} - {""}):
        try:
            unload_model(model)
        except OSError:
            continue
        released.append(model)
    return released
