# Related Work and Differentiation

<!-- journey:where -->
*Reference › Related work*
<!-- /journey:where -->

Detection engineering draws on a substantial body of existing work, including
adversary knowledge bases, rule formats, data-quality models and maturity
assessments. Readers evaluating the framework, particularly those who already
use some of that work, need to know how it fits.

This chapter describes what the framework is for, what it draws from other work,
where it adds something those sources do not, and what it deliberately leaves
to them.

---

## What this framework is for

> **The Detection Engineering Framework governs the full lifecycle of a
> detection — from business driver to retirement — with enforceable conformance
> criteria and machine-readable traceability.**

It is a **process and governance standard**. It is not a rule format, not a
knowledge base of adversary behavior, not a maturity survey, and not a
detection library.

---

## Three differentiators

Everything else in this repository exists elsewhere in some form. These three,
in combination, do not.

### 1. Business-driver traceability as a hard requirement

`GOV-1` to `GOV-4` require that every detection trace upward to a recorded risk,
threat or compliance driver and downward to specific telemetry, in a
machine-readable form, answerable in both directions.

Other frameworks describe threat-informed defense. This one makes the audit
trail a conformance criterion and ships the schema that carries it. The
practical consequence is that "which detections did we lose when the EDR
pipeline failed" and "what are we monitoring because of DORA" are queries, not
projects.

### 2. Response engineering as a co-equal phase

`RSP-1` prohibits a detection reaching production without a linked, exercised
response playbook. Development Phase C is not an appendix to detection
engineering; it is a third of it.

Most detection frameworks stop at the alert. This one treats an alert without a
response plan as an incomplete artifact, because in operational terms it is one:
it generates work rather than security.

### 3. Vendor Agnostic Logic as a correlation layer

VAL states detection intent independently of platform, as named observable
blocks combined by a boolean expression, with all platform implementations
traceable to the same VAL and validated against the same fixtures.

This is explicitly **not** a competitor to Sigma. See below.

---

## Comparison

| Work | What it is | Overlap | How this framework relates |
| --- | --- | --- | --- |
| **MITRE ATT&CK** | Knowledge base of adversary behavior | Technique taxonomy | **Consumes it.** ATT&CK is the shared vocabulary for `threat.attack`. This framework does not attempt to replicate or replace it |
| **MITRE ATLAS** | ATT&CK for AI/ML systems | Technique taxonomy for AI threats | **Consumes it.** See `atlas_techniques` in the schema and [modern attack surfaces](modern-attack-surfaces.md) |
| **MITRE D3FEND** | Countermeasure knowledge graph | Defensive technique taxonomy | **Complementary.** D3FEND classifies countermeasures; this framework governs how they are built and maintained |
| **Summiting the Pyramid** (MITRE CTID) | Research on analytic robustness | Robustness tiering | **Builds on it.** [Detection robustness](detection-robustness.md) adapts the robustness concept and connects it to lifecycle controls: review cadence, coverage weighting and improvement targets |
| **Sigma** | Portable detection rule format | Rule expression, log source taxonomy | **Consumes it.** Sigma is the recommended format for `platform_implementations`. The reference implementation uses Sigma. VAL sits *above* Sigma as the correlation and intent layer, not beside it |
| **DeTT&CT** | Data source and detection quality scoring | Data quality, coverage scoring | **Strongly aligned.** DeTT&CT's data quality dimensions informed [telemetry and data](telemetry-and-data.md). Use DeTT&CT for the scoring; use this framework for the lifecycle around it |
| **Palantir ADS Framework** | Alerting and detection strategy document template | Detection documentation | **Extends it.** ADS is an excellent per-detection template. This framework makes it machine-readable, adds the governance lifecycle around it, and enforces it in CI |
| **Detection Engineering Maturity Matrix** | Self-assessment maturity model | Maturity levelling | **Complementary.** The matrix is a broad maturity survey. The [conformance model](conformance-model.md) is a narrower, requirement-by-requirement conformance model with defined evidence |
| **Atomic Red Team / CALDERA / Stratus Red Team** | Adversary emulation libraries | Validation | **Consumes them.** `DET-11` requires emulation-based validation; these are the recommended sources. The schema records which test validated which detection |
| **Vendor detection-as-code guides** (Splunk, Elastic, Google SecOps) | Platform-specific pipeline guidance | CI/CD for detections | **Generalises them.** [Detection as code](detection-as-code.md) is platform-neutral and adds conformance gates that vendor guides do not, because vendor guides do not define conformance |
| **OCSF / ECS / ASIM** | Telemetry normalization schemas | Data modeling | **Consumes them.** `TEL-7` requires a program to pick one; the framework does not prescribe which |
| **NIST CSF 2.0** | Cybersecurity governance framework | Detect and Respond functions | **Implements a slice of it.** CSF says an organization should detect; this framework says how, and maps back through `compliance_refs` |

---

## On Sigma specifically

Sigma solved rule portability. It did so convincingly and this framework does
not relitigate it.

Where VAL adds something is above the single-rule layer:

| Layer | Owned by |
| --- | --- |
| Intent: what must be true for this to be an attack | **VAL** |
| Correlation: how observable conditions combine, with confidence tiers | **VAL** |
| Single-event matching, portably expressed | **Sigma** |
| Platform execution | Platform backend |

A VAL with four blocks and the expression `B1 AND B2 AND B3 AND NOT B4` may be
implemented as one Sigma rule with filters, as four correlated Sigma rules, or
as a native platform correlation. All three satisfy the same VAL and are
validated against the same fixtures. That is the portability claim, and it
operates at a level Sigma's per-rule format does not address.

**Choosing between them is a category error.** Sigma expresses rule logic; this
framework governs the lifecycle those rules live in.

---

## What this framework deliberately does not do

Stating non-goals is part of positioning.

| Not this | Why |
| --- | --- |
| A detection content library | Detections are environment-specific. A shipped library would be a liability disguised as a head start |
| A rule language | Sigma exists and is good |
| A threat knowledge base | ATT&CK and ATLAS exist and are better maintained than any alternative could be |
| Prevention or recovery guidance | Scoped to Detect and Respond |
| Tool selection advice | Vendor-neutral by design; any recommendation would date within a year |
| A certification scheme | Self-assessment with defined evidence, plus optional independent assessment. Certification requires a neutral body this project does not yet have. See [GOVERNANCE.md](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/GOVERNANCE.md) |

---

## Acknowledgement

The ideas here are assembled, not invented. The framework's contribution is the
lifecycle, the conformance model, the schemas and the enforcement, not the
underlying insights about adversary behavior or detection quality, which belong
to the community and to the projects named above.

Where this framework disagrees with prior work it says so explicitly. The
clearest example is [detection metrics](detection-metrics.md), which argues that the classical
false positive rate is unusable in detection engineering despite its widespread
citation.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [The specification](specification.md) · **Back to the start:** [Welcome](README.md)

</div>
<!-- /journey:next -->
