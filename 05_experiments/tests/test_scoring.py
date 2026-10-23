import math

import pandas as pd

from src.scoring import apply_threshold, bootstrap, metrics, risk, select_threshold, transfer_table


def frame(rows):
    return pd.DataFrame(rows, columns=["item_id", "variant", "sufficiency", "answered", "correct", "score"])


# 4 items x (suff, insuff), one variant. Hand-computed:
#   insuff answered: i1, i2 -> UAR = 2/4
#   suff abstained:  i4     -> UNR = 1/4
#   suff answered: i1 ok, i2 ok, i3 wrong -> sel_acc = 2/3
#   coverage = 5/8; errors among answered = i3-suff + i1-insuff + i2-insuff = 3 -> risk 3/5
TOY = frame([
    ("i1", "EN", "suff", True, True, 0.9), ("i1", "EN", "insuff", True, False, 0.6),
    ("i2", "EN", "suff", True, True, 0.8), ("i2", "EN", "insuff", True, False, 0.3),
    ("i3", "EN", "suff", True, False, 0.7), ("i3", "EN", "insuff", False, False, 0.2),
    ("i4", "EN", "suff", False, False, 0.5), ("i4", "EN", "insuff", False, False, 0.1),
])


def test_metrics_hand_computed():
    m = metrics(TOY)
    assert m["UAR"] == 0.5
    assert m["UNR"] == 0.25
    assert math.isclose(m["sel_acc"], 2 / 3)
    assert m["coverage"] == 5 / 8
    assert math.isclose(m["risk"], 3 / 5)


def test_threshold_application():
    # tau = 0.7 keeps answers with score >= .7: i1-suff ok, i2-suff ok, i3-suff wrong -> risk 1/3
    assert math.isclose(risk(apply_threshold(TOY, 0.7)), 1 / 3)
    # tau = 0.8 keeps only correct answers -> risk 0
    assert risk(apply_threshold(TOY, 0.8)) == 0.0


def test_select_threshold_max_coverage_under_target():
    assert select_threshold(TOY, 0.0) == 0.8
    assert select_threshold(TOY, 0.34) == 0.7
    assert select_threshold(TOY, 1.0) == 0.1


def test_select_threshold_infeasible():
    always_wrong = frame([("i1", "EN", "insuff", True, False, 0.9)])
    assert select_threshold(always_wrong, 0.1) == float("inf")


def test_bootstrap_constant_stat_has_zero_width():
    pt, lo, hi = bootstrap(TOY, lambda d: 1.0, n_boot=50)
    assert pt == lo == hi == 1.0


def test_bootstrap_resamples_items_not_rows():
    # every item has exactly 2 rows, so any resample must have an even row count
    sizes = []
    bootstrap(TOY, lambda d: sizes.append(len(d)) or 0.0, n_boot=30)
    assert all(s % 2 == 0 for s in sizes)


def test_transfer_table_reports_violation():
    test = pd.concat([TOY.assign(variant="EN"),
                      TOY.assign(variant="RBN", correct=False)])  # RBN never correct
    t = transfer_table(TOY, test, target_risk=0.0).set_index("variant")
    assert t.loc["EN", "realised_risk"] == 0.0
    assert t.loc["RBN", "realised_risk"] == 1.0
    assert t.loc["RBN", "violation"] == 1.0


def test_first_token_binary_prob():
    import math
    from src.llm import first_token_binary_prob, mean_logprob
    lp = [{"token": "1", "logprob": math.log(0.6), "top_logprobs": [
        {"token": "1", "logprob": math.log(0.6)}, {"token": "0", "logprob": math.log(0.2)},
        {"token": " 1", "logprob": math.log(0.1)}, {"token": "x", "logprob": math.log(0.1)}]}]
    assert math.isclose(first_token_binary_prob(lp), 0.7 / 0.9)
    assert math.isnan(first_token_binary_prob([]))
    assert math.isclose(mean_logprob([{"logprob": -1.0}, {"logprob": -3.0}]), -2.0)
