# Cognitive case diagrams

<p align="center">
  <a href="https://github.com/docxology/cognitive_case_diagrams/actions/workflows/ci.yml"><img alt="ci.yml workflow status on main" src="https://github.com/docxology/cognitive_case_diagrams/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://doi.org/10.5281/zenodo.19695259"><img alt="Digital Object Identifier (DOI), manuscript series record: 10.5281/zenodo.19695259" src="https://zenodo.org/badge/DOI/10.5281/zenodo.19695259.svg"></a>
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue"></a>
  <img alt="Requires Python 3.11 or newer" src="https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

An executable review of case-role graphs, compositional grammar, synthetic uncertainty, and measurement models. Release identity comes from [package configuration](pyproject.toml), [manuscript configuration](docs/manuscript/config.yaml), and generated [citation metadata](CITATION.cff). The code provides explicit examples; it does not implement a complete linguistic parser, general topos bridge, full distributional active-inference learner, EEG model, or operational security system.

Start with the [documentation index](docs/README.md) for setup, API and
method contracts, and the [canonical manuscript](docs/manuscript/README.md).
The [reproduction guide](docs/reproduction.md) builds synthetic evidence,
figures, and the paper from a clean checkout.

## Agent access

The optional [MCP integration](docs/agent_integrations.md) exposes bounded numerical operations and read-only project resources through `ccd-mcp`. The [installable skill](skills/cognitive-case-diagrams/SKILL.md) documents evidence boundaries and reproducible workflows. Install the MCP dependency with `uv sync --extra mcp`; downstream wheel users select the `mcp` extra. From a repository checkout, `uv sync` alone suffices because the dev group already includes `mcp` — the [install section](docs/agent_integrations.md#install) documents that path.

Try the synthetic examples in the [quickstart](docs/quickstart_tutorial.md).

## Repository map

- [src](src/README.md): numerical and diagram implementations.
- [tests](tests/README.md): real computations, analytic counterexamples, and artifact checks.
- [scripts](scripts/README.md): thin generation and validation entry points.
- [docs](docs/README.md): API, mathematical scope, provenance, and manuscript sources.
- [experiments](src/experiments/README.md): typed synthetic-study configuration, paired controls, uncertainty, and provenance.
- [integrations](src/integrations/README.md): MCP schemas, resources, and stdio entry point.
- `output/`: derived figures, metrics, hydrated chapters, and render products.

This is a self-versioned project. Publish from its own repository, never by force-adding its symlinked contents to the parent workspace or template engine. Software uses [Apache-2.0](LICENSE); the existing Zenodo manuscript series retains its publication license, recorded separately in the deposit metadata.
