# After a call

The order of the skills that run once a call ends. Each step reads the output of the step before. The logic lives in the skills, never here.

| # | Skill | Output |
|---|---|---|
| 1 | `process-call` | the summary in `calls/YYYY-MM/` and the Slack update |
| 2 | `update-crm` (yours, not in this repo) | the deal record, moved only on the evidence the summary quotes |
| 3 | `follow-up-email` (yours, not in this repo) | a draft to the counterpart with the actions both sides owe |

Run it by asking Claude: "run after-a-call on this transcript".
