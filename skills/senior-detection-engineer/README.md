# Senior Detection Engineer Skill

An AI agent skill that makes a coding or chat assistant act as a senior
detection engineer who follows the Detection Engineering Framework (DEF)
v2.1. Detection engineers and SOC leads can use it as a starting point for
building new detections and for reviewing and improving existing SIEM rules
and use cases against the framework.

The skill is self-contained. The framework's rubric, schema, review checklist,
metric definitions and conformance requirements are included in this folder,
so the skill works without access to the framework repository.

## What it does

- Scores use case requests with the framework's anchored rubric and routes
  them to the standard, expedited or compliance path.
- Checks technical feasibility: telemetry, field coverage and cost.
- Designs detections as a hypothesis and Vendor Agnostic Logic (VAL), then
  implements them in the platform's query language.
- Reviews existing rules against a requirement-referenced checklist and
  reports findings by severity.
- Writes schema-conformant detection metadata, true-positive and
  true-negative fixtures, and exception boundary fixtures.
- Drafts response playbooks with pre-authorized containment and defined
  automation failure modes.
- Diagnoses noisy and silent detections from disposition data and proposes
  classified changes.
- Runs conformance gap assessments against levels L1 to L3.

## Contents

| File | Purpose |
| --- | --- |
| `SKILL.md` | The skill: principles, intake questions and step-by-step procedures |
| `references/prioritization-rubric.md` | Anchored scoring descriptors and routing rules |
| `references/detection-record.md` | Metadata fields, enums, conditional rules, YAML template, fixture format |
| `references/review-checklist.md` | Rule review checklist, robustness ladder, brittleness sources |
| `references/tuning-and-metrics.md` | Dispositions, Precision thresholds, change classes, exceptions, reviews, deprecation |
| `references/response-playbook.md` | Playbook requirements and template |
| `references/conformance-levels.md` | Requirements by level and rules for claims |

## Installation

Copy the whole `senior-detection-engineer` folder, keeping its structure, into
a location the assistant reads skills from. The folder name must stay
`senior-detection-engineer`, matching the `name` in `SKILL.md`.

| Assistant | Project location | Personal location |
| --- | --- | --- |
| GitHub Copilot in VS Code | `.github/skills/` or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Other assistants | Paste `SKILL.md` into the system or project instructions and attach the `references` files | |

Once installed, the assistant loads the skill when a request matches its
description, or it can be invoked directly (in VS Code, type
`/senior-detection-engineer` in chat).

## Example requests

- "Review this Splunk search for Kerberoasting against the framework and list
  the findings by severity."
- "Score this use case request and tell me which path it takes."
- "Design a detection for OAuth consent phishing in Entra ID. We use Sentinel
  with ASIM normalization."
- "This rule had 220 alerts last month with 22 true positives. What should we
  change?"
- "Write true-positive and true-negative fixtures for this Sigma rule."
- "Assess our program for L2 conformance. Here is what we have."

## Adapting it

Organizations are expected to adapt the skill. Common changes:

- Replace the example platform in the intake questions with the local SIEM
  and normalization schema, so the assistant stops asking.
- Add the local privileged groups, allowlists and crown-jewel assets to
  `SKILL.md` under "Start of every task", if the file is kept private.
- Adjust thresholds (Precision, exception count, review cadence) where the
  program has documented different values. Conformance claims must then state
  the variation.

## Limitations

- The assistant cannot see the environment. Field names, allowlists and
  volumes it has not been given are assumptions, and it is instructed to label
  them. Every output needs verification against real telemetry before
  deployment.
- Generated rules and fixtures are drafts for review through the program's
  normal change process, not production-ready artifacts.
- The skill encodes DEF v2.1.1. Later framework releases may change
  requirements; check the changelog before relying on it for a conformance
  claim.

## License

Apache License 2.0, as for the rest of the Detection Engineering Framework.
