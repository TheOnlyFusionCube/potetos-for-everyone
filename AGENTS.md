# potetos-for-everyone agent bootstrap

This repository contains a portable engineering skill stack adapted from Lauren Tan's pstack.

When working in this repository:

1. Treat `skills/` as canonical. Never fork behavioral instructions into an adapter.
2. For non-trivial work, read `skills/poteto-mode/SKILL.md`, select its matching playbook, and follow the referenced leaf skills only as needed.
3. Interpret capability names via `PORTABILITY.md`. Feature-detect host tools instead of assuming a vendor API.
4. Preserve the Lauren Tan attribution in `NOTICE.md` and `LICENSE`.
5. Run `./scripts/verify` before declaring repository changes complete.
