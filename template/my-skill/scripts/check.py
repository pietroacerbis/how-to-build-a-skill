#!/usr/bin/env python3
"""Check the output before delivery. Exit 0 = ship it, exit 2 = fix what is printed and run again."""
import pathlib
import sys

REQUIRED_SECTIONS = ["## [Section]"]  # the sections the template promises


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check.py <output-file>")
        return 2
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    errors = [f"missing section: {s}" for s in REQUIRED_SECTIONS if s not in text]
    if "[" in text and "]" in text and "[One line" in text:
        errors.append("template placeholder left in the output")
    for e in errors:
        print(f"FAIL {e}")
    if errors:
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
