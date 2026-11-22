import json
from pathlib import Path

import pytest

from agent_decision_tools import evaluate, schema, tools

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def calculate(tool, payload):
    # Round-trip every result through the public JSON interchange.
    return json.loads(json.dumps(evaluate(tool, payload), allow_nan=False))


def example(name):
    return json.loads((EXAMPLES / f"{name}.json").read_text())


def test_price_defect_check():
    result = calculate("decide", example("defect"))
    assert result["act_now"] == "leave"
    assert result["evpi"] == pytest.approx(2.4)
    assert result["evppi"] == pytest.approx(2.4)
    check = result["checks"]["inspect"]
    assert check["evsi"] == pytest.approx(1.6)
    assert check["net_value"] == pytest.approx(1.35)
    assert check["outcomes"]["positive"]["action"] == "prevent"
    assert check["outcomes"]["negative"]["action"] == "leave"
    assert check["outcomes"]["positive"]["posterior"]["defect"] == pytest.approx(2 / 3)


def test_two_look_policy_buys_a_pilot_only_with_followup():
    data = example("pilot")
    full = calculate("decide", data)["policy"]
    assert full["check"] == "pilot"
    assert full["after"]["flag"]["check"] == "confirm"
    assert full["after"]["clear"]["action"] == "ship"
    assert calculate("decide", dict(data, depth=1))["policy"]["action"] == "ship"
    assert calculate("decide", dict(data, budget=0))["policy"]["action"] == "ship"


def test_sensitivity_without_probabilities():
    report = calculate("robust", example("risk"))
    assert report["minimax_regret_actions"] == ["prevent"]
    assert report["worst_regret"] == {"leave": 12, "prevent": 4}
    assert report["switch_points"][0]["probability"] == pytest.approx(0.25)


def test_fermi_distribution_prices_a_probe():
    result = calculate("breakeven", example("probe"))
    assert result["mean_gain_if_success"] == 120
    assert result["break_even_probability"] == pytest.approx(1 / 6)


def test_schedule_reserves_verification_and_respects_dependencies():
    result = calculate("schedule", example("jobs"))
    chosen = result["jobs"]
    assert set(chosen) == {"inspect", "benchmark"}
    assert chosen["inspect"]["end"] <= chosen["benchmark"]["start"]
    assert chosen["benchmark"]["end"] <= 8
    assert result["value"] == 8


def test_panel_and_calibration():
    assert calculate("panel", example("opinions"))["median"] == pytest.approx(0.45)
    result = calculate("calibrate", example("forecasts"))
    assert result["brier"]["A"] == pytest.approx(0.04)
    assert result["brier"]["equal_pool"] == pytest.approx(0.1225)


def test_interim_on_a_scheduled_look():
    result = calculate("interim", example("interim"))
    assert result["decision"] == "above_threshold"
    assert result["interval"][0] > 0.5


def test_discovery_and_validation():
    assert set(tools()) == {
        "fermi",
        "decide",
        "robust",
        "breakeven",
        "interim",
        "panel",
        "calibrate",
        "schedule",
        "revisit",
    }
    properties = schema("decide")["properties"]
    assert isinstance(properties, dict)
    assert "payoffs" in properties
    with pytest.raises(ValueError, match="Unknown tool"):
        calculate("unknown", {})
    with pytest.raises(ValueError, match="sum to one"):
        calculate(
            "decide",
            dict(example("defect"), probabilities={"defect": 0.2, "clean": 0.2}),
        )


def test_small_payoff_units_preserve_the_choice_and_cost_cap():
    data = example("pilot")
    for row in data["payoffs"].values():
        for action in row:
            row[action] *= 1e-15
    for check in data["checks"]:
        check["cost"] *= 1e-15
    data["budget"] = 9.01e-16
    assert calculate("decide", data)["policy"]["check"] == "pilot"


def test_cost_cap_excludes_only_unaffordable_paths():
    data = example("pilot")
    assert "action" in calculate("decide", dict(data, budget=0.899))["policy"]
    assert calculate("decide", data)["policy"]["after"]["flag"]["check"] == "confirm"
    with pytest.raises(ValueError, match="independence"):
        calculate("decide", dict(data, conditionally_independent=False))


def test_a_certain_observation_has_zero_value():
    data = example("defect")
    data["partition"] = dict.fromkeys(data["probabilities"], "same")
    check = data["checks"][0]
    check["likelihoods"] = {
        state: {"known": 1, "impossible": 0} for state in data["probabilities"]
    }
    report = calculate("decide", data)
    assert report["evppi"] == pytest.approx(0)
    assert report["checks"]["inspect"]["evsi"] == pytest.approx(0)
    assert set(report["checks"]["inspect"]["outcomes"]) == {"known"}
    assert "action" in report["policy"]


def test_scenarios_with_identical_payoffs_and_zero_gain():
    data = example("risk")
    data["payoffs"] = {"A": {"x": 1, "y": 1}, "B": {"x": 0, "y": 0}}
    report = calculate("robust", data)
    assert report["switch_points"] == []
    assert report["minimax_regret_actions"] == ["x", "y"]
    result = calculate("breakeven", dict(example("probe"), gains_if_success=[0, 0]))
    assert result["break_even_probability"] is None
    assert not result["positive_net_possible"]


@pytest.mark.parametrize(
    ("n", "k", "expected"),
    [(10, 0, "below_threshold"), (10, 5, "continue"), (20, 10, "unresolved_at_cap")],
)
def test_uncertainty_at_interim_looks(n, k, expected):
    data = dict(
        example("interim"), looks=[10, 20], trials=n, successes=k, threshold=0.5
    )
    assert calculate("interim", data)["decision"] == expected


@pytest.mark.parametrize(
    ("overrides", "message"),
    [({"trials": 3}, "predeclared"), ({"successes": 2000}, "cannot exceed")],
)
def test_interim_requires_a_valid_design(overrides, message):
    with pytest.raises(ValueError, match=message):
        calculate("interim", {**example("interim"), **overrides})


def test_only_paired_forecasts_have_comparable_scores():
    data = example("forecasts")
    del data["records"][0]["forecasts"]["A"]
    with pytest.raises(ValueError, match="paired"):
        calculate("calibrate", data)
    data = example("forecasts")
    data["records"] *= 2
    with pytest.raises(ValueError, match="unique"):
        calculate("calibrate", data)


def test_schedule_checks_feasibility_and_allows_parallel_resources():
    data = example("jobs")
    data["jobs"]["inspect"]["requires"] = ["missing"]
    with pytest.raises(ValueError, match="unknown dependency"):
        calculate("schedule", data)
    data["jobs"]["inspect"]["requires"] = ["benchmark"]
    with pytest.raises(ValueError, match="cycle"):
        calculate("schedule", data)
    data = example("jobs")
    assert calculate("schedule", dict(data, reserve=10))["jobs"] == {}
    with pytest.raises(ValueError, match="reserve"):
        calculate("schedule", dict(data, reserve=11))
    data["jobs"]["alternative"]["resource"] = "another worker"
    assert calculate("schedule", data)["value"] == 12
