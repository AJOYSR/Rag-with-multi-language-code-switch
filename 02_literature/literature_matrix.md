# Literature Matrix

**Verification levels**
- `metadata-verified`: title, authors and venue confirmed on an official page (proceedings, ACL Anthology, arXiv abs page) in this project.
- `abstract-read`: abstract or official summary read. Findings below come from that summary only.
- `full-read`: paper read in full; notes in `notes/<bibkey>.md`. **Only this level may support specific claims in the paper.**
- `found-only`: surfaced by search; existence not yet confirmed on an official page.

Last updated: 2026-10-23. Nothing is `full-read` yet; that is milestone M1.

---

## A. Closest works: must be full-read for Gate G1

| # | Bibkey | Study | Venue | Objective | Method | Key findings (as summarised) | Limitations / what it leaves open | Relevance | Status |
|---|---|---|---|---|---|---|---|---|---|
| A1 | `joren2025sufficient` | Sufficient Context: A New Lens on RAG Systems — Joren, Zhang, Ferng, Juan, Taly, Rashtchian | ICLR 2025 · arXiv 2411.06037 | Separate errors from insufficient context vs. failure to use sufficient context | Sufficiency autorater; analysis across models; selective generation using sufficiency + confidence | Strong models answer rather than abstain on insufficient context; smaller models hallucinate or abstain even with sufficient context; selective generation improves correct-answer fraction among responses by ~2–10% | English datasets only; no script/language variation | **Direct methodological basis** (M3 method; autorater prompts at github.com/hljoren/sufficientcontext) | metadata-verified, abstract-read |
| A2 | `feng2024abstain` | Teaching LLMs to Abstain across Languages via Multilingual Feedback — Feng, Shi, Wang, *et al.* | EMNLP 2024, pp. 4125–4150 · ACL 2024.emnlp-main.239 · arXiv 2406.15948 | Abstention in multilingual settings | Compares abstention strategies across languages; proposes multilingual feedback | Up to 20.5% gap between high- and low-resource languages; multilingual feedback is more equitable; culture affects which feedback languages help | Knowledge-QA abstention, not RAG with controlled evidence; script/code-mix variation not studied (to confirm) | **Closest prior on multilingual abstention.** Check whether Bengali is included and whether romanized input appears | metadata-verified, abstract-read |
| A3 | `thakur2024nomiracl` | NoMIRACL: Knowing When You Don't Know for Robust Multilingual RAG — Thakur, Bonifacio, Zhang, Ogundepo, Kamalloo, Alfonso-Hermelo, Li, Liu, Chen, Rezagholizadeh, Lin | Findings of EMNLP 2024 · arXiv 2312.11361 | Test whether LLMs recognise when retrieved passages lack an answer, across 18 languages | Human-annotated relevant / non-relevant subsets; hallucination rate and error rate | Most models trade hallucination on non-relevant sets against errors on relevant sets; GPT-4 gave the best trade-off | Relevance-based (whole passage set irrelevant), not minimal-edit sufficiency; no script variation | **Closest multilingual RAG abstention benchmark.** Confirm Bengali coverage (MIRACL lineage suggests yes `[UNVERIFIED]`) | metadata-verified, abstract-read |
| A4 | `khullar2025scriptgap` | Script Gap: Evaluating LLM Triage on Indian Languages in Native vs Romanized Scripts in a Real World Setting — Khullar, Desai, Malviya, Dalmia, Shi | arXiv 2512.10780 (v2 Mar 2026) | Native vs. romanized reliability in maternal-health triage | Real user queries; 5 Indian languages + Nepali; proposes uncertainty-based selective routing | Consistent romanized degradation of up to 24 points; "models that appear to understand romanized input may still fail to act on it reliably" | Classification triage, not RAG abstention; Bengali inclusion unconfirmed | **Strongest evidence that the script gap exists**; their selective routing is a related mitigation, so RQ4 must differ from or compare to it | metadata-verified, abstract-read |
| A5 | `marwah2026confusion` | Output Language Confusion under Multilingual Prompt Contamination — Marwah, Garimella, Bansal, Jain, Sheth | arXiv 2610.02926; NeurIPS 2026 LP4FM workshop | Effect of mixed-language distractors on factual answering | English/Hindi distractors inserted into prompts | Paragraph-length English distractor → near-universal abstention (0.806–0.998); framed as relevant to multilingual RAG | Distractor contamination, not paired script variants of the same query | Supports **H1-alt** (over-abstention) | metadata-verified, abstract-read |
| A6 | `zoumpoulidi2026solvability` | More Capable, Less Faithful: A Multilingual Analysis of Mathematical (Un)Solvability Detection in LLMs — Zoumpoulidi, Xiros, Paraskevopoulos | arXiv 2608.30463 (Aug 2026) | Paired solvable/unsolvable maths problems across languages | Extends ReliableMath to French and Greek; probing | Solvability belief largely language-agnostic internally; higher-resource languages show *lower* solvability-detection faithfulness | Maths, not RAG; EN/FR/EL only | Paired-design precedent; "internal belief vs. behaviour" angle for RQ3 | metadata-verified, abstract-read |

## B. Foundations and surveys

| # | Bibkey | Study | Venue | Relevance | Status |
|---|---|---|---|---|---|
| B1 | `wen2025abstention` | Know Your Limits: A Survey of Abstention in LLMs — Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang | TACL 13:529–556, 2025 · DOI 10.1162/tacl_a_00754 | Taxonomy and metrics for abstention; framing of Related Work | metadata-verified, abstract-read |
| B2 | — | Selective prediction / risk–coverage foundations (e.g., Geifman & El-Yaniv, *Selective classification for deep neural networks*, NeurIPS 2017; El-Yaniv & Wiener 2010) | — | Theory for thresholds, risk–coverage, AURC | found-only — verify |
| B3 | — | Calibration in LLMs (e.g., verbalized confidence; Kadavath et al. 2022 "Language Models (Mostly) Know What They Know") | — | M2 method background | found-only — verify |

## C. Adjacent: multilingual RAG, abstention benchmarks, romanization, Bengali

| # | Study | Venue | Relevance | Status |
|---|---|---|---|---|
| C1 | MIRAGE-Bench: Automatic Multilingual Benchmark Arena for RAG | arXiv 2410.13716 | Multilingual RAG generation evaluation, 18 languages, built on MIRACL; Bengali coverage `[UNVERIFIED]` | found-only (arXiv page seen in search) |
| C2 | CausalAbstain: Enhancing Multilingual LLMs with Causal Reasoning for Trustworthy Abstention | Findings of ACL 2025 · 2025.findings-acl.723 | Multilingual abstention method; possible baseline | found-only |
| C3 | AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions | arXiv 2506.09038 | General abstention benchmark; metric conventions | found-only |
| C4 | RomanSetu: Efficiently unlocking multilingual capabilities of LLMs via romanization | ACL 2024 (2024.acl-long.833) | Romanization can help models; counterpoint for H1 | found-only |
| C5 | BenHalluEval: Bengali multi-task hallucination benchmark (incl. code-mixed QA) | arXiv 2605.31483 (under review) | Closest Bengali hallucination resource; not RAG abstention | found-only |
| C6 | Indi-RomCoM: Code-Mixed Benchmark for Romanized Indic-English Instructions | arXiv 2606.30790 | Romanized code-mix degradation; Bengali inclusion `[UNVERIFIED]` | found-only |
| C7 | CodeMixBench | EMNLP 2025 | Code-mixed comprehension benchmark | found-only |
| C8 | Modeling Romanized Hindi and Bengali (transliteration dataset) | arXiv 2511.22769 | Possible transliteration tool for intervention (ii) | found-only |
| C9 | A. Sarker & Riya, *Calibration Language Changes How Quantized Models Fail* | author's own (`../Papers/`) | Motivating prior work | own work |

## D. Gap status (to update after M1)

- **Already known:** abstention degrades in low-resource languages (A2); romanized input degrades reliability (A4); multilingual RAG models trade hallucination against over-abstention (A3); sufficiency signals help selective generation in English (A1); mixed-language input can cause over-abstention (A5).
- **Apparently unresolved (abstract-level):** whether **thresholds / operating points transfer** across scripts of the *same* language under **controlled evidence sufficiency**, and how much of any gap is comprehension vs. calibration.
- **Open check items for G1:** full-read A1–A6; search arXiv (2025–2026) for "romanized" + "abstention", "code-mixed" + "RAG" + "unanswerable", "sufficient context" + "multilingual"; check the citing papers of A1 and A2 on Semantic Scholar or Google Scholar.
