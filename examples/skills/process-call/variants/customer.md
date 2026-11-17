---
sections: [Health, Requests]
---

# customer

Opened at stop 0 when the counterpart already pays you, whatever the call was about.

## Sections

- `## Health`: always.
- `## Requests`: always, `/` when there were none.
- `## Market read`: only when they named an alternative to you, in the shape of [../schemas/market-read.md](../schemas/market-read.md).

## The fields

| Field | What you are looking for | The rule that makes it useful |
|---|---|---|
| Working | what they use and what it does for them | a use they describe in their words is the renewal argument |
| Not working | each problem, who hit it, how often | frequency turns a complaint into a priority |
| Risk | the renewal date, a champion leaving, usage going down, a rival named | a risk has a date or a name, never a feeling |
| Requests | each request, who asked, why, how urgent in their words | one line per request: `request, who, why, urgency` |

## STOPs

- Something shown in the call (a new module, a new plan) is recorded as shown, never as bought, unless they agreed to it in the room.
