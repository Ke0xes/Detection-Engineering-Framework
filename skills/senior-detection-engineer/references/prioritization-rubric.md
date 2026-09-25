# Prioritization Rubric

Use case requests are scored on five dimensions, each from 1 to 5, by matching
a written descriptor. Bare numbers without descriptors are not permitted
(`PLN-1`).

## Formula

```text
Priority = ((T x 3) + (A x 3) + (G x 2)) / (C + M)
```

Benefit is in the numerator and cost in the denominator. Threat relevance and
asset criticality carry the most weight; the size of the gap matters less.
Priority ranges from 0.80 (every benefit scored 1, every cost scored 5) to
20.00 (every benefit scored 5, every cost scored 1).

## Dimension 1: Threat relevance (T)

How credible is this threat against this organization?

| Score | Descriptor |
| --- | --- |
| 5 | Observed in the organization's environment, or a confirmed campaign against the organization in the last 90 days |
| 4 | Confirmed active against the organization's sector, named in a current CISA, NCSC or ISAC advisory |
| 3 | Actively exploited in the wild generally; no sector-specific reporting |
| 2 | Published technique with proof-of-concept tooling; no observed exploitation |
| 1 | Theoretical or research-stage technique |

## Dimension 2: Asset criticality (A)

What does this detection protect?

| Score | Descriptor |
| --- | --- |
| 5 | Crown jewel: loss causes material financial, safety or regulatory harm; tier 1 in the business impact analysis |
| 4 | Business-critical system or privileged identity infrastructure |
| 3 | Production system supporting a business process with a documented workaround |
| 2 | Supporting or internal system; degradation tolerable for days |
| 1 | Development, test or sandbox environment |

## Dimension 3: Coverage gap (G)

How exposed is the organization today?

| Score | Descriptor |
| --- | --- |
| 5 | No detection and no compensating preventive control |
| 4 | No detection; a preventive control exists but is known to be bypassable |
| 3 | Partial detection with known blind spots, or detection at a lower confidence tier |
| 2 | Detection exists but is brittle (indicator or ephemeral tier) |
| 1 | Robust detection already in place; this request is an enhancement |

## Dimension 4: Build cost (C)

| Score | Descriptor |
| --- | --- |
| 1 | Existing telemetry, existing pattern, under one engineer-day |
| 2 | Existing telemetry, new logic, under one engineer-week |
| 3 | Requires enrichment, correlation across sources, or a new baseline |
| 4 | Requires onboarding a new log source already available in the estate |
| 5 | Requires new instrumentation, agent deployment, or vendor change |

## Dimension 5: Maintenance burden (M)

| Score | Descriptor |
| --- | --- |
| 1 | Deterministic logic, stable telemetry, no expected tuning |
| 2 | Occasional exception maintenance expected |
| 3 | Threshold or baseline requires periodic recalibration |
| 4 | High environmental sensitivity; expected to break on infrastructure change |
| 5 | Requires continuous curation, such as indicator lists or user-behavior baselines |

## Worked example

| Request | T | A | G | C | M | Priority | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OAuth consent phishing against executive tenants | 5 | 5 | 4 | 2 | 2 | (15 + 15 + 8) / 4 = **9.50** | 1 |
| Kerberoasting | 3 | 4 | 3 | 2 | 1 | (9 + 12 + 6) / 3 = **9.00** | 2 |
| Credential dumping via LSASS access | 4 | 5 | 2 | 3 | 3 | (12 + 15 + 4) / 6 = **5.17** | 3 |
| Anomalous data egress volume | 3 | 4 | 5 | 4 | 5 | (9 + 12 + 10) / 9 = **3.44** | 4 |

The last request has the largest gap but the worst cost profile, and ranks
last.

## Rules of use

- **`PLN-2`.** Scores are recorded in the use case request record, not worked
  out at backlog grooming.
- **`PLN-3`.** `T = 5` routes to the expedited path, not the ranked backlog.
- **`PLN-4`.** Compliance requests carry a deadline and are scheduled against
  it. They share the backlog for capacity planning but are not ranked by
  score.
- **`PLN-5`.** The backlog is re-scored at least quarterly.
- **Ties.** The request with the lower build cost goes first.
- **Requesters do not score their own requests.** They supply the evidence;
  detection engineering and threat intelligence apply the descriptors.

## Expedited path

For confirmed active threats (`GOV-12` to `GOV-15`). The Minimum Viable
Detection is: a recorded hypothesis, one true-positive fixture, a named owner,
a response instruction, and a review date no more than 30 days away. At that
date the detection is brought to full conformance or withdrawn. Use of the
expedited path is reported to the detection council.

## Request completeness checks

A request is not ready for scoring unless it has:

- a business driver of type risk, threat or compliance, with justification
  (`GOV-1`);
- an objective and in-scope assets;
- explicit out-of-scope items (`PLN-6`);
- measurable success criteria, such as a target Precision or an acceptable
  alert volume per day (`PLN-7`); "improved visibility" does not qualify;
- a deadline, if compliance-driven (`PLN-4`).
