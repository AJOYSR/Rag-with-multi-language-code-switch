"""Re-check sheet for the second annotator after author revisions (guidelines: revised versions are re-checked).

Usage: python -m src.build_recheck <approved_items.yaml> <review_RETURNED.csv> <out.csv>
One QUESTION row per revised string (any *_EDIT cell in the returned review sheet),
in the annotation_sample.csv format, with the current approved text.
"""
import csv
import sys

from .build_annotation_sample import BENGALI_VARIANTS
from .items import load


def main(items_path, review, out):
    items = {it["id"]: it for it in load(items_path)}
    with open(review, encoding="utf-8-sig", newline="") as f:
        edited = [(r["item_id"], r["question"], v) for r in csv.DictReader(f)
                  for v in BENGALI_VARIANTS if r.get(f"{v}_EDIT", "").strip() and r["item_id"] in items]
    rows = []
    for iid, qname, v in edited:
        q = items[iid]["q"] if qname == "main" else items[iid]["sibling"]["q"]
        rows.append({"row_type": "QUESTION", "item_id": iid, "question": qname, "version": v.upper(),
                     "english_reference": q["en"], "text_to_rate": q[v], "meaning_1to3": "", "naturalness_1to3": "",
                     "answer_still_findable_Y_N": "n/a", "comment": ""})
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} revised strings -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
