# Open Questions

| # | Question | Blocks | Resolve by | Status |
|---|---|---|---|---|
| Q1 | What hardware is available for local inference (GPU / RAM / Apple Silicon)? Is Colab or Kaggle acceptable? | Model choice, budget (§6.3–6.4) | Week 1 | **resolved 2026-10-23** — local Ollama, 4-bit GGUF, Apple M5 16 GB |
| Q2 | Is a second native Bengali speaker available to validate ≥ 20% of variants (≈ 6–10 h of work)? | Gate G3 | Week 1 | **resolved 2026-10-23** — author reports annotator lined up |
| Q3 | Which primary venue: ARR → EMNLP 2027, or an earlier workshop (TrustNLP / BLP)? | Timeline end-date | After G2 | open |
| Q4 | Is the calibration-language paper published or under review? (Affects self-citation and anonymity.) | Related Work, anonymisation | Before writing | **resolved 2026-10-23** — unpublished draft; not cited |
| Q5 | Do NoMIRACL / MIRACL / MIRAGE-Bench / M-AbstainQA include Bengali, and under what licence? | Dataset reuse (§6.2) | M1 | **resolved 2026-10-23** — all four include Bengali (native script only; MIRAGE-Bench dev only). Licences: NoMIRACL conflicting (paper CC BY-SA 4.0 vs card Apache-2.0), MIRACL Apache-2.0, MIRAGE-Bench data unstated, M-AbstainQA none. Not used as core data. See `02_literature/verification_BC.md` |
| Q6 | Which romanization convention should be the canonical RBN (e.g., phonetic "Avro-style" vs. ad-hoc chat style)? | Variant construction | Before M3 | open — BanglaShield (App. H) notes romanized Bangla has no standard spelling and merges ই/ঈ, শ/ষ/স; offers no reusable convention |
| Q7 | Can a citable source be found for the prevalence of romanized / code-mixed Bengali among users? | Introduction motivation | M6 | open — BanglaShield §1 cites only offensive-language dataset papers (not prevalence studies); still needed |
| Q8 | What licence terms apply to Bangladeshi government notices and university circulars? | Document sources (§6.1) | Before M3 | open |
| Q9 | Does "Probe Before you Answer" (Google Scholar-only listing) exist, and does it overlap RQ2? | G1 completeness | G1 | open — author to check in browser |
| Q10 | Licence for adapting Joren et al.'s autorater prompt (repo has no licence; paper is CC BY 4.0) | M3 method release | Before M3 | open — [REC] adapt from paper App. C.1 with attribution |
