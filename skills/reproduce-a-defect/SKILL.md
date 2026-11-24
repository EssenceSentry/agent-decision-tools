---
name: reproduce-a-defect
description: Use when an observed defect, intermittent failure or disagreement between public views needs a reproducible diagnosis and repair.
---

# Make the reported failure observable

Start at the public entry point where someone experienced the defect. Capture the smallest input or event schedule that makes the expected and observed behavior differ. Run that probe on the failing implementation before editing when it is available.

For a race, pause at the event that matters. While one operation is stalled, inspect what another caller can observe, acknowledge or recover. Distinguish a physical intermediate state from the guarantee promised to a caller. Record the triggering schedule when a failure is intermittent.

Repair the responsible boundary, rerun the same probe, and keep the regression when it protects the contract. Report the before-and-after observations. Use the [pollution locator and wait pattern](references/debug-tools.md) for test residue or timing, or [assisted replay](references/assisted-replay.md) for an observation only a human can make. [Diagnostic techniques](references/field-notes.md)
