import copy

from src.items import build_contexts, expand
from src.split import assign


def mk(i, t, ent):
    return {"id": f"N{i:03d}", "format": "multi", "answer_type": t, "entity": {"bn": ent},
            "passage": f"{ent} নোটিশ। উত্তর বাক্য {i}।", "answer_sentence": f"উত্তর বাক্য {i}।",
            "insuff_replacement": "", "gold": {"value": i}, "q": {v: "q" for v in ("en", "bn", "rbn", "cm", "cmr")},
            "sibling": {"answer_type": "number", "gold": {"value": 1}, "q": {v: "s" for v in ("en", "bn", "rbn", "cm", "cmr")}}}


TYPES = ["number", "amount", "date", "name", "yesno"]
ITEMS = [mk(i, TYPES[i % 5], f"সংস্থা{i}") for i in range(1, 51)] + [{"id": "P01", "answer_type": "amount"}]


def test_split_deterministic_and_stratified():
    a, b = assign(ITEMS), assign(copy.deepcopy(ITEMS))
    assert a == b
    assert a["P01"] == "dev"
    for t in TYPES:
        dev = [i for i in ITEMS if i.get("format") == "multi" and i["answer_type"] == t and a[i["id"]] == "dev"]
        assert len(dev) == 4


def test_contexts_same_split_distinct_entities_balanced_positions():
    multi = [i for i in ITEMS if i.get("format") == "multi"]
    split = assign(ITEMS)
    split = {k: v for k, v in split.items() if k != "P01"}
    ctx = build_contexts(multi, split)
    for iid, c in ctx.items():
        assert all(split[d] == split[iid] for d in c["distractors"])
        assert iid not in c["distractors"] and len(c["distractors"]) == 2
        assert c["suff"].count("Notice ") == 3
        assert "উত্তর বাক্য" in c["suff"]
    test_pos = [c["target_pos"] for i, c in ctx.items() if split[i] == "test"]
    assert max(test_pos.count(p) for p in (0, 1, 2)) - min(test_pos.count(p) for p in (0, 1, 2)) <= 1
    assert build_contexts(multi, split) == ctx  # deterministic


def test_insufficient_context_removes_only_target_answer():
    multi = [i for i in ITEMS if i.get("format") == "multi"]
    split = {i["id"]: "test" for i in multi}
    ctx = build_contexts(multi, split)
    c = ctx["N010"]
    assert "উত্তর বাক্য 10।" in c["suff"] and "উত্তর বাক্য 10।" not in c["insuff"]
    for d in c["distractors"]:
        n = int(d[1:])
        assert f"উত্তর বাক্য {n}।" in c["insuff"]  # distractors unchanged


def test_expand_requires_context_for_multi():
    import pytest
    with pytest.raises(ValueError):
        expand([ITEMS[0]])


def test_prompts_plural_only_for_multi_and_single_unchanged():
    from src.prompts import M1_SYSTEM, messages
    single = messages("M1", "q?", "একটি নোটিশ")
    assert single[0]["content"] == M1_SYSTEM
    multi = messages("M1", "q?", "Notice 1:\nক\n\nNotice 2:\nখ")
    assert "the notices" in multi[0]["content"] and "a notice" not in multi[0]["content"]
    assert "noticess" not in multi[0]["content"]
