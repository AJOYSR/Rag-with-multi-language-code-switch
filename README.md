# Does Abstention Transfer Across Scripts?

**Working title:** *Does Abstention Transfer Across Scripts? Controlled Evidence-Sufficiency Evaluation in Bengali–English RAG*

**Author:** Ajoy Sarker (solo) · **Started:** 2026-10-23 · **Status:** Phase 2 (planning) complete; Phase 3 (literature validation) in progress

---

## 1. Objective

Find out whether a retrieval-augmented generation (RAG) system's decision to **answer or abstain** stays reliable when the *same question* over the *same evidence* is written in:

| Code | Variant | Example (illustrative) |
|---|---|---|
| `EN` | English | "What is the registration fee?" |
| `BN` | Bengali, native script | "নিবন্ধন ফি কত?" |
| `RBN` | Romanized Bengali | "nibondhon fee koto?" |
| `CM` | Bengali–English code-mixed | "registration fee koto taka?" |

The core manipulation is **evidence sufficiency**. Every question has a *sufficient* version (the answer is in the evidence) and an *insufficient* version (the key fact is removed). A reliable system answers the first and abstains on the second, **in every variant**.

The main questions are:
1. Do unsupported-answer and unnecessary-abstention rates differ across variants when meaning and evidence are held constant?
2. Does an abstention threshold calibrated in English **transfer** to the other variants?
3. Does a cheap intervention close the gap on held-out items?

The full rationale, hypotheses and design are in [`01_planning/research_plan.md`](01_planning/research_plan.md).

## 2. Folder structure

```
Topic1_Abstention_Transfer_Bengali_RAG/
├── README.md                  ← this file
├── 00_admin/                  project management
│   ├── decision_log.md        every non-trivial decision, with date + rationale
│   ├── progress_log.md        dated weekly log of work done / blockers
│   └── open_questions.md      unresolved questions and who/what resolves them
├── 01_planning/
│   └── research_plan.md       background, gap, RQs, hypotheses, design, timeline, venues
├── 02_literature/
│   ├── literature_matrix.md   one row per study: objective, method, findings, limits, relevance, verification status
│   ├── notes/                 per-paper deep-read notes (<bibkey>.md)
│   └── pdfs/                  local copies (not for redistribution)
├── 03_data/
│   ├── DATA_CARD.md           sources, licences, construction, validation, known issues
│   ├── raw/                   source documents exactly as obtained (+ URL, date, licence)
│   ├── processed/             base items: question, answer, evidence (sufficient / insufficient)
│   ├── variants/              EN / BN / RBN / CM renderings + validation annotations
│   └── splits/                dev / test split by base item (never by variant)
├── 04_methodology/
│   └── protocol.md            (created at protocol freeze, wk 5–6) frozen experimental + analysis protocol
├── 05_experiments/
│   ├── src/                   code (data building, inference, scoring, analysis)
│   ├── configs/               one YAML per run (model, prompt, method, decoding, seed)
│   ├── runs/                  raw model outputs, keyed by run id (append-only)
│   └── EXPERIMENT_LOG.md      run id → config, commit hash, date, cost, notes
├── 06_results/
│   ├── tables/                generated tables (never hand-edited)
│   └── analysis.md            (created at M4) interpretation, including null / negative results
├── 07_figures/                generated figures + the script that made each one
├── 08_references/
│   └── references.bib         only entries verified against the publisher / arXiv / ACL Anthology
├── 09_drafts/                 paper drafts (vNN_YYYY-MM-DD.tex / .md)
└── 10_final/                  submission package, camera-ready, supplementary material
```

## 3. Workflow

The project moves through **gated phases**. A phase starts only when the previous gate passes; the evidence for each gate goes in `00_admin/decision_log.md`.

| Phase | Output | Gate to pass |
|---|---|---|
| 1. Setup | This structure | — |
| 2. Planning | `research_plan.md` | Plan reviewed |
| 3. Literature validation | `literature_matrix.md` with closest works deep-read | **G1 – Novelty:** no prior work already answers RQ2 for Bengali scripts |
| 4a. Pilot | 30 items × 4 variants, 2 models | **G2 – Effect:** a gap in unsupported-answer or abstention rate of ≥ 5 pp, or a clear reason to pivot |
| 4b. Dataset | 150–200 validated base items | **G3 – Quality:** meaning-equivalence agreement meets threshold |
| 4c. Main experiments | Pre-registered runs on the test split | Protocol frozen *before* any test-split run |
| 4d. Intervention + retrieval extension | Held-out results | — |
| 5. Writing | Draft in `09_drafts/` | Every claim traceable to a table, figure or citation |
| 6. QA + submission | `10_final/` | Final checklist (see plan §12) |

## 4. Documentation standards

1. **No fabrication.** Never record a citation, number, or result that was not observed. Mark anything unverified with `[UNVERIFIED]`.
2. **Verification status for literature.** Each entry is tagged `metadata-verified`, `abstract-read`, or `full-read`. Only `full-read` papers may support specific claims in the paper.
3. **Provenance.** Every raw document records its source URL, access date and licence. Every derived item records its parent document id.
4. **Reproducibility.** Every run has a config file, a code commit hash, a model identifier with version or date, decoding parameters, and a seed. Raw outputs are never overwritten.
5. **Test-split discipline.** No prompt, threshold or method tuning on `test`. All tuning uses `dev`.
6. **Negative results are kept.** Failed approaches are logged with a diagnosis in `06_results/analysis.md`.
7. **Decisions are dated.** Decisions use the format `YYYY-MM-DD — decision — why — alternatives considered`.
8. **AI-assistance disclosure.** Record where AI tools were used (drafting, translation drafts, coding) so the disclosure in the paper is accurate.

## 5. Constraints (assumed; confirm in `00_admin/open_questions.md`)

- Solo author, ~20 h/week, ~US$20/month compute/API budget.
- No model training. Inference-only experiments with open-weight models (local) and at most one low-cost API model.

## 6. Related prior work by the author

- A. Sarker & Riya, *Calibration Language Changes How Quantized Models Fail: Case Study of a Small Bangla Math LLM* (in `../Papers/`). This project extends the same thesis, that **language is a hidden variable in LLM reliability**, from calibration to answer/abstain decisions in RAG.
