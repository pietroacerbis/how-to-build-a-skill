---
sections: [Qualification, Market read]
---

# prospect

Opened at stop 0 when the counterpart is evaluating whether to buy from you. The deal stages are company knowledge: this file reads them from `knowledge/deal-stages.md` and never copies them.

## Sections

- `## Qualification`: always, the fields below.
- `## Market read`: always, in the shape of [../schemas/market-read.md](../schemas/market-read.md).

## `## Qualification`, the fields

| Field | What you are looking for | The rule that makes it useful |
|---|---|---|
| Pain and trigger | what is broken, and why it became urgent now | the trigger is worth more than the pain. Verbatim |
| Current way | what they use today, what they built themselves | a do-it-yourself setup that works is a harder rival than a vendor |
| Who decides | who signs, who uses it daily, who champions it, who is missing from the room | the last one is the field that decides the deal |
| Budget and authority | the order of magnitude, and whether the person in the room can commit it | two questions, never one |
| Success | how they will tell in ninety days that it worked | push for something countable |
| Stage | the stage in `knowledge/deal-stages.md` this call gives evidence for, and the evidence | a good conversation is not a stage move |

## STOPs

- Budget not said: `/` and a line in `## Provenance`. Never estimated.
- Who decides incomplete: write who is missing. Silence reads as complete.
- `knowledge/deal-stages.md` missing: no stage, the gap named in `## Provenance`.
