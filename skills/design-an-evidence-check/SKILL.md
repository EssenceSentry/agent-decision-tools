---
name: design-an-evidence-check
description: Use when a proposed experiment, benchmark or software check will cost meaningful time and its result could change a choice.
---

# Choose a check that can change the decision

State what you would do today. For each plausible result of the proposed check, including an inconclusive one, identify the resulting action. Omit a discretionary check if every outcome leads to the same action. For required verification, choose a check that can fail for the relevant reason.

For research, define the unit, comparison, decision threshold and major threat to validity. For software, describe a plausible wrong implementation, the observable failure at a real caller, and an oracle that would catch it. Choose a cheaper discriminating observation if it answers the same question.

Use only the references that match the uncertainty: [research designs](references/research-checks.md), [causal identification](references/causal-designs.md), [software test strategies](references/test-strategies.md), [SQL grain probes](references/sql-probes.md), or [additional examples](references/field-notes.md).
