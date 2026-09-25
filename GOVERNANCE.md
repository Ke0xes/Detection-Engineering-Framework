# Governance

## Current state

This project is currently maintained by a single maintainer with community
contributors. That is a limitation, and this document exists to state it
honestly and to describe the path away from it.

| Role | Holder |
| --- | --- |
| Lead maintainer | Kunal Hatode |
| Maintainers | (seeking) |
| Specification editors | (seeking) |

## Why this matters

A de facto standard requires governance its adopters can trust. An organization
choosing to build its detection program around this framework is taking a
dependency on the project's continuity and neutrality. A single maintainer at a
single employer is a weak guarantee of both, regardless of that maintainer's
intentions.

This is stated plainly because pretending otherwise would be the more serious
problem.

## Decision making

### Ordinary changes

Corrections, clarifications, new explanatory content, tooling improvements:
one maintainer approval.

### Specification changes

Any change to normative text — a new requirement, a changed level assignment, a
withdrawal — requires:

1. An issue using the *Specification change* template, open for at least 14 days
   for comment.
2. Two maintainer approvals.
3. A `CHANGELOG.md` entry naming the requirement identifiers affected.

Where only one maintainer exists, the 14-day comment period is mandatory and
the decision plus its rationale is recorded in the issue, so that the reasoning
survives the maintainer.

### Disputes

Technical disputes are resolved by evidence. "This does not work in practice,
here is what happened" outweighs "this is theoretically better." Implementation
reports are the strongest form of argument available in this project.

Unresolved disputes are decided by the lead maintainer, with the reasoning
recorded publicly.

## Versioning

The specification follows semantic versioning. See
[`specification.md`](specification.md) section 15.

| Change | Increment |
| --- | --- |
| New MUST, or SHOULD promoted to MUST | MAJOR |
| New SHOULD or MAY; clarification not affecting conformance | MINOR |
| Editorial correction | PATCH |

Releases are tagged. A conformance claim names a version, so versions must be
immutable once tagged. Tags are never moved or deleted.

## Becoming a maintainer

Maintainers are invited after sustained contribution. The criteria:

- Multiple substantial merged contributions over at least three months
- Demonstrated judgement in review, particularly on adoptability
- Willingness to say no to good ideas that make the framework harder to adopt

**Maintainers from organizations other than the lead maintainer's employer are
explicitly prioritized.** Vendor neutrality is not credible without it.

## The path to neutral governance

The project's stated intent is to move to a neutral home. The realistic options:

| Option | Trade-off |
| --- | --- |
| **OWASP project** | Established neutral governance, existing community, recognised brand. Requires meeting project criteria and accepting OWASP process |
| **MITRE CTID alignment** | Strong technical alignment with Summiting the Pyramid and adjacent work. Not a governance home in itself |
| **Independent foundation** | Maximum control. Requires funding and administrative effort disproportionate to current project size |
| **Status quo with multiple maintainers** | Lowest friction. Weakest neutrality guarantee |

The immediate objective is the last option as a stepping stone, with an OWASP
project proposal as the target once a second maintainer is in place.

Adopters who need governance assurances before committing should raise it as a
discussion. Adopter demand is the strongest argument for accelerating this.

## Trademark and attribution

The name "Detection Engineering Framework" is not trademarked. Forks and
derivatives are permitted under the licences and are encouraged where the
project is not moving fast enough for an adopter's needs.

Derivative works MUST NOT represent themselves as the upstream specification.
Conformance claims reference a version of *this* specification; a fork that
changes normative requirements should version and name itself distinctly so
that conformance claims remain interpretable.

## Origin and independence

The framework originated in work conducted at Cisco and is published
independently under open licences. Cisco does not control the project, does not
review contributions, and holds no special status in its governance. Adopters
should treat it as an independent community project with a stated intent to
move to neutral governance.
