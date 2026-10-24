# Annotation Guidelines: Second Native-Speaker Validation

Version 0.9 (draft, 2026-10-24) · For the second annotator · Estimated time: 8–10 hours for about 40 items

## Purpose
This study asks whether AI systems decide to *answer* or *refuse* equally reliably when the same question is written in different forms of Bengali. That comparison is only fair if **every version asks exactly the same thing**. Your job is to check that independently. Your ratings are reported in the paper as an agreement statistic, and with your permission you will be credited in the acknowledgements.

You will **not** see any AI model's answers, and you do not need to judge AI behaviour.

## What you receive
A UTF-8 spreadsheet (`annotation_sample.csv`). When saving, choose **"CSV UTF-8"**, because plain CSV destroys Bengali text. Each row is **one question in one version**, alongside its English reference:

| Code | Version |
|---|---|
| BN | Bengali script, Bengali only |
| RBN | Bengali in English letters (romanized), Bengali only |
| CM | Bengali script with some English words in English letters |
| CMR | Romanized Bengali with some English words |

Some rows also show a **short fictional notice** and its **edited version**, where one fact was removed or made vague.

## Task 1: Meaning equivalence (every row)
Compare the version with the English reference and ask: *would a person asking this version expect exactly the same answer?*

| Score | Meaning | Example (reference: "What is the application fee?") |
|---|---|---|
| **3: Same** | Same request, same expected answer | `application fee koto taka?` |
| **2: Minor difference** | Small nuance, same answer | `abedon korte koto lage?` (cost to apply, same figure) |
| **1: Different** | A different or broader request, so the answer could differ | `vortir khoroch koto?` (admission cost, not the application fee) |

Rate the meaning only, not spelling or style.

## Task 2: Naturalness (every row)
Ask: *would a real Bangladeshi user plausibly type this, in this form?*

| Score | Meaning |
|---|---|
| **3: Natural** | Typical of how people write |
| **2: Acceptable** | Understandable but a little stiff or unusual |
| **1: Unnatural** | Nobody would write it this way |

For romanized text, ordinary spelling variation (kobe / kbe, taka / tk) is natural. Mark **1** only if it reads like a machine wrote it or no one would type it.

## Task 3: Insufficiency check (notice rows only)
Read the **edited notice** and the question. Then ask: *can the answer still be found or confidently worked out from this edited notice?*
- **N (cannot):** the answer is truly missing. This is what we want.
- **Y (can):** the answer is still there or can be inferred. In the comment, quote the words that give it away.

Example: the question asks for the fee. The edited notice says "the fee must be paid via bKash" but gives no amount, so the answer is **N**.

## Rules
- Work **independently**. Don't discuss items with the author until you've finished.
- If unsure, choose the lower score and explain in `comment`.
- Don't edit the question text. Suggest a fix in `comment` instead.
- Take breaks. Sessions of about 1 hour work well.

## What happens with your ratings
- We compute percent agreement and Cohen's κ between you and the author.
- Any version you rate **1** on meaning is revised and re-checked, or removed.
- Any notice you mark **Y** is fixed or removed.
- Your ratings are stored without your name in the released data. You decide whether to be named in the acknowledgements.

## Consent
Before you start, the author will explain the study and confirm that you agree to take part, to having your anonymised ratings published, and how you want to be credited. You can stop at any time.
