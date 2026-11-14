# Local Ollama Model Runtime

Triton uses the local OpenAI-compatible Ollama server at `http://localhost:11434/v1`. The connection remains on the laptop; no cloud model is called.

1. Start Ollama and verify the local service with `ollama list`.
2. Install only models you intend to use, beginning with a bounded context window of 4k to 8k tokens.
3. Copy exact names from `ollama list` into the unversioned `../LangGraph_Pipelines/.env`.

Intended sequential role allocation:

| Purpose | Environment variable | Initial candidate status |
| --- | --- | --- |
| Requirements, architecture, execution | `TRITON_DEFAULT_MODEL` | Configure only an admitted `STANDARD` or `FLAGSHIP` candidate. |
| Independent quality validation | `TRITON_VALIDATOR_MODEL` | Configure an admitted independent `STANDARD` or `FLAGSHIP` candidate. |
| Independent Devil's Advocate review | `TRITON_SPECIALIST_MODEL` | Configure an admitted `STANDARD` candidate with a distinct failure profile where feasible. |

Measure candidates with identical tasks before accepting them as a baseline. Classify candidates under `01_Governance_and_Strategy/MODEL_CLASSIFICATION_AND_BENCHMARK_POLICY.md`; the `evaluate_local_models.py` helper records runtime and answers, while substantive assessment remains a human quality gate.

```powershell
python evaluate_local_models.py --base-url http://localhost:11434/v1 --model "<Ollama-Modellname>"
```

After comparison, keep only the accepted model loaded. In Docker live execution, the base URL points to `http://host.docker.internal:11434/v1`.

For observed quality data and controlled local or online escalation, see [MODEL_GOVERNANCE.md](MODEL_GOVERNANCE.md). The observer does not install models or transmit project content automatically.
