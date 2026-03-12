import nox

nox.options.sessions = ["lint", "tests"]


@nox.session(venv_backend="none")
def lint(session: nox.Session) -> None:
    session.run("uv", "run", "ruff", "check", ".", external=True)
    session.run("uv", "run", "ruff", "format", "--check", ".", external=True)


@nox.session(venv_backend="none")
def tests(session: nox.Session) -> None:
    session.run("uv", "run", "pytest", external=True)
