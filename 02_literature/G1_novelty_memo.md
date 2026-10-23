# G1 Novelty Memo — Abstention Transfer Across Scripts (Bengali–English RAG)

2026-10-23 · Prepared by the AI research agent for Ajoy Sarker · **Status: awaiting the author's decision**

Evidence base: 9 papers full-read, with notes in `notes/` and every quote string-matched to the source (A1–A9 in `literature_matrix.md`). Searches are logged in `search_log.md`: arXiv, Semantic Scholar, Google Scholar and ACL Anthology, plus a citation chase of A1 (122 citing papers) and A2 (20).

## 1. What is known [FACT, full-read]

- **Abstention degrades outside English, including in Bengali**, but only for native-script, machine-translated, closed-book multiple-choice QA. Feng et al. (2024) report gaps of "up to 20.5%" and that abstention decisions are "only somewhat transferable" across languages (§5). Alfarano et al. (2026) find lower uncertainty-estimation quality for Bengali than for English.
- **Romanization hurts reliability and shifts models toward abstaining.** In Khullar et al. (2025/26), romanized inputs score up to 24 points worse, and the "insufficient information" label on non-emergency messages rises from 12.8% to 25.2% (Table 2). Bengali is not covered. In BanglaShield (Kabir et al. 2026), the rate at which unsafe Bengali prompts are labelled safe rises from 47.0% (native) to 63.4% (romanized).
- **Multilingual RAG abstention including Bengali has been measured, but on relevance, not sufficiency.** In NoMIRACL, GPT-3.5 hallucinates on 95.2% of Bengali non-relevant sets. Abstention is detected by a rule, with no scores or thresholds.
- **English-tuned thresholds do not transfer cleanly.**
  - Alfarano et al. (2026) apply an English-tuned threshold to 22 languages. It reduces errors by 43%, against 60% for language-specific thresholds. The threshold is chosen by F1 and the results are pooled across languages.
  - Thimma Krishnaram et al. (2026) freeze thresholds tuned on clean English and apply them to paired Tamil–English code-mixed input. This flips 26.5% of moderation decisions. The task is classification, not RAG.
- **The sufficiency lens exists, but only in English** (Joren et al. 2025; Zhang & Wu 2026, abstract-read).

## 2. The three closest works

| | Overlap with us | What it leaves open |
|---|---|---|
| **Alfarano et al. 2026** (Findings EMNLP 2026) | An English-tuned abstention threshold applied to other languages, Bengali included; English reasoning used as a pivot | No evidence or RAG; native script only; threshold chosen by F1, not target risk; no realised risk per language; comprehension inferred, not measured |
| **Thimma Krishnaram et al. 2026** | Frozen English thresholds applied to *paired* code-mixed inputs | Moderation classification; Tamil; script not separated from code-mixing; no comprehension-vs-calibration split |
| **Khullar et al. 2025/26** | The native-vs-romanized gap; over-abstention; script normalisation as a mitigation | Indian languages, not Bengali; triage classification; no thresholds or calibration |

## 3. Is RQ2 already answered?

**Partly. The generic question is answered; our specific question is not.** [REC]

We can no longer claim the general idea that "English-calibrated thresholds may not transfer" (A7, A8). Our search found no study that does all of the following together:
- selects a threshold on English dev data **for a target risk**;
- measures **realised risk and coverage per variant**, with confidence intervals;
- uses **evidence-sufficiency abstention in RAG** with minimal-edit insufficient evidence;
- uses **native-script, romanized and code-mixed renderings of the same item**, kept as separate conditions;
- for Bengali or any other language.

**Residual risks:**
- Three relevant papers appeared between June and October 2026, so the area is moving fast.
- One Scholar-only title, "Probe Before you Answer", is still unresolved.
- Coverage of the ACL Anthology and of Scholar "cited by" was partial.

## 4. Recommendation: **proceed, with a reframing** (not a pivot to Topic 2)

1. **Narrow the novelty claim.** Proposed wording: *"Prior work shows that English-tuned thresholds lose effectiveness in other languages (Alfarano et al., 2026) and on paired code-mixed input (Thimma Krishnaram et al., 2026). To our knowledge, no study tests whether a threshold selected for a target risk holds on native-script, romanized and code-mixed renderings of the same RAG items under controlled evidence sufficiency."* Never write "first".
2. **Make target-risk transfer the core of RQ2.** Report realised against target risk per variant, with bootstrap CIs. This is what separates us from A7, which uses an F1 threshold and pools across languages.
3. **Make RQ3 measure comprehension directly** with a per-item check, rather than inferring it as A7 does.
4. **Reposition RQ4.** The pivot-language judgment is no longer a new idea, so treat it as a baseline. Split it into an English-reasoning arm (like A7) and a transliterate-or-translate arm (like A4). Also add A4's label-triggered normalisation routing as a baseline. Per-variant thresholds remain the primary intervention.
5. **Pre-register H1 and H1-alt as two-sided.** Prior evidence now points toward over-abstention (A2 App. A, A4 Table 2, A8). Under-abstention is still the English pattern (A1).
6. **Make human-validated variants a selling point.** A8 and A9 generate their variants automatically, A9 without any human validation.

## 5. Other findings that affect later phases

- **Q5 (dataset reuse):**
  - Bengali is present in NoMIRACL, MIRACL, MIRAGE-Bench (dev only) and M-AbstainQA, in native script only.
  - Licences:
    - NoMIRACL has a conflict: the paper says CC BY-SA 4.0, while the card and repo say Apache-2.0.
    - MIRACL is Apache-2.0.
    - MIRAGE-Bench's data licence is not stated.
    - M-AbstainQA has no licence.
  - [REC] Reuse none of them as core data. Build our own fictional notices, as planned.
- **M3 prompts:**
  - Joren's GitHub repository has no licence and no code. We would adapt the prompt from App. C.1 of the CC BY 4.0 paper, with attribution.
  - App. C.2 of v3 has its labels swapped. Use the README version.
- **Answer scoring:** Marwah et al. show that a model answering in another script breaks exact match (§5.3). Our normalisation must map answers across scripts.

## 6. Decisions needed from the author

- **(a) Proceed, reframe or pivot?** I recommend proceeding with the reframing in §4.
- **(b) Two manual checks:**
  - Look up "Probe Before you Answer" on Google Scholar.
  - Repeat the ACL Anthology searches in its own search box.
  - About 20 minutes in total.
- **(c) Approve the narrowed contribution wording in plan §4 and the revised gap statement in plan §2.**
