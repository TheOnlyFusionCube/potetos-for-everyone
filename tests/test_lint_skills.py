from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AdapterRegistryLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="potetos-lint-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "adapters").mkdir()
        (self.root / "skills" / "poteto-mode" / "playbooks").mkdir(parents=True)
        shutil.copyfile(ROOT / "scripts" / "lint_skills.py", self.root / "scripts" / "lint_skills.py")
        (self.root / "skills" / "poteto-mode" / "SKILL.md").write_text(
            "---\nname: poteto-mode\ndescription: Test skill\n---\n", encoding="utf-8"
        )
        (self.root / "UPSTREAM_INVENTORY.json").write_text(json.dumps({
            "public_skills": ["poteto-mode"], "principles": [], "poteto_mode_playbooks": []
        }), encoding="utf-8")
        (self.root / "LICENSE").write_text("Copyright (c) 2026 Lauren Tan\n", encoding="utf-8")
        (self.root / "NOTICE.md").write_text("Lauren Tan\n", encoding="utf-8")
        (self.root / "README.md").write_text("Lauren Tan\n", encoding="utf-8")
        self.registry = {name: {"skill_dir": ".kiro/skills" if name == "kiro" else ".agents/skills",
                                "instruction_file": "AGENTS.md"}
                         for name in ("generic", "universal", "cursor", "claude", "codex", "gemini",
                                      "copilot", "windsurf", "cline", "roo", "continue", "kiro")}

    def lint(self, agent=None, field=None, value=None):
        registry = json.loads(json.dumps(self.registry))
        if agent is not None:
            registry[agent][field] = value
        (self.root / "adapters" / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
        return subprocess.run([sys.executable, "scripts/lint_skills.py"], cwd=self.root,
                              capture_output=True, text=True, timeout=15)

    def test_kiro_native_and_existing_adapter_paths_are_accepted(self):
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unsupported_skill_directories_are_rejected(self):
        for agent, value, expected in (
            ("kiro", ".agents/skills", ".kiro/skills"),
            ("cursor", ".kiro/skills", ".agents/skills"),
            ("kiro", ".kiro/skills/../../escape", ".kiro/skills"),
        ):
            with self.subTest(agent=agent, skill_dir=value):
                result = self.lint(agent, "skill_dir", value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"adapter {agent}: skill_dir must be {expected}", result.stderr)
                if ".." in value:
                    self.assertIn(f"adapter {agent}: unsafe skill_dir", result.stderr)

    def test_readme_kiro_and_continue_are_distinct_rows(self):
        lines = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
        kiro_index = next(i for i, line in enumerate(lines) if line.startswith("| **Kiro** |"))
        self.assertTrue(lines[kiro_index + 1].startswith("| **Continue** |"))

    def test_unsafe_instruction_paths_are_rejected_on_all_hosts(self):
        for value in ("", ".", "../escape", "/tmp/escape", "foo/../../escape",
                      r"C:\escape", r"C:escape", r"foo\..\escape", "AGENTS.md:stream"):
            with self.subTest(instruction_file=value):
                result = self.lint("kiro", "instruction_file", value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("adapter kiro: unsafe instruction_file", result.stderr)


if __name__ == "__main__":
    unittest.main()
