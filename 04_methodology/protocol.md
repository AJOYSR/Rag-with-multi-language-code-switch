# Experimental and Analysis Protocol: v1.0 (FROZEN 2026-10-24)

**Status: FROZEN on 2026-10-24, approved by the author (Ajoy Sarker).** Drafted by the AI research agent after Gate G2. The hashes are in `04_methodology/protocol_freeze.txt` and git tag `protocol-v1.0`. The design changes come from the G2 decision (`00_admin/decision_log.md`, 2026-10-24).

**Freezing:** the author approves this file, it is committed, and its SHA-256 and the git hash are recorded in §12. **No test-split run may happen before the freeze** (`src/run.py` enforces this through `protocol_frozen_hash`). Any later change is logged in §13 and disclosed in the paper.

---

## 1. Research questions and primary outcomes

| RQ | Question | Primary outcome | Method |
|---|---|---|---|
| RQ1 | With meaning and evidence held fixed, do variants differ in unsupported answering (H1) or unnecessary abstention (H1-alt)? | **UAR** and **UNR**, paired against EN | M1 |
| RQ2 | Does an abstention threshold selected on EN-dev for target risk *r* achieve *r* on each variant in test? | **Realised risk − r** at r = 0.10 (also reported at 0.05 and 0.20) | M3 |
| RQ3 | How much of any gap remains among items the model comprehends? | RQ1/RQ2 gaps restricted to comprehended items | M1, M3 |
| RQ4 | Do cheap interventions reduce the RQ2 violation at matched coverage? | Violation and coverage on test | M3 + interventions (Phase 4d) |

H1 and H1-alt are tested **two-sided**.

## 2. Items

### 2.1 Sources
- **Core:** fictional notices written for this project. Institutions, places and people are fictional, and the author checks each name.
- **Realism subset (secondary):** up to 20 items from Bengali Wikipedia (CC BY-SA 4.0), each with a closed-book filter. Each source is logged in `03_data/raw/SOURCES.csv`. Results are reported separately by source.

### 2.2 Construction rules (new items)
1. Notice length: 150–300 words for new items (pilot items: 60–110 words).
2. **The question names the target institution or event** in every variant.
3. Answer types: number, amount, date, name, yes/no, balanced as far as possible (target: 40 of each).
4. **Insufficient version:** the answer-bearing sentence is replaced by a minimal edit. About half are **deletions** and half are **neutralisations** (for example, "the fee will be announced later"), stored in `edit_type`. Two automatic checks are required: the gold answer is absent from the insufficient passage, and the sibling answer is present. A human then confirms the answer cannot be inferred: the author for all items, and the second annotator on the sample in §6.
5. **Near-miss sibling question:** must be answerable from the insufficient passage.
6. **Distractor context (G2 change 1):** each new item is shown with **2 distractor notices**. They are passages of other items **from the same split**, preferring the same answer type (so values of the same type appear in the context), and they name different institutions. The selection and the position of the target among the three passages are deterministic (seed 20261024), with the target's position balanced across items. The distractors are identical in the sufficient and insufficient conditions.
7. **Pilot items** (P01–P30) keep their single-passage format and are **dev-only**.

### 2.3 Variants
- **EN, BN, RBN, CM, CMR**, as defined in `03_data/variants/RBN_convention.md` (v0.1 plus author rules). This is a 2×2 within Bengali: script {Bengali, Roman} × mixing {monolingual, English insertions}.
- The AI agent may draft variants. **The author reviews and edits every variant.** AI drafting is disclosed.
- Spreadsheets are exchanged as UTF-8, as `REVIEW_INSTRUCTIONS.md` specifies.

## 3. Splits
- Splits are made **by base item**. All variants, conditions and the sibling of an item share its split.
- **Dev:** the 30 pilot items plus 20 new items. **Test:** the remaining new items, about 150.
- New items are assigned with stratification by answer type (seed 20261024) by `src/split.py`, which writes `03_data/splits/{dev,test}.txt`.
- Distractors are drawn only from the item's own split.
- All prompt, combiner, threshold and intervention choices use **dev only**.

## 4. Models and decoding
- `hf.co/bartowski/Qwen_Qwen3.5-9B-GGUF:Q4_K_M` and `hf.co/bartowski/gemma-2-9b-it-GGUF:Q4_K_M` via Ollama 0.40.9. Digests are recorded per run.
- Temperature 0, seed 0, `num_ctx` 8192 (needed for distractors), `think: false`.
- An optional third model (API) is added only with an approved cost estimate and is reported as exploratory.

## 5. Methods (prompts in `05_experiments/src/prompts.py`, version recorded per run)
- **M1, instructed abstention:** answer briefly or output `NOT_ANSWERABLE`.
- **GEN:** answer with no abstention option. Records the answer and its token log-probabilities.
- **SUFF:** sufficiency rater adapted from Joren et al. 2025 (README/FLAMe wording). Score = P("1") from first-token log-probabilities.
- **M3, selective generation:** logistic combiner of [P(suff), mean answer log-prob], **fitted on EN-dev only**. Abstain when the score is below τ.
- **M2b, token confidence:** the mean GEN log-prob alone, used as a threshold baseline.
- **CB, closed-book:** the question only.
- **TR, comprehension probe (G2 change 3):** (a) **with the passage**: "Restate the question in English"; (b) without the passage, as a secondary measure.
- Instructions are in English for every variant. The instruction-language effect is a robustness check (§9).

## 6. Measurement
- **Response category** (`src/normalize.py::outcome`), deterministic and unit-tested:
  - abstain / non-specific / specific / ambiguous;
  - **only "specific" counts as answering**;
  - **ambiguous** cases are adjudicated by the author and logged with the run id. The adjudicator sees the variant; that is unavoidable and is disclosed.
- **Correctness:** deterministic normalisation and alias matching (`match`). The author adjudicates any disagreement flagged in audit.
- **Classifier audit:** a stratified random sample of 100 test responses per model (stratified by variant × sufficiency) is labelled by the author **blind to the automatic label**. Agreement and Cohen's κ are reported. If κ < 0.8, rules are revised on dev and the audit is repeated.
- **Comprehension label (RQ3):**
  - an LLM judge (the other model, cross-judging) decides whether TR(a) has the same meaning as the EN question;
  - the judge is validated against the author's labels on 120 pairs, stratified by variant, and its κ is reported;
  - if κ < 0.7, human labels replace the judge for RQ3.
- **Second-annotator validation (G3):** at least 20% of base items (about 40), stratified by answer type, rated for meaning equivalence (all variants against EN) and naturalness, following `annotation_guidelines.md`. Percent agreement and κ against the author are reported. Items with failed equivalence are revised and re-validated, or dropped.

## 7. Metrics (per model × method × variant; CIs from 2,000 item-level bootstrap resamples)
- **UAR** = P(specific | insufficient)
- **UNR** = P(not specific | sufficient)
- **Selective accuracy** = P(correct | specific, sufficient)
- **Coverage**
- **Risk** = P(error | answered), where an answer on an insufficient item is always an error
- **AURC**; risk–coverage curves; accuracy at matched coverage
- **RQ2 violation** = realised test risk − r, with τ selected on EN-dev as the lowest score threshold whose EN-dev risk is ≤ r (maximum coverage)
- **ECE** for M2b and M3 scores
- Category distribution (abstain / non-specific / specific)
- Near-miss sibling answer rate and accuracy
- Closed-book correct rate

## 8. Statistical analysis
**Confirmatory family A (RQ1), Holm-corrected within the family (8 tests):**
- Contrasts **RBN−EN and CMR−EN** × outcomes {UAR, UNR} × models {Qwen, Gemma}.
- Test: **exact McNemar** on item-level paired outcomes, from M1 on test.
- Effect size: paired difference with an item-bootstrap 95% CI.

**Confirmatory family B (RQ2), Holm-corrected (8 tests):**
- For each model × variant ∈ {BN, RBN, CM, CMR}: one-sided test that realised risk exceeds r = 0.10.
- p-value from an item-bootstrap distribution of the realised risk (proportion of resamples ≤ r).
- Also reported: violation relative to EN's realised risk, with a CI.

**Secondary (not in the confirmatory families; reported with CIs, no claims of significance):**
- BN−EN and CM−EN contrasts.
- **2×2 script × mixing model:** a mixed-effects logistic regression `specific ~ script * mixing + (1 | item)` on BN/RBN/CM/CMR rows, fitted separately for insufficient (UAR) and sufficient (UNR) rows and per model, with statsmodels `BinomialBayesMixedGLM` (variational Bayes; posterior means and 95% credible intervals). GEE logistic regression with exchangeable item clustering is a sensitivity check.
  - *Deviation from the plan:* the plan named a frequentist GLMM (`lme4`), which is unavailable without R. This deviation is disclosed.
- A pooled model across models with `model` as a fixed effect: `specific ~ variant * sufficiency * model + (1 | item)`.
- RQ3: family A and B estimates restricted to items whose TR(a) passes the comprehension label for that model × variant.

**Power:** from the pilot's discordance, about 150 test items detect paired differences of about 7–8 pp at 80% power (α = .05, before Holm correction). Smaller effects may go undetected. The paper reports effect sizes and CIs whatever the outcome.

## 9. Robustness checks (test, pre-specified; reported as secondary)
1. **Instruction paraphrase:** a second, pre-written wording of the M1, SUFF and GEN instructions (`prompts.py`, PARAPHRASE_B).
2. **Sampling:** temperature 0.7 with seeds {1, 2, 3} on a stratified 40-item subset.
3. **RBN spelling variants:** the author writes an alternative natural spelling for 40 items (RBN-alt).
4. **Bengali-language instructions:** the same prompts translated into Bengali by the author, on a 40-item subset.
5. **Quantisation:** the default Ollama tags (NVFP4 / Q4_0) on the 40-item subset.
6. **Sanity check:** EN-only behaviour should qualitatively match Joren et al. (GEN answers on insufficient context; selective generation improves selective accuracy). If it does not, debug before interpreting anything.

## 10. Exclusions
- Items dropped at validation (§6) are excluded before any test run, and their number is reported.
- **Closed-book contamination:**
  - a non-yes/no item answered correctly closed-book by a model in any variant is excluded from that model's UAR analysis;
  - a yes/no item is excluded if it is answered correctly closed-book in at least 4 of 5 variants (guessing baseline 50%);
  - a sensitivity analysis includes all items.
- Empty or truncated responses count as non-answers and are reported.
- Runs that fail (server errors) are resumed. Partial runs are never mixed across model digests.

## 11. Interventions (Phase 4d, tuned on dev, evaluated once on test)
1. Per-variant thresholds selected on that variant's dev items.
2. **Transliteration:** the model transliterates the RBN/CMR question into Bengali script, then runs M3.
3. **Pivot arms:** (a) the model reasons in English over the unchanged input; (b) the question is translated into English first.
4. Baseline: label-triggered normalisation routing in the style of Khullar et al.: if M1 abstains, retry with the transliterated question.

Compared at matched coverage on test.

## 12. Planned figures (generated by `07_figures/*.py`)
1. UAR and UNR by variant × model with CIs (dot plot).
2. The script × mixing 2×2 interaction.
3. Risk–coverage curves by variant (M3, M2b).
4. Target vs realised risk by variant (RQ2).
5. Comprehension-restricted gaps (RQ3).
6. Intervention effects at matched coverage (RQ4).

## 13. Freeze record and deviations
| Date | Version | git hash | SHA-256 | Approved by |
|---|---|---|---|---|
| 2026-10-24 | 1.0 | see git tag `protocol-v1.0` | see `protocol_freeze.txt` | Ajoy Sarker (author) |

Deviations after the freeze: *none yet*.
