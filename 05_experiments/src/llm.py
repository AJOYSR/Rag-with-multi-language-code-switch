"""Minimal Ollama chat client with deterministic decoding and logprobs."""
import math
import time

import requests

HOST = "http://localhost:11434"


def chat(model: str, messages: list, *, seed: int = 0, temperature: float = 0.0,
         max_tokens: int = 64, num_ctx: int = 4096, top_logprobs: int = 20, timeout: int = 600) -> dict:
    payload = {
        "model": model, "messages": messages, "stream": False, "think": False,
        "logprobs": True, "top_logprobs": top_logprobs,
        "options": {"seed": seed, "temperature": temperature, "num_predict": max_tokens, "num_ctx": num_ctx},
    }
    t0 = time.time()
    r = requests.post(f"{HOST}/api/chat", json=payload, timeout=timeout)
    if r.status_code == 400 and "think" in r.text:  # models without a thinking mode reject the flag
        payload.pop("think")
        r = requests.post(f"{HOST}/api/chat", json=payload, timeout=timeout)
    r.raise_for_status()
    out = r.json()
    return {
        "content": out["message"]["content"],
        "logprobs": out.get("logprobs") or [],
        "prompt_tokens": out.get("prompt_eval_count"),
        "output_tokens": out.get("eval_count"),
        "latency_s": round(time.time() - t0, 3),
        "done_reason": out.get("done_reason"),
    }


def model_info(model: str) -> dict:
    """Exact model identity for the run record: digest, quantisation, parameter size."""
    tags = requests.get(f"{HOST}/api/tags", timeout=30).json()["models"]
    tag = next(m for m in tags if m["name"] == model or m["model"] == model)
    show = requests.post(f"{HOST}/api/show", json={"model": model}, timeout=30).json()
    return {"name": model, "digest": tag["digest"], "details": tag.get("details", {}),
            "size_bytes": tag.get("size"), "license_head": (show.get("license") or "")[:200]}


def server_version() -> str:
    return requests.get(f"{HOST}/api/version", timeout=10).json()["version"]


def first_token_binary_prob(logprobs: list, yes: str = "1", no: str = "0") -> float:
    """P(yes) / (P(yes) + P(no)) from the first generated token's top_logprobs; NaN if absent."""
    if not logprobs:
        return float("nan")
    cands = logprobs[0].get("top_logprobs") or []
    p = {"yes": 0.0, "no": 0.0}
    for c in cands:
        tok = c["token"].strip()
        if tok == yes:
            p["yes"] += math.exp(c["logprob"])
        elif tok == no:
            p["no"] += math.exp(c["logprob"])
    tot = p["yes"] + p["no"]
    return p["yes"] / tot if tot > 0 else float("nan")


def mean_logprob(logprobs: list) -> float:
    """Length-normalised sequence log-probability of the generated answer (M2b confidence)."""
    vals = [x["logprob"] for x in logprobs if "logprob" in x]
    return sum(vals) / len(vals) if vals else float("nan")
