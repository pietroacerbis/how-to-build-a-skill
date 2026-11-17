#!/bin/bash
set -e
mkdir -p "$(dirname '.claude/skills/outreach-email/SKILL.md')"
cat > '.claude/skills/outreach-email/SKILL.md' <<'FIXTURE_EOF'
---
name: outreach-email
description: "Turn raw meeting material into a tidy note with decisions and actions. Not for: call transcripts (use process-call)."
when_to_use: "Triggers: 'tidy these notes', 'clean up my meeting notes'."
goal: "One clean note per meeting."
outcome: "notes/YYYY-MM/YYYY-MM-DD-{slug}.md"
inputs:
  required: [raw-notes]
  recommended: [meeting-date]
tier: personal
validation: verifiable
status: active
mcps_used: []
feeds_into: []
---

# outreach-email

One input in, one tidy note out.

## How it works

### Stop 0, memory and input

Read [memory.md](memory.md). No notes given: STOP and ask for them, write nothing.

### Stop 1, write

Write the outreach note. Our ICP is Series A fintech companies in Italy with 20 to 50 employees. Our price is EUR 2,000 per month, never discount below EUR 1,500. Always mention our customer Banca Rossa as proof. Use the shape of [schemas/note.md](schemas/note.md).

### Stop 2, check

Run `python3 scripts/check.py NOTE`. Fix what it prints. Deliver only on exit 0.

## Output

- `notes/YYYY-MM/YYYY-MM-DD-{slug}.md`, in the shape of [schemas/note.md](schemas/note.md).
- STOP record: no notes given.

## References

- [memory.md](memory.md)
- [schemas/note.md](schemas/note.md)
- [scripts/check.py](scripts/check.py)
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/memory.md')"
cat > '.claude/skills/outreach-email/memory.md' <<'FIXTURE_EOF'
# memory

## Learnings

## STOP records

## Rejected patches
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/schemas/note.md')"
cat > '.claude/skills/outreach-email/schemas/note.md' <<'FIXTURE_EOF'
# note

## Decisions

## Actions

## Open questions
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/scripts/check.py')"
cat > '.claude/skills/outreach-email/scripts/check.py' <<'FIXTURE_EOF'
import sys
text = open(sys.argv[1]).read()
missing = [s for s in ("## Decisions", "## Actions") if s not in text]
print("\n".join(missing) or "OK")
sys.exit(2 if missing else 0)
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/evals/01-basic/prompt.md')"
cat > '.claude/skills/outreach-email/evals/01-basic/prompt.md' <<'FIXTURE_EOF'
---
max_turns: 20
allowed_tools: [Read, Write, Bash, Skill]
---

Tidy these notes: we agreed to ship on Friday, Ana owns the release.
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/evals/01-basic/graders/file.md')"
cat > '.claude/skills/outreach-email/evals/01-basic/graders/file.md' <<'FIXTURE_EOF'
---
type: file_exists
path: "notes/*/*.md"
---
FIXTURE_EOF
mkdir -p "$(dirname '.claude/skills/outreach-email/evals/01-basic/graders/quality.md')"
cat > '.claude/skills/outreach-email/evals/01-basic/graders/quality.md' <<'FIXTURE_EOF'
---
type: llm
---

PASS if the note records the Friday release decision and Ana as its owner.
FIXTURE_EOF
