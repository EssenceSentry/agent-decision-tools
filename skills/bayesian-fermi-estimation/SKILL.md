---
name: bayesian-fermi-estimation
description: Use when an uncertain cost, duration, rate or benefit could change a decision and you need an estimate with a defensible distribution.
---

# Make a forward estimate in Squiggle

Define the output, unit, population and time horizon. Use a direct measurement or a break-even calculation when it settles the decision. Otherwise write **one small forward function in Squiggle**. Decompose unknowns into a few factors grounded in comparable observations or explicitly anchored quantiles. Keep known values fixed. If a pivotal factor lacks a defensible distribution, give conditional results.

Reuse the same draw of a shared driver across alternatives. Keep correlated observations paired. If new case observations update a reference class, [update the input distribution](references/updating-inputs.md) before sampling. Check units and a limiting case. Report the median and a labeled interval, plus a mean or threshold probability when the decision needs it.

Run `node "$SKILL_DIR/scripts/run.mjs" estimate.squiggle`, where `SKILL_DIR` is this skill’s directory. Use `--samples 5000 --seed case-a --draws` for reproducible aligned draws. Install the pinned runtime with `npm ci --ignore-scripts --prefix "$SKILL_DIR"` (Node.js 22+).

[Repository-probe and second-reviewer examples](references/planning-examples.md) · [Cache savings example](references/cache-example.md)
