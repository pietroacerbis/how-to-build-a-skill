---
name: process-call
description: "Process a call transcript end to end: resolve the type of call, reload the earlier thread, extract what that type declares with verbatim quotes, write the dated summary to calls/, and post a short update to Slack. Handles prospect, customer and internal calls. Not for: preparing a call that has not happened yet (plain chat), material that is not a conversation, two calls in one run."
when_to_use: "After any conversation that left a transcript or notes. Triggers: 'process this call', 'summarize this meeting', 'log my call with X', 'processa questa call', 'ho fatto una call con X', or pasting a transcript or raw meeting notes."
goal: "Turn one conversation into a summary somebody can act on, plus the update the team reads."
outcome: "calls/{YYYY-MM}/YYYY-MM-DD-{type}-{slug}.md, plus the Slack update"
inputs:
  required: [transcript]
  recommended: [call-date, counterpart]
tier: personal
validation: verifiable
status: active
mcps_used: [slack]
feeds_into: []
version: 1
last_updated: 2026-11-17
model: sonnet
---

# process-call

One skill for every call. The **type** is resolved first, and everything downstream reads off it: the type names one file in `variants/`, and that file declares what to extract and which sections the summary adds.

## How it works

The scripts live in this skill's folder: run them from there, with `--calls-dir` pointing at the project's `calls/`.

### Stop 0, memory, input, type

Read [memory.md](memory.md) first: it holds what earlier runs got wrong.

No transcript and no notes: STOP, ask for them, write nothing.

Then resolve the type. **The identity of the counterpart decides, never the topic**: a paying customer asking about a new product is `customer`, whatever the user calls the call.

| Type | The counterpart | File |
|---|---|---|
| `prospect` | evaluating whether to buy from you | [variants/prospect.md](variants/prospect.md) |
| `customer` | already pays you | [variants/customer.md](variants/customer.md) |
| `internal` | your own team, no counterpart | [variants/internal.md](variants/internal.md) |

Type unclear: STOP and ask. Never split one call across two types.

### Stop 1, reload the thread

Run the lookback, always, even when it looks like a first call. First contact is a result of this search, never a reason to skip it. The counterpart is the company for `prospect` and `customer`, the meeting name for `internal`.

    python3 scripts/lookback.py --calls-dir calls --date YYYY-MM-DD --counterpart "Company"

- **Exit 2**: this call already has a summary. Open it, add what is new, STOP. Never a second file for one call. A real second call that day: rerun this stop and the next with `--second-call`.
- **Earlier summaries listed**: read the most recent, and carry its open actions into `## Open loops`.

Paste the lookback line into `## Provenance` as it printed, a zero included.

### Stop 2, create the file

    python3 scripts/new_summary.py --calls-dir calls --date YYYY-MM-DD --type TYPE --counterpart "Company"

It prints two paths. Save the transcript, exactly as given, to the `.transcript.md` one. The summary file is born from [schemas/summary-template.md](schemas/summary-template.md) with the sections of the type already in place.

### Stop 3, extract

Open only the variant file of the type. It declares the fields, the sections and its own STOPs. Blocks shared by several types live in `schemas/`, and the variant says when to open them.

Read [worked-examples/quality-bar.md](worked-examples/quality-bar.md) before the first quote. **Every quote is verbatim**: a line that fails the quality bar is paraphrased and said to be a paraphrase.

Dates, deadlines and the order between actions come from the call. An action with no date says `no date given`. The summary describes the call: the day you process it, and what has happened since, go in `## Provenance` only.

### Stop 4, check

    python3 scripts/check_summary.py SUMMARY_PATH TRANSCRIPT_PATH

Exit 2: fix every `FAIL` line, run it again. Deliver only on exit 0.

### Stop 5, Slack

Read the channel from `knowledge/slack.md` in the project. Post 3 to 5 lines: what moved, the actions with their owner, the one quote worth keeping. Never the summary itself.

No Slack tool or no channel file: print the message in chat for the user to paste, and say so in `## Provenance`.

### Stop 6, report

In chat: the summary path, the check result, Slack posted or printed, and each step skipped with its reason. A correction from the user on this run goes into [memory.md](memory.md) before the session moves on.

## Output

Primary: `calls/{YYYY-MM}/YYYY-MM-DD-{type}-{slug}.md`, 200 to 1,500 words. **`{YYYY-MM}` is the month of the call**, also when it is processed weeks later.

The spine, in this order. A section the type declared and the call left empty carries `/`.

| Section | What it holds |
|---|---|
| `# H1` | one line: what happened and what moved |
| `## Framing` | 3 to 5 lines: who they are, why this call, what it was for |
| `## Open loops` | the actions carried from the last summary, and their state. `/` on a first call |
| `## What happened` | the substance, as the variant asks |
| `## Decisions` | only what was resolved in the room |
| `## Actions` | owner and date, ours and theirs kept apart |
| `## Quotes` | verbatim, with the speaker |
| variant sections | in the order the variant lists them |
| `## Next steps` | only the steps the call dated, one per line, opening with the date. Undated actions stay in `## Actions` |
| `## Provenance` | the source, the lookback line, the gaps, the knowledge files missing, Slack posted or printed |

Personal contact details (emails, phone numbers) never enter the summary. Name, role and company do.

**STOP record.** No transcript, a type nobody can resolve, or a summary of this call already on disk: no new summary is written, the reason goes to the user in one line, and to [memory.md](memory.md).

## References

- What earlier runs taught, read at stop 0: [memory.md](memory.md)
- The checks before any quote: [worked-examples/quality-bar.md](worked-examples/quality-bar.md)
- Prospect calls: [variants/prospect.md](variants/prospect.md)
- Customer calls: [variants/customer.md](variants/customer.md)
- Internal calls: [variants/internal.md](variants/internal.md)
- The summary file as it is born: [schemas/summary-template.md](schemas/summary-template.md)
- The competitive alternative block: [schemas/market-read.md](schemas/market-read.md)
- The thread and the duplicate guard: [scripts/lookback.py](scripts/lookback.py)
- The path and the empty summary: [scripts/new_summary.py](scripts/new_summary.py)
- The check before delivery: [scripts/check_summary.py](scripts/check_summary.py)
