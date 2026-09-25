# Security Policy

## Scope

This repository contains documentation, JSON schemas, example detection content
and small Python validation tools. It is not a deployed service and processes no
user data.

Security issues that are in scope:

| Category | Example |
| --- | --- |
| **Tooling vulnerabilities** | Code execution or path traversal in `def_validate.py`, `def_test.py`, `score.py` or `normalize-docs.ps1` |
| **Supply chain** | A compromised or malicious dependency; an unpinned action in a workflow |
| **CI/CD** | A workflow configuration permitting privilege escalation or secret exfiltration |
| **Harmful guidance** | Documented procedures that would materially weaken a reader's security posture if followed |
| **Unsafe example content** | Example rules, runbook commands or fixtures that could cause damage if executed |

Out of scope:

- Detection rules being evadable. All detections are evadable; that is why
  [chapter 13](detection-robustness.md) exists. Open a normal issue.
- Disagreement with a normative requirement. Open a *Specification change* issue.

## Reporting

**Use GitHub's private vulnerability reporting**: go to the repository's
Security tab and select *Report a vulnerability*. This creates a private
advisory visible only to maintainers.

Do not open a public issue for a security report in the first instance.

Please include:

- What the issue is and where in the repository
- How to reproduce it
- What an attacker could achieve
- Any suggested remediation

## Response

| Stage | Target |
| --- | --- |
| Acknowledgement | 5 working days |
| Initial assessment | 10 working days |
| Fix or mitigation for confirmed issues | 30 days |

This project has a single maintainer and no commercial support. These are
good-faith targets, not guarantees. If a report is time-critical and receives
no acknowledgement within the target, escalating publicly is reasonable.

## Disclosure

Coordinated disclosure. We will agree a disclosure date with the reporter and
credit them in the advisory and the changelog unless they prefer otherwise.

## A note on the example content

The `reference-implementation/` directory contains runbook commands that revoke
OAuth grants and disable service principals in Microsoft Entra ID. These are
illustrative and are intended to be reviewed and adapted, not pasted into a
production tenant.

Treat any executable content in this repository as untrusted input to your
change process, exactly as you would treat a detection rule from a public
source.
