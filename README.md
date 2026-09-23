# Detection Engineering Framework

[![Specification](https://img.shields.io/badge/specification-v3.0.0-0d419d)](docs/00-specification.md)
[![Conformance](https://img.shields.io/badge/conformance-L1%20%7C%20L2%20%7C%20L3-1f6feb)](docs/10-conformance.md)
[![Validate](https://github.com/Ke0xes/Detection-Engineering-Framework/actions/workflows/validate.yml/badge.svg)](https://github.com/Ke0xes/Detection-Engineering-Framework/actions/workflows/validate.yml)
[![Docs CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE)
[![Code Apache 2.0](https://img.shields.io/badge/code-Apache%202.0-lightgrey)](LICENSE-CODE)
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
Pyramid and others: **[Related Work](docs/18-related-work.md)**.

---

## This one runs

```bash
git clone https://github.com/Ke0xes/Detection-Engineering-Framework.git
cd Detection-Engineering-Framework
pip install -r reference-implementation/tools/requirements.txt

python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
```

```
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
| Deciding whether to adopt this | [Related Work and Differentiation](docs/18-related-work.md) |
| Wanting to see it work end to end | [Worked Example](docs/19-worked-example.md) |
| Looking for the rules you must follow | [Specification](docs/00-specification.md) |
| Assessing your program | [Conformance Model](docs/10-conformance.md) · [Assessment instrument](assessment/) |
| New to detection engineering | [Background and Introduction](docs/01-introduction.md) |
| Building the pipeline | [Detection as Code](docs/11-detection-as-code.md) |
| A small team with no budget | [Adoption Guide](docs/16-adoption-guide.md) |

---

## The framework

### Normative core

| | Chapter |
| --- | --- |
| 00 | [Specification](docs/00-specification.md) — every requirement, RFC 2119 language |
| 10 | [Conformance Model](docs/10-conformance.md) — L1/L2/L3, evidence, what may be claimed |

### Lifecycle

| | Chapter |
| --- | --- |
| 01 | [Background and Introduction](docs/01-introduction.md) |
| 02 | [Detection Engineering Lifecycle](docs/02-lifecycle.md) |
| 03 | [Planning Phase](docs/03-planning-phase.md) — drivers, feasibility, anchored prioritisation rubric |
| 04 | [Development A — Technical Feasibility](docs/04-development-feasibility.md) |
| 05 | [Development B — Detection Engineering](docs/05-development-detection-engineering.md) |
| 06 | [Development C — Response Engineering](docs/06-development-response-engineering.md) |
| 07 | [Delivery Phase](docs/07-delivery-phase.md) |
| 08 | [Improvement Phase](docs/08-improvement-phase.md) — triggers, change classes, drift, deprecation |

### Engineering practice

| | Chapter |
| --- | --- |
| 09 | [Detection Metrics](docs/09-metrics.md) — precision over FPR, health monitoring |
| 11 | [Detection as Code](docs/11-detection-as-code.md) — repository layout, CI gates, deployment |
| 12 | [Telemetry and Data](docs/12-telemetry-and-data.md) — data quality, normalization, ingest economics |
| 13 | [Detection Robustness](docs/13-detection-robustness.md) — the robustness ladder, coverage weighting |
| 14 | [Modern Attack Surfaces](docs/14-modern-attack-surfaces.md) — identity, cloud, SaaS, containers, CI/CD, OT, AI |
| 15 | [Governance and Roles](docs/15-governance-and-roles.md) — RACI, intake, capacity, SLAs |

### Applying it

| | Chapter |
| --- | --- |
| 16 | [Adoption Guide](docs/16-adoption-guide.md) |
| 17 | [Advanced Best Practices](docs/17-best-practices.md) |
| 18 | [Related Work](docs/18-related-work.md) |
| 19 | [Worked Example](docs/19-worked-example.md) |

---

## Executable artifacts

| Path | What it is |
| --- | --- |
| [`schema/detection.schema.json`](schema/detection.schema.json) | The detection metadata contract |
| [`schema/use-case.schema.json`](schema/use-case.schema.json) | The planning artifact contract |
| [`reference-implementation/`](reference-implementation/) | A complete worked detection, validation tooling and tests |
| [`assessment/`](assessment/) | Conformance instrument and scorer |
| [`templates/`](templates/) | Use case request template and codified intake forms |

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
[Detection Metrics](docs/09-metrics.md).

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
> lead maintainer's employer are explicitly prioritised.

---

## Licence

Dual-licensed, because prose and code have different needs.

| Content | Licence |
| --- | --- |
| Documentation, specification text | [CC BY 4.0](LICENSE) |
| Schemas, tooling, templates, assessment | [Apache-2.0](LICENSE-CODE) |

Details and attribution requirements: [LICENSING.md](LICENSING.md).

## Citing

Machine-readable metadata: [CITATION.cff](CITATION.cff).

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
behaviour, which belong to MITRE, to SigmaHQ, and to the practitioners who
publish their methods.
