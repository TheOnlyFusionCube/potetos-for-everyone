from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime.runner import run_worker


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="potetos-runtime-test-"))
        self.repo_dir = self.temp_dir / "repo"
        self.repo_dir.mkdir()
        self.runs_dir = self.temp_dir / "runs"
        self.runs_dir.mkdir()

        subprocess.run(["git", "init", "-b", "main"], cwd=self.repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo_dir, check=True)

        readme = self.repo_dir / "README.md"
        readme.write_text("# Test Repo\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.repo_dir, check=True, capture_output=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_isolated_delegate_gets_separate_git_worktree(self):
        config = {
            "runners": {
                "echo_runner": {
                    "command": [sys.executable, "-c", "import sys; print('worker run: ' + sys.argv[1])", "{prompt}"],
                }
            }
        }

        res = run_worker(
            config=config,
            runner="echo_runner",
            prompt="test-prompt",
            workspace=self.repo_dir,
            runs_dir=self.runs_dir,
            isolate=True,
        )

        self.assertEqual(res.returncode, 0)
        self.assertIsNotNone(res.branch)
        self.assertTrue(res.branch.startswith("potetos/"))
        self.assertNotEqual(Path(res.workspace).resolve(), self.repo_dir.resolve())
        self.assertTrue(Path(res.stdout_file).exists())


if __name__ == "__main__":
    unittest.main()
