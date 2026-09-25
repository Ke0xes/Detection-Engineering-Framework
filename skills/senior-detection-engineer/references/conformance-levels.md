# Conformance Levels

A program conforms at Level 1, 2 or 3. Levels are cumulative: L2 includes all
of L1, and L3 includes all of L2. A level is attained only when every
requirement at that level and below is met; there is no partial credit
(`CNF-2`).

| | L1 Foundational | L2 Managed | L3 Optimised |
| --- | --- | --- | --- |
| Question | Does the program know what it has and why? | Is it engineered and governed? | Is it measured, validated and self-correcting? |
| Typical team | 1 to 3 people with several roles | A dedicated detection function | A detection function with platform support |
| Detection logic | In version control | In version control, reviewed | Reviewed and deployed by pipeline |
| Testing | Manual, documented | Fixtures in CI | Fixtures plus continuous emulation |
| Metrics | Precision reported | Precision drives a backlog | Full metric set; health monitored automatically |

## Level 1: Foundational

| ID | Requirement |
| --- | --- |
| `GOV-1` | Every detection traces to a recorded risk, threat or compliance driver |
| `GOV-2` | Every detection traces to the telemetry it depends on |
| `GOV-5` | Every detection has an accountable owning team |
| `GOV-9` | Detection metadata conforms to the detection schema, or a documented superset |
| `GOV-10` | Use case requests conform to the use case schema, or a documented superset |
| `PLN-1` | Requests are scored with an anchored rubric |
| `PLN-6` | Requests state what is out of scope |
| `PLN-7` | Requests state measurable success criteria |
| `FEA-1` | Telemetry is confirmed present, complete and queryable before logic is written |
| `DET-1` | Each detection records a hypothesis |
| `DET-4` | Each detection declares severity, confidence and robustness tier |
| `DET-6` | Known benign causes are documented with triage guidance |
| `RSP-1` | No production detection without a linked playbook |
| `DAC-1` | Detection logic and metadata are version-controlled |
| `DEL-5` | Every detection is in a catalog generated from version-controlled metadata |
| `IMP-1` | Every improvement backlog item records the trigger that created it |
| `IMP-5` | Every exception has a justification, owner and expiry date |
| `IMP-8` | Every detection has a review cadence and last-reviewed date |
| `MET-1` | Per-detection Precision is reported over 30 days; FPR is not reported |
| `MET-5` | False negatives are reported as enumerated gaps with owners and dates |
| `TEL-1` | Each detection declares its log sources and whether each is required |

The most common L1 failure is metadata kept in the SIEM console instead of
version control. It cannot be diffed, reviewed or restored.

## Level 2: Managed

Adds to L1:

| ID | Requirement |
| --- | --- |
| `GOV-3` | Traceability is machine-readable |
| `GOV-4` | Drivers to detections, and detections to drivers, can be listed without manual research |
| `GOV-6` | A detection council operates, with detection engineering, SOC, IR, threat intelligence and business or compliance members |
| `GOV-8` | Roles are documented as a RACI covering intake, feasibility, build, review, deployment approval, tuning and deprecation |
| `GOV-11` | Metadata is version-controlled alongside the logic it describes |
| `GOV-12` | An expedited path for active threats is defined, with who may invoke it |
| `GOV-13` | A Minimum Viable Detection is defined for the expedited path |
| `GOV-14` | Expedited detections carry a review date no more than 30 days out |
| `PLN-2` | Scores are recorded in the request record |
| `PLN-3` | Confirmed active threats route to the expedited path |
| `PLN-4` | Compliance requests are scheduled against their deadline |
| `PLN-8` | No development before a feasibility assessment records telemetry availability |
| `FEA-2` | Feasibility records availability, retention, arrival interval, normalization and field gaps per source |
| `FEA-5` | Feasibility output is recorded against the request and available at approval |
| `DET-2` | Each detection records a VAL, and every implementation satisfies it |
| `DET-5` | Each detection declares an alert disposition |
| `DET-8` | Exceptions are in the logic under version control |
| `DET-9` | At least one true-positive and one true-negative fixture before production |
| `RSP-2` | The playbook contains all required sections |
| `RSP-3` | The playbook states pre-authorized containment actions |
| `RSP-6` | Playbooks are reviewed on the same cadence as their detections |
| `DAC-2` | Changes go through reviewed pull requests |
| `DAC-3` | A reviewer other than the author approves |
| `DAC-4` | Automated validation gates merge |
| `DEL-1` | Activation requires a recorded handover with the required contents |
| `DEL-2` | An alert volume forecast from historical data precedes activation |
| `DEL-4` | A rollback procedure exists that someone other than the author can run |
| `DEL-6` | The consuming team has a recorded review period before activation |
| `DEL-7` | Activation date and notification behavior are recorded |
| `IMP-2` | Alerts cannot be closed without a disposition |
| `IMP-3` | Adverse dispositions create backlog items automatically |
| `IMP-4` | Every change is classified before work begins |
| `IMP-6` | Expired exceptions are reviewed, not silently renewed |
| `IMP-11` | Reviews record a decision on all seven dimensions |
| `IMP-13` | Every change passes the existing validation suite before deployment |
| `IMP-14` | Changes deploy through the same controlled path as new detections |
| `IMP-16` | A deprecation path exists and is used |
| `IMP-18` | Decommissioning follows the recorded procedure |
| `IMP-19` | Retired detections are kept in version control permanently |
| `MET-2` | Precision below the threshold (0.50 at L2) enters the tuning backlog |
| `MET-6` | Metrics reported to leadership trace to defined formulas |
| `TEL-2` | Each required source declares an expected arrival interval |
| `TEL-3` | A log source inventory records owner, normalization, retention, interval and gaps |
| `TEL-5` | Loss of a required source raises an alert and identifies affected detections |

The most common L2 failure is leaving alert disposition optional. Without
dispositions, the feedback loop has no input.

## Level 3: Optimised

Adds to L2:

| ID | Requirement |
| --- | --- |
| `GOV-7` | The council is the decision authority for disputes, deprecation and large exceptions |
| `GOV-15` | Use of the expedited path is reported to the council |
| `PLN-5` | The backlog is re-scored at least quarterly |
| `FEA-3` | Feasibility records the cost of new telemetry |
| `FEA-4` | Telemetry for a new technique is generated by emulation before logic is written |
| `DET-3` | Multi-platform implementations trace to one VAL and share fixtures |
| `DET-7` | Ephemeral and indicator detections declare their curation process |
| `DET-10` | Every exception has a boundary fixture |
| `DET-11` | Adversary emulation validates the detection before production, and the result is recorded |
| `DET-12` | Query cost and run time are measured on production-scale data |
| `RSP-4` | Playbooks are exercised with the consuming team before handover |
| `RSP-5` | Automated response has a defined failure mode and never fails open silently |
| `DAC-5` | Fixture tests gate merge |
| `DAC-6` | Deployment to production is automated from reviewed source |
| `DAC-7` | Divergence between repository and platform is detected and reconciled |
| `DAC-8` | Rollback is a commit revert and redeploy |
| `DEL-3` | Rollout is staged, with observation criteria |
| `IMP-7` | Detections above the exception threshold go to rebuild assessment |
| `IMP-9` | Detection debt is reported monthly and kept below 15% |
| `IMP-10` | Improvement capacity is protected (20 to 30% recommended) |
| `IMP-12` | Drift is detected automatically: scheduled emulation, silence and liveness alerts, schema checks |
| `IMP-15` | Every change records version, class, author, reviewer and trigger |
| `IMP-17` | No deprecation on low fire count alone |
| `IMP-20` | Asset and platform changes trigger assessment of affected detections |
| `MET-3` | Coverage is confidence-weighted |
| `MET-4` | Detection silence and log source liveness are monitored automatically |
| `TEL-4` | Data quality is scored and reassessed at least annually |
| `TEL-6` | Telemetry cost is attributable to detections |
| `TEL-7` | Telemetry is normalized to a documented schema and logic is written against it |

At L3 the Precision threshold is 0.70. The most common L3 failure is
validation freshness: emulation is built, run once at deployment, and never
scheduled.

## Scoring and evidence

| Score | Meaning |
| --- | --- |
| `met` | Implemented, with evidence |
| `partial` | Implemented for some detections or environments only |
| `not-met` | Not implemented |
| `n/a` | Not applicable; requires a written justification approved by the council |

A requirement scored `met` needs identifiable evidence (`CNF-5`): a file, a
query result, a CI log, a ticket history. "We do that" is not evidence.

## Claims

A claim states the level, the framework version, the assessment date and the
scope, with exclusions explicit (`CNF-1`, `CNF-3`), and is reassessed at least
annually or after a material change (`CNF-4`). For example:

> Conforms to Detection Engineering Framework v2.1.1 at Level 2, assessed
> 2026-09-01, scope: corporate IT estate and Microsoft 365 tenant. Excludes
> OT networks.

"DEF compliant" is not a valid claim. Report partial progress as, for
example, "L1 conformant, L2 in progress (34 of 41 requirements met)".
