---
name: my-skill                        # a verb, kebab-case, the same as the folder
description: "Verb the main output for the main use case. Use when the user says 'phrase one', 'phrase two', or pastes X. Not for: Y (use other-skill)."
when_to_use: "The phrases a user types, in any language: 'phrase one', 'phrase two'."
goal: "The intent, in one line."
outcome: "output/YYYY-MM/YYYY-MM-DD-{slug}.md"
inputs:
  required: [the-input]               # missing: hard STOP
  recommended: [a-useful-input]       # missing: proceed, mark [UNAVAILABLE]
tier: personal                        # personal | shared | infrastructure
validation: verifiable                # verifiable | outcome-anchored
status: draft                         # draft | active | deprecated
mcps_used: []
feeds_into: []
version: 1
last_updated: YYYY-MM-DD
---

# my-skill

One line: what this skill produces and where it puts it.

## When to use

- What does the user say or paste when this skill should run?

## Not for

- What looks similar and belongs to another skill? Name that skill.

## How it works

### Stop 0, memory, input, variant

Read `memory.md`. Check the required input: missing, stop and ask, write nothing. Decide the situation and open its file in `variants/`. Delete the variant part if the skill has one situation.

### Stop 1, the first step

One action. Name the file it opens or the script it runs, and why.

### Stop 2, check before delivery

Run `python3 scripts/check.py <output>`. Exit 2: fix what it prints, run it again. Deliver only on exit 0.

## Output

- Path: `output/YYYY-MM/YYYY-MM-DD-{slug}.md`, in the shape of `schemas/output-format.md`.
- STOP record: when the skill stops, one line with the reason, in chat and in `memory.md`.

## References

- What real runs taught: [memory.md](memory.md)
- The situation: [variants/variant-name.md](variants/variant-name.md)
- The shape of the output: [schemas/output-format.md](schemas/output-format.md)
- The check before delivery: [scripts/check.py](scripts/check.py)
- The bar to meet: [worked-examples/example.md](worked-examples/example.md)
