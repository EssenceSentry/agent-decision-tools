---
name: bayesian-fermi-estimation
description: Make a forward Fermi estimate when an uncertain cost, rate, duration or benefit could change a decision. Write the forward calculation in Squiggle as one small function that propagates grounded input distributions and returns an output distribution.
---

# Forward Fermi estimation

**Define the target.** Name the quantity, unit, population, time horizon and decision it informs. A mean cost per run and the realized cost of the next run can have different distributions. Use a direct measurement when it answers the question. If a break-even threshold settles the choice, return it.

**Ground the inputs.** Use comparable historical observations of the target when available. Otherwise decompose it into a few factors that are easier to estimate than the whole. Record the unit and basis of each material input.

- **Observed.** Name the source, selection criteria, period and sample size. Use the observations as an empirical input, retaining matched rows for quantities that co-vary.
- **Elicited.** Anchor named percentiles to identified measurements or analogous cases. Explain the choice of distribution and distinguish its percentiles from physical limits.
- **Known.** Use a constant for an amount fixed by a count, contract, specification or identity.

When a pivotal input lacks a defensible distribution, solve for the value that changes the action or show conditional scenarios. Identify the cheapest observation that could resolve it.

**Use Squiggle. Write one forward function per estimate.** Pass in the grounded quantities and express how they produce the target. A sum, product, fixed overhead, conditional cost or small mixture often suffices. Include a remainder if the named categories leave something out. Reuse the same draw of a shared driver across terms and alternatives. For a realized future outcome, represent event-to-event variation where it matters.

**Check the calculation cheaply.** Check units and one limiting case. Use direct arithmetic when it gives the result exactly. For simulation, start with a modest sample count and a reproducible seed. Increase draws only when sampling error could change the decision. If a plausible change to an input would reverse the decision, report that sensitivity.

**Return the distribution.** Supply the function, input sources and reusable distribution or aligned draws. Give the median and a labeled interval in the target units. Add the mean when the decision depends on expected payoff, or the probability of crossing the threshold when that is what the decision needs.

## Worked examples

- [Price a repository probe](references/planning-examples.md#1-how-much-rework-could-a-repository-probe-avert) when a search might save implementation work and the chance of success is unknown.
- [Estimate a second reviewer’s yield](references/planning-examples.md#2-how-often-would-a-second-reviewer-change-the-decision) when historical reviews cover a different case mix from today’s queue.
- [Estimate minutes saved by caching](references/cache-example.md) when alternatives share an uncertain build time.

## Run it locally

Use Node.js 22 or newer. Resolve `scripts/run.mjs` relative to this skill's installed directory. Supply a `.squiggle` file or pipe the program on stdin. The runner returns JSON and uses a fixed seed by default.

```sh
node "$SKILL_DIR/scripts/run.mjs" estimate.squiggle
node "$SKILL_DIR/scripts/run.mjs" --samples 5000 --seed case-a --draws estimate.squiggle
```

`SKILL_DIR` is the directory containing this `SKILL.md`. Distributions return the mean and the 10th, 50th and 90th percentiles. `--draws` adds the actual aligned sample values for downstream decisions. A list of observed values stays a list. The install in each host includes the pinned interpreter. For a fresh checkout, `npm ci --ignore-scripts --prefix "$SKILL_DIR"` installs it.
