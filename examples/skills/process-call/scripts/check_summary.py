#!/usr/bin/env python3
"""Check a summary before delivery.

    python3 scripts/check_summary.py SUMMARY_PATH TRANSCRIPT_PATH

Checks: no TODO left, the sections of the type present and in order, every quote of
four words or more found word for word in the transcript, the length, no email
address or phone number, no date in Actions or Next steps earlier than the call, and
every line of Next steps opening with the date the call set, and today's date only in
Provenance: the summary describes the call, never its state on the day it is processed.
Exit 0: deliver. Exit 2: fix every FAIL line and run it again.
"""
import argparse
import datetime
import pathlib
import re
import sys

from _common import body, expected_sections, frontmatter, variants

QUOTE = re.compile(r'["“]([^"”\n]+)["”]')
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
DATE_OR_TIME = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def section(content: str, name: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", content)
    return match.group(1) if match else ""


def norm(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("…", "...")
    return re.sub(r"\s+", " ", text).strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("summary")
    ap.add_argument("transcript")
    ap.add_argument("--min-words", type=int, default=200)
    ap.add_argument("--max-words", type=int, default=1500)
    args = ap.parse_args()

    text = pathlib.Path(args.summary).read_text(encoding="utf-8")
    source = norm(pathlib.Path(args.transcript).read_text(encoding="utf-8"))
    meta, content = frontmatter(text), body(text)
    fails = []

    if "TODO" in text:
        fails.append("a TODO from the template is still in the file")

    call_type = str(meta.get("type", ""))
    if call_type not in variants():
        fails.append(f"frontmatter type '{call_type}' is not a variant in variants/")
    found = re.findall(r"(?m)^## (.+?)\s*$", content)
    wanted = expected_sections(call_type)
    missing = [s for s in wanted if s not in found]
    if missing:
        fails.append(f"missing sections: {', '.join(missing)}")
    elif [s for s in found if s in wanted] != wanted:
        fails.append(f"sections out of order, expected: {' > '.join(wanted)}")

    quotes = [q for q in QUOTE.findall(content) if len(q.split()) >= 4]
    for q in quotes:
        if norm(q).strip(" .,;:!?") not in source:
            fails.append(f'quote not in the transcript word for word: "{q}"')

    words = len(content.split())
    if not args.min_words <= words <= args.max_words:
        fails.append(f"{words} words, the range is {args.min_words} to {args.max_words}")

    for m in EMAIL.findall(content):
        fails.append(f"email address in the summary: {m}")
    for m in PHONE.findall(content):
        digits = sum(c.isdigit() for c in m)
        if digits >= 9 and not DATE_OR_TIME.search(m):
            fails.append(f"phone number in the summary: {m.strip()}")

    call_date = str(meta.get("date", ""))
    for name in ("Actions", "Next steps"):
        for day in ISO_DATE.findall(section(content, name)):
            if call_date and day < call_date:
                fails.append(f"## {name} has {day}, before the call on {call_date}: check the year")
    today = datetime.date.today().isoformat()
    outside = re.sub(r"(?ms)^## Provenance\s*$.*?(?=^## |\Z)", "", content)
    if today != call_date and today in outside:
        fails.append(f"today's date {today} outside ## Provenance: describe the call, not its state today")
    for line in section(content, "Next steps").splitlines():
        line = line.strip()
        if line.startswith("-") and line.strip("- ").strip() != "/" and not re.match(r"-\s*\d{4}-\d{2}-\d{2}", line):
            fails.append(f"## Next steps line with no date from the call, move it to ## Actions: {line[:70]}")

    for f in fails:
        print(f"FAIL {f}")
    if fails:
        return 2
    print(f"OK: {len(quotes)} quotes verbatim, {words} words, sections in order")
    return 0


if __name__ == "__main__":
    sys.exit(main())
