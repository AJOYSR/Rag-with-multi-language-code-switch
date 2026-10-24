"""Write the author review sheets for drafted pilot items.

Usage: python -m src.build_review_sheet <items.yaml> <out_dir> [prefix]
Produces <prefix>.csv (question variants) and <prefix>_passages.csv (default prefix: review_pilot)
(evidence + insufficient edit). UTF-8 with BOM so spreadsheet apps show Bengali.
An optional item field `review_flag` is shown in a CHECK_FIRST column of both sheets.
"""
import csv
import sys
from pathlib import Path

from .items import VARIANTS, insufficient_passage, load, validate


def readable(answer_type, gold):
    if answer_type == "amount":
        return f"{gold['value']} টাকা"
    if answer_type == "number":
        return str(gold["value"])
    if answer_type == "date":
        return f"{gold['day']}/{gold['month']}/{gold.get('year') or '—'}"
    if answer_type == "name":
        return " / ".join(gold["aliases"])
    return "হ্যাঁ (Yes)" if gold["value"] else "না (No)"


def main(items_path, out_dir, prefix="review_pilot"):
    items = load(items_path)
    problems = [p for it in items for p in validate(it)]
    if problems:
        sys.exit("refusing to build sheet; automatic checks failed:\n" + "\n".join(problems))
    out = Path(out_dir)
    with open(out / f"{prefix}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "CHECK_FIRST", "question", *VARIANTS,
                    *[f"{v}_EDIT" for v in VARIANTS],
                    "meaning_equivalent_all (Y/N)", "natural (Y/N)", "STATUS (approve/edit/drop)", "comment"])
        for it in items:
            for qkey, q in (("main", it["q"]), ("sibling", it["sibling"]["q"])):
                w.writerow([it["id"], it.get("review_flag", ""), qkey, *[q[v] for v in VARIANTS], *[""] * len(VARIANTS), "", "", "", ""])
    with open(out / f"{prefix}_passages.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "CHECK_FIRST", "domain", "institution", "edit_type", "MAIN_QUESTION (en)", "MAIN_QUESTION (bn)", "main_answer",
                    "SIBLING_QUESTION (en)", "SIBLING_QUESTION (bn)", "sibling_answer", "passage_SUFFICIENT",
                    "answer_sentence", "replacement", "passage_INSUFFICIENT",
                    "passage_EDIT", "replacement_EDIT", "insufficient_really_unanswerable (Y/N)",
                    "names_fictional_ok (Y/N)", "STATUS (approve/edit/drop)", "comment"])
        for it in items:
            sib = it["sibling"]
            w.writerow([it["id"], it.get("review_flag", ""), it["domain"], (it.get("entity") or {}).get("bn", ""), it.get("edit_type", "deletion/neutral"), it["q"]["en"], it["q"]["bn"], readable(it["answer_type"], it["gold"]),
                        sib["q"]["en"], sib["q"]["bn"], readable(sib["answer_type"], sib["gold"]),
                        it["passage"].strip(), it["answer_sentence"], it["insuff_replacement"] or "(delete)",
                        insufficient_passage(it).strip(), "", "", "", "", "", ""])
    print(f"wrote {len(items)} items to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
