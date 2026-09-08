# Host adapters

The canonical skills always live in `.agents/skills/`. Adapters are intentionally tiny: they only add the instruction file a host is likely to discover and point it back to the same canonical Poteto Mode skill.

The one-line installer defaults to **all** supported shims so users do not have to know which path their agent expects. Use `POTETOS_AGENT=<name>` (bootstrap) or `--agent <name>` (CLI) to install only one specialized shim when repository minimalism matters more than instant cross-host use.

Supported names are defined in [`registry.json`](registry.json). If an agent is not listed, the generated `AGENTS.md` is the universal fallback for any host that reads repository instructions; otherwise point the host directly at `.agents/skills/poteto-mode/SKILL.md`.

Adapters must never fork behavior. A host-specific behavioral difference belongs in the portable capability contract or canonical skill, not in a second copy of a skill.
