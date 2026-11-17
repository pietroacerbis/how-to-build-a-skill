#!/usr/bin/env python3
"""Find earlier summaries with the same counterpart, and refuse a duplicate of this call.

    python3 scripts/lookback.py --calls-dir calls --date 2026-11-12 --counterpart "Larkspur Freight"

Exit 0: prints the earlier summaries, newest first. Zero is a result, and it is printed.
Exit 2: a summary of this counterpart already exists on this date. Open it and extend it.
        If it really is a second call that day, rerun with --second-call.
"""
import argparse
import pathlib
import sys

from _common import SKILL_DIR, frontmatter, slugify


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calls-dir", default="calls")
    ap.add_argument("--date", required=True, help="the date of the call, YYYY-MM-DD")
    ap.add_argument("--counterpart", required=True)
    ap.add_argument("--second-call", action="store_true")
    args = ap.parse_args()
    if SKILL_DIR in pathlib.Path(args.calls_dir).resolve().parents or pathlib.Path(args.calls_dir).resolve() == SKILL_DIR:
        print(f"STOP: --calls-dir {args.calls_dir} resolves inside the skill folder. Run the script from the project root, never after a cd into the skill.")
        return 2

    slug = slugify(args.counterpart)
    hits = []
    for path in pathlib.Path(args.calls_dir).glob("*/*.md"):
        if path.name.endswith(".transcript.md"):
            continue
        meta = frontmatter(path.read_text(encoding="utf-8"))
        if slugify(str(meta.get("counterpart", ""))) == slug or path.stem.endswith(f"-{slug}"):
            hits.append((str(meta.get("date", path.name[:10])), path))
    hits.sort(reverse=True)

    same_day = [p for d, p in hits if d == args.date]
    if same_day and not args.second_call:
        print(f"STOP: {same_day[0]} already summarizes a call with {args.counterpart} on {args.date}.")
        print("Open it and add what is new. A second call that day: rerun with --second-call.")
        return 2

    earlier = [(d, p) for d, p in hits if d < args.date]
    print(f"lookback: {len(earlier)} earlier summaries with {args.counterpart}")
    for d, p in earlier:
        print(f"  {d}  {p}")
    if not earlier:
        print("  first contact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
