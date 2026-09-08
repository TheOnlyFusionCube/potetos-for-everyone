# Contributing

The design rule is simple: **one canonical behavior tree, many thin adapters**.

- Put reusable workflow behavior in `skills/`.
- Use Agent Skills-compatible `SKILL.md` frontmatter (`name` and `description`).
- Describe optional host features through `PORTABILITY.md` capabilities.
- Do not paste a second copy of a skill into an agent-specific directory.
- Preserve Lauren Tan's pstack attribution and MIT notice.
- Add a regression test for installer, updater, runtime, or portability changes.
- Keep the zero-dependency install path working on macOS/Linux and PowerShell/Windows.
- Run `python3 scripts/verify.py` before opening a PR.

When syncing an upstream pstack idea, update `UPSTREAM.json` / `UPSTREAM_INVENTORY.json` and explain whether the port changes behavior or only maps a host primitive to a capability.

For release work, also run `python3 scripts/publish_check.py` on a clean tree and follow [PUBLISHING.md](PUBLISHING.md).
