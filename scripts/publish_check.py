#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPO = "TheOnlyFusionCube/potetos-for-everyone"
EXPECTED_PACKAGE = "potetos-for-everyone"
REQUIRED = [
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "VERSION",
    "package.json",
    "package-lock.json",
    "npm/core.mjs",
    "npm/potetos.mjs",
    "npm/postinstall.mjs",
    "scripts/check_npm_package.mjs",
    "install.sh",
    "install.ps1",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/portability.yml",
]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing publish file: {rel}", errors)

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"VERSION is not semver: {version!r}", errors)

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8")) if (ROOT / "package.json").exists() else {}
    if package.get("name") != EXPECTED_PACKAGE:
        fail(f"package.json name must be {EXPECTED_PACKAGE!r}", errors)
    if package.get("version") != version:
        fail(f"package.json version {package.get('version')!r} != VERSION {version!r}", errors)
    if package.get("license") != "MIT":
        fail("package.json license must be MIT", errors)
    if package.get("repository", {}).get("url", "").lower().find(EXPECTED_REPO.lower()) < 0:
        fail("package.json repository does not point at expected GitHub repo", errors)
    bins = package.get("bin", {})
    if not {"potetos", "potetos-for-everyone"}.issubset(bins):
        fail("package.json must expose potetos and potetos-for-everyone binaries", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for needle in (EXPECTED_REPO, "Lauren Tan", "pstack", "npm install", EXPECTED_PACKAGE, "install.sh", "install.ps1"):
        if needle not in readme:
            fail(f"README missing publish marker: {needle}", errors)

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
    if "Copyright (c) 2026 Lauren Tan" not in license_text:
        fail("LICENSE does not preserve Lauren Tan copyright", errors)

    upstream = json.loads((ROOT / "UPSTREAM.json").read_text(encoding="utf-8"))
    if not upstream:
        fail("UPSTREAM.json is empty", errors)

    release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    for needle in ("id-token: write", "npm publish", "actions/setup-node@v6"):
        if needle not in release:
            fail(f"release workflow missing npm publish marker: {needle}", errors)

    if not shutil.which("node") or not shutil.which("npm"):
        fail("node and npm are required for publish checks", errors)
    else:
        check = subprocess.run(["node", "scripts/check_npm_package.mjs"], cwd=ROOT, text=True, capture_output=True)
        if check.returncode:
            fail("npm package check failed:\n" + check.stdout + check.stderr, errors)
        pack = subprocess.run(["npm", "pack", "--dry-run", "--ignore-scripts"], cwd=ROOT, text=True, capture_output=True)
        if pack.returncode:
            fail("npm pack dry-run failed:\n" + pack.stdout + pack.stderr, errors)

    if not args.allow_dirty:
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True
        ).stdout.strip()
        if status:
            fail("git worktree is dirty", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"publish check: PASS (v{version}, {EXPECTED_REPO}, npm:{EXPECTED_PACKAGE})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
