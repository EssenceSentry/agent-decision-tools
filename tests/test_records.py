import json
from pathlib import Path

from agent_decision_tools import evaluate


def test_reopening_a_decision_and_missing_signals():
    data = json.loads(Path("examples/signposts.json").read_text())
    out = evaluate("revisit", data)
    assert out["triggered"] == ["volume"]
    assert out["missing"] == ["cost"]
    assert isinstance(out["record"], str)
    assert "retry count" in out["record"]
    assert (
        evaluate(
            "revisit", dict(data, observations={"weekly_requests": 0, "unit_cost": 0})
        )["status"]
        == "keep"
    )
