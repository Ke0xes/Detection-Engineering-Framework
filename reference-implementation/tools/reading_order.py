#!/usr/bin/env python3
"""Keep each chapter's position markers in step with the site navigation.

The navigation in mkdocs.yml is the single source of reading order. From it this
tool generates, in every chapter on the reading path:

* a "where you are" line under the title, and
* previous / next links at the end, for readers on GitHub.

Usage:
    python reference-implementation/tools/reading_order.py          # rewrite
    python reference-implementation/tools/reading_order.py --check  # CI gate
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MKDOCS = REPO_ROOT / "mkdocs.yml"

# Sections of the navigation that form the reading path. Anything else, such
# as project governance documents, gets no position markers.
READING_PARTS = (
    "Understand the framework",
    "Walk the lifecycle",
    "Put it into practice",
    "Reference",
)

# Fill-in templates and portable packages are copied by readers; navigation
# text would be noise in them.
SKIP_FILES = {
    "tools-and-templates/templates/use-case-requests/use-case-request-template.md",
    "skills/senior-detection-engineer/README.md",
}

DEEP_DIVE_PREFIX = "Going deeper: "

TOP_START, TOP_END = "<!-- journey:where -->", "<!-- /journey:where -->"
END_START, END_END = "<!-- journey:next -->", "<!-- /journey:next -->"

LEGACY_BREADCRUMB = re.compile(r"^\*\[Framework index\]\([^)]*\)[^\n]*\*\s*\n\n?", re.MULTILINE)
LEGACY_FOOTER = re.compile(r"\n+---\s*\n+\*(?:Next|Previous):[^\n]*\*\s*$")
TOP_BLOCK = re.compile(re.escape(TOP_START) + r".*?" + re.escape(TOP_END) + r"\n*", re.DOTALL)
END_BLOCK = re.compile(r"\n*" + re.escape(END_START) + r".*?" + re.escape(END_END) + r"\s*$", re.DOTALL)


class _NavLoader(yaml.SafeLoader):
    """SafeLoader that ignores the python/name tags used by markdown extensions."""


_NavLoader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def walk(entries: list, trail: tuple[str, ...]):
    for entry in entries:
        for title, value in entry.items():
            if isinstance(value, list):
                yield from walk(value, trail + (title,))
            else:
                yield trail, title, value


def reading_path() -> list[dict]:
    config = yaml.load(MKDOCS.read_text(encoding="utf-8"), Loader=_NavLoader)
    pages = []
    for trail, title, file in walk(config["nav"], ()):
        if not trail or trail[0] not in READING_PARTS or file in SKIP_FILES:
            continue
        pages.append({"trail": trail, "title": title, "file": file})
    return pages


def where_line(page: dict) -> str:
    parts = list(page["trail"])
    if page["title"].startswith(DEEP_DIVE_PREFIX):
        parts.append("Going deeper")
    elif len(parts) == 1 and page["file"] != "README.md":
        parts.append(page["title"])
    return "*" + " › ".join(parts) + "*"


def link(from_file: str, page: dict) -> str:
    target = posixpath.relpath(page["file"], posixpath.dirname(from_file) or ".")
    return f"[{page['title']}]({target})"


def end_block(index: int, pages: list[dict]) -> str:
    page = pages[index]
    links = []
    if index > 0:
        links.append(f"**Previous:** {link(page['file'], pages[index - 1])}")
    if index + 1 < len(pages):
        links.append(f"**Next:** {link(page['file'], pages[index + 1])}")
    else:
        links.append(f"**Back to the start:** {link(page['file'], pages[0])}")
    # Hidden on the rendered site, which draws its own footer from the same navigation.
    return (
        f"{END_START}\n"
        f'<div class="journey-footer" markdown>\n\n'
        f"---\n\n"
        f"{' · '.join(links)}\n\n"
        f"</div>\n"
        f"{END_END}\n"
    )


def render(text: str, index: int, pages: list[dict]) -> str:
    page = pages[index]
    text = LEGACY_BREADCRUMB.sub("", text, count=1)
    text = LEGACY_FOOTER.sub("\n", text)
    text = TOP_BLOCK.sub("", text, count=1)
    text = END_BLOCK.sub("\n", text).rstrip() + "\n"

    if page["file"] != "README.md":
        lines = text.split("\n")
        h1 = next(i for i, line in enumerate(lines) if line.startswith("# "))
        block = [TOP_START, where_line(page), TOP_END, ""]
        rest = lines[h1 + 1:]
        while rest and not rest[0].strip():
            rest.pop(0)
        text = "\n".join(lines[: h1 + 1] + [""] + block + rest)

    return text.rstrip() + "\n\n" + end_block(index, pages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if any chapter is out of date")
    args = parser.parse_args()

    pages = reading_path()
    stale = []
    for index, page in enumerate(pages):
        path = REPO_ROOT / page["file"]
        current = path.read_text(encoding="utf-8")
        expected = render(current, index, pages)
        if current != expected:
            stale.append(page["file"])
            if not args.check:
                path.write_text(expected, encoding="utf-8", newline="\n")

    if args.check:
        for file in stale:
            print(f"OUT OF DATE  {file}")
        print(f"\n{len(pages)} chapter(s) on the reading path, {len(stale)} out of date")
        if stale:
            print("Run: python reference-implementation/tools/reading_order.py")
        return 1 if stale else 0

    for file in stale:
        print(f"updated  {file}")
    print(f"\n{len(pages)} chapter(s) on the reading path, {len(stale)} updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
