"""Score a pilot run and write tables.

Usage: python -m src.analyze_pilot runs/<run_id> [more run dirs...]
Writes 06_results/tables/<run_id>_*.csv and prints a summary. Every number in the
G2 report must come from these files.

Pilot items are dev-only, so the threshold-transfer table here is EXPLORATORY:
the EN threshold is selected and evaluated on the same 30 items (in-sample for EN).
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from .llm import first_token_binary_prob, mean_logprob
from .normalize import is_abstention, match, outcome
from .scoring import bootstrap, fit_combiner, metrics, paired_diff, transfer_table

ROOT = Path(__file__).resolve().parents[2]
VARIANT_ORDER = ["en", "bn", "rbn", "cm", "cmr"]


def load_run(run_dir: Path) -> pd.DataFrame:
    recs = [json.loads(l) for l in (run_dir / "responses.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(recs)
    df["category"] = [outcome(c, t) for c, t in zip(df["content"], df["answer_type"])]
    # manual adjudication of 'ambiguous' cases (plan §5.5), keyed by run + response key
    adj_path = ROOT / "06_results" / "adjudication_pilot.csv"
    adj = pd.read_csv(adj_path) if adj_path.exists() else pd.DataFrame(columns=["run_id", "key", "label"])
    adj = adj[adj.run_id == run_dir.name].set_index("key")["label"].to_dict()
    df["adjudicated"] = df["key"].map(adj)
    df.loc[df.adjudicated.notna(), "category"] = df.loc[df.adjudicated.notna(), "adjudicated"].map(
        lambda x: "specific" if x.startswith("specific") else x)
    df["abstained"] = df["category"] != "specific"          # strict: only committed values count as answers
    df["explicit_abstain"] = df["category"] == "abstain"
    df["correct"] = [(not a) and (match(c, t, g) if not isinstance(j, str) else
                                  (j == "specific_yes") == bool(g.get("value")) if t == "yesno" else False)
                     for c, t, g, a, j in zip(df["content"], df["answer_type"], df["gold"], df["abstained"], df["adjudicated"])]
    unresolved = df[(df.category == "ambiguous") & df.method.isin(["M1", "GEN"])]
    if len(unresolved):
        print(f"WARNING {run_dir.name}: {len(unresolved)} unadjudicated ambiguous rows (treated as non-answers)")
    df["p_suff"] = df["logprobs"].map(first_token_binary_prob)
    df["conf"] = df["logprobs"].map(mean_logprob)
    return df


def outcome_frame(df: pd.DataFrame, method: str, question: str = "main") -> pd.DataFrame:
    d = df[(df.method == method) & (df.question == question)].copy()
    d["answered"] = ~d["abstained"]
    if question == "main":  # the sibling question stays answerable on the insufficient passage
        d.loc[d.sufficiency == "insuff", "correct"] = False
    return d[["item_id", "variant", "sufficiency", "answered", "correct", "answer_type", "category"]]


def m3_frame(df: pd.DataFrame) -> pd.DataFrame:
    """GEN answers + sufficiency P("1") + answer confidence; score = combiner fitted on EN only."""
    gen = outcome_frame(df, "GEN").merge(
        df[(df.method == "GEN") & (df.question == "main")][["item_id", "variant", "sufficiency", "conf"]],
        on=["item_id", "variant", "sufficiency"], how="left")
    suff = df[(df.method == "SUFF") & (df.question == "main")][["item_id", "variant", "sufficiency", "p_suff"]]
    out = gen.merge(suff, on=["item_id", "variant", "sufficiency"], how="left").dropna(subset=["p_suff", "conf"])
    en = out[out.variant == "en"]
    target = (en.sufficiency == "suff") & en.correct          # answering would be correct
    f = fit_combiner(en[["p_suff", "conf"]].to_numpy(), target.to_numpy())
    out["score"] = f(out[["p_suff", "conf"]].to_numpy())
    out.attrs["combiner_weights"] = f.weights.tolist()
    return out


def per_variant(d: pd.DataFrame, n_boot: int) -> pd.DataFrame:
    rows = []
    for v in [x for x in VARIANT_ORDER if x in set(d.variant)]:
        g = d[d.variant == v]
        row = {"variant": v, "n_items": g.item_id.nunique()}
        for m in ("UAR", "UNR", "sel_acc", "coverage"):
            pt, lo, hi = bootstrap(g, lambda x, m=m: metrics(x)[m], n_boot=n_boot)
            row.update({m: pt, f"{m}_lo": lo, f"{m}_hi": hi})
        rows.append(row)
    return pd.DataFrame(rows)


def paired(d: pd.DataFrame, n_boot: int) -> pd.DataFrame:
    rows = []
    for ref in ("en", "bn"):
        for v in VARIANT_ORDER:
            if v == ref or v not in set(d.variant):
                continue
            for m in ("UAR", "UNR"):
                pt, lo, hi = paired_diff(d, v, ref, m, n_boot=n_boot)
                rows.append({"comparison": f"{v}-{ref}", "metric": m, "diff": pt, "lo": lo, "hi": hi})
    return pd.DataFrame(rows)


def mcnemar_power(d: pd.DataFrame, a: str, b: str, metric: str = "UAR", alpha: float = 0.05,
                  power: float = 0.8, n_planned: int = 130) -> dict:
    """Paired-proportion power (Connor 1987) from pilot discordance.

    For UAR, pairs are (item, variant a) vs (item, variant b) on insufficient main rows.
    """
    sel = d[d.sufficiency == ("insuff" if metric == "UAR" else "suff")]
    col = "answered" if metric == "UAR" else "abstained_flag"
    if metric == "UNR":
        sel = sel.assign(abstained_flag=~sel["answered"])
    w = sel.pivot_table(index="item_id", columns="variant", values=col, aggfunc="first").dropna(subset=[a, b])
    n = len(w)
    p10 = float(((w[a] == True) & (w[b] == False)).mean()) if n else float("nan")
    p01 = float(((w[a] == False) & (w[b] == True)).mean()) if n else float("nan")
    pd_, delta = p10 + p01, p10 - p01
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    if delta == 0 or pd_ == 0 or math.isnan(pd_):
        n_req = float("inf")
    else:
        n_req = (za * math.sqrt(pd_) + zb * math.sqrt(max(pd_ - delta ** 2, 1e-12))) ** 2 / delta ** 2
    # minimum detectable |delta| at n_planned with the observed discordance (approximation)
    mde = (za + zb) * math.sqrt(pd_ / n_planned) if pd_ and not math.isnan(pd_) else float("nan")
    return {"comparison": f"{a}-{b}", "metric": metric, "n_pairs": n, "p10": p10, "p01": p01,
            "observed_diff": delta, "n_required_80pct": n_req, "mde_at_n_planned": mde, "n_planned": n_planned}


def main(*run_dirs, n_boot: int = 2000):
    tables = ROOT / "06_results" / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    for rd in map(Path, run_dirs):
        rd = rd if rd.is_absolute() else ROOT / "05_experiments" / rd
        run_id = rd.name
        df = load_run(rd)
        meta = json.loads((rd / "meta.json").read_text())
        print(f"\n=== {run_id} ({meta['model']['name']}, {meta['model']['details'].get('quantization_level')}) ===")
        results = {}
        m1 = outcome_frame(df, "M1")
        if len(m1):
            results["M1_per_variant"] = per_variant(m1, n_boot)
            results["M1_paired"] = paired(m1, n_boot)
            results["M1_power"] = pd.DataFrame([mcnemar_power(m1, v, "en", m) for v in ("bn", "rbn", "cm", "cmr")
                                                for m in ("UAR", "UNR") if v in set(m1.variant)])
            sib = outcome_frame(df, "M1", "sibling")
            results["M1_categories"] = (df[(df.method == "M1") & (df.question == "main")]
                .groupby(["sufficiency", "variant"])["category"].value_counts(normalize=True)
                .unstack(fill_value=0).reset_index())
            results["M1_sibling_nearmiss"] = sib.groupby("variant").agg(
                n=("answered", "size"), answer_rate=("answered", "mean"), acc=("correct", "mean")).reset_index()
        m3 = m3_frame(df)
        if len(m3) and m3["score"].notna().any():
            results["GEN_per_variant"] = per_variant(m3, n_boot)
            results["GEN_categories"] = (df[(df.method == "GEN") & (df.question == "main")]
                .groupby(["sufficiency", "variant"])["category"].value_counts(normalize=True)
                .unstack(fill_value=0).reset_index())
            results["SUFF_rater"] = m3.assign(pred=m3.p_suff >= 0.5, gold=m3.sufficiency == "suff").groupby("variant").apply(
                lambda g: pd.Series({"acc": (g.pred == g.gold).mean(), "mean_p_suff_suff": g[g.gold].p_suff.mean(),
                                     "mean_p_suff_insuff": g[~g.gold].p_suff.mean()}),
                include_groups=False).reset_index()
            print("M3 combiner weights [bias, p_suff, conf] (fitted on EN):", np.round(m3.attrs["combiner_weights"], 3))
            en = m3[m3.variant == "en"]
            results["M3_transfer_EXPLORATORY"] = pd.concat(
                [transfer_table(en, m3.dropna(subset=["score"]), r) for r in (0.05, 0.10, 0.20)], ignore_index=True)
        tr = df[df.method == "TR"]
        if len(tr):
            en_q = df[(df.variant == "en") & (df.question == "main")].drop_duplicates("item_id").set_index("item_id")["query"]
            stop = {"the", "a", "an", "is", "of", "to", "in", "on", "for", "what", "how", "will", "be", "at", "can", "by", "much", "many", "who", "which", "do", "does"}
            def words(x):
                return {w for w in re.findall(r"[a-z]+", x.lower()) if w not in stop}
            t = tr.assign(en_question=tr.item_id.map(en_q), translation=tr.content.str.strip())
            t["overlap"] = [len(words(a) & words(b)) / max(len(words(a)), 1) for a, b in zip(t.en_question, t.translation)]
            t["flag_for_author"] = t.overlap < 0.5
            results["TR_comprehension_PROXY"] = t[["item_id", "variant", "query", "en_question", "translation", "overlap", "flag_for_author"]]
            results["TR_summary_PROXY"] = t.groupby("variant").agg(mean_overlap=("overlap", "mean"), flagged=("flag_for_author", "mean")).reset_index()
        cb = df[df.method == "CB"]
        if len(cb):
            results["CB_contamination"] = cb.groupby(["variant", "answer_type"]).agg(
                n=("correct", "size"), cb_correct=("correct", "mean"), cb_answered=("abstained", lambda s: 1 - s.mean())
            ).reset_index()
        for name, t in results.items():
            t.to_csv(tables / f"{run_id}_{name}.csv", index=False)
            print(f"\n-- {name}\n{t.round(3).to_string(index=False)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
