# Changelog

All notable changes to the Detection Engineering Framework are recorded here.

The specification follows [Semantic Versioning](https://semver.org/). A
conformance claim names a version; tagged versions are immutable.

---

## [3.0.0] — 2026-09-23

The framework moves from a prose guide to a specification with enforceable
conformance criteria and executable artifacts.

### Added — normative

- **Specification** (`docs/00-specification.md`) with RFC 2119 language and
  stable requirement identifiers across ten domains: `GOV`, `PLN`, `TEL`,
  `FEA`, `DET`, `RSP`, `DAC`, `DEL`, `IMP`, `MET`.
- **Conformance model** (`docs/10-conformance.md`) defining L1 Foundational,
  L2 Managed and L3 Optimised, with assessment rules, evidence types and rules
  governing what may be claimed (`CNF-1` to `CNF-8`).
- **Assessment instrument** (`assessment/`): a 95-requirement CSV and a scorer
  that computes level attainment and emits a conformance statement.

### Added — machine-readable contracts

- `schema/detection.schema.json` — the detection metadata contract, including
  traceability, robustness tiering, exceptions with mandatory expiry,
  validation fixtures, response linkage and lifecycle state. Encodes several
  normative requirements as conditional schema rules.
- `schema/use-case.schema.json` — the planning artifact contract, including the
  anchored priority rubric.

### Added — reference implementation

- A complete worked detection (`DET-2026-0001`, OAuth consent abuse) carried
  from business driver to production metrics, with Sigma and KQL
  implementations, five behavioural fixtures, a response playbook and a
  containment runbook.
- `def_validate.py` — JSON Schema validation plus framework conformance checks
  that a schema cannot express (traceability resolution, expired exceptions,
  detection debt, precision thresholds, liveness declarations).
- `def_test.py` — a fixture regression harness implementing a Sigma subset,
  satisfying `IMP-13`.
- GitHub Actions workflows gating merge on all of the above.

### Added — chapters

- `09-metrics.md` — the required metric set, health monitoring, and the
  argument against the classical false positive rate.
- `11-detection-as-code.md` — repository layout, CI gates, review checklist,
  staged deployment, drift reconciliation.
- `12-telemetry-and-data.md` — data quality dimensions, normalization, log
  source maturity tiers, ingest economics.
- `13-detection-robustness.md` — the five-tier robustness ladder, coverage
  weighting, brittleness sources.
- `14-modern-attack-surfaces.md` — identity, cloud control plane, SaaS,
  containers, CI/CD, OT and AI/ML systems. Introduces MITRE ATLAS mapping.
- `15-governance-and-roles.md` — roles, a full lifecycle RACI, intake workflow,
  capacity model and service levels.
- `18-related-work.md` — explicit positioning against ATT&CK, ATLAS, D3FEND,
  Summiting the Pyramid, Sigma, DeTT&CT, Palantir ADS, maturity matrices and
  vendor detection-as-code guides. States three differentiators and six
  non-goals.
- `19-worked-example.md` — the end-to-end narrative.

### Changed — corrections

- **The false positive rate treatment has been withdrawn and replaced.** The
  previous text defined $FPR = FP/(FP+TN)$ and presented a worked example with
  an assumed true-negative count. That metric is unusable in detection
  engineering because $TN$ is unbounded and unmeasurable in an event stream,
  and any stated value is therefore fabricated. `MET-1` now requires Precision
  ($TP/(TP+FP)$) and prohibits reporting the classical FPR as a KPI. The
  separate and legitimate alert-to-incident ratio is named correctly.
- **False negative reporting.** Previously "reported as a quantity of missed
  security incidents." `MET-5` now requires an enumerated list of identified
  gaps with owners and dates; a bare count implies a total that is by
  definition unknown.
- **Prioritisation.** The unanchored 0-10 urgency and importance scales have
  been replaced by a five-dimension anchored rubric with written descriptors at
  every level, a defined formula, and worked examples (`PLN-1` to `PLN-5`).
- **Improvement phase rewritten** from 8 KB of general guidance to a normative
  chapter with five defined triggers, six change classes, mandatory alert
  disposition, exception expiry, review cadence by severity, drift detection,
  regression testing and a seven-step decommissioning procedure (`IMP-1` to
  `IMP-20`).
- **Grammar repair.** A historical global find-and-replace of "use cases" with
  "Detection Engineering Framework" had corrupted roughly eight sentences in
  the technical feasibility chapter. Repaired.
- **Typography and style.** All emoji removed. Hardcoded Mermaid fill colours
  removed so diagrams honour the reader's theme. Spelling normalised to en-US.
  Heading hierarchy corrected. Several typos fixed (`th phases`, `taddition`,
  `Feasibilty`, `Improvment`, `develped`, `Exception's Handling`).

### Changed — structure

Documentation moved into a numbered `docs/` tree. Old paths will 404; the
mapping is:

| 2.0 path | 3.0 path |
| --- | --- |
| `Background-and-Introduction.md` | `docs/01-introduction.md` |
| `Detection-Engineering-Lifecycle.md` | `docs/02-lifecycle.md` |
| `planning-phase.md` | `docs/03-planning-phase.md` |
| `development-phase-A.md` | `docs/04-development-feasibility.md` |
| `development-phase-B.md` | `docs/05-development-detection-engineering.md` |
| `development-phase-C.md` | `docs/06-development-response-engineering.md` |
| `delivery-phase.md` | `docs/07-delivery-phase.md` |
| `improvement-phase.md` | `docs/08-improvement-phase.md` |
| `from-theory-to-practice.md` | `docs/16-adoption-guide.md` |
| `best-practices.md` | `docs/17-best-practices.md` |
| `tools-and-templates/` | `templates/` |

### Changed — licensing

Dual-licensed. Prose remains CC BY 4.0. Schemas, tooling, templates and
assessment material are now Apache-2.0, because CC licences are unsuitable for
software and most enterprise legal functions will not permit CC-licensed
material in a codebase. Apache-2.0 additionally provides a patent grant, which
matters for a specification vendors may implement. See `LICENSING.md`.

The licence file was renamed from `License` to `LICENSE`, fixing a
case-sensitivity 404 in the README badge.

### Added — project infrastructure

`CONTRIBUTING.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
`ROADMAP.md`, `CITATION.cff`, issue and pull request templates, `.gitattributes`,
`.gitignore`, markdownlint configuration, and a MkDocs Material site published
to GitHub Pages.

### Deprecated

Nothing. This is the first version with normative requirements, so no
requirement identifiers have yet been withdrawn.

---

## [2.0] — 2025-11-26

- Restructured README with table-based navigation and a framework metadata
  block.
- Added codified use case request forms for ServiceNow, Salesforce, Microsoft
  Forms and Google Forms.
- Added the standard use case request template.
- Added `from-theory-to-practice.md`, a candid analysis of the framework's
  practical weaknesses.

## [1.0] — 2025

Initial publication. Lifecycle methodology across planning, development
(feasibility, detection engineering, response engineering), delivery and
improvement phases.
