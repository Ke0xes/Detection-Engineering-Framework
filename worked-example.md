# Worked Example: End to End

*[Framework index](README.md) · [Specification](specification.md) · [Conformance](conformance-model.md)*

This chapter carries a single use case through every phase of the framework, so
that the abstractions have somewhere to land. Every artifact referenced here
exists in
[`reference-implementation/`](https://github.com/Ke0xes/Detection-Engineering-Framework/tree/main/reference-implementation)
and passes the validation gates.

**The scenario:** detecting malicious OAuth application consent in a Microsoft
Entra ID tenant. It was chosen because it is an identity attack with no malware,
no endpoint compromise and no anomalous sign-in — which is where most detection
programs are weakest.

---

## Stage 1 — Business driver

The Head of Identity Services submits a request after an FS-ISAC advisory
describes consent-phishing campaigns against the sector, and two peer
organizations confirm mailbox exfiltration achieved entirely through a consented
third-party application.

The drivers recorded are `threat` and `risk`, linked to `RISK-0114` and
`RISK-0121` in the enterprise risk register.

**What matters here:** the justification states what happens *if this is not
built*, not merely what the detection would do. An adversary obtaining consent
gains access that survives password reset and MFA re-enrollment. That sentence
is what makes the request fundable.

`PLN-6` requires explicit non-goals. This request excludes allowlisted
applications, guest tenants, on-premises Active Directory, and detection of the
phishing email itself — the last of which is already covered by `UC-2025-0042`.
Recording that boundary is what prevents a scope argument at handover.

> Artifact: [`use-cases/UC-2026-0001.yml`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/reference-implementation/use-cases/UC-2026-0001.yml)

---

## Stage 2 — Prioritization

Scored against the anchored rubric in [chapter 3](planning-phase.md):

| Dimension | Score | Anchor that applied |
| --- | --- | --- |
| Threat relevance | 5 | Confirmed campaign against the sector within 90 days |
| Asset criticality | 5 | Executive mailboxes and finance repository are tier 1 in the BIA |
| Coverage gap | 4 | Admin consent workflow exists but is bypassable via scope chaining |
| Build cost | 2 | Telemetry already ingested; new logic only |
| Maintenance burden | 2 | Occasional allowlist maintenance expected |

$$
\text{Priority} = \frac{(5 \times 3) + (5 \times 3) + (4 \times 2)}{2 + 2} = \frac{38}{4} = 9.50
$$

Highest in the backlog.

**Note the coverage gap score.** The honest score is 4, not 5, because a partial
preventive control exists. Scoring it 5 would have inflated the priority. The
rubric's value is that this became an explicit, reviewable judgement against a
written descriptor rather than an unexamined number.

`PLN-3` routes this to the expedited path because threat relevance is 5. The
validator enforces this: scoring 5 while declaring the standard path produces a
warning.

---

## Stage 3 — Technical feasibility

`FEA-1` requires telemetry confirmation before logic is written.

| Question | Finding |
| --- | --- |
| Is the telemetry present? | Yes — Entra ID audit logs, already ingested |
| Are the required fields populated? | Mostly. Granted scopes are inside a nested `modifiedProperties` structure requiring parsing |
| What is missing? | Publisher verification status is not in the audit log; it requires a Graph API enrichment call |
| Cost of new telemetry? | Zero. Already collected |
| Blocking dependency? | A service principal with `Application.Read.All` for enrichment |

**The decision that matters:** the enrichment gap did not block delivery. The
council accepted initial delivery with reduced context and tracked enrichment
separately. Recording that trade-off is what stops it being rediscovered as a
surprise during triage six months later.

---

## Stage 4 — Detection engineering

### The hypothesis

`DET-1` requires one sentence:

> If an adversary obtains consent for a malicious OAuth application, then the
> directory will record a permission grant to a service principal that is not on
> the approval allowlist, carrying scopes that permit data access.

Everything downstream tests this statement.

### The VAL

`DET-2` requires platform-independent logic:

| Block | Condition |
| --- | --- |
| `B1` | A consent or permission grant operation occurred |
| `B2` | Granted scopes permit mail, file or directory access |
| `B3` | The granting identity is privileged or high value |
| `B4` | The service principal is on the approval allowlist |

Expression: `B1 AND B2 AND B3 AND NOT B4`, within a 5 minute window.

**Why `B3` exists.** Without it the detection fires on every consent event in
the tenant — hundreds per day, unusable. Restricting to privileged and
high-value identities trades a small amount of coverage for a detection the SOC
will actually read. That trade-off is recorded in the use case non-goals, so it
is a decision rather than an omission.

### Robustness

Declared `behavior`. Apply the honesty test from
[chapter 13](detection-robustness.md):

> What is the smallest change an adversary could make that stops this firing
> while the technique still works?

They would have to obtain consent from a non-privileged identity and find that
sufficient. That is a real evasion, and it is a genuine technique change rather
than a string change — which confirms `behavior` rather than `indicator`. It is
not `invariant`, precisely because that evasion exists.

### Implementations

One VAL, two implementations, both validated against the same fixtures:

- [`rules/sigma/DET-2026-0001.yml`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/reference-implementation/rules/sigma/DET-2026-0001.yml) — portable
- [`rules/kql/DET-2026-0001.kql`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/reference-implementation/rules/kql/DET-2026-0001.kql) — Sentinel

### Fixtures

`DET-9` requires positive and negative cases. Five were written:

| Fixture | Expect | Asserts |
| --- | --- | --- |
| `tp-01-privileged-consent-mailread` | match | The core case |
| `tp-02-admin-grant-directoryread` | match | A different operation and scope class |
| `tn-01-allowlisted-app` | no-match | The allowlist exclusion works |
| `tn-02-unprivileged-user` | no-match | The `B3` scope restriction works |
| `tn-03-exception-scoped` | no-match | `EXC-0001` suppresses only what it claims |

**`tn-03` is the most valuable fixture here.** It asserts the *boundary* of an
exception (`DET-10`). If someone later widens `EXC-0001` from one application to
a wildcard, the reviewer is forced to confront what the fixture is actually
proving. Without it, exception creep is invisible in a diff.

---

## Stage 5 — Response engineering

`RSP-1` blocks production without a playbook.

> Artifact: [`playbooks/PB-0003-oauth-consent-abuse.md`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/reference-implementation/playbooks/PB-0003-oauth-consent-abuse.md)

Two decisions in it are worth extracting.

**Containment is pre-authorised** (`RSP-3`). The SOC may revoke grants without
waiting for Identity Services approval. Given the access persists until
revocation, delay is more harmful than a mistaken revocation of a benign
application. That trade-off was made in advance, in writing, by the people with
the authority to make it — not at three in the morning by whoever was on shift.

**Token revocation is a mandatory, separately-called-out step.** Removing
consent does not invalidate already-issued refresh tokens. This is the step most
frequently omitted, and omitting it means the containment did not work while
appearing to. The runbook makes it step 6 and the verification section checks it
explicitly.

> Artifact: [`playbooks/RB-0007-revoke-service-principal.md`](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/reference-implementation/playbooks/RB-0007-revoke-service-principal.md)

---

## Stage 6 — Delivery

`DEL-2` requires an alert volume forecast before activation. Running the logic
against 90 days of historical data predicted 0.8 alerts per day, within the 5
per day the use case declared acceptable.

`DEL-3` staged the rollout: Finance business unit first for two weeks, then
tenant-wide. `DEL-6` gave the SOC a review period; they requested that granted
scopes appear in the alert body rather than requiring a pivot — a change made
before activation rather than as a tuning ticket afterwards.

`RSP-4` was satisfied by a joint tabletop with Identity Services on 2026-08-27,
recorded in the playbook header.

---

## Stage 7 — Improvement

The detection has been through one improvement cycle.

**Trigger T1.** Analyst dispositions showed a recurring benign fire: the
identity automation service account re-consenting a Microsoft first-party
application weekly during configuration drift remediation.

**Classified C1** (exception) under `IMP-4`. Not C4, because the logic was
correct — the environment contained a legitimate, predictable exception.

**The exception was scoped to one application ID and one initiator**, not to the
service account generally and not to first-party applications generally. It
carries a justification, an owner, an approver and an expiry of 2026-12-31
(`IMP-5`).

Because the detection now carries an exception, `IMP-8` forces a 90 day review
cadence regardless of its `high` severity. The validator enforces this: setting
`review_cadence_days` to 180 on a detection with exceptions fails the build.

**A fixture was added with the exception**, not after it. `tn-03` is that
fixture.

### Current state

| Metric | Value | Assessment |
| --- | --- | --- |
| Precision (30d) | 0.78 | Above the L3 threshold of 0.70 |
| Alert volume (30d) | 23 | Within forecast |
| Escalation rate | 0.13 | Three genuine investigations in 30 days |
| Last validated | 2026-09-15 | Fresh; stratus-red-team and Atomic both pass |
| Next review | 2026-12-14 | Not in detection debt |

---

## Stage 8 — What the gates actually catch

This is the part that is hard to convey in prose, so try it.

Clone the repository and run:

```bash
python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
```

Both pass. Now break something:

| Change | Result |
| --- | --- |
| Set `last_reviewed` back six months | `IMP-9` fails: *in detection debt: review overdue by N days* |
| Set `expires` on `EXC-0001` to a past date | `IMP-6` fails: *exception EXC-0001 expired on ...* |
| Change `review_cadence_days` to 180 | `IMP-8` fails: detection carries exceptions and requires 90 |
| Set `precision_30d` to 0.4 | `MET-2` fails: below 0.50, must be in the tuning backlog |
| Change `use_case_ref` to a non-existent ID | `TRACE` fails: reference does not resolve |
| Remove the `expected_interval_minutes` from the required log source | `MET-4` fails: liveness cannot be monitored |
| Delete `tn-02` and widen the rule to all users | `def_test` fails on the remaining negative fixtures |
| Change the rubric scores without updating `computed_score` | `PLN-1` fails: score does not match the rubric |

**That is the difference between a framework and a document.** Each of those
failures is a governance requirement that would otherwise depend on somebody
remembering, during a busy quarter, to check.

---

## What this example does not show

Honesty about the limits:

- **Only one use case.** A real catalog has hundreds, and the interesting
  problems are catalog-scale: deduplication, coverage overlap, and capacity.
- **The Sigma evaluator is a subset.** Production programs need a real backend.
  The fixture *contract* is the transferable part, not the evaluator.
- **Metrics are illustrative.** In production they are computed from case
  management data, not hand-written.
- **No deprecation is shown.** A retired detection with a successor would
  demonstrate `IMP-18` properly. Contributions welcome.

---

*Previous: [Related Work](related-work.md) · [Framework index](README.md)*
