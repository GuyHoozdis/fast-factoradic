# Contributing

Thanks for improving `fast-factoradic`.

## Clone and set up

Clone the repository and install the development dependencies with `uv`:

```bash
git clone https://github.com/guyhoozdis/fast-factoradic.git
cd fast-factoradic
uv sync --group dev
```

## Create an isolated worktree

Use a git worktree when you want to keep feature work separate from the main checkout:

```bash
git fetch origin
git worktree add ../fast-factoradic-<topic> -b <topic> origin/main
cd ../fast-factoradic-<topic>
uv sync --group dev
```

## Development workflow

1. Make a focused change.
2. Add or update tests before changing behavior.
3. Run the relevant validation commands.
4. Update `README.md`, `CHANGELOG.md`, or both when the user-facing workflow changes.

## Validation commands

Run the standard checks from the repository root:

```bash
uvx nox
```

For targeted feedback, use:

```bash
uvx nox -s lint
uvx nox -s tests
uvx nox -s build
uv run pytest tests/test_project_metadata.py -v
```

`uvx nox -s build` is the preferred artifact check and wraps `uv build` inside the nox session.

## Pull request checklist

Before you open a pull request, confirm that you:

- kept the change scoped to one task,
- ran the relevant validation commands,
- updated documentation when behavior or workflow changed, and
- reviewed the diff for accidental edits.
