# Strict Ruff and py-pkgs Repository Expansion Design

**Prompt source:** Follow-up user instructions after the initial repository scaffold.

**Assumptions used because the user was unavailable for clarifications:**

- Use Google's Python Style Guide as the stylistic foundation, while relying on Ruff's formatter and rule compatibility constraints where they differ from literal Google wording.
- Increase the line length to `120`.
- Do **not** configure local PyPI credentials or `uv auth` entries without secrets from the user.
- Do **not** add a live PyPI publish workflow yet. Prepare the repository for release instead, and keep any future publish path compatible with GitHub Trusted Publishing.
- Use a dedicated git worktree for implementation and make regular conventional-commit checkpoints there.

## Goal

Expand the repository from a minimal scaffold into a stricter, more production-ready Python package setup by:

- adopting a much stricter Ruff configuration,
- improving package and repository metadata in line with `py-pkgs.org`,
- adding GitHub Actions for validation and build verification,
- keeping the implementation aligned with the repo's existing `uv`, `uv_build`, `uvx nox`, and `src/`-layout choices.

## Current Context

The repository already has:

- `uv_build` as the build backend,
- `uvx nox` for default validation,
- a minimal `README.md`,
- a small `src/fast_factoradic/` package,
- one focused test module,
- no GitHub Actions workflows,
- planning docs under `docs/plans/`.

The prior design doc explicitly treated CI and publishing as out of scope, but the new user request overrides that scope.

## Approaches

### Approach 1: Literal py-pkgs recreation

Add the broadest possible set of `py-pkgs` patterns immediately: richer metadata, changelog, contributor docs, coverage tooling, documentation site scaffolding, CI, and publishing automation.

This would be the closest to the book, but it overshoots the current repository content, collides with the repo's current use of `docs/` for planning artifacts, and risks creating empty or placeholder-heavy project surfaces.

### Approach 2: py-pkgs-aligned release-ready repository expansion

Adopt the compatible, high-value parts of `py-pkgs` now: richer metadata, stricter linting, better README and contributor guidance, GitHub Actions for lint/test/build, and release readiness without live publishing.

This is the recommended approach. It captures the book's repository-setup discipline without inventing content the project does not yet have or requiring secrets that are unavailable.

### Approach 3: Ruff-only hardening

Limit the work to a stricter `ruff.toml` and the code/doc fixes needed to satisfy it.

This would satisfy part of the request, but it would ignore the explicit instruction to follow `py-pkgs.org` and would leave CI and release-readiness gaps unaddressed.

## Recommended Design

### Architecture and Scope

Use **Approach 2**. Keep the repository a small library, but strengthen the engineering surfaces around it. The implementation should stay conservative: improve tooling, metadata, CI, and documentation without inventing algorithms or publishing behavior that the project is not ready to support.

Implementation should happen in a dedicated worktree created from the current branch state, with regular conventional commits that checkpoint major milestones such as Ruff hardening, metadata/docs expansion, and CI setup.

### Ruff Strategy

Make Ruff substantially stricter while avoiding self-inflicted conflicts.

Recommended lint families:

- `E`, `F`, `W`
- `I`
- `N`
- `UP`
- `YTT`
- `B`
- `A`
- `C4`
- `RET`
- `SIM`
- `ARG`
- `PT`
- `RUF`
- `ANN`
- `D`
- `S`
- `INP`
- `TID`

Formatting should remain Ruff's formatter, with `line-length = 120`.

To stay strict without fighting the toolchain:

- use `pydocstyle` with the `google` convention,
- avoid `ALL`,
- avoid `Q`,
- avoid `EM`, `TRY`, and `FBT` unless there is a concrete project need,
- avoid formatter-conflicting rules like `COM812` and `ISC001`,
- keep test-only exceptions narrow, such as `S101` and selected docstring relaxations in `tests/`.

### Repository Configuration

Align the repository more closely with `py-pkgs` by strengthening:

- `pyproject.toml` metadata such as authorship, classifiers, keywords, URLs, and optional sections that clarify project identity,
- `README.md` with install, development, validation, and package-usage guidance,
- contributor-facing instructions for the local workflow,
- release-readiness surfaces such as changelog or release notes guidance if it can be added without placeholder noise.

Because `docs/` is already used for planning documents, do not introduce a documentation site that would overload or restructure that directory in this change.

### GitHub Actions

Add GitHub Actions workflows that verify the repository on push and pull request.

Minimum CI responsibilities:

- set up Python and `uv`,
- run `uvx nox`,
- run `uv build`,
- persist built artifacts for inspection within the workflow.

If a release-oriented workflow is added, it should be build-focused and artifact-safe, not a live publish job. Any future publishing workflow should follow a **build once, promote later** model so the artifact that gets published is the same artifact that passed validation.

### Publishing Boundary

Do not configure `uv auth` or add secrets-dependent publishing steps in this change. Without credentials, any local auth setup would be speculative and unsafe. Instead, document that future PyPI publishing should use GitHub Trusted Publishing/OIDC and a protected GitHub environment.

### Testing and Verification

Verification for this work should include:

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pytest -v`
- `uvx nox`
- `uv build`

Any new workflow files should also be reviewed for consistency with the local commands they automate.

## Out of Scope

- Implementing factoradic algorithms beyond the existing validation helper
- Configuring live PyPI credentials
- Creating pull requests or GitHub releases
- Replacing the current planning-doc use of `docs/`

## Decision Summary

Use a dedicated worktree and implement a **strict, py-pkgs-aligned, release-ready** repository expansion. Make Ruff much stricter with Google-style docstring conventions and a `120`-character line length, enrich repository metadata/docs, add GitHub Actions for validation and build verification, and stop short of live publishing until explicit credentials and approval are provided.
