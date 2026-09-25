# The Detection Engineering Phase

<!-- journey:where -->
*Walk the lifecycle › Development B: Detection engineering*
<!-- /journey:where -->

This is the second of the three development stages. With the telemetry
confirmed, the detection logic can be designed. The framework separates what a
detection is looking for from how a particular platform expresses it. The
intent is written first as Vendor Agnostic Logic (VAL): a set of named
observable conditions, called blocks, and the relationship between them. Only
then is it implemented in a platform's query language, refined with exceptions
and enrichment, and tested.

> **Running example.** The consent phishing detection is expressed as four
> blocks: a consent operation occurred, the scopes granted permit data access,
> the person granting it is privileged, and the application is not on the
> approved list. It is implemented in both Sigma and KQL and tested against five
> samples of data it must and must not match. See
> [stage 4 of the example](worked-example.md#stage-4-detection-engineering).

The sections below cover building the VAL from observed attack blocks,
prototyping a platform rule from it, handling exceptions, enriching events with
context, the limits of rule-based logic for machine learning detections, and
the functional, emulation, non-functional and acceptance testing a detection
passes before release.

## Development Code Engineering and Testing

A detection rule sits between the threat it is meant to find and the incident
response it triggers. Every rule is therefore traceable in two directions: back
to the threat and business driver recorded in planning, and forward to the
playbook built in [response engineering](development-phase-C.md).

### Code Development

Code development starts with a hypothesis, a single statement of the form *if
an adversary does X, then Y will be observable in Z*. The hypothesis is then
expressed as Vendor Agnostic Logic.

**Vendor Agnostic Logic** is the statement of a detection's logic that does
not depend on any detection platform. It names the observable conditions the
detection relies on, and the relationship between them, in plain terms. The
platform rule is then an implementation of the VAL, and can be reviewed
against it.

Separating the two has three practical benefits:

- **Reviewability.** A reviewer can judge whether the logic is sound without
  reading a platform's query language, and can then check separately whether
  the implementation matches it.
- **Portability.** When a detection is implemented on more than one platform,
  or migrated to a new one, each implementation is written against the same
  VAL and tested against the same data.
- **Durability.** Platforms, field names and query languages change. The VAL
  records what the detection is for, so it can be rebuilt when they do.

The conditions in a VAL are the blocks recorded during
[technical feasibility](development-phase-A.md#rule-blocks-structure): each
block is one observable step of the attack, backed by the events seen during
simulation.

#### Blocks Example

The phishing scenario from technical feasibility produced four blocks,
recorded in full in the
[example blocks table](development-phase-A.md#example-blocks):

| Block | Attack step |
| --- | --- |
| Block 1 | Data transferred from the client to an external server, or malware activity on the client |
| Block 2 | The client executes code, contacts a suspicious external site, or downloads malware |
| Block 3 | A suspicious download from an external website or an email link |
| Block 4 | An email with suspicious content detected for the user |

#### VAL Development Examples

Different combinations of the same blocks produce detections with different
confidence. Four VALs built from the phishing blocks illustrate this.

**VAL 1: high confidence.** Every step of the attack is observed, from
delivery to data theft. The phishing playbook's containment actions can be
taken immediately.

```text
IF   Block 1
AND  Block 2
AND  Block 3
AND  Block 4
THEN alert "Phishing attack: data stolen from file share"
```

**VAL 2: medium confidence.** Delivery, download and malicious execution are
observed, but data theft is not. Malicious activity is under way, and the
playbook's investigation steps determine whether the attacker has reached the
data.

```text
IF   Block 2
AND  Block 3
AND  Block 4
THEN alert "Phishing attack: malware executing, no data theft observed"
```

**VAL 3: low confidence.** Data theft or malware activity is observed together
with at least one earlier step. The link between the steps is weaker, so the
alert is raised for investigation rather than immediate containment.

```text
IF   Block 1
AND  (Block 2 OR Block 3 OR Block 4)
THEN alert "Possible phishing attack: data stolen from file share"
```

**VAL 4: conditional.** Data theft and malicious execution are observed, but
not the delivery. This pattern suggests the malware arrived by a route that is
not monitored, which is itself a finding for technical feasibility.

```text
IF   Block 1
AND  Block 2
AND  NOT (Block 3 OR Block 4)
THEN alert "Possible phishing attack: data theft, delivery route not observed"
```

The VAL chosen for a detection, and its confidence, is recorded in the
detection's metadata. The platform rule is then developed from it.

### Rule Prototyping

Converting a VAL into a platform rule follows a consistent sequence:

- **Understand the VAL.** Confirm what the VAL is meant to detect, and the
  hypothesis behind it.
- **Identify the rule syntax.** Establish the query language and rule
  structure of the target platform, which differ between vendors.
- **Map the VAL to the rule language.** Decide how each block, and the
  relationship between blocks, is expressed on the platform.
- **Define conditions.** Specify the event fields, log sources, patterns and
  values each condition matches.
- **Specify operators.** Choose the logical operators (AND, OR, NOT) and
  comparison operators (equals, greater than, contains) that express the
  conditions.
- **Define actions.** Specify what happens when the rule fires: an alert, a
  notification, a script, or another action the platform supports.
- **Prototype the rule.** Write the rule, run it against the events recorded
  during simulation, and confirm it matches them.

### Exception Handling

A prototype rule usually matches some legitimate activity. Exceptions exclude
that activity so that the detection fires on what it was built for. The common
reasons for an exception are:

- **Benign activity that resembles the attack.** For example, an
  administrator's legitimate use of a tool the detection watches for.
- **Authorized activity.** Scheduled maintenance, authorized vulnerability
  scans or penetration tests, and approved automation.
- **Trusted entities.** Addresses, domains or applications the organization
  has approved.
- **Legacy systems.** Older systems that generate unusual but harmless events.
- **Compliance activity.** Processes a regulation requires, such as data
  encryption jobs or mandated scanning, that would otherwise trigger the
  detection.

Every exception is a decision not to look at something, so the framework
treats exceptions as changes to a security control:

- Exceptions are written in the detection logic under version control, not
  applied through the platform's user interface where review cannot see them.
- Each exception is tested with a fixture showing that it suppresses what it
  claims to suppress and nothing adjacent.
- Each exception records a justification, an owner and an expiry date, and is
  reviewed when it expires. The [improvement phase](improvement-phase.md)
  covers that review.

### Data Enrichment

Enrichment adds context to an event so that the analyst can act on the alert
without further searching. Typical sources are:

- **Threat intelligence:** the reputation of addresses, domains and files.
- **Vulnerability data:** whether the affected asset is exposed to a known
  weakness.
- **Asset inventory:** what the system is, who owns it and how critical it is.
- **User directories:** who the user is, their role and their privileges.

Enrichment can happen at ingestion, at detection time or at alert time, using
lookups, database queries or API calls. The enriched fields are normalized to
consistent names and formats, so that they can be queried and correlated like
any other field.

Enrichment sources need maintenance. Threat intelligence and vulnerability data
age quickly, and an asset inventory that is out of date gives the analyst
wrong context with the appearance of authority. Each enrichment source a
detection depends on has an owner and an update schedule.

### Challenges of VAL-Based Detection Rules in AI/ML

VAL works for detections whose logic can be stated as explicit conditions.
Detections based on machine learning models do not fit it as well:

- **No explicit rules.** A model's decision comes from patterns learned from
  data rather than from conditions that can be written down. The VAL can
  describe the model's inputs and the output it acts on, but not the reasoning
  in between.
- **Changing behavior.** Models are retrained, and their behavior changes when
  they are. A VAL, by contrast, only changes when someone edits it. Each
  retraining is therefore a change to the detection and is reviewed as one.
- **Error rates.** Rule-based detections and models both produce false
  positives and false negatives. A model's error rates depend on its training
  data and on how the environment drifts from it, so they need to be measured
  continuously rather than assumed.
- **Scale.** Large rule sets become hard to manage, and models can process
  large volumes of data efficiently. Models bring their own operating costs,
  however: training data, retraining, and monitoring for drift.

Machine learning detections are held to the same lifecycle as any other
detection. They record a hypothesis, the data they depend on and their
disposition. They are tested against true-positive and true-negative data, and
their precision is measured in production.

### Rule Deployment

Before a rule is deployed, it passes four kinds of testing, in order:
functional testing, attack emulation, non-functional testing and acceptance
testing. A failure at any stage returns the rule to development. The test cases
cover the detection from start to finish, one transaction at a time.

### Functional Testing

Functional testing confirms that the rule does what its VAL says. It covers:

- **Rule execution.** The rule fires when its conditions are met, and only
  then.
- **Event correlation.** Where the rule correlates several events, it links the
  right events and ignores unrelated ones.
- **Alert generation.** The alert carries the right severity, the fields the
  analyst needs, and a clear description.
- **True-positive and true-negative fixtures.** The rule matches every sample of
  malicious activity it must detect, and none of the samples of legitimate
  activity it must ignore. Every exception has a fixture proving its boundary.
- **Performance.** The rule completes within an acceptable time and does not
  consume excessive platform resources.
- **Maintainability.** The rule can be changed, for example by adjusting a
  threshold or adding a data source, without breaking its tests.

### Attack Emulation

Fixtures prove the rule against recorded data. Attack emulation proves it
against live activity in the real environment. The attack is carried out
again, preferably with variations the original simulation did not include,
and the rule is observed. Emulation often exposes gaps: a variant technique
that evades the logic, a field populated differently than expected, or a
response action that does not work.

The result is recorded with the detection. Where emulation is not technically
possible, the reason is recorded instead, and the detection is marked as
unvalidated in coverage reporting.

#### Attack Simulation Methods

- **Traffic generation.** Tools that generate network traffic can reproduce
  port scans, brute-force logins, data exfiltration and denial of service
  patterns.
- **Honeypots and canary tokens.** Decoy systems, files and credentials that
  raise an alert when touched test detections for unauthorized access.
- **Malware sandbox execution.** Running samples in a controlled environment
  shows the network, process and file activity they generate.
- **Phishing campaigns.** Simulated phishing emails test detections for
  delivery, link clicks and attachment execution.
- **Endpoint behavior simulation.** Tools that perform attacker actions on an
  endpoint, such as suspicious execution, privilege escalation and lateral
  movement, in a controlled way.
- **Attack traffic replay.** Replaying captured attack traffic or packet
  captures tests the rule against the patterns of a real attack.

### Non-functional Testing

Non-functional testing confirms that the rule can run in production without
harming the platform or the service. The most important measures are query
cost and execution time against production-scale data, which must be
established before deployment. Other measures depend on the detection:

- **Performance.** Response time and resource use under normal and peak load.
- **Scalability.** Behavior as data volumes grow, and where the limits are.
- **Reliability.** Behavior when the platform or a data source is interrupted
  or restarted, including whether events are lost.
- **Evasion resistance.** How the rule copes with evasion techniques and
  malformed input. [Detection robustness](detection-robustness.md) describes
  how to assess this.
- **Usability.** Whether analysts and administrators can understand and
  configure the rule.
- **Compliance.** Whether the rule captures and reports what regulatory and
  policy obligations require.
- **Recovery.** Whether the rule resumes correctly after a platform failure.

### Acceptance Testing

Acceptance testing confirms that the detection meets the requirements agreed in
planning and is acceptable to the people who will use it. The SOC analysts who
will triage its alerts, and the stakeholders who requested it, review it
against the success criteria in the use case request.

A test plan sets out the scenarios, acceptance criteria and expected outcomes.
The scenarios are run in the detection platform, and any defects or deviations
are logged and returned to the engineer. When the detection meets its criteria,
it is approved for the [delivery phase](delivery-phase.md).

---

## In brief

- Detection intent is recorded as Vendor Agnostic Logic before it is written in
  any platform's query language. Every implementation must satisfy the same VAL.
- Exceptions refine a detection for known benign activity. They are expressed
  in the logic under version control, never applied quietly in a console.
- Enrichment adds the context an analyst needs to act without further
  searching.
- Before release a detection is tested against data it must match and data it
  must not match, against emulated attacks, and for its performance at
  production scale.

## Requirements in this chapter

The requirements for this stage, `DET-1` to `DET-12`, are in the
[specification](specification.md#6-development-phase-b-detection-engineering).
They cover the hypothesis and VAL, quality attributes, exceptions and testing.

## What comes next

Two deep dives expand on this stage.
[Detection robustness](detection-robustness.md) explains how to judge how hard
a detection is for an attacker to evade, and
[detection as code](detection-as-code.md) explains how detections are
version-controlled, reviewed, tested and deployed automatically. Readers
following the core path can continue to
[the response engineering phase](development-phase-C.md), which builds what
happens once a detection fires.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [Going deeper: Modern attack surfaces](modern-attack-surfaces.md) · **Next:** [Going deeper: Detection robustness](detection-robustness.md)

</div>
<!-- /journey:next -->
