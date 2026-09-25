# The Response Engineering Phase

<!-- journey:where -->
*Walk the lifecycle › Development C: Response engineering*
<!-- /journey:where -->

This is the last of the three development stages. A detection that fires with
no agreed response creates work rather than security: the analyst who receives
the alert must decide, under time pressure, what it means and what to do. The
framework therefore treats the response as part of the detection. A detection
is not ready for production until the playbook it triggers has been written,
tested and rehearsed with the team that will use it.

> **Running example.** The consent phishing detection triggers playbook
> `PB-0003`. Two decisions in it were made in advance rather than during an
> incident: the SOC may revoke an application's access without waiting for
> approval, and access tokens must be revoked separately, because removing
> consent alone does not end the attacker's access. See
> [stage 5 of the example](worked-example.md#stage-5-response-engineering).

The sections below cover the difference between playbooks and runbooks, how
each is designed, how dashboards support investigation, how playbooks are
tested, how response is automated, and the roles involved.

SOC teams receive more alerts than they can investigate, and alerts that are
not investigated leave attacks unnoticed. Many alerts, however, follow
recurring patterns that a defined set of actions can address. Writing those
actions down in advance is what makes a high volume of alerts manageable.

The environment those actions operate in is complex. A large organization may
have overlapping private address ranges, offices in many countries, business
units running their own infrastructure, and dozens of telemetry sources, from
intrusion detection and antivirus to NetFlow, web proxies, server logs and
authentication logs, alongside threat intelligence from outside. Without
agreed procedures, each responder navigates that complexity differently.

During an active attack, the monitoring and incident response team has to
investigate accurately, make operational decisions quickly, and give senior
management the facts they need for the decisions that are theirs. Playbooks
and runbooks support that work with agreed steps, decided in calm conditions
rather than under pressure.

## Playbooks vs Runbooks

Playbooks and runbooks both support incident response, at different levels.

### Playbooks

A playbook sets out the strategy for responding to a type of incident. It
defines the stages of the response, following an established model such as
NIST's incident handling guidance, and the decisions to be made at each stage:
when to declare an incident, who to involve, what containment is authorized.
Playbooks make the response consistent across responders and across
incidents.

### Runbooks

A runbook gives the step-by-step technical procedure for a task within a
response: analyzing a particular log, isolating a host, collecting forensic
evidence, or revoking a credential. Runbooks are specific to the
organization's technologies and tools, and are usually written for tasks that
recur.

### Complementary Relationship

The playbook decides what should happen and when; the runbook describes how to
do it. A containment step in a playbook, such as isolating an affected host,
refers to the runbook that explains how to isolate a host with the
organization's endpoint tooling. Keeping the two separate means a playbook
does not need rewriting when a tool changes, and a runbook can be reused by
every playbook that needs the same task.

---

## Playbook Design

### Purpose and Structure

A playbook guides the incident response team through a type of incident from
first alert to closure. Its structure follows the stages of an established
incident handling model, so that every playbook in the organization is read
the same way.

### Playbook Components

#### Background Information

The scenario or incident type the playbook addresses, with enough context for
a responder who has not seen it before.

#### Preparation Stage

What must be in place before an incident occurs, both technical, such as
logging, access and tooling, and procedural, such as contacts, authority and
escalation paths.

#### Triggers and Detection

The detections that start the playbook, divided into high-confidence and
low-confidence triggers. The confidence of the trigger determines whether the
responder moves straight to containment or begins with investigation.

#### Investigation and Analysis

The steps for establishing whether an incident has occurred when that is not
yet clear: which data to examine, which questions to answer, and what evidence
confirms or rules out the incident.

#### Incident Declaration

The decision point at which the alert becomes an incident, and what follows:
raising an incident record in the organization's incident management system
and assigning it.

#### Containment and Mitigation

The actions that stop the incident spreading or limit its impact, and the
tools and runbooks used to take them. The playbook states which containment
actions the SOC is authorized to take without further approval. Questions of
authority left open are answered slowly, and during the incident.

#### Remediation and Recovery

The steps that repair the damage, restore affected systems and data, and
return operations to normal.

#### Post-Incident Activity

The work after the incident is closed: recording what happened, capturing
lessons learned, and identifying improvements to detections, playbooks and
controls.

---

## Runbook Design

### Purpose and Functionality

A runbook is the detailed reference for carrying out one task during incident
response. Where a playbook describes the stages and decisions, a runbook
describes the actions.

### Primary Purpose

A runbook guides a responder through a task in real time: which tool to use,
which commands to run, which data to collect and how to interpret it.
Following the same runbook, different responders carry out the task the same
way.

### Scope and Content

Each runbook addresses a specific task or incident type. It may cover
investigation procedures, containment steps, forensic collection, system
recovery or incident closure, and may include checklists, troubleshooting
guidance and scripts.

### Content Structure

The contents of runbooks vary with the organization's tools and processes.
Each runbook states its purpose, prerequisites such as access and tooling, the
steps in order, the expected result of each step, and what to do if a step
fails.

### Benefits

Under pressure, responders miss steps. A runbook that is accurate and current
reduces that risk and shortens the time a task takes. Runbooks that are out of
date do the opposite, so they are reviewed whenever the tools they describe
change.

---

## Dashboard Design

### Overview

A dashboard presents alerts and events in a form that supports the playbook:
it shows the analyst the information the investigation steps call for, in the
order they need it, with links to the underlying data for further analysis.

### Design Considerations

#### Target Audience Understanding

A dashboard is designed for the people who will use it. An analyst triaging
alerts needs different information from a SOC manager reviewing workload or an
executive reviewing risk. The roles, goals and tasks of the intended users
determine what the dashboard shows.

#### Visualization Selection

Each visualization is chosen for the question it answers. Tables suit lists of
alerts to work through; time series show trends and spikes; maps show where
activity originates. A visualization that does not answer a user's question is
removed.

#### Layout and Organization

The most important information appears first and most prominently. Related
information is grouped. A dashboard that shows everything forces the user to
find what matters; one that shows what matters lets them act.

#### Interactive Elements

Filters, drill-down and links to related records let the user move from a
summary to the detail behind it without leaving the investigation.

#### Usability and Accessibility

The dashboard is clear to a user who did not design it, labels its contents,
and works on the screens and devices it will be used on.

#### Iterative Improvement

Dashboards are refined from user feedback. Analysts who use a dashboard
during investigations are the best judges of what it is missing.

---

## Response Testing

### Playbook Testing Overview

A playbook that has not been tested is an assumption about how a response will
go. Testing runs the playbook against realistic scenarios to find gaps,
ambiguities and steps that do not work, and refines it before it is needed.

### Testing Approaches

#### Scenario-Based Testing

The playbook is followed through simulated incidents of the type it covers,
from trigger to closure. The scenarios are as close to real incidents as
possible, including the variations the playbook must handle.

#### Tabletop Exercises

The responders and the teams they depend on walk through a scenario together,
using the playbook, and discuss each decision and action. Tabletop exercises
expose unclear authority, missing contacts and steps that different teams
understand differently. A playbook is exercised this way with the consuming
team before handover; a document review does not substitute for it.

#### Integration Testing

Where the playbook depends on tools, such as the detection platform, the
ticketing system and communication channels, testing confirms that each
integration works and that automated steps carry out the intended actions.

#### Stakeholder Collaboration

Testing involves the teams the response affects: incident response, IT
operations, management and, where relevant, legal. Each checks the playbook
against its own policies, obligations and constraints.

### Output and Improvement

Each test produces a record of findings, recommendations and lessons learned.
The playbook is revised from them, and the revision is reviewed with the
people who will use it.

---

## Playbook Functional Testing

Functional testing confirms that the playbook does what it describes. Beyond
the scenario-based testing above, it covers three areas.

### Testing Components

#### Validation Testing

Given a simulated alert or event, the playbook is triggered correctly and the
responder, or the automation, takes the expected steps and reaches the
expected outcome.

#### Integration Testing

Every external system the playbook uses, such as ticketing, notification and
security tooling, receives and returns what the playbook expects.

#### Error Handling Testing

Erroneous input and unexpected conditions are introduced deliberately to
confirm that the playbook detects them, reports them clearly and recovers.

### Objectives

Functional testing establishes that the playbook can be relied on to guide a
real response: that its triggers, steps and integrations work, and that it
fails safely when they do not.

---

## Playbook Non-functional Testing

Non-functional testing assesses how the playbook performs beyond its steps.
The first measure is performance: how the playbook, and any automation behind
it, behaves under a high volume of simultaneous incidents, and where it slows
or fails.

### Security Testing

The playbook and its automation are checked for weaknesses an attacker could
exploit, such as unauthorized triggering, injection through alert fields, or
exposure of sensitive data in tickets and notifications.

### Usability Testing

Responders confirm that the playbook is clear and easy to follow. Observing
responders using it, and asking them afterwards, shows where instructions are
ambiguous.

### Reliability Testing

The playbook is run repeatedly, across different scenarios and conditions, to
confirm that it behaves consistently.

### Compatibility Testing

The playbook works with the systems, versions and configurations actually in
use, including those of other teams it depends on.

### Benefits

Non-functional testing finds the problems that appear only at scale, under
attack, or in the hands of someone other than the author, before an incident
finds them.

---

## Acceptance Testing

Acceptance testing confirms that the playbook meets the organization's
requirements and is ready for use.

### Purpose in Playbook Context

The question acceptance testing answers is whether the playbook will guide the
team through the incidents it covers: detect, investigate, contain and
recover. It is judged by the people who will use it.

### Testing Types

#### Functional Acceptance Testing

The playbook contains the steps and actions the incident type requires, and
following them in a controlled environment produces the expected outcomes.

#### Usability Acceptance Testing

The responders who will use the playbook find its instructions clear and can
follow it without confusion or error.

#### Compatibility Acceptance Testing

The playbook works with the organization's systems, tools and versions as they
are deployed.

#### Security Acceptance Testing

The playbook meets the organization's security requirements, including the
handling of sensitive information.

### Stakeholder Involvement

Representatives of the incident response team, management and the affected
business units take part. Their acceptance confirms that the playbook meets
their needs and fits the organization's incident response strategy.

---

## Response Automation

Security orchestration, automation and response (SOAR) describes technology
that collects alert data from many sources and carries out playbook steps
automatically, combining machine speed with human judgment. The capability may
be a separate platform or built into the detection platform. This section
covers when and how to automate playbook steps rather than any particular
product.

The main reason to automate is to take recurring, predictable work off
analysts: enrichment, routine response and routine remediation. That frees
time for investigation and threat hunting. Done well, automation:

- speeds up detection and response;
- gives the analyst more context at the start of an investigation;
- makes response steps consistent;
- simplifies alert and incident handling; and
- produces reliable data for reporting.

Automation is not a substitute for a response strategy. Its common failings
are:

- automating a process that was never agreed or tested manually;
- expecting automation to cover work that still needs human judgment;
- adding development and maintenance complexity that outweighs the time saved;
  and
- automation that fails without anyone noticing.

Every automated step has a defined failure mode, and automation does not fail
open silently: when a step cannot complete, the analyst is told.

### Automation Prerequisites

- **A tested manual playbook.** Automation encodes a process; it does not
  design one. The playbook is written, tested and working manually first, and
  automation is introduced step by step.
- **Suitable tools.** The automation platform integrates with the systems the
  playbook acts on and supports the actions it requires.
- **Data integration.** The data the automation needs, such as alerts,
  enrichment and threat intelligence, reaches it through reliable connectors
  or APIs in a consistent format.
- **Process readiness.** Incident response procedures, workflows and
  escalation paths are defined, so that automated steps fit into them.
- **Organizational readiness.** The team has the skills to build and maintain
  the automation, understands what it does, and reviews its performance.

### Layers of Response Automation

#### Orchestration

Orchestration connects internal and external tools through built-in or custom
integrations and APIs: vulnerability scanners, endpoint protection, user
behavior analytics, firewalls, intrusion detection and prevention, the SIEM,
and threat intelligence feeds. Orchestration brings the data together;
automation acts on it.

#### Automation

Automation takes the data orchestration provides and carries out repeatable
actions that analysts would otherwise perform by hand, such as enrichment
lookups, log queries, ticket updates and scans. Where a situation needs human
judgment, automation escalates to an analyst rather than acting.

Automated actions are grouped into playbooks, and playbooks can be chained for
complex responses. For example, when a malicious link is found in an
employee's email, an automated playbook can remove the email, notify the
employee of the phishing attempt, and block the sender. A follow-up playbook
can search other mailboxes for the same message and remove it wherever it is
found.

---

## Key Roles and Stakeholders

### Development Phase Roles

| Role | Responsibilities |
| --- | --- |
| **Content development team** | Leads and owns detection development and response development |
| **IT, system and network teams** | Make the changes and deployments the detection and response require in production |
| **Testing team** | Prepares test cases and runs them against the test plan; arranges test resources |

---

## In brief

- A detection is incomplete until the response it triggers has been designed,
  tested and rehearsed.
- Playbooks set out the strategy for a type of incident: triggers, the decision
  to declare an incident, containment, recovery and follow-up. Runbooks give the
  step-by-step technical procedures within it.
- Containment actions the SOC may take without further approval are agreed in
  advance and written into the playbook.
- Playbooks are tested functionally and non-functionally, and accepted by the
  team that will use them, before the detection goes live.
- Automation encodes a playbook that already works manually, and never fails
  silently.

## Requirements in this chapter

The requirements for this stage, `RSP-1` to `RSP-6`, are in the
[specification](specification.md#7-development-phase-c-response-engineering).

## What comes next

With the logic built and the response prepared, the detection is ready to be
handed to the team that will operate it. [The delivery phase](delivery-phase.md)
covers the handover, activation in production, and entry in the detection
catalog.

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [Going deeper: Detection as code](detection-as-code.md) · **Next:** [The delivery phase](delivery-phase.md)

</div>
<!-- /journey:next -->
