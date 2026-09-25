# Changelog

All notable changes to the Detection Engineering Framework are recorded here.

The specification follows [Semantic Versioning](https://semver.org/). A
conformance claim names a version; tagged versions are immutable.

---

## [3.0.0] — 2026-09-23

The framework moves from a prose guide to a specification with enforceable
conformance criteria and executable artifacts.

### Added — normative

- **Specification** (`specification.md`) with RFC 2119 language and
  stable requirement identifiers across ten domains: `GOV`, `PLN`, `TEL`,
  `FEA`, `DET`, `RSP`, `DAC`, `DEL`, `IMP`, `MET`.
- **Conformance model** (`conformance-model.md`) defining L1 Foundational,
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
  implementations, five behavioral fixtures, a response playbook and a
  containment runbook.
- `def_validate.py` — JSON Schema validation plus framework conformance checks
  that a schema cannot express (traceability resolution, expired exceptions,
  detection debt, precision thresholds, liveness declarations).
- `def_test.py` — a fixture regression harness implementing a Sigma subset,
  satisfying `IMP-13`.
- GitHub Actions workflows gating merge on all of the above.

### Added — chapters

- `detection-metrics.md` — the required metric set, health monitoring, and the
  argument against the classical false positive rate.
- `detection-as-code.md` — repository layout, CI gates, review checklist,
  staged deployment, drift reconciliation.
- `telemetry-and-data.md` — data quality dimensions, normalization, log
  source maturity tiers, ingest economics.
- `detection-robustness.md` — the five-tier robustness ladder, coverage
  weighting, brittleness sources.
- `modern-attack-surfaces.md` — identity, cloud control plane, SaaS,
  containers, CI/CD, OT and AI/ML systems. Introduces MITRE ATLAS mapping.
- `governance-and-roles.md` — roles, a full lifecycle RACI, intake workflow,
  capacity model and service levels.
- `related-work.md` — explicit positioning against ATT&CK, ATLAS, D3FEND,
  Summiting the Pyramid, Sigma, DeTT&CT, Palantir ADS, maturity matrices and
  vendor detection-as-code guides. States three differentiators and six
  non-goals.
- `worked-example.md` — the end-to-end narrative.

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
  removed so diagrams honour the reader's theme. Spelling normalized to en-US.
  Heading hierarchy corrected. Several typos fixed (`th phases`, `taddition`,
  `Feasibility`, `Improvement`, `developed`, `Exception Handling`).

### Changed — structure

**No published URL has changed.** Every chapter that existed in 2.0 keeps its
exact filename and its position at the repository root, so existing links,
bookmarks and search engine results continue to resolve.

New chapters were added alongside them using the same naming style:

| New chapter | File |
| --- | --- |
| Specification | `specification.md` |
| Conformance Model | `conformance-model.md` |
| Detection Metrics | `detection-metrics.md` |
| Detection as Code | `detection-as-code.md` |
| Telemetry and Data | `telemetry-and-data.md` |
| Detection Robustness | `detection-robustness.md` |
| Modern Attack Surfaces | `modern-attack-surfaces.md` |
| Governance and Roles | `governance-and-roles.md` |
| Related Work | `related-work.md` |
| Worked Example | `worked-example.md` |

Chapter numbers used in cross-references (for example "chapter 13") are a
logical reading index published in the README. They are deliberately not
encoded in filenames, because renaming a published document to add a number
would break every link pointing at it.

New directories added: `schema/`, `reference-implementation/`, `assessment/`,
`assets/`. The existing `tools-and-templates/` tree is unchanged.

### Changed — licensing

**Relicensed to Apache License 2.0 in full.** Versions up to and including 2.0
were licensed CC BY 4.0. From 3.0.0, the whole repository — prose,
specification, schemas, tooling, templates and assessment material — is
Apache-2.0.

Reasons: CC licences are not designed for software, and most enterprise legal
functions will not permit CC-licensed material to be vendored into a codebase;
a single licence removes any ambiguity about which terms apply to which file;
and Apache-2.0 provides an explicit patent grant, which matters for a
specification vendors may implement.

Attribution previously required by CC BY is now carried by the `NOTICE` file,
which Apache-2.0 section 4(d) requires redistributors to retain.

The licence file keeps its published name, `License`, so existing links to it
continue to resolve.

Copies obtained under CC BY 4.0 before this change remain available under
those terms; CC grants are irrevocable.

### Added — project infrastructure

`CONTRIBUTING.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
`ROADMAP.md`, `CITATION.cff`, `NOTICE`, issue and pull request templates,
`.gitattributes`,
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
