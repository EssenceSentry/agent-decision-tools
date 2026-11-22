"""Adapter to the skill's local, pinned Squiggle interpreter."""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Annotated

from pydantic import Field

from .models import Name, Request


def _runner() -> Path:
    name = "bayesian-fermi-estimation"
    configured = os.getenv("FERMI_SKILL_DIR")
    candidates = (
        [Path(configured)]
        if configured
        else [
            Path(__file__).resolve().parents[2] / "skills" / name,
            Path.home() / ".codex/skills" / name,
            Path.home() / ".claude/skills" / name,
        ]
    )
    for folder in candidates:
        script = folder / "scripts/run.mjs"
        if script.is_file():
            return script
    raise ValueError("Fermi runtime missing: install the skill or set FERMI_SKILL_DIR")


class Fermi(Request):
    """Run a grounded forward estimate in Squiggle and optionally export draws."""

    source: Name = Field(
        description="One Squiggle program ending in the desired value."
    )
    unit: Name
    samples: Annotated[int, Field(ge=6)] = 1000
    seed: Name = "42"
    draws: bool = False
    timeout_seconds: Annotated[float, Field(gt=0)] = 10.0

    def calculate(self) -> dict[str, object]:
        """Evaluate the program in the pinned runtime with the requested time cap."""
        runner = _runner()
        node = shutil.which("node")
        if not node:
            raise ValueError("Node.js 22 or newer is needed for the Fermi runtime")
        args = [node, str(runner), "--samples", str(self.samples), "--seed", self.seed]
        if self.draws:
            args.append("--draws")
        try:
            # A fixed interpreter and script read the Squiggle source on stdin.
            result = subprocess.run(  # noqa: S603 - argv never enters a shell
                args,
                input=self.source,
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise ValueError("Fermi estimate exceeded the time cap") from error
        if result.returncode:
            raise ValueError(f"Squiggle runtime error: {result.stderr.strip()}")
        return {"unit": self.unit, **json.loads(result.stdout)}
