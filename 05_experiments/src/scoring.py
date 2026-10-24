"""Metrics, item-level bootstrap and target-risk threshold selection.

Row schema (one model response): item_id, variant, sufficiency ('suff'|'insuff'),
answered (bool), correct (bool; only meaningful when answered and sufficient),
and optionally score (float; higher = more willing to answer).

Definitions (research_plan.md §5.5):
  UAR  = P(answered | insufficient)
  UNR  = P(abstained | sufficient)
  selective accuracy = P(correct | answered, sufficient)
  coverage = P(answered)
Risk for selective generation (RQ2) = P(error | answered), where an answer on an
insufficient item is an error and an answer on a sufficient item is an error
unless it is correct.
"""
import numpy as np
import pandas as pd


def _rate(mask_num, mask_den):
    den = mask_den.sum()
    return float(mask_num[mask_den].mean()) if den else float("nan")


def metrics(df: pd.DataFrame) -> dict:
    ins = df["sufficiency"].eq("insuff").to_numpy()
    suf = ~ins
    ans = df["answered"].to_numpy(bool)
    cor = df["correct"].fillna(False).to_numpy(bool)
    return {
        "n": int(len(df)),
        "UAR": _rate(ans, ins),
        "UNR": _rate(~ans, suf),
        "sel_acc": _rate(cor, suf & ans),
        "coverage": float(ans.mean()) if len(df) else float("nan"),
        "risk": risk(df),
    }


def is_error(df: pd.DataFrame) -> np.ndarray:
    """Error indicator for answered rows (False for abstentions)."""
    ans = df["answered"].to_numpy(bool)
    ins = df["sufficiency"].eq("insuff").to_numpy()
    cor = df["correct"].fillna(False).to_numpy(bool)
    return ans & (ins | ~cor)


def risk(df: pd.DataFrame) -> float:
    ans = df["answered"].to_numpy(bool)
    return float(is_error(df)[ans].mean()) if ans.any() else float("nan")


def bootstrap(df: pd.DataFrame, stat, n_boot: int = 2000, seed: int = 0, alpha: float = 0.05):
    """Percentile CI by resampling base items (all rows of an item move together)."""
    rng = np.random.default_rng(seed)
    groups = {k: g for k, g in df.groupby("item_id")}
    keys = np.array(list(groups))
    vals = []
    for _ in range(n_boot):
        sample = rng.choice(keys, size=len(keys), replace=True)
        v = stat(pd.concat([groups[k] for k in sample], ignore_index=True))
        if not np.isnan(v):
            vals.append(v)
    point = stat(df)
    if not vals:
        return point, float("nan"), float("nan")
    lo, hi = np.quantile(vals, [alpha / 2, 1 - alpha / 2])
    return point, float(lo), float(hi)


def paired_diff(df: pd.DataFrame, a: str, b: str, metric: str, **kw):
    """Bootstrap CI for metric(variant a) - metric(variant b), paired over items."""
    def stat(d):
        return metrics(d[d.variant == a])[metric] - metrics(d[d.variant == b])[metric]
    return bootstrap(df[df.variant.isin([a, b])], stat, **kw)


def apply_threshold(df: pd.DataFrame, tau: float) -> pd.DataFrame:
    """Selective generation: answer iff score >= tau (and the base model answered)."""
    out = df.copy()
    out["answered"] = out["answered"].astype(bool) & (out["score"] >= tau)
    return out


def select_threshold(df: pd.DataFrame, target_risk: float) -> float:
    """Smallest threshold whose empirical risk on df is <= target_risk.

    Picks the threshold giving the highest coverage subject to the risk
    constraint. Returns +inf (abstain on everything) if no threshold qualifies.
    """
    for tau in np.sort(df["score"].unique()):
        r = risk(apply_threshold(df, tau))
        if not np.isnan(r) and r <= target_risk:
            return float(tau)
    return float("inf")


def transfer_table(dev_en: pd.DataFrame, test: pd.DataFrame, target_risk: float) -> pd.DataFrame:
    """RQ2: threshold chosen on EN-dev, realised risk/coverage per variant on test."""
    tau = select_threshold(dev_en, target_risk)
    rows = []
    for v, g in test.groupby("variant"):
        m = metrics(apply_threshold(g, tau))
        rows.append({"variant": v, "tau": tau, "target_risk": target_risk,
                     "realised_risk": m["risk"], "coverage": m["coverage"],
                     "violation": m["risk"] - target_risk})
    return pd.DataFrame(rows)


def fit_combiner(X: np.ndarray, y: np.ndarray, l2: float = 1.0, iters: int = 500, lr: float = 0.5):
    """L2-regularised logistic regression by gradient descent (deterministic, no tuning).

    Features are standardised with the fitting data's mean/sd; returns a scorer
    f(X) -> P(answer is correct), used as the M3 selective-generation score.
    """
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    Z = np.c_[np.ones(len(X)), (X - mu) / sd]
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        grad = Z.T @ (p - y) / len(y) + l2 * np.r_[0, w[1:]] / len(y)
        w -= lr * grad

    def score(Xn):
        Zn = np.c_[np.ones(len(Xn)), (np.asarray(Xn, float) - mu) / sd]
        return 1 / (1 + np.exp(-Zn @ w))
    score.weights = w
    return score
