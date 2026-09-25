# The Technical Feasibility Phase

<!-- journey:where -->
*Walk the lifecycle › Development A: Technical feasibility*
<!-- /journey:where -->

Development is the longest phase of the lifecycle and has three stages.
Technical feasibility, covered here, comes first. It establishes whether the
organization can observe the activity a detection is meant to find: which
assets are involved, what telemetry they produce, whether that telemetry reaches
the detection platform, and what it looks like when the attack actually takes
place. The detection engineering stage then designs and tests the logic, and
the response engineering stage builds what happens when the detection fires.

Skipping feasibility is the most common reason a detection passes review and
then fails in production. Logic written against assumed field names or assumed
log coverage cannot be tested until it is already live.

> **Running example.** Feasibility for the consent phishing detection
> confirmed that the identity provider's audit logs were already collected and
> contained the consent events. It also found a gap: whether an application's
> publisher is verified is not recorded in those logs and requires a separate
> lookup. The council accepted delivery with that context missing, and tracked
> the lookup as separate work. See
> [stage 3 of the example](worked-example.md#stage-3-technical-feasibility).

The sections below cover the structure of the development phase, technical
analysis of the threat, attack simulation to observe real telemetry, and the
preparation of data sources: identifying, configuring, shipping, onboarding,
validating and parsing them.

## Development Phase Structure

The three development stages answer three different questions:

| Stage | Question | Chapter |
| --- | --- | --- |
| Technical feasibility | Can the activity be observed with the telemetry available? | This chapter |
| Detection engineering | What logic finds the activity reliably, and how is it proven? | [Detection engineering](development-phase-B.md) |
| Response engineering | What happens when the detection fires? | [Response engineering](development-phase-C.md) |

Each stage depends on the one before it. Logic cannot be designed until the
fields it relies on are known to exist, and a response cannot be designed until
the alert it responds to is defined.

The aim across all three is an alert that analysts can trust. A detection that
fires on legitimate activity consumes analyst time and teaches the team to
ignore it, so every stage contributes to precision: feasibility by confirming
the right evidence exists, engineering by testing the logic against it, and
response engineering by giving the analyst what they need to decide quickly.

---

## Technical Feasibility Analysis

The contextual feasibility analysis in planning established why a detection is
needed and who has a stake in it. The technical feasibility analysis
establishes what the engineer needs to know to build it:

- the assets involved and their technical attributes, such as address,
  location, hardware, operating system, applications and the security controls
  in front of them;
- the telemetry those assets generate, and the telemetry they do not;
- where that telemetry is stored; and
- whether it reaches the detection platform in a usable form.

### Technical Analysis

Technical analysis describes the threat the detection must find. It draws on
threat modeling to assess the organization's exposure and answers five
questions:

- **Taxonomy of the threat.** What capability, intent and opportunity does the
  adversary have?
- **Likelihood.** How probable is the attack, based on threat intelligence,
  past incidents and current activity in the sector?
- **Threat agents.** Who would carry it out?
- **Attack surface.** Which systems, identities and applications are exposed?
- **Threat vectors.** By which routes would the attack arrive and progress?

Answering these questions involves examining assets, vulnerabilities, attack
trees, indicators of compromise and of attack, and the anatomy of known
attacks. The work is often done by, or with, a red team or penetration testing
team, who can describe how an adversary would move through the organization's
systems and which existing controls they would expect to bypass.

The output is a set of attack scenarios fitted to the organization's
environment. Each scenario describes how an attack would unfold, from initial
compromise through lateral movement to the objective, and which systems would
be involved at each step. Those scenarios are what attack simulation then
exercises.

### Attack Simulation

Documentation describes what telemetry an attack should produce. Simulation
shows what it actually produces in the organization's environment. The two
often differ: a field is named differently, an event is not logged at the
configured audit level, or a control blocks the activity before the log source
that was expected to record it.

In an attack simulation, red team or penetration testing staff carry out the
attack scenario while the detection engineers and SOC analysts observe. The
goal is to record which assets, data sources, events and fields the attack
generates, so that the detection is built against evidence. Without
simulation, the engineer is either guessing at the telemetry or trusting
documentation that may not match the deployment.

Because environments change, simulation is not a one-time exercise. Repeating
it confirms that the telemetry a detection depends on is still produced after
infrastructure, configuration or vendor changes. Breach and attack simulation
(BAS) platforms automate this by running known adversary techniques on a
schedule and reporting which ones were observed and detected. The
[improvement phase](improvement-phase.md) uses the same approach for
continuous validation.

#### Example Attack Scenario

> **Phishing attack scenario.** A senior executive using a company-managed
> laptop receives a phishing email carrying a malicious file. Opening the file
> installs a trojan, which connects to a command and control server. The
> attacker then uses the compromised laptop to copy data from the user's
> documents folder to an external server.

The attack is carried out one step at a time. After each step, the monitoring
team records which systems generated events and what those events contained.
That record is the input to rule development in the next stage, and gives the
analyst the context needed to investigate, escalate and remediate when the
detection later fires.

### Identifying the Data Sources

Identifying data sources depends on close communication between the people
carrying out the attack and the people observing it. A shared architecture
diagram helps both sides agree which assets are involved.

To find the events produced by each step, the monitoring team searches the
relevant time window for known evidence such as source and destination
addresses, host names, and strings clearly associated with the attack.

Each observed event is given a unique message ID. The events from all sources
that relate to one attack step form a **block**, and the blocks together are
the basis for the correlation rule built in the next stage.

#### Rule Blocks Structure

Every block describes one step of the attack and records five things:

- **Description.** What happened in this step.
- **Correlation terms.** The values that link events from different sources to
  the same attack, such as host name, address or user.
- **Strings in events.** Distinctive strings that identify the step in the log
  messages, for use in the vendor-agnostic logic.
- **Observed message IDs.** The IDs assigned to the events recorded during
  simulation.
- **Possible sources.** The log sources that could provide evidence of the
  step, including any not yet collected.

#### Example Blocks

The blocks below record the phishing scenario. They are numbered from the
attacker's objective back to the initial delivery; the message IDs run in the
order in which the attack took place.

| Block | Details |
| --- | --- |
| **Block 1** | **If** the client (user `siemtest2`) transfers files to an external server **or** shows any malware activity<br/><br/>**Correlation terms:** user email address, destination email address<br/><br/>**Strings in events:** `MAIL FROM:<siemtest2@example.com>`, `Quarantined duser=superuser@example.net`<br/><br/>**Observed message IDs:** SC1-017 to SC1-019<br/><br/>**Possible sources:** Windows event logs, antivirus, host intrusion prevention, host firewall, server logs |
| **Block 2** | **If** the client (user `siemtest2`) executes code, connects to a suspicious external site or downloads malware<br/><br/>**Correlation terms:** host address, host name, command server address<br/><br/>**Strings in events:** `Suspicious PowerShell`, `System infected`, `Trojan`, `PERMITTED_BY_POLICY_EXCEPTION`<br/><br/>**Observed message IDs:** SC1-010 to SC1-016<br/><br/>**Possible sources:** NetFlow, proxy, intrusion prevention, DNS firewall, host intrusion prevention, advanced threat protection |
| **Block 3** | **Check whether** a suspicious download arrived from an external website **or** an email link<br/><br/>**Correlation terms:** host address, host name, external server address<br/><br/>**Strings in events:** `INDICATOR-COMPROMISE potential Squiblydoo application whitelisting bypass attempt`, `SECURITY_OVERRIDE_BLOCKED_REAL_TIME - Potentially Unwanted Software`, `SymantecServer: Virus found`, `Web Attack: Malicious File Download attack blocked.`, `Malicious Executable`<br/><br/>**Observed message IDs:** SC1-004 to SC1-008<br/><br/>**Possible sources:** NetFlow, proxy, intrusion prevention, antimalware, host intrusion prevention, advanced threat protection |
| **Block 4** | **Check whether** an email with suspicious content was detected for the user<br/><br/>**Correlation terms:** host address, host name, external server address<br/><br/>**Strings in events:** `External Spam/Phishing Mailserver`<br/><br/>**Observed message IDs:** SC1-001 to SC1-003<br/><br/>**Possible sources:** access firewall, mail server, DNS firewall |

### Identify if Attack Indicators are Fully Available

Simulation often shows that some evidence the detection needs is missing. The
simplest case is a log source that exists but is not collected or forwarded to
the detection platform. The harder case is architectural: the information is
not visible at any point where a security control inspects traffic or
activity. Each missing indicator is recorded, with its effect on the
detection's accuracy, before development continues.

### Change Architecture or Onboard Needed Information

Where the architecture prevents the evidence from being captured, the options
are to change the architecture or to onboard another source that provides
equivalent information. Both are assessed for technical and operational cost.
Where neither is feasible, the resulting detection gap is accepted as a risk
with a named owner rather than left undocumented.

### Check if All Needed Data is Available

Any log data the detection needs, either to see a step of the attack or to
distinguish it from legitimate activity, must be onboarded to the detection
platform before development continues. The steps below cover that onboarding.

### Configuring the Data Sources

Each source is configured to produce the required events and send them to the
designated collectors and forwarders. This includes the audit level, the
transport protocol, authentication between source and collector, and reliable
connectivity.

### Shipping Data to Collectors and Forwarders

Data is transported from the sources to central collectors and forwarders over
protocols that protect its confidentiality and integrity. Delivery needs to be
timely enough for the detection's purpose; a detection intended to fire within
minutes cannot rely on a source that is batched hourly.

### Onboarding and Data Validation

Once data reaches the collectors, it is onboarded to the detection platform
and validated. Validation confirms that the data is complete, accurate and in
the expected format, and that the events observed during simulation are
present. Problems found here are much cheaper to fix than problems found after
the detection is live.

### Data Parsing

Each log source has its own format, and formats vary even between logs on the
same system. A parser converts a specific format into structured fields, using
parsing rules, regular expressions or scripts. Where the platform does not
already parse a source, a parser is written and tested. Parsed, normalized
fields are what allow events from different sources to be correlated, and what
the detection logic in the next stage is written against.

### Readiness for Detection Engineering

When the required data sources are identified, configured, onboarded, validated
and parsed, the prerequisites for writing detection logic are in place.

---

## In brief

- Feasibility confirms that the activity a detection targets can actually be
  observed, before any logic is written.
- Technical analysis examines the threat's capability, intent and opportunity,
  its likely vectors, and the assets it would reach.
- Attack simulation generates the real telemetry the attack produces, so the
  detection is built against evidence rather than assumption.
- Each required data source is confirmed as configured, delivered, validated
  and parsed into usable fields.

## Requirements in this chapter

The requirements for this stage, `FEA-1` to `FEA-5`, are in the
[specification](specification.md#5-development-phase-a-technical-feasibility).
They cover confirming telemetry before development, recording its properties
and cost, and making the findings available at detection approval.

## What comes next

Two deep dives expand on this stage.
[Telemetry and data](telemetry-and-data.md) describes how to assess data
quality and the cost of collection, and
[modern attack surfaces](modern-attack-surfaces.md) describes how feasibility
changes for identity, cloud, SaaS and other environments where the endpoint is
not the point of compromise. Readers following the core path can continue to
[the detection engineering phase](development-phase-B.md), where the telemetry
confirmed here is turned into detection logic.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [Going deeper: Governance and roles](governance-and-roles.md) · **Next:** [Going deeper: Telemetry and data](telemetry-and-data.md)

</div>
<!-- /journey:next -->
