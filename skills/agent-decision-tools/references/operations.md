# Choosing an operation

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

## Break-even example

A synthetic example illustrates an unknown success probability. A specification fixes a search allowance of 15 minutes. Three comparable successful repairs avoided 45, 60 and 75 minutes of work. No benefit accrues on a miss.

```sh
agent-decision-tools run breakeven <<'JSON'
{"basis":"Synthetic worked example. Fixed 15-minute allowance and all three matched successful repairs. A miss saves zero.","unit":"active minutes","cost":15,"gains_if_success":[45,60,75]}
JSON
```

The threshold is **25%**. A log containing only successful searches supplies conditional savings but cannot tell you how often searches succeed. If neither the threshold nor a credible range settles the choice, identify the smallest observation that would.
