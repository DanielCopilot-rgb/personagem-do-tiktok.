"""Fail-closed policy decisions for the engineering-agent executor.

This module does not execute commands or grant OS-level isolation. The executor
must call it before every tool operation; untrusted model output must never
bypass this policy or choose its own approval state.
"""

from pathlib import Path

ALLOW = "allow"
REQUIRE_APPROVAL = "require_approval"
BLOCK = "block"

_AUTOMATIC = {"read_file", "edit_file", "run_tests"}
_APPROVAL = {
    "install_dependency",
    "external_request",
    "use_secret",
    "modify_workflow",
    "publish_branch",
    "create_pull_request",
    "change_ruleset",
    "delete_file",
}
_BLOCKED = {
    "print_secret",
    "disable_protection",
    "change_permissions",
    "merge",
    "delete_outside_root",
}
_FILE_OPERATIONS = {"read_file", "edit_file", "delete_file"}
_WRITE_OPERATIONS = {"edit_file", "delete_file", "modify_workflow"}
_SECRET_NAMES = {".env", ".gemini_env", "credentials.json"}


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def evaluate(operation, project_root, target=None, branch=None, approved=False):
    """Return allow / require_approval / block. Unknown operations fail closed."""
    if not isinstance(operation, str) or operation not in (
        _AUTOMATIC | _APPROVAL | _BLOCKED
    ):
        return BLOCK

    if operation in _BLOCKED:
        return BLOCK

    root = Path(project_root).expanduser().resolve()

    if operation in _FILE_OPERATIONS:
        if not isinstance(target, (str, Path)) or not str(target).strip():
            return BLOCK
        candidate = Path(target).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        candidate = candidate.resolve()
        if not _inside(candidate, root):
            return BLOCK

        parts = candidate.relative_to(root).parts
        if ".git" in parts:
            return BLOCK
        if candidate.name in _SECRET_NAMES or candidate.name.endswith("_env"):
            return ALLOW if approved else REQUIRE_APPROVAL
        if operation == "edit_file" and ".github" in parts and "workflows" in parts:
            return ALLOW if approved else REQUIRE_APPROVAL

    if operation in _WRITE_OPERATIONS:
        if branch != "setup/agent-foundation" and not (
            isinstance(branch, str) and branch.startswith("work/")
        ):
            return BLOCK

    if operation in _APPROVAL:
        return ALLOW if approved else REQUIRE_APPROVAL

    if operation in _AUTOMATIC:
        return ALLOW

    return BLOCK
