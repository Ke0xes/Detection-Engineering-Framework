# Licensing

This repository is dual-licensed. The licence that applies depends on which part
of the repository you are using.

| Path | Content type | Licence |
| --- | --- | --- |
| `docs/**` | Prose, specification text, diagrams | [CC BY 4.0](LICENSE) |
| `SPECIFICATION.md`, `README.md`, other root `*.md` | Prose and specification text | [CC BY 4.0](LICENSE) |
| `schema/**` | JSON Schema, YAML examples | [Apache-2.0](LICENSE-CODE) |
| `reference-implementation/**` | Scripts, CI configuration, tests | [Apache-2.0](LICENSE-CODE) |
| `templates/**` | Fill-in templates and forms | [Apache-2.0](LICENSE-CODE) |
| `assessment/**` | Assessment instrument and scoring logic | [Apache-2.0](LICENSE-CODE) |
| `.github/**` | Repository automation | [Apache-2.0](LICENSE-CODE) |

## Why two licences

The prose is licensed CC BY 4.0 so that it can be quoted, translated, excerpted
into internal standards, and cited in academic work with attribution.

The machine-readable and executable material is licensed Apache-2.0 because
CC licences are not designed for software and most enterprise legal functions
will not permit CC-licensed material to be vendored into a codebase. Apache-2.0
also carries an explicit patent grant, which matters for a specification that
vendors may implement.

## Attribution

When citing the prose, the required attribution is:

> Hatode, K. et al. *Detection Engineering Framework*, version 3.0.
> https://github.com/Ke0xes/Detection-Engineering-Framework
> Licensed under CC BY 4.0.

A machine-readable citation is provided in [CITATION.cff](CITATION.cff).

## Contributions

Contributions are accepted under the licence applicable to the path being
modified. See [CONTRIBUTING.md](CONTRIBUTING.md).
