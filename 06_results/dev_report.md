# Phase 4c Dev Report (descriptive; not confirmatory)

Date: 2026-10-30. Runs: `20261027_dev_qwen35_9b`, `20261027_dev_gemma2_9b` (50 dev items, 2,900 calls each). Ambiguous M1/GEN responses: 37, all adjudicated by the author (`06_results/adjudication_dev.csv`); 0 unresolved.

## Calibration frozen for test [RESULT]
Files: `06_results/calibration/Qwen_Qwen3.5-9B-GGUF.json`, `06_results/calibration/gemma-2-9b-it-GGUF.json` (committed before any test run). M3 combiner fitted on EN-dev main rows (100 rows, 50 items per model); τ selected on EN-dev.

| | Qwen | Gemma |
|---|---|---|
| M3 weights [bias, P(suff), conf] (standardised) | −0.926, 3.072, 1.084 | −0.494, 1.382, 1.866 |
| τ at r = 0.10 (confirmatory) | 0.1004 | 0.1109 |

## Sanity check vs Joren et al. (protocol §9.6), EN-dev [RESULT]
| | Qwen | Gemma |
|---|---|---|
| GEN answers on insufficient context (UAR) | 16% | 24% |
| GEN risk | 17.2% | 21.0% |
| M3 at r = 0.10: risk / coverage | 9.4% / 53% | 9.4% / 53% |
| Selective accuracy GEN → M3 | 96% → 96% | 98% → 98% |

**Partial match.** As in Joren et al., the model without an abstention option answers on some insufficient contexts, and selective generation lowers risk. Two differences: the rates of answering on insufficient context are lower than the high rates Joren et al. report for their settings, and the risk reduction here comes from abstaining on insufficient items, not from higher accuracy on sufficient ones (already 96–98%). EN-dev risk at r = 0.10 is in-sample by design (τ is chosen on the same rows). [ASSUMPTION] The difference in rates likely reflects our short, single-fact notices; this is a qualitative comparison only.

## Dev pattern (n = 50; descriptive, CIs overlap; no claims)
Tables: `06_results/tables/20261027_dev_*_per_variant.csv`.
- M1 UAR, Qwen: EN 4%, BN 4%, RBN 12%, CM 2%, CMR 10%. Gemma: EN 2%, BN 0%, RBN 10%, CM 0%, CMR 4%.
- M1 UNR, Gemma: EN 4%, RBN 14%, CMR 10% (over-abstention in Roman script, as in the pilot). Qwen UNR ≤ 2% everywhere.
- GEN UAR, Qwen: EN 16%, RBN 26%, CMR 24%.
Direction is consistent with the pilot (Roman-script variants answer more on insufficient evidence; Gemma also abstains more on sufficient RBN). Not evidence; test is confirmatory.

## Test-run time [RESULT, measured on dev main items]
Mean latency on long main-item prompts: Qwen 3.50 s/call, Gemma 11.67 s/call. Test = 148 items × 58 calls = 8,584 calls per model → about 8.4 h (Qwen) + 27.8 h (Gemma) ≈ 36 h. Cost US$0 (local).
