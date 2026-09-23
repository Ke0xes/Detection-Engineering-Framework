# Conformance Assessment Instrument

This directory contains the self-assessment instrument for the Detection
Engineering Framework v3.0.0.

## Files

| File | Purpose |
| --- | --- |
| [`self-assessment.csv`](self-assessment.csv) | The instrument. One row per requirement. Open in any spreadsheet tool |
| [`score.py`](score.py) | Computes level attainment and produces a conformance statement |

## How to use it

1. Copy `self-assessment.csv` into your own repository. Keep it in version
   control so that conformance trajectory is visible over time.
2. For every row, set `score` to one of `met`, `partial`, `not-met` or `n/a`.
3. For every row scored `met`, record concrete evidence in the `evidence`
   column. A repository path, a pipeline run URL or a council minute reference.
   "We do that" is not evidence (`CNF-5`).
4. For every row scored `n/a`, record a justification. Unjustified `n/a` is the
   most common way self-assessment becomes theatre (`CNF-6`).
5. Run the scorer:

```bash
python assessment/score.py assessment/self-assessment.csv
```

## Scoring rules

- A level is attained only when **every** requirement at that level and below is
  scored `met` or justified `n/a`. There is no partial credit at a level
  (`CNF-2`).
- `partial` does not count toward attainment. It exists so that progress is
  visible, not so that it can be rounded up.
- Report progress toward the next level as a fraction, for example
  *L1 conformant, L2 in progress (34 of 41)*.

## Producing a claim

A valid conformance claim states level, specification version, assessment date
and scope (`CNF-1`):

> Conforms to Detection Engineering Framework v3.0.0 at Level 2, assessed
> 2026-09-01, scope: corporate IT estate and Microsoft 365 tenant. Excludes OT
> networks and the acquired subsidiary environment.

`score.py` emits this statement for you when a level is attained. Scope is the
one field it cannot infer; supply it with `--scope`.

## Reassessment

`CNF-4` requires reassessment at least annually and after any material change in
platform, team structure or scope.

`CNF-8` recommends reporting trend alongside level. The four minimum trend
measures are detection debt percentage, validation freshness, median precision,
and the count of expedited-path detections not yet brought to full conformance.
A program at L2 with those four improving is healthier than one at L3 with them
degrading.
