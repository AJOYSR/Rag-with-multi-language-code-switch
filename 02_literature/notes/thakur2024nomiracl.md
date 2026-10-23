# thakur2024nomiracl — "Knowing When You Don't Know": A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation (NoMIRACL)

**Status:** full-read (all 19 pages of the ACL Anthology PDF, including Limitations, Appendices A–E, Tables 1–9 and Figures 1–10 captions), 2026-10-23.
**Read by:** AI agent (Claude), from text extracted with `pypdf` from the official Anthology PDF. Figures 1, 3, 5, 6, 7, 8 and 9 are images. Only their captions, and any numbers in the running text, were read. **Per-model, per-language values that appear only in Figures 5/6/8/9 were NOT read** (e.g., GPT-4's Bengali hallucination rate is not recorded here).
**Page convention:** "p. N" = proceedings page printed in the PDF footer (PDF page 1 = p. 12508).

## 1. Bibliographic metadata

- **[FACT] Title changed.** The matrix lists the title as "NoMIRACL: Knowing When You Don't Know for Robust Multilingual RAG". The **official published title** (Anthology, PDF title page, and arXiv abs page v3) is: **"Knowing When You Don't Know": A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation**. "NoMIRACL" is the dataset name used in the text. The bib entry and matrix must use the official title. The Anthology bibkey is `thakur-etal-2024-knowing`.
- **Authors (11, in order, from the Anthology BibTeX):** Nandan Thakur, Luiz Bonifacio, Crystina Zhang, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Boxing Chen, Mehdi Rezagholizadeh, Jimmy Lin. *Note:* the PDF title page prints the third author as "Xinyu Zhang", while the Anthology metadata uses "Crystina Zhang". Use the Anthology form in the bib.
- **Affiliations (p. 12508):** University of Waterloo; Huawei Noah's Ark Lab; FEEC-Unicamp, Brazil.
- **Venue:** Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, November 2024. Editors: Al-Onaizan, Bansal, Chen. ACL.
- **Anthology ID:** 2024.findings-emnlp.730
- **Pages:** 12508–12526 (the BibTeX field and the PDF footer agree)
- **DOI:** 10.18653/v1/2024.findings-emnlp.730
- **URL:** https://aclanthology.org/2024.findings-emnlp.730/ (PDF: https://aclanthology.org/2024.findings-emnlp.730.pdf)
- **arXiv:** 2312.11361. Versions: v1 18 Dec 2023, v2 4 Mar 2024, v3 10 Nov 2024. Comment field: "EMNLP 2024 (Findings)". The arXiv abs page title now matches the Anthology title.
- **Code/data:** https://github.com/project-miracl/nomiracl (abstract, p. 12508); HF dataset `miracl/nomiracl`.

BibTeX (fetched from https://aclanthology.org/2024.findings-emnlp.730.bib on 2026-10-23):

```bibtex
@inproceedings{thakur-etal-2024-knowing,
    title = "``Knowing When You Don{'}t Know'': A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation",
    author = "Thakur, Nandan  and Bonifacio, Luiz  and Zhang, Crystina  and Ogundepo, Odunayo  and Kamalloo, Ehsan  and Alfonso-Hermelo, David  and Li, Xiaoguang  and Liu, Qun  and Chen, Boxing  and Rezagholizadeh, Mehdi  and Lin, Jimmy",
    editor = "Al-Onaizan, Yaser  and Bansal, Mohit  and Chen, Yun-Nung",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {EMNLP} 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.730/",
    doi = "10.18653/v1/2024.findings-emnlp.730",
    pages = "12508--12526"
}
```

## 2. Objective

The paper builds a human-annotated multilingual dataset to test whether LLMs, given top-k retrieved passages, can tell when **none** of the passages contains the answer and should say "I don't know", versus when at least one relevant passage is present (abstract and §1, pp. 12508–12509). The task is framed as **binary relevance classification** over the passage set, not as answer generation: "we evaluate whether a passage is relevant or non-relevant for a given query, instead of evaluating actual answer spans" (§10 Limitations item 2, p. 12517).

## 3. Data

- **Construction (§3.1, p. 12510):** same procedure as MIRACL (Zhang et al., 2023, TACL). Native-speaker annotators write a query from a prompt made of the first 100 words of a Wikipedia passage. Top-k passages are retrieved with a hybrid of BM25, mDPR and mColBERT (§4.1, p. 12511). Annotators then give binary relevance labels to each query–passage pair. 31 native-speaker annotators were hired, not crowd-sourced (§1 p. 12509; App. C p. 12522).
- **How "non-relevant" is defined (§3.1, pp. 12510–12511):** queries whose top-k (k ≤ 10) passages were **all** judged non-relevant (relevance = 0). The paper gives two reasons such queries arise: (i) the query is too generic or too specific for Wikipedia to contain the information; (ii) spelling mistakes in query generation. Non-relevance is therefore an **organic retrieval failure**. It is not a controlled edit of an otherwise answerable passage.
- **Relevant subset:** queries with at least one passage judged relevant, "to provide sufficient information to answer the query" (§3.1, p. 12511). These passage sets also contain non-relevant passages. The relevant dev and test splits reuse MIRACL dev and MIRACL test-B queries (§3.2, p. 12511).
- **Splits (§3.2, p. 12511):** the non-relevant subset is randomly split 44% dev / 56% test. Dev and test are disjoint.
- **Sizes (Table 1, p. 12511), all 18 languages:** non-relevant dev 10,922, test 13,903; relevant dev 13,495, test 17,737. §1 says "over 56,000" samples.
- **Experiments use a subsample:** at most 250 queries per language and subset (§3.3 and §4.3, pp. 12511–12512). This came to ≈20K API calls costing US$1,474 (p. 12513).
- **Passage truncation:** each passage is cut to its first 375 tokens to fit k = 10 into 4,096 tokens (§4.3, p. 12512).
- **Languages (§3.3, p. 12511; Table 1):** ar, bn, de, en, es, fa, fi, fr, hi, id, ja, ko, ru, sw, te, th, yo, zh. Footnote 3: "10 families ... and 11 scripts". *Minor erratum:* the prose list in §3.3 omits Telugu (te), but Table 1 and all result tables include it. The GitHub README's "Languages covered" line also omits te, while its own example command lists te.
- **Corpus:** language-specific Wikipedia. The Mr. TyDi languages use an early-2019 dump; the rest use March 2022 (App. C, p. 12522).
- **Quality control (App. D, p. 12522):** "on average agreements of over 80% on query–passage relevance".

### Bengali (bn) coverage — confirmed

- **[FACT] Paper, Table 1 (p. 12511), bn column:** non-relevant dev **495**, test **630**; relevant dev **411**, test **1,130**.
- **[FACT] HF dataset (checked 2026-10-23):** `https://huggingface.co/datasets/miracl/nomiracl` has folder `data/bengali/` with `corpus.jsonl.gz`, `topics/{dev,test}.{relevant,non_relevant}.tsv` and `qrels/...`. The loader `nomiracl.py` defines config `name="bengali"`. Line counts of the four Bengali topic files, fetched today: dev.non_relevant 495, dev.relevant 411, test.non_relevant 630, test.relevant 1130. **These exactly match Table 1.** The queries are in Bengali script; e.g., the first test.non_relevant line is `304236#0  আপেল কোম্পানির প্রতিষ্ঠাতা কে?`.
- Bengali is available in **all four** subset × split combinations (`dev.relevant`, `dev.non_relevant`, `test.relevant`, `test.non_relevant`).
- *Note:* the HF card's YAML `language:` list has 16 codes and omits `de` and `yo`. However, `data/german` and `data/yoruba` exist. This is a metadata slip and does not affect bn.

### Licence — DISCREPANCY (open question Q5)

- **Paper (App. B, p. 12522):** "We follow the same license as Wikipedia for NoMIRACL: Creative Commons Attribution-ShareAlike 4.0 Unported License (CC BY-SA 4.0)."
- **HF dataset card YAML** (https://huggingface.co/datasets/miracl/nomiracl, repo sha ecd08778…, lastModified 2024-11-23): `license: apache-2.0`.
- **GitHub repo** (https://github.com/project-miracl/nomiracl, LICENSE file, latest commit 9c787daa… on 2024-11-29): Apache License 2.0. This probably covers the code. [INFERENCE]
- **[REC]** Treat the **data** as CC BY-SA 4.0. That is the more restrictive licence, the one the paper states, and the one consistent with Wikipedia source text. Apache-2.0 may cover the code and possibly the annotations. If we redistribute any NoMIRACL passages (e.g., as RAG evidence), our derived data would inherit ShareAlike. Record both licences in `03_data/raw/SOURCES.csv` with this note. An author email to resolve it is the human's decision.

## 4. Method

- **Prompt (Figure 4, p. 12512), zero-shot "vanilla":** "I will give you a question and several contexts containing information about the question. Read the contexts carefully. If any of the contexts answers the question, respond as either "Yes, answer is present" or "I don't know"". It is followed by QUESTION and CONTEXTS [1]…[10] (title: text).
- **Language of the prompt:** the instruction is in English; the query and passages are in the target language. "We construct a vanilla prompt template using all top-k (oracle) passages ... along with the input query, both in the same language" (§4.3, p. 12512). "The instruction is provided in English, similar to Ahuja et al. (2023)" (Fig. 4 caption).
- **Models (§4.2, p. 12512; Table 5, p. 12523), 14 checkpoints:** GPT-4o, GPT-4, GPT-3.5-turbo (Azure); Mistral-7B-Instruct-v0.3, Mixtral-8x7B-Instruct-v0.1; Orca-2-7B/13B; Aya-101, Aya-23-35B; Llama-2-7b/13b/70b-chat; Meta-Llama-3-8B/70B-Instruct. *Note:* §4.2 says "eleven state-of-the-art LLMs", but 14 checkpoints are listed (inconsistent count in the paper).
- **Decoding (§4.3, p. 12512):** temperature 0.1, top-p 0.95, max 50 output tokens, max input 4,096 tokens.
- **Abstention detection:**
  - Paper (§4.1, p. 12512): the output is "either y = "I don't know" as negative (N) or "Yes, answer is present" as positive (P). The output is tagged "Invalid" if it does not fall in either one of the above."
  - Released code (`nomiracl/prompts/template.py`, `VanillaTemplate.postprocess`, read 2026-10-23): rule-based string matching on lower-cased output. The rules, in order:
    1. If both strings appear, label "answer" if "yes, answer is present" occurs more than once, else Invalid.
    2. Else "i don't know" → no-answer.
    3. Else "yes, answer is present" → answer.
    4. Else "answer is present" → answer; "answer is not present" → no-answer; a short (<10 chars) output containing "[n]" → answer.
    5. Otherwise Invalid.
  - There is **no confidence score, probability or threshold**. Abstention is a discrete string label.
  - [INFERENCE] The code (`nomiracl/eval/metrics.py`, `ConfusionMetric`) divides by **all** outputs, Invalid included (e.g., hallucination = #"Yes" / (#Yes + #IDK + #Invalid)). The paper formula FP/(FP+TN) does not mention Invalid. Whether the published figures exclude invalids is not stated in the text I read.
- **Further studies (§7, pp. 12514–12515):** three prompt variants (role, repeat, explanation; Fig. 10) on Mistral-7B. LoRA SFT of Mistral-7B and Llama-3-8B on the NoMIRACL dev split for all 18 languages (Tables 4, 6, 7).
- **Error analysis (§6, Table 2, p. 12515):** manual categorisation of outputs, **English only**.

## 5. Languages: romanized or code-mixed?

**[FACT] None.** All queries and passages are in each language's native script, drawn from that language's Wikipedia. Bengali queries are in Bengali script (verified in the HF topic file). I searched the full extracted text for "roman", "code-mix", "translit" and "script". The only "script" hit is footnote 3 ("11 scripts"); there are no hits for romanization, transliteration or code-mixing. **No item is presented in more than one script or language.** Each language has its own, different query set, so items are not parallel across languages. [INFERENCE from §3.1: queries are written per language by native annotators from that language's Wikipedia.]

## 6. Metrics (verbatim, §2.1 p. 12510; repeated in §4.1 p. 12512)

- "we compute the hallucination rate (in %) = FP/(FP+TN) which measures the model's tendency to hallucinate an answer, when no answer is available in all of the passages in the non-relevant subset."
- "we measure the error rate (in %) = FN/(FN + TP) which measures the model's ability to identify the answer present within the passages in the relevant subset."
- The confusion matrix (Fig. 2, p. 12509) uses rows LLM "Yes, answer is present" (FP | TP) and LLM "I don't know" (TN | FN), with columns Non-Relevant | Relevant.
- Figure 7 (p. 12514) plots the "average model accuracy" on each subset.
- Mapping to our metrics [INFERENCE]: hallucination rate ≈ our **UAR**, restricted to the insufficient condition. Error rate ≈ our **UNR**, restricted to the sufficient condition. The difference is that NoMIRACL scores only the relevance decision, not whether an answer is produced or correct.

## 7. Key findings (with locations)

1. **Trade-off between the two failure modes** (abstract, p. 12508): "Models such as LLAMA-2 and Orca-2 achieve over 88% hallucination rate on the non-relevant subset. Mistral and LLAMA-3 hallucinate less but can achieve up to a 74.9% error rate on the relevant subset. Overall, GPT-4 is observed to provide the best tradeoff on both subsets." *(I could not trace the 74.9% figure to any table or running-text number. It may come from Figure 9, which I could not read.)*
2. **Non-relevant subset (§5.1, p. 12513):** "all LLMs (except Mistral) hallucinate that an answer is present across all languages, thereby indicating their poor ability to abstain from answering." Average hallucination: Mixtral 17.4% (lowest), Llama-3-8B 26.8%, GPT-4 35.5%. Llama-2, Orca-2 and Aya-101 are above 80%.
3. **Bengali is the worst case for GPT-3.5 (§5.1, p. 12513):** "GPT-3.5 (cf. Figure 8) is observed with the highest deviation across languages with a hallucination rate as low as 25.2% on Swahili (sw) to 95.2% on Bengali (bn)."
4. **The authors' explanation of cross-language differences is item difficulty, not language competence** (§5.1, p. 12513): "We hypothesize that queries in low-resource languages (smaller Wikipedia corpus) contain retrieved information, likely to be non-relevant (easier negative), thereby making it easier for the LLM to judge as "I don't know"." Also: "LLMs perform poorly to identify non-relevant passages as they are highly similar to the query, but do not contain the exact answer." [INFERENCE] This admits that per-language comparisons in NoMIRACL are confounded by different query/passage sets. That is exactly the confound our paired design removes.
5. **Relevant subset (§5.2, p. 12514):** Aya-101 has the highest average error rate (62.5%). Llama-2-70B and GPT-4o are below 10%. Aya-101, Mixtral and Llama-3-8B are above 40%.
6. **Overall (§5.3, p. 12514):** "Mistral and LLAMA-3 suffer less from hallucination on the non-relevant subset but observe a higher error rate (over 40%) on the relevant subset, indicating they are not confident in identifying passages containing the answer."
7. **Prompt variants move the operating point in opposite directions** (§7, p. 12515; Table 3, p. 12516; Mistral-7B, 18-language averages): role and repeat reduce the error rate by 6.3 and 15.2 points but raise hallucination by 8.7 and 15.9 points; explanation reduces hallucination by 9.7 points but raises error by 8.3 points. Their conclusion: "the user will be required to choose their technique depending on whether they wish to be better on the non-relevant subset by reducing the hallucination rate or the relevant subset by reducing the error rate."
8. **SFT is unstable and language-specific** (§7, p. 12515; Tables 4 and 7): "For a few languages mentioned in Table 7 such as Arabic (ar) the LLM always outputs "Yes, answer is present", whereas for Bengali (bn) heavily relies on "I don't know"."
9. **English-only failure taxonomy** (§6, Table 2, p. 12515): Llama-2-13B repeats the question or instruction in 64.8% of non-relevant outputs. Mistral-7B gives "I don't know" with an explanation in 88.4%. Orca-2-7B uses synonyms such as "No, answer is not present".

### Bengali numbers reported in tables (all test split, ≤250 queries per subset)

| Source | Model / setting | bn hallucination % | bn error % | 18-lang avg (hall / err) |
|---|---|---|---|---|
| Table 3 / Table 7 (pp. 12516, 12524) | Mistral-7B-v0.3, vanilla | 63.2 | 20.4 | 40.0 / 25.5 |
| Table 3 | Mistral-7B + Role | 60.0 | 23.6 | 48.7 / 19.2 |
| Table 3 | Mistral-7B + Repeat | 72.4 | 12.4 | 55.9 / 10.3 |
| Table 3 | Mistral-7B + Explanation | 33.6 | 39.6 | 30.3 / 33.8 |
| Table 7 | Llama-3-8B-Instruct | 20.0 | 56.0 | 26.8 / 45.3 |
| Table 7 | Llama-3-8B + SFT | 12.5 | 70.8 | 44.7 / 34.7 |
| Table 7 | Mistral-7B + SFT | 33.2 | 60.8 | 44.3 / 46.1 |
| §5.1 text | GPT-3.5 | 95.2 | — | — |

[INFERENCE] For vanilla Mistral-7B, Bengali has the second-highest hallucination rate of the 18 languages (after te at 74.0). For Llama-3-8B, Bengali hallucination is below average but its error rate is above average. So the direction of Bengali's deviation from the average depends on the model. This is the same over-abstention vs. over-answering ambiguity as our H1 vs. H1-alt.
*Minor inconsistency:* the vanilla Mistral-7B ar hallucination is 40.0 in Table 3 but 40.4 in Table 7. Bengali values agree across both tables.

## 8. Limitations

Stated by the authors (§10, p. 12517):
- possible human annotation errors;
- relevance-only evaluation, not answer spans;
- Wikipedia-only domain ("for low-resource languages such as Bengali or Yoruba, finding a suitable large enough text corpora is difficult").

Additional [INFERENCE] from this reading:
- (a) Non-relevance is organic, so sufficient and insufficient items are different queries, not minimal pairs.
- (b) Items are not parallel across languages, so language effects are confounded with item difficulty (the authors' own hypothesis in §5.1).
- (c) Native script only; there are no romanized or code-mixed inputs.
- (d) Only a binary string label: no confidence, thresholds, coverage–risk curves or calibration.
- (e) Single English instruction, temperature 0.1, single run, no confidence intervals or significance tests reported.
- (f) Training-data contamination of Wikipedia content is not controlled. Table 2 shows Aya-101 "uses implicit memory to answer" (10.8% non-relevant, 42.0% relevant, en).
- (g) Only k = 10 multi-passage sets; there is no single-passage controlled evidence.
- (h) The paper's metric formula and the code's denominator may differ on Invalid outputs.

## 9. How our work differs (exact statement)

NoMIRACL measures, across 18 native-script languages, whether LLMs label a retrieved top-10 Wikipedia passage set as containing an answer ("Yes, answer is present") or not ("I don't know"). Each language has its own query set, and insufficiency arises organically when no retrieved passage is relevant. Our study holds the item, its meaning and its evidence fixed, and varies only the **surface form of the same question**: EN, BN native script, romanized Bengali (RBN) and Bengali–English code-mixed (CM). Sufficiency is controlled by a **minimal edit** to a single passage. We measure both unsupported answers and unnecessary abstentions on the produced answers. Most importantly, we test whether a **confidence or sufficiency threshold calibrated on English transfers** to the other variants, and separate comprehension failure from miscalibration. NoMIRACL has no romanized or code-mixed inputs, no paired cross-language items, no threshold or score-based abstention, and no transfer analysis.

## 10. Does this paper already answer our RQ2 (threshold transfer)?

**No.** [FACT] NoMIRACL uses no confidence scores, thresholds, risk–coverage curves or selective prediction (§4.1; code `postprocess`). Abstention is a discrete string label. It does not calibrate in one language and evaluate in another. The SFT experiment trains jointly on all 18 languages (§7). It also has no cross-script condition, so RQ1's RBN/CM arms are not covered either.

Partial relevance:
- (i) It provides **Bengali native-script evidence** that abstention behaviour differs from other languages (GPT-3.5 at 95.2% hallucination; Mistral-7B at 63.2%). This supports including BN, but it is confounded by item differences.
- (ii) §7 shows that prompt wording moves the hallucination/error operating point by 6–16 points. This supports our plan to test instruction paraphrases as a robustness check.

**Novelty threat:** low for RQ2 and for RBN/CM. It is moderate only for a weak framing such as "multilingual RAG abstention including Bengali", which NoMIRACL already covers and which we must not claim as new.

## 11. Verbatim quotes for spot-checking (page = proceedings page)

1. "Queries in the non-relevant subset contain passages judged as non-relevant, whereas queries in the relevant subset include at least a single judged relevant passage." (Abstract, p. 12508)
2. "The LLM generates an answer output containing either y = "I don't know" as negative (N) or "Yes, answer is present" as positive (P). The output is tagged "Invalid" if it does not fall in either one of the above." (§4.1, p. 12512)
3. "GPT-3.5 (cf. Figure 8) is observed with the highest deviation across languages with a hallucination rate as low as 25.2% on Swahili (sw) to 95.2% on Bengali (bn)." (§5.1, p. 12513)
4. "We hypothesize that queries in low-resource languages (smaller Wikipedia corpus) contain retrieved information, likely to be non-relevant (easier negative), thereby making it easier for the LLM to judge as "I don't know"." (§5.1, p. 12513)
5. "In our work, we evaluate whether a passage is relevant or non-relevant for a given query, instead of evaluating actual answer spans." (§10, p. 12517)
6. "We follow the same license as Wikipedia for NoMIRACL: Creative Commons Attribution-ShareAlike 4.0 Unported License (CC BY-SA 4.0)." (App. B, p. 12522)
7. "for Bengali (bn) heavily relies on "I don't know"." (§7, p. 12515, describing Llama-3-8B after SFT)
8. "We use a zero-shot "vanilla" prompt template for prompting all LLMs." (§1, p. 12509)

## 12. Inaccessible or unchecked

- Plotted per-language values in Figures 5, 6, 8 and 9 (image-only). This includes Bengali rates for GPT-4, GPT-4o, Aya, Orca-2, Llama-2 and Llama-3-70B.
- The source of the abstract's "74.9% error rate".
- Whether the reported rates exclude Invalid outputs.
- The released baseline output files under `results/baselines/` in the GitHub repo were not downloaded.
- Papers citing NoMIRACL were not searched here; that belongs to the G1 search log.

---
**Quote verification (lead, 2026-10-23):** every verbatim quote in this file was string-matched against the fetched source text (arXiv HTML or ACL Anthology PDF) by `qcheck.py`; unmatched strings were checked by hand and were either non-quote text (metadata, ellipses, paraphrase labels) or were corrected. Status: full-read.
