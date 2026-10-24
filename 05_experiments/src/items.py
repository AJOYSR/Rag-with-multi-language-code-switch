"""Load base items, derive insufficient passages, validate, and expand to prompts.

An item expands to (question ∈ {main, sibling}) × variant × sufficiency rows.
The sibling question is only scored on the insufficient passage, where it must
remain answerable (near-miss control, research_plan.md §5.2).
"""
import hashlib
import random
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
    n_words = len(item["passage"].split())
    if n_words > 300:
        problems.append(f"{iid}: passage longer than 300 words")
    if item.get("format") == "multi":  # protocol v1.0 §2.2 rules for new items
        if n_words < 150:
            problems.append(f"{iid}: new-format passage shorter than 150 words ({n_words})")
        if item.get("edit_type") not in ("deletion", "neutralisation"):
            problems.append(f"{iid}: edit_type must be deletion|neutralisation")
        if (item.get("edit_type") == "deletion") != (not item.get("insuff_replacement")):
            problems.append(f"{iid}: edit_type does not match insuff_replacement")
        ent = item.get("entity") or {}
        if nfc(ent.get("bn", "")) not in nfc(item["passage"]):
            problems.append(f"{iid}: entity.bn not found in passage")
        for v, key in (("en", "en"), ("bn", "bn"), ("rbn", "rom"), ("cm", "bn"), ("cmr", "rom")):
            for qname, qd in (("main", item["q"]), ("sibling", item["sibling"]["q"])):
                if ent.get(key) and nfc(ent[key]).casefold() not in nfc(qd.get(v, "")).casefold():
                    problems.append(f"{iid}: {qname}.{v} does not name the entity ({ent[key]})")
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


def expand(items: list, variants=VARIANTS, contexts: dict = None) -> list:
    rows = []
    for it in items:
        if it.get("format") == "multi":
            if not contexts or it["id"] not in contexts:
                raise ValueError(f"{it['id']}: multi-format item needs a context (build_contexts)")
            suff, insuff = contexts[it["id"]]["suff"], contexts[it["id"]]["insuff"]
        else:
            suff, insuff = nfc(it["passage"]), insufficient_passage(it)
        for v in variants:
            q = nfc(it["q"][v])
            rows.append(Row(it["id"], "main", v, "suff", q, suff, it["answer_type"], it["gold"], True))
            rows.append(Row(it["id"], "main", v, "insuff", q, insuff, it["answer_type"], it["gold"], False))
            sq = nfc(it["sibling"]["q"][v])
            rows.append(Row(it["id"], "sibling", v, "insuff", sq, insuff,
                            it["sibling"]["answer_type"], it["sibling"]["gold"], True))
    return rows


def validate_set(items: list) -> list:
    """Cross-item checks: unique ids and unique institution names."""
    problems = []
    ids = [it["id"] for it in items]
    if len(ids) != len(set(ids)):
        problems.append("duplicate item ids")
    ents = [nfc(it["entity"]["bn"]) for it in items if it.get("entity")]
    dup = {e for e in ents if ents.count(e) > 1}
    if dup:
        problems.append(f"duplicate entities: {sorted(dup)}")
    return problems


CONTEXT_SEED = 20261024


def build_contexts(items: list, split: dict, n_distractors: int = 2, seed: int = CONTEXT_SEED) -> dict:
    """Multi-passage contexts for new-format items (protocol v1.0 §2.2 rule 6).

    Distractors are sufficient passages of other items in the same split, preferring the
    same answer type and never sharing the target entity. Target position cycles
    0,1,2 over items sorted by id within each split, so positions are balanced.
    Returns {item_id: {"suff": str, "insuff": str, "target_pos": int, "distractors": [ids]}}.
    """
    by_id = {it["id"]: it for it in items}
    out = {}
    for s in sorted(set(split.values())):
        pool = sorted(i for i, v in split.items() if v == s and by_id[i].get("format") == "multi")
        for k, iid in enumerate(pool):
            it = by_id[iid]
            rng = random.Random(int(hashlib.sha256(f"{seed}|{iid}".encode()).hexdigest(), 16))
            others = [o for o in pool if o != iid and nfc(by_id[o]["entity"]["bn"]) != nfc(it["entity"]["bn"])]
            same = [o for o in others if by_id[o]["answer_type"] == it["answer_type"]]
            rest = [o for o in others if o not in same]
            rng.shuffle(same)
            rng.shuffle(rest)
            chosen = (same + rest)[:n_distractors]
            pos = k % (n_distractors + 1)
            def render(target_text):
                passages = [nfc(by_id[o]["passage"]).strip() for o in chosen]
                passages.insert(pos, target_text.strip())
                return "\n\n".join(f"Notice {j + 1}:\n{t}" for j, t in enumerate(passages))
            out[iid] = {"suff": render(nfc(it["passage"])), "insuff": render(insufficient_passage(it)),
                        "target_pos": pos, "distractors": chosen}
    return out
