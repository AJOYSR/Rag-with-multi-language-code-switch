"""Deterministic answer normalisation and abstention detection.

Everything here is pure and rule-based so that scoring is reproducible.
Rules are deliberately conservative: when a response is ambiguous the
scorer returns None and the case goes to manual adjudication.
"""
import re
import unicodedata

ABSTAIN_TOKEN = "NOT_ANSWERABLE"

BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

# Month names -> month number. Bengali spellings of Gregorian months as used in
# Bangladeshi notices, plus English names and abbreviations.
MONTHS = {
    "জানুয়ারি": 1, "জানুয়ারী": 1, "ফেব্রুয়ারি": 2, "ফেব্রুয়ারী": 2, "মার্চ": 3,
    "এপ্রিল": 4, "মে": 5, "জুন": 6, "জুলাই": 7, "আগস্ট": 8, "অগাস্ট": 8,
    "সেপ্টেম্বর": 9, "অক্টোবর": 10, "নভেম্বর": 11, "ডিসেম্বর": 12,
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9, "october": 10,
    "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
    # common romanized-Bengali spellings
    "januari": 1, "februari": 2, "agust": 8, "agost": 8, "oktobor": 10,
    "novembor": 11, "disembor": 12, "septembor": 9,
}

CURRENCY = r"(টাকা|টাকার|টাকায়|৳|tk\.?|taka|bdt)"

YES = {"yes", "হ্যাঁ", "হ্যা", "হা", "hya", "haa", "hae", "ha", "haan", "hyan", "ji", "জি"}
NO = {"no", "না", "na", "nah"}

# Phrases that signal abstention when a model ignores the exact token.
# Matched against basic(), which turns apostrophes into spaces ("don t").
ABSTAIN_PATTERNS = [
    r"not[_ ]answerable", r"cannot be answered", r"can ?t be answered",
    r"does not (contain|mention|provide|specify|state)", r"doesn ?t (contain|mention|provide|specify|state)",
    r"not (mentioned|provided|specified|stated|given) in", r"no information",
    r"insufficient (information|context)", r"i (do not|don ?t) know",
    r"(does not|doesn ?t|did not|didn ?t) say", r"not (specified|stated|mentioned)\b",
    r"উল্লেখ (নেই|করা হয়নি|করা নেই)", r"তথ্য (নেই|দেওয়া নেই|দেওয়া হয়নি)",
    r"উত্তর দেওয়া (সম্ভব নয়|যাচ্ছে না)", r"জানা নেই", r"বলা (হয়নি|নেই)",
]


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


# Keyword tables must be NFC like the text they are matched against: NFC
# decomposes "য়" (U+09DF) into U+09AF U+09BC, so raw literals would not match.
MONTHS = {nfc(k): v for k, v in MONTHS.items()}
YES = {nfc(w) for w in YES}
NO = {nfc(w) for w in NO}
ABSTAIN_PATTERNS = [nfc(p) for p in ABSTAIN_PATTERNS]


def basic(text: str) -> str:
    """NFC, Bengali digits -> ASCII, casefold, unify whitespace and punctuation."""
    t = nfc(text).translate(BN_DIGITS).casefold()
    t = t.replace("‌", "").replace("‍", "")  # ZWNJ / ZWJ
    t = re.sub(r"(?<=\d),(?=\d{2,3}\b)", "", t)  # 1,500 / 1,50,000 -> 1500 / 150000
    t = re.sub(r"[\"'“”‘’`*_()\[\]{}<>]", " ", t)
    t = re.sub(r"[।.,;:!?]+(?=\s|$)", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def is_abstention(response: str) -> bool:
    t = basic(response)
    if ABSTAIN_TOKEN.casefold() in t:
        return True
    return any(re.search(p, t) for p in ABSTAIN_PATTERNS)


_BN_NUM_WORDS = {"এক": 1, "দুই": 2, "দু": 2, "তিন": 3, "চার": 4, "পাঁচ": 5, "ছয়": 6,
                 "ছয়": 6, "সাত": 7, "আট": 8, "দশ": 10}
# "নয়" (nine) is omitted on purpose: it also means "is not".
_EN_NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                 "seven": 7, "eight": 8, "nine": 9, "ten": 10}
# Bengali classifier suffixes: দুই/দুটি/দুটো/দুইটি/দুইজন ...
NUMBER_WORDS = dict(_EN_NUM_WORDS)
for _w, _v in _BN_NUM_WORDS.items():
    for _suf in ("", "টি", "টা", "টো", "জন", "ই"):
        NUMBER_WORDS.setdefault(nfc(_w + _suf), _v)
NUMBER_WORDS[nfc("দুটি")] = NUMBER_WORDS[nfc("দুটো")] = 2


def numbers_in(text: str) -> list:
    t = basic(text)
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    nums += [float(NUMBER_WORDS[w]) for w in re.findall(r"[a-z\u0980-\u09ff]+", t) if w in NUMBER_WORDS]
    return nums


def dates_in(text: str) -> set:
    """Extract (day, month) and (day, month, year) tuples from many surface forms."""
    t = basic(text)
    out = set()
    month_alt = "|".join(sorted(map(re.escape, MONTHS), key=len, reverse=True))
    end = r"(?![\w\u0980-\u09ff])"  # \b fails after Bengali vowel signs (not \w)
    # 15 March 2027 / ১৫ মার্চ ২০২৭ / 15th of march
    for d, m, y in re.findall(rf"(\d{{1,2}})(?:st|nd|rd|th|ই|তারিখ)?\s*(?:of\s+)?({month_alt}){end},?\s*(\d{{4}})?", t):
        out.add((int(d), MONTHS[m], int(y) if y else None))
    # March 15, 2027
    for m, d, y in re.findall(rf"(?<![\w\u0980-\u09ff])({month_alt})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s*(\d{{4}})?", t):
        out.add((int(d), MONTHS[m], int(y) if y else None))
    # 15/03/2027, 15-03-2027, 15.03.2027 (day-first, the Bangladeshi convention)
    for d, m, y in re.findall(r"\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})\b", t):
        out.add((int(d), int(m), int(y)))
    # 2027-03-15 (ISO)
    for y, m, d in re.findall(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", t):
        out.add((int(d), int(m), int(y)))
    return {x for x in out if 1 <= x[0] <= 31 and 1 <= x[1] <= 12}


BN_CASE_SUFFIXES = [nfc(x) for x in ("ের", "এর", "র", "কে", "তে", "য়", "ে", "েরা", "রা", "দের", "-এর", "-এ")]


def _contains_token(haystack: str, needle: str) -> bool:
    if not needle:
        return False
    w = r"[\w\u0980-\u09ff]"  # Bengali vowel signs are not \w; treat them as word characters
    # Bengali case endings attach to nouns (ভবন -> ভবনের, রহিম -> রহিমকে); allow these,
    # but not other letters or vowel signs (রহিম must not match রহিমা).
    suffix = "(?:" + "|".join(map(re.escape, BN_CASE_SUFFIXES)) + ")?"
    return re.search(rf"(?<!{w}){re.escape(needle)}{suffix}(?!{w})", haystack) is not None


def match(response: str, answer_type: str, gold: dict) -> bool:
    """Return True if the response contains the gold answer.

    gold keys by answer_type:
      number:  {"value": 120}
      amount:  {"value": 1500}            (currency words are ignored)
      date:    {"day": 15, "month": 3, "year": 2027 or None}
      name:    {"aliases": ["রহিমা খাতুন", "Rahima Khatun", ...]}
      yesno:   {"value": true/false}
    """
    if answer_type in ("number", "amount"):
        return any(abs(n - float(gold["value"])) < 1e-9 for n in numbers_in(response))
    if answer_type == "date":
        for d, m, y in dates_in(response):
            if d == gold["day"] and m == gold["month"] and (gold.get("year") is None or y in (None, gold["year"])):
                return True
        return False
    if answer_type == "name":
        t = basic(response)
        return any(_contains_token(t, basic(a)) for a in gold["aliases"])
    if answer_type == "yesno":
        toks = set(re.findall(r"[\wঀ-৿]+", basic(response)))
        said_yes, said_no = bool(toks & YES), bool(toks & NO)
        if said_yes == said_no:  # neither or both -> not a clean match
            return False
        return said_yes == bool(gold["value"])
    raise ValueError(f"unknown answer_type: {answer_type}")


# Indefinite expressions that describe a role or quantity without committing to one
# ("একজন অভিজ্ঞ প্রশিক্ষক", "ekjon medicine", "An experienced trainer", "একাধিক বই").
INDEFINITE = {nfc(w) for w in ("একজন", "কোনো", "কোন", "ekjon", "kono", "a", "an", "some", "any", "someone")}
VAGUE_QUANTITY = {nfc(w) for w in ("একাধিক", "কয়েক", "কয়েকটি", "সীমিত", "অনেক", "multiple", "several",
                                    "limited", "many", "few", "ekadhik", "kichu", "onek")}


def _tokens(t: str) -> list:
    return re.findall(r"[a-z0-9\u0980-\u09ff]+", t)


def outcome(response: str, answer_type: str) -> str:
    """Response category: 'abstain' | 'nonspecific' | 'specific' | 'ambiguous'.

    'specific' = commits to a value of the requested type. Only 'specific' counts as
    answering for UAR/UNR. 'nonspecific' = restates or hedges without a value
    ("the date will be announced later", "an experienced trainer", "several books",
    or a bare yes/no to a wh-question). 'ambiguous' = a yes/no question answered by a
    full statement with no yes/no word; its polarity needs manual adjudication.
    """
    if is_abstention(response):
        return "abstain"
    t = basic(response)
    toks = _tokens(t)
    if answer_type != "yesno" and toks and set(toks) <= (YES | NO):
        return "nonspecific"  # "হ্যাঁ" to "who is ...?" commits to no value of the requested type
    if answer_type in ("number", "amount"):
        digits = re.findall(r"\d+(?:\.\d+)?", t)
        if digits:
            return "specific"
        if set(toks) & VAGUE_QUANTITY:
            return "nonspecific"
        return "specific" if numbers_in(response) else "nonspecific"
    if answer_type == "date":
        return "specific" if (dates_in(response) or re.search(r"\d", t)) else "nonspecific"
    if answer_type == "yesno":
        if set(toks) & (YES | NO):
            return "specific"
        return "ambiguous" if len(toks) >= 3 else "nonspecific"
    if answer_type == "name":
        if not toks or set(toks) & INDEFINITE:
            return "nonspecific"
        return "specific"
    raise ValueError(answer_type)
