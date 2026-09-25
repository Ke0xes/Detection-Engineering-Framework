# Assessing a Program

<!-- journey:where -->
*Put it into practice › Assessing a program*
<!-- /journey:where -->

A program that adopts the framework will want to know how far it has come, and
stakeholders such as auditors, regulators and leadership may ask the same
question. This chapter describes the conformance model used to answer it: three
cumulative levels, the evidence each requirement needs, and the rules for what
a program may claim.

The levels are designed so that the first is achievable by a small team with no
tooling budget. Level 1 asks whether a program knows what detections it has and
why. Level 2 asks whether they are engineered and governed. Level 3 asks whether
the program measures, validates and corrects itself.

> **Running example.** The consent phishing detection's record in the reference
> implementation passes every automated check the framework defines.
> Conformance, however, is assessed for a program as a whole: a single
> well-documented detection does not make a conforming program.

---

## The three levels

Levels are cumulative. L3 includes everything in L2, which includes everything
in L1.

| | **L1 Foundational** | **L2 Managed** | **L3 Optimised** |
| --- | --- | --- | --- |
| **Question it answers** | Do we know what we have and why? | Is it engineered and governed? | Is it measured, validated and self-correcting? |
| **Typical team** | 1-3 people wearing several hats | Dedicated detection function | Detection function with platform support |
| **Typical duration to reach** | One quarter | Two to four quarters from L1 | Two to four quarters from L2 |
| **Detection logic lives in** | Version control | Version control, reviewed | Version control, reviewed, deployed by pipeline |
| **Testing** | Manual, documented | Fixtures in CI | Fixtures plus continuous adversary emulation |
| **Metrics** | Precision reported | Precision drives a real backlog | Full metric set; health monitored automatically |
| **Improvement** | Reactive, tracked | Scheduled reviews enforced | Drift detected automatically; deprecation routine |

### L1 Foundational

**The claim:** *we know what detections we have, why each exists, and who owns
it.*

L1 is deliberately achievable by a two-person team with no budget. It requires
no CI, no pipeline and no commercial tooling. It requires discipline.

An L1 program has:

- Every detection in version control with conforming metadata (`GOV-9`, `DAC-1`)
- Every detection traced to a business driver and its telemetry (`GOV-1`, `GOV-2`)
- A named accountable owner per detection (`GOV-5`)
- An anchored prioritization rubric in use (`PLN-1`)
- Scope and success criteria on every request (`PLN-6`, `PLN-7`)
- Telemetry confirmed before build (`FEA-1`)
- A hypothesis, severity, confidence and benign causes recorded per detection
  (`DET-1`, `DET-4`, `DET-6`)
- A response playbook per production detection (`RSP-1`)
- A generated catalog (`DEL-5`)
- Exceptions that are time-bound (`IMP-5`) and review dates that exist (`IMP-8`)
- Precision reported, and the classical FPR not reported (`MET-1`)
- False negatives reported as enumerated gaps (`MET-5`)

**The single most common L1 failure** is metadata held in the SIEM console
rather than in version control. It feels equivalent. It is not: it cannot be
diffed, reviewed, restored, or read when the platform is unavailable.

### L2 Managed

**The claim:** *our detections are engineered, reviewed and governed, and the
feedback loop actually closes.*

L2 adds, beyond L1:

- Machine-readable traceability answerable in both directions (`GOV-3`, `GOV-4`)
- A functioning detection council (`GOV-6`) and a documented RACI (`GOV-8`)
- A defined expedited path with a Minimum Viable Detection definition
  (`GOV-12`, `GOV-13`, `GOV-14`)
- Peer-reviewed changes with automated validation gating merge
  (`DAC-2`, `DAC-3`, `DAC-4`)
- VAL recorded per detection (`DET-2`); alert disposition declared (`DET-5`)
- Exceptions under version control (`DET-8`)
- Positive and negative fixtures per production detection (`DET-9`)
- Mandatory disposition on alert closure, auto-creating backlog items
  (`IMP-2`, `IMP-3`)
- Change classification before work begins (`IMP-4`)
- Reviews that cover all seven required dimensions (`IMP-11`)
- Regression testing before deployment (`IMP-13`); controlled deployment
  (`IMP-14`)
- Alert forecasting before activation (`DEL-2`); defined rollback (`DEL-4`)
- A deprecation path that is actually used (`IMP-16`, `IMP-18`, `IMP-19`)
- Precision thresholds that trigger backlog entry (`MET-2`)

**The single most common L2 failure** is the feedback loop. Teams implement
everything else and leave alert disposition optional. It then does not happen,
and `IMP-3` cannot function because there is no input.

### L3 Optimised

**The claim:** *we know when our detections stop working, and we find out from
instrumentation rather than from an incident.*

L3 adds, beyond L2:

- Fixture tests and automated deployment from reviewed source
  (`DAC-5`, `DAC-6`)
- Drift reconciliation against the platform (`DAC-7`) and executable rollback
  (`DAC-8`)
- Telemetry cost assessed at the feasibility gate (`FEA-3`); emulation before
  logic (`FEA-4`)
- Robustness tiering actively managed (`DET-7`); exception boundary fixtures
  (`DET-10`)
- Adversary emulation before production, recorded (`DET-11`); non-functional
  testing at production scale (`DET-12`)
- Playbooks exercised jointly (`RSP-4`); automation with defined failure modes
  (`RSP-5`)
- Staged rollout with canary observation (`DEL-3`)
- Automated drift detection (`IMP-12`); protected improvement capacity
  (`IMP-10`)
- Detection debt below 15% and reported monthly (`IMP-9`)
- Change advisory integration as an improvement trigger (`IMP-20`)
- Confidence-weighted coverage reporting (`MET-3`); automated health monitoring
  (`MET-4`)

**The single most common L3 failure** is validation freshness. Programs build
the emulation capability, run it once at deployment, and never schedule it.
Detection drift then accumulates invisibly, which is precisely the failure L3
exists to prevent.

---

## What may be claimed

**CNF-1.** A conformance claim MUST state all four of: the level, the
specification version, the assessment date, and the scope of the assessed
environment.

A valid claim:

> Conforms to Detection Engineering Framework v2.1.1 at Level 2, assessed
> 2026-09-01, scope: corporate IT estate and Microsoft 365 tenant. Excludes
> OT networks and the acquired subsidiary environment.

An invalid claim:

> DEF compliant.

**CNF-2.** A program MUST NOT claim a level unless **every** requirement at that
level and below is met. There is no partial credit at a level. Partial progress
is reported as "L1 conformant, L2 in progress (34 of 41 requirements met)".

**CNF-3.** Scope exclusions MUST be stated explicitly. A claim that silently
excludes half the estate is a false claim.

**CNF-4.** A conformance claim MUST be reassessed at least annually, and MUST be
reassessed after any material change in platform, team structure or scope.

---

## Assessment

### Self-assessment

The instrument is in
[`assessment/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/assessment).
Each requirement is scored:

| Score | Meaning |
| --- | --- |
| `met` | Implemented, and evidence exists |
| `partial` | Implemented for some detections or some environments only |
| `not-met` | Not implemented |
| `n/a` | Not applicable; a written justification is REQUIRED |

**CNF-5.** A requirement scored `met` MUST have identifiable evidence.
"We do that" is not evidence. The instrument names acceptable evidence for each
requirement.

**CNF-6.** `n/a` MUST carry a written justification and MUST be approved by the
detection council. Unjustified `n/a` scoring is the most common way
self-assessment becomes theatre.

### Evidence types

| Evidence type | Example |
| --- | --- |
| **Artifact** | A conforming metadata file in the repository |
| **Execution** | A CI run showing the validation gate passing |
| **Record** | A council minute approving a deprecation |
| **Query** | A traceability query returning detections for a given driver |
| **Observation** | An assessor watching an analyst disposition an alert |

Artifact and execution evidence are strongest because they are hard to fake and
cheap to re-verify. A conforming program should be able to satisfy most of the
instrument by pointing at its repository and its pipeline.

### Independent assessment

**CNF-7.** An L3 claim SHOULD be validated by an assessor independent of the
detection engineering function. Self-assessment at L3 is acceptable but weaker,
because the requirements that matter most at L3 are the ones a team is most
likely to rate generously.

---

## Trajectory, not destination

Level is a snapshot. A program at L2 with detection debt falling and coverage
rising is healthier than a program at L3 with debt rising and validation stale.

**CNF-8.** Conformance reporting SHOULD include trend, not only level. The
minimum useful trend set is: detection debt percentage, validation freshness,
median precision, and count of detections deployed via the expedited path that
have not been brought to full conformance.

---

## On not skipping L1

The most frequent adoption failure is a team at L1 maturity attempting to
implement L3 controls, because L3 is what conference talks describe. They build
a CI pipeline before they have consistent metadata, and the pipeline has nothing
meaningful to validate.

Build the metadata first. A repository of conforming detection records with no
automation at all is more valuable than an automated pipeline operating on
inconsistent data, because the former can be automated later and the latter
must be redone.

---

## In brief

- There are three cumulative levels: L1 Foundational, L2 Managed and L3
  Optimised. A level is reached only when every requirement at that level and
  below is met.
- Every requirement scored as met needs identifiable evidence, and anything
  scored as not applicable needs a written justification.
- A valid claim states the level, the specification version, the assessment
  date and the scope.
- Trend matters as much as level. A program improving at L2 may be healthier
  than one declining at L3.

## Requirements in this chapter

The rules for claims and assessment, `CNF-1` to `CNF-8`, appear in the sections
above. The requirements being assessed are listed by level in the
[specification](specification.md#14-conformance-summary).

## What comes next

Assessment is easier with the right starting material.
[Tools and templates](tools-and-templates/README.md) lists the intake forms,
schemas, reference implementation and self-assessment instrument that
accompany the framework.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [Advanced practices](best-practices.md) · **Next:** [Tools and templates](tools-and-templates/README.md)

</div>
<!-- /journey:next -->
