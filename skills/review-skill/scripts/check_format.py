#!/usr/bin/env python3
"""Check a skill folder against SKILL-FORMAT.md. Reads files, never runs them.

    python3 check_format.py PATH/TO/SKILL --profile full    a skill on our format
    python3 check_format.py PATH/TO/SKILL --profile spec    a third-party skill, Agent Skills spec only

Prints one line per check: FAIL, WARN or PASS. Exit 0: no FAIL. Exit 2: at least one FAIL.
Standard library only.
"""
import argparse
import pathlib
import re
import sys

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BODY_SECTIONS = ["## How it works", "## Output", "## References"]
PRIVATE_DIRS = ["variants", "schemas", "scripts", "worked-examples", "prompts"]


def parse_frontmatter(text: str):
    """A flat reader for SKILL.md frontmatter: scalars, [lists], and one level of nesting."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None, text
    data, parent = {}, None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = re.sub(r"\s+#.*$", "", raw) if not re.search(r"[\"'][^\"']*#", raw) else raw
        indented = raw.startswith((" ", "\t"))
        if ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        value = value.strip().strip('"').strip("'")
        if indented and parent:
            data[parent] = data[parent] if isinstance(data[parent], dict) else {}
            data[parent][key] = value
            continue
        data[key] = value
        parent = key if value == "" else None
    return data, text[match.end():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("--profile", choices=["full", "spec"], default="full")
    args = ap.parse_args()

    root = pathlib.Path(args.skill_dir).resolve()
    results = []

    def check(ok: bool, label: str, level: str = "FAIL"):
        results.append(("PASS" if ok else level, label))

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print(f"FAIL no SKILL.md in {root}")
        return 2
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    if meta is None:
        print("FAIL SKILL.md has no frontmatter between --- lines")
        return 2

    name = meta.get("name", "")
    description = meta.get("description", "")
    when = meta.get("when_to_use", "")
    lines = text.count("\n") + 1

    # The spec, for every skill
    check(bool(NAME.match(name)) and len(name) <= 64, f"name '{name}' is kebab-case, at most 64 characters")
    check(name == root.name, f"name '{name}' equals the folder name '{root.name}'")
    check(0 < len(description) <= 1024, f"description present, {len(description)} characters of at most 1,024")
    extra = sorted(set(meta) - SPEC_FIELDS)
    check(not extra, f"fields outside the spec, refused by a claude.ai upload: {', '.join(extra) or 'none'}", "WARN")

    if args.profile == "spec":
        check(lines <= 500, f"SKILL.md {lines} lines, at most 500")
    else:
        check(len(description) + len(str(when)) <= 1536, f"description and when_to_use {len(description) + len(str(when))} characters, at most 1,536")
        check("not for" in description.lower(), "description carries a 'Not for:' line")
        check(bool(when), "when_to_use present", "WARN")
        check(bool(meta.get("outcome")), "outcome names the path the skill writes")
        inputs = meta.get("inputs")
        check(isinstance(inputs, dict) and "required" in inputs and "recommended" in inputs, "inputs split into required and recommended")
        check(meta.get("tier") in {"personal", "shared", "infrastructure"}, f"tier '{meta.get('tier', '')}' is personal, shared or infrastructure")
        check(meta.get("validation") in {"verifiable", "outcome-anchored"}, f"validation '{meta.get('validation', '')}' is verifiable or outcome-anchored")
        check(meta.get("status") in {"draft", "active", "deprecated"}, f"status '{meta.get('status', '')}' is draft, active or deprecated")

        check(lines < 200, f"SKILL.md {lines} lines, under 200")
        found = [s for s in BODY_SECTIONS if re.search(rf"(?m)^{re.escape(s)}\s*$", body)]
        positions = [body.find(s) for s in found]
        check(found == BODY_SECTIONS and positions == sorted(positions), "body sections How it works, Output, References, in order")
        check(not re.search(r"(?m)^## (When to use|Not for)\s*$", body), "no When to use or Not for section in the body: they live in the frontmatter")
        check((root / "memory.md").is_file(), "memory.md present")
        first_stop = re.split(r"(?m)^### Stop 1\b", body)[0]
        check("memory.md" in first_stop, "memory.md read at the first stop", "WARN")
        check("STOP" in body, "the body says when the skill stops", "WARN")

        cases = [d for d in (root / "evals").glob("*") if d.is_dir() and ((d / "prompt.md").is_file() or (d / "case.yaml").is_file())] if (root / "evals").is_dir() else []
        check(bool(cases), f"evals/ holds {len(cases)} cases")
        check(len(cases) >= 10, f"{len(cases)} eval cases, the target is 10 to 15", "WARN")
        graders = [g.read_text(encoding="utf-8", errors="replace") for c in cases for g in (c / "graders").glob("*.md")] if cases else []
        llm = sum(bool(re.search(r"(?m)^type:\s*llm\b", g)) for g in graders)
        check(llm > 0 and len(graders) > llm, f"graders: {len(graders) - llm} rule, {llm} LLM judge", "WARN")

        named = body + "".join(p.read_text(encoding="utf-8", errors="replace") for p in (root / "variants").glob("*.md")) if (root / "variants").is_dir() else body
        for folder in PRIVATE_DIRS:
            for path in sorted((root / folder).rglob("*")) if (root / folder).is_dir() else []:
                if path.is_file() and not path.name.startswith(("_", ".")) and path.suffix not in {".pyc"}:
                    rel = path.relative_to(root).as_posix()
                    parents = [p.as_posix() + "/" for p in path.relative_to(root).parents if p.as_posix() not in (".", folder)]
                    check(rel in named or path.name in named or any(d in named for d in parents), f"{rel} is named in SKILL.md or a variant", "WARN")

    for ref in sorted(set(re.findall(r"\]\(([^)#:]+)\)", body))):
        if not ref.startswith(("http", "mailto")):
            check((root / ref).exists(), f"linked file {ref} exists")

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    for level, label in results:
        print(f"{level} {label}")
    print(f"profile {args.profile}: {len(results) - len(fails) - len(warns)} pass, {len(warns)} warn, {len(fails)} fail")
    return 2 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
