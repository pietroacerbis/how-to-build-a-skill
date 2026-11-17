# SKILL-FORMAT, the checklist

Run every skill through this before you install it, yours or someone else's. The why behind each row is in the [guide](README.md).

## Format

| # | Check | Pass when |
|---|---|---|
| 1 | Folder | `SKILL.md` at the root, the folder name equal to `name` |
| 2 | `name` | max 64 characters, lowercase letters, numbers and hyphens, no leading, trailing or double hyphen |
| 3 | `description` | max 1,024 characters, opens with a verb, says when to use it and what it is not for |
| 4 | Size | `SKILL.md` under 500 lines and about 5,000 tokens |
| 5 | Steps | numbered, one action each |
| 6 | Output | an exact path, and a template in `assets/` when the format matters |
| 7 | Stop | says what to do when the input is missing or unclear: stop and ask |
| 8 | Variants | one file per situation in `references/`, and the step that says when to read each |
| 9 | References | every file in `references/` and `assets/` is named in `SKILL.md`, with the condition to read it |
| 10 | Scripts | every deterministic step (dates, paths, counts, exact matches, format checks) is a script in `scripts/` |
| 11 | Validation loop | a check runs before delivery, and the output ships only when it passes |
| 12 | No company knowledge | no prices, ICP, team names, channels or stages inside the skill: they sit in `knowledge/` and the skill opens them |
| 13 | No filler | no line Claude would get right without it |
| 14 | Gotchas | a `## Gotchas` section with corrections from real runs |
| 15 | Evals | 10 to 15 cases in `evals/`, regex graders for the form, an LLM grader for the substance |

## Security

Check these before installing a skill you did not write.

| # | Check | Fail when |
|---|---|---|
| 16 | Hidden instructions | text that tells Claude to ignore the user, hide what it does, or act outside the skill's job, in `SKILL.md`, a reference, an HTML comment or invisible characters |
| 17 | Network | a script or a step calls a URL the description does not explain |
| 18 | Secrets | a script reads `.env`, keys, tokens, SSH files or browser data |
| 19 | Writes | the skill writes or deletes outside its declared output path |
| 20 | Obfuscation | encoded strings (base64, hex) decoded and run, or code downloaded and executed |

One security fail: do not install it.
