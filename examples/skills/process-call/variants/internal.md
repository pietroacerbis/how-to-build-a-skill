---
sections: [Topics, Open questions]
---

# internal

Opened at stop 0 when only your own team was in the room. The counterpart passed to the scripts is the name of the meeting.

## Sections

- `## Topics`: one line per topic, `topic: where it landed`.
- `## Open questions`: what the room could not answer, and who will find out.

## The fields

| Field | What you are looking for | The rule that makes it useful |
|---|---|---|
| Decisions | what was resolved, and who decided | a decision without its owner gets reopened |
| Owners | every action with one owner and its date | two owners means none |
| Open questions | what nobody could answer, and who finds out | an open question with an owner gets answered |

## STOPs

- A topic discussed and not resolved goes to `## Open questions`, never to `## Decisions`.
