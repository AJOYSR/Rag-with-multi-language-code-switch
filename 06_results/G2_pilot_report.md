# G2 Pilot Report — Effect Gate

2026-10-24 · Prepared by the AI research agent for Ajoy Sarker · **Status: awaiting the author's G2 decision**

## 0. What was run

- **Items:** 30 author-reviewed fictional notices (`03_data/processed/pilot_items_approved.yaml`), 6 per answer type. Each item has a sufficient and an insufficient version (minimal edit) and a near-miss sibling question. Every question exists in EN, BN, RBN, CM and CMR. **All pilot items are dev-only.**
- **Models:** two runs at git commit `8ed730b`, Ollama 0.40.9, temperature 0, seed 0:
  - `20261024_pilot_qwen35_9b`: `hf.co/bartowski/Qwen_Qwen3.5-9B-GGUF:Q4_K_M` (digest `446dc6a1b5ef`)
  - `20261024_pilot_gemma2_9b`: `hf.co/bartowski/gemma-2-9b-it-GGUF:Q4_K_M` (digest `85d7938fc7b3`)
- **Calls:** 1,620 per model. Generation time: 21 min (Qwen) and 68 min (Gemma). Cost: $0, all local.
- **Methods:**
  - M1: instructed abstention.
  - GEN: answer with no abstention option.
  - SUFF: sufficiency rater.
  - M3: GEN gated by a logistic combiner of P(sufficient) and answer confidence, fitted on EN.
  - CB: closed-book control.
  - TR: comprehension probe (the model translates the question into English).
- **Sources:**
  - every number below comes from `06_results/tables/20261024_pilot_*` and `06_results/pilot_analysis_stdout.txt`;
  - code: `05_experiments/src/analyze_pilot.py`;
  - CIs: 95% percentile bootstrap over items, 2,000 resamples.

### How the outcome measure was settled (disclosed; it will be frozen in the protocol)
Reading the raw outputs showed that the first scoring rule counted *non-committal restatements* as answers. Examples: "তারিখ পরে জানানো হবে" (the date will be announced later) and "An experienced trainer". These are implicit abstentions.

Each response is now put into one of four categories by deterministic, unit-tested rules: **abstain / non-specific / specific / ambiguous**. **Only "specific" responses count as answering.** Of the 3,240 responses, **7 were ambiguous** (yes/no questions answered with a full statement). They were adjudicated in `06_results/adjudication_pilot.csv`: the author accepted all of the agent's proposed labels.

The preliminary Qwen figures the agent reported in chat earlier (RBN 13%, CMR 17%) were produced **before** this correction. **They are superseded.**

## 1. Results [RESULT]

### 1.1 M1 (instructed abstention): main question
UAR = answers given on insufficient evidence (hallucination). UNR = refusals on sufficient evidence (over-abstention). n = 30 items per cell.

| Variant | Qwen UAR | Qwen UNR | Gemma UAR | Gemma UNR |
|---|---|---|---|---|
| EN | 3.3% [0, 10.0] | 0% | 3.3% [0, 10.0] | 0% |
| BN | 3.3% [0, 10.0] | 0% | 0% | 0% |
| RBN | 6.7% [0, 16.7] | 3.3% [0, 10.0] | 6.7% [0, 16.7] | **10.0% [0, 23.3]** |
| CM | 0% | 0% | 0% | 0% |
| CMR | **10.0% [0, 23.3]** | 0% | 0% | 3.3% [0, 10.0] |

Paired differences against EN (bootstrap 95% CI):

| Contrast | Qwen | Gemma |
|---|---|---|
| RBN−EN, UAR | +3.3 pp [−6.7, +13.3] | +3.3 pp [−6.7, +13.3] |
| RBN−EN, UNR | +3.3 pp [0, +10.0] | **+10.0 pp [0, +23.3]** |
| CMR−EN, UAR | **+6.7 pp [−6.7, +20.0]** | −3.3 pp [−10.0, 0] |
| CMR−EN, UNR | 0 | +3.3 pp [0, +10.0] |
| BN−EN and CM−EN | ≤ 3.3 pp in either direction | ≤ 3.3 pp in either direction |

When a model answered on sufficient evidence, the answer was correct 96.6–100% of the time.

### 1.2 Controls
- **Near-miss sibling (abstention is not triggered just by the edit):** the sibling question, answerable from the *insufficient* passage, was answered correctly in 30/30 cases for every variant (Qwen) and in 29–30/30 (Gemma; RBN 29/30).
- **Closed-book contamination:**
  - amount, date and name questions: 0 of 30 answered correctly without the notice, for both models;
  - number questions: Qwen 1 of 30, Gemma 0 of 30;
  - yes/no questions: Qwen 6 of 30, Gemma 2 of 30. That is consistent with guessing (the guessing baseline is 50%).
  - **The fictional-notice design removes memorisation as a confound.**
- **GEN (no abstention option):** UAR is 20–27% (Qwen) and 17–27% (Gemma) across all variants, with **no variant gap**. It runs above M1 for every variant and model, so the abstention instruction is what does the work.

### 1.3 Sufficiency rater and threshold transfer (RQ2 preview; EXPLORATORY, in-sample)

| | EN | BN | RBN | CM | CMR |
|---|---|---|---|---|---|
| Qwen rater accuracy | 0.90 | 0.90 | **0.78** | 0.90 | 0.87 |
| Qwen mean P(suff) on *insufficient* | 0.25 | 0.25 | **0.48** | 0.29 | 0.39 |
| Gemma rater accuracy | 0.90 | 0.92 | 0.88 | 0.92 | 0.90 |
| Gemma mean P(suff) on *insufficient* | 0.13 | 0.10 | 0.17 | 0.10 | 0.14 |

M3 with a threshold chosen on EN for a target risk of 10%:

| | EN | BN | RBN | CM | CMR |
|---|---|---|---|---|---|
| Qwen realised risk | 9.1% | 6.2% | **14.3% (+4.3 pp)** | 9.1% | 9.1% |
| Gemma realised risk | 9.4% | 9.1% | 7.1% | 6.2% | 3.3% |

These are in-sample on 30 items, and some cells rest on one or two errors, so **this is not evidence yet.** It shows only that the RQ2 machinery works and that Qwen's sufficiency signal **shifts upward on romanized insufficient items**.

### 1.4 Comprehension probe (RQ3 preview; automatic proxy, see `TR_comprehension_PROXY` tables)
Share of translations with less than 50% content-word overlap with the EN question:

| | BN | CM | CMR | RBN |
|---|---|---|---|---|
| Qwen | 17% | 3% | 13% | **90%** |
| Gemma | 20% | 3% | 7% | **80%** |

Reading the outputs confirms that most romanized questions are misunderstood when shown on their own. For example, "abedon fee koto taka?" became "How much does Abedon cost?" (Qwen) and "How much money do you have?" (Gemma); "proti mashe koto taka britti…" became "…given for the bribe?".

**Yet M1 behaviour on RBN stays close to EN.** A plausible explanation [HYPOTHESIS] is that the models match words in the romanized question to the Bengali passage, so the passage stands in for comprehension. That is exactly the kind of mechanism RQ3 should separate. *Caveat:* the probe translates the question **without** the passage. Its 50% threshold is an arbitrary proxy and must be replaced by human judgment in the main study.

## 2. Power for the full study
The study plans about 130 test items, using paired McNemar tests (α = .05, 80% power, before Holm correction). Detectable differences, given the pilot's discordance:

| Contrast | Items needed for the observed difference | Minimum detectable difference at n = 130 |
|---|---|---|
| Gemma RBN−EN UNR (+10 pp) | **76** | 7.8 pp |
| Qwen CMR−EN UAR (+6.7 pp) | 233 | 9.0 pp |
| Qwen RBN−EN UAR (+3.3 pp) | 704 | 7.8 pp |

**Implication:** at about 130 test items, the study can detect differences of roughly 8 pp or more. Smaller effects of 3–5 pp would be missed. Raising this would mean 250–300 base items, which is more review time than planned.

## 3. Assessment against the G2 criterion
**Criterion (CLAUDE.md):** proceed if the gap is at least 5 pp, or if there is a clear reason to continue such as over-abstention (H1-alt).

- **Point estimates of at least 5 pp occur** for Gemma RBN UNR (+10 pp, the H1-alt direction) and Qwen CMR UAR (+6.7 pp). **No confidence interval excludes zero.** With 30 items that is expected; the evidence is suggestive, not conclusive.
- **Under the main method (M1), the core hallucination effect (H1) is small.** Explicitly instructed 9B models abstain well on these short, clean notices in every variant. This is a **floor effect**: EN UAR is only 3%.
- **There are clear reasons to continue:**
  1. over-abstention on RBN (H1-alt), which is consistent with prior findings (Khullar et al., A4; Feng et al., A2);
  2. **a shift in the sufficiency score on romanized input** for Qwen, which is the RQ2 phenomenon;
  3. **near-total comprehension failure on RBN without matching behavioural failure**, a new and paper-worthy RQ3 observation.
- **Threats:** floor effects; a single seed and a single prompt; questions shown in isolation in the comprehension probe; 30 items.

## 4. Recommendation [REC]
**Proceed, with four design changes**, rather than pivot:

1. **Make the abstention decision harder, so effects don't sit at the floor.** Add realistic difficulty:
   - two to three passages per item, one of them a near-miss distractor such as another doctor's name or another date;
   - longer notices of 150–300 words;
   - "neutralised" insufficient edits as well as deletions.
   - Keep the 30 pilot items as dev.
2. **Make RQ2 (threshold/score transfer) and H1-alt (UNR) co-primary**, alongside UAR. The pilot signal is in the score shift and in over-abstention, not in M1 hallucination. Add M2b (token-probability confidence), which is already logged.
3. **RQ3:**
   - run the comprehension probe **with the passage present**;
   - have a human judge translation correctness on a sample;
   - keep the no-passage probe as a secondary measure.
4. **Scale to about 200 base items, if author time allows** (about 150 test items, enough to detect about 7–8 pp). Pre-register that effects below about 7 pp may go undetected, and report effect sizes with CIs whatever the outcome.

**Alternative, if the author prefers:** keep the design as it is and frame the paper around "abstention holds; comprehension doesn't". That is publishable as a careful null, but the current floor effect makes it weaker.

## 5. Decision needed from the author
- **(a) Proceed with the four changes, proceed unchanged, or pivot?**
- **(b) Target size:** about 200 base items (about 8 h of your review plus about 8–10 h for the second annotator), or 150.

Once you decide, Phase 4b begins: protocol draft, then your approval, then a freeze with a commit hash.
