# Telemetry and Data

*[Framework index](index.md) · [Specification](00-specification.md) · [Conformance](10-conformance.md)*

> **Normative status.** This chapter is normative. Requirement identifiers of the
> form `TEL-n` are testable conformance criteria.

Detection engineering is applied data engineering. A detection can be no better
than the telemetry beneath it, and most detection failures that are diagnosed as
logic problems are data problems wearing a disguise.

This chapter covers what a conforming program must know about its data, how to
score data quality, and why ingest economics belong in a detection framework.

---

## Requirements

**TEL-1.** Every detection MUST declare the log sources it depends on and
whether each is required or optional.

**TEL-2.** Every required log source MUST declare an expected arrival interval,
so that liveness can be monitored (`MET-4`).

**TEL-3.** A conforming program MUST maintain a log source inventory recording,
per source: owner, normalization scheme, retention, arrival interval, and known
field-coverage gaps.

**TEL-4.** Log source data quality MUST be scored and reassessed at least
annually, using the dimensions defined below.

**TEL-5.** Loss or degradation of a required log source MUST raise an
operational alert and MUST identify the detections affected.

**TEL-6.** Telemetry cost MUST be attributable to the detections that require
it, at least at log-source granularity.

**TEL-7.** A conforming program at L3 MUST normalize telemetry to a documented
schema and MUST express detection logic against the normalized schema wherever
the source supports it.

---

## Data quality dimensions

Score each source 1-5 on each dimension. The scores feed the feasibility gate
and the confidence-weighted coverage metric.

| Dimension | Question | 1 | 5 |
| --- | --- | --- | --- |
| **Completeness** | Are all in-scope assets reporting? | Ad hoc, unknown coverage | Enrolment verified against the asset inventory |
| **Timeliness** | How long from event to queryable? | Hours, variable | Under a minute, consistent |
| **Field coverage** | Do the fields the detection needs exist and populate? | Key fields frequently null | All required fields reliably populated |
| **Consistency** | Is the format stable across sources and versions? | Multiple formats, frequent change | Single normalized schema, versioned |
| **Integrity** | Can the telemetry be tampered with or suppressed by the adversary? | Local, adversary-writable | Streamed off-host, immutable, gap-detectable |

**Integrity is the dimension most often ignored.** Telemetry that an adversary
with local privileges can delete or disable is telemetry that will not be there
during the incident you care about. Detections that depend on adversary-writable
sources SHOULD be paired with a detection for the suppression itself.

---

## Normalization

Detection logic written against raw vendor fields breaks when the vendor renames
a field. Logic written against a normalized schema breaks when the *mapping*
changes, which is a single controlled artifact rather than hundreds of rules.

| Schema | Origin | Use when |
| --- | --- | --- |
| **OCSF** | Open Cybersecurity Schema Framework | Multi-vendor estates; the broadest vendor-neutral option |
| **ECS** | Elastic Common Schema | Elastic-centric estates |
| **ASIM** | Microsoft Advanced SIEM Information Model | Sentinel-centric estates |
| **CIM** | Splunk Common Information Model | Splunk-centric estates |

The framework does not mandate one. It mandates that you choose one, document
it, and write against it (`TEL-7`).

**A caution.** Normalization is lossy. Fields that do not map are dropped or
stuffed into an unparsed blob. Before writing a detection against a normalized
view, confirm the specific field you need survives the mapping. This is a
frequent cause of detections that validate in a lab against raw logs and fail
in production against normalized ones.

---

## Log source maturity

Not every source is worth the same effort. A pragmatic onboarding order, roughly
by detection value per unit of cost:

| Tier | Sources | Why |
| --- | --- | --- |
| 1 | Identity provider sign-in and audit, EDR process telemetry | Highest yield. Identity is the primary attack surface; process telemetry underpins most behavioral detection |
| 2 | Cloud control plane audit (CloudTrail, Entra audit, GCP admin), DNS | Where cloud compromise is visible; DNS is cheap and broadly useful |
| 3 | Email security, proxy/web, authentication for critical applications | Delivery and lateral movement visibility |
| 4 | Network flow, firewall, VPN | High volume, moderate yield; valuable for correlation rather than primary detection |
| 5 | Full packet capture, verbose application logs | Very high cost; justify per use case, not as a default |

**The common mistake** is to onboard tier 4 and 5 first because they are easy to
obtain and produce impressive volume figures, then discover the budget is spent
before identity telemetry is complete.

---

## Telemetry economics

Every detection framework that ignores cost gets ignored by the people who hold
the budget. Ingest is typically the largest line item in a security operations
platform, and the decision to collect a source is effectively a decision to fund
it in perpetuity.

**TEL-6** requires cost attribution. The minimum model:

$$
\text{Annual cost} = (V_{\text{GB/day}} \times 365) \times (C_{\text{ingest}} + C_{\text{retention}} \times R_{\text{years}})
$$

Put the resulting figure on the feasibility assessment. Then ask the question
that should be asked more often:

> Does the risk reduction from this detection exceed the annual cost of the
> telemetry it requires?

For most high-volume, low-yield sources the honest answer is no, and the
framework gives you a defensible way to say so at the planning gate rather than
after the invoice.

### Cost reduction patterns

| Pattern | Trade-off |
| --- | --- |
| **Tiered retention** — hot for 30 days, cold for the remainder | Cheaper; slower for investigation beyond the hot window |
| **Filtering at the collector** | Cheapest; irreversible, and you cannot detect what you discarded |
| **Summarization** — retain aggregates, discard raw | Preserves baselining; loses per-event detail |
| **Detection at the edge** — evaluate at the agent, forward only signals | Very cheap; removes the ability to hunt retrospectively |

**Record the trade-off you chose.** Every one of these patterns creates a blind
spot, and an undocumented blind spot becomes an unexplained false negative
eighteen months later.

---

## Telemetry as a first-class dependency

The practical consequence of `TEL-1` and `TEL-5` is that you can answer, in
seconds, the question every incident eventually produces:

> The EDR pipeline was down for six hours yesterday. What were we blind to?

With conforming metadata this is a query over the detection catalog for every
detection declaring that source as required. Without it, it is a week of
archaeology and an answer nobody trusts.

This single capability is frequently the argument that persuades leadership to
fund the metadata discipline the framework requires.

---

*Next: [Detection Robustness](13-detection-robustness.md) · Previous: [Detection as Code](11-detection-as-code.md)*
