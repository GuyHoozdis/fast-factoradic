# fast-factoradic

`fast-factoradic` is a small Python package for factoradic-oriented permutation work. The project is still early, but the repository already ships a strict validation helper and a `uv`-based workflow for building, linting, and testing future combinatorics features.

## Install

Install the project for local development with `uv`:

```bash
uv sync --group dev
```

If you only need the package in the current environment, install it from the repository root:

```bash
uv pip install -e .
```

## Usage

The current public API exports `require_non_negative_int`, which validates integer inputs before downstream factoradic calculations:

```python
from fast_factoradic import require_non_negative_int

size = require_non_negative_int(12)
```

## Validation workflow

Run the default automation with:

```bash
uvx nox
```

The GitHub Actions validation workflow runs this same command so local checks and CI stay aligned.

Run individual sessions when you want faster feedback:

```bash
uvx nox -s lint
uvx nox -s tests
uvx nox -s build
```

You can also run pytest directly during focused development:

```bash
uv run pytest
```

## Build artifacts

Build the source distribution and wheel from the repository root:

```bash
uvx nox -s build
```

This session syncs the development environment and runs `uv build` for you.
The GitHub Actions build workflow uses the same `uv build` command before uploading the generated artifacts.

Generated artifacts are written to `dist/`.

## Release readiness

Before tagging a release, make sure you:

1. Run `uvx nox`.
2. Run `uvx nox -s build` if you need to re-check build artifacts directly.
3. Review `CHANGELOG.md`.
4. Confirm package metadata in `pyproject.toml` still matches the repository state.

## Repository guides

- Contributor workflow: [`CONTRIBUTING.md`](https://github.com/guyhoozdis/fast-factoradic/blob/main/CONTRIBUTING.md)
- Change history: [`CHANGELOG.md`](https://github.com/guyhoozdis/fast-factoradic/blob/main/CHANGELOG.md)
