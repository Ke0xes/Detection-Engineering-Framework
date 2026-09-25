# Detection Metrics

<!-- journey:where -->
*Walk the lifecycle › Improvement › Going deeper*
<!-- /journey:where -->

The improvement phase depends on evidence: which detections are noisy, which
have gone silent, what is not covered, and what the program costs to run. Many
programs report alert counts and a percentage described as a false positive
rate, but neither figure tells an engineer what to fix or a manager where to
invest.

This deep dive defines the measures the framework uses, how each is
calculated, and the thresholds at which it should prompt action. It begins with
the false positive rate, because the reasons it misleads explain the choice of
its replacement.

> **Running example.** Over 30 days the consent phishing detection produced 23
> alerts, of which analysts confirmed 78% as genuine. That figure, its
> Precision, is above the level the framework sets for a mature program. The
> detection last fired the day before it was measured, and its most recent
> validation test passed.

---

## The false positive rate trap

Classical detection theory defines the false positive rate as:

$$
FPR = \frac{FP}{FP + TN}
$$

where $TN$ is the count of benign events correctly *not* alerted on.

**This metric MUST NOT be used as a detection engineering KPI.** It is not
merely inconvenient to compute; it is undefined in practice.

| Problem | Explanation |
| --- | --- |
| $TN$ is unbounded | A detection evaluates a continuous event stream. "Benign events correctly identified as benign" has no natural denominator. Is it every process execution? Every log line? Every second the rule did not fire? Each choice yields a different answer. |
| $TN$ is unmeasurable | Nothing in a SIEM records a true negative. There is no artifact to count. |
| It is dominated by the denominator | Because $TN \gg FP$ in any real telemetry stream, $FPR$ is always a tiny number. A rule producing 400 false alerts a day against 50 million events still reports an $FPR$ of 0.0008%. The metric reports "excellent" while the SOC drowns. |
| It hides the only thing analysts care about | Analysts experience the *alert queue*, not the event stream. What matters is: of the alerts I was given, how many were worth my time? |

Any published $FPR$ figure that includes a specific $TN$ count is reporting a
fabricated number, because that count was not measured. It was assumed.

### What to report instead

Report **Precision**, also called alert fidelity or positive predictive value:

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

Every term is directly observable from case management data. $TP$ is the count
of alerts dispositioned as true positive; $FP$ is the count dispositioned as
false positive. Nothing is inferred.

**MET-1.** A conforming program MUST report per-detection Precision over a
rolling 30-day window and MUST NOT report $FPR$ as a substitute.

### Worked example

A rule monitoring suspicious authentication fires 220 times in 30 days. Analyst
disposition: 22 true positive, 190 false positive, 8 benign-but-expected
(exception candidates).

$$
\text{Precision} = \frac{22}{22 + 190 + 8} = \frac{22}{220} = 0.10
$$

Precision is **10%**. Nine out of ten alerts waste analyst time. This rule
breaches the action threshold in MET-2 and enters the tuning backlog.

Under the classical formula, and assuming the rule evaluated 12 million
authentication events, the same rule would report:

$$
FPR = \frac{198}{198 + 11{,}999{,}782} \approx 0.0000165
$$

0.0017% — which sounds exemplary. The two numbers describe the same rule. Only
one of them prompts the correct action.

---

## The required metric set

A conforming program MUST produce the following. Metrics are grouped by the
question they answer.

### Quality: is this detection worth the queue space?

| Metric | Definition | Action threshold |
| --- | --- | --- |
| **Precision** | $TP / (TP + FP + \text{benign})$ over 30 days | `< 0.50` at L2, `< 0.70` at L3 enters tuning backlog |
| **Alert volume** | Absolute alerts per detection per 30 days | `> 2x` forecast from delivery triggers review |
| **Analyst handling cost** | Median minutes to disposition x alert volume | Cost `>` value of detection triggers deprecation review |
| **Escalation rate** | Alerts escalated to incident / total alerts | Persistent `0` over 90 days triggers relevance review |

**MET-2.** Any detection whose Precision falls below the conformance-level
threshold MUST be entered into the tuning backlog within one review cycle.

### Coverage: what are we blind to?

| Metric | Definition | Action threshold |
| --- | --- | --- |
| **Technique coverage** | Distinct ATT&CK techniques with `>=1` active detection / techniques in the organization's prioritized threat profile | Reported quarterly; gaps feed the planning backlog |
| **Confidence-weighted coverage** | Coverage weighted by validated detection quality, not rule count | Preferred over raw count; see [Detection Robustness](detection-robustness.md) |
| **Data source coverage** | Log sources onboarded / log sources required by the threat profile | Gap `> 20%` blocks L2 conformance |

Raw technique counts are a vanity metric. Ten brittle rules mapped to T1059 do
not constitute coverage of T1059. **MET-3.** Coverage reporting MUST be
confidence-weighted at L3.

### Timeliness: how fast does the system respond?

| Metric | Definition | Target |
| --- | --- | --- |
| **MTTD** | Adversary action timestamp to alert timestamp | Per severity tier; defined in SLA |
| **Mean Time to Triage** | Alert creation to first analyst disposition | Per severity tier |
| **Mean Time to Tune (MTTT)** | Feedback submission to tuned rule in production | `< 7` days at L2, `< 3` days at L3 |
| **Time to deploy** | Approved use case request to production detection | Tracked for capacity planning |

### Health: is the detection still alive?

This is the most under-implemented metric class in the industry and the one that
most often causes silent failure.

| Metric | Definition | Action threshold |
| --- | --- | --- |
| **Detection silence** | Days since the detection last fired | Exceeds expected interval -> automated health alert |
| **Log source liveness** | Time since last event from each required source | Any gap `>` expected interval -> automated health alert |
| **Validation freshness** | Days since last successful adversary emulation test | `> 90` days -> detection marked `unvalidated` |
| **Detection drift** | Validation tests passing now vs. at deployment | Any regression -> immediate backlog entry |

**MET-4.** A conforming program MUST monitor detection silence and log source
liveness automatically, and MUST raise an operational alert on breach. A
detection that cannot fire is indistinguishable from a detection that found
nothing; only instrumentation separates the two.

### Program: is the function sustainable?

| Metric | Definition | Purpose |
| --- | --- | --- |
| **Detection debt ratio** | Detections past review date / total active detections | Capacity planning; target `< 15%` |
| **Backlog age** | Median age of open use case requests | Demand vs. capacity signal |
| **Deprecation rate** | Detections retired per quarter | A rate of zero indicates the catalog is not being maintained |
| **Telemetry cost per detection** | Ingest + storage cost attributable to required sources | See [Telemetry and Data](telemetry-and-data.md) |

---

## Alert-to-incident ratio

The original framework text described "false positive ratio" as the ratio
between total alerts and alerts relating to incidents. That is a legitimate and
useful metric, but it is *not* the false positive rate. It is named here
correctly:

$$
\text{Alert-to-incident ratio} = \frac{\text{alerts}}{\text{alerts that became incidents}}
$$

It is a program-level efficiency measure. Use Precision for per-detection
decisions and alert-to-incident ratio for program-level capacity discussion.
Do not conflate them.

---

## On false negatives

False negatives cannot be counted directly. If they could be counted, they would
not be false negatives. Any program claiming a false negative *rate* is either
measuring something else or guessing.

What a conforming program MUST do instead is **estimate** false negatives
through three observable proxies:

1. **Adversary emulation results.** Run a known technique; if no detection
   fires, that is a measured, attributable false negative. This is the only
   direct evidence available.
2. **Incident retrospectives.** For every incident, ask which detections *should*
   have fired and did not. Record the answer as a gap, not as a count.
3. **Purple team exercises.** Structured, scoped, adversary-informed testing
   against the current production configuration.

**MET-5.** False negatives MUST be reported as an enumerated list of identified
detection gaps with owners and remediation dates, never as a bare number.

---

## Reporting cadence

| Audience | Cadence | Content |
| --- | --- | --- |
| Detection engineering team | Weekly | Precision outliers, health alerts, backlog movement |
| SOC leadership | Monthly | Alert volume, handling cost, MTTT, top noisy detections |
| Security leadership | Quarterly | Coverage vs. threat profile, validated gaps, debt ratio, investment asks |
| Risk and audit | Quarterly | Traceability from business drivers to active detections |

**MET-6.** Every metric reported to leadership MUST be traceable to a defined
formula in this chapter. Undefined composite scores and vendor "security
posture" indices MUST NOT be presented as conformance evidence.

---

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Reporting $FPR$ with an assumed $TN$ | Fabricated precision; invites justified scepticism |
| Counting rules as coverage | Ten brittle rules are not coverage |
| Measuring MTTD from alert time | Measures the SOC's clock, not the adversary's dwell time |
| Tracking alert volume alone | Volume without disposition data supports no decision |
| A single "detection health score" | Composite scores hide the variable that needs action |
| Never deprecating | A catalog that only grows is a catalog nobody trusts |

---

## In brief

- Precision, the share of a detection's alerts that analysts confirm as genuine,
  is the primary quality measure. It is read directly from case records.
- The classical false positive rate is not used, because it depends on a count
  of true negatives that cannot be measured in a stream of events.
- Coverage is weighted by how robust and how recently validated each detection
  is, rather than counted by rule.
- Detection silence and log source liveness are monitored automatically,
  because a detection that cannot fire looks the same as one that found
  nothing.
- Missed detections are reported as a named list of gaps with owners, not as a
  number.

## Requirements in this chapter

The requirements `MET-1` to `MET-6` appear in the sections above. The
[specification](specification.md#14-conformance-summary) shows the conformance
level of each.

## What comes next

This completes the walk through the lifecycle. The next part of the guide turns
to applying the framework in a real organization, beginning with
[adopting the framework](from-theory-to-practice.md): the obstacles teams meet
in practice, and how to start small and grow.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [The improvement phase](improvement-phase.md) · **Next:** [Adopting the framework](from-theory-to-practice.md)

</div>
<!-- /journey:next -->
