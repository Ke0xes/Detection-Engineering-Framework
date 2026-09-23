# Reference Implementation

This directory is the executable half of the Detection Engineering Framework.
Everything here runs. If you only read one part of this repository before
adopting the framework, read this one.

It exists to answer a question the prose cannot: *what does a conforming
detection actually look like on disk, and how is conformance enforced without
relying on anyone remembering to check?*

## Layout

```
reference-implementation/
├── use-cases/           Planning artifacts (schema/use-case.schema.json)
├── detections/          Detection metadata (schema/detection.schema.json)
├── rules/
│   ├── sigma/           Portable detection logic
│   └── kql/             Platform-specific implementation
├── fixtures/            Telemetry samples that assert detection behaviour
├── playbooks/           Response playbooks and runbooks
└── tools/
    ├── def_validate.py  Schema + framework conformance checking
    ├── def_test.py      Fixture regression harness
    └── normalise-docs.ps1
```

## The worked example

One use case is carried end to end, so that every link in the traceability
chain is visible:

| Stage | Artifact |
| --- | --- |
| Business driver and priority score | [`use-cases/UC-2026-0001.yml`](use-cases/UC-2026-0001.yml) |
| Detection metadata and VAL | [`detections/DET-2026-0001.yml`](detections/DET-2026-0001.yml) |
| Portable logic | [`rules/sigma/DET-2026-0001.yml`](rules/sigma/DET-2026-0001.yml) |
| Platform implementation | [`rules/kql/DET-2026-0001.kql`](rules/kql/DET-2026-0001.kql) |
| Behavioural assertions | [`fixtures/DET-2026-0001/`](fixtures/DET-2026-0001) |
| Response | [`playbooks/PB-0003-oauth-consent-abuse.md`](playbooks/PB-0003-oauth-consent-abuse.md) |
| Containment procedure | [`playbooks/RB-0007-revoke-service-principal.md`](playbooks/RB-0007-revoke-service-principal.md) |

The narrative walkthrough, explaining *why* each decision was made, is in
[docs/19-worked-example.md](../docs/19-worked-example.md).

## Running it

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r reference-implementation/tools/requirements.txt

python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
```

Expected output:

```
Validated 2 artifact(s): 0 error(s), 0 warning(s)

PASS  DET-2026-0001  tp-01-privileged-consent-mailread.json  (expected match)
PASS  DET-2026-0001  tp-02-admin-grant-directoryread.json  (expected match)
PASS  DET-2026-0001  tn-01-allowlisted-app.json  (expected no-match)
PASS  DET-2026-0001  tn-02-unprivileged-user.json  (expected no-match)
PASS  DET-2026-0001  tn-03-exception-scoped.json  (expected no-match)

5 passed, 0 failed, 0 skipped
```

## What the validator enforces

`def_validate.py` applies two layers. JSON Schema catches structural problems.
The second layer catches the things a schema cannot express, and these are the
ones that matter operationally:

| Check | Requirement | Why it exists |
| --- | --- | --- |
| Use case reference resolves | `TRACE` | A detection with a dangling driver reference cannot demonstrate traceability |
| Delivered use cases name their detections | `TRACE` | Closes the loop in the other direction |
| Priority score matches the rubric | `PLN-1` | Prevents scores being back-fitted to a desired ranking |
| Exceptions carry an expiry, and it has not passed | `IMP-5`, `IMP-6` | Exceptions are the main way detections die silently |
| Exception count below threshold | `IMP-7` | Persistent exclusions mean the logic models the wrong thing |
| Detections carrying exceptions review at 90 days | `IMP-8` | Suppressed detections need more scrutiny, not less |
| Production detections are not past review date | `IMP-9` | Surfaces detection debt as a build failure |
| Required log sources declare an expected interval | `MET-4` | Liveness cannot be monitored without one |
| Production detections report precision | `MET-1` | Blocks the metric being quietly skipped |
| Precision below 0.50 fails the build | `MET-2` | Forces the tuning backlog to be real |
| Positive and negative fixtures both exist | `IMP-13` | A detection that was never tested against benign data is untested |
| Referenced files exist | `REF` | Catches renames that break the chain |

Try it: open the detection file, set `last_reviewed` back six months, and run
the validator. The build fails. That is the entire point — detection debt
becomes visible automatically rather than accumulating unnoticed.

## The fixture contract

`def_test.py` implements a deliberately small Sigma subset: field maps, list
values, the `contains` / `startswith` / `endswith` / `re` / `all` modifiers, and
conditions built from identifiers with `and`, `or`, `not` and parentheses.

It is not a replacement for pySigma. It exists to demonstrate the contract:

> Every detection ships with telemetry samples it must match and telemetry
> samples it must not match, and those assertions run before the rule reaches
> production.

Note `tn-03-exception-scoped.json`. It asserts the *boundary* of an exception,
not just its effect. If somebody later widens `EXC-0001` from one application to
a wildcard, a different fixture would be needed to catch it — which is exactly
the review conversation you want to force.

To adopt this in your own environment, keep the fixture contract and replace the
evaluator with your platform's backend: `splunk-sdk`, the Sentinel REST API,
Elastic's `_eval` endpoint, or pySigma with the appropriate backend.

## Adapting this

1. Copy `schema/` into your detection repository unchanged.
2. Copy `tools/def_validate.py`. Adjust the path constants at the top.
3. Replace `def_test.py`'s evaluator with your platform backend.
4. Copy `.github/workflows/validate.yml` and wire it to your default branch.
5. Migrate detections into the metadata format incrementally. A detection that
   is not yet migrated simply is not covered by the gates; there is no need for
   a big-bang conversion.

Start with step 1 and 2 only. A repository that merely validates metadata is
already ahead of most programs.
