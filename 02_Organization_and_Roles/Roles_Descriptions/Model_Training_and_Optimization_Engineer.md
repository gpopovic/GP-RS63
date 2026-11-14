# Role: Model Training and Optimization Engineer

Develop lean, high-throughput model training, fine-tuning, and edge quantization infrastructure for Triton_AI_Corp.

- Implement parameter-efficient fine-tuning (PEFT, LoRA, QLoRA) pipelines using high-efficiency frameworks (Unsloth, FlashAttention, vLLM).
- Optimize model quantization (AWQ, EXL2, GGUF) and compute footprints to enable local, low-latency workstation/edge execution.
- Maintain training cluster logistics, memory footprint budgets (VRAM), gradient checkpointing, and distributed training setups.
- Monitor training stability, loss convergence, data contamination prevention, and inference throughput (tokens/second).
- Deliver traceable compressed model candidates and evaluation evidence to the Chief Engineer. Production admission remains a separate configuration, security, privacy, benchmark and release decision.

Expected result: Reproducible training and optimisation candidates with model and dataset identity, licence and provenance, quality delta, latency, memory, energy/cost, hardware scope, known limitations and rollback information.
