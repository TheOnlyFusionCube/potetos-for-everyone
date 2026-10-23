from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SessionStartTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="potetos hook test ")
        self.addCleanup(self.temp.cleanup)
        self.plugin = Path(self.temp.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin / "hooks")
        self.config = json.loads((self.plugin / "hooks/hooks.json").read_text())

    @staticmethod
    def _hook_shell():
        # On Windows, plain "bash" can resolve to the WSL launcher rather
        # than Git Bash; run the actual Git Bash binary explicitly.
        if os.name != "nt":
            return "bash"
        git = shutil.which("git")
        if git is None:
            raise RuntimeError("Git for Windows is required for the SessionStart test")
        git_root = Path(git).resolve().parent.parent
        for candidate in (git_root / "bin/bash.exe", git_root / "usr/bin/bash.exe"):
            if candidate.is_file():
                return str(candidate)
        raise RuntimeError("Git Bash executable not found alongside Git")

    def run_event(self, event, value=None):
        env = os.environ.copy()
        env.pop("POTETOS_AUTO_ACTIVATE", None)
        env["CLAUDE_PLUGIN_ROOT"] = str(self.plugin)
        if os.name == "nt":
            # MSYS shells resolve /c/... and /d/... consistently.
            env["CLAUDE_PLUGIN_ROOT"] = (
                f"/{self.plugin.drive[0].lower()}{self.plugin.as_posix()[2:]}"
            )
        if value is not None:
            env["POTETOS_AUTO_ACTIVATE"] = value
        results = []
        for entry in self.config["hooks"]["SessionStart"]:
            if re.search(entry.get("matcher", ""), event):
                for hook in entry["hooks"]:
                    results.append(subprocess.run(
                        [self._hook_shell(), "-c", hook["command"]],
                        input=json.dumps({"hook_event_name": "SessionStart", "source": event}),
                        text=True, capture_output=True, env=env, cwd=self.temp.name,
                        timeout=10,
                    ))
        return results

    def test_automatic_context_is_preserved(self):
        expected = (ROOT / "hooks/session-start-context.md").read_text()
        for event in ("startup", "clear", "compact"):
            for value in (None, "", "1"):
                with self.subTest(event=event, value=value):
                    results = self.run_event(event, value)
                    self.assertEqual(len(results), 1)
                    self.assertEqual(results[0].returncode, 0, results[0].stderr)
                    self.assertEqual(results[0].stdout, expected)
                    self.assertEqual(results[0].stderr, "")

    def test_opt_out_emits_no_context_on_any_registered_event(self):
        for event in ("startup", "clear", "compact"):
            with self.subTest(event=event):
                results = self.run_event(event, "0")
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0].returncode, 0, results[0].stderr)
                self.assertEqual(results[0].stdout, "")
                self.assertEqual(results[0].stderr, "")

    def test_opt_out_does_not_read_context_file(self):
        (self.plugin / "hooks/session-start-context.md").unlink()
        result, = self.run_event("startup", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_resume_still_does_not_inject_context(self):
        self.assertEqual(self.run_event("resume"), [])

    def test_automatic_activation_can_be_restored_after_opt_out(self):
        disabled, = self.run_event("startup", "0")
        restored, = self.run_event("startup", "1")
        self.assertEqual(disabled.stdout, "")
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertEqual(restored.stdout, (ROOT / "hooks/session-start-context.md").read_text())


    def test_on_demand_keeps_manual_plugin_entrypoints_available(self):
        # Issue #1: opting out of SessionStart must never disable manual use.
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        aliases = {entry["name"] for entry in marketplace["plugins"]}
        self.assertTrue({"pstack", "poteto-mode", "pstack-claude"} <= aliases)
        self.assertTrue(all(entry["source"] == "./" for entry in marketplace["plugins"]))
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(plugin["name"], "pstack")
        self.assertTrue((ROOT / "skills/poteto-mode/SKILL.md").is_file())
        self.assertTrue((ROOT / "agents/poteto-agent.md").is_file())
        disabled, = self.run_event("startup", "0")
        self.assertEqual(disabled.returncode, 0, disabled.stderr)
        self.assertEqual(disabled.stdout, "")


if __name__ == "__main__":
    unittest.main()
