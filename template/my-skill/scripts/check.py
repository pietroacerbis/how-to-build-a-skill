#!/usr/bin/env python3
"""Check the output before delivery. Exit 0: deliver. Exit 2: fix every FAIL line and run again."""
import pathlib
import sys

REQUIRED_SECTIONS = ["## Next steps", "## Provenance"]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check.py <output-file>")
        return 2
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    fails = [f"missing section: {s}" for s in REQUIRED_SECTIONS if s not in text]
    if "TODO" in text:
        fails.append("a TODO from the template is still in the file")
    for f in fails:
        print(f"FAIL {f}")
    if fails:
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
