import tempfile
import unittest
from pathlib import Path

from agent_security.policy import ALLOW, BLOCK, REQUIRE_APPROVAL, evaluate


class TestAgentSecurityPolicy(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "main.py").write_text("print('ok')", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_allows_read_inside_project(self):
        self.assertEqual(evaluate("read_file", self.root, "src/main.py"), ALLOW)

    def test_allows_edit_on_work_branch(self):
        self.assertEqual(
            evaluate("edit_file", self.root, "src/main.py", "setup/agent-foundation"),
            ALLOW,
        )

    def test_blocks_edit_on_main(self):
        self.assertEqual(
            evaluate("edit_file", self.root, "src/main.py", "main"), BLOCK
        )

    def test_blocks_path_traversal(self):
        self.assertEqual(
            evaluate("edit_file", self.root, "../outside.txt", "setup/agent-foundation"),
            BLOCK,
        )

    def test_blocks_symlink_escape(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / "escape").symlink_to(outside, target_is_directory=True)
        self.assertEqual(
            evaluate("edit_file", self.root, "escape/payload.txt", "setup/agent-foundation"),
            BLOCK,
        )

    def test_blocks_git_metadata(self):
        self.assertEqual(
            evaluate("edit_file", self.root, ".git/config", "setup/agent-foundation"),
            BLOCK,
        )

    def test_secret_requires_explicit_approval(self):
        self.assertEqual(evaluate("read_file", self.root, ".gemini_env"), REQUIRE_APPROVAL)
        self.assertEqual(
            evaluate("read_file", self.root, ".gemini_env", approved=True),
            ALLOW,
        )

    def test_workflow_changes_require_approval(self):
        result = evaluate(
            "edit_file", self.root, ".github/workflows/tests.yml", "setup/agent-foundation"
        )
        self.assertEqual(result, REQUIRE_APPROVAL)
        approved = evaluate(
            "edit_file", self.root, ".github/workflows/tests.yml", "setup/agent-foundation", approved=True
        )
        self.assertEqual(approved, ALLOW)

    def test_network_and_publish_require_approval(self):
        self.assertEqual(evaluate("external_request", self.root), REQUIRE_APPROVAL)
        self.assertEqual(evaluate("publish_branch", self.root), REQUIRE_APPROVAL)
        self.assertEqual(evaluate("publish_branch", self.root, approved=True), ALLOW)

    def test_high_risk_operations_are_blocked(self):
        for operation in ("print_secret", "disable_protection", "change_permissions", "merge"):
            with self.subTest(operation=operation):
                self.assertEqual(evaluate(operation, self.root, approved=True), BLOCK)

    def test_unknown_operations_fail_closed(self):
        self.assertEqual(evaluate("run_arbitrary_shell", self.root, approved=True), BLOCK)


if __name__ == "__main__":
    unittest.main()
