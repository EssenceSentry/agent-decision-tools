"""Tools for predeclared interim looks, expert panels and resolved forecasts."""

from __future__ import annotations

from math import fsum
from statistics import median
from typing import Annotated, Self

from pydantic import Field, model_validator

from .models import Inputs, Name, Probability, Request


class Interim(Request):
    """Apply simultaneous exact binomial bounds at a finite set of planned looks."""

    looks: Annotated[list[Annotated[int, Field(gt=0)]], Field(min_length=1)]
    trials: Annotated[int, Field(gt=0)]
    successes: Annotated[int, Field(ge=0)]
    threshold: Probability
    alpha: Annotated[float, Field(gt=0, lt=1)] = 0.05

    @model_validator(mode="after")
    def _design(self) -> Self:
        if self.looks != sorted(set(self.looks)) or self.trials not in self.looks:
            raise ValueError(
                "trials must match a predeclared look in a strictly increasing list"
            )
        if self.successes > self.trials:
            raise ValueError("successes cannot exceed trials")
        return self

    def calculate(self) -> dict[str, object]:
        """Compute a familywise interval and a continue, stop or unresolved decision."""
        from scipy.stats import binomtest

        confidence = 1 - self.alpha / len(self.looks)
        interval = binomtest(self.successes, self.trials).proportion_ci(
            confidence_level=confidence, method="exact"
        )
        lower, upper = float(interval.low), float(interval.high)
        decision = "unresolved_at_cap" if self.trials == self.looks[-1] else "continue"
        if lower > self.threshold:
            decision = "above_threshold"
        elif upper < self.threshold:
            decision = "below_threshold"
        return {
            "decision": decision,
            "interval": [lower, upper],
            "per_look_confidence": confidence,
            "familywise_alpha": self.alpha,
            "estimate": self.successes / self.trials,
        }


class Opinion(Inputs):
    """One independently elicited probability and the assumption behind it."""

    probability: Probability
    reason: Name
    previous: Probability | None = None


class Panel(Request):
    """Summarize disagreement and revisions on one common binary question."""

    question: Name
    opinions: Annotated[dict[Name, Opinion], Field(min_length=1)]

    def calculate(self) -> dict[str, object]:
        """Summarize initial or revised judgments and retain their reasoning."""
        values = [op.probability for op in self.opinions.values()]
        return {
            "question": self.question,
            "median": median(values),
            "equal_pool": fsum(values) / len(values),
            "range": [min(values), max(values)],
            "arguments": [op.reason for op in self.opinions.values()],
            "revisions": {
                name: op.probability - op.previous
                for name, op in self.opinions.items()
                if op.previous is not None
            },
        }


class Resolved(Inputs):
    """A resolved event with probabilities supplied before resolution."""

    event: Name
    occurred: bool
    forecasts: Annotated[dict[Name, Probability], Field(min_length=1)]


class Calibration(Request):
    """Score forecasters and their equal-weight pool on the same resolved events."""

    records: Annotated[list[Resolved], Field(min_length=1)]

    @model_validator(mode="after")
    def _paired(self) -> Self:
        labels = self.records[0].forecasts.keys()
        if any(r.forecasts.keys() != labels for r in self.records):
            raise ValueError("forecasters must be paired across events")
        if "equal_pool" in labels or len({r.event for r in self.records}) != len(
            self.records
        ):
            raise ValueError("event names must be unique and equal_pool is reserved")
        return self

    def calculate(self) -> dict[str, object]:
        """Return mean Brier score and signed probability bias for each forecaster."""
        n = len(self.records)
        series = {
            k: [r.forecasts[k] for r in self.records] for k in self.records[0].forecasts
        }
        series["equal_pool"] = [
            fsum(r.forecasts.values()) / len(r.forecasts) for r in self.records
        ]
        differences = {
            k: [
                p - float(r.occurred) for p, r in zip(values, self.records, strict=True)
            ]
            for k, values in series.items()
        }
        return {
            "events": n,
            "brier": {k: fsum(d * d for d in ds) / n for k, ds in differences.items()},
            "mean_bias": {k: fsum(ds) / n for k, ds in differences.items()},
        }
