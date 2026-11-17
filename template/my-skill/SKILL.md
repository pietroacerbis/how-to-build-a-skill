---
name: my-skill
description: "Verb the main thing for the main use case. Use when the user says 'phrase one', 'phrase two', or pastes X. Not for: Y, use other-skill."
---

# my-skill

One line: what this skill produces and where it puts it.

## When to use

- What does the user say or paste when this skill should run?

## Not for

- What looks similar but belongs to another skill or to plain Claude?

## Steps

1. Check the input. Missing or unclear: stop and ask the user, write nothing.
2. Decide the situation and read its file: `references/variant-a.md`. Delete this step if there is one situation.
3. Read the facts this run needs from `knowledge/`, never from memory.
4. Do the work. One action per step.
5. Run `python3 scripts/check.py <output>`. Exit 2: fix what it prints and run it again.
6. Deliver only on exit 0, and report the path.

## Output

- Path: `output/YYYY-MM/YYYY-MM-DD-{slug}.md`
- Template: `assets/output-template.md`

## Gotchas

- What did Claude get wrong on a real run, and what should it do instead? One line each, added after every correction.
