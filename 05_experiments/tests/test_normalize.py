import pytest

from src.normalize import basic, dates_in, is_abstention, match, numbers_in


@pytest.mark.parametrize("text,expected", [
    ("১৫০০ টাকা", [1500.0]),
    ("Tk 1,500", [1500.0]),
    ("৳১,৫০,০০০", [150000.0]),
    ("fee is 1500 taka.", [1500.0]),
    ("২.৫ কিমি", [2.5]),
])
def test_numbers(text, expected):
    assert numbers_in(text) == expected


@pytest.mark.parametrize("text", [
    "১৫ মার্চ ২০২৭", "15 March 2027", "March 15, 2027", "15/03/2027",
    "2027-03-15", "১৫/০৩/২০২৭", "15th of march", "১৫ই মার্চ",
])
def test_dates_match_same_day(text):
    assert match(text, "date", {"day": 15, "month": 3, "year": 2027})


def test_date_wrong_day_or_year():
    assert not match("16 March 2027", "date", {"day": 15, "month": 3, "year": 2027})
    assert not match("15 March 2026", "date", {"day": 15, "month": 3, "year": 2027})
    assert dates_in("31/02/2027") == {(31, 2, 2027)}  # not calendar-validated; only ranges
    assert dates_in("45/13/2027") == set()


@pytest.mark.parametrize("text,ok", [
    ("The fee is 1500 taka.", True),
    ("ফি ১৫০০ টাকা।", True),
    ("ফি ১৫০ টাকা।", False),
    ("15000 taka", False),
])
def test_amount(text, ok):
    assert match(text, "amount", {"value": 1500}) is ok


@pytest.mark.parametrize("text,ok", [
    ("রহিমা খাতুন", True),
    ("The officer is Rahima Khatun.", True),
    ("rahima khatun ma'am", True),
    ("Rahim Khan", False),
])
def test_name(text, ok):
    assert match(text, "name", {"aliases": ["রহিমা খাতুন", "Rahima Khatun"]}) is ok


def test_name_requires_token_boundary():
    assert not match("Karima", "name", {"aliases": ["Rima"]})


@pytest.mark.parametrize("text,gold,ok", [
    ("Yes.", True, True), ("হ্যাঁ, পার্কিং আছে।", True, True), ("ha, ache", True, True),
    ("No.", True, False), ("না", False, True), ("yes and no", True, False), ("Maybe", True, False),
])
def test_yesno(text, gold, ok):
    assert match(text, "yesno", {"value": gold}) is ok


@pytest.mark.parametrize("text", [
    "NOT_ANSWERABLE", "not answerable", "The passage does not mention the fee.",
    "নোটিশে ফি-এর কথা উল্লেখ নেই।", "এই তথ্য দেওয়া নেই", "I don't know", "Notice does not say.",
])
def test_abstention_detected(text):
    assert is_abstention(text)


@pytest.mark.parametrize("text", ["1500 taka", "১৫ মার্চ", "Yes", "রহিমা খাতুন"])
def test_answers_not_abstention(text):
    assert not is_abstention(text)


def test_basic_strips_zero_width_and_punctuation():
    assert basic("রহিমা‌খাতুন।") == "রহিমাখাতুন"


@pytest.mark.parametrize("text,value", [
    ("দুই কপি ছবি", 2), ("দুটি", 2), ("two copies", 2), ("তিনজন", 3), ("৪টি বই", 4),
])
def test_number_words(text, value):
    assert match(text, "number", {"value": value})


def test_number_words_do_not_fire_inside_other_words():
    # "একজন" (one person) is a number word; "একসাথে" (together) is not
    assert numbers_in("একসাথে") == []


@pytest.mark.parametrize("text", ["\u09af\u09bc", "\u09df"])  # decomposed and precomposed "য়"
def test_months_with_ya_match_in_any_unicode_form(text):
    assert match(f"১২ ফেব্রু{text}ারি ২০২৭", "date", {"day": 12, "month": 2, "year": 2027})


def test_bengali_name_boundary_respects_vowel_signs():
    assert not match("রহিমা খাতুন", "name", {"aliases": ["রহিম"]})
    assert match("রহিম সাহেব", "name", {"aliases": ["রহিম"]})


@pytest.mark.parametrize("text,ok", [
    ("নতুন ভবনের হলরুমে", True), ("রহিমের বাড়ি", True), ("রহিমকে", True), ("রহিমা", False), ("রহিমউদ্দিন", False),
])
def test_bengali_case_suffixes(text, ok):
    assert match(text, "name", {"aliases": ["নতুন ভবন", "রহিম"]}) is ok


@pytest.mark.parametrize("text,atype,cat", [
    ("NOT_ANSWERABLE", "date", "abstain"),
    ("তারিখ পরে জানানো হবে।", "date", "nonspecific"),
    ("১২ ফেব্রুয়ারি ২০২৭", "date", "specific"),
    ("সীমিত সংখ্যক", "number", "nonspecific"),
    ("A limited number of visitors.", "number", "nonspecific"),
    ("সপ্তাহে তিন দিন", "number", "specific"),       # a committed (wrong) value
    ("একজন অভিজ্ঞ প্রশিক্ষক।", "name", "nonspecific"),
    ("An experienced trainer.", "name", "nonspecific"),
    ("মাহফুজ করিম", "name", "specific"),
    ("অবসরপ্রাপ্ত কর্মচারীরা", "name", "specific"),  # commits to an (unsupported) referent
    ("না", "yesno", "specific"),
    ("কলেজ পর্যায়ের শিক্ষার্থীরা দলগতভাবে প্রকল্প জমা দিতে পারবে।", "yesno", "ambiguous"),
    ("শুক্রবার একজন মেডিসিন বিশেষজ্ঞ রোগী দেখেন।", "name", "nonspecific"),
    ("ekjon medicine", "name", "nonspecific"),
    ("একজন সাধারণ সদস্য একসাথে একাধিক বই ধার নিতে পারবেন।", "number", "nonspecific"),
    ("one", "number", "specific"),
    ("2", "number", "specific"),
    ("হ্যাঁ", "name", "nonspecific"),
    ("obsorproapta kormochari", "name", "specific"),
])
def test_outcome_categories(text, atype, cat):
    from src.normalize import outcome
    assert outcome(text, atype) == cat
