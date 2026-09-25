# Tools and Templates

<!-- journey:where -->
*Put it into practice › Tools and templates*
<!-- /journey:where -->

The framework is accompanied by artifacts that help put it into practice: intake
forms for use case requests, machine-readable schemas for detection and use
case records, a reference implementation with validation and tests, and a
self-assessment instrument. This page describes what each is for and where to
find it.

All of them are licensed Apache-2.0, like the rest of the repository, so they
can be copied into other repositories and internal systems without licence
friction.

## What is here

| Path | Phase | Purpose |
| --- | --- | --- |
| [`use-case-request-template.md`](templates/use-case-requests/use-case-request-template.md) | Planning | Human-readable use case request |
| [`servicenow-use-case-request-form.txt`](templates/use-case-requests/servicenow-use-case-request-form.txt) | Planning | ServiceNow catalog item definition |
| [`salesforce-use-case-request-form.txt`](templates/use-case-requests/salesforce-use-case-request-form.txt) | Planning | Salesforce form definition |
| [`microsoft-forms-use-case-request-form.txt`](templates/use-case-requests/microsoft-forms-use-case-request-form.txt) | Planning | Microsoft Forms question set |
| [`google-forms-use-case-request-form.txt`](templates/use-case-requests/google-forms-use-case-request-form.txt) | Planning | Google Forms question set |

## Schemas instead of templates

For anything downstream of planning, the **schemas and reference
implementation** are the templates. They are machine-readable, validated in CI,
and therefore cannot drift from the specification the way a Markdown template
can.

| Instead of a template for... | Use |
| --- | --- |
| Use case request | [`schema/use-case.schema.json`](../schema/use-case.schema.json) and [`UC-2026-0001.yml`](../reference-implementation/use-cases/UC-2026-0001.yml) |
| Detection documentation | [`schema/detection.schema.json`](../schema/detection.schema.json) and [`DET-2026-0001.yml`](../reference-implementation/detections/DET-2026-0001.yml) |
| Rule testing | [`fixtures/DET-2026-0001/`](../reference-implementation/fixtures/DET-2026-0001) and [`def_test.py`](../reference-implementation/tools/def_test.py) |
| Response playbook | [`PB-0003-oauth-consent-abuse.md`](../reference-implementation/playbooks/PB-0003-oauth-consent-abuse.md) |
| Runbook | [`RB-0007-revoke-service-principal.md`](../reference-implementation/playbooks/RB-0007-revoke-service-principal.md) |
| Metrics and tracking | [`detection-metrics.md`](../detection-metrics.md) — definitions and thresholds, not a spreadsheet |
| Maturity assessment | [`assessment/`](../assessment/) |

This is deliberate. A Markdown template that duplicates a schema will fall out
of sync with it, and the copy people actually use will be the stale one.

## Using the intake forms

The `.txt` files are field definitions for building the request form in an
existing intake system. Field names can be adapted to the local instance.

Whichever system is used, the form MUST capture enough to satisfy
[`schema/use-case.schema.json`](../schema/use-case.schema.json), because the
submitted request becomes the `UC-` record that every resulting detection
traces back to (`GOV-1`).

The fields most often omitted, and most often regretted:

| Field | Requirement | Why it matters |
| --- | --- | --- |
| Out of scope | `PLN-6` | Undocumented non-goals become handover disputes |
| Success criteria | `PLN-7` | "Improved visibility" cannot be verified at delivery |
| Business driver reference | `GOV-1` | Without it the detection cannot be justified or defended at review |
| Compliance deadline | `PLN-4` | Compliance requests are scheduled to a date, not ranked by score |

## Prioritisation

The request form should capture the five rubric dimensions from
[the planning phase](../planning-phase.md): threat relevance, asset
criticality, coverage gap, build cost and maintenance burden.

**Requesters should not score their own requests.** They supply the evidence;
detection engineering and threat intelligence apply the anchored descriptors.
Self-scoring produces a backlog in which every request is a five.

## AI assistant skill

The [senior detection engineer skill](../skills/senior-detection-engineer/README.md)
packages the rubric, schema, review checklist, metrics and conformance
requirements for use by an AI assistant. It can score requests, review and
write rules, produce detection records, fixtures and playbooks, and run a
conformance gap assessment. Its outputs are drafts, to be verified against
real telemetry and passed through the program's normal review.

## Contributing templates

New templates are welcome where a machine-readable artifact would not serve
better. Before contributing, check whether the proposed template should
instead be an extension to the schema. See
[CONTRIBUTING.md](../CONTRIBUTING.md).

## What comes next

The remaining chapters are reference material.
[The specification](../specification.md) states every requirement in the
framework in testable form, and [related work](../related-work.md) compares
the framework with other established work in the field.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [Assessing a program](../conformance-model.md) · **Next:** [Use case request forms](templates/use-case-requests/README.md)

</div>
<!-- /journey:next -->
