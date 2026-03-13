from pathlib import Path


def test_noxfile_defines_build_session_when_build_is_default() -> None:
    noxfile = Path("noxfile.py").read_text(encoding="utf-8")

    assert 'nox.options.sessions = ["lint", "tests", "build"]' in noxfile
    assert "def build(session: Session) -> None:" in noxfile
    assert 'session.run("uv", "build", external=True)' in noxfile
