"""Control-round sheet for the second annotator (key: 04_methodology/annotation_controls_KEY.yaml).

Usage: python -m src.build_annotation_controls <approved_items.yaml> <key.yaml> <out.csv>
       python -m src.build_annotation_controls --score <key.yaml> <returned.csv>
Same columns as annotation_sample.csv, plus a control_id; rows shuffled with a fixed seed.
Clean question rows use the approved text; planted-flaw rows use the key's text.
"""
import csv
import json
import random
import sys
from pathlib import Path

import yaml

from .build_annotation_sample import SEED
from .items import insufficient_passage, load

FIELDS = ["control_id", "row_type", "item_id", "question", "version", "english_reference", "text_to_rate",
          "meaning_1to3", "naturalness_1to3", "answer_still_findable_Y_N", "comment"]


def build(items_path, key_path, out):
    items = {it["id"]: it for it in load(items_path)}
    rows = []
    for c in yaml.safe_load(Path(key_path).read_text(encoding="utf-8"))["controls"]:
        it = items[c["item"]]
        if c["version"]:
            rows.append({"control_id": c["cid"], "row_type": "QUESTION", "item_id": c["item"], "question": c["question"],
                         "version": c["version"], "english_reference": it["q"]["en"],
                         "text_to_rate": c.get("text") or it["q"][c["version"].lower()],
                         "meaning_1to3": "", "naturalness_1to3": "", "answer_still_findable_Y_N": "n/a", "comment": ""})
        else:
            text = it["passage"] if c["passage"] == "sufficient" else insufficient_passage(it)
            rows.append({"control_id": c["cid"], "row_type": "NOTICE", "item_id": c["item"], "question": "main",
                         "version": "", "english_reference": it["q"]["en"], "text_to_rate": text.strip(),
                         "meaning_1to3": "n/a", "naturalness_1to3": "n/a", "answer_still_findable_Y_N": "", "comment": ""})
    random.Random(SEED).shuffle(rows)
    for i, r in enumerate(rows, 1):
        r["control_id"] = f"X{i:02d}"  # neutral ids; scoring matches rows to the key by (item, version)
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {out}")


def score(key_path, returned):
    key = {(c["item"], c["version"]): c for c in yaml.safe_load(Path(key_path).read_text(encoding="utf-8"))["controls"]}
    with open(returned, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    flaws = hits = clean = false_alarms = 0
    detail = []
    for r in rows:
        c = key[(r["item_id"], r["version"])]
        m, n, y = r["meaning_1to3"].strip(), r["naturalness_1to3"].strip(), r["answer_still_findable_Y_N"].strip().upper()
        if c["expect"] == "clean":
            alarm = m == "1" or n == "1" or y == "Y"
            clean += 1
            false_alarms += alarm
            detail.append({"cid": c["cid"], "expect": "clean", "false_alarm": alarm, "a2": [m, n, y]})
        else:
            hit = {"meaning": m == "1", "naturalness": n in ("1", "2"), "leak": y == "Y"}[c["expect"]]
            flaws += 1
            hits += hit
            detail.append({"cid": c["cid"], "expect": c["expect"], "detected": hit, "a2": [m, n, y]})
    res = {"flaws": flaws, "detected": hits, "clean": clean, "false_alarms": false_alarms,
           "pass": hits >= 7 and false_alarms <= 1, "detail": detail}
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return res


if __name__ == "__main__":
    if sys.argv[1] == "--score":
        score(*sys.argv[2:4])
    else:
        build(*sys.argv[1:4])
