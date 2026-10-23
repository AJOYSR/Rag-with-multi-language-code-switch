"""Write the author review sheets for drafted pilot items.

Usage: python -m src.build_review_sheet <items.yaml> <out_dir>
Produces review_pilot.csv (question variants) and review_pilot_passages.csv
(evidence + insufficient edit). UTF-8 with BOM so spreadsheet apps show Bengali.
"""
import csv
import sys
from pathlib import Path

from .items import VARIANTS, insufficient_passage, load, validate


def main(items_path, out_dir):
    items = load(items_path)
    problems = [p for it in items for p in validate(it)]
    if problems:
        sys.exit("refusing to build sheet; automatic checks failed:\n" + "\n".join(problems))
    out = Path(out_dir)
    with open(out / "review_pilot.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "question", *VARIANTS,
                    *[f"{v}_EDIT" for v in VARIANTS],
                    "meaning_equivalent_all (Y/N)", "natural (Y/N)", "STATUS (approve/edit/drop)", "comment"])
        for it in items:
            for qkey, q in (("main", it["q"]), ("sibling", it["sibling"]["q"])):
                w.writerow([it["id"], qkey, *[q[v] for v in VARIANTS], *[""] * len(VARIANTS), "", "", "", ""])
    with open(out / "review_pilot_passages.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "domain", "answer_type", "gold", "sibling_gold", "passage_SUFFICIENT",
                    "answer_sentence", "replacement", "passage_INSUFFICIENT",
                    "passage_EDIT", "replacement_EDIT", "insufficient_really_unanswerable (Y/N)",
                    "names_fictional_ok (Y/N)", "STATUS (approve/edit/drop)", "comment"])
        for it in items:
            w.writerow([it["id"], it["domain"], it["answer_type"], it["gold"], it["sibling"]["gold"],
                        it["passage"].strip(), it["answer_sentence"], it["insuff_replacement"] or "(delete)",
                        insufficient_passage(it).strip(), "", "", "", "", "", ""])
    print(f"wrote {len(items)} items to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
