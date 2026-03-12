# Python Repository Initialization Design

**Prompt source:** `docs/plans/initialize-repo-prompt.md`

**Assumption:** Use `fast_factoradic` as the Python import package name and `fast-factoradic` as the distribution name.

## Goal

Initialize this repository as a small Python library project that uses `uv` for dependency management, `nox` for developer automation, `ruff` for linting and formatting, `pytest` and `hypothesis` for testing, and a `src/` layout for import isolation.

## Current Context

The repository is almost empty. It contains `README.md`, `LICENSE`, and `docs/`. The current `README.md` describes the project as `fast-factoradic`, and `.gitignore` already includes common Python, `uv`, `pytest`, `hypothesis`, `nox`, and `ruff` entries.

## Approaches

### Approach 1: Explicit library scaffold with split config files

Create a conventional Python library layout with `pyproject.toml`, `ruff.toml`, `noxfile.py`, `src/fast_factoradic/`, and `tests/`. Keep package metadata in `pyproject.toml`, place strict Ruff settings in `ruff.toml`, and use `nox` to wrap lint, format-check, and test commands.

This is the recommended approach. It matches the prompt, keeps each tool's responsibility clear, and leaves room for future package growth without hiding important settings inside one file.

### Approach 2: `uv init`-generated scaffold with light edits

Start from `uv init --package` output, then layer in `nox`, `ruff.toml`, and tests. This is fast, but the generated structure can drift from the repository's exact needs and may still require manual cleanup.

This approach is acceptable, but it gives up some control for little benefit in such a small repository.

### Approach 3: Single-file configuration in `pyproject.toml`

Keep nearly all tool configuration in `pyproject.toml`, including Ruff settings. This minimizes file count, but it conflicts with the prompt's request for a strict `ruff.toml` and makes the repository harder to scan when more tooling arrives.

This approach is not recommended.

## Recommended Design

### Architecture

Treat the project as a library-first package. The `src/fast_factoradic/` tree will hold importable code, `tests/` will hold test coverage, and `nox` will provide the stable entry points for linting and test execution. `uv` remains the package manager and environment driver underneath those commands.

The initial package should stay intentionally small. Repository setup is the goal, not algorithm delivery. To give the test stack something real to exercise, the scaffold can include one tiny internal validation helper that future factoradic code is likely to reuse.

### File Layout

- Create `pyproject.toml` for package metadata, Python version requirements, build backend, and dependency groups.
- Create `ruff.toml` for strict lint and format policy.
- Create `noxfile.py` with `lint`, `format`, and `tests` sessions.
- Create `src/fast_factoradic/__init__.py` for package exports.
- Create `src/fast_factoradic/_validation.py` for a minimal non-negative integer guard used by early tests.
- Create `tests/test_validation.py` for `pytest` and `hypothesis` coverage of the validation helper.
- Update `README.md` with setup and developer workflow commands once the scaffold exists.

### Tooling Choices

Use `uv` to manage dependencies and developer environments. Put runtime metadata and development dependency groups in `pyproject.toml`. Use `pytest` as the test runner and `hypothesis` for one property-based test that proves the stack works against project code, not a toy function hidden inside the test file.

Use `ruff.toml` instead of inline Ruff configuration. Keep the rules strict but practical: lint for correctness, imports, simplification, and modernization; format with Ruff's formatter; and set a line length and target Python version explicitly.

Use `nox` as the human-friendly automation layer. Each session should call `uv run ...` so the repository has one dependency manager and one consistent way to execute tooling.

### Workflow

The expected developer flow should be:

1. Run `uv sync --group dev`.
2. Run `uv run nox -s lint`.
3. Run `uv run nox -s tests`.

This keeps local usage simple and avoids teaching multiple competing workflows.

### Error Handling

The initial validation helper should reject negative integers with a `ValueError` and non-integer inputs with a `TypeError`. That gives the package one explicit example of precise error behavior and gives `hypothesis` a meaningful invariant to test.

### Testing

Start with one focused test module:

- Standard `pytest` tests for happy-path and error-path behavior.
- One `hypothesis` property test that proves non-negative integers round-trip through the validation helper unchanged.

This keeps the scaffold honest without pretending the factoradic algorithms already exist.

## Out of Scope

- Implementing the factoradic algorithms described in `README.md`
- Publishing to PyPI
- Adding CI workflows
- Adding a CLI

## Decision Summary

Use an explicit library scaffold with separate config files. It satisfies the prompt directly, keeps the repository easy to read, and creates a clean foundation for future math-heavy work.
