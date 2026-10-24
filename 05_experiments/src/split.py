"""Deterministic dev/test split by base item (protocol v1.0 §3).

Usage: python -m src.split <items.yaml> <out_dir>
Pilot items (format != "multi") are dev-only. New items: N_DEV_PER_TYPE per answer type
go to dev, the rest to test, chosen with a fixed seed.
"""
import random
import sys
from pathlib import Path

from .items import ANSWER_TYPES, load

SEED = 20261024
N_DEV_PER_TYPE = 4  # 5 types x 4 = 20 new dev items


def assign(items: list, seed: int = SEED, n_dev_per_type: int = N_DEV_PER_TYPE) -> dict:
    split = {it["id"]: "dev" for it in items if it.get("format") != "multi"}
    new = [it for it in items if it.get("format") == "multi"]
    rng = random.Random(seed)
    for t in ANSWER_TYPES:
        ids = sorted(it["id"] for it in new if it["answer_type"] == t)
        rng.shuffle(ids)
        for i, iid in enumerate(ids):
            split[iid] = "dev" if i < n_dev_per_type else "test"
    return split


def main(items_path, out_dir):
    split = assign(load(items_path))
    out = Path(out_dir)
    for s in ("dev", "test"):
        ids = sorted(k for k, v in split.items() if v == s)
        (out / f"{s}.txt").write_text("\n".join(ids) + "\n")
        print(s, len(ids))


if __name__ == "__main__":
    main(*sys.argv[1:3])
