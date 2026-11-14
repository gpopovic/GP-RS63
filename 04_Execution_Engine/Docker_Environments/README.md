# Triton Container Runtime

The Compose file provides two intentionally separate profiles:

- `smoke`: runs the deterministic graph test without model or LangSmith calls.
- `live`: uses values from `04_Execution_Engine/LangGraph_Pipelines/.env` or the project-root `.env` and calls the configured OpenAI-compatible endpoint.

Run from this directory:

```powershell
docker compose --profile smoke up --build
docker compose --profile live run --rm triton-live
docker compose --profile live run --rm triton-live python 04_Execution_Engine/LangGraph_Pipelines/master_graph.py "Implement a typed health-check endpoint."
```

For the recommended local Ollama runtime, the live container automatically uses `OPENAI_API_BASE=http://host.docker.internal:11434/v1`. Outside Docker, Triton uses `http://localhost:11434/v1`. `TRITON_DEFAULT_MODEL`, `TRITON_SPECIALIST_MODEL`, and `TRITON_VALIDATOR_MODEL` run sequentially, so only one model consumes scarce GPU memory at a time. For LiteLLM in a separate container, set `TRITON_DOCKER_API_BASE` to its Compose service, for example `http://litellm:4000/v1`. Keep keys only in an unversioned `.env`.

`triton-filesystem` in `.vscode/mcp.json` runs isolated in the official filesystem MCP container and receives access only to the open workspace. `mcp-documentation` points to the official MCP documentation. Add further MCP servers only after purpose, permission, and trust review.
