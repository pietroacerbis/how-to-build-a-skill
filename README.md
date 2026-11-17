# How to build a skill

This guide takes you from a process you run by hand to a Claude skill that runs it the same way every time, in ten steps. It is the format we use at [gaja](https://trygaja.com) for the skills we run every day, with a template to copy and a complete skill to read.

- **The guide**: this page.
- **The format**: [SKILL-FORMAT.md](SKILL-FORMAT.md), every rule in one place.
- **The template**: [template/my-skill/](template/my-skill/), an empty skill with every folder.
- **The example**: [examples/skills/process-call/](examples/skills/process-call/), a skill that turns a call transcript into a summary, with variants, scripts and evals.

---

## 1. What a skill is

Anthropic's definition: *"Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Skills teach Claude how to complete specific tasks in a repeatable way."* ([What are skills](https://support.claude.com/en/articles/12512176-what-are-skills))

Claude reads the name and the description of every skill it has. When a request matches one, it loads the rest of the folder. That is why a skill costs little while it waits, and why the description decides whether it ever runs.

How it differs from what you already use:

- **MCP** connects Claude to a tool. A skill teaches Claude how to use that tool for your process.
- **Custom instructions and `CLAUDE.md`** apply to every conversation. A skill loads only for its task.

Our own definition adds one line: **a skill is a process of yours, with one job and one output in a place it names.**

## 2. Run it by hand first

A skill written before any real run has none of the corrections that make it work. So before writing anything, do the task with Claude in a normal chat, on real inputs, more than once. Correct it as you go and keep notes on:

- the steps that worked, in the order they worked
- every correction you made, and what Claude did before it
- what the input looked like, and what a good output looks like
- the facts about your company you had to tell Claude

The first three become the skill. The fourth becomes knowledge, step 3.

Then keep iterating. A skill is worth keeping when it is your process, run and corrected enough times that a run comes out right without you touching it.

## 3. The method in the skill, the knowledge outside

A skill carries the **method**: the order of the steps, what to check, when to stop, the shape of the output. It never carries the **knowledge**: your ICP, your prices, your deal stages, your tone of voice, your team, your channels.

The test is one question:

> If I changed company tomorrow, would this line change?

| Answer | It is | It lives in |
|---|---|---|
| No | method | the skill |
| Yes | knowledge | your knowledge base, a folder of markdown files the skill opens |

A skill that holds knowledge breaks quietly. Your prices change, you update the prices page, and the skill that copied them keeps quoting the old ones until a customer reads the wrong number.

Kept apart, the skill is invariant: the same `process-call` runs in any company, and what changes is the knowledge it opens. In the example, how to read a prospect call is in the skill, and the deal stages it maps the call to are in `knowledge/deal-stages.md`.

A second test for any file inside the folder: **delete the skill, is the file still true?** If yes, it is knowledge and it moves out.

## 4. The folder

```
my-skill/
├── SKILL.md            required, the path, under 200 lines
├── evals/              required, the test cases
├── memory.md           required, what real runs taught
├── variants/           one file per situation
├── schemas/            the shape of the output, shared blocks
├── scripts/            the deterministic steps, as code
├── worked-examples/    a real example of the bar to meet
└── prompts/            prompts only this skill uses
```

Three files are required, the rest only when the skill needs them. Copy [template/my-skill/](template/my-skill/) into `.claude/skills/` in your project, or `~/.claude/skills/` for every project, and rename it.

## 5. SKILL.md

### The frontmatter

Each field answers a question someone will ask about the skill. A few are read by Claude to decide when and how to run it. The others describe the skill to you, your team and your tools. Every field is in the [template](template/my-skill/SKILL.md).

| Field | Answers | Read by |
|---|---|---|
| `name` | what it is called: a verb, kebab-case, the same as the folder | Claude |
| `description` | what it does and when Claude should run it: verb first, the main use case first, and a `Not for:` line | Claude |
| `when_to_use` | the phrases a user types, in any language | Claude |
| `model` | the model to switch to while the skill runs, optional | Claude |
| `goal` | the intent, in one line | you |
| `outcome` | the exact path of what it writes | you |
| `inputs` | what it needs: `required` stops the run when missing, `recommended` lets it continue and flag the gap | you |
| `tier` | who it serves: `personal`, `shared` with the team, or `infrastructure` when it writes a system everyone uses | you |
| `validation` | how you know it works: `verifiable` by its evals, or `outcome-anchored` when only results over weeks can tell | you |
| `status` | `draft`, `active`, `deprecated`, moved by a person, never by a date | you |
| `mcps_used` | the tools it calls | you |
| `feeds_into` | the skills that read its output | you |

The `description` and `when_to_use` together stay under 1,536 characters. When in doubt, describe more: a skill that never fires is worse than one that fires too often.

**Where you run the skill decides which fields it can carry:**

| You run it in | The frontmatter |
|---|---|
| Claude Code, in the terminal or an IDE such as VS Code | every field above loads. Claude skips the ones it does not use, without errors |
| claude.ai or the Skills API | only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. Any other field stops the upload with an error, so the phrases of `when_to_use` move into `description` |

### The body

The body is a **path**: the steps Claude walks, and the files it opens on the way. Three sections, always in this order:

1. `## How it works`, the stops, numbered from 0
2. `## Output`, the exact path, and what happens when the skill stops
3. `## References`, every file the skill opens, one line each

When to use the skill, and when not, lives in the frontmatter only. Claude loads the body after it has picked the skill, so a `## When to use` section there never helps it pick: Anthropic's own skill-creator puts all of it in the description.

Keep it under 200 lines. A longer body is carrying knowledge or examples that belong in another file. While you write it:

- **Cut what Claude already knows.** For each line ask: would Claude get this wrong without it? If not, delete it.
- **Give a default, never a menu.** "Use X. For scanned files, use Y."
- **Explain the why** in one clause. Claude applies a rule better when it knows what the rule protects.

### Stopping is an outcome

Every skill writes its output where `outcome` says, or it stops and says why. A missing required input, an ambiguous case, a duplicate: each one ends the run with a one-line STOP record, never with an empty or invented output.

## 6. Variants

Some processes look the same and are not. A call with a prospect and a call with a customer follow the same spine and look for different things.

When the difference is in the input only, one file takes it as a parameter. When the fields, the checks or the output sections differ, each situation gets its own file in `variants/`:

```
variants/
├── prospect.md
├── customer.md
└── internal.md
```

- **The folder is the list.** Nothing else declares the variants, so nothing can disagree with them.
- **Stop 0 picks one** and the skill opens only that file.
- **A skill with one situation** keeps its steps in `SKILL.md` and has no `variants/`.

## 7. Scripts

If the same input always gives the same output, it is a script: dates, paths, counts, exact matches, format checks. Judgment stays in `SKILL.md`: which variant, what matters, what to write.

The signal is Claude rebuilding the same logic on every run, or getting a mechanical step wrong once in ten. The example has three scripts:

| Script | What it does | The mistake it removes |
|---|---|---|
| `lookback.py` | finds earlier summaries with the same counterpart, refuses a second summary of the same call | a lost thread, a duplicate file |
| `new_summary.py` | builds the path from the date of the call and writes the empty summary | a call from October filed in November |
| `check_summary.py` | checks every quote word for word against the transcript, the sections, the length, the dates, no email or phone number | invented quotes, a renewal dated in the wrong year, summaries three times too long, personal data |

The last one runs as a **validation loop**: check, fix what it prints, check again, deliver only when it passes.

## 8. Evals

Evals are the proof that the skill works, and that it does better than Claude without it. Claude Code runs them with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals): each case is a folder with the task as a user would type it, and the graders that score the result.

```
evals/01-prospect-discovery/
├── prompt.md
└── graders/
    ├── file.md         did the summary land at the right path?
    ├── check-ran.md    did the check script run?
    └── quotes.md       are the quotes word for word?
```

Two kinds of grader, for two kinds of question:

- **Rules** for the form: a regex on the output, a file that must exist, a script that must run. Free, and the same answer every time.
- **An LLM judge** for the substance: the quotes are real, nothing is invented, the right variant was picked. One claim per judge: in our first run a judge asked four things at once failed a correct summary.

Write 10 to 15 cases, one for each mistake you have seen. Two or three on day one are fine, as long as they run. Each case runs with and without the skill, and the difference in score is what the skill adds.

```bash
cd examples/skills/process-call
claude plugin eval . --allow-tools Bash Write Edit --scaffold --no-publish
```

One run of the 10 example cases on Sonnet takes about two minutes and costs about $1.40.

A skill whose result only shows over weeks, like an outreach sequence, is `outcome-anchored`: its evals certify the form, and the replies decide the rest.

## 9. Iterate

Every run that needs a correction teaches the skill something. `memory.md` is where it goes:

- **Read at stop 0**, so the next run starts from what the last one learned.
- **Written** when you correct a run, when the skill stops, or when a run shows something new. One dated line each.
- **A lesson that comes back** stops being a line in memory and becomes a step in `SKILL.md`, a script, or an eval case.

| What happens | What you change |
|---|---|
| you correct a run | a line in `memory.md` |
| the same correction twice | a step in `SKILL.md`, or a script |
| a new kind of mistake | an eval case that catches it |
| the skill does not fire, or fires on the wrong request | the `description` |

`status` moves to `active` when a person has seen it run with its evals passing.

A real loop from the example. The evals caught a summary writing a deadline the call never set, and a line in `memory.md` fixed it for the next runs. A later run wrote another invented deadline, and dated a renewal "on the first of March", said in November, in the current year. The same correction twice, so it became code: `check_summary.py` now fails a step dated before the call, and a next step with no date.

## 10. Chains

Some processes are several skills in a row: one produces what the next consumes. Write that order in a **chain**, also called an SOP, and keep it free of logic.

| # | Skill | Hands to the next |
|---|---|---|
| 1 | `list-build` | a list of accounts |
| 2 | `icp-qualifier` | the accounts that fit your ICP |
| 3 | `research` | a brief per account |
| 4 | `outreach` | the first message |

- **The chain orders the skills, each skill orders its stops.** A rule written in the chain is a rule the skill does not know.
- **Each step names its skip condition**, and a skip is recorded.
- **Write it after you walked it**, like a skill: a chain you only imagined has the same problem as a skill you only imagined.

---

## Before you ship

Run your skill against [SKILL-FORMAT.md](SKILL-FORMAT.md), section 9: one checklist for the frontmatter, the folder, the body and the evals.

<!-- CTA -->
---

## Want skills built on your own process?

The skill is the method. What makes it work in your company is the knowledge it opens: your ICP, your stages, your objections, your voice.

We build both from your calls, your CRM and your team, on your business. Get in touch.

- Pietro Acerbis, pietro@trygaja.com, [LinkedIn](https://www.linkedin.com/in/pietroacerbis-prospeiq/)
- [trygaja.com](https://trygaja.com)

MIT licence.
