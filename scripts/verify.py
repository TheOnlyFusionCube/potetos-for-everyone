#!/usr/bin/env python3
from __future__ import annotations

import compileall
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    run(sys.executable, "scripts/lint_skills.py")

    # Keep the default verifier fast and reliable while still covering each
    # safety-critical boundary. CI also runs the full discovered test suite.
    critical_tests = [
        "tests.test_install.InstallTests.test_default_install_is_self_contained_and_all_agent",
        "tests.test_install.InstallTests.test_install_and_uninstall_preserve_existing_content",
        "tests.test_install.InstallTests.test_update_refreshes_clean_install_and_refuses_local_edits",
        "tests.test_runtime.RuntimeTests.test_isolated_delegate_gets_separate_git_worktree",
    ]
    for test_id in critical_tests:
        run(sys.executable, "-m", "unittest", "-v", test_id)

    if not shutil.which("node"):
        raise SystemExit("Node.js 18+ is required to verify the npm distribution")
    run("node", "scripts/check_npm_package.mjs")

    if not compileall.compile_file(str(ROOT / "bin" / "potetos"), quiet=1, force=True):
        raise SystemExit("failed to compile bin/potetos")
    for folder in (ROOT / "tests", ROOT / "scripts", ROOT / "runtime"):
        if not compileall.compile_dir(str(folder), quiet=1, force=True):
            raise SystemExit(f"failed to compile {folder}")
    for cache in ROOT.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)
    print("verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
