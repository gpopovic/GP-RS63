# Model Governance and Escalation

`model_observer.py` stores evidence only under `observations/model_quality_history.jsonl` and produces routing recommendations. It does not directly change `.env` or model artifacts.

## Local Automatic Response

A model is marked insufficient only after at least `TRITON_MIN_QUALITY_SAMPLES` assessed observations below `TRITON_MIN_QUALITY_SCORE`, or after `TRITON_MAX_CONSECUTIVE_CRITICAL_FAILURES`. When `TRITON_AUTO_MODEL_ROUTING_ENABLED=true`, Triton then uses the already approved local backup from `TRITON_<ROLE>_BACKUP_MODEL`. The model baseline in `.env` remains unchanged and auditable.

Example of a reviewed observation:

```powershell
python model_observer.py record --model gemma3:4b --role primary --score 0.6 --critical-failure --evidence "Review T-42: incorrect safety assumption"
python model_observer.py status --model gemma3:4b --role primary
```

## Online Escalation

Online escalation follows the order local, EU/EEA, then US/CN only as an approved exception. It requires a minimised approved data capsule and must never transfer the complete graph state. Details are in [ONLINE_ESCALATION_POLICY.md](ONLINE_ESCALATION_POLICY.md).

## Updates

New models or tags are configuration changes under ASPICE SUP.8: document the candidate, measure it against the same Triton test set, retain the result as an observation, and make it a baseline only after human sign-off. Apply `MODEL_CLASSIFICATION_AND_BENCHMARK_POLICY.md` before classifying a candidate. Official catalog pages serve as the local watchlist: [Gemma](https://ollama.com/library/gemma3) and [Qwen3](https://ollama.com/library/qwen3).
