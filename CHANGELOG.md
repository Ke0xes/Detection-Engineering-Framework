# Changelog

All notable changes to the Detection Engineering Framework are recorded here.

The specification follows [Semantic Versioning](https://semver.org/). A
conformance claim names a version; tagged versions are immutable.

---

## [2.1.1] — 2026-09-26

### Why this release

Version 2.1.0 made the framework something a program can be assessed against.
It did not yet make it easy to read. Feedback on 2.1.0 was that the guide felt
like a set of project notes rather than a guide: it jumped between topics, changed
voice from one chapter to the next, and repeated the same point in a diagram,
a list and several paragraphs. Some chapters still carried text from before
2.0 that contradicted the rules added later.

This release is for the reader. It gives the guide one path from start to
finish, one example that runs through it and one voice, and it corrects the
places where the explanation and the rules disagreed. It also adds an AI
assistant skill, so that the framework can be applied directly to real rules
and use cases.

**No requirement has been added, removed or changed.** A program that
conforms to 2.1.0 conforms to 2.1.1 at the same level. The schemas remain at
`schema_version: "2.1"`, and every published page URL still works. This is a
PATCH release under section 15 of the specification.

### What changes for readers

- **One path through the guide.** The guide now has four parts: *Understand
  the framework*, *Walk the lifecycle*, *Put it into practice* and
  *Reference*. Chapters that go deeper into one stage, such as telemetry or
  detection robustness, sit with that stage, so readers meet them at the
  point they become relevant.
- **One story throughout.** The worked example, a detection for OAuth consent
  phishing, moves from the end of the guide to the fourth chapter as *A
  detection's journey*. Each phase chapter returns to it, so every idea is
  shown working on the same detection.
- **Chapters that start and end the same way.** Each chapter says where it
  sits in the lifecycle and what it covers, and closes with an *In brief*
  summary, the requirements it contains, and a link to what comes next.
  Readers who need conclusions rather than method can read the summaries
  alone.
- **One voice.** The guide is written in the neutral third person
  throughout. Chapters no longer address the reader as "you" in one place and
  "we" in another. The style rules are in `CONTRIBUTING.md`.
- **Shorter, plainer chapters.** The planning, development, delivery, adoption
  and advanced practices chapters have been rewritten. Diagrams that only
  repeated the list beside them, generic explanations of IT concepts, and
  paragraphs that restated the same point have been removed. The substance of
  every section is kept, and so is almost every heading readers may have
  linked to (see *Compatibility*).
- **Chapter numbers** are no longer used. Cross-references name the chapter.
- **Home page** rewritten to explain what the framework is, the problem it
  addresses and how it works, before showing the reference implementation.
- **Navigation markers** under each chapter title, and previous and next links
  at its foot, are generated from the site navigation by `reading_order.py`.
  CI fails if they fall out of date.

### What changes for practitioners

These corrections change how parts of the guide read in practice, although
none changes a requirement.

- **False positive rate removed everywhere.** The adoption guide, the advanced
  practices chapter and the use case request template still set targets as a
  false positive rate, which `MET-1` forbids. All now use Precision, with the
  thresholds from the detection metrics chapter.
- **VAL examples corrected.** The four example VALs in the detection
  engineering chapter are rewritten as readable logic, each with the
  confidence it represents. One referred to "file encryption" that was not
  part of the scenario, and another had ambiguous logic.
- **Minimum Viable Detection aligned with the specification.** The adoption
  guide now defines the MVD exactly as `GOV-13` does, including the 30-day
  review date.
- **Development structure corrected.** The technical feasibility chapter
  described development as two stages; it now matches the three-stage model
  used everywhere else.
- **Testing order made consistent.** The detection engineering chapter now
  describes functional testing, attack emulation, non-functional testing and
  acceptance testing in one order, matching the rest of the chapter.
- **Response automation** moves from the delivery chapter to the response
  engineering chapter, where it is built, and now states the `RSP-5` rule that
  automation must not fail silently.
- **Release benchmark table completed.** The table showing which elements are
  complete at each release stage was empty. It is now filled in from the
  stage descriptions.
- **Catalog and ATT&CK details corrected.** Two catalog field descriptions
  were wrong (rule description and decommissioning date). The ATT&CK section
  no longer presents PRE-ATT&CK as a separate matrix; its tactics have been
  part of ATT&CK Enterprise since 2020. Example log strings no longer use real
  domain names.
- **Lifecycle chapter.** Phase headings no longer carry stray numbers
  ("1Planning Phase"), the delivery phase is correctly labeled steps 11 to 13,
  and step 14, refinement, has its own heading.
- **Schema descriptions** no longer refer to chapter file paths from before
  2.1.
- Two headings in the advanced practices chapter were at the wrong level.

### Added

- **AI assistant skill** (`skills/senior-detection-engineer/`). A
  self-contained agent skill that makes an assistant such as GitHub Copilot or
  Claude act as a senior detection engineer working to this framework. It
  scores use case requests, checks feasibility, designs and reviews rules,
  writes detection records, fixtures and playbooks, tunes noisy detections and
  runs conformance gap assessments. The rubric, schema, review checklist,
  metrics and conformance requirements are packaged with it, so it works
  outside this repository. Its outputs are drafts for review, not production
  artifacts.

### Compatibility

- Page URLs are unchanged. These in-page anchors changed:
  - *The detection engineering lifecycle*: the four phase headings under
    *Lifecycle phases* (for example, `#1planning-phase` is now
    `#planning-phase`), and the delivery steps heading
    (`#delivery-phase-steps-11-12-deployment-operations` is now
    `#delivery-phase-steps-11-13-deployment-operations`).
  - *The delivery phase*: `#response-automation` and its subsections now
    live in *The response engineering phase*.
  - *Tools and templates*: `#the-templates-you-probably-want-instead` is now
    `#schemas-instead-of-templates`.
- New conformance claims should name 2.1.1. Claims made against 2.1.0 remain
  valid.

---

## [2.1.0] — 2026-09-23

The framework moves from a prose guide to a specification with enforceable
conformance criteria and executable artifacts. Released as a minor version:
every chapter, filename and published URL from 2.0 is preserved, and 2.0 defined
no conformance criteria that this release could break.

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
were licensed CC BY 4.0. From 2.1.0, the whole repository — prose,
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
