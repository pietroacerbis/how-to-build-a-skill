# report-format

The shape of every review, written to `skill-reviews/YYYY-MM-DD-{skill}.md`.

```markdown
---
skill: {name}
source: {local path or GitHub URL}
date: YYYY-MM-DD
profile: full | spec
verdict: install | fix first | do not install
---

# {name}: {verdict}

## Verdict

One sentence: the verdict and the reason that decides it.

## Security

Each FAIL and WARN of scan_security.py, with file:line, confirmed or cleared in one sentence.
The domains the skill contacts, and what it sends. "/" when the scan found nothing.

## Format

Each FAIL and WARN of check_format.py, as printed. "/" when it passed clean.

## Judgment

- Knowledge inside the skill: the lines quoted, or "/".
- Description: one request that would trigger it wrongly, or "/".
- Stops: the stop that does more than one action or opens no file, or "/".

## Fixes

1. What changes the verdict, most important first. "/" when the verdict is install.

## Suggestions

- What would make the skill better without changing the verdict: the WARN lines and the other judgment findings.
```
