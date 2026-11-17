---
name: process-call
description: "Turn a call transcript into a dated summary with verbatim quotes, actions with owners and next steps, then post a short update to Slack. Use when the user pastes a transcript or meeting notes, or says 'process this call', 'summarize this meeting', 'log my call with X'. Handles prospect, customer and internal calls. Not for: preparing a call that has not happened yet, or material that is not a conversation."
license: MIT
---

# process-call

One call in, one summary out at `calls/YYYY-MM/YYYY-MM-DD-{type}-{slug}.md`, plus a Slack update.

## When to use

- The user pastes a transcript or notes from a call, or a call recorder export.
- One call per run. Two transcripts: two runs.

## Not for

- A call that has not happened: help the user prepare in plain chat.
- A document, an email thread, an article.

## Steps

1. **Check the input.** No transcript and no notes: stop, ask for them, write nothing.
2. **Decide the type.** Who the counterpart is decides, never the topic: a customer asking about a new product is still `customer`. Unclear: stop and ask.

   | Type | The counterpart | Read |
   |---|---|---|
   | `prospect` | evaluating whether to buy from you | `references/prospect.md` |
   | `customer` | already pays you | `references/customer.md` |
   | `internal` | your own team only | `references/internal.md` |

3. **Find the thread.** Always, even when it looks like a first call. The counterpart is the company for `prospect` and `customer`, the meeting name for `internal`. Scripts live in this skill's folder.

       python3 scripts/lookback.py --calls-dir calls --date YYYY-MM-DD --counterpart "Company"

   - Exit 2: this call already has a summary. Open it, add what is new, stop. Never write a second file. A real second call that day: rerun both scripts with `--second-call`.
   - Earlier summaries listed: read the latest, carry its open actions into `## Open loops`.
4. **Create the file.**

       python3 scripts/new_summary.py --calls-dir calls --date YYYY-MM-DD --type TYPE --counterpart "Company"

   It prints two paths. Save the transcript, exactly as given, to the `.transcript.md` path.
5. **Fill the summary.** Follow the variant file. Read `references/quality-bar.md` before the first quote.
6. **Check it.**

       python3 scripts/check_summary.py SUMMARY_PATH TRANSCRIPT_PATH

   Exit 2: fix what it prints, run it again. Deliver only on exit 0.
7. **Slack.** Read the channel from `knowledge/slack.md`. Post 3 to 5 lines: what moved, the actions with their owner, one quote. No Slack tool or no channel: print the message in chat for the user to paste.
8. **Report.** The summary path, the check result, Slack posted or printed.

## Output

- `calls/YYYY-MM/YYYY-MM-DD-{type}-{slug}.md`, from `assets/summary-template.md`, 200 to 1,500 words.
- The month is the month of the call, also when you process it weeks later.
- Deal stages, channels and other company facts come from `knowledge/`. A missing file: write what the call said and flag it in `## Provenance`.

## Gotchas

- A quote from an auto-translated transcript is not verbatim. Quote only passages in their original language, paraphrase the rest and say so.
- "Would you buy this?" gets a polite yes. Record what the counterpart did or committed to, with a date, over what they predicted they would do.
- A friendly call is not a decision. `## Decisions` holds only what was resolved in the room.
- Dates, deadlines and the order between actions come from the call. An action with no date says "no date given". Never infer a deadline, a dependency, or a status as of the day you process it.
- Two calls with the same counterpart on the same day are two summaries. The same call processed twice is one: `lookback.py` tells them apart.
- Emails and phone numbers never enter the summary. Name, role and company do.
