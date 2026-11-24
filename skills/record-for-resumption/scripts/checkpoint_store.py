"""Storage format shared by registration, capture and recovery."""

import hashlib
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path

SNAPSHOT = re.compile(r"[a-f0-9]{32}\.md")
SESSION = re.compile(r"(claude|codex)-[a-f0-9]{24}")
LIMITS = {"progress": (0, 8), "keep": (1, 100), "max-age-days": (1, 3650)}


def digest(value):
    """Hash UTF-8 text using the existing checkpoint naming convention."""
    return hashlib.sha256(str(value).encode()).hexdigest()


def state_dir():
    """Return the per-user default recovery directory."""
    home = os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state"
    return Path(home) / "agent-process/checkpoints"


def checked_limits(args):
    """Validate explicitly supplied snapshot limits."""
    result = {}
    for name, (low, high) in LIMITS.items():
        value = getattr(args, name.replace("-", "_"))
        if value is not None:
            if not low <= int(value) <= high:
                raise ValueError(f"--{name} takes a whole number from {low} to {high}")
            result[name] = int(value)
    return result


def atomic_text(path, content, mode=0o600):
    """Publish a complete file by replacing it inside its own directory."""
    with tempfile.NamedTemporaryFile(
        dir=path.parent, mode="w", encoding="utf-8", suffix=".tmp", delete=False
    ) as stream:
        tmp = Path(stream.name)
        try:
            os.chmod(tmp, mode)
            stream.write(content)
            stream.close()
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)


@contextmanager
def locked(project_state):
    """Serialize readers, publication and pruning for one project."""
    project_state.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (project_state / ".lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt

            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def owned(path):
    """Recognize only regular checkpoint files and their temporary writes."""
    return (
        not path.is_symlink()
        and path.is_file()
        and (
            path.name == "latest"
            or SNAPSHOT.fullmatch(path.name)
            or path.suffix == ".tmp"
        )
    )


def prune(directory, current, keep, cutoff):
    """Expire only recognized, stale sessions and excess local snapshots."""
    snapshots = sorted(
        (
            p
            for p in directory.iterdir()
            if p.name != current and SNAPSHOT.fullmatch(p.name) and owned(p)
        ),
        key=lambda p: p.stat().st_mtime_ns,
        reverse=True,
    )
    for p in snapshots[keep - 1 :]:
        p.unlink()
    for session in directory.parent.iterdir():
        if (
            session == directory
            or not SESSION.fullmatch(session.name)
            or session.is_symlink()
            or not session.is_dir()
        ):
            continue
        contents = list(session.iterdir())
        if all(owned(p) and p.stat().st_mtime < cutoff for p in contents):
            for p in contents:
                p.unlink()
            session.rmdir()
