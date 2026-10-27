# Gate G3: Dataset Quality Report

Date: 2026-10-27. Protocol: v1.0 (frozen, tag `protocol-v1.0`). Every number below traces to a file named in its row.

## 1. Final item counts [RESULT]

| | Items | Source file |
|---|---|---|
| Pilot (dev only) | 30 | `03_data/processed/pilot_items_approved.yaml` |
| Main, drafted | 170 (N001–N170, batches A–D) | `03_data/processed/main_items_draft.yaml` |
| Main, dropped | 2: N083 (answer leak), N007 (no RBN/CMR mixing contrast) | `03_data/variants/review_main_outcome.json` |
| Main, approved | 168 | `03_data/processed/main_items_approved.yaml` |
| **Total base items** | **198** | |
| **Dev** | **50** (30 pilot + 20 main; 10 per answer type) | `03_data/splits/split_v1.json` |
| **Test** | **148** (main only; amount 30, name 30, number 30, date 29, yes/no 29) | same |

Each base item expands to 5 variants (EN, BN, RBN, CM, CMR) × {main question on sufficient and insufficient evidence, sibling question on insufficient evidence}.

Main items: passages 155–195 words (mean 174), each shown with 2 distractor notices; 86 deletion and 82 neutralisation edits; 24 domains.

## 2. Author review (native Bengali speaker) [RESULT]

| Set | Kept | String edits | File |
|---|---|---|---|
| Pilot | 30/30 | 10/300 (3.3%) | `03_data/variants/review_outcome.json` |
| Main, first pass | 168/170 | 0/1,685 | `03_data/variants/review_main_outcome.json` |
| Main, after control round | 168 | +10 author-directed edits (8 RBN "korse/korser" → "course e/er"; 2 CMR given the insertion "total") | `review_main_RETURNED.csv` (`*_EDIT` columns), decision_log 2026-10-27 |

The main review sheets were returned 31 minutes after they were built (23:24 → 23:55, 2026-10-24). The author stated it was a full review of every item; this is recorded in the decision log.

## 3. Second-annotator validation (A2, native Bengali speaker) [RESULT]

**Main sample** (`06_results/agreement_A2.json`): 35 items (21%, stratified by answer type); 280 question versions; 35 insufficient notices.

| Dimension | n | Agreement with author | Cohen's κ |
|---|---|---|---|
| Meaning equivalent (A2 ≥ 2) | 280 | 100% | undefined |
| Natural (A2 ≥ 2) | 280 | 100% | undefined |
| Answer not findable in insufficient notice | 35 | 100% | undefined |

κ is undefined because both raters used a single category on every dimension. A2 rated meaning 3 on all 280 versions and naturalness 2 on 3 (all on N003, with comments); no item met a failure rule.

**Control round** (added after the freeze because of the ceiling; key and pass rule written before A2 saw it: `04_methodology/annotation_controls_KEY.yaml`; result `06_results/annotation_controls_A2.json`):

- 7/8 planted flaws detected: all 4 meaning changes, the scrambled word order, and both notices with the answer still present. Missed: a CM question with a whole English clause and a duplicated question word (rated 3/3).
- 1/4 clean rows flagged: N031 RBN (meaning 1, naturalness 1). [HYPOTHESIS] The cause was the romanization "korser" for course; the author revised it (§2).
- **Pass rule (≥ 7/8 and ≤ 1/4): passed, exactly at the threshold.**

**Re-check of the 10 revised strings** (`06_results/annotation_recheck_A2.json`): no meaning 1; meaning 3 on 9 and 2 on 1 (N023 main RBN); naturalness 2 on 3 (N023 main RBN, N031 main and sibling RBN). All pass.

## 4. Deviations and protocol notes

1. **Addition:** annotator control round and re-check (§3). Disclose in the paper.
2. Test = 148 items (protocol: "≈ 150"). Within the stated approximation.
3. Realism subset (Wikipedia, "up to 20"): not built; within the protocol. Disclosed as a limitation.
4. Two encoding incidents (review CSVs saved without Unicode); no author decision lost; raw files and recovery logs in `03_data/variants/returned_raw/`.

## 5. Limitations to disclose

- All notices are fictional and AI-drafted (Claude Opus 5.5), then reviewed by the author. AI-drafted text may differ from real notices.
- One second annotator. Main-sample ratings are at ceiling (κ undefined); the control round shows A2 detects meaning changes and answer leaks, but rated one heavily mixed, unnatural question as natural.
- Several RBN questions keep English loanwords (e.g., "fee", "course"), which narrows the RBN/CMR contrast for those items.
- Same-type decoy values (e.g., a different fee) are left in some notices on purpose; flagged items are listed in `03_data/processed/batches/review_flags.yaml`.

## 6. Open item before G3 closes

- **A2 consent** to participation and anonymised publication, and credit preference: **not yet confirmed** (only the author can confirm this).

## 7. What G3 approval unlocks (Phase 4c)

Main runs on **dev** first (M3 combiner fit on EN-dev; RQ2 threshold selection), then on **test**, with both models, as frozen.

Calls per main item: 58 (M1, GEN and SUFF on 15 rows each; CB on 5; TR and TRP on 4 each). Test: 148 × 58 = 8,584 calls per model; dev main items add 20 × 58 = 1,160.

**Time estimate** [ASSUMPTION]: the pilot took about 21 min (Qwen) and 67 min (Gemma) for 1,620 calls with single 35–60-word notices (file timestamps in `05_experiments/runs/20261024_pilot_*`). Main contexts are about 10× longer, so roughly 5–10 h per model. The dev run will measure this before test.

Cost: local Ollama, US$0.

## 8. Decision requested

- **Approve G3** → proceed to Phase 4c (dev runs, then test runs as frozen).
- **Revise** → name the items or checks to redo.
