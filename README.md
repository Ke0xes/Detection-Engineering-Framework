# Detection Engineering Framework

[![Specification](https://img.shields.io/badge/specification-v3.0.0-0d419d)](specification.md)
[![Conformance](https://img.shields.io/badge/conformance-L1%20%7C%20L2%20%7C%20L3-1f6feb)](conformance-model.md)
[![Validate](https://github.com/Ke0xes/Detection-Engineering-Framework/actions/workflows/validate.yml/badge.svg)](https://github.com/Ke0xes/Detection-Engineering-Framework/actions/workflows/validate.yml)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/License)
[![Stars](https://img.shields.io/github/stars/Ke0xes/Detection-Engineering-Framework?style=flat&color=555)](https://github.com/Ke0xes/Detection-Engineering-Framework/stargazers)

**A lifecycle standard for building, governing and retiring security
detections.**

Most detection programs can tell you how many rules they have. Far fewer can
tell you which business risk each rule serves, whether it still works, what
would break if a log source failed, or when it was last reviewed. This framework
makes those questions answerable — and enforces the answers in CI.

**[Read the documentation](https://ke0xes.github.io/Detection-Engineering-Framework/)**

---

## What makes this different

Three things, in combination, that you will not find together elsewhere:

**1. Traceability is a hard requirement, not an aspiration.**
Every detection traces upward to a recorded risk, threat or compliance driver
and downward to specific telemetry — in a machine-readable form, answerable in
both directions. *"The EDR pipeline was down for six hours; what were we blind
to?"* becomes a query rather than a week of archaeology.

**2. Response engineering is a co-equal phase.**
A detection cannot reach production without a linked, exercised response
playbook. An alert without a response plan generates work, not security.

**3. Vendor Agnostic Logic sits above rule formats, not beside them.**
VAL expresses detection intent as named observable conditions and a boolean
relationship between them. One VAL, many platform implementations, one fixture
set. This complements Sigma; it does not compete with it.

Full positioning against ATT&CK, Sigma, DeTT&CT, Palantir ADS, Summiting the
Pyramid and others: **[Related Work](related-work.md)**.

---

## This one runs

```bash
git clone https://github.com/Ke0xes/Detection-Engineering-Framework.git
cd Detection-Engineering-Framework
pip install -r reference-implementation/tools/requirements.txt

python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
```

```text
Validated 2 artifact(s): 0 error(s), 0 warning(s)

PASS  DET-2026-0001  tp-01-privileged-consent-mailread.json  (expected match)
PASS  DET-2026-0001  tp-02-admin-grant-directoryread.json  (expected match)
PASS  DET-2026-0001  tn-01-allowlisted-app.json  (expected no-match)
PASS  DET-2026-0001  tn-02-unprivileged-user.json  (expected no-match)
PASS  DET-2026-0001  tn-03-exception-scoped.json  (expected no-match)

5 passed, 0 failed, 0 skipped
```

Now break something and watch the governance fail the build:

| Edit `reference-implementation/detections/DET-2026-0001.yml` | Result |
| --- | --- |
| Set `last_reviewed` back six months | `IMP-9` fails — in detection debt |
| Expire an exception | `IMP-6` fails — exception expired |
| Set `review_cadence_days: 180` | `IMP-8` fails — detections with exceptions review at 90 |
| Set `precision_30d: 0.4` | `MET-2` fails — must be in the tuning backlog |
| Point `use_case_ref` at nothing | `TRACE` fails — reference does not resolve |

That is the difference between a framework and a document.

---

## Start here

| If you are... | Go to |
| --- | --- |
| Deciding whether to adopt this | [Related Work and Differentiation](related-work.md) |
| Wanting to see it work end to end | [Worked Example](worked-example.md) |
| Looking for the rules you must follow | [Specification](specification.md) |
| Assessing your program | [Conformance Model](conformance-model.md) · [Assessment instrument](assessment/) |
| New to detection engineering | [Background and Introduction](Background-and-Introduction.md) |
| Building the pipeline | [Detection as Code](detection-as-code.md) |
| A small team with no budget | [Adoption Guide](from-theory-to-practice.md) |

---

## The framework

> Chapter numbers are a stable reading index used for cross-references in the
> text. Filenames are unchanged from earlier versions so that existing links
> keep working.

### Normative core

| # | Chapter |
| --- | --- |
| 00 | [Specification](specification.md) — every requirement, RFC 2119 language |
| 10 | [Conformance Model](conformance-model.md) — L1/L2/L3, evidence, what may be claimed |

### Lifecycle

| # | Chapter |
| --- | --- |
| 01 | [Background and Introduction](Background-and-Introduction.md) |
| 02 | [Detection Engineering Lifecycle](Detection-Engineering-Lifecycle.md) |
| 03 | [Planning Phase](planning-phase.md) — drivers, feasibility, anchored prioritization rubric |
| 04 | [Development A — Technical Feasibility](development-phase-A.md) |
| 05 | [Development B — Detection Engineering](development-phase-B.md) |
| 06 | [Development C — Response Engineering](development-phase-C.md) |
| 07 | [Delivery Phase](delivery-phase.md) |
| 08 | [Improvement Phase](improvement-phase.md) — triggers, change classes, drift, deprecation |

### Engineering practice

| # | Chapter |
| --- | --- |
| 09 | [Detection Metrics](detection-metrics.md) — precision over FPR, health monitoring |
| 11 | [Detection as Code](detection-as-code.md) — repository layout, CI gates, deployment |
| 12 | [Telemetry and Data](telemetry-and-data.md) — data quality, normalization, ingest economics |
| 13 | [Detection Robustness](detection-robustness.md) — the robustness ladder, coverage weighting |
| 14 | [Modern Attack Surfaces](modern-attack-surfaces.md) — identity, cloud, SaaS, containers, CI/CD, OT, AI |
| 15 | [Governance and Roles](governance-and-roles.md) — RACI, intake, capacity, SLAs |

### Applying it

| # | Chapter |
| --- | --- |
| 16 | [Adoption Guide](from-theory-to-practice.md) |
| 17 | [Advanced Best Practices](best-practices.md) |
| 18 | [Related Work](related-work.md) |
| 19 | [Worked Example](worked-example.md) |

---

## Executable artifacts

| Path | What it is |
| --- | --- |
| [`schema/detection.schema.json`](schema/detection.schema.json) | The detection metadata contract |
| [`schema/use-case.schema.json`](schema/use-case.schema.json) | The planning artifact contract |
| [`reference-implementation/`](reference-implementation/) | A complete worked detection, validation tooling and tests |
| [`assessment/`](assessment/) | Conformance instrument and scorer |
| [`tools-and-templates/`](tools-and-templates/) | Use case request template and codified intake forms |

---

## Conformance in one table

| | **L1 Foundational** | **L2 Managed** | **L3 Optimised** |
| --- | --- | --- | --- |
| Answers | Do we know what we have and why? | Is it engineered and governed? | Is it measured, validated and self-correcting? |
| Reachable by | 1-3 people, no budget | A dedicated detection function | Detection function with platform support |
| Testing | Manual, documented | Fixtures in CI | Fixtures plus continuous adversary emulation |
| Improvement | Reactive, tracked | Scheduled reviews enforced | Drift detected automatically |

A conformance claim names the level, the specification version, the assessment
date and the scope. *"DEF compliant"* is not a claim.

---

## One correction worth calling out

Version 2.0 of this framework defined the false positive rate as
$FPR = FP/(FP+TN)$ and gave a worked example with an assumed true-negative
count.

That is withdrawn. $TN$ — benign events correctly *not* alerted on — is
unbounded and unmeasurable in an event stream, so any stated value is
fabricated. It also always produces a flatteringly small number: a rule
generating 400 false alerts a day against 50 million events reports an FPR of
0.0008% while the SOC drowns.

The framework now requires **Precision** ($TP/(TP+FP)$), which is read directly
from case management data and reflects what analysts actually experience. See
[Detection Metrics](detection-metrics.md).

Other frameworks still publish the old formula. This one does not, and says why.

---

## Contributing

**Implementation reports are the most valuable contribution.** If you adopted
part of this and something did not work, [tell us](https://github.com/Ke0xes/Detection-Engineering-Framework/issues/new?template=implementation-report.yml).
A requirement that cannot be met in practice is a defect in the specification.

Also wanted: a second worked example on a non-identity surface, platform
backends for the fixture runner, and compliance mappings.

See [CONTRIBUTING.md](CONTRIBUTING.md), [ROADMAP.md](ROADMAP.md) and
[GOVERNANCE.md](GOVERNANCE.md).

> **On governance.** This project currently has one maintainer. That is a real
> limitation for something aiming to be a standard, and the path away from it —
> additional maintainers from other organizations, then a neutral home — is
> documented in [GOVERNANCE.md](GOVERNANCE.md). Maintainers from outside the
> lead maintainer's employer are explicitly prioritized.

---

## Licence

Everything in this repository — prose, specification, schemas, tooling,
templates and assessment material — is licensed under the
[Apache License 2.0](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/License).
Attribution requirements are in
[NOTICE](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/NOTICE).

Apache 2.0 includes an explicit patent grant, which matters for a specification
that vendors may implement, and it is a licence most enterprise legal functions
already approve for internal use.

## Citing

Machine-readable metadata: [CITATION.cff](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/CITATION.cff).

> Hatode, K. et al. *Detection Engineering Framework*, version 3.0.0, 2026.
> https://github.com/Ke0xes/Detection-Engineering-Framework

## Credits

Created by **[Kunal Hatode](https://kunal.hatode.com)**, developed originally
during work as a Cyber Operations Security Architect at Cisco and published
independently.

With thanks to:

- **[Frank Hassenrueck](https://www.linkedin.com/in/frank-hassenr%C3%BCck-371529116/)** — co-wrote technical core elements
- **[Matrix Chau](https://www.linkedin.com/in/matrixchau/)** — early feedback and co-writing

The ideas here are assembled from the work of the wider security community.
The framework's contribution is the lifecycle, the conformance model, the
schemas and the enforcement — not the underlying insights about adversary
behavior, which belong to MITRE, to SigmaHQ, and to the practitioners who
publish their methods.
