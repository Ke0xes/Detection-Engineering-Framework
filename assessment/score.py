#!/usr/bin/env python3
"""Score a Detection Engineering Framework self-assessment.

Reads the instrument CSV, computes level attainment and emits a conformance
statement. Levels are cumulative and all-or-nothing: a level is attained only
when every requirement at that level and below is scored 'met' or is a
justified 'n/a' (CNF-2).

Usage:
    python assessment/score.py assessment/self-assessment.csv
    python assessment/score.py assessment/self-assessment.csv --scope "Corporate IT estate"
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

SPEC_VERSION = "3.0.0"
LEVELS = ["L1", "L2", "L3"]
VALID_SCORES = {"met", "partial", "not-met", "n/a", ""}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--scope", default="<STATE YOUR SCOPE>",
                        help="Scope of the assessed environment, including exclusions.")
    args = parser.parse_args()

    if not args.csv_path.is_file():
        print(f"Instrument not found: {args.csv_path}")
        return 2

    by_level: dict[str, list[dict]] = defaultdict(list)
    malformed: list[str] = []

    with args.csv_path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            level = (row.get("level") or "").strip()
            score = (row.get("score") or "").strip().lower()
            rid = (row.get("requirement_id") or "?").strip()

            if level not in LEVELS:
                malformed.append(f"{rid}: unknown level {level!r}")
                continue
            if score not in VALID_SCORES:
                malformed.append(f"{rid}: invalid score {score!r}")
                continue

            row["score"] = score
            by_level[level].append(row)

    if malformed:
        print("Instrument problems:")
        for line in malformed:
            print(f"  {line}")
        print()

    # CNF-5 and CNF-6: claims need evidence, and n/a needs justification.
    integrity: list[str] = []
    for level in LEVELS:
        for row in by_level[level]:
            rid = row["requirement_id"]
            if row["score"] == "met" and not (row.get("evidence") or "").strip():
                integrity.append(f"CNF-5  {rid} scored 'met' with no evidence recorded")
            if row["score"] == "n/a" and not (row.get("notes") or "").strip():
                integrity.append(f"CNF-6  {rid} scored 'n/a' with no justification recorded")

    print(f"Detection Engineering Framework v{SPEC_VERSION} — self-assessment\n")
    print(f"{'Level':<6} {'Met':>5} {'Partial':>8} {'Not met':>8} {'N/A':>5} {'Unscored':>9} {'Total':>6}")
    print("-" * 52)

    summary: dict[str, tuple[int, int]] = {}

    for level in LEVELS:
        rows = by_level[level]
        counts = {k: sum(1 for r in rows if r["score"] == k)
                  for k in ("met", "partial", "not-met", "n/a", "")}
        total = len(rows)
        satisfied = counts["met"] + counts["n/a"]
        summary[level] = (satisfied, total)

        print(f"{level:<6} {counts['met']:>5} {counts['partial']:>8} "
              f"{counts['not-met']:>8} {counts['n/a']:>5} {counts['']:>9} {total:>6}")

    print()

    # Levels are cumulative and all-or-nothing (CNF-2): stop at the first gap.
    attained: str | None = None
    first_incomplete: str | None = None
    for level in LEVELS:
        satisfied, total = summary[level]
        if total and satisfied == total:
            attained = level
        else:
            first_incomplete = level
            break

    if integrity:
        print("Evidence integrity findings:")
        for line in integrity:
            print(f"  {line}")
        print()

    if attained:
        print("CONFORMANCE STATEMENT")
        print("-" * 52)
        print(f"Conforms to Detection Engineering Framework v{SPEC_VERSION} at "
              f"Level {attained[1]}, assessed {date.today().isoformat()}, "
              f"scope: {args.scope}.")
    else:
        print("No level attained.")

    if first_incomplete:
        satisfied, total = summary[first_incomplete]
        print(f"\nProgress toward {first_incomplete}: {satisfied} of {total} requirements satisfied.")
        outstanding = [r["requirement_id"] for r in by_level[first_incomplete]
                       if r["score"] not in ("met", "n/a")]
        print("Outstanding: " + ", ".join(outstanding))

    if integrity:
        print("\nNote: evidence integrity findings above must be resolved before "
              "this statement is defensible.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
