# Detection Engineering Framework Specification

*[Framework index](index.md) · [Conformance](10-conformance.md)*

| | |
| --- | --- |
| **Specification version** | 3.0.0 |
| **Status** | Active |
| **Date** | 2026-09-23 |
| **Supersedes** | 2.0 (prose-only, non-normative) |

---

## 1. Scope and purpose

This document is the normative core of the Detection Engineering Framework. It
states what an organization MUST, SHOULD and MAY do to operate a conforming
detection engineering program.

The remaining chapters in this repository are explanatory. Where this
specification and an explanatory chapter disagree, this specification governs.

This specification addresses the **Detect** and **Respond** functions. It does
not address prevention, recovery or governance of the wider security program
except where those intersect with detection.

### 1.1 Requirement keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY** and **OPTIONAL** are to be
interpreted as described in RFC 2119 and RFC 8174, and only when they appear in
capitals.

### 1.2 Requirement identifiers

Every normative requirement carries a stable identifier of the form `XXX-n`.
Identifiers are permanent. A withdrawn requirement is marked withdrawn; its
identifier is never reused.

| Prefix | Domain | Defined in |
| --- | --- | --- |
| `GOV` | Governance, roles and accountability | This document, [15](15-governance-and-roles.md) |
| `PLN` | Planning and prioritization | [03](03-planning-phase.md) |
| `TEL` | Telemetry and data | [12](12-telemetry-and-data.md) |
| `FEA` | Technical feasibility | This document |
| `DET` | Detection engineering | This document, [13](13-detection-robustness.md) |
| `RSP` | Response engineering | This document |
| `DAC` | Detection as code | [11](11-detection-as-code.md) |
| `DEL` | Delivery | This document |
| `IMP` | Improvement | [08](08-improvement-phase.md) |
| `MET` | Metrics | [09](09-metrics.md) |

### 1.3 Conformance

Conformance is claimed at Level 1, 2 or 3 as defined in
[Conformance Model](10-conformance.md). A conformance claim MUST state the
level, the specification version, the assessment date and the scope of the
assessed environment.

A claim of the form "conforms to the Detection Engineering Framework" without a
level and version is meaningless and MUST NOT be made.

---

## 2. Definitions

| Term | Definition |
| --- | --- |
| **Use case** | A security monitoring scenario aimed at detecting manifestations of cyber threats, managing risk, and aligning with compliance requirements, together with the response it guides. A use case has strategic, tactical and operational components. |
| **Detection** | A single implemented artifact that evaluates telemetry and produces a signal. One use case may yield many detections. |
| **Detection logic** | The executable expression of a detection on a specific platform. |
| **VAL** (Vendor Agnostic Logic) | The platform-independent statement of a detection's intent, expressed as named observable conditions and a boolean relationship between them. |
| **Block** | A single named observable condition within a VAL. |
| **Signal** | The output of a detection. A signal may alert, correlate, enrich or feed hunting, per its declared disposition. |
| **Alert** | A signal that is placed in an analyst queue for disposition. |
| **Detection debt** | The state of a detection that has passed its review date. |
| **Detection drift** | Degradation in a detection's efficacy caused by change in telemetry, environment or adversary tradecraft, without any change to the detection itself. |
| **Robustness tier** | A detection's resistance to adversary evasion, per [13](13-detection-robustness.md). |
| **Exception** | A scoped, time-bound suppression applied to a detection. |
| **Detection council** | The cross-functional body accountable for detection strategy, prioritization and deprecation decisions. |

---

## 3. Foundational requirements

### 3.1 Traceability

Two-way traceability is the framework's central principle. Without it, a
detection program cannot demonstrate why it monitors what it monitors, nor what
would be lost if it stopped.

**GOV-1.** Every detection MUST be traceable upward to at least one recorded
business driver of type risk, threat or compliance.

**GOV-2.** Every detection MUST be traceable downward to the specific telemetry
sources it depends upon.

**GOV-3.** Traceability MUST be machine-readable. It MUST NOT exist only in
prose documentation or in a wiki page maintained by hand.

**GOV-4.** Given any business driver, a conforming program MUST be able to
enumerate the active detections implementing it. Given any detection, it MUST
be able to enumerate the drivers it serves. Both directions MUST be answerable
without manual research.

### 3.2 Accountability

**GOV-5.** Every detection MUST have a named accountable owner. The owner MUST
be a team, not an individual.

**GOV-6.** A conforming program MUST operate a detection council with
representation from, at minimum: detection engineering, security operations,
incident response, threat intelligence, and a business or compliance
stakeholder.

**GOV-7.** The detection council MUST be the decision authority for
prioritization disputes, deprecation, and exception approval above the
program-defined threshold.

**GOV-8.** Roles and responsibilities MUST be documented as a RACI covering at
minimum: use case intake, feasibility assessment, detection build, peer review,
deployment approval, tuning, and deprecation. See
[Governance and Roles](15-governance-and-roles.md).

### 3.3 Documentation as artifact

**GOV-9.** Detection metadata MUST conform to
[`schema/detection.schema.json`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/schema/detection.schema.json)
or to a documented superset of it.

**GOV-10.** Use case requests MUST conform to
[`schema/use-case.schema.json`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/schema/use-case.schema.json)
or to a documented superset of it.

**GOV-11.** Detection metadata MUST be version-controlled alongside the
detection logic it describes. Metadata held only in a detection platform's
user interface does not satisfy this requirement, because it cannot be
diffed, reviewed or restored.

---

## 4. Planning phase

**PLN-1** to **PLN-5** are defined in [Planning Phase](03-planning-phase.md).
Summarised:

| ID | Requirement |
| --- | --- |
| `PLN-1` | Requests MUST be scored using an anchored rubric with written descriptors for every level |
| `PLN-2` | Scores MUST be recorded in the request record |
| `PLN-3` | Confirmed active threats MUST route to the expedited path |
| `PLN-4` | Compliance requests MUST be scheduled against their deadline |
| `PLN-5` | The backlog MUST be re-scored at least quarterly |

Additionally:

**PLN-6.** A use case request MUST state what is explicitly out of scope.
Requests without recorded non-goals MUST NOT be accepted, because scope
disputes at handover are otherwise unresolvable.

**PLN-7.** A use case request MUST state measurable success criteria. "Improved
visibility" is not a success criterion.

**PLN-8.** A request MUST NOT proceed to development before a feasibility
assessment has recorded telemetry availability.

---

## 5. Development phase A: technical feasibility

**FEA-1.** Before detection logic is written, the required telemetry MUST be
confirmed present, complete and queryable in the target platform. Assumed
telemetry MUST NOT be treated as available.

**FEA-2.** The feasibility assessment MUST record, for each required source:
availability, retention, expected arrival interval, normalization scheme, and
known field-coverage gaps.

**FEA-3.** The feasibility assessment MUST record the estimated ingest and
storage cost of any telemetry not already collected. Detections whose telemetry
cost exceeds the assessed risk reduction SHOULD be rejected at this gate rather
than discovered to be uneconomic after deployment.

**FEA-4.** Where the detection targets a technique not previously observed in
the environment, the program SHOULD generate the telemetry through adversary
emulation before writing logic. Writing detection logic against assumed
telemetry field values is the single most common cause of detections that pass
review and fail in production.

**FEA-5.** The output of the feasibility assessment MUST be recorded against
the use case request and MUST be available to the reviewer at detection
approval.

---

## 6. Development phase B: detection engineering

### 6.1 Intent before implementation

**DET-1.** Every detection MUST record a hypothesis: a single statement of the
form *if an adversary does X, then Y will be observable in Z*.

**DET-2.** Every detection MUST record a VAL, being the platform-independent
statement of its logic. Every platform implementation MUST satisfy the VAL.

**DET-3.** Where a detection is implemented on more than one platform, all
implementations MUST be traceable to the same VAL and MUST be validated against
the same fixtures.

### 6.2 Quality attributes

**DET-4.** Every detection MUST declare a severity, a confidence and a
robustness tier.

**DET-5.** Every detection MUST declare an alert disposition. Not every
detection SHOULD produce an analyst alert; correlate-only, enrich-only and
hunt-only are legitimate and under-used dispositions.

**DET-6.** Every detection MUST document its known benign causes together with
triage guidance written for an analyst who has no context.

**DET-7.** A detection whose logic depends on an ephemeral indicator (a hash,
an IP address, a domain) MUST declare robustness tier `ephemeral` or
`indicator` and MUST declare the curation process that maintains it. Indicator
lists that nobody owns decay into pure noise.

### 6.3 Exceptions

**DET-8.** Exceptions MUST be expressed in the detection logic under version
control, not applied out of band in the detection platform's user interface.
An exception that is invisible to code review is an undocumented change to a
security control.

`IMP-5` to `IMP-7` govern exception lifecycle.

### 6.4 Testing

**DET-9.** Every detection MUST ship with at least one true-positive fixture
and at least one true-negative fixture before reaching `production` status.

**DET-10.** Every exception MUST ship with a fixture asserting its boundary:
that it suppresses what it claims to suppress and nothing adjacent.

**DET-11.** A detection MUST be validated against adversary emulation before
reaching `production` status, and the result MUST be recorded. Where emulation
is not technically possible, the program MUST record why, and the detection
MUST be marked as unvalidated in coverage reporting.

**DET-12.** Non-functional testing MUST establish query cost and execution time
against production-scale data before deployment.

---

## 7. Development phase C: response engineering

**RSP-1.** A detection MUST NOT reach `production` status without a linked
response playbook. A detection without a response plan generates work, not
security.

**RSP-2.** The playbook MUST state, at minimum: preparation prerequisites,
triggers by confidence, investigation steps, the incident declaration decision
point, containment actions, recovery steps, and post-incident activity.

**RSP-3.** The playbook MUST state which containment actions the SOC is
pre-authorised to take without further approval. Ambiguity about authority is
resolved slowly, and it is resolved during the incident.

**RSP-4.** The playbook MUST be exercised jointly with the consuming team
before handover. A tabletop walkthrough satisfies this; a document review does
not.

**RSP-5.** Where response is automated, the automation MUST have a defined
failure mode and MUST NOT fail open silently.

**RSP-6.** Playbooks MUST be reviewed on the same cadence as the detections
that trigger them.

---

## 8. Detection as code

**DAC-1** to **DAC-8** are defined in
[Detection as Code](11-detection-as-code.md). Summarised:

| ID | Requirement |
| --- | --- |
| `DAC-1` | Detection logic and metadata MUST be version-controlled |
| `DAC-2` | Changes MUST be made through reviewed pull requests |
| `DAC-3` | At least one reviewer other than the author MUST approve |
| `DAC-4` | Automated validation MUST gate merge |
| `DAC-5` | Fixture tests MUST gate merge |
| `DAC-6` | Deployment to production MUST be automated from the reviewed source |
| `DAC-7` | Out-of-band changes in the platform MUST be detected and reconciled |
| `DAC-8` | Rollback MUST be possible without manual reconstruction |

---

## 9. Delivery phase

**DEL-1.** A detection MUST NOT be activated in production without a recorded
handover that includes: the planning record, the feasibility assessment, the
detection metadata, validation results, stakeholder approvals, an alert volume
forecast, and the response playbook.

**DEL-2.** An alert volume forecast MUST be produced before activation, by
executing the detection logic against historical data. Activating a detection
without a forecast risks an alert storm that the framework exists to prevent.

**DEL-3.** Detections MUST be deployed through a staged rollout: a limited
scope first, with defined observation criteria, before full activation.

**DEL-4.** A rollback procedure MUST be defined and MUST be executable without
the original author.

**DEL-5.** Every detection MUST be entered in the detection catalog at
activation. The catalog MUST be generated from the version-controlled metadata,
not maintained separately.

**DEL-6.** The consuming team MUST be given a defined period to review and
object before activation. The period MUST be recorded.

**DEL-7.** Activation date and the agreed notification behavior MUST be
recorded.

---

## 10. Improvement phase

**IMP-1** to **IMP-20** are defined in
[Improvement Phase](08-improvement-phase.md).

---

## 11. Metrics

**MET-1** to **MET-6** are defined in [Detection Metrics](09-metrics.md).

Of these, two are the most commonly breached and bear repeating here:

**MET-1.** Precision MUST be reported per detection. The classical false
positive rate $FP/(FP+TN)$ MUST NOT be reported as a detection engineering KPI,
because $TN$ is unmeasurable in an event stream and any stated value is
fabricated.

**MET-5.** False negatives MUST be reported as an enumerated list of identified
gaps with owners and dates, never as a bare count.

---

## 12. Telemetry and data

**TEL-1** to **TEL-7** are defined in
[Telemetry and Data](12-telemetry-and-data.md).

---

## 13. The expedited path

A framework that cannot respond to an active threat faster than its standard
lifecycle is a liability. This is a normative part of the framework, not an
exception to it.

**GOV-12.** A conforming program MUST define an expedited path for confirmed
active threats, and MUST define who may invoke it.

**GOV-13.** The expedited path MUST define a Minimum Viable Detection: the
smallest artifact set acceptable for production deployment. The framework's
baseline MVD is a recorded hypothesis, one true-positive fixture, a named owner,
a response instruction, and a mandatory review date.

**GOV-14.** Every detection deployed through the expedited path MUST carry a
review date no more than 30 days out, at which it is either brought to full
conformance or withdrawn. Expedited detections MUST NOT persist indefinitely in
reduced-rigour form.

**GOV-15.** Use of the expedited path MUST be reported to the detection council.
Sustained high usage indicates the standard path is too slow and is a signal
about the process, not about the engineers.

---

## 14. Conformance summary

| Requirement family | L1 Foundational | L2 Managed | L3 Optimised |
| --- | --- | --- | --- |
| `GOV` | 1, 2, 5, 9, 10 | + 3, 4, 6, 8, 11, 12, 13, 14 | + 7, 15 |
| `PLN` | 1, 6, 7 | + 2, 3, 4, 8 | + 5 |
| `FEA` | 1 | + 2, 5 | + 3, 4 |
| `DET` | 1, 4, 6 | + 2, 5, 8, 9 | + 3, 7, 10, 11, 12 |
| `RSP` | 1 | + 2, 3, 6 | + 4, 5 |
| `DAC` | 1 | + 2, 3, 4 | + 5, 6, 7, 8 |
| `DEL` | 5 | + 1, 2, 4, 6, 7 | + 3 |
| `IMP` | 1, 5, 8 | + 2, 3, 4, 6, 11, 13, 14, 16, 18, 19 | + 7, 9, 10, 12, 15, 17, 20 |
| `MET` | 1, 5 | + 2, 6 | + 3, 4 |
| `TEL` | 1 | + 2, 3, 5 | + 4, 6, 7 |

The full assessment instrument is in
[`assessment/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/assessment).

---

## 15. Versioning of this specification

This specification follows semantic versioning.

| Change | Version increment |
| --- | --- |
| New MUST requirement, or a SHOULD promoted to MUST | MAJOR |
| New SHOULD or MAY, or clarification that does not change conformance | MINOR |
| Editorial correction | PATCH |

**Conformance claims MUST name the specification version.** A program
conforming to 3.0.0 does not automatically conform to 4.0.0.

Deprecated requirements are retained in the document marked `WITHDRAWN` with
the version in which they were withdrawn, so that historical conformance claims
remain interpretable.

---

*Next: [Background and Introduction](01-introduction.md) · [Conformance Model](10-conformance.md)*
