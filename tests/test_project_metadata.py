from pathlib import Path


def test_readme_mentions_uvx_nox_and_uv_build() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "uvx nox" in readme
    assert "uv build" in readme


def test_pyproject_contains_richer_package_metadata() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    assert "authors = [" in pyproject
    assert "keywords = [" in pyproject
    assert "classifiers = [" in pyproject
    assert 'Repository = "https://github.com/guyhoozdis/fast-factoradic"' in pyproject
    assert (
        'Documentation = "https://github.com/guyhoozdis/fast-factoradic#readme"'
        in pyproject
    )


def test_contributor_docs_exist() -> None:
    assert Path("CONTRIBUTING.md").exists()
    assert Path("CHANGELOG.md").exists()
