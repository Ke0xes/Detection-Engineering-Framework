# Contributing

Thank you for considering a contribution. This project aims to become a
community standard, which means it needs contributors who disagree with it.

## What is most useful

Ranked by how much it helps the project right now:

1. **Implementation reports.** You adopted some of this. What broke? What was
   unrealistic? Open a discussion. This is more valuable than any pull request.
2. **Conformance feedback.** A requirement that cannot be evidenced, or that is
   ambiguous, is a defect in the specification.
3. **Worked examples.** A second end-to-end example on a different surface —
   cloud, container, OT, AI — would materially improve the framework. The
   existing one is identity-focused.
4. **Platform backends.** The reference test runner implements a Sigma subset.
   Backends for Splunk, Elastic, Google SecOps or a pySigma integration would
   make the fixture contract portable.
5. **Corrections.** Technical errors, broken links, unclear wording.
6. **Translations.** The prose is CC BY 4.0 specifically to enable this.

## What is out of scope

- **Detection content.** This is not a rule library. Detections are
  environment-specific; shipping them would be a liability disguised as a head
  start. Contribute to Sigma instead.
- **Tool recommendations.** The framework is vendor-neutral by design.
- **Prevention guidance.** Scoped to Detect and Respond.

## Before you open a pull request

### Everything

- Read [`LICENSING.md`](LICENSING.md). Prose is CC BY 4.0; code, schemas and
  templates are Apache-2.0. Contributions are accepted under the licence
  applicable to the path you modify.
- One logical change per pull request.
- Run the checks locally. They are the same ones CI runs.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r reference-implementation/tools/requirements.txt -r requirements-docs.txt

python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
mkdocs build --strict
```

### Documentation changes

House style, which exists because the project is trying to be a standard rather
than a blog:

- **No emoji.** Anywhere. Not in headings, not in tables, not in diagrams.
- **No decorative diagrams.** A Mermaid diagram must convey branching, sequence
  or ownership. A diagram that restates the bullet list above it should be
  deleted.
- **No hardcoded colours in Mermaid.** Diagrams must honour the reader's theme.
- **en-US spelling.** The normalisation script enforces the common cases.
- **Terse.** If a paragraph restates the heading, cut it. The specification is
  terse by design; explanatory chapters may breathe, but not repeat.
- **RFC 2119 keywords only in normative text**, and only in capitals.

### Specification changes

Changing normative text is a bigger deal than changing prose.

- **Open an issue first** using the *Specification change* template. Do not
  start with a pull request.
- A new or strengthened `MUST` is a **MAJOR** version change and requires
  discussion. Expect this to take time.
- Every new requirement needs: a stable identifier, a level assignment
  (L1/L2/L3), and at least one form of acceptable evidence. A requirement that
  cannot be evidenced cannot be assessed and will not be accepted.
- Add the requirement to [`assessment/self-assessment.csv`](assessment/self-assessment.csv)
  in the same pull request.
- Never reuse a withdrawn identifier.

### Schema changes

- Additive changes (new optional properties) are MINOR.
- New required properties, removed properties or narrowed enums are MAJOR.
- Update `reference-implementation/` so the example still validates.
- If the change encodes a normative requirement, reference the requirement ID
  in a `$comment`.

### Code changes

- Python: standard library plus the two declared dependencies. Resist adding
  more; the tooling must stay trivial to adopt.
- Comment only what the code cannot show. No commentary explaining the change
  to the reviewer — that belongs in the pull request description.
- If you change validation behaviour, demonstrate it: show the check failing
  on a deliberately broken artifact.

## Review

Pull requests need at least one approving review from a maintainer.
Specification changes need two.

Reviewers will ask:

- Does this make the framework more adoptable, or only more complete?
- Can a two-person team with no budget still reach L1 after this change?
- Is any new requirement evidenceable?

The second question is the one that most often blocks otherwise good ideas.
Requirements that are only achievable by large, well-funded teams belong at L3
or not at all.

## Attribution

Contributors are listed in the repository's contributor graph. Substantial
contributions are additionally acknowledged in [CITATION.cff](CITATION.cff) and
in the README on request.

## Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). In short: argue with the idea,
not the person. Technical disagreement is the point of the project.
