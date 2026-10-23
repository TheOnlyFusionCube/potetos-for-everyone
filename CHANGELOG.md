# Changelog

All notable changes to `potetos-for-everyone` will be documented here.

## 0.1.0 - Unreleased

### Added

- Import ten additional upstream pstack v0.15.30 skills and associated help/statechart resources, expanding the portable catalog from 47 to 57 skills (33 workflow skills and 24 principles).
- Pin the upstream snapshot to 4ec7ffa and update the inventory and npm skill-count tests. Existing adaptations are not yet fully reconciled with upstream changes.

- Claude Code on-demand activation via `POTETOS_AUTO_ACTIVATE=0`, preserving automatic activation by default and access to plugin skills and commands.
- Portable adaptation of Lauren Tan's pstack with 47 canonical skills and 23 Poteto Mode playbooks.
- Synced with upstream cursor/plugins/pstack at 71ed0d1 (23 playbooks, 23 principles).
- Enhanced CLI and bootstrap installers with zero-friction defaults (npx auto-install/update without subcommands, cross-runtime runner fallback for node, bun, python, and shell).
- Thin compatibility shims for major AI coding-agent hosts.
- Zero-dependency installer, safe updater, uninstaller, status, doctor, and external-agent runner.
- One-line macOS/Linux and PowerShell bootstrap installers.
- Zero-dependency npm package with local auto-setup, global/npx CLI entry points, and a pure Node core installer.
- Trusted-publishing-ready npm release automation with package/provenance checks.
- Cross-platform CI, release automation, issue templates, and publish checks.
- Explicit upstream attribution, provenance tracking, and MIT license preservation.
