from pathlib import Path
import tomllib


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_pyproject_contains_structured_package_metadata() -> None:
    pyproject = tomllib.loads(read_text("pyproject.toml"))
    project = pyproject["project"]

    assert project["authors"] == [{"name": "Guy Hoozdis"}]
    assert project["keywords"] == [
        "factoradic",
        "permutations",
        "combinatorics",
        "ranking",
        "unranking",
    ]
    assert project["classifiers"] == [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
    assert project["urls"] == {
        "Homepage": "https://github.com/guyhoozdis/fast-factoradic",
        "Repository": "https://github.com/guyhoozdis/fast-factoradic",
        "Documentation": "https://github.com/guyhoozdis/fast-factoradic#readme",
        "Changelog": "https://github.com/guyhoozdis/fast-factoradic/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/guyhoozdis/fast-factoradic/issues",
    }


def test_readme_documents_core_workflows() -> None:
    readme = read_text("README.md")

    for heading in (
        "## Install",
        "## Usage",
        "## Validation workflow",
        "## Build artifacts",
        "## Release readiness",
    ):
        assert heading in readme

    for command in ("uv sync --group dev", "uvx nox", "uv run pytest", "uv build"):
        assert command in readme


def test_contributing_guides_local_worktree_validation_flow() -> None:
    contributing = read_text("CONTRIBUTING.md")

    for heading in (
        "## Clone and set up",
        "## Create an isolated worktree",
        "## Development workflow",
        "## Validation commands",
        "## Pull request checklist",
    ):
        assert heading in contributing

    for command in (
        "uv sync --group dev",
        "git worktree add ../fast-factoradic-<topic> -b <topic> origin/main",
        "uvx nox -s lint",
        "uv run pytest tests/test_project_metadata.py -v",
        "uv build",
    ):
        assert command in contributing


def test_changelog_tracks_unreleased_work_without_a_fictional_release_date() -> None:
    changelog = read_text("CHANGELOG.md")

    for heading in ("# Changelog", "## [Unreleased]", "### Added"):
        assert heading in changelog

    for entry in (
        "- Package metadata for authors, keywords, classifiers, and project URLs.",
        "- Contributor and release-readiness documentation for the `uv` and `nox` workflow.",
        "- Initial project scaffold with `uv_build`, `uvx nox`, `pytest`, `hypothesis`, and `ruff`.",
    ):
        assert entry in changelog

    assert "## [0.1.0]" not in changelog
