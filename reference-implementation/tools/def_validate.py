#!/usr/bin/env python3
"""Validate Detection Engineering Framework artifacts.

Two layers of checking are applied:

1. JSON Schema validation against schema/detection.schema.json and
   schema/use-case.schema.json.
2. Framework conformance rules that a JSON Schema cannot express, such as
   cross-file traceability, expired exceptions and detection debt.

Exit code 0 means every artifact conforms. Any non-zero exit fails CI.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install -r reference-implementation/tools/requirements.txt")

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install -r reference-implementation/tools/requirements.txt")


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schema"
DETECTION_DIR = REPO_ROOT / "reference-implementation" / "detections"
USECASE_DIR = REPO_ROOT / "reference-implementation" / "use-cases"


class Findings:
    """Collects errors and warnings with a stable, greppable output format."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, artifact: str, rule: str, message: str) -> None:
        self.errors.append(f"ERROR  {artifact}  [{rule}] {message}")

    def warn(self, artifact: str, rule: str, message: str) -> None:
        self.warnings.append(f"WARN   {artifact}  [{rule}] {message}")

    @property
    def ok(self) -> bool:
        return not self.errors


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schema(name: str) -> dict:
    with (SCHEMA_DIR / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def validate_schema(doc: dict, schema: dict, artifact: str, findings: Findings) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in err.path) or "<root>"
        findings.error(artifact, "SCHEMA", f"{location}: {err.message}")


def check_detection(doc: dict, path: Path, use_case_ids: set[str], findings: Findings,
                    today: date) -> None:
    artifact = path.relative_to(REPO_ROOT).as_posix()
    det_id = doc.get("id", "<unknown>")

    # Filename must match the detection id so the catalog is navigable.
    if path.stem != det_id:
        findings.error(artifact, "NAMING", f"filename stem '{path.stem}' does not match id '{det_id}'")

    # Traceability must resolve. A detection with a dangling use case reference
    # cannot demonstrate the two-way traceability the framework requires.
    ref = doc.get("traceability", {}).get("use_case_ref")
    if ref and ref not in use_case_ids:
        findings.error(artifact, "TRACE", f"use_case_ref '{ref}' does not resolve to a known use case")

    # Referenced files must exist.
    for impl in doc.get("platform_implementations", []):
        target = REPO_ROOT / impl.get("path", "")
        if not target.is_file():
            findings.error(artifact, "REF", f"platform_implementations path not found: {impl.get('path')}")

    fixtures = doc.get("validation", {}).get("fixtures", [])
    for fixture in fixtures:
        target = REPO_ROOT / fixture.get("path", "")
        if not target.is_file():
            findings.error(artifact, "REF", f"fixture path not found: {fixture.get('path')}")

    # IMP-13: at least one positive and one negative fixture.
    expectations = {f.get("expect") for f in fixtures}
    if doc.get("status") in {"production", "canary"}:
        if "match" not in expectations:
            findings.error(artifact, "IMP-13", "no true-positive fixture (expect: match)")
        if "no-match" not in expectations:
            findings.error(artifact, "IMP-13", "no true-negative fixture (expect: no-match)")

    # IMP-5 / IMP-6: exceptions must be time-bound and not silently expired.
    exceptions = doc.get("exceptions", []) or []
    for exc in exceptions:
        expires = parse_date(exc.get("expires", ""))
        if expires is None:
            findings.error(artifact, "IMP-5", f"exception {exc.get('id')} has no parsable expiry")
        elif expires < today:
            findings.error(artifact, "IMP-6", f"exception {exc.get('id')} expired on {expires}")
        elif expires - today < timedelta(days=30):
            findings.warn(artifact, "IMP-6", f"exception {exc.get('id')} expires in "
                                             f"{(expires - today).days} days")

    # IMP-7: excessive exceptions indicate the logic models the wrong thing.
    if len(exceptions) > 10:
        findings.error(artifact, "IMP-7", f"{len(exceptions)} exceptions exceeds the threshold of 10; "
                                          "escalate for C5 rebuild assessment")

    lifecycle = doc.get("lifecycle", {})
    cadence = lifecycle.get("review_cadence_days")

    # IMP-8: any detection carrying exceptions reviews at 90 days regardless of severity.
    if exceptions and cadence != 90:
        findings.error(artifact, "IMP-8", "detection carries exceptions and therefore requires a "
                                          "90 day review cadence")

    last_reviewed = parse_date(lifecycle.get("last_reviewed", ""))
    if doc.get("status") == "production":
        if last_reviewed is None:
            findings.error(artifact, "IMP-8", "production detection has no parsable last_reviewed date")
        elif cadence and last_reviewed + timedelta(days=cadence) < today:
            overdue = (today - (last_reviewed + timedelta(days=cadence))).days
            findings.error(artifact, "IMP-9", f"in detection debt: review overdue by {overdue} days")

    # MET-4: liveness monitoring requires a declared expected interval.
    for source in doc.get("logsources", []):
        if source.get("required") and not source.get("expected_interval_minutes"):
            findings.error(artifact, "MET-4", f"required logsource '{source.get('name')}' has no "
                                              "expected_interval_minutes, so liveness cannot be monitored")

    # MET-1 / MET-2: production detections declare precision and act on it.
    if doc.get("status") == "production":
        precision = doc.get("metrics", {}).get("precision_30d")
        if precision is None:
            findings.error(artifact, "MET-1", "production detection reports no precision_30d")
        elif precision < 0.5:
            findings.error(artifact, "MET-2", f"precision_30d {precision:.2f} is below 0.50; "
                                              "must be in the tuning backlog")
        elif precision < 0.7:
            findings.warn(artifact, "MET-2", f"precision_30d {precision:.2f} is below the L3 "
                                             "threshold of 0.70")

    # A detection without a response plan is an unfinished detection.
    playbook = doc.get("response", {}).get("playbook_ref")
    if playbook and not (REPO_ROOT / playbook).exists():
        findings.warn(artifact, "REF", f"playbook_ref not found in repository: {playbook}")


def check_use_case(doc: dict, path: Path, detection_ids: set[str], findings: Findings) -> None:
    artifact = path.relative_to(REPO_ROOT).as_posix()
    uc_id = doc.get("id", "<unknown>")

    if path.stem != uc_id:
        findings.error(artifact, "NAMING", f"filename stem '{path.stem}' does not match id '{uc_id}'")

    priority = doc.get("priority", {})
    required = ("threat_relevance", "asset_criticality", "coverage_gap", "build_cost", "maintenance_burden")
    if all(k in priority for k in required):
        expected = round(
            (priority["threat_relevance"] * 3 + priority["asset_criticality"] * 3
             + priority["coverage_gap"] * 2) / (priority["build_cost"] + priority["maintenance_burden"]),
            2,
        )
        declared = priority.get("computed_score")
        if declared is not None and abs(declared - expected) > 0.01:
            findings.error(artifact, "PLN-1", f"computed_score {declared} does not match the rubric "
                                              f"result {expected}")

        # PLN-3: an actively exploited threat does not wait in the backlog.
        if priority["threat_relevance"] == 5 and priority.get("path") == "standard":
            findings.warn(artifact, "PLN-3", "threat_relevance is 5; confirm the expedited path was "
                                             "considered before assigning the standard path")

    # Traceability must close in both directions.
    for det in doc.get("resulting_detections", []) or []:
        if det not in detection_ids:
            findings.error(artifact, "TRACE", f"resulting_detections references unknown detection '{det}'")

    if doc.get("status") == "delivered" and not doc.get("resulting_detections"):
        findings.error(artifact, "TRACE", "use case is delivered but references no resulting detections")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    findings = Findings()
    today = date.today()

    detection_schema = load_schema("detection.schema.json")
    use_case_schema = load_schema("use-case.schema.json")

    detection_files = sorted(DETECTION_DIR.glob("*.yml")) if DETECTION_DIR.exists() else []
    use_case_files = sorted(USECASE_DIR.glob("*.yml")) if USECASE_DIR.exists() else []

    detections = {p: load_yaml(p) for p in detection_files}
    use_cases = {p: load_yaml(p) for p in use_case_files}

    detection_ids = {d.get("id") for d in detections.values()}
    use_case_ids = {u.get("id") for u in use_cases.values()}

    for path, doc in use_cases.items():
        artifact = path.relative_to(REPO_ROOT).as_posix()
        validate_schema(doc, use_case_schema, artifact, findings)
        check_use_case(doc, path, detection_ids, findings)

    for path, doc in detections.items():
        artifact = path.relative_to(REPO_ROOT).as_posix()
        validate_schema(doc, detection_schema, artifact, findings)
        check_detection(doc, path, use_case_ids, findings, today)

    for line in findings.warnings:
        print(line)
    for line in findings.errors:
        print(line)

    total = len(detections) + len(use_cases)
    print(f"\nValidated {total} artifact(s): "
          f"{len(findings.errors)} error(s), {len(findings.warnings)} warning(s)")

    if findings.errors:
        return 1
    if args.strict and findings.warnings:
        print("Strict mode: warnings treated as errors.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
