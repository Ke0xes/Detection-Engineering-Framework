#!/usr/bin/env python3
"""Verify every repository link resolves, and that no emoji crept back in.

Covers relative links and absolute links to this repository's main branch.
The documentation site cannot enforce this on its own: chapters deliberately
link to schemas, fixtures and tooling that are excluded from the rendered site.
This checker covers the whole repository instead.

Exit code 0 means clean. Any non-zero exit fails CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".venv", "venv", "site", "node_modules", ".git", "__pycache__"}

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
EXTERNAL = ("http://", "https://", "mailto:", "#", "tel:")

# Absolute links to this repository's default branch. Checked against the working
# tree, because files new in a pull request do not exist on main until it merges.
SELF_LINK = re.compile(
    r"^https://github\.com/Ke0xes/Detection-Engineering-Framework/(?:blob|tree)/main/([^#?]*)"
)


def resolve_target(path: Path, target: str) -> Path | None:
    """Return the local path a link points at, or None if it is not a repository link."""
    self_link = SELF_LINK.match(target)
    if self_link:
        return REPO_ROOT / self_link.group(1)
    if target.startswith(EXTERNAL):
        return None
    file_part = target.split("#")[0]
    return (path.parent / file_part).resolve() if file_part else None


def main() -> int:
    broken: list[str] = []
    emoji_hits: list[str] = []

    for path in sorted(REPO_ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue

        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")

        for match in EMOJI.finditer(text):
            emoji_hits.append(f"{rel}: {match.group()!r}")

        for _, target in LINK.findall(text):
            local = resolve_target(path, target)
            if local is not None and not local.exists():
                broken.append(f"{rel}  ->  {target}")

    for line in broken:
        print(f"BROKEN LINK  {line}")
    for line in emoji_hits:
        print(f"EMOJI        {line}")

    print(f"\n{len(broken)} broken repository link(s), {len(emoji_hits)} emoji occurrence(s)")
    return 1 if (broken or emoji_hits) else 0


if __name__ == "__main__":
    raise SystemExit(main())
