# Romanized Bengali (RBN / CMR) Convention — draft v0.1 (2026-10-23)

**Status:** a provisional convention for open question Q6, drafted by the AI agent. **The author may change any rule during the variant review.** Changes are logged in `00_admin/decision_log.md`.

## Principle
Write romanized Bengali the way Bangladeshi users type in chat and search: phonetic, plain ASCII, no diacritics, lowercase, and spellings that are common in chat. Avoid scholarly transliteration (ISO 15919) and Avro keyboard codes.

## Rules for the canonical form
| Bengali | Roman | Example |
|---|---|---|
| inherent অ (spoken /ɔ/) | o | কত → koto, কবে → kobe |
| আ / া | a | টাকা → taka |
| ই ঈ / ি ী | i | দিন → din |
| উ ঊ / ু ূ | u | শুরু → shuru |
| এ / ে | e | কেন → ken; spoken /æ/ → e (দেখা → dekha) |
| ও / ো | o | কোন → kon |
| ঐ / ৈ, ঔ / ৌ | oi, ou | কৈ → koi |
| শ ষ | sh | শেষ → shesh |
| স | s (sh where it is spoken /ʃ/ and commonly written that way) | সময় → shomoy |
| চ ছ | ch | ছুটি → chuti |
| জ য | j | জমা → joma |
| ট ত | t | তারিখ → tarikh |
| ঠ থ | th | থাকবে → thakbe |
| ড দ | d | দিতে → dite |
| ঢ ধ | dh | ধরন → dhoron |
| ড় ঢ় র | r | বড় → boro |
| ভ | v (chat convention) | ভর্তি → vorti |
| ফ | f | ফি → fi (the English word "fee" is CM, not RBN) |
| ব | b | বই → boi |
| য় (as a semivowel) | y, or dropped between vowels | নয় → noy, দেওয়া → dewa |
| ং ঙ | ng | বাংলা → bangla |
| ঁ (chandrabindu) | dropped | চাঁদা → chada |
| ৎ | t | হঠাৎ → hothat |
| ্য (ya-phala) | doubles the consonant or is dropped | সত্য → shotto |
| ক্ষ | kkh / kh | পরীক্ষা → porikkha |
| Bengali digits | ASCII digits | ১৫ → 15 |

## Code-mixed renderings
- **CM** (Bengali script + English): the matrix language is Bengali in Bengali script. Common English content words such as fee, form, date, deadline, office, apply, submit, online, last date and ticket are written in **Latin script**. Example: `Application fee কত টাকা?`
- **CMR** (Roman script + English): the same insertions, with the Bengali matrix romanized by the rules above. Example: `application fee koto taka?`
- Mixing target: 1–3 English content words per question. Function words and question words stay Bengali (koto, kobe, ki, ke, kothay).

## Not canonical (robustness variants only)
Alternative spellings users also type (for example `kobe/kbe`, `taka/tk`, `vorti/bhorti`, `ase/ache`) are generated later as a robustness check (plan §7). They are kept out of the canonical items.
