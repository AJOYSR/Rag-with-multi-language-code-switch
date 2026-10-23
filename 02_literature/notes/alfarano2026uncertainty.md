# alfarano2026uncertainty — reading notes

**Status:** full-read (v3), 2026-10-23, by AI agent (Claude). Read from the arXiv v3 PDF (18 pages, text extracted with pypdf), covering main text, references and Appendices A–M. Figures 3, 6 and 7 were also viewed as images from the arXiv HTML rendering (https://arxiv.org/html/2607.06327v3/img/…). Figures 1, 2, 4, 5 and 8–10 were **not** viewed; only their captions and the text discussing them were read. Page numbers below are PDF pages (p.1–18).

## 1. Bibliographic metadata (checked on the arXiv abs page, 2026-10-23)

- **Title:** Estimating Uncertainty from Reasoning: A Large-Scale Study of Multi- and Crosslingual MCQA Performance in LLMs
- **Authors:** Andrea Alfarano, Andrea Bacciu, Saab Mansour, Amin Mantrach, Marcello Federico. Amazon. Alfarano and Bacciu share equal contribution, and Alfarano's work was done during an internship (p.1 footnotes).
- **arXiv:** 2607.06327, DOI 10.48550/arXiv.2607.06327. Versions: v1 7 Jul 2026, v2 10 Jul 2026, **v3 4 Sep 2026 (read)**.
- **Venue:** the arXiv Comments field says "Accepted at Findings of EMNLP 2026". **Not verified on ACL Anthology.** Re-check the Anthology entry and page numbers at Phase 6.

```
@misc{alfarano2026uncertainty,
  title  = {Estimating Uncertainty from Reasoning: A Large-Scale Study of Multi- and Crosslingual {MCQA} Performance in {LLMs}},
  author = {Alfarano, Andrea and Bacciu, Andrea and Mansour, Saab and Mantrach, Amin and Federico, Marcello},
  year   = {2026}, eprint = {2607.06327}, archivePrefix = {arXiv}, primaryClass = {cs.CL},
  note   = {v3, 4 Sep 2026. arXiv comment: Accepted at Findings of EMNLP 2026 (Anthology entry not yet verified)},
  doi    = {10.48550/arXiv.2607.06327}
}
```

## 2. Objective

The paper evaluates nine uncertainty-estimation (UE) methods across 22 languages. Uncertainty is computed on **chain-of-thought reasoning text** produced before an MCQA answer, and correctness comes from exact-match MCQA labels, so no LLM judge is needed (Abstract; §1; §3). It poses five research questions (§1, p.2):
- RQ1: which UE methods are robust;
- RQ2: the effect of scale;
- RQ3: the effect of reasoning language;
- RQ4: cross-lingual answer options;
- RQ5: threshold selection for selective prediction.

## 3. Data

- **Global-MMLU** (4 options) and **MMLU-ProX** (10 options). Both are parallel and human-curated. The authors sample 100 questions per category, which gives 600 + 1,400 = 2,000 questions. Across 22 languages that is 44,000 instances (§3, p.3).
- **Task type:** closed-book knowledge MCQA. **There is no passage, no retrieval evidence and no sufficient/insufficient-evidence manipulation.** The "abstention" is selective prediction on the model's own possibly wrong answer.
- **Languages (App. C, p.14):** ar, **bn**, cs, de, en, es, fr, hi, id, it, ja, ko, ne, pt, ru, sr, sw, te, uk, vi, yo, zh.
  - **Bengali is included, in native script only** (the Global-MMLU / MMLU-ProX bn release).
  - **There is no romanized and no code-mixed condition anywhere.** The term "cross-lingual" refers to answer options drawn from different languages (§4 RQ4). It is not a script variation.
- Contamination caveat: the data are MMLU-derived, and the authors acknowledge this (§6, App. M).

## 4. Method

- **Models:** Gemma3 0.27B/1B/4B/12B/27B, Qwen3 4B/30B-A3B/235B-A22B (235B at 4-bit), and Claude Sonnet 4.5 (§3, p.4). The quantisation check in App. G found no significant effect for Qwen3-30B at 8-bit or 4-bit.
- **UE methods** (§3; App. A), all run through LM-Polygraph:
  - open-box: Token Entropy, Max Prob, Self Certainty;
  - closed-box: Self-Verbalized confidence (a follow-up prompt asking for P(correct), App. D.2), Lexical Similarity (ROUGE-L), and Semantic Entropy, EigValLaplacian, DegMat and Eccentricity, all with **Jaccard** similarity rather than NLI.
- **Reasoning-language manipulation (RQ3, §4 p.6):** in the "Multilingual" condition, the model reasons in the question language. In the "English Reasoning" condition, the question and options stay in the target language and the model reasons in English. **The input is not translated.**
- **Cross-lingual setting (RQ4, §4 p.7):** the question and reasoning are in the target language, and each answer option comes from a different language.
- **Threshold selection (RQ5, §4 p.7):** accept a prediction if u < t. The threshold t is chosen **by maximising F1 for error detection** on validation data. Three strategies are compared:
  1. t_EN: tuned on English only and applied to all languages;
  2. t_GLOBAL: tuned on pooled multilingual data;
  3. t_LANG: per-language thresholds.
  
  Validation and test are **different datasets** ("one dataset as validation set … the other as test set"). RQ5 uses only **Claude Sonnet 4.5 + Self-Verbalized**, and an Oracle condition (tuned on test) is included.
  - **Yes, a threshold chosen in English is applied to other languages.** However, the selection criterion is F1, not a target risk level.

## 5. Metrics and statistics

- The main metric is AUROC for error detection, with DeLong tests (paired or unpaired) and BH-FDR correction across languages (§3; App. L).
- RQ3 uses paired bootstrap, and accuracy is compared with McNemar tests (App. F, M).
- RQ5 reports a pooled confusion matrix (Acc over accepted, TP/FP/TN/FN as % of samples; Table 1, p.9).
- ECE appears in App. K (figure not viewed).
- **There are no risk–coverage curves and no realised-risk-versus-target-risk analysis.**

## 6. Key findings (with locations)

1. **Method ranking (RQ1, Fig. 3, p.4–5):** Self-Verbalized has the highest mean AUROC (0.72), followed by Token Entropy (0.71) and Self Certainty (0.70). Sampling methods collapse on low-resource languages.
   - Quote: "Sampling-based methods maintain reasonable performance on high-resource languages but fail on low-resource ones" (p.5).
   - The cause is diversity of reasoning traces: "For low-resource languages, this gap collapses to ≤0.03: Yoruba (0.93 vs. 0.93), Swahili (0.93 vs. 0.92), Bengali (0.83 vs. 0.80)" (p.5).
2. **Scale (RQ2, §4 p.5–6; App. L Tables 5–6):** Self-Verbalized rises from 0.65 to 0.66 to 0.77 AUROC (Qwen3 4B → 30B → 235B). At 30B, Token Entropy beats Self-Verbalized in 19 of 22 languages. At 235B the ranking reverses (Wilcoxon, App. L, p.17). The authors note that distillation within Qwen3 may confound this comparison (p.6).
3. **Reasoning language (RQ3, Fig. 6, p.6–7):** "On average, English reasoning improves UE quality (0.72 vs. 0.68 AUROC). Crucially, this improvement is driven by low-resource languages" (p.6).
   - Their argument: "If comprehension were the bottleneck, changing the reasoning language would not help: the model would not know what to reason about" (p.6).
   - Their conclusion: "models comprehend low-resource questions adequately but struggle to generate coherent reasoning in those languages" (p.6–7).
4. **Cross-lingual options (RQ4, Fig. 7, p.7):** "AUROC remains stable (0.68 vs. 0.67)". Accuracy falls by 4–6 points in this setting (App. F, p.15).
5. **Thresholds (RQ5, Table 1, p.7–9):**

   | Strategy | Acc over accepted | Error-rate reduction | Correct predictions filtered (FN) |
   |---|---|---|---|
   | No filter | 86.5 | — | — |
   | t_EN | 91.2 | 43% (from 13.5% to 7.7%) | 6.6% |
   | t_GLOBAL | 92.4 | 56% | 13.5% |
   | t_LANG | 93.0 | 60% | 14.4% |
   | Oracle | 93.4 | 62% | 14.4% |

   - Quote: "English-only calibration (tEN) offers the most practical entry point" (p.7).
   - Quote: "threshold calibration transfers across datasets but benefits from language awareness" (§5, p.9).
   - **Table 1 is pooled over all 22 languages and two datasets. No per-language accepted-error or realised-risk numbers are reported**, so this result says nothing about whether t_EN under- or over-shoots for Bengali specifically.
   - [INFERENCE] The caption says values are "percentages of the 44,000 samples, averaged across the two datasets", which seems to conflict with one dataset being used only for validation. The exact test pool is unclear.

### How strong is the "comprehension intact / generation bottleneck" claim?

The evidence is (a) the RQ3 AUROC gain under English reasoning with the question still in the target language (Fig. 6), and (b) two controls (p.7):
- Self-Verbalized alone improves "AUROC 0.665 → 0.679, paired bootstrap p < 0.001";
- on the 88.4% of questions answered identically under both conditions, AUROC goes 0.670 → 0.684.

My assessment:
- **[INFERENCE] The evidence is indirect, and the paper words it more strongly than the evidence supports.** No comprehension probe was run (no paraphrase, translation or entailment check). "Comprehension largely intact" is inferred from the fact that a generation-side manipulation helps.
- The control effect sizes are small: about +0.014 AUROC. The headline average gap of 0.68 vs 0.72 averages across all UE methods, including the Jaccard-based methods the authors themselves say are language-sensitive.
- The argument "if comprehension were the bottleneck … would not help" assumes comprehension is all-or-nothing. Partial comprehension could still limit performance while English generation helps.
- English reasoning also raises **accuracy** (BN 0.697 → 0.738, Table 2, p.15), which shows that target-language reasoning was losing information.
- The abstract's word "suggesting" is appropriately hedged. The Conclusion's "indicating that the reliability bottleneck lies in generation rather than comprehension" (p.9) is stronger.
- All evidence comes from native-script, closed-book MCQA with MMLU-derived items.

## 7. Bengali-specific results

| Result | Location | Value |
|---|---|---|
| UE AUROC, averaged over methods and models | Fig. 3 (image) | bn 0.64 (en 0.71). Self-Verbalized 0.72, Token Entropy 0.68, Semantic Entropy 0.60, Eccentricity 0.60 |
| Reasoning-trace diversity, incorrect vs correct | p.5 | 0.83 vs 0.80 |
| Native vs English reasoning AUROC (Indic group) | Fig. 6 (image) | 0.66 → 0.71 (en 0.72) |
| Cross-lingual options AUROC | Fig. 7 (image) | 0.65 vs 0.65 |
| Accuracy, native vs English reasoning | Table 2, p.15 | 0.697 → 0.738 (+5.8% rel., p < 0.001) |
| Self-Verbalized AUROC, Global-MMLU, Qwen3-235B vs 30B | Table 5, p.17 | 0.710 vs 0.582 |
| Token Entropy vs Self-Verbalized AUROC, Qwen3-30B | Table 6, p.17 | 0.645 vs 0.582 (p_BH = 0.03) |

- Figure values were read off the published bar and heatmap labels.
- **No Bengali-specific threshold-transfer result is reported** (RQ5 is pooled).

## 8. Limitations

Stated by the authors (§6, p.9):
- only two MCQA datasets;
- no training-based UE methods;
- possible MMLU contamination for high-resource languages.

My additions:
- [INFERENCE] There is no evidence-grounded (RAG) setting, so "unanswerable from the evidence" is never tested.
- [INFERENCE] There are no script or romanization variants.
- [INFERENCE] The RQ5 threshold analysis is pooled across languages, uses a single model and method, and uses an F1 criterion rather than a target risk.
- [INFERENCE] There are no per-language risk–coverage results.
- [INFERENCE] The Jaccard-based consistency methods are confounded with script and tokenisation, as the authors partly acknowledge (§5).

## 9. How our work differs

- **Construct.** We test abstention when the **supplied evidence is sufficient or insufficient** (controlled minimal edits) in RAG. They test the correctness of closed-book MCQA knowledge.
- **Script axis.** We use BN / **RBN / CM** renderings of the same item. They use only native-script parallel translations. Romanized Bengali and code-mixed input are absent from their study.
- **RQ2.** We select a threshold on EN-dev for a **target risk r** and measure **realised risk per variant** on test. Their t_EN is selected by F1, reported pooled across 22 languages, and transferred across datasets. Their result is that t_EN gives a 43% error reduction versus 60% for t_LANG. **It does not answer whether the realised risk for any single language matches the English target.**
- **H3 (comprehension vs calibration).** We test this directly by restricting to items the model is verified to comprehend. Their claim is inferred from a reasoning-language manipulation, with no comprehension check.

## 10. Does it pre-empt or contradict us?

- **RQ2: partially overlaps, but does not answer it.** The paper does contain English-tuned → all-language threshold transfer (t_EN). That result is pooled, uses a single model, is closed-book, does not separate Bengali, and has no RBN or CM input. **We must cite it and must not claim to be the first to test English-to-other-language threshold transfer.** We can still say our study tests *risk-targeted* transfer *per script variant* under *evidence insufficiency*. [INFERENCE] The gap between t_EN and t_LANG in their Table 1 (43% vs 60% error reduction) is prior evidence consistent with English thresholds being suboptimal for other languages, which motivates RQ2.
- **H3: no contradiction, and broadly consistent.** Their view is that the bottleneck lies in generation or confidence rather than comprehension. H3 predicts that a gap remains after controlling for comprehension, attributable to calibration. Their evidence supports "the gap is not mainly comprehension" for native-script low-resource MCQA. [INFERENCE] It does not show the comprehension share is zero. For romanized and code-mixed Bengali, comprehension may play a larger role, which their data cannot speak to.
- **RQ4(iii) pivot-language sufficiency judgment: partially pre-empted in spirit.** Their "English Reasoning" condition (input unchanged, reasoning in English) is close to a pivot-language judgment, and it closed most of the UE gap for bn (0.66 → 0.71). Our intervention (iii) is therefore **expected to help, and it is not novel as a general idea.** What would be new:
  - applying it to *sufficiency* judgments rather than answer confidence;
  - applying it to RBN and CM input;
  - measuring it as realised risk and coverage.
  
  [REC] Implement (iii) in two arms, defined in the protocol before any data are seen:
  - (iii-a) input unchanged, judge reasons in English (mirrors Alfarano et al.);
  - (iii-b) input translated or transliterated to English or BN, then judged.

## 11. Recommended framing

[REC] Cite this paper as the closest multilingual-UE work. Describe it as "closed-book MCQA, native script; English-reasoning narrows UE gaps; English-tuned thresholds transfer with reduced error reduction relative to per-language thresholds (pooled)". Position our contribution as:
1. evidence-sufficiency abstention under controlled oracle evidence;
2. a script/register axis (RBN, CM) on identical items;
3. per-variant realised risk at a target risk level;
4. a direct comprehension control for H3, rather than one inferred from a reasoning-language manipulation.

Treat their generation-bottleneck claim as a [HYPOTHESIS] that our H3 analysis tests in a different setting, not as established fact.

---
**Quote verification (lead, 2026-10-23):** verbatim quotes string-matched against the arXiv PDF text (pypdf); unmatched strings were checked by hand and were PDF-extraction artefacts (footnote/table markers inside sentences), labels/paraphrases, or quotes from the GitHub README rather than the paper. Status: full-read.
