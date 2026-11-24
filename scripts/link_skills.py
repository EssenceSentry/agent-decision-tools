"""Make selected local skills discoverable by Codex or Claude Code."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "skills"


def registries(host: str, project: Path | None) -> list[Path]:
    """Return the requested per-project or per-user skill registries."""
    if project is None:
        codex = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
        claude = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    else:
        if not project.is_dir():
            raise ValueError(f"Project directory does not exist: {project}")
        codex, claude = project / ".agents", project / ".claude"
    roots = {"codex": [codex], "claude": [claude], "both": [codex, claude]}
    return [root / "skills" for root in roots[host]]


def install(folders: list[Path], skills: list[Path]) -> None:
    """Check every destination before linking any skill; preserve existing installs."""
    links = [(folder / skill.name, skill) for folder in folders for skill in skills]
    for target, source in links:
        if (target.is_symlink() or target.exists()) and target.resolve() != source:
            raise ValueError(f"Existing skill at {target}. Kept its contents.")
    for target, source in links:
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            target.symlink_to(source, target_is_directory=True)
        except FileExistsError:
            if target.resolve() != source:
                raise
        print(target)


def main() -> int:
    """Link only named skills, or the entire collection on explicit request."""
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path)
    scope.add_argument("--user", action="store_true")
    parser.add_argument("--host", required=True, choices=("claude", "codex", "both"))
    parser.add_argument("--all", action="store_true", help="link every available skill")
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    available = {p.parent.name: p.parent for p in sorted(SKILLS.glob("*/SKILL.md"))}
    if args.all == bool(args.names):
        parser.error("Supply one or more skill names or --all.")
    names = list(available) if args.all else list(dict.fromkeys(args.names))
    unknown = set(names).difference(available)
    if unknown:
        parser.error(f"Unknown skills: {', '.join(sorted(unknown))}")
    try:
        install(registries(args.host, args.project), [available[n] for n in names])
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
