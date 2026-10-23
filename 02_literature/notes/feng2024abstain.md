# feng2024abstain — Teaching LLMs to Abstain across Languages via Multilingual Feedback

**Status:** full-read (all 26 pages of the ACL Anthology PDF, incl. appendices A–B and Tables 1–16), 2026-10-23.
**Read by:** AI agent (Claude), from text extracted from the official PDF. Figures 1, 5, 6, 8 and 9 are images. Only their captions and any numbers given in the running text were read, not the plotted values.

## 1. Bibliographic metadata

- **Title:** Teaching LLMs to Abstain across Languages via Multilingual Feedback
- **Authors (all 9, in order, confirmed from the ACL Anthology BibTeX and the PDF title page):** Shangbin Feng, Weijia Shi, Yike Wang, Wenxuan Ding, Orevaoghene Ahia, Shuyue Stella Li, Vidhisha Balachandran, Sunayana Sitaram, Yulia Tsvetkov
- **Affiliations (PDF p. 4125):** University of Washington; The University of Texas at Austin; Microsoft Research
- **Venue:** Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024, main), Miami, Florida, USA, November 2024. Editors: Al-Onaizan, Bansal, Chen. ACL.
- **Pages:** 4125–4150 (BibTeX field and PDF header agree)
- **DOI:** 10.18653/v1/2024.emnlp-main.239
- **Anthology URL:** https://aclanthology.org/2024.emnlp-main.239/ (PDF: https://aclanthology.org/2024.emnlp-main.239.pdf)
- **arXiv:** 2406.15948. The abs page says "Submitted on 22 Jun 2024".
- **Code and data:** https://github.com/BunsenFeng/M-AbstainQA (paper footnote 1, p. 4125)
- **Note on the `M-AbstainQA` name:** the paper text never uses it. It appears only as the GitHub repo name (README title "Multilingual AbstainQA").

BibTeX (fetched from https://aclanthology.org/2024.emnlp-main.239.bib on 2026-10-23):

```bibtex
@inproceedings{feng-etal-2024-teaching,
    title = "Teaching {LLM}s to Abstain across Languages via Multilingual Feedback",
    author = "Feng, Shangbin  and Shi, Weijia  and Wang, Yike  and Ding, Wenxuan  and Ahia, Orevaoghene  and Li, Shuyue Stella  and Balachandran, Vidhisha  and Sitaram, Sunayana  and Tsvetkov, Yulia",
    editor = "Al-Onaizan, Yaser  and Bansal, Mohit  and Chen, Yun-Nung",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-main.239/",
    doi = "10.18653/v1/2024.emnlp-main.239",
    pages = "4125--4150"
}
```

## 2. Objective

The paper first tests whether English-developed abstention methods hold up in other languages, especially low-resource ones. It then proposes a better method: the model abstains by self-reflecting on feedback about its proposed answer, where that feedback is generated in languages related to the question's language.

- Research question, verbatim (§1, p. 4126): *"how to identify knowledge gaps in LLMs and reliably abstain beyond English?"*
- Setting: abstention is **knowledge-based**, meaning parametric knowledge only. Limitations (p. 4133): *"LLMs should abstain when their parametric knowledge is insufficient to provide a correct answer."*
- Task definition (§2, p. 4126): an abstention function f(q, LLM) → {true, false}. The LLM should abstain when it would answer incorrectly, and should not abstain when it can answer correctly.

## 3. Data

- **Main datasets:** Multilingual MMLU (M-MMLU) and Multilingual HellaSwag (M-Hellaswag) from Lai et al. 2023 (Okapi). Both are multiple-choice (§3, p. 4127). *"Originally in English, these QA problems were translated into 26 other languages through machine translation."*
- **Additional dataset:** Belebele (Bandarkar et al. 2023), a multilingual reading-comprehension benchmark (§3 and App. A, Table 5, p. 4141).
- **Splits (§3, p. 4127; App. B, p. 4143):** *"we create random splits with 200 instances for validation and 800 for test, with minor variation across languages due to data availability."* Splits are made per language.
- **Languages (App. B, p. 4143):** 26 languages besides English.
  - **High-resource (8):** ru, de, zh, fr, es, it, nl, vi
  - **Mid-resource (11):** id, ar, hu, ro, da, sk, uk, ca, sr, hr, hi
  - **Low-resource (7):** **bn (Bengali)**, ta, ne, ml, mr, te, kn
  - Resource level follows Lai et al. 2023 pretraining-data frequency.
- **Bengali: YES, native Bengali script only.** Evidence:
  - Bengali is listed as low-resource in App. B: *"7 low-resource languages (Bengali, bn; ..."*
  - It has its own column in Table 1 (p. 4128), Table 4 (p. 4131), Table 10 (p. 4143) and Figures 7 and 9.
  - The repo has `data/mmlu/mmlu_bn.json`, observed in the GitHub API listing on 2026-10-23.
  - The Bengali data is **machine-translated from English** (§3).
- **Romanized or code-mixed input: NO.** Nothing in the paper mentions romanized/transliterated questions, code-mixing or script variation. [INFERENCE: given that the data are MT outputs of Okapi M-MMLU/HellaSwag, the bn items are in Bengali script. The Table 14–16 working examples are all in Chinese script. I did not open `mmlu_bn.json` to check.]
- **Retrieval/RAG:** the main experiments are closed-book. There is one appendix experiment (App. A, Fig. 7) that uses cross-lingual retrieval from English Wikipedia (see §7, F6).
- **Licence:**
  - The paper states none.
  - The GitHub repo has **no licence file**: the GitHub API returned `license: null` on 2026-10-23, and the README has no licence section.
  - The README says M-MMLU and HellaSwag come from `nlp-uoregon/mlmm-evaluation` and Belebele from arXiv 2308.16884. The upstream licences were not checked in this session.
  - [REC] Treat M-AbstainQA as "no explicit licence, so reuse/redistribution rights unclear" for Q5. Check the upstream mlmm-evaluation/Okapi and Belebele licences separately.

## 4. Method

**Proposed method, three steps (§2, pp. 4126–4127):**

1. The LLM proposes an answer, a = LLM(q).
2. The LLM generates k feedback paragraphs on that answer, each in language ℓi, with the prompt: *"Please review the proposed answer and provide a paragraph of feedback on its correctness. Feedback should be in ℓi."*
3. The LLM decides, with the prompt: *"Based on the feedback, is the proposed answer True or False?"* It abstains if the answer is judged False.

**How feedback languages are chosen (§2, p. 4127):**

- MONO-NATIVE: all feedback in the question's language.
- MONO-ENGLISH: all feedback in English.
- MULTI-RANDOM: random languages, as a control.
- MULTI-RELATED, the proposed method: the k nearest languages under Lang2vec, averaged over six attributes (syntactic, geographic, phonological, genetic, inventory, featural). Default k = 3.
- For bn, the default related languages are Hindi, Telugu and Nepali (Table 11, p. 4145).

**Baselines (§3, p. 4127; details in Feng et al. 2024 "Don't hallucinate, abstain"):**

- Calibration: PROBS (token probabilities), TEMP, ASK CALI.
- Training: INSTRUCT
- Prompting: REFLECT, MORE INFO, BACKTRANS.
- Consistency: SC THRES., CONFLICT

**BACKTRANS, the baseline closest to our RQ2 (App. B, p. 4143):** *"we translate the question to English and make an abstain decision in English, then use that abstain decision for other languages."* This transfers an abstention **decision** made on the English translation. It is not a threshold transfer.

**Thresholds and calibration:**

- The paper does not describe how thresholds for PROBS, TEMP or SC THRES. are chosen. It refers readers to Feng et al. 2024 (App. B).
- From the released code (not the paper), observed 2026-10-23:
  - `approach-probability.py` and `approach-scthreshold.py` load `data/<dataset>/<dataset>_<lang>.json` and grid-search a threshold on that file's `dev` split.
  - `approach-probability.py` also caps the dev abstain rate below 50%.
  - The threshold is then applied to the same language's `test` split.
  - [INFERENCE] So the threshold baselines are **tuned per language on in-language dev data**. Thresholds are not transferred across languages.
- The proposed MULTI-RELATED method makes a binary decision with no threshold.
- App. A reports AbstainECE (Table 6), computed from the probability of the True/False decision token. Nothing is calibrated in one language and evaluated in another.

**Models and decoding (§3; App. B):**

- Aya-13B (`CohereForAI/aya-101`)
- GPT-4 (Azure "gpt4")
- ChatGPT (`GPT-3.5-TURBO-INSTRUCT`)
- Decoding: greedy for QA and abstention decisions; temperature 0.7 for repeated sampling and feedback.

## 5. Languages

English plus 26 others (see §3). The study includes Bengali in native script only. It has no romanized, transliterated or code-mixed conditions.

## 6. Metrics

- **Main metric:** Abstain Accuracy (A-Acc) = (TP+TN)/(TP+FP+TN+FN), where TP means "should abstain and did" (§3, p. 4128).
- **Appendix metrics:**
  - Reliable Accuracy and Effective Reliability (Table 9, p. 4143)
  - AbstainECE (Table 6)
  - FP/FN rates (Fig. 8)
- **Fairness metrics (§5, Table 2, p. 4129):**
  - Demographic utility M1 and linguistic utility M0, following Song et al. 2023 (GlobalBench)
  - Gini coefficient G as an equity measure
- **Not reported:** no risk–coverage or selective-risk-at-coverage curves, and no confidence intervals or significance tests. The only variability measures are the run-to-run SD over three runs (App. A, "Standard Deviation") and the decision-consistency counts (Table 10).

## 7. Key findings (with locations)

**F1. English-developed abstention methods degrade in low-resource languages.**
- Abstract (p. 4125): *"directly applying these solutions beyond English results in up to 20.5% performance gaps between high and low-resource languages"*
- Fig. 1 caption: *"Existing abstain strategies drop by 8.4% on average when applied to QA in low-resource languages."*
- §4 (pp. 4128–4129): ASK CALI. drops 0.613 → 0.486 on MMLU with Aya-13B, and *"collapses and repeatedly generate the same number (e.g., 0.8) for almost all questions in low-resource languages."* Other drops: Instruction Tuning 35.3%, Self-Reflect 33.3%, SCthreshold 12.2%. MULTI-RELATED drops 8.5%.

**F2. MULTI-RELATED gives the best low-resource average in every model × dataset setting.**
- §4, p. 4128: *"improving over the strongest baseline by 4.9% on average"*
- Abstract: up to 9.2% improvement.
- Bengali values (Table 1, p. 4128), MULTI-RELATED, bn column: Aya-13B M-MMLU .621; GPT-4 M-MMLU .752; Aya-13B M-Hellaswag .468; GPT-4 M-Hellaswag .532.
  - Note that MULTI-RELATED is **not** the best method for bn on Hellaswag. With Aya-13B, TEMP has .610 and PROBS .597 on bn Hellaswag, against MULTI-RELATED's .468. (Bold and underline styling was lost in text extraction. These are the raw values.)

**F3. Abstention is language-specific.**
- §4, p. 4129: *"there is no one-size-fits-all solution for abstaining across multilingual contexts and robust strategies should be language-specific."* Tamil and Malayalam were hardest (0.484 and 0.492, against a low-resource average of 0.520).
- Conclusion, p. 4133: *"abstention is a language-specific problem"*

**F4. Abstention decisions transfer only partly across languages. This is the finding closest to our RQ2.**
- §5, p. 4131: *"One solution to multilingual abstain is to take the highest-resource language (e.g., English), make abstain decisions, and use that decision to abstain/generate in low-resource languages. However, to what extent do abstain decisions overlap across languages and thus transferable remains underexplored"*
- Results, from overlap on parallel questions:
  - three related languages: 74.5% "2+ overlap"
  - three unrelated languages: 48.1%
  - three high-resource languages: 70.5%
  - three low-resource languages: 48.4%
- Conclusion (p. 4131): *"abstain decisions are only somewhat transferable in the case of high-resource closely related languages"* and *"English-only abstain methods are not one-size-fit-all solutions"*
- App. A repeats the analysis with a consensus definition (p. 4143), with the same direction of results.

**F5. Using a different model for feedback helps low-resource languages.**
- Table 4, p. 4131: GPT-4 answers and Aya-13B generates feedback. This gives *"a 5.4% improvement on average"* for low-resource languages.
- bn: .752 → .788 (§5, p. 4132).

**F6. Cross-lingual retrieval setting (the only RAG-like experiment).**
- App. A, p. 4141: *"we use English Wikipedia for retrieval and prepend back-translated paragraphs before the query from the seven low-resource languages"*
- With ChatGPT, MULTI-RELATED beats the baselines on 6 of the 7 low-resource languages, by 6.9% on average (Fig. 7).
- Retrieval is uncontrolled (WikiSearch API). Evidence sufficiency is neither manipulated nor labelled.

**F7. Low-resource languages show more over-abstention.**
- App. A, p. 4141: *"for low-resource languages, LLMs tend to be more 'conservative' and the FP is usually higher."*
- Here FP means the model abstained although it could have answered correctly, which corresponds to our UNR. The authors call this *"desirable"*.
- [INFERENCE] This is relevant to our H1-alt (over-abstention on less-understood variants), though it is about languages, not scripts.

**F8. Abstention performance and QA accuracy are separate.**
- App. A, p. 4141: *"there is no lock-step synchronization between the two metrics, indicating that abstaining is an independent problem to question answering"*
- Source: Fig. 9.

**F9. The method is not best on reading comprehension.**
- Belebele (Table 5, p. 4141): MULTI-RELATED is best on low-resource languages (0.6386) but behind the strongest baselines on high and mid (e.g., SC THRES. 0.8136 high).
- Authors' conclusion: *"This motivates using different methodologies for abstention in different language contexts."*

**F10. Culture matters.**
- Table 3 (p. 4131): selecting related languages by culture (World Value Survey clusters) gives the best low-resource average and equity (Avg-L 0.5322, G 0.0438).
- §5: the largest high/low-resource gaps are in West-centric MMLU domains.

## 8. Limitations

**Stated by the authors (Limitations, p. 4133):**
- Scope is knowledge-based abstention only. Safety abstention is not covered.
- Sampled feedback adds randomness.
- Inference cost is higher than simple prompting.

**Observed by us [INFERENCE / our assessment]:**
- All non-English data are machine translations of English MCQ benchmarks. The paper reports no human check of translation quality.
- Every task is multiple-choice. The README says non-MC datasets are left to future work.
- "Should abstain" is defined by whether the model's own answer is correct. No evidence condition is manipulated, so the ground truth for abstention depends on the model and is not fixed per item.
- No confidence intervals or significance tests are reported for the method comparisons.
- Romanized and code-mixed inputs are absent. Variation is only *across languages*, never *across scripts of one language*.
- The cross-language transfer analysis (F4) measures the *overlap of decisions* across languages. It does not measure whether a calibrated operating point (threshold, target risk, coverage) holds.
- Figures 5, 6, 8 and 9 were read only from captions and running text here.

## 9. How our work differs (exact statement)

Feng et al. (2024) study **knowledge-based, closed-book** abstention on **machine-translated multiple-choice** QA (M-MMLU, M-HellaSwag, Belebele) in 26 languages besides English, including **native-script Bengali**. Their ground truth for "should abstain" is whether **the model's own answer** is correct. They show that English-developed abstention methods degrade in low-resource languages. They propose multilingual self-feedback, and report that abstention **decisions** on parallel questions overlap only partly across languages.

Our study differs in four ways:

1. **Variation axis.** We vary **script and code-mixing within one language**: EN vs. native-script Bengali (BN) vs. romanized Bengali (RBN) vs. Bengali–English code-mixed (CM), all on human-edited, meaning-validated variants of the same item. Feng et al. vary only **across languages**, using MT data, and never include romanized or code-mixed input.
2. **Ground truth for abstention.** We use **controlled oracle evidence** (sufficient vs. minimally edited insufficient passage), so "should abstain" is defined by the item and not by the model. Feng et al. are closed-book, apart from one uncontrolled English-Wikipedia retrieval appendix.
3. **Transfer of operating points (RQ2).** We test whether a **threshold selected on English dev data** to meet a target risk keeps that risk and coverage on BN, RBN and CM test data. Feng et al. tune threshold baselines **per language on in-language dev data**. This is visible in their released code; the paper text does not describe the procedure. They evaluate only the overlap of binary decisions (F4) and a translate-to-English decision transfer baseline (BACKTRANS). They report no risk–coverage or threshold-transfer analysis.
4. **Diagnosis.** We separate comprehension failure from miscalibration (RQ3), using a free-form short-answer RAG task rather than MCQ.

## 10. Does this paper already answer our RQ2?

**No. It answers a related but weaker question, and we must cite it as the closest evidence.**

- **What it does answer.** Whether abstention *decisions* made in one language coincide with decisions on the parallel question in another language. They mostly do not for unrelated or low-resource languages (§5, p. 4131): *"abstain decisions are only somewhat transferable in the case of high-resource closely related languages"*. The BACKTRANS baseline, which translates to English and transfers the English decision (App. B, p. 4143), does worse than MULTI-RELATED on low-resource Avg-L in all four Table 1 settings, e.g. Aya-13B M-MMLU .390 vs .635.
- **What it does not answer.**
  - Whether a confidence or sufficiency **threshold calibrated** in English (or any language) meets a **target risk/coverage** in another language or script.
  - Thresholds in their baselines are tuned per language on that language's dev split (repo code, see §4). No experiment holds an English-tuned threshold fixed and measures realised risk elsewhere.
  - Nothing is said about romanized or code-mixed forms of the same language, or about evidence-sufficiency abstention in RAG.
- [REC] In our paper:
  - Present F4 as prior evidence that abstention behaviour is language-dependent.
  - Frame RQ2 as moving from decision overlap across languages to **operating-point transfer across scripts of one language under controlled evidence**.
  - Do **not** claim to be the first to study multilingual abstention. Feng et al. call themselves *"the first study on multilingual LLM abstention"* (§1, p. 4126; also §6, p. 4133).

## 11. Verbatim quotes for spot-checking (PDF page = proceedings page)

1. p. 4125, Abstract: "directly applying these solutions beyond English results in up to 20.5% performance gaps between high and low-resource languages"
2. p. 4126, §1: "we present the first study on multilingual LLM abstention"
3. p. 4127, §3: "Originally in English, these QA problems were translated into 26 other languages through machine translation."
4. p. 4129, §4: "there is no one-size-fits-all solution for abstaining across multilingual contexts and robust strategies should be language-specific."
5. p. 4131, §5: "abstain decisions are only somewhat transferable in the case of high-resource closely related languages"
6. p. 4141, App. A: "for low-resource languages, LLMs tend to be more “conservative” and the FP is usually higher."
7. p. 4143, App. B: "we translate the question to English and make an abstain decision in English, then use that abstain decision for other languages."
8. p. 4133, Limitations: "LLMs should abstain when their parametric knowledge is insufficient to provide a correct answer."

## 12. Inaccessible or unchecked

- Plotted values inside Figures 1, 5, 6, 8 and 9 (images). Only captions and in-text numbers were read.
- Upstream dataset licences (mlmm-evaluation/Okapi, Belebele) were not checked.
- Contents of `mmlu_bn.json` (script, item count) were not opened.
- The baseline threshold procedures are described only in Feng et al. 2024 ("Don't hallucinate, abstain", arXiv 2402.00367), which was not read in this session. The per-language tuning claim rests on this paper's released code only.

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
