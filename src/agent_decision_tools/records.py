"""Revisit a recorded decision when a predeclared signpost is observed."""

from typing import Annotated, Literal

from pydantic import Field, FiniteFloat

from .models import Inputs, Name, Request


class Signpost(Inputs):
    """An observable threshold with an explicit action and owner."""

    metric: Name
    direction: Literal["at_least", "at_most"]
    threshold: FiniteFloat
    unit: Name
    action: Name
    owner: Name


class Revisit(Request):
    """Evaluate decision reopening conditions and render a handoff record."""

    decision: Name
    signposts: Annotated[dict[Name, Signpost], Field(min_length=1)]
    observations: dict[Name, FiniteFloat]

    def calculate(self) -> dict[str, object]:
        """Identify reached thresholds, missing observations and follow-up actions."""
        missing: list[str] = []
        triggered: list[str] = []
        lines = [f"# {self.decision}", "", self.basis, ""]
        for name, rule in self.signposts.items():
            value = self.observations.get(rule.metric)
            if value is None:
                missing.append(name)
            elif (
                value >= rule.threshold
                if rule.direction == "at_least"
                else value <= rule.threshold
            ):
                triggered.append(name)
            observed = "unobserved" if value is None else str(value)
            direction = rule.direction.replace("_", " ")
            lines.append(
                f"- {name} uses {rule.metric} ({rule.unit}), currently {observed}. "
                f"At a value {direction} {rule.threshold}, "
                f"{rule.owner} should take this action — {rule.action}."
            )
        return {
            "status": "reopen" if triggered else "await_data" if missing else "keep",
            "triggered": triggered,
            "missing": missing,
            "record": "\n".join(lines) + "\n",
        }
