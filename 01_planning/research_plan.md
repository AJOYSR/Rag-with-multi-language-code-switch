# Research Plan — Abstention Transfer Across Scripts in Bengali–English RAG

Version 0.1 · 2026-10-23 · Author: Ajoy Sarker

> **Epistemic status labels used in this document**
> **[FACT]** verified in a source listed in `02_literature/literature_matrix.md` (verification level noted there).
> **[ASSUMPTION]** believed true but not yet checked; must be resolved before the stage that depends on it.
> **[HYPOTHESIS]** a testable claim this project will test.
> **[REC]** a recommendation or design choice; may change and is logged in `decision_log.md`.

---

## 1. Background and context

RAG systems are deployed so that answers are grounded in documents. A grounded system must do two things: answer correctly when the evidence supports an answer, and **abstain** when it does not. Failing at the second produces confident, unsupported answers, which is the main trust failure of RAG in practice.

What is established:

- **[FACT]** Joren et al. (ICLR 2025) separate RAG errors caused by *insufficient context* from errors caused by *failing to use sufficient context*. They show that strong models often answer instead of abstaining when context is insufficient, and that a sufficiency signal used for selective generation raises the share of correct answers among those given by about 2–10%. Their evaluation is on English datasets.
- **[FACT]** Feng et al. (EMNLP 2024) report that abstention methods degrade outside high-resource languages, with gaps of up to 20.5% between high- and low-resource languages. They propose multilingual feedback as a fairer abstention strategy.
- **[FACT]** NoMIRACL (Thakur et al., EMNLP 2024 Findings) measures, across 18 languages, both hallucination when all passages are irrelevant and errors when relevant passages exist. Models trade one failure for the other.
- **[FACT]** Khullar et al. (arXiv 2512.10780, 2025/26) find consistent degradation of up to 24 points for **romanized** vs. native-script Indian-language inputs in a real triage setting. They note that models that appear to understand romanized input may still fail to act on it reliably.
- **[FACT]** Marwah et al. (arXiv 2610.02926v1; NeurIPS 2026 LP4FM workshop per the arXiv comment) study closed-book TriviaQA with distractors prepended to the prompt. Under Hindi distractors, several models abstain more often (e.g. Qwen-2.5-3B 0.352→0.730; Table 4). A paragraph-length **English** Wikipedia distractor raises abstention to 0.424–0.998 across five models (Table 4). The abstract's "0.806–0.998 across all models" omits two models. *(Corrected 2026-10-23 after full read; v0.1 overstated this as mixed-language contamination causing near-universal abstention.)*
- **[FACT]** Wen et al. (TACL 2025) survey abstention in LLMs and its evaluation.

Why Bengali: Bengali is spoken by over 200 million people, and real users write it in three forms (native script, romanized, and Bengali–English code-mixed). Production systems in Bangladesh receive all three. **[ASSUMPTION — find a citable source for script-usage prevalence before the Introduction is written.]**

## 2. Problem and research gap

**Problem.** Abstention mechanisms (prompts, confidence thresholds, sufficiency checks) are designed and calibrated mostly in English. A deployed Bengali system will receive Romanized and code-mixed queries. If the abstention operating point shifts with script, a threshold that delivers a target error rate in testing will **silently** miss it in deployment.

**Candidate gap [HYPOTHESIS, pending gate G1]:**
No study found so far tests, under controlled conditions, whether an abstention rule or threshold **calibrated in one language transfers to another script or a code-mixed form** of the same language, while separating:
(a) evidence availability (sufficient vs. insufficient),
(b) comprehension of the variant, and
(c) retrieval failure.

What the closest works cover, and what they leave open (**updated 2026-10-23 after full reading; see `02_literature/notes/` and `G1_novelty_memo.md`**):

| Work (status) | Covers | Does not cover (full-read) |
|---|---|---|
| Joren et al. 2025 (full-read) | sufficiency autorater; selective generation from sufficiency + confidence | any non-English input; held-out threshold selection; threshold transfer |
| Feng et al. 2024 (full-read) | abstention across English + 26 other languages incl. Bengali (native script, MT; App. B); "only somewhat transferable" abstention *decisions* across languages | RAG with controlled evidence; romanized/code-mixed input; threshold transfer at a target risk |
| NoMIRACL 2024 (full-read) | multilingual RAG relevance-based abstention incl. Bengali | minimal-edit sufficiency; same-item script variation; scores/thresholds (rule-based IDK) |
| Khullar et al. 2025/26 (full-read) | native vs romanized gap (up to 24 pts); shift toward "insufficient information" under romanization; script-normalisation routing | Bengali; RAG/sufficiency; numeric thresholds or calibration |
| Marwah et al. 2026 (full-read) | distractor-induced abstention escalation (closed-book) | paired script variants; evidence sufficiency; thresholds |
| Zoumpoulidi et al. 2026 (full-read) | paired solvable/unsolvable items across EN/FR/EL; language-dependent false abstention | RAG; scripts; Bengali; thresholds |
| **Alfarano et al. 2026** (full-read) | **English-tuned threshold applied to 22 languages incl. Bengali (pooled; F1-selected)**; English-reasoning (pivot) improves UE | evidence sufficiency/RAG; romanized/code-mixed; target-risk realised risk per language; direct comprehension measurement |
| **Thimma Krishnaram et al. 2026** (full-read) | **thresholds tuned on clean English, frozen, applied to paired code-mixed input → decision flips** | RAG; Bengali; script separated from code-mixing; comprehension vs calibration |
| Kabir et al. 2026, BanglaShield (full-read) | aligned Bangla native / romanized / code-mixed items (auto-generated); romanized degrades safety refusal | RAG/sufficiency; English pairing; thresholds; human-validated variants |
| **Krause et al. 2026, WMT** (full-read) | **cross-lingual context-based QA; answer-sentence-deletion negatives; probe threshold does not transfer across question languages (incl. Bengali passages)** | romanized/code-mixed; behavioural abstention methods (prompted, verbalized, sufficiency autorater); target-risk evaluation |
| Zhang & Wu 2026 (abstract-read) | English five-level evidence-sufficiency abstention benchmark | any non-English input |

**Revised gap statement [HYPOTHESIS, pending author decision at G1]:** prior work shows that abstention degrades across languages and under romanization, and that English-tuned or globally-fitted thresholds shift on code-mixed or other-language input, including an answerability-probe threshold in cross-lingual context-based QA (Krause et al. 2026). To our knowledge, no study measures whether an abstention threshold selected on English dev **for a target risk** keeps that risk on native-script, romanized and code-mixed renderings of the **same** RAG items under **controlled evidence sufficiency**, nor separates comprehension from calibration with a direct per-item comprehension check, for Bengali or any other language.

**Gate G1 must confirm this table by full reading.** The paper must **not** claim to be "the first" to study multilingual abstention or Bengali RAG.

## 3. Research questions, objectives, hypotheses

**RQ1 — Variant sensitivity.** With meaning and evidence held fixed, do unsupported-answer rate (UAR) and unnecessary-abstention rate (UNR) differ across EN, BN, RBN and CM?
- **H1 [HYPOTHESIS]:** UAR on insufficient-evidence items is higher for RBN and CM than for EN and BN.
- **H1-alt:** UNR rises instead, i.e. the model over-abstains on variants it partly fails to understand (consistent with Marwah et al.'s abstention escalation under Hindi distractors, Feng et al.'s finding of more unnecessary abstention in low-resource languages, and Khullar et al.'s shift toward "insufficient information" under romanization — see notes). Either direction is a reportable reliability failure.

**RQ2 — Threshold transfer.** Does a confidence or sufficiency threshold selected on English dev data achieve the same target risk and coverage on the other variants?
- **H2 [HYPOTHESIS]:** An English-selected threshold violates the target risk on at least one non-English variant by more than the bootstrap confidence interval.

**RQ3 — Source of the gap.** How much of any gap comes from comprehension failure rather than miscalibration?
- **H3 [HYPOTHESIS]:** After restricting to items whose variant passes a comprehension check, the gap shrinks but does not disappear.

**RQ4 — Mitigation.** Does a cheap intervention close the gap on held-out items at matched coverage?
Candidates: (i) per-variant threshold from a small dev set (≈ 30–50 items); (ii) transliterating RBN into BN script before the sufficiency check; (iii) running the sufficiency judgment in a fixed pivot language.
- **H4 [HYPOTHESIS]:** (i) or (ii) reduces the risk-target violation found in H2 at comparable coverage.

**Objectives:** (O1) a validated, redistributable paired dataset; (O2) a controlled measurement of RQ1–RQ3; (O3) an evaluated intervention (RQ4); (O4) released code, prompts and data.

## 4. Novelty and expected contributions

1. **A controlled paired benchmark.** About 175 base items × 4 variants × 2 sufficiency conditions, with meaning-equivalence validation. *Novel element:* script and code-mix variation of the same item under controlled evidence.
2. **A threshold-transfer analysis.** Realised vs target risk, per variant, for a threshold selected on English dev. *Novel element (narrowed 2026-10-23):* target-risk transfer for evidence-sufficiency abstention in RAG, with script and code-mixing separated. The generic question of English→other-language threshold transfer is **not** new (Alfarano et al. 2026; Thimma Krishnaram et al. 2026).
3. **A decomposition** of gaps into comprehension and calibration components.
4. **A low-cost mitigation** evaluated on held-out items.

A null result (no gap once comprehension is controlled) is a valid and publishable contribution if the method is rigorous. The paper will be framed so that it holds in either case.

## 5. Methodology / experimental design

### 5.1 Factors

| Factor | Levels | Note |
|---|---|---|
| Query variant | EN, BN, RBN, CM | within-item |
| Evidence sufficiency | sufficient, insufficient | within-item; minimal edit |
| Evidence language | BN (core); EN (extension) | [REC] start with BN only |
| Abstention method | M1 instructed abstention; M2 verbalized confidence + threshold; M3 sufficiency autorater + selective generation; M2b token-probability confidence (open models only) | |
| Model | 2–3 open-weight multilingual models (7–9B) + optionally 1 low-cost API model | see §6.3 |
| Context | oracle evidence (core); retrieved top-k (extension) | retrieval only after the core result |

### 5.2 Item construction

1. **Source document.** A short passage (≤ 300 words) from a redistributable source.
2. **Base question** with a short, objectively checkable answer: a number, date, amount, name, or yes/no.
3. **Insufficient evidence** is made by deleting or neutralising the answer-bearing sentence. A checker confirms the answer cannot be inferred from what remains. Each insufficient item also gets a **near-miss** design where possible: the passage still answers a sibling question (fee present, deadline missing), so that abstention cannot be triggered by topic mismatch alone.
4. **Parametric-knowledge control (important).** Each item is also asked **closed-book**. Items that models answer correctly without evidence are flagged and analysed separately. Otherwise "answering an insufficient item" may reflect memorisation rather than hallucination. [REC] Prefer documents with local or recent facts that are unlikely to be memorised.
5. **Variants.** The author writes BN, RBN and CM renderings (LLM drafts allowed, always human-edited and logged). RBN follows a documented romanization convention plus a controlled amount of natural spelling variation.

### 5.3 Validation

- A **second native speaker** independently rates a stratified ≥ 20% sample for (a) meaning equivalence with EN and (b) naturalness. Report percent agreement and Cohen's κ. Items failing equivalence are revised or dropped.
- An **insufficiency check**: a second person, or two models plus manual adjudication, confirms the answer is not derivable.
- A **comprehension probe** per variant (for RQ3): the model paraphrases or translates the query into English, and the result is checked against EN. This yields a per-item "understood" flag.

### 5.4 Splits

The split is **by base item**: dev ≈ 25% and test ≈ 75%, stratified by answer type. All variants of an item share a split, which prevents leakage between near-duplicate variants. Thresholds, prompts and interventions are tuned on dev only.

### 5.5 Metrics

| Metric | Definition |
|---|---|
| Unsupported-answer rate (UAR) | P(answers \| insufficient) |
| Unnecessary-abstention rate (UNR) | P(abstains \| sufficient) |
| Selective accuracy | P(correct \| answered, sufficient) |
| Coverage | P(answers) |
| Risk–coverage curve, AURC | from M2/M2b/M3 scores |
| Accuracy at matched coverage | compare variants at the same coverage |
| Target-risk violation (RQ2) | observed risk on variant *v* at a threshold chosen on EN dev for target risk *r* |
| ECE | calibration of verbalized or token confidence |

**Answer scoring** uses deterministic normalisation (Bengali↔ASCII digits, units, date formats, transliterated names), then exact or alias match. Ambiguous cases go to manual adjudication. If an LLM judge is used, it is audited against a human-labelled sample and its agreement is reported.

### 5.6 Statistical analysis (to be frozen in `04_methodology/protocol.md` before the test run)

- Paired differences between variants use **McNemar's test** and **paired bootstrap 95% CIs** (resampling base items).
- A **mixed-effects logistic regression** models the probability of answering: `answers ~ variant * sufficiency * method + (1 | item) + (1 | model)`.
- Multiple comparisons are corrected with **Holm–Bonferroni**.
- A **power check** is run after the pilot: estimate the detectable UAR difference given n ≈ 130 test items and the observed discordance rate. Raise n if needed.

## 6. Data sources, tools, techniques

### 6.1 Candidate document sources [all ASSUMPTIONS until licence checked]

| Source | Pros | Risks |
|---|---|---|
| Bengali Wikipedia (CC BY-SA) | clear licence | high memorisation risk → closed-book filter essential |
| Bangladesh government notices / circulars | realistic, local, often recent | licence or redistribution terms unclear |
| University admission circulars | realistic numbers and dates | same as above |
| Author-written synthetic notices (fictional institutions) | zero memorisation, full licence control | lower ecological validity; must be disclosed |

[REC] Use a mix of author-written fictional notices (core, for control) and Wikipedia passages (realism check), and report results per source.

### 6.2 Existing datasets to consider for reuse or extension (check licences and Bengali coverage)
MIRACL / NoMIRACL (Bengali subset `[UNVERIFIED]`), M-AbstainQA (Feng et al.), MIRAGE-Bench (Bengali coverage `[UNVERIFIED]`), BenHalluEval (arXiv 2605.31483, under review; licence `[UNVERIFIED]`).

### 6.3 Tools
Python; Hugging Face `transformers` or `llama.cpp`/Ollama for local open-weight models; pandas, statsmodels, scipy; matplotlib. Candidate models (check current availability and Bengali support): Qwen-family, Gemma-family and Llama-family instruct models in the 7–9B range. Use one low-cost API model only if the budget allows. Record exact model IDs and dates.

### 6.4 Budget estimate
Core run size: 175 items × 4 variants × 2 sufficiency conditions = 1,400 prompts per method per model; × 3 methods × 3 models ≈ 12.6k generations, plus closed-book and comprehension probes. That is roughly free on local hardware, or a few US$ on a low-cost API. **[ASSUMPTION — depends on the author's hardware; see open questions.]**

## 7. Validation strategy for the *claims*

- **Held-out test split** for every reported number. Dev is used only for selection.
- **At least two model families**, so findings are not one-model artefacts.
- **At least two document sources** (fictional and Wikipedia), so findings are not source artefacts.
- **Robustness checks:** prompt paraphrase (2 instruction wordings), temperature 0 vs. sampling (3 seeds for a subset), and RBN spelling variants.
- **Sanity checks:** EN-only results should qualitatively reproduce the direction reported by Joren et al. (strong models under-abstain on insufficient context). If they do not, debug before going further.

## 8. Ethical considerations

- No personal data. KYC or other production data from employment is **excluded**.
- Annotators (second speaker) give informed consent and are credited in the acknowledgements; their time is compensated if possible.
- Source licences are documented; only redistributable text is released.
- AI assistance (translation drafts, coding, writing) is disclosed according to venue policy (ACL policy on AI writing assistance).
- Fictional institutions are clearly fictional and do not imitate real organisations.

## 9. Limitations (anticipated)

- Scale (~175 base items) limits fine-grained subgroup analysis.
- Author-constructed variants may not cover the full range of natural romanization or code-mixing; a single annotator community (Bangladeshi Bengali) is used.
- Oracle evidence isolates generation but under-represents real retrieval noise. The retrieval extension only partly addresses this.
- Small open models may not reflect frontier-model behaviour.

## 10. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Close prior work appears (field is fast-moving) | Medium | High | G1 deep read now; set an arXiv alert; reframe around the transfer + decomposition contribution |
| No gap in pilot | Medium | Medium | Report the "gap disappears once controlled" framing; or pivot to Topic 2 (prompt-injection) reusing the variant pipeline |
| Memorisation confounds UAR | High for Wikipedia | High | closed-book filter; fictional documents |
| Variant quality challenged by reviewers | Medium | High | second annotator, κ, released guidelines |
| No second annotator available | Medium | Medium | recruit early (week 1); fallback: two-pass self-review with a time gap + model back-translation check, disclosed as a limitation |
| Hardware too weak for local 7–9B models | Unknown | Medium | 4-bit quantised models; free tiers; Colab — record the quantisation, which is itself a variable (cf. author's prior paper) |
| Time overrun (20 h/week) | Medium | Medium | gates allow cutting the retrieval extension and the EN-evidence factor first |

## 11. Timeline (20 h/week; start Mon 2026-10-26)

Dates are planning targets. Each gate decision is logged.

| Weeks | Dates | Milestone | Deliverables | Depends on |
|---|---|---|---|---|
| 1–2 | Oct 26 – Nov 8 | **M1 Literature validation** | Full-read notes for the 6–8 closest works; updated gap table; **G1 decision** | — |
| 1 | Oct 26 – Nov 1 | Recruit second annotator; confirm hardware | `open_questions.md` resolved | — |
| 3–4 | Nov 9 – Nov 22 | **M2 Pilot** | 30 items × 4 variants × 2 conditions; 2 models; M1+M3; power estimate; **G2 decision** | G1 |
| 5–6 | Nov 23 – Dec 6 | Protocol freeze | `04_methodology/protocol.md`, annotation guidelines, scoring code tested | G2 |
| 5–9 | Nov 23 – Dec 27 | **M3 Dataset** | 175 base items, variants, validation stats; `DATA_CARD.md`; **G3** | G2 |
| 10–12 | Dec 28 – Jan 17 | **M4 Main experiments** (RQ1–RQ3) | runs + EXPERIMENT_LOG; tables | G3, protocol frozen |
| 13–14 | Jan 18 – Jan 31 | **M5 Intervention** (RQ4) + robustness | held-out results | M4 |
| 15 | Feb 1 – Feb 7 | Optional retrieval extension | — (cut first if late) | M4 |
| 15–18 | Feb 1 – Feb 28 | **M6 Writing** | full draft v1 | M4–M5 |
| 19–20 | Mar 1 – Mar 14 | **M7 QA** | internal review, checklist, arXiv preprint | M6 |
| — | per venue | **Submission** | see §12 | M7 |

Buffer: about 2 weeks are implicitly absorbed by the holiday period (late Dec – early Jan). If the pilot slips, shift everything; do not compress the protocol freeze.

## 12. Target venues [all dates UNVERIFIED — check official sites before planning against them]

| Venue | Fit | Note |
|---|---|---|
| ACL Rolling Review → ACL / EMNLP 2027 (main or Findings) | Best for a rigorous empirical study | 8 pages long / 4 short + unlimited refs; Limitations section mandatory; Responsible NLP checklist |
| TrustNLP workshop (typically at NAACL/ACL) | Trustworthy-NLP focus | good fallback / early venue |
| MRL (Multilingual Representation Learning) workshop, typically at EMNLP | multilingual focus | — |
| BLP (Bangla Language Processing) workshop | Bengali community | 2025 edition was at AACL-IJCNLP 2025; a 2026/27 edition is not yet confirmed |

[REC] Primary target: the ARR cycle that feeds **EMNLP 2027** (typically a deadline around May). An **arXiv preprint by mid-March 2027** also supports PhD applications.

### 12.1 Pre-submission checklist (Phase 6)
- [ ] Every claim maps to a table, figure or `full-read` citation
- [ ] All bib entries verified (DOI / ACL Anthology / arXiv ID)
- [ ] Novelty re-checked against arXiv within 2 weeks of submission
- [ ] Test split untouched during development (git history shows this)
- [ ] Statistical tests match the frozen protocol; any deviations disclosed
- [ ] Limitations, ethics statement and Responsible NLP checklist completed
- [ ] AI-assistance disclosure per venue policy
- [ ] Data card, code and prompts released (anonymised for review)
- [ ] Anonymity: no self-identifying links in the submission
- [ ] Page limits and template compliance

## 13. Paper skeleton (to be filled only after M4)
1. Introduction · 2. Related Work (abstention; sufficient context; multilingual RAG; romanization/code-mixing) · 3. Task & Dataset · 4. Methods (abstention mechanisms, transfer protocol) · 5. Results (RQ1–RQ3) · 6. Mitigation (RQ4) · 7. Discussion · Limitations · Ethics · Appendix (prompts, annotation guide, per-model tables)
