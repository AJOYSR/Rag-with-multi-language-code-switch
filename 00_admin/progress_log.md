# Progress Log

## Week 0 — 2026-10-23
**Done**
- Project folder and structure created; README with workflow and documentation standards.
- Research plan v0.1 (`01_planning/research_plan.md`).
- Initial literature scan: 6 closest works and 1 survey metadata-verified; abstracts read. Nothing full-read yet.
- Seed `references.bib` with verified metadata only.

**Next (Week 1–2, M1)**
- Full-read A1–A6 in `02_literature/literature_matrix.md`; write `notes/<bibkey>.md` for each.
- Run the G1 novelty searches listed in literature matrix §D.
- Resolve Q1 (hardware) and Q2 (second annotator).

**Blockers**
- None yet.

## Session — 2026-10-23 (Phase 3, M1 → Gate G1)
**Done**
- Resolved Q1 (local Ollama, 4-bit, Apple M5 16 GB), Q2 (annotator lined up), Q4 (calibration paper unpublished → not cited); `git init` (local only).
- Full-read A1–A6 plus three new close works found by search (A7 Alfarano et al. 2026, A8 Thimma Krishnaram et al. 2026, A9 BanglaShield). Notes in `02_literature/notes/` (9 files). Every verbatim quote was string-matched against the fetched source text; mismatches were checked by hand (one verb-form fix in the Khullar notes).
- Novelty searches logged in `02_literature/search_log.md` (arXiv API, Semantic Scholar, Google Scholar, web, ACL via site search; citation chase A1 = 122, A2 = 20) plus lead follow-ups L1–L4.
- B2/B3 and C1–C8 verified (`02_literature/verification_BC.md`); C10–C14 added. `references.bib` now 25 entries; Feng/NoMIRACL TODOs fixed.
- Corrections to v0.1 facts: Marwah et al. (English distractor; range 0.424–0.998, not 0.806–0.998); NoMIRACL official title; Khullar does **not** include Bengali.
- Updated research plan §2 gap table + revised gap statement, §4 contribution 2 (narrowed). Literature matrix §D updated.
- **G1 deliverable:** `02_literature/G1_novelty_memo.md` — recommendation: proceed with reframing.

**Failed / limited**
- Semantic Scholar rate-limited 12/15 searches; ACL Anthology covered only via web site-search (no hit counts); Google Scholar "cited by" blocked. "Probe Before you Answer" (Scholar-only) unresolved. Gaikwad & Gaikwad 2026 full text paywalled (abstract only).
- Figures in several papers are images; only captions read (noted per file).

**Next task**
- Author decision at G1. If "proceed": Phase 4a — install Ollama + Python env, choose 2 models, draft 30 fictional base items for author approval.

**Blockers**
- G1 author decision (hard stop). Manual checks listed in memo §6(b).

## Session — 2026-10-23 (cont.) — G1 passed; Phase 4a started
**Done**
- G1 decision recorded (author: "proceed"). Manual checks run by agent in a browser: "Probe Before you Answer" found and full-read (Krause et al., WMT 2026, A10 — closest RQ2 work; probe thresholds don't transfer across native-script languages); 10 ACL Anthology queries logged (L6–L15); memo addendum written.
- Environment: Ollama 0.40.9, uv 0.13.5, Python 3.11 `.venv`, pinned `requirements.txt`, `Makefile`.
- Code (`05_experiments/src/`): `normalize.py`, `scoring.py`, `items.py`, `prompts.py`, `llm.py`, `run.py` (integrity guards), `analyze_pilot.py`, `build_review_sheet.py`, `apply_review.py`. **65 unit tests pass** (`make test`). Tests caught 4 real bugs before any run: contraction patterns; NFC "য়" in month names; `\b` failing after Bengali vowel signs (dates, names); case-suffix handling for Bengali names.
- 30 pilot items drafted (6 per answer type, fictional notices) → `03_data/processed/pilot_items_draft.yaml`; all pass automatic checks; review sheets + instructions in `03_data/variants/`.
**Not done / blocked**
- Model downloads in progress (qwen3.5:9b, gemma2:9b; ~2.3 MB/s). Gemma3-12B dropped (outside 7–9B spec; download time).
- **Pilot blocked on author review of variants** (CLAUDE.md Phase 4a).
**Next**
- When models finish: 2-item smoke test (not a result), record model digests/licences, check Bengali behaviour.
- After review returned: `apply_review` → `make pilot` → `analyze-pilot` → G2 report.

## Session — 2026-10-24 — Phase 4a pilot run → Gate G2
**Done**
- Author reviewed all 30 pilot items (string edit rate 3.3%). Encoding incident (CSV saved without Unicode) recovered; 3 Bengali edits reconstructed and confirmed by the author; logged.
- Matched-quantisation models (Q4_K_M, same quantiser); smoke tests; pilot runs `20261024_pilot_qwen35_9b`, `20261024_pilot_gemma2_9b` (1,620 calls each, $0).
- Scoring refined (4-way outcome; 86 unit tests pass); 7 ambiguous responses adjudicated (author accepted).
- **G2 deliverable:** `06_results/G2_pilot_report.md`. Headline: M1 hallucination gaps are small (≤ 6.7 pp, CIs include 0; EN floor 3%); Gemma RBN over-abstention +10 pp; Qwen sufficiency score shifts on RBN; RBN comprehension largely fails (80–90% flagged) without matching behavioural failure; no memorisation (fictional notices).
**Failed / caveats**
- Initial scoring rule overcounted UAR (found by manual audit; fixed before reporting). Comprehension probe is a crude proxy and lacks passage context.
**Next**
- Author G2 decision (proceed with 4 changes / unchanged / pivot) and target size. Then Phase 4b protocol draft.
**Blockers**
- G2 decision (hard stop).

## Session — 2026-10-24 (cont.) — G2 passed; Phase 4b
**Done**
- G2 passed (author: proceed + 4 changes, ~200 items). Protocol v1.0 drafted, **approved and frozen** (tag `protocol-v1.0`, `04_methodology/protocol_freeze.txt`). Annotation guidelines drafted (`04_methodology/annotation_guidelines.md`).
- Code: `split.py` (deterministic dev/test), distractor-context assembly, TRP probe, paraphrase-B prompts, plural wording for multi-notice contexts, annotation-sample builder, prefix-aware review tools. 92 tests pass.
- Batch D (42 items, N129–N170) drafted by a subagent and validated (0 problems); committed (NOT author-reviewed).
**Failed**
- Batches A–C drafting agents were terminated by an account spend limit (HTTP 429) before writing any file; relaunched with incremental saving.
**Next**
- Validate batches A–C, cross-batch checks, build combined review sheet (`review_main`) for the author.
**Blockers**
- Author review of ~170 new items; second annotator consent/briefing.
