# Pilot Review: Instructions for the Author

**Why this is needed:** the AI agent (Claude Opus 5.5) drafted every passage and every question variant. The research protocol (CLAUDE.md §3, Phase 4a) does not allow the pilot to run on text that a native speaker has not reviewed, and the paper must disclose who wrote and edited each part. **Estimated time: 2–3 hours.**

Open both CSV files in Excel, Numbers or Google Sheets. They are UTF-8, so Bengali should display correctly.

## File 1: `review_pilot_passages.csv` (30 rows)
For each fictional notice:
1. Read `passage_SUFFICIENT`. Does it read like a real Bangladeshi notice? If not, write a corrected version in `passage_EDIT`.
2. Read `passage_INSUFFICIENT`. This is the same notice with the answer removed or neutralised. **Can the answer to the main question still be worked out from it?** Put `Y` in `insufficient_really_unanswerable` only if it truly cannot. If it can, suggest a better wording in `replacement_EDIT`. Pay most attention to items **P05, P10, P14, P24 and P29**, where a reader might infer the answer from what is left.
3. `names_fictional_ok`: put `N` if any institution, place or person name matches a real organisation or a well-known person.
4. `STATUS`: `approve`, `edit` or `drop`.

## File 2: `review_pilot.csv` (60 rows: main and sibling question per item)
Columns `en / bn / rbn / cm / cmr` hold the five versions of one question:
- **en**: English
- **bn**: Bengali script, Bengali only
- **rbn**: romanized Bengali, Bengali only (rules in `RBN_convention.md`)
- **cm**: Bengali script with some English words in English letters
- **cmr**: romanized Bengali with some English words, as typed in chat

For each row:
1. Is every version **the same question**, with the same meaning and the same expected answer? Mark `meaning_equivalent_all`.
2. Does each version sound like something a real person would type? Mark `natural`. Correct anything unnatural in the matching `*_EDIT` column. Leave `*_EDIT` blank if no change is needed.
3. `STATUS`: `approve`, `edit` or `drop`.

## Please also decide
- **Romanization convention (Q6):** is `RBN_convention.md` acceptable? Write any changes at the bottom of that file.
- Save the returned files as `review_pilot_RETURNED.csv` and `review_pilot_passages_RETURNED.csv` in this folder.

The agent will then apply your edits to produce `03_data/processed/pilot_items_approved.yaml`, re-run the automatic checks, log the edit rate, and start the pilot. **Your edits are not changed silently.** Any edit that fails an automatic check, for example a gold answer still present in an insufficient passage, will be sent back to you.
