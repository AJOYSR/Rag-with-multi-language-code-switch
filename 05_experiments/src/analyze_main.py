"""Main analysis, exactly as frozen in protocol v1.0 §7, §8, §10.

Usage:
  python -m src.analyze_main calibrate runs/<dev_run>            (dev only; writes 06_results/calibration/<model>.json)
  python -m src.analyze_main confirm runs/<test_run> [runs/<test_run> ...]

`calibrate` fits the M3 combiner on EN-dev and selects thresholds; its output is committed
before any test run, so nothing chosen on test feeds back. `confirm` loads that file and runs
the confirmatory families A (RQ1) and B (RQ2) with Holm correction, the closed-book exclusions
(with an all-items sensitivity analysis) and the secondary BN/CM contrasts.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest
from statsmodels.stats.multitest import multipletests

from .analyze_pilot import VARIANT_ORDER, load_run, outcome_frame, per_variant
from .scoring import bootstrap, combiner, fit_combiner, metrics, paired_diff, select_threshold, apply_threshold

ROOT = Path(__file__).resolve().parents[2]
CAL_DIR = ROOT / "06_results" / "calibration"
TABLES = ROOT / "06_results" / "tables"
R_CONFIRM = 0.10
R_ALL = (0.05, 0.10, 0.20)
N_BOOT = 2000


def _run_dir(p) -> Path:
    p = Path(p)
    return p if p.is_absolute() else ROOT / "05_experiments" / p


def model_tag(meta: dict) -> str:
    return meta["model"]["name"].split("/")[-1].split(":")[0]


def selective_frame(df: pd.DataFrame) -> pd.DataFrame:
    """GEN answers on main rows with P(suff) and answer confidence (inputs to M3 and M2b)."""
    gen = outcome_frame(df, "GEN").merge(
        df[(df.method == "GEN") & (df.question == "main")][["item_id", "variant", "sufficiency", "conf"]],
        on=["item_id", "variant", "sufficiency"], how="left")
    suff = df[(df.method == "SUFF") & (df.question == "main")][["item_id", "variant", "sufficiency", "p_suff"]]
    return gen.merge(suff, on=["item_id", "variant", "sufficiency"], how="left")


def calibrate(run):
    rd = _run_dir(run)
    meta = json.loads((rd / "meta.json").read_text())
    if meta["config"].get("split") != "dev":
        sys.exit("refusing: calibrate uses dev runs only")
    df = load_run(rd)
    sel = selective_frame(df).dropna(subset=["p_suff", "conf"])
    en = sel[sel.variant == "en"]
    target = ((en.sufficiency == "suff") & en.correct).to_numpy()
    f = fit_combiner(en[["p_suff", "conf"]].to_numpy(), target)
    out = {"dev_run": rd.name, "model": meta["model"]["name"], "digest": meta["model"].get("digest"),
           "git_commit_of_run": meta["git_commit"], "n_en_dev_rows": int(len(en)),
           "n_en_dev_items": int(en.item_id.nunique()),
           "M3": {"features": ["p_suff", "conf"], "weights": f.weights.tolist(), "mu": f.mu.tolist(), "sd": f.sd.tolist(),
                  "tau": {}},
           "M2b": {"tau": {}}}
    en_m3 = en.assign(score=f(en[["p_suff", "conf"]].to_numpy()))
    en_m2b = en.assign(score=en["conf"])
    for r in R_ALL:
        out["M3"]["tau"][str(r)] = select_threshold(en_m3, r)
        out["M2b"]["tau"][str(r)] = select_threshold(en_m2b, r)
    # Sanity check (protocol §9.6), on EN-dev: GEN answers on insufficient context; M3 at r=0.10 vs GEN.
    gen_m = metrics(en)
    m3_m = metrics(apply_threshold(en_m3, out["M3"]["tau"][str(R_CONFIRM)]))
    out["sanity_EN_dev"] = {"GEN_UAR": gen_m["UAR"], "GEN_sel_acc": gen_m["sel_acc"], "GEN_risk": gen_m["risk"],
                            "M3_r0.10_risk": m3_m["risk"], "M3_r0.10_coverage": m3_m["coverage"],
                            "M3_r0.10_sel_acc": m3_m["sel_acc"]}
    out["rows_missing_scores"] = int(selective_frame(df)[["p_suff", "conf"]].isna().any(axis=1).sum())
    CAL_DIR.mkdir(parents=True, exist_ok=True)
    path = CAL_DIR / f"{model_tag(meta)}.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    # descriptive dev tables (not confirmatory)
    TABLES.mkdir(parents=True, exist_ok=True)
    m1 = outcome_frame(df, "M1")
    per_variant(m1, N_BOOT).to_csv(TABLES / f"{rd.name}_M1_per_variant.csv", index=False)
    per_variant(sel, N_BOOT).to_csv(TABLES / f"{rd.name}_GEN_per_variant.csv", index=False)
    print(f"-> {path}")


def cb_excluded(df: pd.DataFrame) -> set:
    """Protocol §10: items excluded from this model's UAR analysis for closed-book contamination."""
    cb = df[(df.method == "CB") & (df.question == "main")]
    out = set()
    for iid, g in cb.groupby("item_id"):
        n_ok = int(g["correct"].sum())
        if (g.answer_type.iloc[0] == "yesno" and n_ok >= 4) or (g.answer_type.iloc[0] != "yesno" and n_ok >= 1):
            out.add(iid)
    return out


def mcnemar(d: pd.DataFrame, a: str, b: str, metric: str) -> dict:
    """Exact McNemar on item-paired binary outcomes (UAR: answered on insufficient; UNR: not answered on sufficient)."""
    s = d[d.sufficiency == ("insuff" if metric == "UAR" else "suff")]
    w = s.pivot_table(index="item_id", columns="variant", values="answered", aggfunc="first").dropna(subset=[a, b])
    x = w.astype(bool) if metric == "UAR" else ~w.astype(bool)
    n10, n01 = int((x[a] & ~x[b]).sum()), int((~x[a] & x[b]).sum())
    p = binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1.0
    pt, lo, hi = paired_diff(d[d.item_id.isin(w.index)], a, b, metric, n_boot=N_BOOT)
    return {"n_items": int(len(w)), "n10": n10, "n01": n01, "diff": pt, "lo": lo, "hi": hi, "p": p}


def risk_test(g: pd.DataFrame, r: float) -> dict:
    """Family B: one-sided item-bootstrap p = share of resamples with realised risk <= r (resamples with no answers dropped)."""
    rng = np.random.default_rng(0)
    groups = {k: x for k, x in g.groupby("item_id")}
    keys = np.array(list(groups))
    vals = []
    for _ in range(N_BOOT):
        v = metrics(pd.concat([groups[k] for k in rng.choice(keys, len(keys))], ignore_index=True))["risk"]
        if not np.isnan(v):
            vals.append(v)
    m = metrics(g)
    vals = np.array(vals)
    return {"realised_risk": m["risk"], "coverage": m["coverage"], "violation": m["risk"] - r,
            "risk_lo": float(np.quantile(vals, .025)) if len(vals) else float("nan"),
            "risk_hi": float(np.quantile(vals, .975)) if len(vals) else float("nan"),
            "p": float((vals <= r).mean()) if len(vals) else float("nan"), "n_boot_used": int(len(vals))}


def confirm(*runs):
    fam_a, fam_b, secondary, excl_rows, sens = [], [], [], [], []
    for run in runs:
        rd = _run_dir(run)
        meta = json.loads((rd / "meta.json").read_text())
        if meta["config"].get("split") != "test":
            sys.exit(f"refusing: {rd.name} is not a test run")
        tag = model_tag(meta)
        cal = json.loads((CAL_DIR / f"{tag}.json").read_text())
        if cal["digest"] != meta["model"].get("digest"):
            sys.exit(f"refusing: model digest differs between dev calibration and {rd.name}")
        df = load_run(rd)
        excl = cb_excluded(df)
        excl_rows.append({"model": tag, "n_items": df.item_id.nunique(), "n_cb_excluded": len(excl),
                          "excluded": " ".join(sorted(excl))})
        m1 = outcome_frame(df, "M1")
        m1_uar = m1[~m1.item_id.isin(excl)]
        for v in ("rbn", "cmr", "bn", "cm"):
            for metric in ("UAR", "UNR"):
                d = m1_uar if metric == "UAR" else m1
                row = {"model": tag, "contrast": f"{v}-en", "metric": metric, **mcnemar(d, v, "en", metric)}
                (fam_a if v in ("rbn", "cmr") else secondary).append(row)
                if metric == "UAR":
                    sens.append({"model": tag, "contrast": f"{v}-en", "metric": "UAR (all items, sensitivity)",
                                 **mcnemar(m1, v, "en", "UAR")})
        sel = selective_frame(df).dropna(subset=["p_suff", "conf"])
        f = combiner(cal["M3"]["weights"], cal["M3"]["mu"], cal["M3"]["sd"])
        sel["score"] = f(sel[["p_suff", "conf"]].to_numpy())
        tau = cal["M3"]["tau"][str(R_CONFIRM)]
        thr = apply_threshold(sel, tau)
        en = risk_test(thr[thr.variant == "en"], R_CONFIRM)
        for v in ("bn", "rbn", "cm", "cmr"):
            row = {"model": tag, "variant": v, "tau": tau, "r": R_CONFIRM, **risk_test(thr[thr.variant == v], R_CONFIRM),
                   "en_realised_risk": en["realised_risk"]}
            pt, lo, hi = bootstrap(thr[thr.variant.isin([v, "en"])],
                                   lambda x, v=v: metrics(x[x.variant == v])["risk"] - metrics(x[x.variant == "en"])["risk"],
                                   n_boot=N_BOOT)
            row.update({"risk_minus_en": pt, "risk_minus_en_lo": lo, "risk_minus_en_hi": hi})
            fam_b.append(row)
        for name, t in (("M1", per_variant(m1, N_BOOT)), ("GEN", per_variant(sel, N_BOOT))):
            t.to_csv(TABLES / f"{rd.name}_{name}_per_variant.csv", index=False)
    TABLES.mkdir(parents=True, exist_ok=True)
    for name, rows in (("familyA_RQ1", fam_a), ("familyB_RQ2", fam_b)):
        t = pd.DataFrame(rows)
        t["p_holm"] = multipletests(t["p"], method="holm")[1]
        t["reject_at_.05"] = t["p_holm"] < 0.05
        t.to_csv(TABLES / f"main_{name}.csv", index=False)
        print(f"\n-- {name} (Holm within family, {len(t)} tests)\n{t.round(4).to_string(index=False)}")
    for name, rows in (("secondary_BN_CM", secondary), ("sensitivity_all_items", sens), ("cb_exclusions", excl_rows)):
        t = pd.DataFrame(rows)
        t.to_csv(TABLES / f"main_{name}.csv", index=False)
        print(f"\n-- {name}\n{t.round(4).to_string(index=False)}")


if __name__ == "__main__":
    {"calibrate": calibrate, "confirm": confirm}[sys.argv[1]](*sys.argv[2:])
