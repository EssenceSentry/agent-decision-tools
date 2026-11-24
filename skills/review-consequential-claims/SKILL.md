---
name: review-consequential-claims
description: Use when an analysis, code guarantee or recommendation is about to support a decision and a specific error could change it.
---

# Audit a claim at its point of use

Identify the consequential claim and the action that relies on it. Trace the claim to evidence at the applicable revision. For a measured change, check the unit, denominator, eligibility and time window on each side. For a software guarantee, exercise the public caller with a counterexample that would expose a violation.

Report the finding, the evidence and exactly which decision changes. Preserve any valid narrower claim or separately usable output. If there are no decision-changing findings, say so. Distinguish a check actually executed from a check proposed or claimed by the author.

For causal claims, inspect the [method-specific assumptions](references/causal-diagnostics.md). For a review against a contract, consult the [review techniques](references/field-notes.md).
