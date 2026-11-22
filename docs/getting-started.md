# Work through a decision

Install from this checkout. Python tools use the locked uv environment. The forward estimator also uses Node.js 22+ and a pinned local Squiggle runtime.

```sh
uv sync --locked
npm ci --ignore-scripts --prefix skills/bayesian-fermi-estimation
uv run agent-decision-tools list
uv run agent-decision-tools schema decide
```

## Price the first observation

Run `uv run agent-decision-tools run decide examples/defect.json`. Defects cost 16 hours, prevention costs four hours and the modeled defect rate is 20%. Leaving the design alone costs 3.2 hours in expectation. Perfect information could save 2.4 hours. The proposed inspection detects 80% of defects and flags 10% of clean cases. Its positive result raises the defect probability to two thirds, above the 25% prevention threshold. Accounting for both possible results gives 1.6 hours of expected savings before inspection cost.

Use one payoff unit throughout. Enter losses as negative payoffs and prices as positive costs. Each row of the likelihood table describes possible observations conditional on one state. Include inconclusive results if they can occur. A named partition returns the value of learning a group exactly while uncertainty within that group remains. The policy can always stop and act. A budget limits spend on every possible path. The values under `checks` price standalone checks even if the current budget rules them out.

## Look ahead when a pilot unlocks another check

Run `uv run agent-decision-tools run decide examples/pilot.json`. With a one-check limit, the best decision is to ship immediately. With two checks available, run the cheap pilot, confirm only after a flag, and ship after a clear result. Each flag leads to a confirmation before taking a final action. The policy improves the expected payoff from −1.000 to −0.776 hours, including both check prices on the branches where they are paid.

This solver handles a finite state and action table, fixed observation costs and up to two distinct checks. For two checks, the caller must justify and declare conditional independence of their observations given the state. Two reviewers sharing an unmodeled failure mode can violate that assumption. Enrich the states or supply a different joint observation model in a specialist solver.

## Pass an uncertain quantity between tools

The example models three callers and a common per-caller effort distribution. Its illustrative comparison set puts the 10th and 90th percentiles of additional effort at 20 and 80 minutes. A 20-minute repository probe only saves effort if it finds a compatible helper.

```python
import json
from pathlib import Path
from agent_decision_tools import evaluate

request = json.loads(Path("examples/fermi.json").read_text())
estimate = evaluate("fermi", {**request, "draws": True})
threshold = evaluate("breakeven", {
    "unit": estimate["unit"],
    "basis": request["basis"] + " A failed probe saves zero active minutes.",
    "cost": 20,
    "gains_if_success": estimate["value"]["draws"],
})
print(threshold["break_even_probability"])
```

With the modeled lognormal effort, the probe breaks even at about 14% success probability. This calculation needs the **mean** time saved conditional on success. A compatible helper's chance of existing can remain unknown. Preserve matched rows when the same historical case determines several inputs. Document the source, unit, selection and sample size for measured factors, and the analogues used for elicited percentiles. The free-text evidence field records this basis. Its presence alone cannot establish its quality.

## Runnable inputs

Pass one row's operation and file to `uv run agent-decision-tools run` from the repository root.

| Operation | File | Assumption to inspect |
|---|---|---|
| `fermi` | `examples/fermi.json` | One common integration difficulty across three callers. |
| `decide` | `examples/defect.json`, `examples/pilot.json` | Risk-neutral expected payoff in hours. |
| `robust` | `examples/risk.json` | The enumerated scenarios cover the decision's material risks. |
| `breakeven` | `examples/probe.json` | Conditional savings draws have equal weight. A miss saves zero. |
| `interim` | `examples/interim.json` | Independent Bernoulli observations, one stable rate and a finite schedule of looks fixed in advance. |
| `panel` | `examples/opinions.json` | All panelists answered the same binary question independently before seeing revisions. |
| `calibrate` | `examples/forecasts.json` | Every forecaster supplied a probability for every event before resolution. Lower Brier scores are better. |
| `schedule` | `examples/jobs.json` | Fixed integer durations, additive job values and one shared resource of capacity one per named resource. `FEASIBLE` is an incumbent; `OPTIMAL` certifies the objective. |
| `revisit` | `examples/signposts.json` | Observations use each signpost's declared units. Missing values remain unknown. |

The statistical interim rule uses a Bonferroni allocation across exact two-sided intervals. It can end unresolved at the last look. One or two deliberately difficult benchmark cases can diagnose a failure or refute a claimed capability. A handpicked pair cannot estimate a model's population success rate.
