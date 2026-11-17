# process-call, memory

Read at stop 0. Written when a run is corrected, when the skill stops, or when a run shows something new. One dated line each, never rewritten. A lesson that comes back becomes a change to `SKILL.md`.

## Learnings

- 2026-08-15 · A recorder that auto-translates a mixed-language call corrupts it: product names came back as common words. A machine translation inside quote marks is a fabricated quote. Quote only lines that stayed in their language.
- 2026-08-15 · Asking someone to predict their own behaviour ("would you buy this?") gets a polite yes every time. Record what they did or committed to, with a date.
- 2026-09-17 · Two runs processed the same meeting minutes apart and filed it twice. The counterpart search could not see it, since a duplicate of this call is not an earlier call. `lookback.py` now takes the date and stops on a second file.
- 2026-11-17 · The first full eval run caught a summary writing a deadline and a dependency the call never stated. Dates and order come from the call; an action without one says `no date given`.
- 2026-11-17 · The line above did not hold: a later run wrote "Before 2026-11-19" for an undated step again, and dated "the first of March", said in November, in the current year. Both moved into `check_summary.py`: a date in `## Actions` or `## Next steps` before the call fails, and a `## Next steps` line must open with a date. The run after noted a deadline "passed as of" the day of processing: today's date outside `## Provenance` fails too.

## STOP records

## Rejected patches
