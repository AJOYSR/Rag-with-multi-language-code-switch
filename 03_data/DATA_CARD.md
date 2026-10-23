# Data Card (draft — to be completed in M3)

| Field | Value |
|---|---|
| Name | TBD |
| Version | 0.1 — pilot draft (30 items, AI-drafted, **awaiting author review**) |
| Base items | target 150–200 (pilot: 30) |
| Variants | EN, BN (Bengali script), RBN (romanized), CM (Bengali script + English insertions), CMR (romanized + English insertions) — 2×2 script × mixing design (decision_log 2026-10-23); RBN rules in `variants/RBN_convention.md` |
| Conditions | sufficient / insufficient evidence (minimal edit) |
| Sources | Pilot: 30 **fictional** notices written for this project (no external source text; licence: project-owned). Wikipedia realism subset planned for M3; each raw doc will be logged in `raw/SOURCES.csv` (id, url, access_date, licence) |
| Construction | Pilot passages, questions and all variants **drafted by an AI agent (Claude Opus 5.5, 2026-10-23)**; author review/edit pending (`variants/review_pilot*.csv`); edit rate will be recorded in `variants/review_outcome.json`. Insufficient passages are generated programmatically from a marked answer sentence + replacement, with automatic checks (gold absent from insufficient passage; near-miss sibling answer present). |
| Validation | TBD — second-annotator sample size, percent agreement, κ, dropped items |
| Closed-book filter | TBD — items answerable without evidence, per model |
| Splits | by base item; dev ≈ 25%, test ≈ 75%, stratified by answer type |
| Licence of release | TBD (must be compatible with every source) |
| Known issues | Fictional names may accidentally match real entities (author check pending). Yes/no items have a 50% closed-book guessing baseline. Pilot items are dev-only (used for prompt/setting choices). |
| Personal data | None (KYC or other employer data excluded by design) |
