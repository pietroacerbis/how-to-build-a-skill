---
name: create-skill
description: "Create a Claude skill. Use it for every request to make, build, write or turn something into a skill or a SKILL.md, even when the user has not run the process yet: stop 0 checks that first. It collects what the manual runs taught, interviews you on what is missing, keeps company knowledge out of the skill, and writes the folder on the How to build a skill format with its memory, its first eval cases and a format check. Not for: reviewing an existing skill (use review-skill), editing one line of a skill."
when_to_use: "When a process you repeat with Claude is ready to become a skill. Triggers: 'make this a skill', 'create a skill for X', 'turn this process into a skill', 'build a skill from this chat', 'crea una skill', 'trasforma questo processo in una skill'."
goal: "Turn a process you already run into a skill that runs it the same way every time."
outcome: ".claude/skills/{name}/, plus knowledge/{topic}.md when the runs held company knowledge"
inputs:
  required: [manual-runs]
  recommended: [skill-name, skill-folder]
tier: personal
validation: verifiable
status: active
mcps_used: []
feeds_into: [review-skill]
version: 1
last_updated: 2026-11-17
---

# create-skill

A skill is written from runs that already happened. This skill collects what those runs taught, asks only what they leave open, and writes the folder from the template of this plugin.

## How it works

### Stop 0, memory and the gate

Read [memory.md](memory.md).

Then the gate: **has the user run this process with Claude, by hand, at least twice?** Ask when the request does not say.

- No: STOP. Tell them to run it by hand two or three times first, correcting Claude as they go, and to come back with that chat or their notes. Step 2 of the guide: https://github.com/pietroacerbis/how-to-build-a-skill#2-run-it-by-hand-first. Write nothing.
- Yes: go on.

### Stop 1, the material

Read the material of the manual runs: this chat, a pasted transcript, or the user's notes. None at hand: ask for it. Extract four lists:

| From the runs | Becomes |
|---|---|
| the steps that worked, in order | the stops |
| every correction the user made | lines in `memory.md`, and a step when it came back |
| what went in and what came out | `inputs`, `outcome` and the output template in `schemas/` |
| the facts the user had to give Claude | knowledge, stop 3 |

### Stop 2, the interview

Ask what the material leaves open, one question at a time, with AskUserQuestion and a recommended answer first. The questions and their defaults are in [schemas/interview.md](schemas/interview.md). Skip every question the material or the request already answers.

### Stop 3, method and knowledge

For every line of the future skill, ask: **would it change if the company changed?**

- Yes: it is knowledge. Write it to `knowledge/{topic}.md` at the project root, one file per topic, and have the stop that needs it open that file.
- No: it is method, and it stays in the skill.

### Stop 4, write the folder

Write the folder to `.claude/skills/{name}/`, or to the folder the user named. Installed as a plugin, start from a copy of `${CLAUDE_PLUGIN_ROOT}/template/my-skill/`; without it, write the same tree from this list. Every item is required unless it says otherwise:

- **Frontmatter**: every field, `status: draft`.
- **Stops** numbered from 0, stop 0 reading `memory.md`, one action each, a STOP for a missing required input.
- **Variants**: one file per situation in `variants/` when the interview found two or more. Otherwise delete the folder.
- **Scripts**: every step where the same input always gives the same output (dates, paths, counts, sums, format checks) is a script in `scripts/`, with a check before delivery.
- **`memory.md`**: the corrections from the manual runs, one dated line each.
- **`evals/`**: two or three cases from the manual runs, in the layout `claude plugin eval` reads: one folder per case, `evals/01-{slug}/prompt.md` with the task as a user would type it and its input pasted in, and `evals/01-{slug}/graders/` with a `file_exists` or `regex` grader on the output and an `llm` grader on the mistake the runs corrected.
- Delete the template folders the skill does not use.
- **Knowledge stays out**: no fact written to `knowledge/` appears in any file of the skill. The stop names the knowledge file, never its content.

### Stop 5, check

Run `review-skill` on the new folder with the `full` profile, and fix every format `FAIL` it reports. Hand over only when it passes. `review-skill` not installed: check by hand that `SKILL.md`, `memory.md` and `evals/` with two cases or more exist, and tell the user to run `review-skill` before the first real use.

### Stop 6, hand over

In chat: the folder tree, the knowledge files written, the `WARN` lines left, and the next step: run it on a real input, then add eval cases until there are ten.

## Output

- `.claude/skills/{name}/`, or the folder the user named, on the template of this plugin, `status: draft`.
- `knowledge/{topic}.md` for each body of company facts the runs used.
- STOP record: no manual run behind the process, or no material to read. Nothing is written, the reason goes to the user in one line and to [memory.md](memory.md).

## References

- What earlier runs taught, read at stop 0: [memory.md](memory.md)
- The interview, its questions and defaults: [schemas/interview.md](schemas/interview.md)
- The template copied at stop 4, every folder of the format: `${CLAUDE_PLUGIN_ROOT}/template/my-skill/`
- The check at stop 5: the `review-skill` skill of this plugin
