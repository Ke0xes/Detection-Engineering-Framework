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
6. **Translations.** The Apache 2.0 licence permits translation and
   redistribution, provided the `NOTICE` file is retained.

## What is out of scope

- **Detection content.** This is not a rule library. Detections are
  environment-specific; shipping them would be a liability disguised as a head
  start. Contribute to Sigma instead.
- **Tool recommendations.** The framework is vendor-neutral by design.
- **Prevention guidance.** Scoped to Detect and Respond.

## Before you open a pull request

### Everything

- Everything in this repository is licensed under the
  [Apache License 2.0](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/License).
  Under section 5 of that licence, contributions
  you submit are accepted under the same terms.
- One logical change per pull request.
- Run the checks locally. They are the same ones CI runs.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r reference-implementation/tools/requirements.txt -r requirements-docs.txt

python reference-implementation/tools/def_validate.py --strict
python reference-implementation/tools/def_test.py
python reference-implementation/tools/reading_order.py --check
mkdocs build --strict
```

### Documentation changes

The guide is read as a journey, from why the framework exists, through each
lifecycle phase, to putting it into practice. Changes to the documentation
should keep that journey intact.

#### Audience and voice

- **Primary readers are detection engineers and SOC leads.** Security leaders
  read the home page and the *In brief* summary at the end of each chapter, so
  those must stand on their own.
- **Neutral third person.** Write "a team", "the analyst" or "the program", not
  "you" or "we". Imperatives are acceptable in procedures and runbooks.
- **Explain before prescribing.** State the problem and the reasoning before the
  rule. A requirement should never be the first thing a reader meets in a
  chapter.
- **Calm and explanatory.** Avoid closing flourishes and one-line punchlines
  ("It runs.", "That is the difference..."), rhetorical contrasts with an
  imagined critic, and chapters that talk about themselves ("Why this chapter
  exists").
- **Prose carries reasoning; tables carry comparisons.** Use a table only when
  several items are compared on the same attributes.
- **Name chapters, never number them.** Write "see
  [detection robustness](detection-robustness.md)", not "see chapter 13".

#### Chapter structure

Every chapter on the reading path follows the same pattern:

1. **Title**, then the generated position line. Do not edit it by hand.
2. **Orientation.** One or two paragraphs placing the chapter in the lifecycle
   and describing the problem it addresses.
3. **Running example.** In lifecycle chapters, a short quoted block describing
   what happened to the consent phishing detection at this stage, linking to
   the matching stage of [A detection's journey](worked-example.md).
4. **What follows.** A sentence listing the sections below.
5. **The body.**
6. **In brief.** Three to five bullets that a reader can act on without
   reading the body.
7. **Requirements in this chapter.** Where the chapter has normative content,
   the requirement identifiers it covers, with a link to the specification.
8. **What comes next.** A short bridge to the next chapter on the reading path.
   Deep-dive chapters also offer a route back to the core path.
9. The generated previous and next links. Do not edit them by hand.

#### Reading order

The `nav` section of `mkdocs.yml` is the single source of reading order. To add,
remove or move a chapter, change the navigation, then run:

```bash
python reference-implementation/tools/reading_order.py
```

This regenerates the position line and the previous and next links in every
chapter. CI fails if they are out of date.

#### House style

- **No emoji.** Anywhere. Not in headings, not in tables, not in diagrams.
- **No decorative diagrams.** A Mermaid diagram must convey branching, sequence
  or ownership. A diagram that restates the bullet list above it should be
  deleted.
- **No hardcoded colors in Mermaid.** Diagrams must honor the reader's theme.
- **en-US spelling.** The normalization script enforces the common cases.
- **No repetition.** If a paragraph restates its heading, cut it.
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
- If you change validation behavior, demonstrate it: show the check failing
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
contributions are additionally acknowledged in
[CITATION.cff](https://github.com/Ke0xes/Detection-Engineering-Framework/blob/main/CITATION.cff)
and in the README on request.

## Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). In short: argue with the idea,
not the person. Technical disagreement is the point of the project.
