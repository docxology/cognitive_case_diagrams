# Reproduce the diagrams and manuscript

Use a clean disposable project checkout. The project writes its intermediate
artifacts and renders under `output/`. The editable chapters live only under
[`docs/manuscript/`](manuscript/README.md). Numbers in the paper are inserted
from the source-bound quality receipt, synthetic experiments, and computed
examples as described in the [method contracts](method_contracts.md).

## Build and validate the project artifacts

From the project root, use the locked environment. Python 3.14 is a supported
CI version and can also run the pinned Template.

```bash
uv sync --locked --python 3.14 --extra mcp
uv run --locked --python 3.14 python scripts/quality_gate.py --coverage
uv run --locked --python 3.14 python scripts/run_experiments.py
uv run --locked --python 3.14 python scripts/generate_diagrams.py
uv run --locked --python 3.14 python scripts/inject_variables.py
uv run --locked --python 3.14 python scripts/validate_project.py
```

The quality gate records lint, type, and test results. Experiments use declared
synthetic inputs and fixed seeds. The diagram index ties each reference to
the plot and the corresponding authored alt text. The artifact validator checks
hydration, figure files, bibliography, labels, and checksums.

## Render with pinned Template

Use a separate Template checkout and follow its
[pinned setup guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md).
From that checkout:

```bash
git switch --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
mkdir -p projects/working
ln -s /absolute/path/to/cognitive_case_diagrams projects/working/cognitive_case_diagrams
uv run --locked python scripts/pipeline/stage_03_render.py --project working/cognitive_case_diagrams --skip-manuscript-hydration
```

A detached worktree directly at the named slot also works. The
`--skip-manuscript-hydration` flag preserves the project's already hydrated
chapters and its own evidence checks.

Run the web correction from the project checkout, then validate from the
Template checkout. Do this after the last render so validation observes
the corrected HTML.

```bash
# Project checkout
uv run --locked --python 3.14 python scripts/correct_web.py

# Template checkout
uv run --locked python scripts/pipeline/stage_04_validate.py --project working/cognitive_case_diagrams
```

The combined outputs are `output/pdf/cognitive_case_diagrams_combined.pdf`
and `output/web/index.html` inside the project. Template writes validation
and provenance reports under `output/reports/`. Check the paper's section
order, resolved citations, and [figure index](manuscript_figure_index.md).
The [release workflow](release_workflow.md) describes the additional visual
and browser observations required for a release review.
