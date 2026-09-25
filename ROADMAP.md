# Roadmap

This is a statement of intent, not a commitment schedule. The project has one
maintainer; sequencing is more reliable than timing.

Items marked **help wanted** are where external contribution would have the
largest effect.

---

## Near term

### A second worked example — **help wanted**

The existing example is identity-focused. A second on a different surface would
prove the framework generalises. Highest value: a cloud control plane example
(IAM privilege escalation) or a CI/CD example (pipeline modification).

### A deprecation example

`IMP-16` to `IMP-19` govern retirement, and nothing in the repository
demonstrates it. A retired detection with a named successor and a recorded
coverage impact assessment would close this gap.

### Platform backends for the fixture runner — **help wanted**

`def_test.py` implements a Sigma subset. The fixture *contract* is the portable
part; the evaluator is not. Backends wanted for:

- pySigma integration (highest value — removes the bespoke evaluator entirely)
- Splunk
- Microsoft Sentinel
- Elastic Security
- Google SecOps

### Coverage model tooling

A script that reads the detection catalog and emits an ATT&CK Navigator layer
weighted by robustness tier and validation freshness, implementing `MET-3`.

### Migration tooling

A script that ingests an existing detection catalog (Sigma directory, Sentinel
export, Splunk savedsearches) and emits skeleton metadata files. The single
largest adoption barrier is the perceived cost of backfilling metadata for an
existing catalog.

---

## Medium term

### Governance

Recruit at least one maintainer from an organization other than the lead
maintainer's employer, then open an OWASP project proposal. See
[GOVERNANCE.md](GOVERNANCE.md).

### Citability

Register a Zenodo DOI against the v3.0.0 tag so the framework can be cited in
academic work and audit documentation.

### Compliance mappings

Reference mappings from the framework's requirements to NIST CSF 2.0, ISO
27001:2022, DORA and NIS2, so that adopters can reuse conformance evidence for
regulatory purposes. **help wanted** — particularly from practitioners subject
to DORA or NIS2.

### Requirement stability review

After twelve months of implementation reports, review every `MUST` for
achievability. Requirements that adopters consistently cannot evidence are
defects in the specification, not failures of the adopters.

### Translations — **help wanted**

The Apache 2.0 licence permits translation and redistribution, provided the
`NOTICE` file is retained.

---

## Longer term

### Independent assessment guidance

`CNF-7` recommends independent assessment at L3 but the project provides no
assessor guidance. Needed: an assessment procedure, evidence sufficiency
criteria, and a sampling approach for large catalogs.

### Catalog-scale guidance

The framework is written from the perspective of a single detection. The
genuinely hard problems in mature programs are catalog-scale: deduplication,
coverage overlap, correlated failure across detections sharing a log source,
and capacity modeling against a backlog. This deserves its own chapter.

### AI/ML chapter maturity

[Chapter 14](modern-attack-surfaces.md) treats AI systems briefly and
will date faster than anything else in the framework. As ATLAS matures and
agent telemetry standards emerge, this should become a full chapter.

---

## Explicitly not planned

| Not planned | Why |
| --- | --- |
| A detection content library | Detections are environment-specific. See [Related Work](related-work.md) |
| A rule language | Sigma exists |
| A certification scheme | Requires a neutral body the project does not have |
| A hosted assessment service | Out of scope for a specification project |
| Vendor-specific deployment tooling | Vendors maintain their own; the framework stays neutral |

---

## How to influence this

Implementation reports carry more weight than feature requests. If you adopted
part of this framework and something did not work, open a discussion. That
feedback reorders this roadmap faster than anything else.
