---
name: agent-decision-tools
description: Use when a calculation about the value of information, robustness, stopping, scheduling or forecast accuracy could change an actual decision.
---

# Calculate when the result matters

State the action you would take now and what result would change it. Use arithmetic by hand when it settles the choice. For an uncertain input, use comparable observations or a grounded forward estimate. If neither is available, report a break-even threshold or conditional scenarios. Record the basis, units and costs in the request.

Use `decide` to price an observation or a contingent policy. For each check, include the same outcome labels in every state and explicitly give zero probability to impossible outcomes. Charge each cost once. Check the best action before observing, then the action after each possible result.

Use the [operation guide](references/operations.md) for `robust`, `breakeven`, `fermi`, `interim`, `panel`, `calibrate`, `schedule` and `revisit`. Run [the launcher](scripts/decision-tools) with `list`, `schema NAME`, or `run NAME [FILE]`. Omitting the file reads JSON from stdin. The Python API exposes `evaluate(name, payload)`. Return the decision and the uncertainty that could reverse it.
