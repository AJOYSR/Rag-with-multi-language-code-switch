"""Load base items, derive insufficient passages, validate, and expand to prompts.

An item expands to (question ∈ {main, sibling}) × variant × sufficiency rows.
The sibling question is only scored on the insufficient passage, where it must
remain answerable (near-miss control, research_plan.md §5.2).
"""
from dataclasses import dataclass
from pathlib import Path

import yaml

from .normalize import match, nfc

VARIANTS = ("en", "bn", "rbn", "cm", "cmr")
ANSWER_TYPES = ("number", "amount", "date", "name", "yesno")


@dataclass
class Row:
    item_id: str
    question: str        # "main" | "sibling"
    variant: str
    sufficiency: str     # "suff" | "insuff"
    query: str
    passage: str
    answer_type: str
    gold: dict
    expect_answer: bool  # True if the evidence supports an answer


def insufficient_passage(item: dict) -> str:
    passage, sent = nfc(item["passage"]), nfc(item["answer_sentence"])
    if passage.count(sent) != 1:
        raise ValueError(f"{item['id']}: answer_sentence must occur exactly once in passage")
    out = passage.replace(sent, nfc(item["insuff_replacement"]))
    return " ".join(out.split(" ")).replace("  ", " ")


def validate(item: dict) -> list:
    """Return a list of problems (empty = passes the automatic checks)."""
    problems = []
    iid = item.get("id", "?")
    for key in ("id", "passage", "answer_sentence", "insuff_replacement", "answer_type", "gold", "q", "sibling"):
        if key not in item:
            problems.append(f"{iid}: missing {key}")
    if problems:
        return problems
    if item["answer_type"] not in ANSWER_TYPES:
        problems.append(f"{iid}: bad answer_type {item['answer_type']}")
    missing = [v for v in VARIANTS if not item["q"].get(v)] + [f"sibling.{v}" for v in VARIANTS if not item["sibling"]["q"].get(v)]
    if missing:
        problems.append(f"{iid}: missing variants {missing}")
    if len(item["passage"].split()) > 300:
        problems.append(f"{iid}: passage longer than 300 words")
    try:
        insuff = insufficient_passage(item)
    except ValueError as e:
        return problems + [str(e)]
    if item["answer_type"] != "yesno":
        # yes/no answers cannot be string-checked against a passage
        if not match(item["passage"], item["answer_type"], item["gold"]):
            problems.append(f"{iid}: gold answer not found in sufficient passage")
        if match(insuff, item["answer_type"], item["gold"]):
            problems.append(f"{iid}: gold answer still present in insufficient passage")
    sib = item["sibling"]
    if sib["answer_type"] != "yesno" and not match(insuff, sib["answer_type"], sib["gold"]):
        problems.append(f"{iid}: sibling answer missing from insufficient passage")
    return problems


def load(path) -> list:
    items = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    ids = [it["id"] for it in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate item ids")
    return items


def expand(items: list, variants=VARIANTS) -> list:
    rows = []
    for it in items:
        suff, insuff = nfc(it["passage"]), insufficient_passage(it)
        for v in variants:
            q = nfc(it["q"][v])
            rows.append(Row(it["id"], "main", v, "suff", q, suff, it["answer_type"], it["gold"], True))
            rows.append(Row(it["id"], "main", v, "insuff", q, insuff, it["answer_type"], it["gold"], False))
            sq = nfc(it["sibling"]["q"][v])
            rows.append(Row(it["id"], "sibling", v, "insuff", sq, insuff,
                            it["sibling"]["answer_type"], it["sibling"]["gold"], True))
    return rows
