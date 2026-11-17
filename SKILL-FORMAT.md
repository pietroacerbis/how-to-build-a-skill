# SKILL-FORMAT, how a skill is written

The rules behind the [guide](README.md), in one place. The skill creator writes to them and the skill reviewer checks against them.

## 1. What a skill is

A skill is a **doer that carries the path, never the knowledge**. It orders the stops of one process, and each stop opens the one file it needs. A business fact (your ICP, your prices, your stages) lives in your knowledge base, and the skill points at it.

- **One job, one output** in a declared place.
- **Before writing a line, ask:** does it change when the company changes? The answer (which ICP, which price) is knowledge. The method (how to qualify, how to price) stays in the skill. That question keeps a skill portable.
- **A chain of skills is a flow**, written apart and free of logic: guide, step 10.

## 2. Names and variants

- **A skill is a bare verb**: `research`, `write`, `process-call`. The domain never becomes a prefix.
- **The folder is flat**: `.claude/skills/{skill-name}/SKILL.md`. Claude Code discovers one level only, so a skill inside a subfolder is invisible.
- **One verb, several situations: variants.** One file each in `variants/`, picked at stop 0, never separate skills.
- **When to split a variant:** same logic with a different input stays one file that takes the input. Different inputs, weights or output shape become separate variants.

## 3. Frontmatter

```yaml
---
name: process-call                    # kebab-case, the folder name
description: <verb first, key use case first, "Not for:">
when_to_use: <trigger phrases and example requests, any language>
goal: <one line, the intent>
outcome: <the artifact and its EXACT path>
audience: customer-facing             # only when the output is a deliverable
inputs:
  required: [transcript]              # missing: hard STOP, the gap named
  recommended: [call-date]            # missing: proceed, mark [UNAVAILABLE]
tier: personal                        # personal | shared | infrastructure
validation: verifiable                # verifiable | outcome-anchored
status: draft                         # draft | active | deprecated
mcps_used: [slack]                    # the tools it calls
feeds_into: []                        # optional, the skills that read its output
version: 1                            # optional
last_updated: YYYY-MM-DD              # optional
model: sonnet                         # optional hint
---
```

| Field | Rule |
|---|---|
| `description` | written for discovery: verb first, key use case first, an explicit `Not for:`. With `when_to_use`, at most 1,536 characters. A skill that never fires is worse than one that fires too often |
| `outcome` | the exact path the skill writes. A skill with no output home is not finished |
| `audience` | only when the output is a deliverable. `customer-facing` and `prospect` mean every fact is verified before handoff; `investor` adds every number traced to its primary source |
| `inputs` | a missing `required` input is a hard STOP with the gap named; a missing `recommended` one proceeds and writes `[UNAVAILABLE]` |
| `tier` | `personal` lives on your machine; `shared` is the team library, changed by proposal; `infrastructure` writes a system everyone uses, like the CRM, and changes only by its owner |
| `status` | moved by a person, never by a clock: `draft` by the author, `active` once it ran with passing evals, `deprecated` with its replacement named |
| `feeds_into` | documents who reads the output. It never routes |

**Where the skill runs.** Claude Code, in the terminal or an IDE, loads every field: Claude acts on `name`, `description`, `when_to_use` and `model`, and skips the rest without errors. claude.ai and the Skills API accept only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`, and refuse the upload on any other field: there the phrases of `when_to_use` move into `description`.

## 4. Folder anatomy

```
.claude/skills/{skill-name}/
├── SKILL.md              required, path-only, under 200 lines
├── evals/                required, the test cases
├── memory.md             required, learnings, STOP records, rejected patches
├── variants/             one file per variant: the folder is the set
├── schemas/              optional, the shape of the output and shared blocks
├── scripts/              optional, the deterministic parts as code
├── worked-examples/      optional, a real example of the bar
└── prompts/              optional, prompts only this skill uses
```

- **`variants/` is the set.** Nothing else lists the variants, so nothing can disagree with the folder. A skill with one variant keeps its stops in `SKILL.md` and has no folder.
- **`schemas/` holds what a variant is not:** a shape every variant fills, a block several variants open, a format the output takes.
- **`prompts/` and `schemas/` are private to the skill.** When a second skill needs the same file, it moves to the knowledge base.
- **The residency test:** delete the skill, is the file still true? No: it belongs to the skill. Yes: it is knowledge, and it moves out.
- **`worked-examples/` point at real material** and never copy knowledge in.
- **`memory.md` is read at the first stop** and written only on a correction, a STOP or a new learning. One dated line each, append-only. A lesson that recurs becomes a change to `SKILL.md`, proposed to the owner, never applied by the skill to itself.

## 5. The SKILL.md body

The body is the path: the stops in order and the file each opens. Under 200 lines, with zero copied knowledge: a longer body is carrying something that belongs in another file.

**Sections, in this order:** `## How it works` (the stops), `## Output` (the path and the STOP record), `## References` (one line per file the skill opens). When to use the skill, and when not, lives in `description` and `when_to_use` only: the body loads after Claude has picked the skill.

- **A stop opens one variant of one file**, never a whole folder.
- **Three sources or more open at once: add a compaction stop.** The skill writes a short brief scoped to this run, and the later stops work from the brief.
- **Log what was opened and what was skipped**, in the output's provenance.
- **Deterministic parts are code** in `scripts/`. A domain truth (names, stages, channels, routing targets) is never hardcoded: open the file that owns it.
- **A default at every choice.** Imperatives that explain why, no capitals for emphasis, a worked example where the format matters.

## 6. Output, and STOP

- **Every skill writes to its `outcome` path, or emits a STOP record** with its reason. Never an empty or silent output.
- **A synthesis skill declares what it does not know**, and how fresh its sources are.

## 7. Evals

- **10 to 15 realistic cases** in `evals/`, run with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). A day-0 set of 2 or 3 cases is legal, as long as it runs.
- **Rule graders certify the form**: `regex`, `file_exists`, `tool_used`, `tool_order`. Free and deterministic.
- **An LLM judge checks the substance**, one claim per grader.
- **`verifiable` skills** (formatting, processing, syncing) are judged by their evals alone. **`outcome-anchored` skills** (outreach, writing, research) pass evals on form, and their results over weeks are the real judge.

## 8. Naming

- kebab-case everywhere. `SKILL.md` in capitals, everything else lowercase.
- The skill in English, trigger phrases in `when_to_use` in any language your team types.

## 9. Checklist

| # | Check |
|---|---|
| 1 | `name` is a verb in kebab-case and equals the folder name |
| 2 | `description` opens with a verb, leads with the key use case, has `Not for:`, and with `when_to_use` stays under 1,536 characters |
| 3 | `outcome` is an exact path |
| 4 | `inputs` split into `required` and `recommended` |
| 5 | `tier`, `validation` and `status` set |
| 6 | `SKILL.md`, `evals/` and `memory.md` present |
| 7 | `SKILL.md` under 200 lines, with the three sections in order and no `## When to use` in the body |
| 8 | variants, if any, one file each in `variants/`, picked at stop 0 |
| 9 | every stop opens one file, and every file opened is in `## References` |
| 10 | no company knowledge inside the folder: the residency test passes on every file |
| 11 | every deterministic step is a script |
| 12 | a missing required input, an ambiguous case and a duplicate each end in a STOP record |
| 13 | `memory.md` is read at the first stop |
| 14 | evals: rule graders for the form, one-claim LLM judges for the substance, passing |
