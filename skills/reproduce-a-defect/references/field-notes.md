# Diagnosing a defect

<a id="diagnosing-bugs"></a>

## Build a tight red-capable feedback loop

Capture a reproducible public symptom with a pass/fail signal. Prefer an automated command, captured fixture or direct observation. For intermittent failures record attempts and exposure conditions. Minimize the input while retaining failure. Make rival predictions, instrument their point of divergence and repair the responsible seam. Rerun the original scenario, keep a regression and remove temporary logging. For a human-only observation use the [assisted replay](assisted-replay.md) and redact sensitive material.

<a id="systematic-debugging"></a>

## Trace where the bad value first appeared

Trace a failing value backwards through callers until its first invalid producer. Compare a working example and check dependencies and environment. Change one predicted cause at a time. Persistent failed fixes warrant revisiting architecture. Repair at origin, add boundary guards where independently useful, and observe a real readiness signal for timing issues. Use the [pollution locator and bounded waiter](debug-tools.md) when their assumptions fit.
