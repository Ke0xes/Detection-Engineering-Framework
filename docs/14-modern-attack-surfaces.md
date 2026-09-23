# Modern Attack Surfaces

*[Framework index](index.md) · [Specification](00-specification.md) · [Conformance](10-conformance.md)*

The lifecycle in this framework is surface-independent. The *assumptions* most
detection programs carry are not: they were formed when the estate was Windows
endpoints on a corporate network, and they transfer poorly.

This chapter records what changes when the framework is applied to surfaces
where the endpoint is not the unit of compromise.

---

## Identity

Identity is the primary attack surface. In most intrusions that matter, no
malware executes and no endpoint is compromised.

### What changes

| Assumption | Reality |
| --- | --- |
| Compromise begins at an endpoint | Compromise begins at an identity provider, frequently from an unmanaged device |
| Authentication is the control point | Post-authentication *authorization* is the control point; tokens and consent grants outlive credentials |
| Password reset contains the incident | Password reset does nothing to a stolen refresh token, a consented application, or an added authentication method |
| MFA is a detection boundary | MFA fatigue, adversary-in-the-middle proxies and device-code phishing all produce successful, MFA-satisfied sign-ins |

### Priority detection surfaces

| Surface | Why |
| --- | --- |
| OAuth consent and permission grants | Persistent delegated access that survives credential rotation. See the [worked example](19-worked-example.md) |
| Authentication method registration | Adding a method is the quietest persistence mechanism in most tenants |
| Conditional access policy modification | Disabling a control is a precondition to using it |
| Privileged role assignment and eligible-role activation | Privilege escalation in a cloud directory |
| Token anomalies | Impossible travel is weak; token replay from a new device or unexpected client ID is strong |
| Federation and trust changes | Adding a federated domain or signing certificate is total tenant compromise |
| Service principal credential addition | A new secret on an existing application is backdoor persistence with legitimate-looking telemetry |

### Framework implications

- Asset criticality in the [planning rubric](03-planning-phase.md) applies to
  *identities*, not only systems. A privileged identity is a tier 1 asset.
- Response playbooks MUST include token revocation explicitly. Consent removal
  or password reset alone does not end access, and this step is the one most
  often omitted.
- Robustness: identity telemetry is comparatively stable and schema-consistent,
  so behavioural detections here tend to last longer than endpoint equivalents.

---

## Cloud control plane

### What changes

The control plane is an API. Compromise is a sequence of authorized API calls,
each individually legitimate. There is no malicious binary to find.

| Assumption | Reality |
| --- | --- |
| Lateral movement is network-based | Lateral movement is role assumption and cross-account trust |
| Persistence is a file or service | Persistence is an IAM role, a Lambda trigger, an automation account or a resource policy |
| Exfiltration crosses the perimeter | Exfiltration is a bucket policy change or a snapshot shared to an external account |
| The blast radius is the host | The blast radius is whatever the compromised principal may call |

### Priority detection surfaces

| Surface | Why |
| --- | --- |
| IAM policy and role changes | Privilege escalation, and the precondition to nearly everything else |
| Resource sharing to external accounts | Snapshot, image and bucket sharing is quiet, complete exfiltration |
| Logging and guardrail modification | Disabling CloudTrail, audit logs or a security service precedes the rest |
| Credential and key creation | New access keys on an existing principal |
| Serverless function and automation changes | Execution-on-trigger persistence |
| Unusual regions | Activity in never-used regions is a durable, high-precision signal |

### Framework implications

- Telemetry is cheap and complete relative to endpoint. `TEL-3` inventory work
  is comparatively easy here; the difficulty is volume and cost.
- Many control-plane detections are `invariant` tier: the API call is the
  technique. This is the highest-yield robustness territory available.
- Preventive controls (service control policies, guardrails) are strong here,
  which changes the `coverage_gap` score. Monitor the guardrail itself.

---

## SaaS

The estate most programs monitor least. Data lives in applications the security
team does not administer and frequently cannot query.

| Surface | Why |
| --- | --- |
| Third-party application integration | The most common SaaS-to-SaaS lateral path |
| Sharing and permission changes | Public link creation, external collaborator addition |
| Administrative action outside change windows | Small admin populations make anomalies visible |
| Bulk export and download | The clearest exfiltration signal available in most SaaS platforms |
| Authentication bypass | Legacy protocols, app passwords, and API tokens that skip conditional access |

**The dominant constraint is telemetry availability.** Many SaaS platforms emit
audit logs only at premium licence tiers or with short retention. Make this a
procurement requirement: audit log availability, retention and API access
belong in the security requirements for any SaaS purchase. Raising it after
signature is raising it too late, and `FEA-1` will otherwise block the use case
permanently.

---

## Containers and Kubernetes

| Surface | Why |
| --- | --- |
| Workload spawning an interactive shell | Containers are normally single-purpose; a shell is anomalous by construction |
| Privileged or host-namespace containers | The standard escape path |
| Service account token abuse | Kubernetes credentials are files in the filesystem |
| API server anomalies | `exec`, `port-forward`, secret enumeration |
| Unexpected image sources | Registry outside the approved set |
| Runtime drift from the image | A process running that was not in the image |

The advantage here is that container environments are **more** predictable than
general-purpose hosts. Immutability makes deviation detectable. Detections built
on "this workload should never do X" are often `invariant` tier and exceptionally
precise.

The disadvantage is ephemerality: a container may live for seconds. Telemetry
must be streamed and correlated by workload identity, not host.

---

## CI/CD and software supply chain

The highest-leverage target in most organizations, and the least monitored.
Build systems hold production credentials, run arbitrary code by design, and are
trusted by everything downstream.

| Surface | Why |
| --- | --- |
| Pipeline definition changes | A modified workflow file is arbitrary code execution with production credentials |
| Secret access anomalies | A job reading secrets it has never read before |
| Self-hosted runner compromise | Long-lived, credential-rich, rarely monitored |
| Dependency changes | Typosquats, newly introduced transitive dependencies, maintainer changes |
| Artifact signing failures | Unsigned or mis-signed artifacts reaching a registry |
| Branch protection modification | Disabling review is the precondition to injecting code |

**Framework implication.** The detection repository described in
[Detection as Code](11-detection-as-code.md) is itself in this category. A
program that automates detection deployment has created a new high-value target
and MUST monitor it. Apply the framework to itself.

---

## Operational technology

Where the framework applies with the most modification.

| Difference | Consequence |
| --- | --- |
| Availability outranks confidentiality | Automated containment is usually forbidden. `RSP-3` pre-authorisation is typically "none" |
| Protocols are deterministic | Baselining works unusually well; deviation is meaningful |
| Systems cannot be patched or instrumented | Detection is almost entirely network-based and passive |
| Change is rare and scheduled | Any unscheduled change is high-signal |
| Safety consequences are physical | Response playbooks must involve engineering and safety authorities, not only IT |

Use the same lifecycle. Change the response engineering assumptions: `RSP-3`
authority, escalation paths and containment options all differ fundamentally.

---

## AI and machine learning systems

New surface, and the one most likely to date this framework if omitted. Map
threats using **MITRE ATLAS** alongside ATT&CK; the detection schema supports
`atlas_techniques` for this purpose.

### Two distinct problems

**1. Attacks on AI systems you operate.**

| Surface | Why |
| --- | --- |
| Prompt injection reaching a tool-enabled agent | Indirect injection via retrieved content is the dominant practical attack |
| Agent tool invocation anomalies | An agent calling tools or APIs outside its expected pattern |
| Model or system prompt extraction | Repeated probing; unusual output volume |
| Training and RAG data poisoning | Unauthorized writes to a corpus or vector store |
| Model artifact tampering | Changes to weights or model files outside the deployment pipeline |
| Inference cost anomalies | Resource abuse; also an early indicator of automated probing |

**The critical framing:** an AI agent with tool access is a *privileged
identity*. It authenticates, it holds permissions, and it acts. Treat it as one.
Give it an identity in the asset inventory, score it in the planning rubric,
monitor its authorization changes and its actions, and give it a containment
procedure. Most organizations currently do none of this.

**2. Attacks that use AI.**

Adversaries using generative tooling produce higher-quality lures and faster
tooling iteration. This does not create new techniques so much as it *degrades
detections that relied on poor adversary craft*. Detections whose implicit
signal was "badly written English" or "unusual binary structure" have lost
efficacy and should be re-scored for robustness.

### Framework implications

- Add AI systems to the telemetry inventory (`TEL-3`). Most have none today.
- Agent action logs are a required log source for any agent with write access.
- Expect this section to change faster than any other. It is versioned with the
  specification for that reason.

---

## Applying the framework across surfaces

The lifecycle does not change. What changes per surface is:

| Element | What to re-examine |
| --- | --- |
| Asset criticality | The unit of value: identity, workload, dataset, pipeline, agent |
| Telemetry availability | Frequently the binding constraint; sometimes a procurement problem |
| Robustness | API-based surfaces offer more `invariant` detections than endpoints |
| Response authority | OT and production cloud constrain automated containment |
| Review cadence | Faster-changing surfaces need shorter cadences |

**The framework's claim is that one lifecycle governs all of them.** A consent
grant, a container escape, an IAM policy change and an agent tool invocation are
all: a business driver, a hypothesis, telemetry, logic, a test, a response, and
a review date.

---

*Next: [Governance and Roles](15-governance-and-roles.md) · Previous: [Detection Robustness](13-detection-robustness.md)*
