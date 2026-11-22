# Agent Decision Tools

A local Python API and JSON CLI for deciding whether to inspect, run a pilot, ask for another opinion, or proceed with the evidence in hand. Related calculations share their inputs. For example, one payoff table and one description of a check give the value of acting now, the value of learning, the action to take after each result, and the best affordable next step.

## Run a decision

From this checkout, install the locked dependencies with Python 3.12+ and Node.js 22+.

```sh
uv sync --locked
npm ci --ignore-scripts --prefix skills/bayesian-fermi-estimation
uv run agent-decision-tools run decide examples/defect.json
```

The example inspection costs 0.25 hours. It changes the preferred action to prevention after a positive result and leaves the design alone after a negative result. Its expected value is 1.60 hours gross and 1.35 hours net. All example data are synthetic.

## Choose a calculation

| Question | Operation | Result |
|---|---|---|
| How much could this cost or save? | `fermi` | Runs a forward Squiggle program with a seed and returns quantiles, means and optional draws. |
| Is a pilot, benchmark or follow-up worth its cost? | `decide` | Expected action payoffs, EVPI, optional EVPPI, EVSI, net value, posterior actions and an affordable policy up to two observations deep. |
| Which action holds up across plausible scenarios? | `robust` | Worst payoffs, worst regrets, and the preference threshold in a two-action, two-state problem. |
| How often would a probe need to pay off? | `breakeven` | Minimum success probability from conditional savings and a fixed cost. |
| Do the results clear a predeclared threshold? | `interim` | An exact binomial interval adjusted for the planned looks and a stop, continue or unresolved result. |
| Where do independent judgments differ? | `panel` | Reasons, revisions, probability range, median and equal-weight pool on one binary question. |
| How accurate were our forecasts? | `calibrate` | Paired Brier scores and signed mean errors for each forecaster and for their equal-weight pool. |
| What work fits after reserving time for verification? | `schedule` | OR-Tools selects optional jobs, enforces dependencies and resource limits, and reports solver status. |
| Has a recorded decision reached a reopening condition? | `revisit` | Triggered thresholds, missing observations and an owner/action record. |

## Call from an agent

```python
import json
from pathlib import Path
from agent_decision_tools import evaluate, schema, tools

operations = tools()
request_shape = schema("decide")
report = evaluate("decide", json.loads(Path("examples/pilot.json").read_text()))
next_step = report["policy"]
```

The CLI exposes the same operations through `list`, `schema NAME` and `run NAME [FILE]`. Omit the file to send JSON on stdin. Every request requires a `basis` naming the evidence or modeling assumptions. Use historical records or the forward Fermi skill to ground material estimates. If a pivotal probability has no defensible basis, calculate the threshold or compare scenarios.

The [worked guide](docs/getting-started.md) connects Squiggle draws to a decision, explains the pilot example and lists the runnable fixtures. The [method catalog](docs/methods.md) maps the earlier tool survey to the implemented routines and specialist packages. The [Fermi skill](skills/bayesian-fermi-estimation/SKILL.md) can also run directly from Codex or Claude.
