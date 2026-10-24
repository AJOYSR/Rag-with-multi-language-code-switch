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

PROMPT_VERSION = "v1.0-2026-10-24"

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

TRP_SYSTEM = ("You will see one or more notices and a question about them. "
              "Restate the question in English. Output only the English question, nothing else.")

# Pre-specified paraphrases for robustness check 1 (protocol v1.0 §9). Written before any test run.
PARAPHRASE_B = {
    "M1": ("Use only the notice to answer the question. Give just the answer, without explanation. "
           f"If the notice does not provide what is needed, write {ABSTAIN_TOKEN} and nothing else."),
    "GEN": "Use the notice to answer the question. Give just the answer, without explanation.",
    "SUFF": ("You are given a document and a question. Can the answer to the question be determined from "
             "the document? Answer 1 for yes or 0 for no. Output only the digit."),
}


def with_passage(passage: str, query: str) -> str:
    head = "" if passage.lstrip().startswith("Notice 1:") else "Notice:\n"  # multi-passage contexts carry their own headings
    return f"{head}{passage.strip()}\n\nQuestion: {query.strip()}"


def suff_user(passage: str, query: str) -> str:
    return f"Document:\n{passage.strip()}\n\nQuestion: {query.strip()}"


def _plural(msgs: list) -> list:
    """Multi-notice contexts: 'a notice'/'the notice' -> plural, so instructions match the input."""
    sys_ = msgs[0]["content"].replace("a notice", "the notices").replace("the notice", "the notices")
    return [{"role": "system", "content": sys_.replace("the noticess", "the notices")}] + msgs[1:]


def messages(method: str, query: str, passage: str = "", paraphrase: str = "A") -> list:
    msgs = _messages(method, query, passage, paraphrase)
    return _plural(msgs) if passage.lstrip().startswith("Notice 1:") else msgs


def _messages(method: str, query: str, passage: str = "", paraphrase: str = "A") -> list:
    if paraphrase == "B" and method in PARAPHRASE_B:
        user = suff_user(passage, query) if method == "SUFF" else with_passage(passage, query)
        return [{"role": "system", "content": PARAPHRASE_B[method]}, {"role": "user", "content": user}]
    if method == "TRP":
        return [{"role": "system", "content": TRP_SYSTEM}, {"role": "user", "content": with_passage(passage, query)}]
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
