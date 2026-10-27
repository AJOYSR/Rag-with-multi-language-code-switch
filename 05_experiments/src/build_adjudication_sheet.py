"""Author adjudication sheet for 'ambiguous' M1/GEN responses (protocol v1.0 §6).

Usage: python -m src.build_adjudication_sheet <out.csv> runs/<run> [runs/<run> ...]
Lists ambiguous rows not yet labelled in any 06_results/adjudication_*.csv. The gold
answer is not shown; the variant is (unavoidable, disclosed). The author fills `label` with
one of: specific_yes, specific_no, specific (non-yes/no value), nonspecific, abstain.
"""
import csv
import sys
from pathlib import Path

from .analyze_pilot import ROOT, load_run

LABELS = "specific_yes | specific_no | specific | nonspecific | abstain"


def main(out, *runs):
    rows = []
    for run in runs:
        rd = Path(run) if Path(run).is_absolute() else ROOT / "05_experiments" / run
        df = load_run(rd)
        en_q = df[(df.variant == "en")].drop_duplicates(["item_id", "question"]).set_index(["item_id", "question"])["query"]
        amb = df[(df.category == "ambiguous") & df.method.isin(["M1", "GEN"]) & df.adjudicated.isna()]
        for _, r in amb.iterrows():
            rows.append({"run_id": rd.name, "key": r["key"], "answer_type": r["answer_type"],
                         "english_question": en_q[(r["item_id"], r["question"])], "question_as_asked": r["query"],
                         "model_response": r["content"].strip(), "label": "", "note": ""})
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["run_id", "key", "answer_type", "english_question", "question_as_asked",
                                          "model_response", "label", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {out}  (labels: {LABELS})")


if __name__ == "__main__":
    main(*sys.argv[1:])
