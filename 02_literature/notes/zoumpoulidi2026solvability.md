# zoumpoulidi2026solvability — More Capable, Less Faithful: A Multilingual Analysis of Mathematical (Un)Solvability Detection in LLMs (A6)

**Read status:** full-read on 2026-10-23, from the arXiv HTML rendering of v1 (https://arxiv.org/html/2608.30463). Covered: §1–§5, Limitations, Ethical Considerations, Appendices A–H, and Tables 1–11. **Not read:** the values in Figure 1 (probe AUC) and Figure 2 (abstention rates). Both are images, so only their captions and the text describing them were available. No numeric abstention rates are quoted below for that reason.

## Bibliographic metadata (confirmed)

- **Title:** More Capable, Less Faithful: A Multilingual Analysis of Mathematical (Un)Solvability Detection in LLMs [FACT; abs page `citation_title`]
- **Authors:** Maria-Eleni Zoumpoulidi, Nikolaos Xiros, Georgios Paraskevopoulos [FACT; abs page]. The HTML footnote says the first two authors contributed equally, with author order "determined by coin flip". Affiliation: Institute for Language and Speech Processing, Athena Research Center, Greece.
- **arXiv:** 2608.30463v1 [cs.CL], submitted 31 Aug 2026. Only v1 exists as of 2026-10-23. DOI: 10.48550/arXiv.2608.30463.
- **Venue:** none stated. The abs-page Comments field reads only "10 pages, 3 Figures". Cite as an arXiv preprint.
- **URLs:** https://arxiv.org/abs/2608.30463 ; https://arxiv.org/html/2608.30463

## Objective

The paper asks whether multilingual failures to detect unsolvable maths problems come from (a) a different internal "Solvability Belief" or (b) language-dependent failure to *express* that belief (Abstract; §1). It has two research questions (§1):
- "RQ1: How does LLM performance in mathematical reasoning and unsolvability detection vary across languages?"
- "RQ2: How does language affect the faithfulness between internal solvability representations and textual solvability judgments?"

## Data

- ReliableMath (Xue et al., 2025), translated into French and Greek with Claude Sonnet 5 using the prompt in Table 7 (§2). It contains:
  - 313 solvable problems from MATH, MinervaMath and AIME24/AMC;
  - 1,102 unsolvable variants "obtained by removing or contradicting information essential to the solution" (§3).
- Translation validation (Appendix G): two authors each checked 100 problems, one author per language. Agreement was 97.0% for French and 95.0% for Greek (Table 6). This is a single annotator per language, so no inter-annotator κ is reported. [FACT]
- The authors state the code and data "will be available under the Apache 2.0 license" (§1). The footnote link reads only "Data: repository" and no URL is given in the HTML. [FACT]

## Method

- **Models (§3):** Qwen3-30B-A3B-Instruct-2507, Qwen3-4B-Instruct-2507, Llama-3.1-8B-Instruct and Gemma4-31B-IT. Two language-adapted Llama-3.1-8B variants were also tested: Llama-Krikri-8B (Greek) and French-Alpaca (French). Each adapted variant was evaluated only on English and its own target language.
- **Prompts (§2; Tables 9–10):** CoT prompting in two settings.
  - "standard" asks the model to solve the problem step by step.
  - "aware" adds an explicit unsolvable option, `\boxed{unsolvable}`.
  - Prompts are written in the language of the problem.
- **Probing (§2; App. D):** an L1-regularised logistic-regression probe on hidden states from the best layer. The probe uses the "ground-truth solvability label of the problem as a proxy for the model's internal belief". Hidden states from the standard and aware settings are pooled. Each sequence is represented by 20 uniformly sampled token vectors. Probes are either per-language or "universal" (pooled across languages).
- **Verdict annotation (§2; App. C, F):** Llama-3.3-70B-Instruct acts as judge and labels each trace "solved" or "unsolvable". The judge agreed with a human on 93.0% of a balanced set of 100 traces (Table 5). One author annotated that set.
- **Faithfulness (§4.4):** the agreement rate between the universal probe's prediction and the judge's verdict.
- **Statistics (App. E):** paired problem-level bootstrap (1000 resamples, 95%) for probe AUC differences, and two-proportion z-tests for faithfulness.

## Languages

- **Bengali: no** [FACT; full read].
- **Romanized input: no.** Greek appears in native script only [FACT; e.g., Tables 8–10].
- **Code-mixed input: no** [FACT].
- Languages covered: English, French and Greek, all in native script. Variants are machine-translated with single-annotator validation, not authored by humans.

## Metrics

- Accuracy on the solvable split under the standard prompt (Table 1).
- Probe validation AUC (Fig. 1).
- Abstention, shown in Fig. 2 and defined in §4.3:
  - "hit rate (true abstention) on the unsolvable split";
  - "false-abstentions rate on the solvable split".
- Faithfulness rate, i.e. probe–judge agreement (Tables 2–3).

## Key findings (with locations)

1. **Capability is highest in English.** In nearly every model, accuracy on solvable problems is best in English and degrades towards French and then Greek (§4.1, Table 1). For example, Gemma-4-31B-it scores 61.3 / 55.6 / 56.5 and Llama-3.1-8B scores 23.3 / 15.0 / 14.4 (EN / FR / EL). Qwen3-4B is an exception for French (52.1 EN vs 53.3 FR).
2. **The internal Solvability Belief is mostly language-agnostic.**
   - The universal probe "matches or exceeds the per-language probe performance for every model" (§4.2).
   - It is "never significantly worse than the per-language probe across any of the 16 model-language combinations tested" (App. E.1).
   - Probe AUC is highest in English. The English-over-Greek advantage is significant for Qwen3-4B (+3.8 AUC×100, CI [1.3, 6.5]), Qwen3-30B, Gemma-4-31B and Krikri. Krikri shows the largest gap, +7.9 (App. E.1).
3. **Under the aware prompt, false abstention increases in non-English languages (most relevant to H1-alt).**
   - Natively multilingual models "flag unsolvable problems at a comparable rate across all three languages, but their false-abstentions rate rises as we move from English to French and Greek" (§4.3).
   - For the language-adapted models, "the surge of true abstentions in the target language is accompanied by a spike in false-abstentions concentrated in that same language". The authors conclude that "language adaptation appears to lower the abstention threshold globally for the target language" (§4.3).
   - The exact numbers are in Fig. 2 (image only) and were not available to us.
   - Under the *standard* prompt, both Qwen3 models show a higher hit rate and fewer false abstentions in Greek than in English (§4.3).
4. **Faithfulness is reversed relative to capability.**
   - Pooled faithfulness (Table 2) is higher in the lower-resource languages for Gemma and Qwen. Qwen3-4B, for instance, scores 0.691 in EN and 0.728 in both FR and EL.
   - Llama-3.1-8B shows the opposite pattern: 0.544 / 0.529 / 0.498.
   - Only Qwen3-4B's English-worse effect (p<0.001) and Llama-3.1-8B's English-better effect (p<0.01) are significant. The other models "trend in the same English-worse direction but do not reach significance (p between 0.07 and 0.49)" (App. E.2).
   - Faithfulness is modest overall. Pooled values range from 0.473 to 0.730 (Table 2). [FACT]
5. **The aware prompt raises faithfulness on unsolvable items, most of all outside English.**
   - Gemma-4-31B goes from 0.271 to 0.762 in EN and from 0.253 to 0.791 in FR. Krikri goes from 0.273 to 0.556 in EL (Table 3).
   - The non-English advantage is significant for Krikri-EL, Alpaca-FR and Qwen3-4B (FR and EL). It is not significant for Qwen3-30B, Gemma or Llama-3.1-8B (App. E.2).

## Short verbatim quotes (with locations)

- "We find that Solvability Belief is encoded as a largely universal, language-agnostic feature, and that higher-resource languages such as English, despite achieving stronger mathematical reasoning performance, exhibit lower solvability-detection faithfulness." (Abstract)
- "Thus, under aware prompting, language adaptation appears to lower the abstention threshold globally for the target language, increasing both true hits and false refusals." (§4.3)
- "This indicates the Solvability Belief signal is largely encoded in a shared, only mildly language-specific subspace." (§4.2)
- "Our findings suggest that a model's dominant language yields stronger raw capability but not more trustworthy self-reports." (§5)
- "We acknowledge that, while our analysis provides informative insights, it would benefit from broader language coverage." (Limitations)

## Limitations

**Stated by the authors.** Coverage is limited to three languages. The authors plan to add Chinese and "typologically diverse, lower-resource languages" (Limitations).

**Our assessment [INFERENCE]:**
- (a) **The probe target is the ground-truth label, not the model's belief.** The paper says so itself: the label is used "as a proxy for the model's internal belief" (§2). "Faithfulness" is therefore agreement between a probe for the true label and the verbal verdict. A low score may partly reflect probe error, not unfaithfulness.
- (b) Abstention rates are shown only in figures, with no tables or CIs in the text. The §4.3 claims about false abstention carry no significance tests that we could find.
- (c) The translations are LLM-generated, and each language was checked by a single annotator on 100 items.
- (d) The faithfulness differences are small and mostly non-significant (App. E.2).
- (e) The task is maths solvability, with no retrieval and no evidence passages.
- (f) No confidence threshold is calibrated or transferred.
- (g) The paper uses "the first multilingual benchmark" claims. We have not verified them.

## How our work differs (exact statement)

Zoumpoulidi et al. study whether models detect **unsolvable maths problems**. Their problems are machine-translated into **French and Greek, in native script**. They analyse the gap between a linear probe's solvability signal and the verbal verdict.

Our study differs in five ways:
1. We study **RAG question answering under oracle evidence** that is either sufficient or insufficient (a minimal edit), not self-contained maths problems.
2. We vary **script and code-mixing within one language**: Bengali native script, romanized Bengali, and Bengali–English code-mixed. They vary language identity only, always in native script.
3. Our variants are human-authored and edited, and a second native speaker validates them.
4. We test **transfer of an English-calibrated abstention threshold** (RQ2). They calibrate no threshold.
5. We separate comprehension failure from miscalibration with a behavioural comprehension check (RQ3), not with hidden-state probes.

They do not cover Bengali, romanization, code-mixing, RAG, or threshold transfer. [FACT, from full read, for the negatives listed]

## Relevance to H1-alt / RQ3

- **H1-alt.** The §4.3 finding is closely analogous to H1-alt in a different domain. Under an explicit abstention option, multilingual models' **false abstentions on solvable items rise in the non-English languages**, while true abstentions stay level. The authors read this as a shifted abstention threshold. [INFERENCE] This is precedent for expecting UNR, not UAR, to rise on BN/RBN/CM, and for describing the effect as a shift in operating point. That is RQ2's framing.
  - Caveat: Fig. 2 values were not readable and no significance tests were given, so cite this as qualitative only.
- **RQ3.** The paper decomposes failures into internal belief versus verbalisation. [INFERENCE] This is a different decomposition from ours (comprehension versus calibration), but related.
  - Their result that the belief signal is language-agnostic while verbalisation varies by language is consistent with H3: a gap that persists after controlling for comprehension would point to calibration or verbalisation.
  - A probe-based arm (M2b, open models) could echo this in our study. Note this as optional, not planned.
- **Pairing precedent.** The paper uses parallel items and a paired bootstrap across languages (App. E.1). This supports our paired, item-level analysis.
- **Novelty threat: low.** Domain, languages, the script/code-mix factor and the threshold-transfer question all differ. We should cite it as adjacent evidence that abstention operating points shift across languages.

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
