# Response Playbook

A production detection links to a playbook (`RSP-1`). A playbook sets out the
strategy for one type of incident; runbooks give the step-by-step technical
procedures it calls on.

## Requirements

| ID | Requirement |
| --- | --- |
| `RSP-1` | No `production` status without a linked playbook |
| `RSP-2` | The playbook states, at minimum: preparation prerequisites, triggers by confidence, investigation steps, the incident declaration decision point, containment actions, recovery steps, and post-incident activity |
| `RSP-3` | The playbook states which containment actions the SOC may take without further approval |
| `RSP-4` | The playbook is exercised with the consuming team before handover; a tabletop walkthrough counts, a document review does not |
| `RSP-5` | Automated response has a defined failure mode and never fails open silently |
| `RSP-6` | Playbooks are reviewed on the same cadence as the detections that trigger them |

## Template

```markdown
# PB-<NNNN>: <Incident type>

| Field | Value |
| --- | --- |
| Playbook ID | PB-<NNNN> |
| Version | <x.y.z> |
| Owner | <Team> |
| Triggering detections | DET-<YYYY>-<NNNN> |
| Severity | <Default severity> |
| Triage SLA | <Minutes> |
| Last exercised | <Date and type, e.g. tabletop with the owning team> |

## Background

<What the attack is, why it matters, and what ends the attacker's access. One
paragraph a responder new to this incident type can act on.>

## Preparation

| Requirement | Owner | Verified |
| --- | --- | --- |
| <Access, logging, tooling or watchlist the steps depend on> | <Team> | <Cadence> |

## Triggers and detection

| Confidence | Trigger |
| --- | --- |
| High | <Detection fires and a condition that makes it near-certain> |
| Low | <Detection fires with weaker supporting evidence> |

## Investigation and analysis

1. **<Step name>.** <What to check, where, and what the result means.>
2. ...

**Decision point.** Declare an incident if any of the following are true:
<explicit, testable conditions>.

## Incident declaration

<Ticket type, default and escalated severity, who is notified.>

## Containment and mitigation

Pre-authorized for the SOC without further approval: <list, or "none">.
Requires approval from <role>: <list>.

1. **<Action>.** <How, with runbook reference RB-<NNNN>.>
2. **Preserve evidence** before any deletion: <which logs and artifacts>.

## Remediation and recovery

- <Steps that remove persistence, restore service and close the control gap.>

## Post-incident activity

- <Indicators to record, lessons learned, detection improvement triggers,
  and updates to this playbook.>

## Analyst feedback

Record the detection disposition before closing. Choose
`insufficient-context` if the alert could not be triaged without pivoting.
```

## Guidance

- **Split triggers by confidence.** High-confidence triggers go to
  containment quickly; low-confidence triggers start with investigation.
- **Make the decision point testable.** "If suspicious" is not a decision
  point. "If the application has no change record, or application-level
  permissions were granted" is.
- **Settle authority in advance.** Questions of who may act are answered
  slowly, and during the incident. Record them in the playbook.
- **Order containment deliberately.** State which actions are reversible,
  and preserve evidence before anything destructive. Disable before deleting.
- **Automation encodes a working manual process.** Automate a step only after
  it has worked by hand. For each automated step, state what happens if it
  fails, and make sure an analyst is told.
- **Close the loop.** Post-incident activity names the improvement trigger
  for the detection if it fired late, fired without enough context, or missed
  part of the attack.
