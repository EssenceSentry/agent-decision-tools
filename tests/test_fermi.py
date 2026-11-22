import json
import subprocess
from pathlib import Path

import pytest

from agent_decision_tools import evaluate


def test_real_fermi_and_bridge(monkeypatch):
    skill = Path("skills/bayesian-fermi-estimation").resolve()
    if not (skill / "node_modules/@quri/squiggle-lang").is_dir():
        pytest.skip("Run npm ci in the skill directory for the Node integration.")
    monkeypatch.setenv("FERMI_SKILL_DIR", str(skill))
    data = {
        "basis": "Synthetic percentile anchoring example",
        "source": Path("examples/probe.squiggle").read_text(),
        "unit": "minutes",
        "samples": 1000,
        "draws": True,
    }
    estimate = json.loads(json.dumps(evaluate("fermi", data)))
    result = evaluate(
        "breakeven",
        {
            "basis": data["basis"],
            "unit": "minutes",
            "cost": 20,
            "gains_if_success": estimate["value"]["draws"],
        },
    )
    assert result["break_even_probability"] == pytest.approx(0.144, abs=0.015)


def test_fermi_failure_is_actionable(monkeypatch, tmp_path):
    monkeypatch.setenv("FERMI_SKILL_DIR", str(tmp_path))
    with pytest.raises(ValueError, match="runtime"):
        evaluate("fermi", {"basis": "fixture", "unit": "hours", "source": "1"})
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/run.mjs").write_text("")
    monkeypatch.setattr("shutil.which", lambda _: "node")

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("node", 1)

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(ValueError, match="time cap"):
        evaluate("fermi", {"basis": "fixture", "unit": "hours", "source": "1"})
