# Python Repository Initialization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Initialize `fast-factoradic` as a Python library repository with `uv`, `nox`, strict `ruff`, `pytest`, `hypothesis`, and a `src/` layout.

**Architecture:** Build a small library-first scaffold with explicit config files and one tiny internal validation helper so the test stack exercises real package code from the start. Keep tool execution centered on `uv`, with `nox` providing stable developer commands for linting, formatting, and tests.

**Tech Stack:** Python, uv, nox, Ruff, pytest, Hypothesis, setuptools, src-layout packaging

---

### Task 1: Create package metadata and source layout

**Files:**
- Create: `pyproject.toml`
- Create: `src/fast_factoradic/__init__.py`
- Create: `src/fast_factoradic/_validation.py`
- Modify: `README.md`

**Step 1: Write the failing test**

Create `tests/test_validation.py` with a basic import and behavior test:

```python
from fast_factoradic._validation import require_non_negative_int


def test_require_non_negative_int_returns_input_for_zero() -> None:
    assert require_non_negative_int(0) == 0
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_validation.py::test_require_non_negative_int_returns_input_for_zero -v`

Expected: FAIL with an import error because the package files do not exist yet.

**Step 3: Write minimal implementation**

Create `pyproject.toml` with package metadata and developer dependencies:

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "fast-factoradic"
version = "0.1.0"
description = "O(1) calculations of a permutation in nPr-space via factoradics."
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [
  "hypothesis>=6.0",
  "nox>=2025.0.0",
  "pytest>=8.0",
  "ruff>=0.11.0",
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

Create `src/fast_factoradic/__init__.py`:

```python
from ._validation import require_non_negative_int

__all__ = ["require_non_negative_int"]
```

Create `src/fast_factoradic/_validation.py`:

```python
def require_non_negative_int(value: int) -> int:
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be non-negative")
    return value
```

Update `README.md` to add a short "Development" section with `uv sync --group dev`.

**Step 4: Run test to verify it passes**

Run: `uv sync --group dev && uv run pytest tests/test_validation.py::test_require_non_negative_int_returns_input_for_zero -v`

Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml README.md src/fast_factoradic/__init__.py src/fast_factoradic/_validation.py tests/test_validation.py
git commit -m "feat: scaffold python package metadata and source layout"
```

### Task 2: Add strict Ruff configuration

**Files:**
- Create: `ruff.toml`
- Modify: `pyproject.toml`
- Test: `tests/test_validation.py`

**Step 1: Write the failing test**

Introduce a style issue in `tests/test_validation.py` temporarily, such as an unused import, or keep an intentionally noncompliant snippet in a scratch change while developing this task.

```python
import math
```

**Step 2: Run test to verify it fails**

Run: `uv run ruff check tests/test_validation.py`

Expected: FAIL with an unused import diagnostic.

**Step 3: Write minimal implementation**

Create `ruff.toml`:

```toml
target-version = "py311"
line-length = 88

[lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = []

[format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
```

Remove the temporary style violation after confirming Ruff catches it.

**Step 4: Run test to verify it passes**

Run: `uv run ruff check . && uv run ruff format --check .`

Expected: PASS

**Step 5: Commit**

```bash
git add ruff.toml tests/test_validation.py
git commit -m "chore: add strict ruff configuration"
```

### Task 3: Add `nox` automation sessions

**Files:**
- Create: `noxfile.py`
- Modify: `README.md`

**Step 1: Write the failing test**

Try to run a `nox` session before the file exists.

```bash
uv run nox -s lint
```

**Step 2: Run test to verify it fails**

Run: `uv run nox -s lint`

Expected: FAIL with a message that `noxfile.py` or the requested session is missing.

**Step 3: Write minimal implementation**

Create `noxfile.py`:

```python
import nox

nox.options.sessions = ["lint", "tests"]


@nox.session
def lint(session: nox.Session) -> None:
    session.run("uv", "run", "ruff", "check", ".")
    session.run("uv", "run", "ruff", "format", "--check", ".")


@nox.session
def tests(session: nox.Session) -> None:
    session.run("uv", "run", "pytest")
```

Update `README.md` so the recommended commands are `uv sync --group dev`, `uv run nox -s lint`, and `uv run nox -s tests`.

**Step 4: Run test to verify it passes**

Run: `uv run nox -s lint && uv run nox -s tests`

Expected: PASS

**Step 5: Commit**

```bash
git add noxfile.py README.md
git commit -m "chore: add nox automation sessions"
```

### Task 4: Add property-based tests with Hypothesis

**Files:**
- Modify: `tests/test_validation.py`
- Test: `src/fast_factoradic/_validation.py`

**Step 1: Write the failing test**

Add a property-based test:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers(min_value=0))
def test_require_non_negative_int_round_trips_non_negative_values(value: int) -> None:
    assert require_non_negative_int(value) == value
```

Also add error-path tests:

```python
import pytest


def test_require_non_negative_int_rejects_negative_values() -> None:
    with pytest.raises(ValueError):
        require_non_negative_int(-1)


def test_require_non_negative_int_rejects_non_integers() -> None:
    with pytest.raises(TypeError):
        require_non_negative_int(1.5)
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_validation.py -v`

Expected: FAIL if the validation helper does not yet handle all cases exactly as specified.

**Step 3: Write minimal implementation**

Tighten `src/fast_factoradic/_validation.py` until all three behaviors hold:

```python
def require_non_negative_int(value: int) -> int:
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be non-negative")
    return value
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_validation.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add src/fast_factoradic/_validation.py tests/test_validation.py
git commit -m "test: add hypothesis coverage for validation helper"
```

### Task 5: Run full verification

**Files:**
- Verify only

**Step 1: Write the failing test**

No new test code is needed. This task verifies the whole scaffold together.

**Step 2: Run test to verify the current state**

Run: `uv run ruff check . && uv run ruff format --check . && uv run pytest -v && uv run nox -s lint && uv run nox -s tests`

Expected: PASS across all commands.

**Step 3: Write minimal implementation**

Fix any final packaging, import, or configuration issues surfaced by the full run. Keep fixes limited to the files above.

**Step 4: Run test to verify it passes**

Run: `uv run ruff check . && uv run ruff format --check . && uv run pytest -v && uv run nox -s lint && uv run nox -s tests`

Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml ruff.toml noxfile.py README.md src/fast_factoradic tests/test_validation.py
git commit -m "chore: finish python repository scaffold"
```
