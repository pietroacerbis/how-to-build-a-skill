# quality-bar, the checks before a quote

Run every check before quoting a line. A line that fails one is paraphrased, never quoted, and the problem is named in one line of `## Provenance`.

## The source

| Check | Tell | Action |
|---|---|---|
| Empty record | a title and participants, no sentences | STOP, write nothing: a bot joined, nobody talked |
| Auto-summary | the text is the recorder's summary, not the transcript | never quote it, never take a date or an action from it |
| Auto-translation | the call mixed two languages | quote only lines that stayed in their original language |

## The transcript

| Check | Tell | Action |
|---|---|---|
| Mangled name | a product or person name reads wrong inside a sentence that reads fine | never quote the name as transcribed, name the garble |
| Speaker mix-up | two people under one label | attribute from the content, and say so |
| Hallucinated tail | a long final stretch, one speaker, thinning content | find where the call ended, quote nothing after it |

## The summary

| Bad | Good | Why |
|---|---|---|
| "They love the product" | "We open it every morning before standup" (Marta Keller) | a quote is their words, never your summary of them |
| "Pricing is a concern" | "Above the current tool's price, I can't sign alone" (Marta Keller) | the exact words carry the constraint: a signing limit |
| `## Decisions`: the demo went well | `## Decisions`: / | a feeling is not a decision |
| Action: follow up | Action: send the security answers, Sam, 2026-11-14 | one owner and a date |
| 2,800 words retelling the call | 600 words on what moved | the transcript is already saved beside the summary |
