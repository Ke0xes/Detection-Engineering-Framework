# Review Checklist

Use this checklist to review a new or existing detection. Record each failed
item as a finding with a severity and the requirement ID.

| Severity | Meaning |
| --- | --- |
| **Blocking** | Violates a MUST requirement for production status |
| **Major** | Likely to cause missed attacks or unmanageable analyst load |
| **Minor** | Affects quality, clarity or maintainability |
| **Advisory** | An improvement beyond what the framework requires |

## Intent

- [ ] The hypothesis is one sentence: *if an adversary does X, then Y will be
      observable in Z* (`DET-1`). **Blocking** if absent.
- [ ] A VAL exists: named blocks and a boolean expression (`DET-2`).
      **Blocking** at L2 and above.
- [ ] The platform rule actually implements the VAL. Check every block and
      every operator, especially `NOT` and precedence in mixed `AND`/`OR`.
- [ ] Where there are several platform implementations, all trace to the same
      VAL and run against the same fixtures (`DET-3`).
- [ ] The title names the adversary behavior, not the tool that observed it.

## Traceability and ownership

- [ ] Linked to a use case request and a risk, threat or compliance driver
      (`GOV-1`).
- [ ] Every log source the logic depends on is declared, with `required` set
      correctly (`GOV-2`, `TEL-1`).
- [ ] Each required source has an expected arrival interval, so that silence
      can be detected (`TEL-2`, `MET-4`).
- [ ] The owner is a team (`GOV-5`).
- [ ] ATT&CK techniques are mapped at the most specific level that is true.

## Classification

- [ ] Severity, confidence and robustness tier are declared (`DET-4`).
- [ ] The robustness tier survives the smallest-change test (see
      [Robustness](#robustness)).
- [ ] The alert disposition is appropriate (`DET-5`). A low-confidence
      signal that alerts an analyst is usually a finding.
- [ ] Known benign causes are listed with triage guidance an analyst with no
      context could follow (`DET-6`).
- [ ] An `ephemeral` or `indicator` detection names the curation process that
      keeps its list current (`DET-7`).

## Telemetry and fields

- [ ] Every field in the logic is confirmed to exist in the target platform,
      with the exact name and case, from a real event (`FEA-1`).
- [ ] If the logic uses a normalized schema, each field is confirmed to
      survive the mapping. Normalization is lossy.
- [ ] Parsing is confirmed for the fields used; the rule does not silently
      depend on a field that is sometimes empty.
- [ ] The time window and lookback cover the whole behavior, allowing for
      ingestion delay.

## Logic quality

Check for each brittleness source:

| Source | Symptom | Better approach |
| --- | --- | --- |
| Hardcoded paths | Fails on another OS build or install location | Match on behavior, not location |
| Hardcoded case | Fails on case variation | Normalize case |
| Exact-match strings | Fails on padding or encoding changes | Match on structure where possible |
| Parent-child process assumptions | Fails when the parent is spoofed | Pair with a parent-spoofing detection |
| Single-field dependency | Fails when the vendor renames the field | Write against a normalized schema (`TEL-7`) |
| Static thresholds | Fails as the environment grows | Baseline relative to the population |
| Accumulated exceptions | Exclusions now cover the attack path | Rebuild assessment (`IMP-7`) |

Also check:

- [ ] Wildcards and regular expressions are anchored and bounded; leading
      wildcards on large fields are justified by necessity.
- [ ] Joins and correlations have bounded windows and keys that actually link
      the same activity.
- [ ] Query cost and run time have been measured on production-scale data
      (`DET-12`).

## Exceptions

- [ ] Every exception is in the rule under version control, not applied in
      the platform console (`DET-8`). **Blocking** if not.
- [ ] Each is narrowly scoped, ideally one entity and one condition.
- [ ] Each has a justification, owner and expiry date (`IMP-5`). **Blocking**
      if the expiry is missing.
- [ ] Each has a boundary fixture proving it suppresses nothing adjacent
      (`DET-10`).
- [ ] No expired exception has been silently renewed (`IMP-6`).
- [ ] The exception count is below the program threshold, default 10
      (`IMP-7`). Above it, recommend a rebuild assessment, not another
      exception.
- [ ] Any detection with an exception has a 90-day review cadence (`IMP-8`).

## Testing

- [ ] At least one true-positive and one true-negative fixture exist
      (`DET-9`). **Blocking** for production.
- [ ] The true negatives include the most likely benign look-alike, not only
      unrelated events.
- [ ] Adversary emulation has been run and recorded, or the reason it is not
      possible is recorded and the detection is marked unvalidated (`DET-11`).
- [ ] The last successful emulation is less than 90 days old; otherwise the
      detection counts as unvalidated.

## Response

- [ ] A playbook is linked (`RSP-1`). **Blocking** for production.
- [ ] The playbook's triggers match the detection's confidence levels.
- [ ] Pre-authorized containment actions are stated (`RSP-3`).
- [ ] The alert carries the fields the playbook's first investigation steps
      need, so the analyst does not have to search for them.

## Delivery and lifecycle

- [ ] An alert volume forecast from historical data exists before activation
      (`DEL-2`).
- [ ] Rollout is staged, and a rollback can be carried out by someone other
      than the author (`DEL-3`, `DEL-4`).
- [ ] The review cadence matches severity: critical 90 days, high 180, medium
      and low 365; 90 if any exception exists (`IMP-8`).
- [ ] The version number reflects the size of the last change.

## Robustness

Five tiers, from easiest to hardest to evade:

| Tier | Detects | Cost to evade | Example |
| --- | --- | --- | --- |
| `ephemeral` | A specific transient value | Trivial: change one value | Hash, IP address, domain, mutex name |
| `indicator` | A named artifact of one implementation | Low: rename, recompile, repack | File name, service name, registry path, user agent |
| `tool-artifact` | Behavior characteristic of a specific tool | Moderate: use another tool | A tool's default command-line flags or named-pipe pattern |
| `behavior` | The action itself, independent of tooling | High: change technique | Process opening LSASS with read access; consent grant conferring mail scopes |
| `invariant` | A property the technique cannot avoid | Very high: abandon the technique | Kerberos service ticket requested with RC4 for an account with an SPN |

**Smallest-change test.** Write down the single smallest change an adversary
could make that stops the detection firing while the technique still
succeeds. If the answer is "change a string", the tier is `indicator`,
whatever the metadata says. If no such change can be constructed, the tier
may be `invariant`.

**Coverage weights** for confidence-weighted coverage (`MET-3`): invariant
1.0, behavior 0.8, tool-artifact 0.5, indicator 0.2, ephemeral 0.05; multiply
by 0.5 if unvalidated. A technique's coverage is the weight of its strongest
validated detection, not the sum of its detections.

**Promotion.** Rebuilding an `indicator` detection at `behavior` is a
legitimate improvement that adds security without adding alert volume.
Detect what the technique requires, not what the current tool does, and
prefer choke points: authentication, privilege assignment, persistence and
data egress.
