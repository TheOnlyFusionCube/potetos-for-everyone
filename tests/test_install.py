from __future__ import annotations

import importlib.machinery
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]

loader = importlib.machinery.SourceFileLoader("potetos_cli", str(ROOT / "bin" / "potetos"))
potetos = loader.load_module()


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="potetos-test-"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_default_install_is_self_contained_and_all_agent(self):
        args = SimpleNamespace(
            target=str(self.temp_dir),
            agent="all",
            link=False,
            force=False,
            no_gitignore=False,
        )
        potetos.install(args)

        skill_file = self.temp_dir / ".agents" / "skills" / "poteto-mode" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "poteto-mode skill must exist")

        manifest_file = self.temp_dir / ".potetos" / "install.json"
        self.assertTrue(manifest_file.exists(), "manifest must exist")
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("mode"), "copy")
        self.assertIn("universal", manifest.get("agents", []))
        self.assertIn("cursor", manifest.get("agents", []))
        self.assertIn("claude", manifest.get("agents", []))

        agents_md = self.temp_dir / "AGENTS.md"
        self.assertTrue(agents_md.exists(), "AGENTS.md must exist")
        content = agents_md.read_text(encoding="utf-8")
        self.assertIn("<!-- potetos-for-everyone:begin -->", content)

    def test_install_and_uninstall_preserve_existing_content(self):
        agents_md = self.temp_dir / "AGENTS.md"
        user_header = "# Existing User Project Guidelines\n\nKeep this content intact."
        agents_md.write_text(user_header, encoding="utf-8")

        args = SimpleNamespace(
            target=str(self.temp_dir),
            agent="all",
            link=False,
            force=False,
            no_gitignore=False,
        )
        potetos.install(args)

        content_after_install = agents_md.read_text(encoding="utf-8")
        self.assertIn("Existing User Project Guidelines", content_after_install)
        self.assertIn("<!-- potetos-for-everyone:begin -->", content_after_install)

        potetos.uninstall(SimpleNamespace(target=str(self.temp_dir)))

        content_after_uninstall = agents_md.read_text(encoding="utf-8")
        self.assertIn("Existing User Project Guidelines", content_after_uninstall)
        self.assertNotIn("<!-- potetos-for-everyone:begin -->", content_after_uninstall)

    def test_update_refreshes_clean_install_and_refuses_local_edits(self):
        args = SimpleNamespace(
            target=str(self.temp_dir),
            agent="all",
            link=False,
            force=False,
            no_gitignore=False,
        )
        potetos.install(args)

        target_skill = self.temp_dir / ".agents" / "skills" / "poteto-mode" / "SKILL.md"
        target_skill.write_text("modified content", encoding="utf-8")

        update_args = SimpleNamespace(
            target=str(self.temp_dir),
            force=False,
            copy=False,
            link=False,
        )
        with self.assertRaises(SystemExit):
            potetos.update(update_args)

        update_force_args = SimpleNamespace(
            target=str(self.temp_dir),
            force=True,
            copy=False,
            link=False,
        )
        potetos.update(update_force_args)
        self.assertNotEqual(target_skill.read_text(encoding="utf-8"), "modified content")


if __name__ == "__main__":
    unittest.main()
