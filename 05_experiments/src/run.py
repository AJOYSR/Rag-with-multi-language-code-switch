"""Run one config: python -m src.run configs/<name>.yaml

Writes runs/<run_id>/meta.json and runs/<run_id>/responses.jsonl (append-only;
an interrupted run resumes by skipping keys already written). If the environment variable
RUN_DEADLINE (Unix time) is set, the run stops cleanly between calls once it passes.
"""
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from . import llm
from .items import build_contexts, expand, load, validate
from .split import assign
from .prompts import PROMPT_VERSION, messages

ROOT = Path(__file__).resolve().parents[2]
MAX_TOKENS = {"M1": 64, "GEN": 64, "SUFF": 2, "CB": 64, "TR": 96, "TRP": 96}


def git_commit() -> str:
    try:
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return head + ("-dirty" if dirty else "")
    except OSError:
        return "unknown"


def guard(cfg: dict, items: list):
    """Integrity rules: no runs on unreviewed items except labelled smoke tests; no test split here."""
    path = cfg["items"]
    if "draft" in Path(path).name and not (cfg.get("smoke") and cfg.get("max_items", 99) <= 2):
        sys.exit(f"refusing: {path} is an unreviewed draft. Only smoke runs with max_items <= 2 may use it.")
    if cfg.get("split", "dev") == "test" and not cfg.get("protocol_frozen_hash"):
        sys.exit("refusing: test-split runs require protocol_frozen_hash (protocol freeze + author approval).")
    problems = [p for it in items for p in validate(it)]
    if problems:
        sys.exit("refusing: item validation failed:\n" + "\n".join(problems))


def jobs(cfg: dict, items: list, all_items: list = None):
    contexts = None
    if any(it.get("format") == "multi" for it in items):
        pool = all_items or items
        contexts = build_contexts(pool, assign(pool))
    rows = expand(items, cfg["variants"], contexts)
    para = cfg.get("paraphrase", "A")
    for r in rows:
        for m in cfg["methods"]:
            if m in ("M1", "GEN", "SUFF"):
                yield m, r, messages(m, r.query, r.passage, para)
            elif m == "TRP" and r.question == "main" and r.sufficiency == "suff" and r.variant != "en":
                yield m, r, messages(m, r.query, r.passage)
            elif m == "CB" and r.question == "main" and r.sufficiency == "suff":
                yield m, r, messages(m, r.query)
            elif m == "TR" and r.question == "main" and r.sufficiency == "suff" and r.variant != "en":
                yield m, r, messages(m, r.query)


def main(cfg_path: str):
    cfg = yaml.safe_load(Path(cfg_path).read_text())
    all_items = load(ROOT / cfg["items"])
    guard(cfg, all_items)
    items = all_items
    if cfg.get("split") in ("dev", "test") and any(it.get("format") == "multi" for it in all_items):
        split = assign(all_items)
        items = [it for it in all_items if split[it["id"]] == cfg["split"]]
    items = items[: cfg.get("max_items", len(items))]
    run_id = cfg.get("run_id") or f"{dt.date.today():%Y%m%d}_{Path(cfg_path).stem}"
    out = ROOT / "05_experiments" / "runs" / run_id
    out.mkdir(parents=True, exist_ok=True)
    meta_path = out / "meta.json"
    if not meta_path.exists():
        meta = {"run_id": run_id, "config": cfg, "config_path": str(cfg_path), "started": dt.datetime.now().isoformat(),
                "git_commit": git_commit(), "ollama_version": llm.server_version(),
                "model": llm.model_info(cfg["model"]), "prompt_version": PROMPT_VERSION,
                "decoding": {"temperature": cfg.get("temperature", 0.0), "seed": cfg.get("seed", 0),
                             "num_ctx": cfg.get("num_ctx", 4096), "max_tokens": MAX_TOKENS}}
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    resp_path = out / "responses.jsonl"
    done = set()
    if resp_path.exists():
        lines = resp_path.read_text(encoding="utf-8").splitlines()
        if lines and lines[-1].strip():
            try:
                json.loads(lines[-1])
            except json.JSONDecodeError:  # half-written last line from a hard stop: drop it, the call is redone
                resp_path.write_text("\n".join(lines[:-1]) + ("\n" if len(lines) > 1 else ""), encoding="utf-8")
                lines = lines[:-1]
                print("dropped a half-written last line", flush=True)
        done = {json.loads(l)["key"] for l in lines if l.strip()}
    todo = [(m, r, msg) for m, r, msg in jobs(cfg, items, all_items)
            if f"{m}|{r.item_id}|{r.question}|{r.variant}|{r.sufficiency}" not in done]
    print(f"{run_id}: {len(done)} done, {len(todo)} to go", flush=True)
    deadline = float(os.environ.get("RUN_DEADLINE", "inf"))
    with open(resp_path, "a", encoding="utf-8") as f:
        for i, (m, r, msg) in enumerate(todo, 1):
            if dt.datetime.now().timestamp() > deadline:
                print(f"{run_id}: deadline reached, stopped cleanly after {i - 1} calls this session", flush=True)
                sys.exit(3)
            res = llm.chat(cfg["model"], msg, seed=cfg.get("seed", 0), temperature=cfg.get("temperature", 0.0),
                           max_tokens=MAX_TOKENS[m], num_ctx=cfg.get("num_ctx", 4096))
            rec = {"key": f"{m}|{r.item_id}|{r.question}|{r.variant}|{r.sufficiency}", "method": m,
                   **{k: v for k, v in r.__dict__.items() if k != "passage"}, "messages": msg, **res}
            if (res.get("prompt_tokens") or 0) + MAX_TOKENS[m] >= cfg.get("num_ctx", 4096):
                sys.exit(f"refusing: prompt may be truncated ({res['prompt_tokens']} tokens, num_ctx {cfg.get('num_ctx', 4096)}) "
                         f"at {rec['key']}; raise num_ctx in the config")
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if i % 50 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    print(f"{run_id}: finished", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
