# Detection Engineering Framework

**Version 3.0.0** · A lifecycle standard for building, governing and retiring
security detections.

---

## Start here

| If you are... | Read |
| --- | --- |
| Deciding whether to adopt this | [Related Work and Differentiation](18-related-work.md) |
| New to detection engineering | [Background and Introduction](01-introduction.md) |
| Looking for the rules you must follow | [Specification](00-specification.md) |
| Assessing your program | [Conformance Model](10-conformance.md) |
| Wanting to see it work | [Worked Example](19-worked-example.md) |
| Building the pipeline | [Detection as Code](11-detection-as-code.md) |
| Adopting with a small team and no budget | [Adoption Guide](16-adoption-guide.md) |

---

## The framework

### Normative core

| | Chapter | Contains |
| --- | --- | --- |
| 00 | [Specification](00-specification.md) | Every normative requirement, RFC 2119 language, conformance summary |
| 10 | [Conformance Model](10-conformance.md) | L1/L2/L3 definitions, assessment rules, what may be claimed |

### Lifecycle

| | Chapter | Phase |
| --- | --- | --- |
| 01 | [Background and Introduction](01-introduction.md) | Foundation |
| 02 | [Detection Engineering Lifecycle](02-lifecycle.md) | Overview and traceability |
| 03 | [Planning Phase](03-planning-phase.md) | Drivers, feasibility, anchored prioritization rubric |
| 04 | [Development Phase A](04-development-feasibility.md) | Technical feasibility, threat modeling, attack simulation |
| 05 | [Development Phase B](05-development-detection-engineering.md) | VAL, rule prototyping, exceptions, enrichment, testing |
| 06 | [Development Phase C](06-development-response-engineering.md) | Playbooks, runbooks, dashboards, automation |
| 07 | [Delivery Phase](07-delivery-phase.md) | Handover, activation, cataloging |
| 08 | [Improvement Phase](08-improvement-phase.md) | Triggers, change classes, drift, deprecation |

### Engineering practice

| | Chapter | Contains |
| --- | --- | --- |
| 09 | [Detection Metrics](09-metrics.md) | Precision over FPR, the required metric set, health monitoring |
| 11 | [Detection as Code](11-detection-as-code.md) | Repository layout, CI gates, review checklist, deployment |
| 12 | [Telemetry and Data](12-telemetry-and-data.md) | Data quality scoring, normalization, ingest economics |
| 13 | [Detection Robustness](13-detection-robustness.md) | The robustness ladder, coverage weighting, brittleness |
| 14 | [Modern Attack Surfaces](14-modern-attack-surfaces.md) | Identity, cloud, SaaS, containers, CI/CD, OT, AI |
| 15 | [Governance and Roles](15-governance-and-roles.md) | Roles, RACI, intake workflow, capacity, SLAs |

### Applying it

| | Chapter | Contains |
| --- | --- | --- |
| 16 | [Adoption Guide](16-adoption-guide.md) | Real-world obstacles and how to work around them |
| 17 | [Advanced Best Practices](17-best-practices.md) | Practices for programs already operating |
| 18 | [Related Work](18-related-work.md) | How this relates to ATT&CK, Sigma, DeTT&CT, ADS and others |
| 19 | [Worked Example](19-worked-example.md) | One use case carried end to end |

---

## Executable artifacts

The framework ships working code, not only prose.

| Artifact | Purpose |
| --- | --- |
| [`schema/detection.schema.json`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/schema/detection.schema.json) | The detection metadata contract |
| [`schema/use-case.schema.json`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/schema/use-case.schema.json) | The planning artifact contract |
| [`reference-implementation/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/reference-implementation) | A complete worked detection with validation and tests |
| [`assessment/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/assessment) | The conformance self-assessment instrument and scorer |
| [`templates/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/templates) | Use case request templates and codified intake forms |

---

## The shortest useful summary

1. Every detection traces to a business driver and to its telemetry, in a
   machine-readable form.
2. Every detection has a hypothesis, a declared robustness tier, a response
   playbook and a review date.
3. Every detection ships with telemetry it must match and telemetry it must not
   match, and those assertions run in CI.
4. Precision is the quality metric. The classical false positive rate is not
   usable and is not reported.
5. Exceptions expire. Reviews are enforced. Detections get retired.
6. There is a fast path for active threats, and it has a defined minimum and a
   30 day expiry.

Everything else is detail.
