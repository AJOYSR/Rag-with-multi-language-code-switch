# khullar2025scriptgap — reading notes

**Status:** full-read (v2), 2026-10-23, by AI agent (Claude). Read from the arXiv HTML rendering of v2 (https://arxiv.org/html/2512.10780v2), main text + Appendices A–M. The v2 PDF (22 pages) was downloaded but could not be text-extracted in this environment (no PDF tool), so **page numbers are not given; locations are section / table / figure / appendix labels from the v2 HTML.** Figures (1, 2, 4–9) were not viewable as images; only their captions and any text discussing them were read. Some inline math (e.g., the % columns of Table 1, κ symbols, Eq. 1–3 bodies) did not survive HTML→text extraction and is not reported here.

## 1. Bibliographic metadata (confirmed on official pages, 2026-10-23)

- **Title (v2):** Script Gap: Evaluating LLM Triage on Indian Languages in Native vs Romanized Scripts in a Real World Setting
  - v1 title differs slightly: "... Native vs **Roman** Scripts ..." (arXiv abs v1 page). Semantic Scholar still lists the v1 title.
- **Authors:** Manurag Khullar, Utkarsh Desai, Poorva Malviya, Aman Dalmia, Zheyuan Ryan Shi. Affiliation printed in v2: School of Computing and Information, University of Pittsburgh (marked with ∗ for Khullar and Shi).
- **arXiv id:** 2512.10780 — DOI 10.48550/arXiv.2512.10780. Subjects: cs.CL; cs.LG.
- **Versions** (abs page submission history): v1 Thu 11 Dec 2025 (931 KB); **v2 Mon 30 Mar 2026 (1,080 KB) — latest, the version read.**
- **Venue:** none found. The arXiv abs page has **no Comments and no Journal-ref field** (checked 2026-10-23). Semantic Scholar API lists venue "arXiv.org" only (DBLP key journals/corr/abs-2512-10780, i.e., CoRR). v2 anonymises the partner as "Maternal Health Organization A" with footnote "Anonymized organization name for peer review" (§1) → [INFERENCE] it was under (or prepared for) anonymous review as of v2, but no venue is confirmed. DBLP search returned a bot-check page; not verified there.
- **Licence of the paper:** arXiv.org perpetual non-exclusive license (v2 HTML header).
- URLs: https://arxiv.org/abs/2512.10780 ; https://arxiv.org/html/2512.10780v2 ; https://arxiv.org/pdf/2512.10780v2

Suggested bib entry (to verify again at Phase 6):
```
@misc{khullar2025scriptgap,
  title  = {Script Gap: Evaluating {LLM} Triage on {I}ndian Languages in Native vs Romanized Scripts in a Real World Setting},
  author = {Khullar, Manurag and Desai, Utkarsh and Malviya, Poorva and Dalmia, Aman and Shi, Zheyuan Ryan},
  year   = {2025},
  eprint = {2512.10780}, archivePrefix = {arXiv}, primaryClass = {cs.CL},
  note   = {Version 2, 30 Mar 2026},
  doi    = {10.48550/arXiv.2512.10780}
}
```

## 2. Objective

Quantify how romanization (vs. native script) affects LLM reliability on a real-world, safety-critical task — 3-way maternal/newborn health message **triage** — diagnose where the gap comes from (content vs. orthography; comprehension vs. classification), and propose a mitigation (Abstract; §1 contributions (1)–(4)).

## 3. Data

- **Real-world corpus (real queries: yes).** De-identified WhatsApp messages from a partner maternal-health nonprofit ("Maternal Health Organization A"); ~133k conversations; experiments use a **stratified random sample of 3,153 single-turn user messages** (§2.1).
- **Table 1 counts (native / romanized / total):** English –/–/321; Hindi 158/702/860; Telugu 140/383/523; Kannada 253/210/463; Marathi 253/165/418; Punjabi 129/227/356; Nepali 125/87/212; Total 1,058/1,774/3,153.
- **Native vs romanized in the real-world corpus are DIFFERENT messages from different users**, not paired renderings of the same query (§2.1; implied by §2.3, which introduces the parallel set specifically to "eliminates confounds present in our real world corpus").
- **Labels:** Emergency / Non-emergency / Insufficient Information, human-annotated; 200-message stratified double-annotation: 87.5% agreement, Cohen's κ 0.74 (§2.2; per-language Table 6, App. B: overall κ 0.742).
- **Parallel validation set (paired: yes, but machine-made).** 453 HealthBench "emergency referrals" prompts (physician labels: Emergent / Conditional Emergent / Non-Emergent), translated **by GPT-4o** into native-script and romanized variants for all six languages (§2.3). No mention of human checking of these translations was found in the text read. [INFERENCE] Romanized variants are therefore MT/transliteration outputs, not naturally produced romanization.
- **Bengali: NOT included.** Languages: English (baseline), Hindi, Telugu, Kannada, Marathi, Punjabi, Nepali (§2.1, Table 1). §8 explicitly lists Bengali as absent.
- **Code-mixed:** not a studied condition. Prompts say messages "may include code-mixed content" (App. C, D), but there is no CM variant or CM analysis.
- **Availability / licence of data:** no data or code release statement found in the v2 text (searched for "release", "available", "github", "licen"). Real-world data are from the partner's pilot studies (§9). [INFERENCE] Data appear not to be public; not usable by us.

## 4. Method

- **Task:** 3-way triage classification + brief reasoning; raw messages, no normalisation; single fixed prompt, temperature 0 (§3.1).
- **Models (§3.2):** GPT-4o, Claude Sonnet 4.5; DeepSeek V3, LLaMA-4 Maverick 17B, Qwen3-Next-80B-A3B-Instruct; Mixtral-7B, Qwen2.5-7B, Sarvam-M 24B. (Naming is inconsistent within the paper: §4.1 says "Qwen2-7B" and "Mixtral-8 7B"; §5 RQ2/RQ3 use Qwen3-32B, not in the §3.2 list.)
- **Prompt:** chosen by a 4-way sweep on a held-out 500-message subset of the real-world data (zero-shot, few-shot, Rules+KB CoT, Rules+KB direct); Rules+KB direct selected (§3.3; Table 14, App. L: w-F1 0.767, E-Rec 0.61 for GPT-4o). Full prompts in App. C (real-world) and App. D (HealthBench). [INFERENCE] The 500-message prompt-selection subset is described as "held-out", but it is not stated whether it is excluded from the 3,153 evaluation sample.
- **How native vs romanized pairs are formed:** real-world = different populations/messages (unpaired); HealthBench = same query, GPT-4o-translated into native and romanized (paired) (§2.1, §2.3).
- **Diagnostics (§5):** RQ1 script normalisation (GPT-4o translates romanized→English and romanized→native, then re-triage; Table 3); RQ2 robustness = label flip rate over temperature sweep t ∈ {0, 0.2, 0.4, 0.8, 1} with Qwen3-32B (Eq. 2–3, Fig. 8); RQ3 comprehension vs. triage failure via GPT-5.1 LLM-judge on Qwen3-32B English CoT traces (judge–human agreement 85.8%, κ 0.705 on 100 romanized items, Table 9, App. F; judge prompt App. G); RQ4 comprehension-controlled pairwise analysis on HealthBench (App. K, Table 13).
- **Uncertainty-based Selective Routing (USR) (§6, Fig. 9):**
  - **How "uncertainty" is measured:** it is **not** a numeric confidence score. The uncertainty signal is simply the model's own first-pass prediction of the label **"Insufficient Information"**. Quote (§6 Method): *"Emergency and Non-Emergency predictions are accepted as final as models have high precision on these two labels. Insufficient Information predictions are routed to a second pass with script-aware prompting (SAP)."*
  - Second pass (SAP): within one call, normalise the query "into denoised native script followed by chain-of-thought reasoning to obtain the final triage label" (§6).
  - **Thresholds: none.** There is no tuned threshold, no risk target, no calibration step; routing is a discrete label rule, and it is **the same rule for all scripts and languages** (shared, not per-script) (§6, Fig. 9). [INFERENCE] The paper does separately motivate cross-model disagreement as "epistemic uncertainty" (§4.4, Fig. 6), but that signal is not used in USR as far as the text describes.
  - Evaluated on GPT-4o and Qwen3-80B; ablation SAP-on-all vs USR+SAP (Table 5; per-language Tables 11–12, App. J; cost Table 10, App. I).

## 5. Languages

EN (baseline only), Hindi, Telugu, Kannada, Marathi, Punjabi (native + romanized), Nepali (native + romanized). No Bengali, no Tamil/Gujarati (§8). No controlled code-mixed condition.

## 6. Metrics

Weighted F1 (w-F1) and Emergency recall (§4.1, Fig. 4–5); confusion rates (Table 2); cross-model consensus (§4.4, Fig. 6); flip rate across temperatures (§5 RQ2, Eq. 2–3); share of romanized errors due to comprehension vs triage (Table 4); output tokens / fraction routed (Table 10). **No calibration metric (ECE), no risk–coverage curve, no selective-prediction metrics, no confidence intervals or significance tests** were found in the text read.

## 7. Key findings (with locations and verbatim quotes)

1. **Romanized gap exists, up to 24 points.** Abstract: *"Our results reveal consistent degradation in performance for romanized messages, with gap reaching up to 24 points across languages and models."* §4.1: romanized w-F1 *"drops anywhere from 1 to 8 points below native among the top-tier models on average"*; Sarvam drops ~7 points. §4.2: Nepali largest (often >15, up to 24); Kannada/Telugu *"some models losing 20–30 points in accuracy"* [note: the abstract's 24 vs §4.2's 20–30 are not reconciled in the text].
2. **Gap persists on content-controlled parallel data** (HealthBench): *"romanized w-F1 trails native-script w-F1, with an average drop of 5.4 pp"* (§4.3, Fig. 5).
3. **Romanization pushes models toward "Insufficient Information" — i.e., toward an abstention-like label (over-abstention).** §4.5.1: *"romanization systematically pushes models toward over-predicting Insufficient Information at the expense of both Emergency and Non-Emergency accuracy."* Table 2 (avg of Claude-S4.5, GPT-4o, Qwen3-80B, DeepSeek-V3): NE→II 12.8% native vs 25.2% romanized (EN 20.2%); E→II 11.9% native vs 19.4% romanized. Bigrams in wrong romanized predictions include "message vague", "lacks details" (§4.6). **This is directly relevant to our H1-alt (UNR rises on RBN).**
4. **Normalisation recovers most of the gap; romanized→native beats romanized→English.** Table 3: GPT-4o romanized 75.9 → 78.9 (→English) → 80.1 (→native); Qwen3-80B 70.5 → 77.1 → 78.0; native baselines 78.5 / 78.2. §5 RQ1 Answer: *"normalization of romanized messages into native scripts yields the largest gains, suggesting that native script mapping preserves clinical nuance more faithfully than translation into English"*. Normaliser was GPT-4o itself.
5. **Lower robustness:** romanized inputs show higher temperature flip rates (§5 RQ2, Fig. 8; Qwen3-32B; II label dropped for the real-world set).
6. **Comprehension vs classification depends on resource level** (Table 4): romanized errors that are triage (not comprehension) failures — Hindi 91.8% (HB) / 72.6% (RW); Kannada 30.5% / 19.4%; Telugu 30.9% / 26.1%. §5 RQ3 Answer: *"For lower resource languages such as Kannada and Telugu, romanization causes comprehension failures predominantly"*.
7. **Residual penalty after controlling comprehension:** on comprehension-controlled HealthBench pairs, native 74.8 vs English 74.7 vs romanized 70.9 w-F1 (§5 RQ4; Table 13, n = 1,527 aggregate; Kannada gap 11.2, Marathi 8.9, Punjabi −0.8 i.e. romanized higher). Quote: *"romanized w-F1 reveals a residual +3.8 pp triage penalty attributable solely to script choice"* (§5 RQ4 Answer). [INFERENCE] "attributable solely" is strong given that comprehension is judged by an LLM on a single model's (Qwen3-32B) trace with κ 0.705, and no CI is reported.
8. **The "appear to understand ... fail to act" claim — exact wordings:**
   - Abstract (v2 and v1, identical sentence): *"Our findings highlight a critical safety blind spot in LLM-based health systems: models that appear to understand romanized input may still fail to act on it reliably."*
   - §7 Discussion: *"Models appear to comprehend romanized input, as evidenced by their reasoning traces capturing the user's clinical symptoms, yet still fail to act on that understanding reliably at the triage classification stage."*
   - §1 contribution (3): *"romanized inputs lead to brittle output, even when models seem to generate rationales that capture the user's intent."*
   - Note: v1's abstract stated more strongly *"this performance gap by scripts is not due to a failure in clinical reasoning"*; v2 dropped that sentence and added the comprehension decomposition (Table 4), which shows comprehension failure dominates for Kannada/Telugu. So in v2 the claim holds mainly for higher-resource languages (Hindi, Punjabi).
9. **Mitigation (USR+SAP) results** (Table 5): GPT-4o romanized w-F1 75.9 → 82.5, E-Rec 64.3 → 69.3; Qwen3-80B romanized 70.5 → 76.4, E-Rec 63.9 → 71.5. SAP on all queries hurts GPT-4o emergency recall (60.6→53.9 native, 64.3→51.7 romanized). §6 Insights: *"This makes a strong case that LLMs need to develop intrinsic robustness to script variation in safety-critical classes rather than relying on external normalization pipelines."* Routed fraction: 24% (GPT-4o), 16% (Qwen3-80B) (§6; Table 10).
   - [INFERENCE] Possible internal inconsistency: §6 says output tokens "drop by 76% for GPT-4o and 85% for Qwen3-80B", but Table 10 lists 329K→249K (GPT-4o) and 668K→319K (Qwen3-80B) output tokens, i.e. ~24% and ~52% reductions. Do not cite the token-saving numbers without re-checking against the PDF.
   - USR is evaluated on the real-world set with no separate dev/test split described for the mitigation (§6) — [INFERENCE] design choices (route only II) were motivated by the same data's error analysis ("Based on the findings of research questions and error analysis", §6).
10. **Prevalence:** romanized = 83% (Hindi) and 73% (Telugu) of inputs (§1); 56% of partner messages romanized; "nearly 2 million excess misclassifications" estimate from an average 8.6% penalty (§7).

## 8. Limitations

Stated by authors (§8): language coverage (no Bengali, Tamil, Gujarati, nor non-South-Asian romanization); single domain/task (clinical triage) — *"it remains an open question whether similar degradation patterns hold across other domains and for different tasks."*

Our additional observations [INFERENCE]:
- Real-world native vs romanized sets are unpaired (different users/content); the paired set is GPT-4o-translated with no human validation reported.
- No confidence intervals or significance tests; many comparisons are single-run at t = 0.
- Diagnostic analyses (RQ2–RQ4) use Qwen3-32B, which is not among the benchmarked models; the normaliser (GPT-4o) is also an evaluated model.
- No evidence/retrieval context: the "Insufficient Information" label is about the user message's vagueness, not about whether supplied evidence supports an answer. Not RAG.
- No calibrated confidence scores, thresholds, or risk targets anywhere; nothing on threshold transfer.
- Data and code release not stated.
- Model-naming inconsistencies (§3.2 vs §4.1) and the token-saving inconsistency (§6 vs Table 10).

## 9. How our work differs (exact statement)

Khullar et al. (v2) measure a native-vs-romanized performance gap for **3-way classification of user messages without any supplied evidence**, in **Hindi, Telugu, Kannada, Marathi, Punjabi and Nepali (no Bengali)**, using unpaired real messages plus GPT-4o-translated parallel prompts, and propose a **label-triggered two-pass routing rule (re-process only "Insufficient Information" predictions with script normalisation + CoT)** that has **no confidence score, threshold, or risk target**. Our study instead holds **meaning and oracle evidence fixed** across **human-edited EN / BN / RBN / CM** renderings of the same item, manipulates **evidence sufficiency (sufficient vs. minimally-edited insufficient)** in a **RAG answer-or-abstain** setting, measures **UAR/UNR, selective accuracy and coverage**, and asks whether a **confidence/sufficiency threshold calibrated on English dev data achieves the same target risk on the other variants (RQ2)** — a question Khullar et al. do not pose. We also add a **code-mixed** variant and **Bengali**, both absent from their study.

## 10. Does it answer our RQ2? Implications for RQ1/RQ3/RQ4

- **RQ2 (threshold transfer): NOT answered.** No thresholds, calibration, risk–coverage analysis, or transfer of an operating point across scripts appear in v2 (§3–§6, App. I–L). Novelty threat to RQ2: **low**.
- **RQ1 (H1-alt):** their Table 2 / §4.5.1 finding that romanization raises "Insufficient Information" predictions is prior evidence for **over-abstention on romanized input** in a classification setting. We must cite this as motivating H1-alt and must not present "romanized input increases abstention-like outputs" as a new finding in general; our contribution is measuring it with controlled evidence sufficiency (UNR vs UAR separated).
- **RQ3 (comprehension vs calibration):** their §5 RQ3–RQ4 (Table 4, Table 13) already do a comprehension-controlled decomposition for romanized input (LLM-judge on reasoning traces), finding a residual gap after controlling comprehension. **Moderate overlap** with our RQ3/H3 in spirit; we must cite it, position our probe (paraphrase/translate-to-EN check, per plan §5.3) relative to their trace-judging approach, and claim novelty only for doing it under controlled evidence sufficiency, for Bengali/CM, and for abstention metrics.
- **RQ4 (mitigation):** **Moderate overlap.** Their RQ1 (Table 3) already shows romanized→native normalisation recovers most of the gap and beats →English pivoting, and their SAP normalises to native script. Our intervention (ii) "transliterate RBN→BN before the sufficiency check" and (iii) "pivot-language sufficiency judgment" are therefore **close analogues of their romanized→native and romanized→English normalisation**, but applied to evidence-sufficiency judgment in RAG rather than triage. RQ4 must:
  1. cite Table 3 / §6 as prior evidence that native-script normalisation > English pivot for classification, and test whether this ordering holds for sufficiency judgments;
  2. include a **USR-style baseline adapted to our setting**: route only first-pass abstentions ("insufficient" verdicts) to a second pass with RBN→BN normalisation, and compare against always-normalise and per-variant thresholds **at matched coverage** (their comparison is at fixed label rule, not matched coverage);
  3. report the emergency-recall-style trade-off analogue — their finding that always-normalising can hurt the safety-critical class (Table 5, GPT-4o) — as UAR vs UNR trade-off;
  4. note that per-variant thresholds (our intervention (i)) have no counterpart in their paper.

**Overall novelty threat level:** RQ2 — low; RQ4 — moderate (mitigation (ii)/(iii) partially anticipated for classification; (i) per-variant thresholds and the matched-coverage evaluation are not); RQ1 H1-alt and RQ3 — moderate (must cite as prior evidence).

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
