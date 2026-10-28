# Portability contract

The canonical `skills/` tree is runtime-neutral. A skill asks for a capability, not a product API.

## Capabilities

| Capability | Meaning | Required fallback |
|---|---|---|
| `files.read` | Read repository/workspace content | Ask for supplied context only when nothing readable exists |
| `files.write` | Make workspace edits | Return an exact patch/draft when writes are unavailable |
| `run` | Execute commands, tests, profilers, or scripts | State that runtime proof is unavailable; do not claim success |
| `vcs` | Inspect diff/history/branches/PR state | Use available repository files; label missing history explicitly |
| `delegate` | Spawn isolated workers/subagents | Run sequential passes; label them non-independent |
| `search` | Query web, docs, issues, chat, observability, analytics | Use only available evidence and report the gap |
| `observe` | Drive/inspect the real UI, service, device, CLI, or artifact | Use the closest artifact only as a proxy and label it |
| `track` | Maintain todos/decision logs/checkpoints | Write a small repo-local Markdown/TSV log when writes exist |

## Rules

1. Do not name a vendor-specific tool in canonical workflow instructions unless the vendor itself is the subject of the task.
2. Feature-detect. Never assume subagents, a browser, a PR API, MCP, memory, or a particular model exists.
3. A fallback must preserve epistemic honesty. Sequential role-play is not independent review. A compile is not runtime proof. A screenshot description is not pixel comparison.
4. Prefer the open Agent Skills package shape: `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`.
5. Keep model routing in `.potetos/config.json`, outside canonical skill logic.
6. Irreversible or externally consequential actions remain safety-gated by the host agent's own policy and permissions.

## Host adapters

Adapters do only two things: expose skill discovery and tell a host how to invoke the canonical files. They must not fork skill behavior. If an adapter needs different behavior, change the capability contract or the canonical skill instead.

## Kiro native Agent Skills

Kiro discovers workspace skills under `.kiro/skills/<skill-name>/SKILL.md` and can activate them on demand or by slash command. Run `npx potetos install --agent kiro` (or `python3 bin/potetos install --agent kiro`) in the target workspace. This installs all 57 canonical skills into Kiro's discovery directory; it also adds a small marked `AGENTS.md` routing hint, not full always-on skill instructions.

The default `--agent all` keeps `.agents/skills` for existing hosts and installs additional copies under `.kiro/skills` for Kiro. Both are generated from the same source `skills/`; **no divergent canonical instructions are maintained**. Copies are intentionally self-contained (including on platforms without working symlinks), so multiple discovery directories occupy additional disk space. The Python `--link` development mode links each selected destination back to the canonical source checkout.

Run `potetos status`, `potetos update`, or `potetos uninstall` for managed lifecycle operations. Checksums cover both discovery locations; updates and uninstalls refuse edited skills unless `--force` is explicitly selected. User-owned skills in either directory are left alone. During migration from an older installation, an unrelated conflicting native Kiro skill blocks update rather than being overwritten.

The repository tests assert the file layout, manifests, lifecycle safeguards, and default multi-agent installation. They **do not** test actual Kiro IDE or CLI runtime discovery, automatic activation, or slash-command invocation. For end-to-end assurance, open a freshly installed workspace in Kiro and check those behaviors in a running Kiro environment.

Kiro documentation: https://kiro.dev/docs/cli/skills/
