# The Delivery Phase

<!-- journey:where -->
*Walk the lifecycle › Delivery*
<!-- /journey:where -->

Delivery moves a detection from the engineering team that built it to the
security monitoring team that will operate it. It is the point at which a
detection starts producing work for other people, so it is also the point at
which poor preparation becomes visible: an unforecast flood of alerts, an alert
that lacks the context to act on, or a rule that quietly overloads the
platform.

> **Running example.** Before activation, the consent phishing detection was run
> against 90 days of historical data, which forecast fewer than one alert a day.
> It was enabled for one business unit for two weeks before the whole
> organization. During the SOC's review period, analysts asked for the granted
> permissions to appear in the alert itself, and the change was made before
> activation. See [stage 6 of the example](worked-example.md#stage-6-delivery).

The sections below cover the handover to the SOC, activating the rule and
monitoring its early behavior, the metrics reported from the start, and
cataloging the detection. Response automation, which is built before delivery,
is covered in [response engineering](development-phase-C.md).

## SOC Handover

Handover is the transition of a detection from the people who built it to the
people who will run it, mainly the security monitoring team. It begins when
development is complete or nearly complete. A good handover lets the
monitoring team operate, maintain and support the detection for the rest of
its life without needing to go back to its author.

The development team is responsible for the completeness of what it hands
over.

### Handover Checklist

- **The documentation pack**, containing everything recorded in planning and
  development, and in improvement if the detection is being revised.
- **The technical analysis** carried out before development.
- **The exceptions** applied during development, with their justifications.
- **The VAL and the platform rule or code** developed from it.
- **The validation results** for the detection's tests and the playbook's
  tests.
- **Confirmation of stakeholder approvals**, technical and non-technical.
- **An alert volume forecast**, produced by running the logic against
  historical data.
- **A joint walkthrough and tabletop exercise** of the response playbook with
  the monitoring team.
- **A proposed quality rating** for the detection.
- **The catalog entry** for the detection and its rules.
- **A review period** in which the monitoring team can consider the detection
  and raise objections, recorded with its dates.
- **An agreed activation date and time**, and the agreed notification
  behavior.

## Rule Activation

Once tested in preproduction, the rule is moved to the production platform and
activated with its agreed notification type, such as an analyst alert or a
watchlist entry. Activation is staged: the rule is enabled for a limited scope
first, with defined criteria for what counts as acceptable behavior, before it
is enabled everywhere. A rollback procedure is defined that someone other than
the author can carry out.

### Monitoring Rule Behavior

Thorough testing in development keeps early surprises to a minimum, but the
production environment differs from any test: its assets, their
configuration and the threats against them change continually. For the first
period after activation, the rule is watched for:

- more alerts than the team can handle;
- alerts without enough information to begin an investigation;
- degraded platform performance;
- data sources that have stopped sending the telemetry the rule depends on;
  and
- any other unexpected effect on the platform or the service.

### Monitoring Metrics

#### Number of Alerts

The number of alerts each detection produces is reported per detection, as an
absolute count. It shows which detections fire often and which rarely, and,
combined with precision, feeds the threat management process. Not every alert
becomes an incident, so the number of incidents is reported per detection as
well.

#### Detection Precision

Precision indicates the quality of a detection as experienced by the analysts
who consume it. It answers the only question that drives a tuning decision: of
the alerts this detection produced, what proportion were worth an analyst's
time?

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

Where:

- $TP$ = **True Positives**: alerts dispositioned by an analyst as genuine.
- $FP$ = **False Positives**: alerts dispositioned as benign or erroneous.

Both terms are read directly from case management data. Nothing is estimated.

> **Do not report the classical false positive rate.** $FPR = FP / (FP + TN)$
> requires a count of true negatives, which is unmeasurable and unbounded in an
> event stream. Reporting it produces a flatteringly small number that is
> unrelated to analyst experience. The full argument, worked examples, action
> thresholds and the complete required metric set are defined in
> [Detection Metrics](detection-metrics.md).

Alert volume and the alert-to-incident ratio remain valid program-level
measures and are defined alongside Precision in that chapter.

#### Number of False-negatives

A false negative is an attack that took place within the scope of a detection
and was not detected. Where precision describes the cost of a detection's
alerts, false negatives describe the cost of its silence: an attacker who is
not seen keeps their access.

A false negative has one of three causes: the detection is tuned or configured
incorrectly, the attacker used a variant the logic does not cover, or no
detection exists because the attack vector was not foreseen or not yet built.
Each identified false negative shows a specific gap in coverage, and is
evidence for the improvement phase and for the next round of planning.

False negatives MUST be reported as an enumerated list of identified detection
gaps, each with an owner and a remediation date, and MUST NOT be reported as a
bare count. A count implies the total is known; by definition it is not. The
three legitimate sources of false-negative evidence are adversary emulation
results, incident retrospectives and purple team exercises. See
[Detection Metrics](detection-metrics.md) for the full treatment.

## Use Case Cataloging

A catalog records which detections the organization has, what each is for,
where it runs and how important it is. Without one, the SOC faces predictable
problems:

- no clear view of what is and is not visible or detected;
- duplicate copies of the same detection;
- detections interpreted differently by different people;
- no record of why a detection exists; and
- no auditable history of changes.

The catalog is generated from the version-controlled detection metadata
rather than maintained separately, so that it cannot drift from what is
deployed.

The framework borrows from descriptive cataloging in libraries, which records
the identifying traits of each item so that users can find it, rather than
trying to describe it perfectly. Catalog entries are ordered by a key, such as
detection ID, category or creation date. Any single ordering serves some
purposes better than others, so each entry also carries enough descriptive
fields to be found by other routes: by threat, by asset type, by data source
or by ATT&CK technique.

A catalog serves two purposes: it shows each type of user, such as analyst,
engineer or auditor, which detections are relevant to them, and it lets them
navigate the detections in the way that suits their work.

### Catalog Fields

The following fields identify a use case, its rules and their attributes:

| Field Name | Field Description |
| --- | --- |
| **Use Case ID#** | A serial number that uniquely identifies the use case |
| **Use Case Name** | A short descriptive name for the use case |
| **Use Case Description** | A brief description of the use case |
| **Use Case Requestor Name** | The person who requested the use case |
| **Use Case Date of Creation** | The date the use case was first recorded |
| **Use Case Date of Revision** | The date the use case was last modified |
| **Use Case Date of Decommission** | The date the use case was decommissioned |
| **Rule ID#** | A serial number that uniquely identifies the rule |
| **Rule Onboarding Status** | The rule's stage in the development process |
| **Rule Name** | A short descriptive name for the rule |
| **Rule Description** | A brief description of the rule |
| **Rule Creator Name** | The person who created the rule |
| **Rule Modifier Name** | The person who last modified the rule |
| **Rule Date of Creation** | The date the rule was first created |
| **Rule Date of Revision** | The date the rule was last modified |
| **Rule Date of Decommissioning** | The date the rule was decommissioned |
| **Rule Required Log Sources** | The telemetry the rule needs to work |
| **Rule Actions** | What the rule does when it matches. Some rules generate alerts, some provide building blocks for more complex detections, and others feed reports |
| **Rule Priority** | The initial priority of alerts the rule generates |
| **Rule VAL** | The detection logic, including event matches and suggested thresholds |
| **Rule Exceptions** | Known benign activity that matches the rule and is excluded |
| **Rule Quality Rating** | The rule's maturity rating, described below |
| **Rule Release benchmark** | The rule's release stage, described below |
| **Rule Alert Status** | Whether the rule's alerting is enabled or disabled |
| **Rule associated playbooks** | The playbooks the rule triggers |
| **Rule ATT&CK Tactic mapping** | The related MITRE ATT&CK tactic |
| **Rule ATT&CK Technique mapping** | The related MITRE ATT&CK technique |
| **Rule ATT&CK Sub-Technique mapping** | The related MITRE ATT&CK sub-technique |
| **SOC Manager Approval** | Approval by the SOC manager |
| **Stakeholder Requestor Approval** | Approval by the requesting stakeholder |
| **Notes and Comments** | Special considerations, such as required audit configuration, high event volume, or a recommended implementation approach |

### Category and Naming Convention

A consistent naming convention makes detections easy to find, compare and
manage. The suggested convention combines four elements: a sequence number, a
use case category, an ATT&CK tactic and the infrastructure the rule runs on.
Each column below lists example values for one element; the columns are
independent of each other.

| **No.** | **Use case category** | **ATT&CK Tactic** | **Infrastructure** |
|:-------:|:---------------------:|:-----------------:|:------------------:|
| 0001 | Self-Monitoring | Reconnaissance | Windows |
| 0002 | Access Control | Resource Development | Linux |
| 0003 | Application | Initial Access | AWS |
| 0004 | Host | Execution | Azure |
| **...** | Mobile | Persistence | Firewall |
| | Wireless Network | Privilege Escalation | IDS/IPS |
| | Internal Network | Defense Evasion | SIEM |
| | Cloud | Credential Access | 2FA System |
| | Perimeter | Discovery | Web application |
| | Physical | Lateral Movement | MySQL Database |
| | Policy | Collection | Proxy |
| | | Command and Control | Door Card Reader |
| | | Exfiltration | Printer |
| | | Impact | Point of Sale |
| | | | Elevator PLC |
| | | | Water Meter |
| | | | SMART HVAC |
| | | | **...** |

#### Naming Format

**Use case name:**

```text
<USE CASE NAME>
```

**Rule name:**

```text
<####>-<USE CASE CATEGORY>-<ATT&CK TACTIC>-<USE CASE NAME> On <INFRASTRUCTURE>
```

**Example:**

**Use case name:**

```text
Unauthorized Software Deployment
```

**Rule name:**

```text
0021-Host-Execution-Unauthorized Software Deployment On Windows
```

### Rule Quality Rating

The quality rating tells stakeholders, engineers and analysts at a glance how
mature a detection is. Each level includes everything in the level below it.

| **Rating** | **Description** | **Quality** | **Risk** |
|:----------:|----------------|-------------|----------|
| **0** | Use case or rule disabled | - | - |
| **1** | Active but untested; many false positives or no detections; no mapped business case, response playbook or automation | Lowest | Highest |
| **2** | As rating 1, with some exclusions and filtering to reduce false positives; logic still needs optimization; still no business case, playbook or automation | Low | High |
| **3** | As rating 2, with a recorded business case, a specific response playbook and, where used, working automation | Medium | Medium |
| **4** | As rating 3, with metrics measured continuously | High | Low |
| **5** | As rating 4, with metrics used to drive business decisions | Highest | Lowest |

### Release Benchmark

The release benchmark records how far a use case has progressed, from an idea
arising from a risk, threat or compliance driver to a detection running in
production, and eventually to its retirement. Recording the stage in the
catalog shows stakeholders, engineers and analysts where each use case stands.

The table shows which elements are complete at each stage: the plan, the
detection code, testing of the code, the response playbook, and testing of the
response.

| Stage | Plan | Code | Code tested | Response | Response tested |
| --- | --- | --- | --- | --- | --- |
| **Concept** | | | | | |
| **Pre-Alpha** | Yes | | | | |
| **Alpha** | Yes | Yes | | | |
| **Beta** | Yes | Yes | Yes | | |
| **Release Candidate** | Yes | Yes | Yes | Yes | |
| **Release to Production** | Yes | Yes | Yes | Yes | Yes |
| **Maintenance** | Yes | Yes | Yes | Yes | Yes |
| **Decommissioned** | | | | | |

#### Concept

The use case is an idea that has arisen from a risk, threat or compliance
driver, but has not been documented. Concepts do not need to be cataloged, but
naming the stage helps distinguish an informal discussion from a formal
request.

#### Pre-Alpha

The request has been submitted, validated and added to the technical
feasibility backlog. Its objective, drivers, scope, purpose, value, priority,
stakeholders, alignment, outputs and resourcing have all been established.

#### Alpha

A prototype rule exists but has not been through functional or non-functional
testing. Its behavior may be poor: too many alerts, none at all, or excessive
load on the platform. It may rely on a generic playbook or none. Alpha rules
belong in preproduction, where they cannot disrupt the SOC's platform or its
analysts.

#### Beta

The rule has passed functional and non-functional testing and behaves as
intended. It still lacks a specific, approved response playbook, relying on a
generic one if any.

#### Release Candidate (RC)

The rule and its specific, approved playbook are ready for release. The
playbook has not yet been exercised with the SOC analysts or the wider teams
it involves. Analysts can generally handle alerts at this stage, but teams
outside the SOC may be unprepared for the requests the playbook makes of them.

#### Release to Production (RTP)

The plan, code and response have all been developed and tested. Every use case
aims to reach this stage.

#### Maintenance

The code or response is being changed, whether to correct a defect or to
improve the quality of its alerts.

#### Decommissioned

The use case is no longer required and has been retired. Its record is kept, so
that past security cases that relied on it remain traceable.

### Mapping to Mitre ATT&CK

Seen from the attacker's side, each use case describes an attack scenario: the
outcome an attacker is trying to achieve, such as access to a particular asset.
That outcome is mapped to the tactics, techniques and sub-techniques of MITRE
ATT&CK.

Alongside the ATT&CK mapping, each use case records the context of the attack:
its likely source, its place in the kill chain, the log sources that observe
it, its risk level, a short explanation of the threat, and the playbook that
responds to it.

Once the organization's use cases are mapped to ATT&CK, the gaps in coverage
become visible, and the development of new use cases can be prioritized
against them. The [coverage gap dimension](planning-phase.md#dimension-3-coverage-gap-g-1-5)
of the planning rubric draws on this view.

MITRE ATT&CK is a continually updated knowledge base of adversary tactics,
techniques and procedures, drawn from observed attacks. A tactic is the
adversary's goal, such as credential access; a technique is a way of achieving
it. For each technique, ATT&CK provides:

- a unique identifier of the form `T####`, such as `T1037` for boot or logon
  initialization scripts, with sub-techniques identified as `T####.###`;
- the tactic or tactics it serves (a technique can serve more than one);
- the platforms it applies to;
- the permissions or system requirements the attacker needs;
- the defenses it bypasses;
- the data sources that can observe it; and
- mitigations and detection approaches.

Extracting the data sources for the techniques that matter to the
organization shows which telemetry is missing, and gives a measurable view of
the organization's ability to detect those techniques.

ATT&CK is published as several matrices. The ones relevant depend on the
organization:

- **Enterprise.** The most widely used matrix, covering Windows, macOS and
  Linux; cloud platforms such as AWS, Azure and Google Cloud; SaaS and
  identity services; network devices; and containers. It includes the
  Reconnaissance and Resource Development tactics, which describe an
  attacker's preparation before an intrusion and were previously published
  separately as PRE-ATT&CK.
- **Mobile.** Techniques against Android and iOS devices, including those
  that do not require access to the device.
- **ICS.** Techniques used against industrial control systems.

---

## In brief

- Handover gives the operating team everything captured during planning and
  development, time to review it, and an agreed activation date.
- An alert volume forecast, produced from historical data, comes before
  activation, and rollout is staged.
- From activation, each detection reports alert volume and Precision, the share
  of its alerts that analysts confirm as genuine.
- Every detection enters a catalog generated from its version-controlled
  record, with a consistent name and category and an ATT&CK mapping.

## Requirements in this chapter

The requirements for this phase, `DEL-1` to `DEL-7`, are in the
[specification](specification.md#9-delivery-phase).

## What comes next

Once a detection is live, the work shifts from building to maintaining.
[The improvement phase](improvement-phase.md) describes how feedback, scheduled
review and automated checks keep a detection accurate, and how it is retired
when it no longer earns its place.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [The response engineering phase](development-phase-C.md) · **Next:** [The improvement phase](improvement-phase.md)

</div>
<!-- /journey:next -->
