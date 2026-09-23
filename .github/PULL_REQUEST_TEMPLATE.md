## What this changes

<!-- One or two sentences. What and why. -->

## Type

- [ ] Correction (typo, broken link, factual error)
- [ ] Documentation (explanatory, non-normative)
- [ ] Specification change (normative — requires a linked issue)
- [ ] Schema change
- [ ] Tooling or CI
- [ ] Reference implementation
- [ ] Assessment instrument

## Linked issue

<!-- Required for specification changes. Fixes #NNN -->

## Checks

Run locally before requesting review:

```bash
python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
mkdocs build --strict
```

- [ ] `def_validate.py --strict` passes
- [ ] `def_test.py` passes
- [ ] `mkdocs build --strict` passes
- [ ] No emoji added
- [ ] No decorative Mermaid diagrams added; any new diagram conveys branching, sequence or ownership
- [ ] No hardcoded colours in Mermaid
- [ ] en-US spelling

## For specification changes only

- [ ] Requirement has a stable identifier, and no withdrawn identifier is reused
- [ ] A conformance level (L1/L2/L3) is assigned
- [ ] At least one form of acceptable evidence is defined
- [ ] The requirement is added to `assessment/self-assessment.csv` in this PR
- [ ] The conformance summary table in `docs/00-specification.md` is updated
- [ ] `CHANGELOG.md` names the affected requirement identifiers
- [ ] Version impact stated below

**Version impact:** <!-- MAJOR / MINOR / PATCH, and why -->

## For schema changes only

- [ ] `reference-implementation/` still validates
- [ ] Any requirement encoded in the schema is referenced in a `$comment`
- [ ] Version impact stated above

## Adoptability

<!--
The question reviewers will ask: can a two-person team with no budget still
reach L1 after this change? If your change makes the framework more complete
but less adoptable, say so here and explain the trade-off.
-->
