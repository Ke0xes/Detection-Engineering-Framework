# Tuning and Metrics

## Dispositions

Every alert is closed with a disposition (`IMP-2`). The minimum set:

| Disposition | Meaning | Routes to |
| --- | --- | --- |
| `true-positive` | Genuine malicious or policy-violating activity | Incident response |
| `true-positive-benign` | The activity occurred as described but was authorized | Exception candidate |
| `false-positive-logic` | The detection logic is wrong | Detection engineering |
| `false-positive-data` | The logic is right; the telemetry was wrong, missing or malformed | Telemetry owner |
| `insufficient-context` | Could not be dispositioned from the alert without manual pivoting | Enrichment work |

The last three create an improvement backlog item automatically (`IMP-3`).
Separating logic from data matters: editing a rule to fix a data problem is
the most common reason tuning fails.

## Precision

```text
Precision = TP / (TP + FP)
```

Counted from dispositions over a rolling 30-day window (`MET-1`). Alerts that
were benign but expected count against Precision; they are not true
positives. Example: 220 alerts, 22 true positive, 190 false positive, 8 benign
but expected gives 22 / 220 = 0.10.

**Never report the false positive rate**, FP / (FP + TN). True negatives are
unbounded in an event stream, so the figure is always tiny and says nothing
about analyst experience. The same rule above, against 12 million events,
reports an FPR of about 0.0017 percent.

## Metric set and thresholds

| Metric | Definition | Threshold |
| --- | --- | --- |
| Precision | TP / (TP + FP), 30 days | Below 0.50 at L2, below 0.70 at L3: enters the tuning backlog (`MET-2`) |
| Alert volume | Alerts per detection per 30 days | Over 2x the delivery forecast: review |
| Analyst handling cost | Median minutes to disposition x volume | Cost above the detection's value: deprecation review |
| Escalation rate | Alerts escalated to incident / total alerts | Zero for 90 days: relevance review |
| Technique coverage | Techniques with an active detection / techniques in the prioritized threat profile | Reported quarterly; gaps feed planning |
| Confidence-weighted coverage | Coverage weighted by robustness and validation | Required at L3 (`MET-3`) |
| Data source coverage | Sources onboarded / sources the threat profile requires | Gap over 20% blocks L2 |
| Mean time to tune (MTTT) | Feedback to tuned rule in production | Under 7 days at L2, under 3 at L3 |
| Detection silence | Days since the detection last fired | Beyond expected interval: automated health alert (`MET-4`) |
| Log source liveness | Time since the last event from each required source | Beyond expected interval: automated health alert (`MET-4`) |
| Validation freshness | Days since last successful emulation | Over 90: detection marked unvalidated |
| Detection debt ratio | Detections past review date / active detections | Target under 15% (`IMP-9`) |

**False negatives** are reported as an enumerated list of gaps, each with an
owner and a remediation date, never as a count (`MET-5`). The evidence comes
from adversary emulation, incident retrospectives and purple team exercises.

**Alert-to-incident ratio** (alerts / alerts that became incidents) is a
program-level capacity measure. Use Precision for decisions about individual
detections.

## Change classes

Classify every change before starting work (`IMP-4`).

| Class | Description | Testing required | Approval |
| --- | --- | --- | --- |
| **C1 Exception** | Add or remove a specific exclusion | Regression test; confirm the exception is scoped and time-bound | Peer review |
| **C2 Threshold** | Adjust a threshold, window or baseline | Regression test plus a 30-day backtest | Peer review |
| **C3 Enrichment** | Add context without changing trigger logic | Confirm the enrichment resolves and performance holds | Peer review |
| **C4 Logic** | Change when the detection fires | Full validation suite and emulation re-run | Two reviewers and owner sign-off |
| **C5 Rebuild** | Replace the approach entirely | Full lifecycle, as a new detection | As for a new detection |
| **C6 Deprecation** | Retire the detection | Coverage impact assessment | Detection council |

Every change passes the existing fixtures before deployment (`IMP-13`) and is
deployed through the same staged path as a new detection (`IMP-14`). Record
the version, change class, author, reviewer and trigger (`IMP-15`).

## Tuning order of preference

1. **Fix the data** if dispositions are mostly `false-positive-data`.
2. **Tighten the logic** (C4) if the rule matches activity outside its
   hypothesis. Add a block, correct a condition, or narrow a field match.
3. **Enrich** (C3) if analysts mark alerts `insufficient-context`.
4. **Adjust a threshold** (C2), with a backtest, if the behavior is right but
   the level is wrong.
5. **Add an exception** (C1) only for a specific, understood, authorized
   activity, scoped as narrowly as possible.

## Exceptions

- Written in the rule under version control, never in the console (`DET-8`).
- Justification, owner and expiry date are mandatory (`IMP-5`).
- Expired exceptions are reviewed and renewed with fresh justification or
  removed; no silent renewal (`IMP-6`).
- Each has a boundary fixture (`DET-10`).
- More than the program threshold, default 10: escalate for a C5 rebuild
  assessment instead of adding another (`IMP-7`).
- Any exception forces a 90-day review cadence (`IMP-8`).

## Scheduled review

Review intervals: critical 90 days, high 180, medium and low 365, and 90 for
any detection with an open exception (`IMP-8`). Each review records a decision
on all seven points (`IMP-11`):

1. **Relevance.** Re-score threat relevance with the rubric.
2. **Efficacy.** A validation test result, not an opinion.
3. **Precision.** Above the level's threshold?
4. **Robustness.** Has the tier drifted because of exceptions or change?
5. **Telemetry.** Are required sources live, complete and parsed?
6. **Response.** Is the playbook accurate, and was it used?
7. **Cost.** Are query, ingest and handling costs proportionate?

## Silent detections and drift

Before changing the logic of a detection that has stopped firing, check for
drift (`IMP-12`):

| Cause | Example |
| --- | --- |
| Schema change | A vendor renames a field; the rule matches nothing |
| Parser change | The source is re-onboarded through a different pipeline |
| Sampling | Cost controls start sampling the source |
| Environmental change | The application moves to a platform with different telemetry |
| Exception accumulation | Exclusions now cover the attack path |
| Technique evolution | The adversary changes tooling and the indicator disappears |

Silence alone is not evidence that a detection is useless. A detection for a
rare, high-impact technique is meant to be quiet; only a validation test
tells the two apart. Never deprecate on low fire count alone (`IMP-17`).

## Deprecation

Allowed reasons (`lifecycle.deprecation.reason`):

| Reason | Criterion |
| --- | --- |
| `threat-irrelevant` | Threat relevance re-scored to 1 |
| `superseded` | A named successor gives equal or better coverage |
| `irreparable-precision` | Below threshold after two completed C4 cycles |
| `telemetry-withdrawn` | A required source is permanently gone with no alternative |
| `cost-disproportionate` | Total cost of ownership exceeds the risk reduction |
| `preventive-control-adopted` | The activity is now reliably blocked, and the block is monitored |

Procedure (`IMP-18`): assess coverage impact; notify the SOC, council and
requester (and the control owner for compliance detections); set status to
`deprecated` for at least one review cycle; then set `retired`, disabling but
never deleting (`IMP-19`); update the catalog and coverage model; retire
artifacts that existed only for this detection.
