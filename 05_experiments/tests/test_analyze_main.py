import numpy as np
import pandas as pd

from src.analyze_main import cb_excluded, mcnemar, risk_test
from src.scoring import combiner, fit_combiner


def _m1(answers_en, answers_v, suff="insuff"):
    rows = []
    for i, (a, b) in enumerate(zip(answers_en, answers_v)):
        rows += [{"item_id": f"I{i}", "variant": "en", "sufficiency": suff, "answered": a, "correct": False},
                 {"item_id": f"I{i}", "variant": "rbn", "sufficiency": suff, "answered": b, "correct": False}]
    return pd.DataFrame(rows)


def test_mcnemar_counts_and_exact_p():
    # 6 items answered only in rbn, 1 only in en, 3 concordant
    d = _m1([False] * 6 + [True] + [False] * 3, [True] * 6 + [False] + [False] * 3)
    r = mcnemar(d, "rbn", "en", "UAR")
    assert (r["n10"], r["n01"], r["n_items"]) == (6, 1, 10)
    assert abs(r["p"] - 0.125) < 1e-9          # exact binomial, 7 discordant, two-sided
    assert abs(r["diff"] - 0.5) < 1e-9


def test_mcnemar_unr_uses_non_answers():
    d = _m1([True] * 4, [False, False, True, True], suff="suff")
    r = mcnemar(d, "rbn", "en", "UNR")
    assert (r["n10"], r["n01"]) == (2, 0)


def test_cb_exclusion_rules():
    rows = []
    for iid, t, ok in (("A", "amount", [0, 0, 1, 0, 0]), ("B", "amount", [0] * 5),
                       ("Y", "yesno", [1, 1, 1, 0, 0]), ("Z", "yesno", [1, 1, 1, 1, 0])):
        for v, c in zip(("en", "bn", "rbn", "cm", "cmr"), ok):
            rows.append({"method": "CB", "question": "main", "item_id": iid, "answer_type": t, "variant": v, "correct": bool(c)})
    assert cb_excluded(pd.DataFrame(rows)) == {"A", "Z"}


def test_risk_test_all_correct_has_zero_risk():
    g = pd.DataFrame([{"item_id": f"I{i}", "variant": "bn", "sufficiency": "suff", "answered": True, "correct": True}
                      for i in range(20)])
    r = risk_test(g, 0.10)
    assert r["realised_risk"] == 0.0 and r["p"] == 1.0


def test_combiner_roundtrip():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(50, 2))
    y = X[:, 0] > 0
    f = fit_combiner(X, y)
    g = combiner(f.weights, f.mu, f.sd)
    assert np.allclose(f(X), g(X))
