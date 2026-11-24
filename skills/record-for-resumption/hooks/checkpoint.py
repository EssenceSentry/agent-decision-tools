#!/usr/bin/env python3
"""Capture the owning record and public assistant messages on PreCompact."""

import argparse
import json
import os
import re
import stat
import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import checkpoint_store as store

HANDOFF = re.compile(r"^```handoff-state[^\S\n]*\n(.*?)^```[^\S\n]*$", re.M | re.S)


def tail(path, size):
    """Read at most size bytes, even for large host transcripts."""
    if not path or not stat.S_ISREG(Path(path).stat().st_mode):
        return ""
    with Path(path).open("rb") as stream:
        stream.seek(max(0, os.fstat(stream.fileno()).st_size - size))
        return stream.read(size).decode("utf-8", errors="replace")


def assistant_text(row):
    """Select visible assistant text from supported host envelopes."""
    if not isinstance(row, dict):
        return ""
    kind = row.get("type")
    payload = row.get("payload")
    if (
        kind == "event_msg"
        and isinstance(payload, dict)
        and payload.get("type") == "agent_message"
    ):
        return payload.get("message")
    message = (
        row.get("message")
        if kind == "assistant"
        else payload
        if kind == "response_item"
        else None
    )
    if (
        not isinstance(message, dict)
        or message.get("role") != "assistant"
        or message.get("channel") == "analysis"
    ):
        return ""
    parts = message.get("content")
    if not isinstance(parts, list):
        return ""
    return "\n".join(
        p["text"]
        for p in parts
        if isinstance(p, dict)
        and p.get("type") in ("text", "output_text")
        and isinstance(p.get("text"), str)
    )


def progress(path, limit):
    """Extract the latest handoff and a bounded number of distinct excerpts."""
    notes = deque(maxlen=limit)
    marked = ""
    try:
        contents = tail(path, 4 * 1024 * 1024)
    except OSError:
        contents = ""
    for line in contents.splitlines():
        try:
            text = assistant_text(json.loads(line))
        except ValueError:
            continue
        if not isinstance(text, str) or not text.strip():
            continue
        for match in HANDOFF.finditer(text):
            marked = match[1].strip()[-12000:]
        excerpt = text.strip()[-2400:]
        if not notes or notes[-1] != excerpt:
            notes.append(excerpt)
    return notes, marked


def checkpoint(event, args):
    """Publish a content-addressed recovery file and a session pointer."""
    if event.get("hook_event_name") != "PreCompact" or event.get("trigger") not in (
        "auto",
        "manual",
    ):
        return
    if (
        not isinstance(event.get("session_id"), str)
        or not event["session_id"]
        or not event.get("cwd")
    ):
        raise ValueError("Missing host session or working directory")
    limits = store.checked_limits(args)
    project = args.project.resolve(strict=True)
    if not Path(event["cwd"]).resolve(strict=True).is_relative_to(project):
        return
    sections = ["# Resume checkpoint", "", f"Project: {project}"]
    if args.record:
        record = (project / args.record).resolve()
        if not record.is_relative_to(project):
            raise ValueError("The owning record resolves outside the project")
        if record.is_file() and (content := tail(record, 32768).strip()):
            sections.extend(
                ("", f"## Owning record ({args.record}, last 32 KiB)", "", content)
            )
    limit = limits.get("progress", 3)
    notes, marked = progress(event.get("transcript_path"), limit)
    if marked:
        sections.extend(("", "## Latest explicit handoff", "", marked))
    if notes:
        sections.extend(
            (
                "",
                "## Recent progress reported by the assistant",
                "",
                f"Up to {limit} recent visible assistant messages from the final "
                "4 MiB of JSONL. Check primary artifacts before acting.",
                "",
                *notes,
            )
        )
    if len(sections) == 3:
        print(
            "Checkpoint has no readable record or supported assistant messages. "
            "Earlier snapshots are preserved.",
            file=sys.stderr,
        )
        return
    content = "\n".join(sections) + "\n"
    root = args.state_dir / store.digest(project)
    session = root / (args.host + "-" + store.digest(event["session_id"])[:24])
    saved = session / (store.digest(content)[:32] + ".md")
    with store.locked(root):
        session.mkdir(exist_ok=True, mode=0o700)
        store.atomic_text(saved, content)
        store.atomic_text(session / "latest", saved.name + "\n")
        try:
            store.prune(
                session,
                saved.name,
                limits.get("keep", 5),
                time.time() - limits.get("max-age-days", 30) * 86400,
            )
        except OSError as error:
            print(f"Older checkpoints were not pruned: {error}", file=sys.stderr)
    if args.host == "claude":
        print(
            f"Preserve the current decision, failed approaches and next action. "
            f"A recovery copy is at {saved}"
        )
    else:
        print(json.dumps({"systemMessage": f"Recovery copy saved to {saved}"}))


def main():
    """Read one host event from standard input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--record")
    parser.add_argument("--state-dir", type=Path, required=True)
    for name in store.LIMITS:
        parser.add_argument("--" + name)
    checkpoint(json.load(sys.stdin), parser.parse_args())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(f"Could not save resume checkpoint: {error}")
