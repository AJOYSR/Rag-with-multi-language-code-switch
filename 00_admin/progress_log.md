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
