"""Second-annotator sample sheet (protocol v1.0 §6; 04_methodology/annotation_guidelines.md).

Usage: python -m src.build_annotation_sample <approved_items.yaml> <out_dir> [fraction]
Draws a stratified (by answer type) random sample of >= 20% of new-format items,
seed fixed. Writes annotation_sample.csv (UTF-8 with BOM) with one row per question
version (BN/RBN/CM/CMR against the EN reference) plus one notice row per item for the
insufficiency check. Rating columns are left blank for the annotator.
"""
import csv
import math
import random
import sys
from pathlib import Path

from .items import ANSWER_TYPES, insufficient_passage, load

SEED = 20261024
BENGALI_VARIANTS = ("bn", "rbn", "cm", "cmr")


def sample_ids(items: list, fraction: float = 0.2, seed: int = SEED) -> list:
    new = [it for it in items if it.get("format") == "multi"]
    rng = random.Random(seed)
    chosen = []
    for t in ANSWER_TYPES:
        ids = sorted(it["id"] for it in new if it["answer_type"] == t)
        rng.shuffle(ids)
        chosen += ids[: math.ceil(len(ids) * fraction)]
    return sorted(chosen)


def main(items_path, out_dir, fraction="0.2"):
    items = {it["id"]: it for it in load(items_path)}
    ids = sample_ids(list(items.values()), float(fraction))
    rows = []
    for iid in ids:
        it = items[iid]
        rows.append({"row_type": "NOTICE", "item_id": iid, "question": "main", "version": "",
                     "english_reference": it["q"]["en"], "text_to_rate": insufficient_passage(it).strip(),
                     "meaning_1to3": "n/a", "naturalness_1to3": "n/a",
                     "answer_still_findable_Y_N": "", "comment": ""})
        for qname, q in (("main", it["q"]), ("sibling", it["sibling"]["q"])):
            for v in BENGALI_VARIANTS:
                rows.append({"row_type": "QUESTION", "item_id": iid, "question": qname, "version": v.upper(),
                             "english_reference": q["en"], "text_to_rate": q[v],
                             "meaning_1to3": "", "naturalness_1to3": "",
                             "answer_still_findable_Y_N": "n/a", "comment": ""})
    out = Path(out_dir) / "annotation_sample.csv"
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(ids)} items ({len(ids) / max(1, sum(1 for i in items.values() if i.get('format') == 'multi')):.0%} of new items), "
          f"{len(rows)} rows -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
