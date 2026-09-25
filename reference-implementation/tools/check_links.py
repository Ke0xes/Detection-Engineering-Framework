#!/usr/bin/env python3
"""Verify every relative link in the repository resolves, and that no emoji crept back in.

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
            if target.startswith(EXTERNAL):
                continue
            file_part = target.split("#")[0]
            if not file_part:
                continue
            if not (path.parent / file_part).resolve().exists():
                broken.append(f"{rel}  ->  {target}")

    for line in broken:
        print(f"BROKEN LINK  {line}")
    for line in emoji_hits:
        print(f"EMOJI        {line}")

    print(f"\n{len(broken)} broken relative link(s), {len(emoji_hits)} emoji occurrence(s)")
    return 1 if (broken or emoji_hits) else 0


if __name__ == "__main__":
    raise SystemExit(main())
