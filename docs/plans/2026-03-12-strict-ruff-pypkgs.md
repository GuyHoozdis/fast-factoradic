# Strict Ruff and py-pkgs Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand the repository into a stricter, release-ready Python package setup with a much stricter Ruff configuration, richer repository metadata/docs, and GitHub Actions CI/build automation.

**Architecture:** Perform the work in a dedicated git worktree created from the current branch state, then tighten local tooling before adding CI. Keep the repository aligned with its existing `uv`, `uv_build`, `uvx nox`, and `src/`-layout choices while following `py-pkgs` where it does not conflict with current repository constraints.

**Tech Stack:** Python, uv, uv_build, uvx, nox, Ruff, pytest, Hypothesis, GitHub Actions

---

### Task 1: Create the implementation worktree

**Files:**
- Verify only

**Step 1: Create the worktree**

Run:

```bash
git worktree add -b strict-ruff-pypkgs ../fast-factoradic-strict-ruff-pypkgs HEAD
```

**Step 2: Copy the current working tree snapshot into the worktree**

Run:

```bash
rsync -a --delete --exclude '.git' ./ ../fast-factoradic-strict-ruff-pypkgs/
```

Expected: the new worktree contains the current scaffold plus planning docs.

**Step 3: Verify the worktree is active**

Run:

```bash
cd ../fast-factoradic-strict-ruff-pypkgs && git --no-pager branch --show-current && git --no-pager status --short
```

Expected: branch `strict-ruff-pypkgs` and a working tree that reflects the copied snapshot.

**Step 4: Commit the imported baseline**

```bash
cd ../fast-factoradic-strict-ruff-pypkgs
git add .
git commit -m "chore: checkpoint scaffold baseline"
```

### Task 2: Enrich repository metadata and contributor docs

**Files:**
- Modify: `pyproject.toml`
- Modify: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`

**Step 1: Write the failing test**

Add a metadata-focused test file:

```python
from pathlib import Path


def test_readme_mentions_uvx_nox_and_uv_build() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "uvx nox" in readme
    assert "uv build" in readme
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_project_metadata.py::test_readme_mentions_uvx_nox_and_uv_build -v`

Expected: FAIL because the test file does not exist yet.

**Step 3: Write minimal implementation**

- Add richer `pyproject.toml` metadata: authors, keywords, classifiers, repository/documentation URLs, and optional project URLs.
- Expand `README.md` with install, usage, validation, build, and release-readiness sections.
- Create `CONTRIBUTING.md` with clone/setup/worktree/validation workflow.
- Create `CHANGELOG.md` with an initial Keep a Changelog-style structure.
- Create `tests/test_project_metadata.py` with the test above plus checks for key metadata strings.

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_project_metadata.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml README.md CONTRIBUTING.md CHANGELOG.md tests/test_project_metadata.py
git commit -m "docs: add package metadata and contributor docs"
```

### Task 3: Harden Ruff configuration and fix code/doc issues

**Files:**
- Modify: `ruff.toml`
- Modify: `noxfile.py`
- Modify: `src/fast_factoradic/__init__.py`
- Modify: `src/fast_factoradic/_validation.py`
- Modify: `tests/test_validation.py`
- Modify: `tests/test_project_metadata.py` (format-only changes if required by repo-wide Ruff formatting)
- Create: `tests/__init__.py`

**Step 1: Write the failing test**

Temporarily add a Google-docstring-sensitive Ruff failure, or create a missing-docstring case by leaving one new helper undocumented, then run Ruff against the repository.

**Step 2: Run test to verify it fails**

Run: `uv run ruff check .`

Expected: FAIL with docstring and/or annotation diagnostics once the stricter rules are enabled.

**Step 3: Write minimal implementation**

- Increase `line-length` to `120`.
- Enable a much stricter Ruff ruleset rooted in Google style:
  - `E,F,W,I,N,UP,YTT,B,A,C4,RET,SIM,ARG,PT,RUF,ANN,D,S,INP,TID`
- Add:

```toml
[lint.pydocstyle]
convention = "google"

[lint.per-file-ignores]
"tests/**/*.py" = ["D", "S101"]
```

- Keep formatter-conflict and overreach rules disabled by omission.
- Add `tests/__init__.py` to satisfy `INP`.
- Add or tighten docstrings, annotations, and exception assertions in source/tests until Ruff passes cleanly.

**Step 4: Run test to verify it passes**

Run: `uv run ruff check . && uv run ruff format --check . && uv run pytest tests/test_validation.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add ruff.toml noxfile.py src/fast_factoradic/__init__.py src/fast_factoradic/_validation.py tests/__init__.py tests/test_validation.py
git commit -m "style: enforce strict ruff rules"
```

### Task 4: Add build verification to nox

**Files:**
- Modify: `noxfile.py`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

**Step 1: Write the failing test**

Try to run a build session before it exists.

```bash
uvx nox -s build
```

**Step 2: Run test to verify it fails**

Run: `uvx nox -s build`

Expected: FAIL because no `build` session is defined yet.

**Step 3: Write minimal implementation**

- Add a `build` nox session that syncs dev dependencies and runs `uv build`.
- Keep `lint`, `tests`, and `build` as the default session set.
- Update `README.md` and `CONTRIBUTING.md` to use `uvx nox` for default validation and `uvx nox -s build` when needed directly.

**Step 4: Run test to verify it passes**

Run: `uvx nox -s build`

Expected: PASS and produce the wheel and sdist in `dist/`.

**Step 5: Commit**

```bash
git add noxfile.py README.md CONTRIBUTING.md
git commit -m "chore: add nox build verification"
```

### Task 5: Add GitHub Actions CI and build workflows

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/build.yml`
- Modify: `README.md`
- Modify: `tests/test_project_metadata.py` (workflow regression assertions if needed to pin CI/build expectations)

**Step 1: Write the failing test**

Add a workflow sanity test by checking that the workflows directory does not exist yet.

```bash
test -f .github/workflows/ci.yml
```

**Step 2: Run test to verify it fails**

Run: `test -f .github/workflows/ci.yml`

Expected: FAIL because the file does not exist.

**Step 3: Write minimal implementation**

- Create `ci.yml` to run on push and pull request:
  - checkout
  - install `uv`
  - set up Python
  - run `uvx nox`
- Create `build.yml` to run on workflow dispatch and tags:
  - checkout
  - install `uv`
  - set up Python
  - run `uv build`
  - upload the built artifacts
- Update `README.md` to mention local/CI parity.

**Step 4: Run test to verify it passes**

Run:

```bash
python - <<'PY'
from pathlib import Path
assert Path('.github/workflows/ci.yml').exists()
assert Path('.github/workflows/build.yml').exists()
PY
```

Expected: PASS

**Step 5: Commit**

```bash
git add .github/workflows/ci.yml .github/workflows/build.yml README.md
git commit -m "ci: add validation and build workflows"
```

### Task 6: Run full verification and clean build artifacts

**Files:**
- Verify only

**Step 1: Run the full suite**

Run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
uvx nox
```

Expected: PASS

**Step 2: Verify package build**

Run:

```bash
uv build
```

Expected: PASS and create `dist/fast_factoradic-0.1.0.tar.gz` and `dist/fast_factoradic-0.1.0-py3-none-any.whl`

**Step 3: Clean temporary build artifacts**

Run:

```bash
rm -rf dist
```

**Step 4: Verify final git state**

Run:

```bash
git --no-pager status --short
```

Expected: only intentional repository changes remain.

**Step 5: Commit**

```bash
git add .
git commit -m "feat: complete strict ruff and py-pkgs repository expansion"
```
