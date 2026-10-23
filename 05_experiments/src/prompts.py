"""Prompt templates. Instructions are in English for every variant (a fixed
protocol choice; instruction-language effects are a robustness check).

M1  instructed abstention (single call)
M3  selective generation (Joren et al. 2025, §5.1, adapted):
      gen   answer without an abstention option -> answer + token logprobs (M2b confidence)
      suff  sufficiency rater, adapted from the FLAMe prompt in the
            github.com/hljoren/sufficientcontext README (paper App. C.2 has the labels
            swapped; the README version is used). Score = P("1") from first-token logprobs.
CB  closed-book control (no passage)
TR  comprehension probe: translate the query into English (RQ3)
"""
from .normalize import ABSTAIN_TOKEN

PROMPT_VERSION = "v0.1-2026-10-23"

M1_SYSTEM = (
    "You answer questions about a notice using only the information in the notice. "
    f"If the notice does not contain the information needed to answer the question, reply exactly {ABSTAIN_TOKEN}. "
    "Otherwise reply with the short answer only, with no explanation."
)

GEN_SYSTEM = (
    "You answer questions about a notice using the information in the notice. "
    "Reply with the short answer only, with no explanation."
)

SUFF_SYSTEM = (
    "In this task, you will be provided with a document and a question. "
    "Decide whether the document is sufficient to infer the answer to the question.\n"
    "1: The document is sufficient to infer the answer to the question.\n"
    "0: The document is not sufficient to infer the answer to the question.\n"
    "Reply with a single digit, 1 or 0, and nothing else."
)

CB_SYSTEM = (
    f"Answer the question. If you do not know the answer, reply exactly {ABSTAIN_TOKEN}. "
    "Reply with the short answer only, with no explanation."
)

TR_SYSTEM = "Translate the following question into English. Output only the English translation."


def with_passage(passage: str, query: str) -> str:
    return f"Notice:\n{passage.strip()}\n\nQuestion: {query.strip()}"


def suff_user(passage: str, query: str) -> str:
    return f"Document:\n{passage.strip()}\n\nQuestion: {query.strip()}"


def messages(method: str, query: str, passage: str = "") -> list:
    if method == "M1":
        return [{"role": "system", "content": M1_SYSTEM}, {"role": "user", "content": with_passage(passage, query)}]
    if method == "GEN":
        return [{"role": "system", "content": GEN_SYSTEM}, {"role": "user", "content": with_passage(passage, query)}]
    if method == "SUFF":
        return [{"role": "system", "content": SUFF_SYSTEM}, {"role": "user", "content": suff_user(passage, query)}]
    if method == "CB":
        return [{"role": "system", "content": CB_SYSTEM}, {"role": "user", "content": query.strip()}]
    if method == "TR":
        return [{"role": "system", "content": TR_SYSTEM}, {"role": "user", "content": query.strip()}]
    raise ValueError(method)
