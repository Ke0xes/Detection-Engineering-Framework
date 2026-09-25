# Detection Robustness

<!-- journey:where -->
*Walk the lifecycle › Development B: Detection engineering › Going deeper*
<!-- /journey:where -->

Two detections can both claim coverage of the same ATT&CK technique and differ
greatly in how hard they are to evade. One matches the file name of a known
tool; the other matches the action the tool performs. Renaming a file defeats
the first in seconds. Defeating the second requires a different technique
altogether. A coverage report that simply counts rules treats them as equal.

This deep dive describes how to tell the two apart, and why the difference
should shape prioritization, coverage reporting and review. It builds on the
Pyramid of Pain and on MITRE's Summiting the Pyramid research, and connects
that work to the lifecycle controls described elsewhere in the guide.

> **Running example.** The consent phishing detection is classed as
> behavior-based. It matches the permission grant itself rather than any
> attacker tooling, so it cannot be evaded by renaming or recompiling anything.
> The worked comparison at the end of this chapter shows how that classification
> is tested.

---

## The robustness ladder

Every detection declares one of five tiers (`DET-4`).

| Tier | Detects | Adversary cost to evade | Example |
| --- | --- | --- | --- |
| **Ephemeral** | A specific transient value | Trivial — change one value | Hash, IP address, domain, mutex name |
| **Indicator** | A named artifact of a specific implementation | Low — rename, recompile, repack | Filename, service name, registry key path, user agent string |
| **Tool-artifact** | A behavior characteristic of a specific tool | Moderate — use a different tool | A named tool's default command-line flags or named pipe pattern |
| **Behavior** | The action itself, independent of tooling | High — change technique | Process accessing LSASS memory with read rights; consent grant conferring mail scopes |
| **Invariant** | A property the technique cannot avoid without ceasing to work | Very high — the technique must be abandoned | Kerberos service ticket requested with RC4 encryption for an SPN-bearing account |

### The honesty problem

Robustness tier is self-declared, and there is an obvious incentive to declare
optimistically. Apply this test:

> Write down the single smallest change an adversary could make that would
> cause this detection to stop firing while the technique still succeeds.

If the answer is "change a string" it is `indicator`, whatever the metadata
says. If you cannot construct such a change, it may genuinely be `invariant`.

**DET-7** requires that ephemeral and indicator detections declare their
curation process. An indicator list that nobody owns decays into pure noise, and
a detection built on it degrades to zero without ever failing visibly.

---

## Why tier drives decisions

### It drives coverage reporting

`MET-3` requires confidence-weighted coverage at L3. Raw technique counts let a
program claim coverage of T1003 on the basis of three hash-matching rules. A
weighted model tells the truth:

| Tier | Suggested weight |
| --- | --- |
| Invariant | 1.0 |
| Behavior | 0.8 |
| Tool-artifact | 0.5 |
| Indicator | 0.2 |
| Ephemeral | 0.05 |
| Unvalidated (any tier) | multiply by 0.5 |

Coverage for a technique is the weight of its strongest validated detection,
not the sum of its detections. Ten ephemeral rules do not add up to one
behavioral one; they add up to ten things to maintain.

### It drives review cadence

Lower tiers decay faster. A program SHOULD shorten review cadence for ephemeral
and indicator detections regardless of severity, because their failure mode is
silent.

### It drives improvement targets

Robustness promotion is a legitimate, plannable improvement activity: take a
detection at `indicator` and rebuild it at `behavior`. This is one of the few
improvement activities that increases security without increasing alert volume,
which makes it unusually easy to justify.

---

## Building for robustness

### Detect the thing, not the tool

Ask what the technique *requires*, not what the current tool *does*. A
credential dumping tool can be renamed, recompiled and obfuscated. Obtaining
credential material from LSASS requires opening a handle to that process with
specific access rights. One of those is a durable detection surface; the other
is a string.

### Prefer the choke point

Adversaries have wide latitude at the edges of an attack and very little at the
choke points. Authentication, privilege assignment, persistence installation and
data egress are choke points. Detections placed there survive tooling changes.

### Assume single-detection failure

**Detection in depth.** For each critical attack path, map more than one
detection at different points and against different data sources. A single
detection covering an entire attack vector is a single point of failure, and it
will fail: through evasion, through a telemetry outage, or through drift.

Record redundancy explicitly in the coverage model so that the loss of one
detection shows its true impact rather than appearing catastrophic when it is
covered, or appearing survivable when it is not.

### Design for the analyst

A robust detection that produces an unactionable alert is not a good detection.
Robustness and precision are both required; optimising either alone produces
either a blind SOC or an exhausted one.

---

## Brittleness sources

| Source | Symptom | Mitigation |
| --- | --- | --- |
| Hardcoded paths | Fails on a different OS build or install location | Match on behavior, not location |
| Hardcoded case | Fails on case variation | Normalize case in the logic |
| Exact-match strings | Fails on any padding or encoding change | Match on structure where possible |
| Parent-child process assumptions | Fails when the adversary spoofs the parent | Pair with parent spoofing detection |
| Single field dependency | Fails when the vendor renames the field | Write against a normalized schema (`TEL-7`) |
| Static thresholds | Fails as the environment grows | Baseline relative to the population |
| Accumulated exceptions | Fails because the exclusions now cover the attack path | `IMP-7` escalation to rebuild |

The last row deserves emphasis. Exception accumulation is *robustness decay
without any change to the logic*. The detection's declared tier stays the same
while its actual resistance to evasion falls, because the adversary need only
operate inside an exclusion. This is why `IMP-7` exists and why exception
boundary fixtures (`DET-10`) are required at L3.

---

## Worked comparison

Two detections, both claiming T1003.001:

**Detection A** — matches process name `mimikatz.exe`.
Tier: `ephemeral`. Evasion cost: rename the file. Weight 0.05.

**Detection B** — matches a process handle open to `lsass.exe` with
`PROCESS_VM_READ`, excluding an allowlist of signed security tooling, where the
requesting process is not itself signed by a trusted publisher.
Tier: `behavior`. Evasion cost: obtain credential material by a different
technique entirely, for example from a memory dump taken by a legitimate signed
tool. Weight 0.8.

Both appear as "one detection for T1003.001" in a coverage report that counts
rules. Detection A stops working as soon as the tool is renamed; Detection B
continues to work until the attacker changes technique.

Note that Detection B is still not `invariant`: the named alternative evasion is
real, which is why detection-in-depth requires a second detection covering
credential access via legitimate dumping tooling.

---

## In brief

- Every detection declares one of five robustness tiers, from ephemeral
  indicators such as hashes to invariant properties the technique cannot avoid.
- The tier is tested by asking what minimal change would let an attacker evade
  the detection while the technique still succeeds.
- Coverage is weighted by tier and by validation, not counted by rule.
- Accumulated exceptions erode robustness without any change to the logic,
  which is why an exception needs an expiry and a test of its boundary.

## Requirements in this chapter

The tier declaration is required by `DET-4`, curation of indicator-based
detections by `DET-7`, and boundary tests for exceptions by `DET-10`, all in
the [specification](specification.md#62-quality-attributes). Weighted coverage
reporting is `MET-3`, described in [detection metrics](detection-metrics.md).

## What comes next

The second deep dive for this stage, [detection as code](detection-as-code.md),
explains how detections and the tests that protect their robustness are
managed like software. Readers following the core path can continue to
[the response engineering phase](development-phase-C.md).

<!-- journey:next -->
<div class="journey-footer" markdown>

---

**Previous:** [The detection engineering phase](development-phase-B.md) · **Next:** [Going deeper: Detection as code](detection-as-code.md)

</div>
<!-- /journey:next -->
