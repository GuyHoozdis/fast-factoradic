"""Nox sessions for linting, tests, and builds."""

import nox
from nox.sessions import Session

nox.options.sessions = ["lint", "tests", "build"]
nox.options.default_venv_backend = "uv"


def sync_dev_dependencies(session: Session) -> None:
    """Synchronize the session environment with the development dependencies."""
    environment_path = str(session.virtualenv.location)
    session.run_install(
        "uv",
        "sync",
        "--group",
        "dev",
        "--locked",
        f"--python={environment_path}",
        env={"UV_PROJECT_ENVIRONMENT": environment_path},
    )


@nox.session
def lint(session: Session) -> None:
    """Run Ruff checks and formatting validation."""
    sync_dev_dependencies(session)
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session
def tests(session: Session) -> None:
    """Run the project's test suite."""
    sync_dev_dependencies(session)
    session.run("pytest")


@nox.session
def build(session: Session) -> None:
    """Build the project's source and wheel distributions."""
    sync_dev_dependencies(session)
    session.run("uv", "build", external=True)
