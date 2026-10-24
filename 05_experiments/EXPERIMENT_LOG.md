# Experiment Log

Append-only. One row per run. Raw outputs are stored in `runs/<run_id>/` and never overwritten.

| run_id | date | split | config | git commit | model (exact id + quant) | method | n prompts | cost | notes |
|---|---|---|---|---|---|---|---|---|---|
| 20261024_smoke_gemma2_9b | 2026-10-24 | dev (2 draft items) | configs/smoke_gemma2_9b.yaml | b3cecd657903 | gemma2:9b digest ff02c3702f32 (Q4_0), Ollama 0.40.9 | M1, GEN, SUFF, CB, TR | 108 | $0 (local) | **Pipeline smoke test only — not a result, not reported.** All calls returned logprobs; median latency ~0.9 s. SUFF first-token probabilities near-binary → add confidence combiner for M3. |
