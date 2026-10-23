# Decision Log

Format: `YYYY-MM-DD — decision — why — alternatives considered`

- **2026-10-23** — Selected Topic 1 (abstention transfer across Bengali scripts in RAG) over Topic 2 (prompt-injection security–utility). — Best fit with the author's Bengali NLP + production RAG background, continuity with the calibration-language paper, objective evaluation, and feasibility at 20 h/week and ~$20/month. — Topic 2 (crowded; harder labels) is kept as the follow-up; the variant-generation pipeline will be reused.
- **2026-10-23** — Core design uses **oracle evidence**; retrieval is an optional extension. — Isolates generation and abstention from retrieval failure; the retrieval extension is the first thing cut if late. — Full RAG from the start (confounded).
- **2026-10-23** — Split by **base item**, not by variant. — Prevents leakage between near-duplicate variants. — Random split by row.
- **2026-10-23** — Add a **closed-book control** to every item. — Separates hallucination from parametric memorisation on insufficient-evidence items. — No control (confounded UAR).
- **2026-10-23** — Do not claim "first" multilingual abstention or Bengali RAG study. — Feng et al. 2024, NoMIRACL 2024 and others already exist. — n/a
- **2026-10-23** — Inference stack: local **Ollama** with GGUF 4-bit (Q4_K_M by default) on the author's Apple M5 / 16 GB unified memory; exact model tags + quantisation recorded per run (resolves Q1). — Free, reproducible, exposes logprobs for M2b; hardware checked in-session (`sysctl`: Apple M5, 17179869184 bytes RAM). — MLX (fewer standard quantised builds), Colab/Kaggle (less reproducible), + API model (cost; can be revisited after G2).
- **2026-10-23** — Second native-speaker annotator: author reports one is lined up (resolves Q2; consent + credit per plan §8). — Required for G3. — Self-review fallback (weaker).
- **2026-10-23** — Calibration-language paper (Sarker & Riya) is an **unpublished draft**: it will **not** be cited; it may motivate the work only informally (resolves Q4). — Cannot cite an unavailable draft; avoids anonymity issues. — Cite as preprint (not available).
- **2026-10-23** — Initialise a local git repository; commit at each milestone and at protocol freeze; never push (author approved). — Protocol hash + evidence that the test split was untouched (plan §12.1). — Dated snapshots + SHA-256.
