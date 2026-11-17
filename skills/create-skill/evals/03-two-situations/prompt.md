---
description: "Two kinds of runs become two variants"
tags: [create, variants]
max_turns: 80
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Make this a skill, call it write-investor-update, and write it to skills/write-investor-update. I've written our monthly investor update with Claude three times now, in September, October and November, and here is what I learned.

How each run went:
1. I paste the metrics export from our finance sheet, a CSV with month, MRR, new customers, churned customers, cash and burn.
2. Claude computes the month-over-month change of MRR and burn, and the runway in months, cash divided by burn. It got the percentages wrong twice, so I recheck them by hand every time.
3. Claude writes five sections: Highlights, Metrics, Lowlights, Asks, Next month.
4. I save it as updates/YYYY-MM/YYYY-MM-investor-update.md.

Corrections I made:
- When there was nothing bad to report, Claude invented a lowlight. Now I tell it to write "none this month".
- It kept using superlatives like "incredible month". No superlatives.

Facts I had to give Claude every time: our investors are Northbeam Ventures and two angels, Sara Lind and Marco Bassi; our runway target is 18 months; we report in EUR.

There are two kinds of runs. The monthly update to investors has the five sections above. The quarterly board pack adds Financials against plan, Hiring and Risks, and ends with Decisions needed from the board. Only I use it. It needs the CSV to start; last month's update helps but is optional. No tools or connectors.
