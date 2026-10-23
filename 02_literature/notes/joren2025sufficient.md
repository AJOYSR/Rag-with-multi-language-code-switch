# joren2025sufficient — Reading notes

**Status:** full-read (arXiv v3, HTML rendering, main text + all appendices A–D), 2026-10-23.
**Reader:** AI research agent (Claude), session of 2026-10-23. Not yet spot-checked by the author.

Label conventions follow CLAUDE.md: [FACT] = read in the source this session; [INFERENCE] = my reading/derivation, not stated by the authors; [REC] = recommendation for our project.

---

## 1. Bibliographic metadata (as confirmed)

| Field | Value | Confirmed on |
|---|---|---|
| Title | Sufficient Context: A New Lens on Retrieval Augmented Generation Systems | arXiv abs page; ICLR proceedings page; OpenReview |
| Authors (order) | Hailey Joren, Jianyi Zhang, Chun-Sung Ferng, Da-Cheng Juan, Ankur Taly, Cyrus Rashtchian | arXiv abs page (`citation_author` metadata); ICLR proceedings page; OpenReview note `Jjr2Odj8DJ` |
| Venue | International Conference on Learning Representations 2025 (ICLR 2025), Conference track; OpenReview lists it as "ICLR 2025 Poster" | https://proceedings.iclr.cc/paper_files/paper/2025/hash/33dffa2e3d2ab74a783d1a8c292f66d9-Abstract-Conference.html ; https://openreview.net/forum?id=Jjr2Odj8DJ (via OpenReview API, venueid `ICLR.cc/2025/Conference`) |
| Year | 2025 (arXiv v1 dated 9 Nov 2024) | as above |
| arXiv | 2411.06037 [cs.CL]; v1 9 Nov 2024, v2 7 Dec 2024, v3 23 Apr 2025 | https://arxiv.org/abs/2411.06037 (submission history) |
| Version read | **v3** (23 Apr 2025), HTML at https://arxiv.org/html/2411.06037 (page header reads "arXiv:2411.06037v3 [cs.CL] 23 Apr 2025") | — |
| Paper licence (arXiv) | CC BY 4.0 (stated in the arXiv HTML header) | arXiv HTML |
| Affiliations | Joren: UC San Diego; Zhang: Duke University (both "Work done during an internship at Google"); others: Google | arXiv HTML title block |

Not verified: page numbers in the ICLR camera-ready PDF. I read the arXiv v3 HTML, which has no pagination, and could not extract text from the PDF in this environment (no PDF text tool available). **All locations below are section / table / figure / appendix references in arXiv v3, not page numbers.** I did not compare v3 against the ICLR proceedings PDF; minor differences are possible.

Suggested BibTeX (fields confirmed above; the repo README gives the same key, `joren2025sufficient`):
```
@inproceedings{joren2025sufficient,
  title     = {Sufficient Context: A New Lens on Retrieval Augmented Generation Systems},
  author    = {Joren, Hailey and Zhang, Jianyi and Ferng, Chun-Sung and Juan, Da-Cheng and Taly, Ankur and Rashtchian, Cyrus},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2025},
  url       = {https://openreview.net/forum?id=Jjr2Odj8DJ}
}
```
Note: the repo README's BibTeX title uses "Retrieval-Augmented" (hyphenated); the arXiv and proceedings titles have no hyphen. Use the proceedings form.

---

## 2. Objective

[FACT] The paper asks "whether errors arise because LLMs fail to utilize the context from retrieval or the context itself is insufficient to answer the query" (Abstract). Its three stated contributions (§1, contribution list) are: (1) a definition of sufficient context plus an autorater; (2) an analysis of model responses stratified by sufficiency; (3) a selective-generation method "using both confidence and sufficient context signals".

---

## 3. Data (datasets, languages)

[FACT]
- **Autorater evaluation set:** 115 human-labelled (query, context; answer) instances sampled from PopQA, FreshQA, Natural Questions and EntityQuestions; designed "to be very challenging", single- and multi-hop, often with entity overlap between question and an insufficient context (§3.2, "Sufficient Context Labeled Dataset"). Gold labels were built from (query, context) only: "We did not use ground truth answers or model responses." Annotators are thanked in Acknowledgments (four named people); no inter-annotator agreement statistic is reported in v3.
- **Analysis datasets (§4.1, App. A.3):**
  - FreshQA "True Premise" setting, 452 instances; context = scraped pages from the dataset's URLs (App. A.3 "Retrieval for FreshQA").
  - Musique-Ans: 500 random instances from dev; context = the 20 supporting snippets provided by the dataset.
  - HotPotQA: 500 random instances from dev; top-5 retrieved snippets. §4.1 says retrieval was "via REPLUG ... from FlashRAG"; App. A.3 says the corpus is wiki-18 with `intfloat/e5-base-v2` dense retriever, top-5, and that REPLUG was "also" evaluated. [INFERENCE] The two passages are not fully consistent about which retrieval produced the main HotPotQA contexts.
  - Contexts truncated to 6000 tokens for all three datasets (§4.1, Figure 2 caption).
- **Fine-tuning data (App. A.2, B.1):** 2,000-example subsets from Musique-Ans train and HotPotQA dev (dev used because train was "over 88% sufficient context, while the dev set was only 44%", App. A.2 footnote 2).
- **Languages:** all datasets are English-language QA benchmarks. See §5.

---

## 4. Method

### 4.1 Definition of sufficiency (§3, §3.1)

[FACT] "An instance $q'=(Q,C)$ has sufficient context if and only if there exists an answer $A'$ such that $A'$ is a plausible answer to the question $Q$ given the information in $C$." (§3.1, Definition). It differs from AIS-style entailment because it does not presuppose the answer; it allows the context to contain an incorrect answer (§3.1). §3 adds that a context is insufficient if the query "requires specialized knowledge that is not provided in the context or if the information in the context is incomplete, inconclusive, or contradictory." Remarks 1–3 (§3.1) cover multi-hop (no unstated connections), ambiguous queries, and ambiguous contexts (sufficient only if the context disambiguates).

### 4.2 Autorater (§3.2, Table 1, App. C.1–C.2)

[FACT]
- Main autorater: Gemini 1.5 Pro (`gemini-1.5-pro-0514`), 1-shot, chain-of-thought style prompt (App. C.1) that asks the model to list step-by-step sub-questions, answer them, write an `### EXPLANATION`, then output JSON `{"Sufficient Context": 1|0}`. The prompt includes a `<TIMESTAMP>` slot ("Assume the queries have timestamp <TIMESTAMP>").
- Cheaper autorater: FLAMe-RM-24B (App. A.1); because of its small context window, contexts are split into 1600-token chunks and the instance is labelled sufficient "If any chunk is labeled sufficient" (§3.2, §5.1).
- Baselines needing the gold answer: TRUE-NLI (T5-11B, threshold 0.05 on max chunk probability, chosen as best F1 on the human set, App. A.1) and "Contains GT".
- Results on the 115-item set (Table 1): Gemini 1.5 Pro 1-shot F1 0.935 / Acc 0.930; 0-shot 0.878 / 0.870; FLAMe 0.892 / 0.878; TRUE-NLI 0.818 / 0.826; Contains GT 0.810 / 0.809.
- In §4 the Gemini 1-shot rater labels the analysis datasets; in §5.1 FLAMe supplies the sufficiency signal for selective generation (§3.2, "Discussion").

### 4.3 Answer evaluation (§4.2, App. B.3, C.3, C.4)

[FACT] Generation uses a CoT prompt ending with "The answer is:" (App. C.4). Responses are first string-matched to gold answers; unclear cases go to an "LLMEval" judge (zero-shot, Gemini 1.5 Pro per App. C.3, prompt based on Krishna et al. 2024) that labels perfect / acceptable / incorrect / missing, mapped to correct / hallucinate / abstain. Normalisation: "removing punctuation, converting to lowercase, and eliminating stop words" (App. C.3). App. B.3 / Table 5 shows lexical "Contains" is generally stricter than LLMEval.

### 4.4 Selective generation: how sufficiency and confidence are combined (§5.1)

[FACT]
- Signals: (a) self-rated confidence and (b) the **binary** sufficiency label from FLAMe.
  - **P(True)** (open model, Gemma): "sampling 20 responses for each question and querying the model 5 times to evaluate whether the answer is correct or incorrect (without using the ground truth)" (§5.1, Methods), following Kadavath et al. 2022.
  - **P(Correct)** (proprietary models, Gemini and GPT): the prompt "requests the most likely and second most likely answers along with their probabilities"; the highest-probability answer and its probability are kept by string matching (§5.1, Methods), adapted from Li et al. 2024.
- Combiner: "a simple logistic regression model to predict hallucinations with 100 iterations of random hyperparameter search" (§5.1).
- Decision: "we use the logistic regression model scores to threshold the outputs, abstaining when the score is below a chosen threshold" (§5.1).
- Baseline: the same confidence signal alone (grey vs. purple lines, Figure 4).

### 4.5 How thresholds are chosen

[FACT] v3 does **not** describe a procedure for selecting a specific operating threshold (e.g. for a target risk), nor a train/calibration/test split for fitting the logistic regression. The results are reported as full coverage–selective-accuracy curves (Figure 4). §5.1 Discussion says: "While ordering examples is impossible in real settings, we can estimate a coverage level and use a threshold to choose when to answer."
[INFERENCE] The curves appear to be produced by sweeping the threshold over the score (coverage in 5% steps in the repo copy of the figure), so every point is effectively an in-sample operating point; I found no statement of whether the logistic model was fit on the same items it is evaluated on. **This is a gap we should note, and a reason RQ2 is not answered by this paper.**

### 4.6 Fine-tuning (§5.2, App. A.2, B.1)

[FACT] LoRA (rank 4, alpha 8, 2 epochs, batch 16, lr 1e-5) on Mistral-7B-Instruct-v0.3 with three data mixes (gold answers; 20% random → "I don't know"; 20% autorater-insufficient → "I don't know"). Checkpoint choice was by best Correct % (App. A.2) — [INFERENCE] i.e. selected on the evaluation metric.

---

## 5. Languages

[FACT] I searched the full v3 text for "multilingual", "English", "Bengali", "Bangla", "roman", "translit", "code-mix", "cross-lingual", "non-English" and "script": **none occur** in the paper's own content. Every dataset used (FreshQA, Musique-Ans, HotPotQA; PopQA, Natural Questions, EntityQuestions for the autorater set) is an English QA benchmark, and every prompt in App. C–D is in English.

**Explicit statement:** the paper includes **no Bengali, no romanized text, no code-mixed text, and no non-English language of any kind**. It does not discuss language or script as a factor at all.

---

## 6. Metrics

[FACT]
- Autorater: F1, accuracy, precision, recall against human labels (Table 1).
- Response outcomes: % Correct, % Abstain, % Hallucinate (Figure 3, Tables 3–4), stratified by sufficient vs. insufficient context.
- Selective generation: coverage ("% of questions answered") vs. selective accuracy ("# correct / # answered") (Figure 4 caption).
- No confidence intervals, significance tests, AURC, or calibration error (ECE) are reported in v3 [FACT: none found in text or tables].

---

## 7. Key findings (with locations and verbatim quotes)

1. **Autorater accuracy.** "Gemini 1.5 Pro (1-shot) performs the best overall in terms of F1 score and accuracy." (§3.2, Results; Table 1: acc 0.930, F1 0.935, n = 115.) The authors conclude "classifying sufficient context is a different (and more complex) task than determining entailment" (§3.2, Discussion).

2. **Benchmarks are often insufficient.** Figure 2 / §4.1: FreshQA has the highest sufficient-context share; Musique and HotPotQA are lower. Figure 1 caption: "standard datasets have many instances with insufficient context (here, 55.4%)" (Musique). Figure 5 caption gives FreshQA 77.4% sufficient. [FACT, from the repo's copy of Figure 2, `resources/compare_fraction_sufficient_context.png`, which I viewed: at 6000 tokens FreshQA 77.4, HotpotQA 46.2, Musique 44.6. I did not render the arXiv v3 SVG of Figure 2, so these bar values are from the repo image, which may differ from the paper version.]

3. **Strong models answer instead of abstaining on insufficient context; smaller models also hallucinate or abstain on sufficient context.** Abstract: larger models "excel at answering queries when the context is sufficient, but often output incorrect answers instead of abstaining when the context is not." and smaller models "hallucinate or abstain often, even with sufficient context." §1: "when given instances without sufficient context, models tend to hallucinate more than they abstain, especially for multi-hop questions."

4. **RAG reduces abstention.** §4.2 ("Models Abstain Less with RAG"): "the introduction of additional context paradoxically reduces the model’s ability to abstain from answering when appropriate." Reported numbers: Claude 3.5 Sonnet 84.1% → 52%, GPT 4o 34.4% → 31.2%, Gemini 1.5 Pro 100% → 18.6% abstention, without vs. with RAG. [INFERENCE] The text does not state which dataset these figures are from; the Figure 5 caption (FreshQA) mentions "100% for Gemini 1.5 Pro" without RAG, so they are probably FreshQA. Treat as unconfirmed.

5. **Correct answers despite insufficient context.** §1 contribution 2: "SOTA LLMs output correct responses 35–62% of the time with insufficient context." §1 also says this "remains true after we filter out questions that the model answers correctly in a closed book (w/o RAG) setting." Table 2 (§4.3) gives eight reasons (yes/no guessing, limited choice, multi-hop fragment, multi-hop partial, too many hops, ambiguous query, rater error, closed-book correct). [FACT] v3 does not report a table of the closed-book-filtered rates that I could find; the claim is stated in prose only.

6. **Hallucination even with sufficient context.** §4.2: "in the sufficient context case (top row), we see that models hallucinate more than they abstain". On the human-labelled set (App. B.2, Table 4a), with sufficient context the hallucination rate is 3.2% (Claude 3.5 Sonnet) to 25.4% (Gemma 27B); with insufficient context (Table 4b) abstention is 50.0–73.1% and hallucination 15.4–40.4%. [INFERENCE] Table 4's 54.8% / 45.2% split equals 63/115 and 52/115, so Table 4 is probably on the 115-item autorater set; the paper calls it "a curated set of challenging context-dependent questions" and does not give n.

7. **Selective generation helps, but not uniformly.** §5.1 Results: "We find that our approach leads to a better selective accuracy-coverage trade-off compared to using model confidence alone." Gains "of over 10% for Gemma 27B on HotpotQA in the highest accuracy regions, and gains of over 5% for Gemini 1.5 Pro on the same dataset near the 70% coverage region." On Gemma 27B / Musique (18.4% overall accuracy) "there is no added benefit from the sufficient context signal" (Figure 4 caption: "coeff. for stuff. context is 0"). Headline: "improves the fraction of correct answers among times where the model responds by 2–10% for Gemini, GPT, and Gemma" (Abstract). [INFERENCE] From the repo copy of Figure 4 (`resources/accuracy_vs_coverage_grid_3_models_2_datasets.png`, viewed), for GPT 4o the two curves largely overlap above ~30% coverage on both datasets; the gains are concentrated in low-coverage regions and in Gemini/Gemma on HotpotQA. The paper does not say whether "2–10%" means percentage points (the repo README says "percentage points").

8. **Abstaining on every insufficient instance is too blunt.** §5.1: using the autorater alone to abstain "can lower overall performance, since all models answer some questions correctly even with insufficient context". A stated prerequisite: "models should have a non-trivial accuracy on sufficient and insufficient context instances" (§5.1, Discussion).

9. **Fine-tuning to say "I don't know" does not fix it.** App. B.1: "refuting our hypothesis, Data Mix 2 and 3 do not lead to more abstentions than Vanilla RAG." (Table 3: abstention 1.2–2.2% on Musique, 0.8–2.0% on HotPotQA for the "idk" mixes vs. 11.8% / 9.2% for vanilla RAG.)

---

## 8. Limitations

### 8.1 Stated by the authors (§6, "Limitations")
[FACT] QA only, not summarisation; no study of "how often different retrieval methods lead to sufficient context"; no iterative retrieve-or-answer use of the autorater. Future work: a graded (non-binary) autorater, multimodal RAG.

### 8.2 Our assessment [INFERENCE unless marked]
- **English only** (§5 above). Nothing about language, script, transliteration or code-mixing.
- **No threshold-transfer or held-out operating-point evaluation** (§4.5 above). Curves show ranking quality, not whether a threshold chosen on one set delivers its target risk on another.
- **Autorater validated on 115 items**, with no inter-annotator agreement reported and no confidence intervals on Table 1.
- **Selective-generation sufficiency signal is FLAMe-24B with an any-chunk-sufficient rule**, not the more accurate Gemini 1-shot rater; on multi-hop items an any-chunk rule may miss sufficiency that only holds across chunks. [INFERENCE]
- **LLM-as-judge (Gemini 1.5 Pro) for correctness**; App. B.3 compares it with lexical matching but not with human labels on these datasets.
- **No statistical tests or CIs** anywhere in v3.
- **Fine-tuning checkpoint selected by Correct %** (App. A.2), apparently on the evaluation data.
- **Prompt typo in v3:** App. C.2 (FLAMe prompt) defines "1. sufficient: The documents are not sufficient ..." and "2. insufficient: The documents are sufficient ..." — labels swapped. The GitHub README version of the same prompt has them the right way round. Use the README version.
- **Sufficiency judged on English contexts by English-centric raters.** [INFERENCE] Whether FLAMe/Gemini-style raters are accurate on Bengali-script or romanized queries is untested, and this is exactly our RQ4(ii)/(iii) territory.

---

## 9. Details useful for replication (M3)

[FACT unless marked]
- **Prompt text:** App. C.1 (autorater, Gemini 1-shot), App. C.2 (FLAMe), App. C.3 (LLMEval), App. C.4 (CoT and answer-only QA prompts), App. D (Mistral RAG / no-RAG prompts with "I don’t know" instruction). The same autorater, FLAMe and LLMEval prompts are reproduced in the repo README (`## 🔧 Prompts`). The P(Correct) prompt (adapted from Li et al. 2024) and the P(True) prompts are **not** reproduced in v3 or in the repo — we must reconstruct them from Li et al. 2024 and Kadavath et al. 2022 (both would need their own reading before we describe them).
- **Models (App. A.1):** `gpt-4o-2024-08-06`; `gemini-1.5-pro-0514`; `claude-3-5-sonnet-20240620`; `gemma-2-27b-it`; `Mistral-7B-Instruct-v0.3`; FLAMe-RM-24B; TRUE-NLI `t5_xxl_true_nli_mixture`.
- **Decoding:** temperature, top-p, max tokens and seeds are **not reported** in v3 (none found). P(True) uses 20 sampled responses per question × 5 judgement queries, which implies non-greedy sampling, but the temperature is not given.
- **Context handling:** truncate to 6000 tokens; FLAMe chunks of 1600 tokens with any-chunk-sufficient aggregation; FreshQA timestamp injected into the autorater prompt.
- **Combiner:** logistic regression on [binary sufficiency, self-rated confidence], 100 iterations of random hyperparameter search; abstain when score < threshold. Hyperparameter space, regularisation and data split are not reported.
- **Thresholds:** no specific value or selection rule given; results are swept curves (§4.5 above).
- **Code and licence:** https://github.com/hljoren/sufficientcontext (checked 2026-10-23 via the GitHub API; last push 2025-07-22). The repo holds **only `README.md` and five figure PNGs in `resources/` — no code**. The GitHub API reports **no licence** (`license: null`) and there is no LICENSE file. [INFERENCE] Without a licence, default copyright applies to the repo contents. The prompts also appear in the paper itself, which arXiv distributes under **CC BY 4.0**, so adapting the App. C.1 prompt with attribution seems to be covered by the paper's licence. This is not legal advice, and **the author should confirm** before we release an adapted prompt (relevant to open question on licences).
- [REC] For M3 with local 7–9B models: (a) use the C.1 autorater prompt as the base, translated/adapted only in the instruction language we decide on (a protocol choice, to be logged); (b) since FLAMe-24B and Gemini are outside our budget/hardware, our sufficiency rater will differ from theirs — we must validate it on our own human-labelled sufficiency items and report its accuracy per variant; (c) fit the logistic combiner on EN-dev only, freeze it, and choose the threshold for target risk *r* on EN-dev — which is precisely the step Joren et al. leave unspecified.

---

## 10. How our work differs (exact statement)

Joren et al. (2025) define context sufficiency, build an English-language sufficiency autorater, stratify model errors by sufficiency on three English QA benchmarks, and show that adding a binary sufficiency signal to self-rated confidence improves the coverage–selective-accuracy curve. **Our study differs in four ways:** (1) we hold meaning and evidence fixed and vary only the query form — English, Bengali script, romanized Bengali, Bengali–English code-mixed — none of which they test; (2) we construct sufficiency by minimal controlled edits to oracle passages instead of labelling naturally retrieved contexts with an autorater, so sufficiency is known by design rather than estimated; (3) we test whether an operating threshold selected on English dev data achieves its target risk and coverage on held-out items in each variant (RQ2), whereas they report swept curves and do not evaluate a pre-selected threshold on held-out data; (4) we separate comprehension failure from miscalibration (RQ3) and include a closed-book control per item. We use their sufficiency definition and adapt their autorater prompt and confidence-plus-sufficiency combiner as method M3.

### Does this paper already partly answer RQ2?
**No.** [FACT] It contains no cross-language or cross-script experiments and no evaluation of a threshold selected on one set and applied to another. [INFERENCE] The closest relevant points are indirect: (a) the added value of the sufficiency signal varied strongly across model–dataset pairs (zero for Gemma/Musique, §5.1), which suggests operating characteristics are distribution-dependent — a motivation for RQ2, not an answer; (b) the authors note that "ordering examples is impossible in real settings" and that one must "estimate a coverage level and use a threshold" (§5.1), which is the deployment problem RQ2 tests under a script shift.

### Novelty threats from this paper
None for RQ1–RQ4 as framed [INFERENCE]. The table in research_plan §2 ("Does not cover: non-English languages, script variation, threshold transfer") is **confirmed by full reading**. We must not claim novelty for the sufficiency definition, the autorater, or the confidence+sufficiency selective-generation idea; those are theirs.

---

## 11. Verbatim quote index (for spot-checking against arXiv v3 HTML)

1. Abstract: "an open question is whether errors arise because LLMs fail to utilize the context from retrieval or the context itself is insufficient to answer the query."
2. §3.1 Definition: "An instance $q^{\prime}=(Q,C)$ has sufficient context if and only if there exists an answer $A^{\prime}$ such that $A^{\prime}$ is a plausible answer to the question $Q$ given the information in $C$ ."
3. §1 contribution 2: "SOTA LLMs output correct responses 35–62% of the time with insufficient context."
4. §4.2: "the introduction of additional context paradoxically reduces the model’s ability to abstain from answering when appropriate."
5. §5.1: "we use the logistic regression model scores to threshold the outputs, abstaining when the score is below a chosen threshold"
6. §5.1 Results: "We find that our approach leads to a better selective accuracy-coverage trade-off compared to using model confidence alone."
7. §5.1 Discussion: "While ordering examples is impossible in real settings, we can estimate a coverage level and use a threshold to choose when to answer."
8. App. B.1: "refuting our hypothesis, Data Mix 2 and 3 do not lead to more abstentions than Vanilla RAG."
9. §3.2 Discussion: "classifying sufficient context is a different (and more complex) task than determining entailment."

---

## 12. Parts not accessed / caveats

- Figures 1, 3, 5, 6 (stacked/pie charts of correct/abstain/hallucinate rates) are images in the arXiv HTML; I read their captions but did **not** read per-bar values from the arXiv versions. For Figures 2 and 4 I viewed the copies in the GitHub repo `resources/` folder, not the arXiv SVGs; any values quoted from them are labelled as such above.
- Page numbers not available (see §1).
- The ICLR camera-ready PDF was not compared against arXiv v3.
- Cited works (Kadavath et al. 2022; Li et al. 2024; Vu et al. 2024 FLAMe; Krishna et al. 2024) were **not** read; nothing here should be taken as a claim about their content beyond how Joren et al. describe their use.

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
