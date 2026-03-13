# fast-factoradic

O(1) caclulations of a permutation in nPr-space via factoradics - indexes in base factorial.

In the same way that you can have a number system in base 10 (decimal), or 2 (binary), or 16 (hexadecimal), you can have a number system in base factorial, where the place values are 1!, 2!, 3!, and so on. 


## Install

Install the project for local development with `uv`:

```bash
uv sync --locked
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

Run the default automation locally with:

```bash
uvx nox
```

Run individual sessions when you want faster feedback:

```bash
uvx nox -s lint
uvx nox -s tests
```

You can also run pytest directly during focused development:

```bash
uv run pytest path/to/test_file.py
```

## Build artifacts

Build the source distribution and wheel from the repository root:

```bash
uv build
```

Generated artifacts are written to `dist/`.

## Release readiness

Before tagging a release, make sure you:

1. Run `uvx nox`.
2. Run `uv build` if you need to re-check build artifacts directly.
3. Review `CHANGELOG.md`.
4. Confirm package metadata in `pyproject.toml` still matches the repository state.

## Repository guides

- Contributor workflow: [`CONTRIBUTING.md`](https://github.com/guyhoozdis/fast-factoradic/blob/main/CONTRIBUTING.md)
- Change history: [`CHANGELOG.md`](https://github.com/guyhoozdis/fast-factoradic/blob/main/CHANGELOG.md)
