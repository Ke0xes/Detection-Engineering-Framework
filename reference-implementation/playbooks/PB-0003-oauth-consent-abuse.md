# PB-0003 — OAuth Consent Abuse

| Field | Value |
| --- | --- |
| Playbook ID | PB-0003 |
| Version | 1.1.0 |
| Owner | CSIRT |
| Triggering detections | DET-2026-0001 |
| Severity | High |
| Triage SLA | 30 minutes |
| Last exercised | 2026-08-27 (tabletop with Identity Services) |

## Background

An adversary who obtains OAuth consent does not need the user's password again.
Delegated access survives password reset, MFA re-enrollment and session
revocation. Token revocation and application removal are the only controls that
end the access. Treat every fire as potential active compromise until the
application is positively identified.

## Preparation

Before this playbook can be executed, the following must be in place.

| Requirement | Owner | Verified |
| --- | --- | --- |
| SOC has Cloud Application Administrator standing access or break-glass | Identity Services | Quarterly |
| `ApprovedApplications` watchlist is current | Identity Services | Monthly |
| SOAR action `revoke-service-principal` tested in the development tenant | Detection Engineering | Quarterly |
| Mailbox audit logging enabled tenant-wide | Messaging | Quarterly |

## Triggers and detection

| Confidence | Trigger |
| --- | --- |
| High | DET-2026-0001 fires **and** the application was first seen in the tenant within the last 24 hours **and** the publisher is unverified |
| High | DET-2026-0001 fires **and** the consenting identity holds a privileged directory role |
| Low | DET-2026-0001 fires for an identity in a high-value group with a verified publisher |

## Investigation and analysis

1. **Identify the application.** Record application ID, display name, publisher,
   publisher verification status and tenant first-seen date.
2. **Establish provenance.** Search change management for a record naming this
   application ID. Contact the application owner if one is named.
3. **Determine the granted scopes.** Distinguish delegated permissions (act as
   the user) from application permissions (act as the tenant). Application
   permissions escalate severity to Critical.
4. **Establish blast radius.** Enumerate every identity that has consented to
   this application, not only the one that triggered the alert.
5. **Look for the delivery mechanism.** Search mail flow for the consent URL.
   Confirm whether other recipients received it. If so, raise a linked incident
   against UC-2025-0042.
6. **Look for use of the grant.** Query for Graph API activity by this service
   principal: mailbox reads, file downloads, directory enumeration, mailbox
   rule creation.

**Decision point.** Declare an incident if any of the following are true: the
application has no provenance, application-level permissions were granted, or
service principal activity against user data is observed.

## Incident declaration

Raise a ticket of type `Identity — Consent Abuse`. Severity High by default,
Critical if application permissions were granted or data access is confirmed.
Notify Identity Services on-call and the Data Protection Officer if mailbox or
file access occurred.

## Containment and mitigation

Containment is pre-authorised for this detection. Execute in order:

1. **Revoke the grant.** Delete the OAuth2 permission grants and app role
   assignments for the service principal. See RB-0007.
2. **Disable the service principal.** Set `accountEnabled` to false rather than
   deleting, so that forensic artifacts are preserved.
3. **Revoke refresh tokens** for every affected identity. Consent revocation
   alone does not invalidate tokens already issued.
4. **Block the application tenant-wide** if it is confirmed malicious.
5. **Preserve evidence** before any deletion: audit log export, sign-in log
   export, mailbox audit records, Graph activity logs.

Do not delete the application registration until evidence collection is
complete and signed off by the CSIRT lead.

## Remediation and recovery

- Reset credentials for affected identities if any secondary compromise is
  suspected.
- Remove any mailbox rules, forwarding addresses or delegate permissions
  created by the service principal.
- Review and tighten the tenant consent policy. If end-user consent is still
  permitted for this scope class, raise a control gap.
- Add the application to the tenant block list.

## Post-incident activity

- Record the application ID and any infrastructure as indicators.
- Feed the observed technique variation back to Detection Engineering as an
  improvement trigger (T4) if the detection fired late or with insufficient
  context.
- Confirm whether the `ApprovedApplications` watchlist needs updating, which is
  a common root cause of benign fires.
- Update this playbook if any step proved wrong, missing or ambiguous.

## Analyst feedback

Before closing, record the detection disposition required by `IMP-2`. If the
alert did not contain enough context to triage without pivoting, select
`insufficient-context` — that routes an improvement item to the engineering
backlog automatically.
