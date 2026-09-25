#!/usr/bin/env python3
"""Run detection fixtures against their Sigma rules.

This is the regression harness required by IMP-13: every detection must match
its true-positive fixtures and must not match its true-negative fixtures. The
evaluator implements the subset of Sigma the reference implementation uses:

  * search identifiers containing field/value maps
  * list values (OR semantics within a field)
  * the modifiers: contains, startswith, endswith, re, all
  * conditions built from identifiers, and, or, not and parentheses

It is deliberately small. The point is not to reimplement pySigma; it is to
demonstrate that detection logic can be executed against fixtures in CI before
it reaches production. Programs running Splunk, Sentinel or Elastic should
substitute their own backend while keeping the same fixture contract.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install -r reference-implementation/tools/requirements.txt")

REPO_ROOT = Path(__file__).resolve().parents[2]
DETECTION_DIR = REPO_ROOT / "reference-implementation" / "detections"


# ---------------------------------------------------------------------------
# Field matching
# ---------------------------------------------------------------------------

def _as_list(value):
    return value if isinstance(value, list) else [value]


def _compare(event_value, expected, modifier: str) -> bool:
    if event_value is None:
        return False

    if isinstance(event_value, bool) or isinstance(expected, bool):
        return event_value == expected

    haystack = str(event_value)
    needle = str(expected)

    if modifier == "contains":
        return needle.lower() in haystack.lower()
    if modifier == "startswith":
        return haystack.lower().startswith(needle.lower())
    if modifier == "endswith":
        return haystack.lower().endswith(needle.lower())
    if modifier == "re":
        return re.search(needle, haystack) is not None
    return haystack.lower() == needle.lower()


def match_selection(event: dict, selection) -> bool:
    """A selection matches when every field matches (AND across fields)."""
    if isinstance(selection, list):
        return any(match_selection(event, item) for item in selection)

    for raw_field, expected in selection.items():
        field, _, modifier_spec = raw_field.partition("|")
        modifiers = modifier_spec.split("|") if modifier_spec else []
        require_all = "all" in modifiers
        modifier = next((m for m in modifiers if m != "all"), "")

        candidates = _as_list(expected)
        event_value = event.get(field)

        results = [_compare(event_value, c, modifier) for c in candidates]
        if not (all(results) if require_all else any(results)):
            return False
    return True


# ---------------------------------------------------------------------------
# Condition parsing: identifiers combined with not / and / or and parentheses
# ---------------------------------------------------------------------------

TOKEN_RE = re.compile(r"\(|\)|\b(?:and|or|not)\b|[A-Za-z_][A-Za-z0-9_]*")


class ConditionError(ValueError):
    pass


def tokenize(condition: str) -> list[str]:
    tokens = TOKEN_RE.findall(condition)
    if not tokens:
        raise ConditionError(f"unparsable condition: {condition!r}")
    return tokens


class Parser:
    def __init__(self, tokens: list[str], selections: dict, event: dict) -> None:
        self.tokens = tokens
        self.pos = 0
        self.selections = selections
        self.event = event

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        token = self.peek()
        self.pos += 1
        return token

    def parse(self) -> bool:
        value = self.parse_or()
        if self.pos != len(self.tokens):
            raise ConditionError(f"unexpected trailing token {self.peek()!r}")
        return value

    def parse_or(self) -> bool:
        value = self.parse_and()
        while self.peek() == "or":
            self.next()
            value = self.parse_and() or value
        return value

    def parse_and(self) -> bool:
        value = self.parse_unary()
        while self.peek() == "and":
            self.next()
            value = self.parse_unary() and value
        return value

    def parse_unary(self) -> bool:
        if self.peek() == "not":
            self.next()
            return not self.parse_unary()
        return self.parse_atom()

    def parse_atom(self) -> bool:
        token = self.next()
        if token == "(":
            value = self.parse_or()
            if self.next() != ")":
                raise ConditionError("unbalanced parenthesis")
            return value
        if token in (None, ")", "and", "or"):
            raise ConditionError(f"unexpected token {token!r}")
        if token not in self.selections:
            raise ConditionError(f"condition references unknown search identifier {token!r}")
        return match_selection(self.event, self.selections[token])


def evaluate(rule: dict, event: dict) -> bool:
    detection = rule.get("detection")
    if not detection:
        raise ConditionError("rule has no detection block")
    condition = detection.get("condition")
    if not condition:
        raise ConditionError("rule has no condition")
    selections = {k: v for k, v in detection.items() if k != "condition"}
    return Parser(tokenize(condition), selections, event).parse()


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run() -> int:
    if not DETECTION_DIR.exists():
        print("No detections directory found.")
        return 0

    passed = failed = skipped = 0

    for det_path in sorted(DETECTION_DIR.glob("*.yml")):
        with det_path.open(encoding="utf-8") as fh:
            detection = yaml.safe_load(fh)

        det_id = detection.get("id", det_path.stem)
        sigma_impl = next(
            (i for i in detection.get("platform_implementations", []) if i.get("language") == "sigma"),
            None,
        )
        fixtures = detection.get("validation", {}).get("fixtures", [])

        if not sigma_impl or not fixtures:
            print(f"SKIP  {det_id}  no sigma implementation or no fixtures")
            skipped += 1
            continue

        rule_path = REPO_ROOT / sigma_impl["path"]
        with rule_path.open(encoding="utf-8") as fh:
            rule = yaml.safe_load(fh)

        for fixture in fixtures:
            fixture_path = REPO_ROOT / fixture["path"]
            name = fixture_path.name
            expect_match = fixture["expect"] == "match"

            try:
                with fixture_path.open(encoding="utf-8") as fh:
                    event = json.load(fh)
                actual = evaluate(rule, event)
            except (OSError, json.JSONDecodeError, ConditionError) as exc:
                print(f"FAIL  {det_id}  {name}  error: {exc}")
                failed += 1
                continue

            if actual == expect_match:
                print(f"PASS  {det_id}  {name}  (expected {'match' if expect_match else 'no-match'})")
                passed += 1
            else:
                print(f"FAIL  {det_id}  {name}  expected "
                      f"{'match' if expect_match else 'no-match'}, got "
                      f"{'match' if actual else 'no-match'}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())
