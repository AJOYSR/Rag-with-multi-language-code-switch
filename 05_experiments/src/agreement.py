"""Second-annotator agreement (protocol v1.0 §6; annotation_guidelines.md).

Usage: python -m src.agreement <annotation_RETURNED.csv> <review_RETURNED.csv> <review_passages_RETURNED.csv> <out.json>
Compares the second annotator (A2) with the author's review decisions:
  meaning      A2 meaning_1to3 >= 2  vs author meaning_equivalent_all = Y (per version)
  naturalness  A2 naturalness_1to3 >= 2  vs author natural = Y (per version)
  insufficiency A2 answer_still_findable = N  vs author insufficient_really_unanswerable = Y (per notice)
Failures (guidelines): any version A2 rates 1 on meaning; any notice A2 marks Y.
Cohen's kappa is undefined (None) when both raters use a single category.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path


def _rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cohen_kappa(a: list, b: list):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / n ** 2
    return po, (None if pe == 1 else (po - pe) / (1 - pe))


def main(ann, review, passages, out):
    a2 = _rows(ann)
    author_q = {(r["item_id"], r["question"]): r for r in _rows(review)}
    author_p = {r["item_id"]: r for r in _rows(passages)}
    pairs = {"meaning": ([], []), "naturalness": ([], []), "insufficiency": ([], [])}
    fails = []
    for r in a2:
        if r["row_type"] == "NOTICE":
            pairs["insufficiency"][0].append(author_p[r["item_id"]]["insufficient_really_unanswerable (Y/N)"].strip().upper() == "Y")
            pairs["insufficiency"][1].append(r["answer_still_findable_Y_N"].strip().upper() == "N")
            if r["answer_still_findable_Y_N"].strip().upper() == "Y":
                fails.append(f"{r['item_id']}: notice answer still findable")
            continue
        au = author_q[(r["item_id"], r["question"])]
        m, nat = int(r["meaning_1to3"]), int(r["naturalness_1to3"])
        pairs["meaning"][0].append(au["meaning_equivalent_all (Y/N)"].strip().upper() == "Y")
        pairs["meaning"][1].append(m >= 2)
        pairs["naturalness"][0].append(au["natural (Y/N)"].strip().upper() == "Y")
        pairs["naturalness"][1].append(nat >= 2)
        if m == 1:
            fails.append(f"{r['item_id']}:{r['question']}:{r['version']}: meaning 1")
    res = {"n_items": len({r["item_id"] for r in a2}), "fails": fails, "dimensions": {}}
    for k, (au, an) in pairs.items():
        po, kappa = cohen_kappa(au, an)
        res["dimensions"][k] = {"n": len(au), "percent_agreement": po, "cohen_kappa": kappa,
                                "author_positive": sum(au), "a2_positive": sum(an)}
    res["a2_meaning_dist"] = dict(Counter(r["meaning_1to3"] for r in a2 if r["row_type"] == "QUESTION"))
    res["a2_naturalness_dist"] = dict(Counter(r["naturalness_1to3"] for r in a2 if r["row_type"] == "QUESTION"))
    res["a2_comments"] = [{k: r[k] for k in ("item_id", "question", "version", "naturalness_1to3", "comment")}
                          for r in a2 if r["comment"].strip()]
    Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:5])
