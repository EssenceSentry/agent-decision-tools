"""Exercise linking just the selected skill into both project registries."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "compare-rival-approaches"


def link(project: Path, *names: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603 -- invokes the local installer in a temporary project
        [
            sys.executable,
            str(ROOT / "scripts/link_skills.py"),
            "--project",
            str(project),
            "--host",
            "both",
            *names,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_only_selected_skill_is_linked_idempotently(tmp_path: Path) -> None:
    for _ in range(2):
        result = link(tmp_path, NAME)
        assert result.returncode == 0, result.stderr
    for host in (".agents", ".claude"):
        registry = tmp_path / host / "skills"
        assert [p.name for p in registry.iterdir()] == [NAME]
        assert (registry / NAME).resolve() == ROOT / "skills" / NAME
        assert (registry / NAME / "references/field-notes.md").is_file()


def test_collision_preserves_both_registries(tmp_path: Path) -> None:
    existing = tmp_path / ".claude/skills" / NAME
    existing.mkdir(parents=True)
    (existing / "user.md").write_text("local edits")
    assert link(tmp_path, NAME).returncode != 0
    assert (existing / "user.md").read_text() == "local edits"
    assert not (tmp_path / ".agents/skills" / NAME).exists()


def test_unknown_name_has_no_side_effects(tmp_path: Path) -> None:
    assert link(tmp_path, NAME, "../skills").returncode != 0
    assert list(tmp_path.iterdir()) == []
