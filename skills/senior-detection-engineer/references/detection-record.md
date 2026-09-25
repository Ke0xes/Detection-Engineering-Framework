# Detection Record

Every detection has a metadata record, kept in version control next to its
rule files (`GOV-9`, `GOV-11`). The record describes everything except the
query itself: why the detection exists, what it depends on, how it is tested,
and how it is maintained. This reference reproduces the DEF v2.1 detection
schema (`schema_version: "2.1"`).

## Required fields

| Field | Rule |
| --- | --- |
| `schema_version` | Always `"2.1"` |
| `id` | `DET-YYYY-NNNN`. Immutable; never reused or renumbered |
| `version` | Semantic version. MAJOR: logic changes that alter what fires. MINOR: scope or enrichment changes. PATCH: documentation and exceptions |
| `title` | 10 to 120 characters. Names what the adversary did, not the tool that saw it |
| `description` | At least 50 characters. What it detects, why it matters, what an analyst should conclude when it fires |
| `status` | `draft`, `testing`, `canary`, `production`, `deprecated` or `retired` |
| `created` | ISO date |
| `owner` | A team, not an individual (`GOV-5`) |
| `traceability` | `use_case_ref` (`UC-YYYY-NNNN`) and `driver_type` (one or more of `risk`, `threat`, `compliance`) |
| `classification` | `severity`, `confidence`, `robustness_tier` |
| `threat.attack.techniques` | At least one, `T####` or `T####.###` |
| `logsources` | At least one, each with `name` and `required` |
| `platform_implementations` | At least one, each with `platform`, `language` and `path` |
| `response.playbook_ref` | The playbook the detection triggers (`RSP-1`) |
| `lifecycle.review_cadence_days` | `90`, `180` or `365` |

## Enumerations

| Field | Allowed values |
| --- | --- |
| `classification.severity` | `critical`, `high`, `medium`, `low`, `informational` |
| `classification.confidence` | `high`, `medium`, `low` |
| `classification.robustness_tier` | `ephemeral`, `indicator`, `tool-artifact`, `behavior`, `invariant` |
| `classification.alert_disposition` | `alert`, `correlate-only`, `enrich-only`, `hunt-only` |
| `threat.kill_chain_phase` | `reconnaissance`, `weaponization`, `delivery`, `exploitation`, `installation`, `command-and-control`, `actions-on-objectives` |
| `logsources[].normalization` | `ocsf`, `ecs`, `asim`, `cim`, `native`, `custom` |
| `platform_implementations[].language` | `spl`, `kql`, `eql`, `esql`, `yara-l`, `sigma`, `sql`, `lucene`, `other` |
| `validation.fixtures[].expect` | `match`, `no-match` |
| `validation.emulation[].framework` | `atomic-red-team`, `caldera`, `stratus-red-team`, `leonidas`, `commercial-bas`, `manual` |
| `validation.emulation[].result`, `validation.validation_result` | `pass`, `fail`, `partial`, `not-run` |
| `lifecycle.deprecation.reason` | `threat-irrelevant`, `superseded`, `irreparable-precision`, `telemetry-withdrawn`, `cost-disproportionate`, `preventive-control-adopted` |

Other patterns: tactics `TA####`; ATLAS techniques `AML.T####` or
`AML.T####.###`; VAL block IDs `B1`, `B2` and so on; data quality scores 1 to
5.

## Conditional rules

- `severity: critical` requires `review_cadence_days: 90` (`IMP-8`).
- Any entry in `exceptions` requires `review_cadence_days: 90` (`IMP-8`).
- `status: production` requires `validation` (with `fixtures` and
  `last_validated`), `metrics`, and `lifecycle.last_reviewed`.
- `status: deprecated` or `retired` requires `lifecycle.deprecation` with
  `reason`, `coverage_impact` and `deprecated_on`.
- Every exception requires `id`, `scope`, `justification` (at least 20
  characters), `owner`, `created` and `expires` (`IMP-5`).
- `validation.fixtures` needs at least two entries: at least one `match` and
  one `no-match` (`DET-9`).
- No additional properties are allowed at any level. Organization-specific
  fields go in a documented superset of the schema.

## Template

Replace every angle-bracketed value. Remove optional sections that do not
apply rather than leaving them empty.

```yaml
schema_version: "2.1"
id: DET-<YYYY>-<NNNN>
version: 0.1.0
title: <What the adversary did, 10-120 characters>
description: >
  <What fires, why it matters, and what the analyst should conclude.
  At least 50 characters.>
status: draft
created: "<YYYY-MM-DD>"
author: <Team or person who wrote it>
owner: <Accountable team>

traceability:
  use_case_ref: UC-<YYYY>-<NNNN>
  driver_type: [threat]            # risk | threat | compliance
  risk_refs: [<RISK-ID>]
  compliance_refs:
    - framework: <e.g. NIST CSF 2.0>
      control: <e.g. DE.CM-01>
  business_service: [<Service or crown-jewel asset>]

classification:
  severity: high                   # critical | high | medium | low | informational
  confidence: medium               # high | medium | low
  robustness_tier: behavior        # ephemeral | indicator | tool-artifact | behavior | invariant
  alert_disposition: alert         # alert | correlate-only | enrich-only | hunt-only
  tags: [<tag>]

threat:
  attack:
    version: "<ATT&CK version>"
    tactics: [TA<####>]
    techniques: [T<####>.<###>]
  kill_chain_phase: [actions-on-objectives]

logsources:
  - name: <source-name>
    product: <product>
    service: <service>
    category: <category>
    required: true                 # false = degrades but still works without it
    normalization: <ocsf | ecs | asim | cim | native | custom>
    expected_interval_minutes: <max tolerable gap before a liveness alert>
    data_quality:
      completeness: <1-5>
      timeliness: <1-5>
      field_coverage: <1-5>
      assessed_on: "<YYYY-MM-DD>"

val:
  hypothesis: >
    If an adversary <does X>, then <Y> will be observable in <Z>.
  blocks:
    - id: B1
      description: <Observable condition>
      condition: <Plain-language or pseudo-code condition>
      correlation_fields: [<field>]
      logsource_refs: [<source-name>]
    - id: B2
      description: <Condition that separates the attack from benign use>
      condition: <condition>
      logsource_refs: [<source-name>]
  expression: B1 AND B2
  time_window_minutes: <window>

platform_implementations:
  - platform: sigma
    language: sigma
    path: rules/sigma/DET-<YYYY>-<NNNN>.yml
  - platform: <platform>
    language: <language>
    path: rules/<language>/DET-<YYYY>-<NNNN>.<ext>
    schedule: "<cron or native schedule>"
    lookback_minutes: <minutes>

false_positives:
  - description: <Known benign cause>
    triage_guidance: >
      <What the analyst checks, and how to close it, written for someone
      with no context.>

exceptions:
  - id: EXC-<NNNN>
    scope: <Exactly what is suppressed; one entity and one condition if possible>
    justification: <Why, at least 20 characters>
    owner: <Team>
    created: "<YYYY-MM-DD>"
    expires: "<YYYY-MM-DD>"
    approved_by: <Approver>

enrichments:
  - source: <asset-inventory | identity-directory | threat-intel-platform | ...>
    fields: [<field>]
    required: false

validation:
  fixtures:
    - path: fixtures/DET-<YYYY>-<NNNN>/tp-01-<description>.json
      expect: match
      description: <What attack variant this represents>
    - path: fixtures/DET-<YYYY>-<NNNN>/tn-01-<description>.json
      expect: no-match
      description: <What benign look-alike this represents>
  emulation:
    - framework: atomic-red-team
      test_id: <test ID>
      result: not-run

response:
  playbook_ref: playbooks/PB-<NNNN>-<name>.md
  runbook_ref: playbooks/RB-<NNNN>-<name>.md
  triage_priority_minutes: <minutes>
  escalation_path: <Tier 2 -> owning team -> incident lead>
  containment_authorised: false    # true only if pre-authorized in the playbook

lifecycle:
  review_cadence_days: 90          # 90 | 180 | 365; 90 if critical or any exception
  next_review_due: "<YYYY-MM-DD>"

references:
  - "<https://...>"
```

`metrics` (`precision_30d`, `alert_volume_30d`, `escalation_rate_30d`,
`median_triage_minutes`, `last_fired`, `computed_on`) is populated by
automation from case management data and is not written by hand.

## Fixtures

A fixture is a single event, or a small set of events, in the platform's
field names, with the expected result recorded in the detection record.

- **Naming.** `tp-NN-<description>.json` for events that must match;
  `tn-NN-<description>.json` for events that must not.
- **Comment.** Start each fixture with a `_comment` field stating what it
  represents and why it exists.
- **Coverage.** At least one true positive for each block combination the
  VAL treats as an attack; at least one true negative for the most likely
  benign look-alike; and one boundary fixture per exception (`DET-10`).
- **Synthetic data.** Use reserved domains (`example.com`, `example.net`) and
  documentation address ranges (`192.0.2.0/24`, `198.51.100.0/24`,
  `203.0.113.0/24`). Never include real credentials or personal data.

Example boundary fixture for an exception:

```json
{
  "_comment": "True negative asserting the scope of EXC-0001. The named application consented by the named automation account is suppressed. If a change widens the exception, the paired true-positive fixture tp-03 (same application, different initiator) will fail.",
  "TimeGenerated": "2026-06-08T02:00:13Z",
  "Operation": "Consent to application",
  "Result": "success",
  "InitiatorUpn": "svc-identity-automation@example.com",
  "InitiatorIsPrivileged": true,
  "ApplicationId": "00000000-0000-0000-0000-000000000001",
  "ApplicationIsAllowlisted": false,
  "GrantedScopes": "Mail.Read Files.Read.All offline_access"
}
```

## Use case request record

The detection's `use_case_ref` points to a use case request with at least:
`id` (`UC-YYYY-NNNN`), `title`, `status` (`submitted`, `triage`, `accepted`,
`in-development`, `delivered`, `rejected`, `withdrawn`), `submitted`,
`requester` (name and department), `drivers` (types and a justification of at
least 50 characters), `scope` (objective and in-scope items, plus
`out_of_scope`), `priority` (the five rubric scores and `scored_on`), and
`outcomes.success_criteria`. Compliance-driven requests carry a deadline on
each compliance reference. Accepted requests record a feasibility assessment
and a decision.
