#!/usr/bin/env python3
"""Build the summary path from the call date and write the empty summary from the template.

    python3 scripts/new_summary.py --calls-dir calls --date 2026-11-12 --type prospect --counterpart "Larkspur Freight"

Prints two lines: the summary path, and the path where the transcript is saved.
The month in the path is the month of the call, whenever you run it.
Exit 2: unknown type, a bad date, or the file already exists.
"""
import argparse
import datetime
import pathlib
import sys

from _common import SKILL_DIR, slugify, variants


def main() -> int:
    known = variants()
    ap = argparse.ArgumentParser()
    ap.add_argument("--calls-dir", default="calls")
    ap.add_argument("--date", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--counterpart", required=True)
    ap.add_argument("--second-call", action="store_true")
    args = ap.parse_args()

    if args.type not in known:
        print(f"STOP: unknown type '{args.type}'. Known: {', '.join(known)}")
        return 2
    try:
        day = datetime.date.fromisoformat(args.date)
    except ValueError:
        print(f"STOP: '{args.date}' is not a date in YYYY-MM-DD")
        return 2

    folder = pathlib.Path(args.calls_dir) / f"{day:%Y-%m}"
    stem = f"{day.isoformat()}-{args.type}-{slugify(args.counterpart)}"
    path = folder / f"{stem}.md"
    if args.second_call:
        n = 2
        while path.exists():
            path = folder / f"{stem}-{n}.md"
            n += 1
    if path.exists():
        print(f"STOP: {path} exists. Run lookback.py, then open and extend it.")
        return 2

    sections = "".join(f"## {s}\n\nTODO see references/{args.type}.md\n\n" for s in known[args.type])
    template = (SKILL_DIR / "assets" / "summary-template.md").read_text(encoding="utf-8")
    text = (template.replace("{type}", args.type)
                    .replace("{date}", day.isoformat())
                    .replace("{counterpart}", args.counterpart)
                    .replace("{variant_sections}", sections))
    folder.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"summary: {path}")
    print(f"transcript: {path.with_suffix('')}.transcript.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
