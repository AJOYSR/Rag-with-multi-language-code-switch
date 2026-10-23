# Novelty Search Log — Topic 1 (Gate G1)

Date of all searches: **2026-10-23** (agent session; system clock UTC+6). Searcher: AI research agent (Claude), on behalf of A. Sarker.
Purpose: test the candidate gap in `01_planning/research_plan.md` §2 — *no prior work tests, under controlled evidence sufficiency, whether an abstention rule/threshold calibrated in English transfers to BN, RBN and CM versions of the same RAG question, separating comprehension from calibration.*

**Status labels used below.** `found-only` = surfaced by a search result/snippet; existence not confirmed on an official page. `metadata-verified` = official abs/proceedings page opened in this session. `abstract-read` = abstract read in this session (arXiv API returns the official abstract; abs page opened for the top threats). **No paper below is `full-read`.** Nothing here may support a specific claim in the paper until it is full-read.

## Method notes and caveats (read before using the counts)

- **arXiv**: official export API (`https://export.arxiv.org/api/query`), `max_results=100`; hit count = `opensearch:totalResults`. Titles and abstracts of all returned entries were screened. Caveat [FACT, observed]: the API stems terms, so `romanized` also matches "Roman" (e.g., *Nancy Grace Roman Space Telescope*); AX16 and AX32 are dominated by astronomy noise. Counts from the arXiv API for multi-term AND queries were small; this reflects the API's matching, and a 0 does not prove absence.
- **ACL Anthology**: the Anthology's own search is a Google custom-search widget that cannot be called programmatically here. Searches were run through the agent's WebSearch tool with `site:aclanthology.org`; the tool reports no hit count (→ "n/a") and only partly honoured the site filter (arXiv pages also returned). This source is therefore **weakly covered**; treat ACL rows as a supplement, not a systematic Anthology search. [REC] Author to repeat ACL1–ACL8 in the Anthology search box.
- **Semantic Scholar**: Graph API without key. The API returned **HTTP 429 (rate-limited)** for most calls. Of 15 search attempts, **3 succeeded and 12 failed** (logged individually). The two citation-chase calls **succeeded**. The citation-count metadata call for A1 failed (429); for A2 it succeeded (`citationCount` = 20).
- **Google Scholar**: plain HTTPS fetch of the results page, page 1 only. 6 of the first 14 queries returned the CAPTCHA/"unusual traffic" page (**blocked**); all 6 were retried after a pause and returned results (GS15–GS20). Where the results page did not contain the "About N results" string, the count is recorded as "not reported on parsed page" — **no count was inferred**. A later single title lookup was blocked. Scholar counts are approximate by design.
- Raw API/HTML-derived outputs were saved to the agent's session scratchpad (not in the project tree; ephemeral). [REC] If the author wants an audit trail, re-run the arXiv rows (deterministic URLs given) or ask the agent to copy the JSON into `02_literature/`.

## Search table

| # | Date | Source | Exact query string / URL | Hit count (as reported by the source; "n/a" if not reported) | Screened | Relevant hits (titles + IDs) |
|---|---|---|---|---|---|---|
| AX1 | 2026-10-23 | arXiv API | `all:romanized AND all:abstention` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3Aabstention&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX2 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:RAG AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3ARAG+AND+all%3Aunanswerable&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX3 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:retrieval AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3Aretrieval+AND+all%3Aunanswerable&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX4 | 2026-10-23 | arXiv API | `all:"sufficient context" AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3A%22sufficient+context%22+AND+all%3Amultilingual&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX5 | 2026-10-23 | arXiv API | `all:transliteration AND all:"selective prediction"` — https://export.arxiv.org/api/query?search_query=all%3Atransliteration+AND+all%3A%22selective+prediction%22&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX6 | 2026-10-23 | arXiv API | `all:Bengali AND all:hallucination AND all:retrieval` — https://export.arxiv.org/api/query?search_query=all%3ABengali+AND+all%3Ahallucination+AND+all%3Aretrieval&start=0&max_results=100 | 2 | 2 titles (+abstracts) | Bengali Hallucination Detection with Retrieval and Programs (adjacent: Bengali, detection not abstention) [arXiv:2610.22892]; BanglAssist (adjacent: BN-EN code-switching RAG chatbot; no abstention eval in abstract) [arXiv:2503.22283] |
| AX7 | 2026-10-23 | arXiv API | `all:romanized AND all:hallucination` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3Ahallucination&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX8 | 2026-10-23 | arXiv API | `all:abstention AND all:"cross-lingual" AND all:threshold` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3A%22cross-lingual%22+AND+all%3Athreshold&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX9 | 2026-10-23 | arXiv API | `all:abstention AND all:"cross-lingual" AND all:calibration` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3A%22cross-lingual%22+AND+all%3Acalibration&start=0&max_results=100 | 1 | 1 titles (+abstracts) | MKA: Cross-Lingual Consensus for Model Abstention (abstention incl. Bengali; no script variants) [arXiv:2503.23687] |
| AX10 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:abstain` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3Aabstain&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX11 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:abstention` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3Aabstention&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX12 | 2026-10-23 | arXiv API | `all:Bangla AND all:RAG AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3ABangla+AND+all%3ARAG+AND+all%3Aunanswerable&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX13 | 2026-10-23 | arXiv API | `all:Bangla AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3ABangla+AND+all%3Aunanswerable&start=0&max_results=100 | 1 | 1 titles (+abstracts) | NCTB-QA (Bangla unanswerable QA; encoder models, no LLM abstention/scripts) [arXiv:2603.05462] |
| AX14 | 2026-10-23 | arXiv API | `all:Bengali AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3ABengali+AND+all%3Aunanswerable&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX15 | 2026-10-23 | arXiv API | `all:"selective prediction" AND all:multilingual AND all:calibration` — https://export.arxiv.org/api/query?search_query=all%3A%22selective+prediction%22+AND+all%3Amultilingual+AND+all%3Acalibration&start=0&max_results=100 | 1 | 1 titles (+abstracts) | Estimating Uncertainty from Reasoning: multi-/cross-lingual MCQA (threshold selection for selective prediction across 22 languages) — THREAT for RQ2 [arXiv:2607.06327] |
| AX16 | 2026-10-23 | arXiv API | `all:romanized AND all:calibration` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3Acalibration&start=0&max_results=100 | 115 | 100 titles (+abstracts) | none relevant |
| AX17 | 2026-10-23 | arXiv API | `all:romanized AND all:RAG` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3ARAG&start=0&max_results=100 | 5 | 5 titles (+abstracts) | none relevant |
| AX18 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:calibration AND all:confidence` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3Acalibration+AND+all%3Aconfidence&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX19 | 2026-10-23 | arXiv API | `all:abstention AND all:multilingual AND all:"retrieval-augmented"` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3Amultilingual+AND+all%3A%22retrieval-augmented%22&start=0&max_results=100 | 3 | 3 titles (+abstracts) | MTRACE (FR/EN RAG with abstention prompt; no scripts) [arXiv:2512.12694]; Output Language Confusion (A5; already in matrix) [arXiv:2610.02926] |
| AX20 | 2026-10-23 | arXiv API | `all:"context sufficiency" AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3A%22context+sufficiency%22+AND+all%3Amultilingual&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX21 | 2026-10-23 | arXiv API | `all:"selective generation" AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3A%22selective+generation%22+AND+all%3Amultilingual&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX22 | 2026-10-23 | arXiv API | `all:"code-switching" AND all:abstention` — https://export.arxiv.org/api/query?search_query=all%3A%22code-switching%22+AND+all%3Aabstention&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX23 | 2026-10-23 | arXiv API | `all:transliterated AND all:unanswerable` — https://export.arxiv.org/api/query?search_query=all%3Atransliterated+AND+all%3Aunanswerable&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX24 | 2026-10-23 | arXiv API | `all:romanized AND all:Bengali AND all:LLM` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3ABengali+AND+all%3ALLM&start=0&max_results=100 | 1 | 1 titles (+abstracts) | Modeling Romanized Hindi and Bengali (C8; tool) [arXiv:2511.22769] |
| AX25 | 2026-10-23 | arXiv API | `all:abstention AND all:romanization` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3Aromanization&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX26 | 2026-10-23 | arXiv API | `all:unanswerable AND all:multilingual AND all:RAG` — https://export.arxiv.org/api/query?search_query=all%3Aunanswerable+AND+all%3Amultilingual+AND+all%3ARAG&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX27 | 2026-10-23 | arXiv API | `all:"insufficient context" AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3A%22insufficient+context%22+AND+all%3Amultilingual&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AX28 | 2026-10-23 | arXiv API | `all:abstain AND all:Bengali` — https://export.arxiv.org/api/query?search_query=all%3Aabstain+AND+all%3ABengali&start=0&max_results=100 | 1 | 1 titles (+abstracts) | MKA: Cross-Lingual Consensus for Model Abstention (abstention incl. Bengali; no script variants) [arXiv:2503.23687] |
| AX29 | 2026-10-23 | arXiv API | `all:transliteration AND all:abstention` — https://export.arxiv.org/api/query?search_query=all%3Atransliteration+AND+all%3Aabstention&start=0&max_results=100 | 1 | 1 titles (+abstracts) | none relevant |
| AX30 | 2026-10-23 | arXiv API | `all:"code-mixed" AND all:hallucination` — https://export.arxiv.org/api/query?search_query=all%3A%22code-mixed%22+AND+all%3Ahallucination&start=0&max_results=100 | 6 | 6 titles (+abstracts) | Does the Truthfulness Signal Survive Code-Mixing? (Hinglish probe transfer) — adjacent THREAT for RQ2 framing [arXiv:2609.22138]; BenHalluEval (C5; already in matrix) [arXiv:2605.31483] |
| AX31 | 2026-10-23 | arXiv API | `all:Hinglish AND all:hallucination` — https://export.arxiv.org/api/query?search_query=all%3AHinglish+AND+all%3Ahallucination&start=0&max_results=100 | 1 | 1 titles (+abstracts) | Does the Truthfulness Signal Survive Code-Mixing? (Hinglish probe transfer) — adjacent THREAT for RQ2 framing [arXiv:2609.22138] |
| AX32 | 2026-10-23 | arXiv API | `all:romanized AND all:uncertainty` — https://export.arxiv.org/api/query?search_query=all%3Aromanized+AND+all%3Auncertainty&start=0&max_results=100 | 123 | 100 titles (+abstracts) | Script Gap (A4; already in matrix) [arXiv:2512.10780]; Neither Here Nor There (code-mixed representations; background) [arXiv:2603.19771] |
| AX33 | 2026-10-23 | arXiv API | `all:abstention AND all:script AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3Ascript+AND+all%3Amultilingual&start=0&max_results=100 | 1 | 1 titles (+abstracts) | Output Language Confusion (A5; already in matrix) [arXiv:2610.02926] |
| AX34 | 2026-10-23 | arXiv API | `all:"native script" AND all:romanized AND all:LLM` — https://export.arxiv.org/api/query?search_query=all%3A%22native+script%22+AND+all%3Aromanized+AND+all%3ALLM&start=0&max_results=100 | 8 | 8 titles (+abstracts) | RomanLens (latent romanization; background) [arXiv:2502.07424]; RomanSetu (C4) [arXiv:2401.14280]; Script Gap (A4; already in matrix) [arXiv:2512.10780]; Modeling Romanized Hindi and Bengali (C8; tool) [arXiv:2511.22769]; Indi-RomCoM (C6) [arXiv:2606.30790]; BanglaShield (paired BN native/romanized/code-mixed; safety) — design precedent for RQ1 [arXiv:2610.24288] |
| AX35 | 2026-10-23 | arXiv API | `all:abstention AND all:"low-resource" AND all:languages` — https://export.arxiv.org/api/query?search_query=all%3Aabstention+AND+all%3A%22low-resource%22+AND+all%3Alanguages&start=0&max_results=100 | 2 | 2 titles (+abstracts) | A2 (Feng et al.) [arXiv:2406.15948]; Estimating Uncertainty from Reasoning: multi-/cross-lingual MCQA (threshold selection for selective prediction across 22 languages) — THREAT for RQ2 [arXiv:2607.06327] |
| AX36 | 2026-10-23 | arXiv API | `all:"risk control" AND all:multilingual` — https://export.arxiv.org/api/query?search_query=all%3A%22risk+control%22+AND+all%3Amultilingual&start=0&max_results=100 | 2 | 2 titles (+abstracts) | none relevant |
| AX37 | 2026-10-23 | arXiv API | `all:"conformal" AND all:multilingual AND all:abstention` — https://export.arxiv.org/api/query?search_query=all%3A%22conformal%22+AND+all%3Amultilingual+AND+all%3Aabstention&start=0&max_results=100 | 0 | 0 titles (+abstracts) | none relevant |
| AXT1 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Answerability Probing"` | 1 | all | 1 hit, irrelevant (2608.30345) |
| AXT2 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Calibrated LLM-as-a-judge"` | 0 | all | 0 |
| AXT3 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Confidence-Aware Hallucination Detection"` | 0 | all | 0 |
| AXT4 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Paired Study of Code-Mixed"` | 1 | all | 1 (2606.05654) |
| AXT5 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Smishing Detection in Code-Mixed"` | 0 | all | 0 |
| AXT6 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Clarification Failure"` | 0 | all | 0 |
| AXT7 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Calibration Transfer Gap"` | 0 | all | 0 |
| AXT8 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Two Axes of LLM Abstention"` | 1 | all | 1 (2607.08456) |
| AXT9 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Indian Code-Mixed Queries"` | 0 | all | 0 |
| AXT10 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `ti:"Probe Before"` | 2 | all | 2, both irrelevant (2506.16447, 2606.00555) |
| AXT11 | 2026-10-23 | arXiv API (title lookup to resolve Scholar-only hits) | `all:answerability AND all:"cross-lingual" AND all:abstention` | 2 | all | 2 (2503.23687 MKA; 2512.12694 MTRACE) |
| ACL1 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org romanized abstention LLM` | n/a | 9 results returned | No Anthology paper combining romanization + abstention. Returned (mostly arXiv despite site: filter): Wen et al. survey [arXiv:2407.18418] (B1); RomanSetu [arXiv:2401.14280] (C4); A2 [arXiv:2406.15948]; "Twin Worlds: Equivariance-Based Abstention" [arXiv:2608.28018]; AbstentionBench [arXiv:2506.09038] (C3) |
| ACL2 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org code-mixed retrieval-augmented generation unanswerable` | n/a | 9 results returned | none relevant (author pages; K18-1012 code-mixed QG/QA 2018, background) |
| ACL3 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org multilingual abstention threshold calibration transfer cross-lingual` | n/a | 9 results returned | MKA [arXiv:2503.23687]; A2; no Anthology paper on threshold transfer |
| ACL4 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org Bengali Bangla RAG unanswerable hallucination retrieval` | n/a | 10 results returned | TraSe Bangla RAG [ACL 2025.lm4uc-1.2] (found-only, adjacent); long-context Bangla QA with distractors [ACL 2025.banglalp-1.29] (found-only, adjacent); ICNLSP 2026 RAG hallucination paper [2026.icnlsp-1.6] (English data; not relevant) |
| ACL5 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org sufficient context multilingual RAG abstain` | n/a | 9 results returned | A1 (arXiv/ICLR page); "On the Consistency of Multilingual Context Utilization in RAG" [ACL 2025.mrl-main.15] (found-only, adjacent); BordIRLines / "Multilingual RAG for Culturally-Sensitive Tasks" [ACL 2025.findings-acl.219] (found-only, adjacent) |
| ACL6 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org romanized transliterated input hallucination selective prediction` | n/a | 10 results returned | "Happiness is Sharing a Vocabulary: A Study of Transliteration Methods" [ACL 2026.eacl-long.365] (found-only, background for RQ4-ii); C8 [arXiv:2511.22769]; "The Latin Substrate" [arXiv:2605.31363] (found-only, background) |
| ACL7 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org code-mixed abstention LLM unanswerable questions Hinglish Banglish` | n/a | 9 results returned | none relevant (W18-3204 code-mixed QA challenge 2018, background) |
| ACL8 | 2026-10-23 | ACL Anthology via WebSearch tool (site: filter; filter only partly honoured) | `site:aclanthology.org selective prediction multilingual calibration confidence threshold languages LLM` | n/a | 10 results returned | arXiv:2607.06327 (via papers.cool); EACL 2026 short paper on multilingual calibration after instruction tuning [ACL 2026.eacl-short, exact ID not resolved] (found-only); Ahuja et al. "On the Calibration of Massively Multilingual LMs" [ACL 2022.emnlp-main.290] (found-only, background); Jiang et al. "Calibrating Zero-shot Cross-lingual (Un-)structured Predictions" [ACL 2022.emnlp-main.170] (found-only, background — cross-lingual calibration transfer for encoders) |
| W1 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `romanized Bengali native script code-mixed paired evaluation LLM abstention retrieval-augmented question answering` (extended mode) | n/a | 9 results returned | BanglaShield [arXiv:2610.24288]; Indi-RomCoM [arXiv:2606.30790]; BenHalluEval [arXiv:2605.31483]; C8; "RetrieveGPT … Code-Mixed Information Retrieval" [arXiv:2411.04752] (found-only, adjacent). None combines script variants + abstention + RAG. |
| W2 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Probe Before you Answer" Answerability Probing for Abstention in Cross-Lingual Context-Based Question Answering` | n/a | 9 results returned | Title NOT found outside Google Scholar. Returned "Two Axes of LLM Abstention" [arXiv:2607.08456]; CausalAbstain [arXiv:2506.00519] |
| W3 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Answerability Probing for Abstention in Cross-Lingual" question answering` (extended) | n/a | 9 results returned | Title NOT found |
| W4 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Probe Before you Answer" abstention cross-lingual context-based question answering pdf` | n/a | 9 results returned | Title NOT found |
| W5 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"When Retrieval Hurts" Evidence Utilization Script Fidelity Knowledge Conflicts Multilingual RAG` | n/a | 10 results returned | Resolved to ACL 2026.mellm-1.9 (abs page opened, see candidates) |
| W6 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Trust-Calibrated Multilingual RAG for Humanitarian Information Platforms"` | n/a | 10 results returned | Resolved to journal.stekom.ac.id IJGD 4(1) (not opened; found-only). DE/EN; not script variants |
| W7 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Fine-Tuning Creates Confident Errors" Clarification Failure Bengali–English Agricultural Question Answering` | n/a | 9 results returned | Title NOT found; KrishokChat [arXiv:2606.29243] returned (found-only, adjacent) |
| W8 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Cross-Lingual RAG for Question Answering with Confidence-Aware Hallucination Detection"` | n/a | 9 results returned | Title NOT found |
| W9 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"CalibJudge" calibrated LLM-as-a-judge multilingual RAG uncertainty-aware scoring` | n/a | 10 results returned | Title NOT found |
| W10 | 2026-10-23 | General web (WebSearch tool) — title resolution / broad search | `"Reducing Hallucinations in Retrieval-Augmented LLM Question Answering for Indian Code-Mixed Queries"` (extended) | n/a | 9 results returned | Resolved to Springer chapter DOI 10.1007/978-3-032-27754-1_37 (SmartCom 2026, LNNS vol. 1991 per search snippet). Springer page could not be opened (auth redirect) → found-only |
| S2-0 | 2026-10-23 | Semantic Scholar API (first script) | `romanized abstention` (+15 queued queries) — /graph/v1/paper/search?query=… | FAILED (HTTP 429 on all 8 retries of query 1; script stopped manually) | 0 | — |
| S2-1 | 2026-10-23 | Semantic Scholar API | `romanized abstention` — https://api.semanticscholar.org/graph/v1/paper/search?query=romanized+abstention&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-2 | 2026-10-23 | Semantic Scholar API | `code-mixed RAG unanswerable` — https://api.semanticscholar.org/graph/v1/paper/search?query=code-mixed+RAG+unanswerable&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-3 | 2026-10-23 | Semantic Scholar API | `sufficient context multilingual` — https://api.semanticscholar.org/graph/v1/paper/search?query=sufficient+context+multilingual&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | 117579 | 20 | none relevant (keyword-OR ranking; mostly education/linguistics); "Modeling Romanized Hindi and Bengali" [arXiv:2511.22769] (C8) |
| S2-4 | 2026-10-23 | Semantic Scholar API | `transliteration selective prediction` — https://api.semanticscholar.org/graph/v1/paper/search?query=transliteration+selective+prediction&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-5 | 2026-10-23 | Semantic Scholar API | `Bengali hallucination retrieval` — https://api.semanticscholar.org/graph/v1/paper/search?query=Bengali+hallucination+retrieval&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-6 | 2026-10-23 | Semantic Scholar API | `romanized hallucination` — https://api.semanticscholar.org/graph/v1/paper/search?query=romanized+hallucination&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-7 | 2026-10-23 | Semantic Scholar API | `abstention cross-lingual threshold` — https://api.semanticscholar.org/graph/v1/paper/search?query=abstention+cross-lingual+threshold&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-8 | 2026-10-23 | Semantic Scholar API | `abstention calibration transfer cross-lingual` — https://api.semanticscholar.org/graph/v1/paper/search?query=abstention+calibration+transfer+cross-lingual&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-9 | 2026-10-23 | Semantic Scholar API | `code-mixed abstain` — https://api.semanticscholar.org/graph/v1/paper/search?query=code-mixed+abstain&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-10 | 2026-10-23 | Semantic Scholar API | `Bangla RAG unanswerable` — https://api.semanticscholar.org/graph/v1/paper/search?query=Bangla+RAG+unanswerable&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | 63 | 20 | "BHRE-RAG: … Comprehension-Based QA in Bangla" (DOI 10.1109/ICCIT68739.2025.11491594; found-only); "BanglaMedQA and BanglaMMedBench" [arXiv:2511.04560] (found-only); "TraSe … RAG in Bangla" [ACL 2025.lm4uc-1.2] (found-only); "NCTB-QA" [arXiv:2603.05462]; "Evidence-Calibrated RAG for Unanswerable QA … Abstention Calibration" (DOI 10.51903/jtie.v4i2.536; English SQuAD 2.0; found-only) |
| S2-11 | 2026-10-23 | Semantic Scholar API | `selective prediction multilingual calibration` — https://api.semanticscholar.org/graph/v1/paper/search?query=selective+prediction+multilingual+calibration&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-12 | 2026-10-23 | Semantic Scholar API | `romanized Bengali LLM` — https://api.semanticscholar.org/graph/v1/paper/search?query=romanized+Bengali+LLM&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | 721 | 20 | "Script Fragmentation and Format: What Drives the English-Bengali Performance Gap in Open LLMs?" [arXiv:2507.23248] (found-only, adjacent); "Automatic back transliteration of Romanized Bengali (Banglish) to Bengali" (DOI 10.1007/s42044-022-00122-9; tool for RQ4-ii); "Register Shifts Break LLM Safety: A Bengali Benchmark" [arXiv:2608.22335] (found-only, adjacent); C8 |
| S2-13 | 2026-10-23 | Semantic Scholar API | `multilingual RAG abstention insufficient context` — https://api.semanticscholar.org/graph/v1/paper/search?query=multilingual+RAG+abstention+insufficient+context&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| S2-14 | 2026-10-23 | Semantic Scholar API | `script variation abstention LLM` — https://api.semanticscholar.org/graph/v1/paper/search?query=script+variation+abstention+LLM&fields=title%2Cyear%2Cvenue%2CexternalIds&limit=20 | FAILED (HTTP 429 after 4 attempts, 40 s back-off) | 0 | — |
| GS0 | 2026-10-23 | Google Scholar (manual curl probe) | `"romanized" "abstention"` — https://scholar.google.com/scholar?q=%22romanized%22+%22abstention%22 (no hl param) | "About 223 results" | 0 (count only) | count only; titles not parsed |
| GS1 | 2026-10-23 | Google Scholar | `"romanized" "abstention"` — https://scholar.google.com/scholar?q=%22romanized%22+%22abstention%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS2 | 2026-10-23 | Google Scholar | `"code-mixed" "RAG" "unanswerable"` — https://scholar.google.com/scholar?q=%22code-mixed%22+%22RAG%22+%22unanswerable%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS3 | 2026-10-23 | Google Scholar | `"sufficient context" "multilingual"` — https://scholar.google.com/scholar?q=%22sufficient+context%22+%22multilingual%22&hl=en | 1,010 | 10 titles (page 1 only) | none relevant (generic multilingual/translation titles) |
| GS4 | 2026-10-23 | Google Scholar | `"transliteration" "selective prediction"` — https://scholar.google.com/scholar?q=%22transliteration%22+%22selective+prediction%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | "Trust-Calibrated Multilingual RAG for Humanitarian Information Platforms" (found-only; abstention in multilingual RAG, DE/EN); "Fine-Tuning Creates Confident Errors: Clarification Failure in Bengali–English Agricultural QA" (found-only; could not locate outside Scholar); "Adversarial Robustness in Multilingual and Code-Mixed NLP: Insights from Indian Language Settings" (found-only) |
| GS5 | 2026-10-23 | Google Scholar | `"Bengali" "hallucination" "retrieval"` — https://scholar.google.com/scholar?q=%22Bengali%22+%22hallucination%22+%22retrieval%22&hl=en | 282 | 10 titles (page 1 only) | "Bengali Hallucination Detection with Retrieval and Programs" [arXiv:2610.22892]; "BanglaDiaHallu" (found-only); "When Retrieval Hurts: Evidence Utilization, Script Fidelity, and Knowledge Conflicts in Multilingual RAG" [ACL 2026.mellm-1.9] |
| GS6 | 2026-10-23 | Google Scholar | `"romanized" "hallucination"` — https://scholar.google.com/scholar?q=%22romanized%22+%22hallucination%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS7 | 2026-10-23 | Google Scholar | `"abstention" "cross-lingual" "threshold"` — https://scholar.google.com/scholar?q=%22abstention%22+%22cross-lingual%22+%22threshold%22&hl=en | 170 | 10 titles (page 1 only) | "Probe Before you Answer! Answerability Probing for Abstention in Cross-Lingual Context-Based Question Answering" (found-only; Scholar listing only); "CalibJudge: Calibrated LLM-as-a-judge for multilingual RAG" (found-only); "Cross-Lingual RAG for Question Answering with Confidence-Aware Hallucination Detection" (found-only) |
| GS8 | 2026-10-23 | Google Scholar | `"abstention" "calibration transfer"` — https://scholar.google.com/scholar?q=%22abstention%22+%22calibration+transfer%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | "The Calibration Transfer Gap: When Recalibration Parameters Fail to Transfer under Distribution Shift" (found-only; generic, not language) |
| GS9 | 2026-10-23 | Google Scholar | `"code-mixed" "abstain"` — https://scholar.google.com/scholar?q=%22code-mixed%22+%22abstain%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | "When Surface Form Changes Moderation Decisions: A Paired Study of Code-Mixed Workflow Instability" [arXiv:2606.05654]; "Trustworthy Smishing Detection in Code-Mixed Bangla-English SMS: … Calibration, Selective Classification …" (found-only) |
| GS10 | 2026-10-23 | Google Scholar | `"Bangla" "RAG" "unanswerable"` — https://scholar.google.com/scholar?q=%22Bangla%22+%22RAG%22+%22unanswerable%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | none directly relevant ("Systematic review … cross lingual QA for low resource Indic languages", found-only, background) |
| GS11 | 2026-10-23 | Google Scholar | `"selective prediction" "multilingual" "calibration"` — https://scholar.google.com/scholar?q=%22selective+prediction%22+%22multilingual%22+%22calibration%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS12 | 2026-10-23 | Google Scholar | `"romanized" "abstain" "LLM"` — https://scholar.google.com/scholar?q=%22romanized%22+%22abstain%22+%22LLM%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | "Probe Before you Answer!" (found-only, again); "When Surface Form Changes Moderation Decisions" [arXiv:2606.05654] |
| GS13 | 2026-10-23 | Google Scholar | `"sufficient context" "Bengali"` — https://scholar.google.com/scholar?q=%22sufficient+context%22+%22Bengali%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS14 | 2026-10-23 | Google Scholar | `"code-mixed" "abstention" "LLM"` — https://scholar.google.com/scholar?q=%22code-mixed%22+%22abstention%22+%22LLM%22&hl=en | BLOCKED (CAPTCHA / unusual-traffic page) — retried later | 0 titles (page 1 only) | — |
| GS15 | 2026-10-23 | Google Scholar | `"romanized" "abstention"` — https://scholar.google.com/scholar?q=%22romanized%22+%22abstention%22&hl=en | 194 | 10 titles (page 1 only) | "Probe Before you Answer!" (found-only); "IndicJR: jailbreak robustness in South Asian languages" (found-only; safety, adjacent) |
| GS16 | 2026-10-23 | Google Scholar | `"code-mixed" "RAG" "unanswerable"` — https://scholar.google.com/scholar?q=%22code-mixed%22+%22RAG%22+%22unanswerable%22&hl=en | not reported on parsed page (results listed) | 8 titles (page 1 only) | "Reducing Hallucinations in Retrieval-Augmented LLM Question Answering for Indian Code-Mixed Queries" (Springer SmartCom 2026, DOI 10.1007/978-3-032-27754-1_37; found-only); "Investigating language preference of multilingual RAG systems" (found-only, background) |
| GS17 | 2026-10-23 | Google Scholar | `"romanized" "hallucination"` — https://scholar.google.com/scholar?q=%22romanized%22+%22hallucination%22&hl=en | 155 | 10 titles (page 1 only) | "Cross Lingual Transfer in Tulu Legal Comprehension: Script-Dependent Improvement and RAG-Induced Knowledge Conflict" (found-only, adjacent); "Beyond Accuracy: … Marathi Script Variation" (found-only, adjacent) |
| GS18 | 2026-10-23 | Google Scholar | `"selective prediction" "multilingual" "calibration"` — https://scholar.google.com/scholar?q=%22selective+prediction%22+%22multilingual%22+%22calibration%22&hl=en | 163 | 10 titles (page 1 only) | "Translation Equivalence Is Not Linguistic Equity: English–Arabic–Chinese Calibration …" (found-only, adjacent); "Distribution-Free Selective Prediction for LLM-RAG Hallucination Detection … under Domain Shift" (found-only, adjacent) |
| GS19 | 2026-10-23 | Google Scholar | `"sufficient context" "Bengali"` — https://scholar.google.com/scholar?q=%22sufficient+context%22+%22Bengali%22&hl=en | 120 | 10 titles (page 1 only) | "BenHalluEval" [arXiv:2605.31483] (C5, already in matrix); otherwise none |
| GS20 | 2026-10-23 | Google Scholar | `"code-mixed" "abstention" "LLM"` — https://scholar.google.com/scholar?q=%22code-mixed%22+%22abstention%22+%22LLM%22&hl=en | not reported on parsed page (results listed) | 10 titles (page 1 only) | "Reducing Hallucinations in RAG QA for Indian Code-Mixed Queries" (found-only, again) |

### Totals
- arXiv API: 37 topic queries (AX1–AX37) + 11 title/verification lookups (AXT1–AXT11). All succeeded.
- ACL Anthology (via WebSearch `site:`): 8 queries; no hit counts reported by the tool.
- General web (WebSearch): 10 broad/title-resolution queries.
- Semantic Scholar: 15 search attempts → 3 succeeded, 12 failed (HTTP 429); 2 citation-chase calls succeeded.
- Google Scholar: 14 distinct queries; 6 initially blocked, all 6 succeeded on retry (20 page fetches + 1 count probe GS0 + 1 later blocked title lookup).

## Citation chase (Semantic Scholar `/citations`, fetched 2026-10-23)

URLs: `https://api.semanticscholar.org/graph/v1/paper/arXiv:2411.06037/citations?fields=title,year,venue,externalIds&limit=1000&offset=0` and the same for `arXiv:2406.15948`. Both returned all records in one page (`next` absent).

| Seed | Citing papers returned by S2 | Screened | Relevant for our gap |
|---|---|---|---|
| A1 Joren et al. (arXiv:2411.06037) | **122** | 122 titles | **None** of the 122 titles mentions multilingual, cross-lingual, script, romanization, code-mixing, Bengali/Bangla or any non-English language (title-level screen). Sufficiency/abstention-adjacent (English, by title): DeclineCraft [arXiv:2610.28340]; Relevance Is Not Sufficient Evidence [arXiv:2609.37469]; Learning Evidence Sufficiency Boundaries for Selective Answering [arXiv:2609.01687]; Prompt-Based Abstention Fails Under Misleading Context [arXiv:2608.22228]; Twin Worlds [arXiv:2608.28018]; Knowing What's Missing [arXiv:2512.06476]; Sieve and Sage [arXiv:2609.35794]; Sufficiency-Gated RAG [DOI:10.32604/cmc.2026.088937]. "Towards Geo-Culturally Grounded LLM Generations" [arXiv:2502.13497] is cultural, not script. |
| A2 Feng et al. (arXiv:2406.15948) | **20** (matches S2 `citationCount` = 20) | 20 titles | CausalAbstain [arXiv:2506.00519] (C2); MKA [arXiv:2503.23687]; **"Choosing the Right Language Mode at Inference Time for Multilingual Reliability" [arXiv:2609.04653]** (abstract-read; calibration across language modes, no scripts/RAG); Twin Worlds [arXiv:2608.28018] (cites A1 and A2; English, no languages per abs page); "Why Do Multilingual Reasoning Gaps Emerge…" [arXiv:2510.27269] (background); "Towards Trustworthy AI-Mediated Communication Across Languages and Cultures" [DOI:10.18653/v1/2026.bigpicture-main.5] (position, found-only). No title mentions romanized/script/code-mixed/Bengali. |

Caveat: S2 citation coverage is incomplete (e.g., 122 for an ICLR 2025 paper is likely an undercount; Google Scholar "cited by" could not be fetched — blocked). The screen is **title-level**, so a citing paper with a generic title could still be multilingual. [REC] Repeat via Google Scholar "Cited by" manually before G1 closes.

<details><summary>Full A1 citing list (122, as returned)</summary>

- 2026 · arXiv:2610.27541 · EviDial: When Correct Depression Predictions Lack Evidence
- 2026 · arXiv:2610.28340 · DeclineCraft: A RAG Abstention Benchmark for Jointly Measuring Combined Retrieval and Parametric Knowledge
- 2026 · arXiv:2610.28843 · Beyond Correct Answers: How Compositional Cues Shape Visual Judgments
- 2026 · arXiv:2610.26836 · Same Simulation, Different Evidence: Where Retrieved Tool Output Costs LLM Agents Accuracy
- 2026 · arXiv:2610.25867 · Benefit-Targeted Routing and Bounded Revision for LLM-Based Evidence Screening in Manufacturing Supplier Discovery
- 2026 · arXiv:2610.23721 · Recognizing Study Lineage Is Not Enough: Over-Crediting Same-Trial Evidence in LLM-Based Medical Verification
- 2026 · arXiv:2610.23480 · MuninAI: A Self-Hosted Agentic Framework for Independent Research Groups
- 2026 · arXiv:2610.21184 · Beyond Retrieval Failure: Understanding Why LLMs Miss Evidence in Multi-Hop RAG
- 2026 · arXiv:2610.22668 · From Relevant Memories to Sufficient Evidence: Rethinking Memory Utilization in LLM Agents
- 2026 · arXiv:2610.18497 · Judges Follow the Reference: The Derivation Gap in Verifying Tool-Call Arguments
- 2026 · arXiv:2610.09348 · Relevance Is Not Sufficiency: What Actually Closes the Evidence Gap in Long-Term Memory QA
- 2026 · arXiv:2610.09412 · Finding the Right Balance: Relevance and Diversity in LLM Retrieval
- 2026 · arXiv:2610.07894 · Rethinking Faithfulness in LLMs: A Pairwise Context-Sensitive Perspective
- 2026 · arXiv:2610.03190 · Not Until the Evidence Says So: Teaching LLM Investigators When to Close a Case
- 2026 · arXiv:2609.37993 · BITEM at the NTCIR-19 R2C2 Task: Predicting Confidence from Agentic RAG Pipeline Signals
- 2026 · arXiv:2609.34358 · FORGE: Form-Optimal Routing of Grounded Evidence for Frozen LLM Agents
- 2026 · arXiv:2609.35621 · Cartridges++: KV Cache Compression without Off-Context Derailment
- 2026 · arXiv:2609.37469 · Relevance Is Not Sufficient Evidence: Detecting Evidence Gaps Before Generation in RAG
- 2026 · arXiv:2609.32269 · Before Answering: Evidence Sufficiency under Size-Matched Memory Construction
- 2026 · DOI:10.1007/s10676-026-09922-0 · From capability to assertability: epistemic regulation of LLM-mediated claim presentation
- 2026 · arXiv:2609.28876 · Forecast-Dojo: Replayable Environments for Benchmarking and Training LLM Forecasting Agents
- 2026 · arXiv:2609.24885 · The Copy Ceiling: An Input-Exposure Control for Ontology-Grounded Generation over Curated Corpora
- 2026 · arXiv:2609.23354 · From Ranked Documents to Reliable Contexts: An Answer-Oriented Context Construct Framework for AI Search
- 2026 · arXiv:2609.22537 · EvidenT: Building Trustworthy Enterprise Assistants through Evidence Groundedness and Traceability
- 2026 · arXiv:2609.22486 · Semantics Delivery Network: Rethinking Web Retrieval Infrastructure for LLM Agents
- 2026 · arXiv:2609.35794 · Sieve and Sage: Efficient Distraction Filtering for Reliable RALM Abstention
- 2026 · arXiv:2609.17081 · EviScope: Paired Counterfactual Evidence Diagnostics for Faithful and Efficient Grounded Language Models
- 2026 · arXiv:2609.16818 · InceptionRAG: Stealthy Poisoning Attack Against Retrieval-Augmented Generation
- 2026 · arXiv:2609.08943 · Evaluating and Improving Evidence-Grounded Fact-Checking in LLMs via Multi-Round Evidence Ablation
- 2026 · arXiv:2609.26086 · CoVeR: Coverage-Based Routing of Verifier Calls in Agentic Retrieval
- 2026 · arXiv:2609.01687 · Learning Evidence Sufficiency Boundaries for Selective Answering in Grounded Multi-Hop QA
- 2026 · arXiv:2608.31115 · InsightToast: Proactive Information Retrieval&Glanceable Visualization in the Side Channel of Data-Rich Meetings
- 2026 · arXiv:2608.28018 · Twin Worlds: Equivariance-Based Abstention for Evidence-Grounded Reasoning
- 2026 · arXiv:2608.27020 · Representation Measurements Under Function-Preserving Reparameterizations
- 2026 · arXiv:2608.27768 · Why Didn't It Check? Unsupported Final Claims and Their Repair in Two Tool-Equipped Language Models
- 2026 · arXiv:2608.27661 · Knowing Before Answering: Decoding Language Models for Reliable RAG
- 2026 · arXiv:2608.23763 · TrustShiftProbe: Characterizing, Benchmarking, and Defending Staged Trust Attacks on MCP Servers
- 2026 · arXiv:2608.22228 · Prompt-Based Abstention Fails Under Misleading Context: A Controlled Study of Small Frozen RAG Models
- 2026 · arXiv:2608.21558 · Automating Multi-Hop RAG Evaluation via TRIAD: From Context Extraction to Validated Dataset Generation
- 2026 · arXiv:2608.17433 · Task-Aware Harness Provisioning for LLM Agents in Mission-Critical Infrastructure Operations
- 2026 · arXiv:2608.16776 · GRIP: Grounded Reasoning via Information-Restricted Premises
- 2026 · DOI:10.1145/3770855.3817934 · UniDocVLM: Enhancing Visual Reasoning and Document Understanding for VLM via Reinforcement Learning
- 2026 · arXiv:2608.07943 · Locating Failure in Multi-Page Visually Rich Document Understanding Systems: An Empirical Attribution
- 2026 · arXiv:2608.04591 · When Absence Is Evidence: Evaluating Completeness-Sensitive Negative Reasoning in Large Language Models
- 2026 · arXiv:2608.02009 · HALT: Verification-Aware Stopping for Retrieval-Augmented Search Agents
- 2026 · arXiv:2608.01565 · DocNavRAG: Document-Structured Graph RAG with Stateful Evidence Construction for Complex Document Question Answering
- 2026 · DOI:10.1109/ICITCOM70739.2026.11714386 · An Empirical Analysis of Multi-Hop Retrieval and Reasoning Failures in Agentic RAG
- 2026 · arXiv:2607.27232 · Sympathetic Framing: Evaluating AI Alignment across Sociodemographic Groups
- 2026 · DOI:10.1145/3805712.3809544 · Corpus-Centric Learning for Zero-Shot Table Retrieval
- 2026 · arXiv:2607.00570 · Dual-Confidence Contrastive Decoding for Retrieval-Augmented Generation
- 2026 · DOI:10.1109/ICECET65726.2026.11632725 · Comparative Analysis of Context-Extension and Question-Matching RAG Architectures: A Case Study on German Regulatory Documentation
- 2026 · arXiv:2606.23937 · When Retrieval Metrics Mislead: Measuring Policy Signal in Long-Horizon Tool-Use Agents
- 2026 · arXiv:2607.09691 · What Context Does a Coding Agent Actually Need to Act?
- 2026 · arXiv:2607.22625 · TokenMem: Faithful Knowledge Injection for Frozen LLMs
- 2026 · arXiv:2606.23716 · Legal Reasoning Is Not Lawyering: Rethinking Legal Benchmarks for Pro Se Access to Justice
- 2026 · arXiv:2606.09005 · Document-Authored Control-Signal Impersonation: A Low-Cost Indirect Prompt Attack on RAG Safety Boundaries
- 2026 · arXiv:2606.04109 · Discourse-Role Labels as Presentation-Time Variables for Context Use in Language Models
- 2026 · arXiv:2606.01075 · On the Generalization Gap in Self-Evolving Language Model Reasoning
- 2026 · arXiv:2605.30790 · On the impact of retrieved content representations in RAG Pipelines
- 2026 · arXiv:2605.29956 · Uncertainty Quantification for Multimodal Retrieval Augmented Generation
- 2026 · arXiv:2605.26663 · Evidence Absence Is Not Evidence Insufficiency: Diagnosing NEI Construction Artifacts in Fact Verification
- 2026 · arXiv:2605.13052 · RAG-Enhanced Large Language Models for Dynamic Content Expiration Prediction in Web Search
- 2026 · arXiv:2605.02010 · Reliable AI Needs to Externalize Implicit Knowledge: A Human-AI Collaboration Perspective
- 2026 · DOI:10.63317/25dqodqmcsa4 · Verifiable Financial Enterprise Question Answering via Inference-Time Grounding and Traceability
- 2026 · arXiv:2604.17227 · Cloud-native and Distributed Systems for Efficient and Scalable Large Language Models - A Research Agenda
- 2026 · arXiv:2604.05552 · Context-Agent: Dynamic Discourse Trees for Non-Linear Dialogue
- 2026 · DOI:10.1109/ICNDSA68777.2026.11652357 · Intent-Aware Personalized Career Guidance using Agentic AI Framework
- 2026 · arXiv:2603.19008 · Hypothesis-Conditioned Query Rewriting for Decision-Useful Retrieval
- 2026 · DOI:10.1609/aaai.v40i48.42311 · Hallucinations at the Firewall
- 2026 · arXiv:2603.01486 · Agentic Multi-Source Grounding for Enhanced Query Intent Understanding: A DoorDash Case Study
- 2026 · arXiv:2602.20091 · How Retrieved Context Shapes Internal Representations in RAG
- 2026 · arXiv:2603.06604 · Know When You're Wrong: Aligning Confidence with Correctness for LLM Error Detection
- 2026 · DOI:10.3390/informatics13020030 · HierFinRAG - Hierarchical Multimodal RAG for Financial Document Understanding
- 2026 · arXiv:2602.08294 · When Does Context Help? Error Dynamics of Contextual Information in Large Language Models
- 2026 · arXiv:2603.29875 · UnWeaving the knots of GraphRAG - turns out VectorRAG is almost enough
- 2026 · arXiv:2604.06173 · Beyond Case Law: Evaluating Structure-Aware Retrieval and Safety in Statute-Centric Legal QA
- 2026 · arXiv:2601.11037 · BAPO: Boundary-Aware Policy Optimization for Reliable Agentic Search
- 2026 · arXiv:2601.10413 · LADFA: A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies
- 2025 · arXiv:2512.16553 · Needle in the Web: A Benchmark for Retrieving Targeted Web Pages in the Wild
- 2025 · DOI:10.1109/BigData66926.2025.11401780 · RAG-CUE: Actionable and Unified Evaluation for Retrieval-Augmented Generation Systems
- 2025 · arXiv:2512.06476 · Knowing What's Missing: Assessing Information Sufficiency in Question Answering
- 2025 · DOI:10.1007/s44443-025-00334-6 · Improving negative rejection ability in language models: A review of fine-tuned LLMs, RAG, and RAFT
- 2025 · arXiv:2511.17906 · AnimAgents: Coordinating Multi-Stage Animation Pre-Production with Human-Multi-Agent Collaboration
- 2025 · arXiv:2511.14010 · Knowledge-Grounded Agentic Large Language Models for Multi-Hazard Understanding from Reconnaissance Reports
- 2025 · arXiv:2511.06738 · Rethinking Retrieval-Augmented Generation for Medicine: A Large-Scale, Systematic Expert Evaluation and Practical Insights
- 2025 · arXiv:2511.05706 · AdvisingWise: Supporting Academic Advising in Higher Educations Through a Human-in-the-Loop Multi-Agent Framework
- 2025 · DOI:10.1109/ICTAI66417.2025.00068 · Translating Human Instructions to AI Agents Using Language Models for Planning
- 2025 · DOI:10.1109/EEPS68057.2025.11351537 · Zero-Shot Anomaly Detection in Smart Grid GOOSE Communication via Retrieval-Augmented Contrastive Learning
- 2025 · arXiv:2510.26242 · Retrieval Augmented Generation-Enhanced Distributed LLM Agents for Generalizable Traffic Signal Control with Emergency Vehicles
- 2025 · arXiv:2510.17764 · Evaluating Medical LLMs by Levels of Autonomy: A Survey Moving from Benchmarks to Applications
- 2025 · arXiv:2510.16609 · Prior Knowledge Makes It Possible: From Sublinear Graph Algorithms to LLM Test-Time Methods
- 2025 · arXiv:2510.15253 · Scaling Beyond Context: A Survey of Multimodal Retrieval-Augmented Generation for Document Understanding
- 2025 · arXiv:2510.13935 · Instruction Retrieval at Inference Time for Small Language Models
- 2025 · arXiv:2510.07231 · EconCausal: A Context-Aware Economic Reasoning Benchmark for Large Language Models
- 2025 · arXiv:2510.05363 · MHA-RAG: Improving Efficiency, Accuracy, and Consistency by Encoding Exemplars as Soft Prompts
- 2025 · arXiv:2510.00508 · Copy-Paste to Mitigate Large Language Model Hallucinations
- 2025 · arXiv:2509.20324 · RAG Security and Privacy: Formalizing the Threat Model and Attack Surface
- 2025 · arXiv:2509.18868 · Memory in Large Language Models: Mechanisms, Evaluation and Evolution
- 2025 · arXiv:2509.21359 · Influence Guided Context Selection for Effective Retrieval-Augmented Generation
- 2025 · arXiv:2509.07759 · A Survey of Long-Document Retrieval in the PLM and LLM Era
- 2025 · arXiv:2508.10467 · FIRESPARQL: A LLM-based Framework for SPARQL Query Generation over Scholarly Knowledge Graphs
- 2025 · arXiv:2508.01290 · Prompting Large Language Models with Partial Knowledge for Answering Questions with Unseen Entities
- 2025 · arXiv:2507.22716 · From Sufficiency to Reflection: Reinforcement-Guided Thinking Quality in Retrieval-Augmented Reasoning for LLMs
- 2025 · arXiv:2506.20051 · Controlled Retrieval-augmented Context Evaluation for Long-form RAG
- 2025 · arXiv:2505.24449 · When Large Multimodal Models Confront Evolving Knowledge: Challenges and Explorations
- 2025 · arXiv:2506.00054 · Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers
- 2025 · arXiv:2502.18108 · Uncertainty Quantification in Retrieval Augmented Question Answering
- 2025 · arXiv:2502.13497 · Towards Geo-Culturally Grounded LLM Generations
- 2025 · arXiv:2502.12893 · H-CoT: Hijacking the Chain-of-Thought Safety Reasoning Mechanism to Jailbreak Large Reasoning Models, Including OpenAI o1/o3, DeepSeek-R1, and Gemini 2.0 Flash Thinking
- 2024 · arXiv:2412.13746 · RAG-RewardBench: Benchmarking Reward Models in Retrieval Augmented Generation for Preference Alignment
- 2024 · arXiv:2411.04105 · A Implies B: Circuit Analysis in LLMs for Propositional Logical Reasoning
- 2024 · arXiv:2411.02433 · SLED: Self Logits Evolution Decoding for Improving Factuality in Large Language Models
- 2024 · arXiv:2409.06067 · MLLM-LLaVA-FL: Multimodal Large Language Model Assisted Federated Learning
- 2024 · arXiv:2406.12044 · ARTIST: Improving the Generation of Text-Rich Images with Disentangled Diffusion Models and Large Language Models
- 2026 · DOI:10.5220/0014403000004052 · Towards AI-Enabled Training Needs Analysis Using Dual AI-Agent Collaboration
- 2026 · DOI:10.5220/0014232000004052 · Think before You Fetch: Smarter Retrieval for Smarter LLMs with Enhanced Table Understanding and Long-Form Reasoning
- 2026 · DOI:10.18653/v1/2026.acl-long.1740 · TH-RAG : Topic-Based Hierarchical Knowledge Graphs for Robust Multi-hop Reasoning in Graph-based RAG Systems
- 2026 · DOI:10.63317/4m84m2k77g97 · SciCiteVal: A Multi-Domain Dataset for Scientific Citation Verification
- 2026 · DOI:10.32604/cmc.2026.088937 · Sufficiency-Gated Retrieval-Augmented Generation: Reducing Hallucination via Context Adequacy Estimation
- 2025 · DOI:10.18653/v1/2025.ijcnlp-long.56 · Generate but Verify: Answering with Faithfulness in RAG-based Question Answering
- 2025 · DOI:10.48550/arXiv.2510.05363 · MHA-RAG: Improving Efficiency, Accuracy, and Consistency by Encoding Exemplars as Soft Prompts
- None · S2:95888b89c2f6045e579a6632ffd666b131cb0ad4 · NDERSTANDING C ONFORMAL F ACTUALITY FOR RAG-BASED LLM S : N OVEL M ETRICS AND S YSTEM - ATIC I NSIGHTS

</details>

<details><summary>Full A2 citing list (20, as returned)</summary>

- 2026 · arXiv:2609.22494 · Datasets and Methods for Improving the Cultural Capabilities of NLP Systems: A Survey
- 2026 · arXiv:2609.09702 · Decision Shifts, Lost Label Functionality, and an Inconclusive Grounding Audit in Correctness-Gated Multi-Teacher Distillation
- 2026 · arXiv:2609.04653 · Choosing the Right Language Mode at Inference Time for Multilingual Reliability
- 2026 · arXiv:2608.28018 · Twin Worlds: Equivariance-Based Abstention for Evidence-Grounded Reasoning
- 2026 · DOI:10.1109/JoCICI69279.2026.11701728 · English or Spanish Prompts: Effect of Language Prompt on LLM Code Generation Quality
- 2026 · arXiv:2601.07767 · Are LLM Decisions Faithful to Verbal Confidence?
- 2025 · arXiv:2512.07454 · Persian-Phi: Efficient Cross-Lingual Adaptation of Compact LLMs via Curriculum Learning
- 2025 · arXiv:2510.27269 · Why Do Multilingual Reasoning Gaps Emerge in Reasoning Language Models?
- 2025 · arXiv:2509.23499 · Multi-modal Data Spectrum: Multi-modal Datasets are Multi-dimensional
- 2025 · arXiv:2508.13908 · Translating the Force Concept Inventory in the age of AI
- 2025 · arXiv:2506.04721 · SPARTA ALIGNMENT: Collectively Aligning Multiple Language Models through Combat
- 2025 · arXiv:2506.00519 · CausalAbstain: Enhancing Multilingual LLMs with Causal Reasoning for Trustworthy Abstention
- 2025 · arXiv:2505.21701 · Do We Know What LLMs Don't Know? A Study of Consistency in Knowledge Probing
- 2025 · arXiv:2503.23687 · MKA: Leveraging Cross-Lingual Consensus for Model Abstention
- 2025 · arXiv:2501.06143 · Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories
- 2024 · arXiv:2407.18418 · Know Your Limits: A Survey of Abstention in Large Language Models
- 2024 · arXiv:2407.12043 · The Art of Saying No: Contextual Noncompliance in Language Models
- 2026 · DOI:10.18653/v1/2026.bigpicture-main.5 · Towards Trustworthy AI-Mediated Communication Across Languages and Cultures
- 2026 · DOI:10.32604/cmes.2026.075507 · Advancing Large Language Models for Low-Resource Languages: A Systematic Review of Pretraining, Adaptation, and Ethical Challenges
- 2024 · DOI:10.48550/arXiv.2407.18418 · The Art of Refusal: A Survey of Abstention in Large Language Models

</details>

## Candidate new close works

Ranked by threat to our novelty claims. "Abstract" statements below are paraphrases of the abstract only — **not** findings we may cite.

| Rank | ID | Title | Why relevant | Threat to | Verification status |
|---|---|---|---|---|---|
| 1 | arXiv:2606.05654 | When Surface Form Changes Moderation Decisions: A Paired Study of Code-Mixed Workflow Instability (Thimma Krishnaram, Hu, Saravanan; v2 5 Jun 2026; no venue listed) | Abstract: thresholds tuned on **clean-English dev data** are applied to **paired** Tamil-English code-mixed versions of the same content; reports decision-flip rate and shifted review/false-flag rates; tests a deferral rule. This is the **same experimental logic as our RQ2** (EN-calibrated operating point → paired code-mixed variant), but for hate-speech moderation classification, Tamil not Bengali, no romanized-native contrast, no RAG/evidence sufficiency. | RQ2 framing ("the transfer question itself" is no longer wholly new in general NLP) | metadata-verified, abstract-read |
| 2 | arXiv:2607.06327 | Estimating Uncertainty from Reasoning: A Large-Scale Study of Multi- and Crosslingual MCQA Performance in LLMs (Alfarano, Bacciu, Mansour, Mantrach, Federico; Findings of EMNLP 2026 per arXiv comments) | Abstract: UE for abstention across 22 languages; claims comprehension of low-resource languages is "largely intact" and the bottleneck is generation; includes an **analysis of threshold selection for selective prediction** in multilingual settings. Overlaps RQ2 (threshold behaviour across languages) and RQ3 (comprehension vs. calibration). Abs page does not mention Bengali, romanization, code-mixing or RAG; MCQA, not evidence-controlled RAG. | RQ2, RQ3 | metadata-verified, abstract-read. **Must be full-read** (language list, whether thresholds are transferred from English) |
| 3 | arXiv:2610.24288 | BanglaShield: A Script-Robust Safety Classifier and Benchmark for Bangla Native, Romanized, and Code-Mixed Prompts (Kabir, Tariquzzaman, Rifat, Ranasinghe, Raihan; v1 16 Oct 2026) | Abstract: every prompt rendered in **aligned native / romanized / code-mixed Bangla** for strictly paired comparison; romanization worsens LLM safety classification. Closest **paired-script Bangla design precedent** for RQ1; task is safety classification, not abstention/RAG; no EN-calibrated threshold transfer. Possible resource/romanization-convention reference. | RQ1 design novelty (paired BN/RBN/CM items are no longer unique as a design) | metadata-verified, abstract-read |
| 4 | arXiv:2609.22138 | Does the Truthfulness Signal Survive Code-Mixing? Probing Hidden States for Hallucination Detection in Hinglish (T. Singh; v1 25 Aug 2026) | Abstract: trains hallucination probes on clean-language states and tests **transfer to Hinglish**; matched-fact Hindi/English/Hinglish items; reports more hallucination on Hindi/Hinglish. Detector-transfer, not abstention threshold; Hindi not Bengali; QA without controlled evidence sufficiency (per abstract). | RQ2 (adjacent: cross-variant transfer of a reliability signal), RQ1 (adjacent) | metadata-verified, abstract-read |
| 5 | Springer DOI 10.1007/978-3-032-27754-1_37 | Reducing Hallucinations in Retrieval-Augmented LLM Question Answering for Indian Code-Mixed Queries (S. S. Gaikwad, J. S. Gaikwad; SmartCom 2026, LNNS — per search snippet) | Per search-engine summary only: RAG with an abstention control layer evaluated on English, Hindi and Hindi–English code-mixed queries. Closest **code-mixed RAG + abstention** hit. Unknown whether items are paired or evidence is controlled; Bengali/romanized not mentioned in snippet. | RQ1 (partial) | **found-only** (Springer page not accessible; nothing verified) |
| 6 | (no ID found) | "Probe Before you Answer! Answerability Probing for Abstention in Cross-Lingual Context-Based Question Answering" | Appeared in Google Scholar listings (GS7, GS12, GS15) as a [PDF]. Title suggests answerability/abstention in cross-lingual context-based QA. Could not be found on arXiv (AXT1, AXT10) or the web (W2–W4). | RQ1/RQ3 (unknown) | **found-only** (Scholar title only; existence unverified). [REC] Author to open via Scholar in a browser. |
| 7 | ACL 2026.mellm-1.9 | When Retrieval Hurts: Evidence Utilization, Script Fidelity, and Knowledge Conflicts in Multilingual RAG (Mohan et al.; MeLLM 2026, pp. 92–107) | Abstract: 21 languages, RAG vs. non-RAG; non-Latin-script languages show larger drops and more hallucination. Script effects across *languages*, not script variants of the same language; no abstention per abstract. | Related Work; motivates H1 | metadata-verified, abstract-read (summary) |
| 8 | arXiv:2503.23687 | MKA: Leveraging Cross-Lingual Consensus for Model Abstention (Duwal; ICLR 2025 Building Trust workshop) | Abstract: multilingual consensus pipeline for confidence calibration/abstention; reports Bengali gains. No script variants, no RAG. Possible baseline/Related Work. | RQ4 (adjacent) | metadata-verified, abstract-read |
| 9 | arXiv:2609.04653 | Choosing the Right Language Mode at Inference Time for Multilingual Reliability (Mitra, Agrawal; Findings of EMNLP 2026 per arXiv) | Abstract: target-only vs English vs bilingual context; ECE-aware routing. Related to our pivot-language intervention RQ4-(iii); no script/RAG/abstention thresholds. | RQ4-(iii) | metadata-verified, abstract-read |
| 10 | arXiv:2607.08456 | Two Axes of LLM Abstention: Answer Correctness and Question Answerability (Wagner; v1 9 Jul 2026) | Abstract: separate thresholds for answerability vs correctness; English only per page. Methodological relevance for M3 thresholds. | method | metadata-verified, abstract-read (via arXiv API abstract) |
| 11 | arXiv:2610.22892 | Bengali Hallucination Detection with Retrieval and Programs: A System Study | Bengali hallucination detection system (Olikbochon challenge); not abstention, no script variants. | Related Work | abstract-read (arXiv API); abs page not opened |
| 12 | arXiv:2507.23248 | Script Fragmentation and Format: What Drives the English-Bengali Performance Gap in Open LLMs? | Title suggests script-related EN–BN gap analysis; S2 hit only. | RQ3 background | found-only |
| 13 | arXiv:2603.05462 | NCTB-QA: A Large-Scale Bangla Educational QA Dataset | Bangla answerable/unanswerable QA (encoder models). Possible item-source/related work. | none (adjacent) | abstract-read (arXiv API) |
| — | found-only, low threat | "Trust-Calibrated Multilingual RAG for Humanitarian Information Platforms" (IJGD); "Trustworthy Smishing Detection in Code-Mixed Bangla-English SMS … Selective Classification" (Scholar); "CalibJudge" (Scholar); "Cross-Lingual RAG … Confidence-Aware Hallucination Detection" (Scholar); "Fine-Tuning Creates Confident Errors … Bengali–English Agricultural QA" (Scholar); BHRE-RAG (DOI 10.1109/ICCIT68739.2025.11491594); BanglaMedQA [arXiv:2511.04560]; KrishokChat [arXiv:2606.29243] | Adjacent; none appears (from title/snippet) to test EN-calibrated threshold transfer to Bengali script variants under controlled sufficiency. | — | found-only |

### Provisional reading for G1 (abstract-level only; [HYPOTHESIS])
- **RQ2 (threshold transfer across scripts):** No hit tests an English-selected abstention/sufficiency threshold on BN/RBN/CM variants of the same RAG item. However, the *general idea* "operating points tuned on clean English do not transfer to paired code-mixed inputs" is now present in arXiv:2606.05654 (moderation, Tamil-English), and multilingual threshold selection for selective prediction is analysed in arXiv:2607.06327 (MCQA, 22 languages). The plan's §4 claim "*Novel element: the transfer question itself*" should be **narrowed** to: transfer across scripts/code-mix of one language, for abstention in RAG, under controlled evidence sufficiency.
- **RQ1 (paired script variants + sufficiency):** Paired native/romanized/code-mixed Bangla items exist for safety (arXiv:2610.24288); paired matched-fact EN/HI/Hinglish QA exists for hallucination probing (arXiv:2609.22138). No hit combines paired script variants with minimal-edit sufficient/insufficient evidence. Item 5 (Springer) and item 6 (Scholar-only) are unresolved and must be checked.
- **RQ3:** arXiv:2607.06327's "comprehension intact, generation is the bottleneck" claim (abstract) is directly relevant and may pre-empt or contradict H3; full-read required.

## Addendum — lead researcher follow-up (2026-10-23)

| # | Date | Source | Query / URL | Hit count | Result |
|---|---|---|---|---|---|
| L1 | 2026-10-23 | arXiv API `id_list` | 2606.05654, 2607.06327, 2610.24288, 2609.22138, 2609.04653, 2503.23687 | 6/6 resolved | Titles/authors match the search agent's report; abstracts read. 2607.06327 and 2609.04653 carry "Accepted at Findings of EMNLP 2026" comments. |
| L2 | 2026-10-23 | Crossref API + Springer page (browser) | DOI 10.1007/978-3-032-27754-1_37 | 1 | **metadata-verified, abstract-read.** Gaikwad, S. S. & Gaikwad, J. S. (2026). "Reducing Hallucinations in Retrieval-Augmented LLM Question Answering for Indian Code-Mixed Queries." *Smart Trends in Computing and Communications*, LNNS, pp. 402–415. Abstract: RAG framework with code-mixed query normalisation and a "Hallucination Control Layer" that "enforces explicit abstention when supporting information is insufficient"; custom English/Hindi/Hindi–English dataset. Full text paywalled → no claims beyond the abstract. No Bengali, no romanized-script condition, no threshold transfer. |
| L3 | 2026-10-23 | Web search (standard + extended) | `"Probe Before you Answer" cross-lingual answerability abstention` | 0 exact-title matches | **Unresolved.** Not found outside Google Scholar listings. Author to check in a browser (Scholar) before G1 is closed; treated as non-existent for citation purposes until found. |
| L4 | 2026-10-23 | Web search (extended) → ScienceDirect (browser) | DOI 10.32604/cmc.2026.086343 | 1 (new) | **metadata-verified, abstract-read (+ sections 4.2, 8 skimmed).** Zhang, H. & Wu, W. (2026). "Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration in Retrieval-Augmented Generation." *Computers, Materials & Continua* 89(1), open access. Five evidence levels (full/partial support, irrelevant, no context, conflicting); SQuAD + HotpotQA (English only; §4.2); 7 models, 3 prompts; multilingual extension named as future work (§8). Relevant as an English controlled-sufficiency benchmark; **no language/script variation, no threshold transfer.** |
