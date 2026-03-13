import re
from pathlib import Path

USES_PATTERN = re.compile(r"^\s*uses:\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}(?:\s+#\s+v\d+)?\s*$")


def test_workflow_actions_are_pinned_by_commit_sha() -> None:
    workflow_paths = [
        Path(".github/workflows/ci.yml"),
        Path(".github/workflows/build.yml"),
    ]

    for workflow_path in workflow_paths:
        uses_lines = [line for line in workflow_path.read_text(encoding="utf-8").splitlines() if "uses:" in line]

        assert uses_lines
        assert all(USES_PATTERN.match(line) for line in uses_lines), workflow_path.as_posix()
