---
name: agent-decision-tools
description: Price an optional search, experiment, review or follow-up and choose whether to act now. Use the local decision API when time, money or uncertainty could change a research or engineering decision.
---

# Decide whether the next step pays

Write the action you would take now and the loss if it is wrong. Name the cheapest alternative and one observation that would make you switch. If every possible result leads to the same action, skip that investigation unless it serves a separate obligation. A requested deliverable, acceptance test or binding requirement belongs in the feasible set. Price the discretionary depth around it. Keep a single allowance for the task, including time to check and deliver.

**Ground the inputs.** Start with comparable historical decisions, remembering the misses as well as the successes. Give the population, dates, unit, denominator and revision. For a missing quantity, use `bayesian-fermi-estimation` to write a small **Squiggle** forward function. Anchor distributions for its factors to observations or named analogues. Carry shared drivers through the same draws. Enter known terms directly. For unresolved assumptions use conditional scenarios or solve for the break-even point. A generated probability, a confidence adjective or an unexplained score does not establish a prior. Record material sources in the request's `basis`.

**Choose the least expensive calculation that can settle the decision.** A comparison you can settle by inspection needs no solver call. Use measured time or a common payoff unit, count delay and false alarms, and keep genuine hard limits separate. When units cannot be converted defensibly, report the frontier or show separate scenarios.

| If the decision turns on… | Call | What to read |
|---|---|---|
| An uncertain duration, loss or conditional benefit | `fermi` | Describe the target and unit. Read the mean for expected payoff, the interval for uncertainty, or set `draws` for downstream samples. |
| Whether a probe pays if it sometimes succeeds | `breakeven` | Supply fixed cost and equally weighted conditional savings draws. A miss must save zero. Compare the threshold to historical hit rates or leave it as a condition. |
| Which action survives poorly known odds | `robust` | Supply a state × action payoff table. Examine worst payoff and worst regret. A binary switch point gives the odds that reverse the preference. |
| Which imperfect observation to buy | `decide` | Supply the same table, a grounded state distribution, outcome likelihoods within each state, and check costs. EVPI caps the value of perfect information. A partition prices perfect knowledge of that group. EVSI prices the proposed observation. Read net value and the budget-constrained policy. |
| A pilot followed by selective confirmation | `decide` | Set `depth` to 2, include both checks and a per-path budget. Use only when observations are conditionally independent given the modeled state. Read the next action separately on each branch. |
| Stopping a repeatable pass/fail trial | `interim` | Predeclare the independent Bernoulli units, threshold, cumulative looks and error rate. Report above, below, continue or unresolved at cap. A deliberately selected challenge pair does not satisfy the sampling design. |
| Expert disagreement or track record | `panel`, `calibrate` | Collect comparable independent judgments before sharing reasons. Inspect revisions. On the same resolved cases, compare each forecaster's Brier score and signed error to the equal pool. These operations summarize supplied records. |
| Work competing for one or more calendars | `schedule` | Use integer durations, additive values, prerequisites and one resource per job. Set deadline and reserve. Read solver status before claiming optimality. A solver allocation confers no execution authority. |
| Whether an accepted decision has expired | `revisit` | Supply the observed metric in its declared unit, threshold, direction, owner and response. Check missing signals as well as triggered ones. |

## Call the toolkit

Use `agent-decision-tools list`, `schema NAME`, or `run NAME [FILE]`. An omitted file reads JSON on stdin. If the CLI is outside PATH, run the [launcher](scripts/decision-tools) from this skill by its full path. It uses the prepared package environment in the tools checkout, an installed CLI, or the executable named by `AGENT_DECISION_TOOLS_BIN`. It preserves the caller's working directory. Python callers can use `from agent_decision_tools import evaluate, schema, tools` and `evaluate(name, payload)`.

A synthetic example illustrates an unknown success probability. A specification fixes a search allowance of 15 minutes. Three comparable successful repairs avoided 45, 60 and 75 minutes of work. No benefit accrues on a miss.

```sh
agent-decision-tools run breakeven <<'JSON'
{"basis":"Synthetic worked example. Fixed 15-minute allowance and all three matched successful repairs. A miss saves zero.","unit":"active minutes","cost":15,"gains_if_success":[45,60,75]}
JSON
```

The threshold is **25%**. A log containing only successful searches supplies conditional savings but cannot tell you how often searches succeed. If neither the threshold nor a credible range settles the choice, identify the smallest observation that would.

Return the action, the basis, what result could reverse it and the remaining cap. A check whose net value is positive still competes with other uses of that allowance. Recompute when a material observation changes the decision. In a research or coding stage, this can mean act now, do one cheap check, reopen an earlier choice, or finish with the current evidence.
