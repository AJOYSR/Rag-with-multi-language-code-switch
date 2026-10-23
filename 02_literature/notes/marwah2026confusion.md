# marwah2026confusion — Output Language Confusion under Multilingual Prompt Contamination (A5)

**Read status:** full-read (2026-10-23), from the arXiv HTML rendering of v1 (https://arxiv.org/html/2610.02926). Read: main text §1–§7, Tables 1–4, figure captions, references. The PDF was downloaded but could not be rendered in this session (no PDF tools), so the numbers below come from the HTML version only. Figure 2 is an image, so only its caption was read.

## Bibliographic metadata (confirmed)

- **Title:** Output Language Confusion under Multilingual Prompt Contamination. [FACT; arXiv abs page `citation_title`]
- **Authors:** Riju Marwah, Ritvik Garimella, Khusham Bansal, Atishay Jain, Amit Sheth. [FACT; abs page] These match the authors listed in the literature matrix.
- **Affiliations (from the HTML):** University of Tübingen; AI Institute, University of South Carolina; Thapar Institute; IIT Kanpur; Indian AI Research Organization.
- **arXiv:** 2610.02926v1 [cs.CL], submitted 2 Oct 2026. Only v1 exists as of 2026-10-23. DOI: 10.48550/arXiv.2610.02926.
- **Venue:** the abs-page Comments field reads verbatim "Accepted at NeurIPS 2026 Workshop LP4FM". [FACT; abs page] This is the authors' own statement. It has **not** been checked against the workshop or OpenReview site.
- URLs: https://arxiv.org/abs/2610.02926 ; https://arxiv.org/html/2610.02926

## Objective

The paper tests whether a semantically irrelevant foreign-language sentence placed before an English factual question disrupts the answer. It also shows that exact-match "hallucination" metrics confuse two cases: answers that switch script but are still correct, and answers that are genuinely wrong (§1, contributions 1–3).

## Data

- TruthfulQA mc1 (validation): 500 questions sampled with seed 42. TriviaQA `unfiltered.nocontext` (validation): 500 questions, same seed, scored against the gold alias list (§4.2).
- The paper reports "5 models × 2 datasets × 8 conditions × 500 questions = 40,000 evaluations" (§4.3).
- TriviaQA is used **closed-book** (the `nocontext` configuration), so no evidence passage is supplied (§4.2). [FACT]

## Method — Multilingual Distractor Interference (MDI)

- Eight conditions (§3.1): `clean`; `es`/`es_long`; `hi`/`hi_long` (Devanagari); `zh`/`zh_long` (Simplified Chinese). The `_long` versions repeat the sentence three times. The eighth is `wiki_para`, a fixed English WikiText-2 paragraph of at least 200 characters.
- The distractor sentence declares itself irrelevant. The Spanish version is "Nota: Este texto no tiene relación con la pregunta. Por favor ignóralo." (§3.1). It is placed before the question, separated by a blank line.
- The question is always in English. Spanish serves as the same-script control (§1, §3.1).
- TruthfulQA is scored by log-probability over the letters A–D, with no generation. TriviaQA uses free generation with greedy decoding (T=0) and at most 32 new tokens. The system prompt includes "If you do not know, say: I don't know." (§3.2).
- Models (Table 1): Llama-3.1-8B-Instruct, Llama-3.2-3B-Instruct, Phi-3-mini-4k-instruct, Mistral-7B-Instruct-v0.2, Qwen2.5-3B-Instruct. All run in float16 on a single GPU.
- Statistics: McNemar's test with continuity correction against `clean`, and bootstrap 95% CIs with n=2000 (§3.3).

## Languages

- **Bengali: no.** No Bengali appears anywhere in the paper. [FACT; full read]
- **Romanized input: no.** Hindi appears only in Devanagari script. Romanized Hindi is not tested. [FACT]
- **Code-mixed input: no.** Each prompt is an English question with one foreign sentence placed before it. That is prompt contamination at the sentence level, not code-mixing within a sentence. [FACT; §3.1] [INFERENCE: this is not code-mixing in the sociolinguistic sense that our CM variant uses.]
- Distractor languages: Spanish, Hindi, Chinese, plus English in `wiki_para`. The task language is always English.

## Metrics

TriviaQA (§3.3) uses four metrics: (i) exact-match accuracy; (ii) abstention rate, detected by substring match on "I don't know", "unknown" and similar phrases; (iii) hallucination proxy = 1 − accuracy − abstention; (iv) script-switching rate, defined as at least one character from the distractor script's Unicode block. TruthfulQA uses MC accuracy.

## Key findings (with locations)

1. **Paragraph-length English distractor and abstention: exact numbers and conditions.**
   - The abstract says: "A paragraph-length English distractor triggers near-universal abstention (0.806-0.998) across all models, consistent with reading-comprehension confusion, a failure mode with direct consequences for multilingual RAG pipelines."
   - §5.5 says: "near-universal abstention (Mistral-7B: 0.860; Qwen-2.5-3B: 0.998; even Llama-3.1-8B, which shows minimal abstention under Hindi, abstains on 80.6% of wiki_para questions)".
   - **Table 4** ("TriviaQA abstention rates under Hindi and wiki_para conditions") gives these `wiki` abstention rates: Llama-3.1-8B **0.806**, Llama-3.2-3B **0.424**, Phi-3-mini **0.538**, Mistral-7B **0.860**, Qwen-2.5-3B **0.998**. The clean baselines are 0.066 / 0.072 / 0.082 / 0.098 / 0.352.
   - **Internal inconsistency [FACT, observed in Table 4 against the abstract]:** the range "0.806–0.998 across all models" covers only 3 of the 5 models. Table 4 shows 0.424 (Llama-3.2-3B) and 0.538 (Phi-3-mini). The correct range over all five models is **0.424–0.998**. Every model rises well above its clean baseline. **We must not cite "0.806–0.998 across all models".** If we cite this result, we should give the Table 4 values.
   - **Conditions:** TriviaQA, closed-book (no evidence), English question, greedy decoding, explicit "I don't know" instruction, and a fixed English WikiText-2 paragraph placed before the question. The paragraph is **English, not mixed-language.** The authors explain the effect as "context-format confusion": models "treat the prepended paragraph as part of the question context and decline to answer when the 'passage' does not contain the answer, as if performing reading comprehension rather than open-domain QA" (§5.5). They do not test this explanation directly. [INFERENCE: it is an interpretation, not a measured mechanism.]
2. **Abstention escalation under a non-Latin-script distractor.** Under the Hindi distractor, abstention rises from 0.082 to 0.248 for Phi-3-mini, from 0.098 to 0.250 for Mistral-7B, and from 0.352 to 0.730 for Qwen-2.5-3B (Table 4). For these three models, "hallucination rates fall significantly as abstention increases. These models are pulled toward refusal, not toward language-confused generation." (§5.2). Under `hi_long`, Qwen's abstention reaches 0.842 (§5.6).
3. **Script-switching confound (headline result).** Under the Hindi distractor, Llama-3.1-8B produces Devanagari on 58.2% of responses (Table 3). Its accuracy falls by 29 pp and the hallucination proxy rises by 29.4 pp, while abstention stays flat (0.066 → 0.062) (§5.2). Of 148 responses that were correct under `clean` and then switched script, "120 (81.1%) were semantically correct answers written in Devanagari script" (§5.3). After this adjustment the hallucination rate is 235/500 = 0.470, against a raw proxy of 0.710 and a clean baseline of 0.416 (§5.3).
4. **Script, not resource level.** For Llama-3.1-8B, the Chinese distractor yields 0% CJK output and a slightly lower hallucination rate (0.382; Δ=−0.034, p=0.009) (§5.4). Llama-3.2-3B uses the same tokenizer but switches script on only 1.2% of responses (§5.4).
5. **Multiple-choice format is robust.** "No accuracy drop is statistically significant under single-sentence conditions" for TruthfulQA (§5.1, Table 2). The exception is Llama-3.2-3B, which drops by 0.100 under `zh_long` (p<0.001).
6. **The failure taxonomy depends on the model.** The paper lists three modes: "(1) script-switching hallucination … (2) abstention escalation … and (3) stability" (§6).

## Short verbatim quotes (with locations)

- "A paragraph-length English distractor triggers near-universal abstention (0.806-0.998) across all models, consistent with reading-comprehension confusion" (Abstract)
- "These models are pulled toward refusal, not toward language-confused generation." (§5.2)
- "Our results suggest that such mismatches can cause widespread abstention independent of retrieval quality." (§5.5)
- "Any response degradation therefore reflects a failure of language-grounded instruction following rather than a failure of comprehension." (§3)
- "Abstention detection via substring matching may miss non-standard refusal formulations, particularly Mistral-7B's more discursive refusals." (§6, Limitations)

## Limitations

**Stated by the authors (§6 Limitations):**
- The distractors say outright that they are irrelevant. More naturalistic contamination "may produce larger effects".
- Only five open models are tested, all released in 2023–2024, in float16.
- Substring-based abstention detection.
- The authors state they lack training-data access needed to explain the Devanagari switching (§6).

**Our assessment [INFERENCE]:**
- (a) There is no evidence-sufficiency manipulation. TriviaQA is closed-book, so the paper cannot tell appropriate abstention from inappropriate abstention. A rise in "I don't know" is not shown to be over-abstention relative to what the model knows.
- (b) `wiki_para` has a single fixed paragraph, so it has no item-level variation.
- (c) There is no threshold or confidence-based abstention, only instructed abstention.
- (d) The abstract misstates the range across all models (see finding 1).
- (e) The paper's claim that the probe separates instruction-following from comprehension is asserted by design, not measured.

## How our work differs (exact statement)

Marwah et al. keep the English question fixed and add an irrelevant foreign-language or English sentence or paragraph to a **closed-book** factual QA prompt. They measure **instructed** abstention with substring matching. Our study is different in four ways:

1. We vary **the query itself** across EN, native-script Bengali, romanized Bengali and Bengali–English code-mixed renderings of the **same** item, with meaning equivalence validated by a second native speaker.
2. We supply **oracle evidence** under a controlled **sufficient vs. insufficient** manipulation, so that abstention can be scored as correct (UAR) or unnecessary (UNR).
3. We test whether a **confidence or sufficiency threshold calibrated on English dev data transfers** to the other variants (RQ2). Marwah et al. calibrate nothing.
4. We separate comprehension failure from miscalibration with a comprehension check (RQ3).

Marwah et al. do not study Bengali, romanized input, code-mixing, RAG with supplied evidence, or threshold transfer. [FACT, from full read, for the negatives listed]

## Relevance to H1-alt / RQ3

- **H1-alt (over-abstention on partly understood variants):** this paper gives indirect, setting-mismatched support. Some models respond to unexpected non-Latin-script context with more "I don't know" rather than more errors (Table 4, Hindi column). A context paragraph that is present but does not contain the answer also sharply raises abstention (Table 4, wiki column). [INFERENCE] The second result is a caution for our design. Our insufficient-evidence items present a passage without the answer, which is exactly the `wiki_para`-like situation. Our near-miss design (plan §5.2) and the sufficient-evidence condition are what let us tell appropriate abstention from format-driven abstention. UNR on *sufficient* items is the quantity that would show over-abstention.
- **RQ3:** the authors *assume* that comprehension is intact because the question stays in English. They do not measure it. Our RQ3 measures comprehension explicitly. [INFERENCE] Their script-switching confound also has a practical consequence for our scoring. Answers in BN or RBN may come back in a different script from the gold answer. Our deterministic normalisation (Bengali/ASCII digits, transliterated names) must handle this, or UAR and accuracy will be biased. This supports the planned normalisation unit tests.
- **Novelty threat: low.** The paper does not touch paired script variants, evidence sufficiency, or threshold transfer. It should be cited as related work on mixed-language context driving abstention. Our framing should not claim it shows over-abstention on *code-mixed* input. It does not.

## Note for the literature matrix (not edited here)

Row A5 in `literature_matrix.md` currently reads "near-universal abstention (0.806–0.998)", "English/Hindi distractors", and (in the §-summary) "mixed-language input can cause over-abstention (A5)". Suggested corrections:
- the across-model range per Table 4 is 0.424–0.998;
- the distractor languages are Spanish, Hindi and Chinese, plus an English paragraph;
- the near-universal abstention came from an **English** paragraph, not mixed-language input.

Status can move to `full-read`.

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
