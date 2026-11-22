"""Finite decisions, sensitivity and the value of information."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import fsum, isclose, ulp
from typing import Annotated, Literal, Self

from pydantic import Field, FiniteFloat, model_validator

from .models import Inputs, Name, Nonnegative, Probability, Request

type Weights = dict[str, float]
type Payoffs = dict[str, dict[str, float]]


def _validate_probabilities(weights: Weights) -> None:
    if not isclose(fsum(weights.values()), 1.0, rel_tol=0, abs_tol=1e-10):
        raise ValueError("probabilities must sum to one")


def _best(weights: Weights, payoffs: Payoffs) -> tuple[str, float]:
    actions = next(iter(payoffs.values()))
    values = {a: fsum(p * payoffs[s][a] for s, p in weights.items()) for a in actions}
    return max(values.items(), key=lambda pair: pair[1])


class _Table(Request):
    unit: Name = Field(
        description="Common payoff unit. Higher is better. Enter costs as negatives."
    )
    payoffs: Annotated[dict[Name, dict[Name, FiniteFloat]], Field(min_length=1)] = (
        Field(description="State -> action -> payoff. Each state has the same actions.")
    )

    @model_validator(mode="after")
    def _rectangular(self) -> Self:
        actions = next(iter(self.payoffs.values())).keys()
        if not actions or any(row.keys() != actions for row in self.payoffs.values()):
            raise ValueError("each state must contain the same nonempty set of actions")
        return self


class Robust(_Table):
    """Compare actions across scenarios without assigning probabilities."""

    def calculate(self) -> dict[str, object]:
        """Compute maximin payoff, minimax regret and a binary switch point."""
        rows = self.payoffs
        actions = next(iter(rows.values()))
        bests = {s: max(row.values()) for s, row in rows.items()}
        regret = {a: max(bests[s] - row[a] for s, row in rows.items()) for a in actions}
        floors = {a: min(row[a] for row in rows.values()) for a in actions}
        return {
            "unit": self.unit,
            "worst_regret": regret,
            "worst_payoff": floors,
            "minimax_regret_actions": [
                a for a, v in regret.items() if v == min(regret.values())
            ],
            "maximin_actions": [
                a for a, v in floors.items() if v == max(floors.values())
            ],
            "switch_points": self._switch_points(),
        }

    def _switch_points(self) -> list[dict[str, object]]:
        rows = self.payoffs
        if len(rows) != 2 or len(next(iter(rows.values()))) != 2:
            return []
        first, second = rows
        a, b = rows[first]
        d0 = rows[first][a] - rows[first][b]
        d1 = rows[second][a] - rows[second][b]
        if d0 == d1 or (d0 * d1) > 0:
            return []
        return [
            {
                "state": first,
                "probability": d1 / (d1 - d0),
                "above": a if d0 > d1 else b,
                "below": b if d0 > d1 else a,
            }
        ]


class Check(Inputs):
    """An imperfect observation priced in the decision's payoff unit."""

    name: Name
    cost: Nonnegative
    likelihoods: dict[Name, dict[Name, Probability]] = Field(
        description="State -> observation -> conditional probability. Zeros are valid."
    )

    @model_validator(mode="after")
    def _rows(self) -> Self:
        for row in self.likelihoods.values():
            _validate_probabilities(row)
        labels = next(iter(self.likelihoods.values()), None)
        if not labels or any(
            row.keys() != labels.keys() for row in self.likelihoods.values()
        ):
            raise ValueError(
                "use the same nonempty set of outcome labels in every state"
            )
        return self

    def branches(self, prior: Weights) -> dict[str, tuple[float, Weights]]:
        """Return the probability and updated state weights of each possible outcome."""
        result: dict[str, tuple[float, Weights]] = {}
        for label in next(iter(self.likelihoods.values())):
            joint = {s: p * self.likelihoods[s][label] for s, p in prior.items()}
            chance = fsum(joint.values())
            if chance > 0:
                result[label] = (chance, {s: v / chance for s, v in joint.items()})
        return result


@dataclass
class _Policy:
    value: float
    tree: dict[str, object]


def _policy(
    rows: Payoffs, prior: Weights, checks: list[Check], depth: int, budget: float
) -> _Policy:
    action, baseline = _best(prior, rows)
    winner = _Policy(baseline, {"action": action, "value": baseline})
    if depth == 0:
        return winner
    for check in checks:
        if check.cost > budget:
            continue
        remaining = [x for x in checks if x.name != check.name]
        branches = check.branches(prior)
        children = {
            k: _policy(
                rows,
                w,
                remaining,
                depth - 1,
                float(Decimal(str(budget)) - Decimal(str(check.cost))),
            )
            for k, (_, w) in branches.items()
        }
        value = (
            fsum(p * children[k].value for k, (p, _) in branches.items()) - check.cost
        )
        if value > winner.value and not isclose(
            value,
            winner.value,
            rel_tol=0,
            abs_tol=4 * max(ulp(value), ulp(winner.value)),
        ):
            winner = _Policy(
                value,
                {
                    "check": check.name,
                    "value": value,
                    "after": {k: v.tree for k, v in children.items()},
                    "probabilities": {k: v[0] for k, v in branches.items()},
                },
            )
    return winner


class Decision(_Table):
    """Compare actions, price imperfect observations and select a bounded policy."""

    probabilities: dict[Name, Probability]
    partition: dict[Name, Name] | None = Field(
        default=None,
        description="State -> observable group for partial perfect information.",
    )
    checks: list[Check] = Field(default_factory=list)
    depth: Literal[0, 1, 2] = 1
    budget: Nonnegative | None = None
    conditionally_independent: bool = False

    @model_validator(mode="after")
    def _coherent(self) -> Self:
        _validate_probabilities(self.probabilities)
        maps = [set(self.probabilities), *(set(c.likelihoods) for c in self.checks)]
        if self.partition is not None:
            maps.append(set(self.partition))
        if any(keys != self.payoffs.keys() for keys in maps):
            raise ValueError("state labels must match the payoff table")
        if len({c.name for c in self.checks}) != len(self.checks):
            raise ValueError("check names must be unique")
        if (
            self.depth == 2
            and len(self.checks) > 1
            and not self.conditionally_independent
        ):
            raise ValueError(
                "declare conditional independence of checks given each state"
            )
        return self

    def _price(self, check: Check, baseline: float) -> dict[str, object]:
        outcomes: dict[str, object] = {}
        gains: list[float] = []
        for label, (chance, weights) in check.branches(self.probabilities).items():
            action, value = _best(weights, self.payoffs)
            outcomes[label] = {
                "probability": chance,
                "posterior": weights,
                "action": action,
                "value": value,
            }
            gains.append(chance * value)
        value = fsum(gains) - baseline
        return {
            "cost": check.cost,
            "evsi": value,
            "net_value": value - check.cost,
            "outcomes": outcomes,
        }

    def _partial(self, partition: dict[str, str], baseline: float) -> float:
        groups: dict[str, Weights] = {}
        for state, group in partition.items():
            groups.setdefault(group, {})[state] = self.probabilities[state]
        return (
            fsum(_best(weights, self.payoffs)[1] for weights in groups.values())
            - baseline
        )

    def calculate(self) -> dict[str, object]:
        """Return expected payoffs, information values and the selected action tree."""
        weights = self.probabilities
        action, value = _best(weights, self.payoffs)
        evpi = (
            fsum(p * max(self.payoffs[s].values()) for s, p in weights.items()) - value
        )
        cap = float("inf") if self.budget is None else self.budget
        return {
            "unit": self.unit,
            "act_now": action,
            "value_now": value,
            "evpi": evpi,
            "expected_payoffs": {
                a: fsum(p * self.payoffs[s][a] for s, p in weights.items())
                for a in self.payoffs[next(iter(weights))]
            },
            "evppi": None
            if self.partition is None
            else self._partial(self.partition, value),
            "checks": {c.name: self._price(c, value) for c in self.checks},
            "policy": _policy(self.payoffs, weights, self.checks, self.depth, cap).tree,
        }


class BreakEven(Request):
    """Price a probe from equal-weight conditional savings draws and its fixed cost."""

    unit: Name
    cost: Nonnegative
    gains_if_success: Annotated[list[Nonnegative], Field(min_length=1)]

    def calculate(self) -> dict[str, object]:
        """Compute the threshold given zero gain on an unsuccessful probe."""
        import numpy as np

        mean = float(np.mean(self.gains_if_success))
        threshold = self.cost / mean if mean else None
        return {
            "unit": self.unit,
            "mean_gain_if_success": mean,
            "break_even_probability": threshold,
            "positive_net_possible": mean > self.cost,
            "gain_quantiles_10_50_90": np.quantile(
                self.gains_if_success, [0.1, 0.5, 0.9]
            ).tolist(),
        }
