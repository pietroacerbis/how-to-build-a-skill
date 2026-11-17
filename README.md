# How to build a skill

Ten steps from a process you run by hand to a Claude skill that runs it the same way every time. Built on the [Agent Skills standard](https://agentskills.io/specification) and its [best practices](https://agentskills.io/skill-creation/best-practices), plus what we learned running our own skills every day at [gaja](https://trygaja.com).

| What | Where |
|---|---|
| The guide | this page |
| The rules as a checklist | [SKILL-FORMAT.md](SKILL-FORMAT.md) |
| An empty skill to copy | [template/my-skill/](template/my-skill/) |
| A complete skill: variants, scripts, evals | [examples/skills/process-call/](examples/skills/process-call/) |

---

## 1. What a skill is

A folder of instructions, scripts and resources that Claude loads when a task needs it ([Anthropic](https://support.claude.com/en/articles/12512176-what-are-skills)).

| Claude loads | When | Budget |
|---|---|---|
| `name` and `description` | always, for every installed skill | about 100 tokens |
| the `SKILL.md` body | when a request matches the description | under 500 lines, 5,000 tokens |
| `scripts/`, `references/`, `assets/` | when the body says to | as needed |

| Skill vs | The difference |
|---|---|
| Project knowledge | loads in every chat of the project. A skill loads only for its task |
| MCP | gives Claude access to a tool. A skill teaches Claude your way of using it |
| `CLAUDE.md`, custom instructions | apply to every conversation. A skill applies to one task |

**Write one when** you run the same process again and again and want the same result every time.

## 2. Run it by hand first

Do the task with Claude in a normal chat, on real inputs, two or three times. Correct it as you go. Then write down:

| What you noted | What it becomes |
|---|---|
| the steps that worked, in order | the steps in `SKILL.md` |
| every correction you made | the `## Gotchas` section |
| what the input and the output looked like | the output template in `assets/` |
| the facts you had to tell Claude | knowledge files, step 3 |

- A skill written before any run has none of these, and the first real input finds the mistakes for you.
- A skill is worth keeping when it is your process, run and corrected enough times that a run comes out right without you touching it.

## 3. Method in the skill, facts outside

Ask of every line: **if I changed company tomorrow, would this line change?**

| Answer | It is | It lives in | Examples |
|---|---|---|---|
| No | method | the skill | the order of the steps, what to check, when to stop, the shape of the output |
| Yes | knowledge | `knowledge/` at your project root, opened by the skill | your ICP, prices, tone of voice, deal stages, team names, Slack channels |

- When your prices change you edit one file. A skill that copied them keeps quoting the old ones.
- The same skill runs in any company: point it at other files, keep the skill.

## 4. The folder

```
my-skill/
├── SKILL.md       required: frontmatter and instructions
├── references/    read on a condition: variants, detailed docs
├── assets/        templates for the output
├── scripts/       the deterministic steps, as code
└── evals/         test cases for claude plugin eval
```

| Install it in | Available |
|---|---|
| `.claude/skills/my-skill/` | in that project |
| `~/.claude/skills/my-skill/` | in every project |

Start from [template/my-skill/](template/my-skill/).

## 5. SKILL.md

**Frontmatter**

| Field | Required | Rule |
|---|---|---|
| `name` | yes | max 64 characters, lowercase letters, numbers and hyphens, the same as the folder |
| `description` | yes | max 1,024 characters: what it does and when to use it. It decides when the skill fires |
| `license`, `compatibility`, `metadata`, `allowed-tools` | no | see the [specification](https://agentskills.io/specification) |

A description that fires when it should:
- opens with the verb and the main use case
- lists the words a user types: "process this call", "summarize this meeting"
- says what it is not for

**Body**

| Section | What goes in |
|---|---|
| `## When to use` / `## Not for` | the boundaries |
| `## Steps` | numbered, one action each, the script to run named in the step |
| `## Output` | the exact path, the template in `assets/` |
| `## Gotchas` | the corrections from your runs |

- **Cut what Claude already knows.** For each line: would Claude get this wrong without it? If not, delete it.
- **A default, never a menu.** "Use X. For scanned files, use Y."
- **Tell it when to read each file.** "Read `references/prospect.md` when the call is with a prospect."

## 6. Variants

One process, several situations: one file per situation in `references/`, chosen at the first step.

```markdown
1. Decide the type of call: prospect, customer or internal.
2. Read the file of that type in references/ and follow it.
```

| Same file | Separate files |
|---|---|
| same steps, a different input | different fields, different checks, different output sections |

Example: [process-call](examples/skills/process-call/) has three, `prospect`, `customer`, `internal`.

## 7. Scripts

**If the same input always gives the same output, it is a script**: dates, paths, counts, exact matches, format checks. Judgment stays in `SKILL.md`: which variant, what matters, what to write.

| Script in the example | What it does | The mistake it removes |
|---|---|---|
| `lookback.py` | finds earlier summaries with the same counterpart, refuses a second summary of the same call | a lost thread, a duplicate file |
| `new_summary.py` | builds the path from the call date and writes the empty summary from the template | the wrong month in the path, sections out of order |
| `check_summary.py` | checks every quote word for word against the transcript, the sections, the length, no emails or phone numbers | invented quotes, 4,000-word summaries, personal data |

**The validation loop**: run the check, fix, run it again, deliver only on exit 0.

When to write one: Claude rebuilds the same logic on every run.

## 8. Evals

The proof that the skill works, and that it beats Claude without it. Claude Code runs them with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals).

```
evals/prospect-discovery/
├── prompt.md          the task, as a user would type it
└── graders/
    ├── file.md        file_exists, free
    ├── sections.md    regex on the file, free
    └── quotes.md      llm judge, paid
```

| Grader | Checks | Cost |
|---|---|---|
| `regex` | text in the reply, the trace or a file | free |
| `file_exists` | the output landed where it should | free |
| `tool_used`, `tool_order` | the script ran, in the right order | free |
| `llm` | what a regex cannot see: quotes are real, nothing invented, the right variant | paid, Haiku by default |

- Regex for the form, the LLM judge for the substance.
- One claim per LLM grader. A judge asked four things at once voted PASS, FAIL, FAIL on a correct summary in our first run; split into one claim each, it stopped.
- 10 to 15 cases, one for each mistake you have seen.
- Each case runs with and without the skill. The difference in score is what the skill adds.

```bash
cd examples/skills/process-call
claude plugin eval . --allow-tools Bash Write Edit --scaffold --no-publish
```

One run of the 10 example cases on Sonnet: about 100 seconds and $1.20.

## 9. Iterate

| What happens | What you do |
|---|---|
| you correct a run | add a line to `## Gotchas` |
| the same correction comes back | make it a step, or a script |
| a new kind of mistake | add an eval case that catches it |
| the skill does not fire, or fires on the wrong request | rewrite the description |

A real loop from this repo: the first full run of the evals caught the example writing a deadline the call never set. One Gotcha line fixed it, and the case passed 3 runs out of 3.

## 10. Chains

When skills always run in a row, write the order in one file and keep the logic in the skills.

```markdown
# After a call
1. process-call: the summary in calls/
2. update-crm: the deal record           (your skill, not in this repo)
3. follow-up-email: a draft to the client (your skill, not in this repo)
```

- The chain holds the order, each skill holds its steps.
- Example: [examples/sops/after-a-call.md](examples/sops/after-a-call.md).

---

## Before you ship

Run your skill through [SKILL-FORMAT.md](SKILL-FORMAT.md): 20 checks, format and security.

<!-- CTA -->
---

## Want skills built on your own process?

A skill is as good as the process and the knowledge it runs on. At gaja we build both from your calls, your CRM and your team: the knowledge your skills open, and the skills that run your GTM.

- Pietro Acerbis, pietro@trygaja.com, [LinkedIn](https://www.linkedin.com/in/pietroacerbis-prospeiq/)
- [trygaja.com](https://trygaja.com)

MIT licence.
