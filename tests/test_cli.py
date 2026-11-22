import io
import json

from agent_decision_tools.cli import main


def test_cli_discovery(capsys):
    assert main(["list"]) == 0
    assert "decide" in json.loads(capsys.readouterr().out)
    assert main(["schema", "interim"]) == 0
    assert "looks" in json.loads(capsys.readouterr().out)["properties"]


def test_run_file_and_stdin(capsys, monkeypatch):
    assert main(["run", "decide", "examples/defect.json"]) == 0
    assert json.loads(capsys.readouterr().out)["act_now"] == "leave"
    monkeypatch.setattr("sys.stdin", io.StringIO("{"))
    assert main(["run", "decide", "-"]) == 2
    assert "error" in json.loads(capsys.readouterr().err)
