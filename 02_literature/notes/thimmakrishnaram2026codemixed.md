# thimmakrishnaram2026codemixed — When Surface Form Changes Moderation Decisions: A Paired Study of Code-Mixed Workflow Instability

**Read status:** full-read (2026-10-23). Source: the arXiv PDF of **v2** (https://arxiv.org/pdf/2606.05654, 9 pages; the PDF margin stamp reads "arXiv:2606.05654v2 [cs.SE] 5 Jun 2026"). Text was extracted with pypdf and read in full: Abstract, §I–§VIII, Tables I–V, figure captions, references. Figures 1–3 are images, so only their captions were read. v1 was not read. The abs page lists both versions at the same size (2,328 KB) and gives no reason for the revision. The HTML rendering was downloaded but not used.

## Bibliographic metadata (confirmed on the arXiv abs page, 2026-10-23)

- **Title:** When Surface Form Changes Moderation Decisions: A Paired Study of Code-Mixed Workflow Instability [FACT; `citation_title`]
- **Authors:** Suraj Babu Thimma Krishnaram, Yibo Hu, Karthikeyan Saravanan (Illinois Institute of Technology, per the PDF header) [FACT]
- **arXiv:** 2606.05654. v1 was submitted on 4 Jun 2026 and v2 on 5 Jun 2026; v2 is current. Primary class: **cs.SE**, cross-listed to cs.AI and cs.LG. [FACT; abs page]
- **Venue:** the abs page has no Comments or venue field. The paper is an unrefereed preprint as far as we can verify. [FACT]
- **Licence of the paper:** CC BY 4.0 (abs page licence link `licenses/by/4.0/`). [FACT]
- **Code:** https://github.com/Surajtk/workflow-moderation-code (§I, "Code availability"). The GitHub API reports an **MIT** licence. The repo contains three notebooks (data cleaning, training, workflow evaluation) plus a LICENSE and a README. [FACT; GitHub API, 2026-10-23] I did not open the notebooks.
- URLs: https://arxiv.org/abs/2606.05654 ; https://arxiv.org/pdf/2606.05654

Suggested bibkey: `thimmakrishnaram2026codemixed`. Use the arXiv preprint type (cs.SE).

## Objective

The paper treats hate moderation as action routing (ALLOW / FLAG / REVIEW) rather than classification. It asks whether paired clean-English and Tamil–English code-mixed versions of the same content receive different routed actions under a fixed operating point tuned on English (§I; §II-B: "we study whether paired clean and code-mixed versions of the same underlying content trigger different moderation actions under a fixed operating point").

## Data

- **Source:** HateBenchSet (Shen et al., USENIX Security 2025). It has 7,838 manually labelled samples covering 34 identity groups (§III-B, fn. 2: huggingface `TrustAIRLab/HateBenchSet`). [FACT] [INFERENCE: HateBench is about LLM-generated hate content, so the "clean English" sources are themselves partly LLM-generated text. The paper does not discuss this.]
- **Code-mix creation:** **automatic**. "Code-mix generation follows the public CodeMixBench-style preprocessing pipeline [5], [20]" (§III-B, using the CodeMixBench implementation, fn. 1). The paper does **not** name the generator model, say whether it is an LLM or MT system, or give the prompt. Its own Limitations section calls the views "automatically generated" (§VII). It is **not** human-written. [FACT] [INFERENCE: CodeMixBench (Yang & Chai, EMNLP 2025) is an LLM-based benchmark, so the generator is probably an LLM. This is not verified here, and I did not read CodeMixBench.]
- **Validation:** "we manually inspect 500 randomly sampled generated pairs and remove low-quality or label-inconsistent examples"; "In total, we filter approximately 1,000 candidate rows (about 25% of the initially generated set)" (§III-B, p.4). The paper does not say who inspected the pairs, whether they were native Tamil speakers, or what the agreement was. [FACT: these are not reported] It also does not explain how 1,000 rows were removed when only 500 were inspected. [INFERENCE: this suggests automatic filtering as well, which the paper does not describe]
- **Variants:** English (`x_en`), Tamil–English code-mix (`x_mix`, described as including "mixed-language tokens, romanized forms, and non-standard spellings", §III-B), and a **Tamil-only** diagnostic view (§III-B). The paper does not say which script the Tamil-only view uses. The code-mixed examples in Table IV are **romanized Tamil–English** (e.g., "Muslim aga iruppathil entha problem-um illa..."). [FACT; Table IV]
- **Splits:** a 738-example clean English dev split for threshold selection; 3,017 paired test examples per view (§III-B, p.4).
- **Labels:** inherited from the English source without re-annotation (§III-B: "y ∈ {hate, non-hate}: the inherited gold label").
- **Release:** the code is released under MIT. The paper does not say whether the generated paired dataset is released. [FACT: not stated]

## Method — thresholds tuned on English dev, then frozen

- **Detector:** mBERT (`bert-base-multilingual-cased`) fine-tuned on the English training view for binary hate/non-hate. HateBERT and MetaHateBERT are used zero-shot as supporting detectors (§IV-A). These are **classifier scores, not LLM generation**, and there is **no retrieval or evidence**.
- **Decision layer (§III-A):** ALLOW if s(x) < τ_low, FLAG if s(x) > τ_high, otherwise REVIEW.
- **Operating criterion (§III-D):** "min RR s.t. HFA ≤ ε_H, NFF ≤ ε_NH" with ε_H = 0.05 and ε_NH = 0.10. Among feasible pairs, the pair with the lowest review rate is chosen.
- **Tuning procedure (§IV-B):** a grid sweep with τ_low ∈ {0.001, 0.006, …, 0.196} and τ_high ∈ {0.800, 0.805, …, 0.995}, run on the 738 clean English dev examples. The selected pair is τ_low = 0.031, τ_high = 0.800, which gives dev HFA = 0.0478, NFF = 0.0733, RR = 0.1341. The thresholds are then **frozen** for the clean, code-mix and Tamil test sets ("without retuning on stressed conditions", §IV-B).
- **Is this risk control or selective prediction?** It is a **risk-budget operating point**: constrained error rates with deferral to REVIEW. The paper explicitly links it to abstention and selective prediction (§II-C, citing Xin et al. 2021). [FACT] It does **not** use conformal or finite-sample risk-control guarantees. The constraint is checked only empirically on dev, and the paper does not test whether the realised test HFA/NFF stays within ε. [FACT: no such analysis appears] [INFERENCE: from Table I, the code-mix test NFF of 0.104 exceeds ε_NH = 0.10, while code-mix HFA of 0.011 stays well under ε_H. The authors never frame this as a budget violation.]
- **Confidence-abstention baseline (§III-E):** a single threshold τ_conf on max-class probability, tuned on English dev under the same criterion (τ_conf = 0.965) and frozen.
- **Mitigation, "disagreement-based deferral" (§III-F):** run the pipeline on the English view and an alternate view (code-mix or Tamil). If the routed actions disagree, route to REVIEW. This is training-free and assumes both paired views are available at inference time. The paper does not implement or cost an auxiliary-view generator (translation, transliteration or normalisation are only mentioned, §III-F, §VII).
- **No per-variant recalibration or retuning** is evaluated. The paper says it does not optimise "through retraining, calibration, language identification, translation-based preprocessing" (§VII). [FACT]

## Languages

- **Bengali: no.** [FACT; full read]
- **Romanized: yes, implicitly.** The code-mix views include "romanized forms" (§III-B), and the examples are romanized Tamil (Table IV). Romanized is **not a separate, controlled condition** from code-mixed. [FACT]
- **Native script:** Tamil-only view. The script is not specified (§III-B).
- **Code-mixed: yes**, Tamil–English, automatically generated.

## Metrics

HFA = Pr[ALLOW | hate]; NFF = Pr[FLAG | non-hate]; RR = Pr[REVIEW]; the paired decision flip rate with 95% bootstrap CIs; McNemar tests on HFA, NFF and RR (§III-C, §V-B).

## Key findings (with locations)

1. **Fixed English-dev thresholds plus code-mix lead to action instability.** The flip rate is 0.265 (Abstract, §I, Table V) or **0.266, 95% CI [0.251, 0.281]** (Table II). [FACT: the paper reports both values, a small internal inconsistency.] Clean→Tamil flip is 0.557 [0.539, 0.573] (Table II).
2. **Errors are redistributed, not uniformly increased** (Table I, §V-A). Clean → code-mix: RR 0.138 → 0.297; NFF 0.069 → 0.104; HFA 0.040 → **0.011** (hate false-accept *decreases*). Tamil: RR 0.637, HFA 0.009, NFF 0.060.
3. **McNemar:** significant for clean vs code-mix on HFA, NFF and RR; significant for clean vs Tamil on HFA and RR; not significant for Tamil NFF (§V-B). The paper reports no p-values and no multiple-comparison correction. [FACT]
4. **Label-conditioned asymmetry** (Table III): non-hate clean ALLOW → code-mix REVIEW 0.339; hate clean ALLOW → REVIEW 0.793 and → FLAG 0.121. In other words, code-mix makes the detector more conservative.
5. **Mitigation trade-off** (Table I): code-mix + disagreement gives HFA 0.003, NFF 0.046, RR 0.355. Code-mix + confidence gives HFA 0.016, NFF 0.032, RR 0.417.
6. **The effect depends on the detector** (Table V): MetaHateBERT flip 0.608 with code-mix NFF 0.436; HateBERT zero-shot routes 100% to REVIEW (RR 1.000, flip 0.000).

### Verbatim quotes

- "Under thresholds tuned on clean English development data, code-mixed inputs produce substantial action instability, with a paired clean-to-code-mix decision flip rate of 0.265." (Abstract)
- "The selected thresholds are tuned on clean English development data only, then frozen and reused for clean, code-mixed, and Tamil test evaluations." (§III-D)
- "This ensures that any downstream change reflects robustness differences rather than threshold adaptation to the test setting." (§IV-B)
- "The main effect in the current setup is therefore not a uniform rise in all automatic errors, but a redistribution of actions toward review and, for code-mix, increased false-flagging of non-hateful content." (§V-A)
- "Tamil-only degradation is stronger overall, suggesting a broader language-coverage limitation rather than the same workflow phenomenon as code-mixed instability." (§I)
- "Because we use a single generation pipeline, the results should be interpreted as specific to this construction process rather than universal across all code-mixed text." (§III-B)
- "We evaluate robustness under a fixed pipeline rather than optimizing multilingual performance through retraining, calibration, language identification, translation-based preprocessing, or stronger multilingual baselines." (§VII)

## Limitations

**Stated by the authors (§VII):** a single Tamil–English setting; automatically generated code-mix that was only partly validated; about 25% filtered out, so hard cases may be under-represented; the disagreement rule assumes paired views exist and is not costed; no subgroup or fairness analysis; no calibrated-confidence baselines and no modern multilingual backbones.

**Additional (my reading) [INFERENCE]:**
- Small fine-tuned encoders only, not LLMs, and there is no generation.
- The task is classification. There is no evidence, retrieval or sufficiency notion.
- Comprehension and calibration are not separated, so a flip could come from misunderstanding the text or from a shifted score.
- The paper does not report realised-versus-target risk on test as a calibration-transfer test.
- No CIs for the HFA/NFF/RR deltas beyond the flip rate. McNemar p-values are omitted.
- The Tamil-only script is unspecified.
- The validation protocol is underspecified (who validated, the numbers do not reconcile, no agreement statistic).
- The flip rate is reported as both 0.265 and 0.266.
- Single run, with no seeds reported.

## How our work differs

1. **Task:** RAG question answering with abstention under **controlled sufficient/insufficient oracle evidence**, versus hate-speech classification routing. Our "risk" is answering when evidence is insufficient, or answering wrongly. Theirs is label-cost errors.
2. **Models:** generative multilingual instruct LLMs (~7–9B) with prompted abstention and a sufficiency autorater, versus fine-tuned mBERT and zero-shot BERT classifiers.
3. **Variants:** BN native script, RBN romanized and CM code-mixed as **three separate controlled conditions**, so script and code-mixing effects can be told apart. They have a single code-mix view that already mixes romanization with code-mixing, plus a Tamil-only diagnostic. Our variants are human-edited by a native speaker with a second-annotator agreement check (plan); theirs are automatically generated and partly filtered.
4. **Language:** Bengali (they have none) versus Tamil.
5. **RQ2 framing:** we test whether a threshold chosen for target risk *r* on EN-dev achieves **realised risk ≈ r** on each test variant (risk-control transfer). They report shifts in action distribution and flip rates, but never compare realised and target budgets on test.
6. **RQ3:** we separate comprehension failure from calibration failure. They do not; their English-versus-Tamil-only contrast is a coarse proxy that they describe only in words.
7. **RQ4 mitigations:** per-variant thresholds, transliteration to BN before the sufficiency check, and pivot-language sufficiency judgment. They evaluate only cross-view disagreement deferral and English-tuned confidence abstention. They explicitly do **not** evaluate per-variant recalibration or transliteration/translation preprocessing (§III-F, §VII).

## What we must concede / cite

- **Concede [FACT]:** prior work already shows empirically that **thresholds or operating points tuned on clean English dev and frozen produce materially different decisions and error rates on paired, meaning-preserving code-mixed (partly romanized) inputs.** This holds for a Tamil–English classification pipeline with a risk-budget operating criterion and deferral (§III-D, §IV-B, Tables I–II). We **cannot** claim to be the first to show that English-tuned abstention or deferral thresholds fail to transfer to paired code-mixed input in general.
- **Concede:** paired-view designs measuring decision flips (with bootstrap CIs and McNemar tests) have been used for code-mix robustness of abstention/deferral pipelines. We should cite this as precedent for our paired design and our flip/instability metrics.
- **Also note:** their direction of failure (more conservative behaviour, with higher review and false-flag rates and lower false-accept) parallels our H1-alt (over-abstention). It is worth citing whichever direction we observe.
- **What remains ours (narrowed RQ2) [REC]:** transfer of an EN-dev-selected abstention/sufficiency threshold **for generative RAG QA under controlled evidence sufficiency**, evaluated as **realised-versus-target risk**, **separately for native script, romanized and code-mixed** Bengali, with comprehension controlled (RQ3) and per-variant / transliteration / pivot mitigations (RQ4).
- **Recommended wording [REC]:** "Prior work shows that decision thresholds tuned on clean English shift moderation actions on paired Tamil–English code-mixed inputs (Thimma Krishnaram et al., 2026). To our knowledge, the transfer of an English-calibrated abstention threshold to a target risk level has not been examined for retrieval-augmented QA under controlled evidence sufficiency. Nor has it been examined with native-script, romanized and code-mixed variants kept separate, or for Bengali."
- **Threat level for RQ2:** **moderate.** The core phenomenon (English-tuned thresholds fail to transfer to paired code-mix) is now established in a neighbouring task. This removes any generic novelty claim, but the RAG-sufficiency, risk-control, script-separation, comprehension-controlled and Bengali aspects are untouched. This assessment reflects only this paper; other works have not been checked here.
- **Gaps in this read:** v1 not compared; figures read only as captions; repo notebooks not inspected (so the code-mix generator model is unconfirmed); CodeMixBench not read.

---
**Quote verification (lead, 2026-10-23):** verbatim quotes string-matched against the arXiv PDF text (pypdf); unmatched strings were checked by hand and were PDF-extraction artefacts (footnote/table markers inside sentences), labels/paraphrases, or quotes from the GitHub README rather than the paper. Status: full-read.
