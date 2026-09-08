# Security policy

`potetos-for-everyone` can install repository instructions and can optionally launch external agent CLIs. Treat runner configuration and downloaded install scripts as code execution surfaces.

## Supported versions

Security fixes are applied to the latest release and `main`.

## Reporting a vulnerability

Prefer GitHub's **private vulnerability reporting** for this repository once it is published and that feature is enabled. If private reporting is unavailable, open a minimal issue requesting a private contact path and do **not** include exploit details, credentials, or sensitive logs in the public issue.

Please include the affected version/commit, platform, minimal reproduction, and expected security boundary.

## Runner safety

- Keep `.potetos/config.json` local and secret-free.
- Review any configured external agent command before using `delegate` or `panel`.
- Use `--isolate` when a worker should not share a mutable checkout.
- The host agent's own permissions and safety policy always remain authoritative.
## npm install behavior

The npm package has zero third-party runtime dependencies. Its `postinstall` hook performs only local filesystem setup inside the invoking project: it copies the bundled canonical skills, merges bounded instruction blocks, updates `.gitignore`, and writes `.potetos/install.json`. It does not contact external services. Set `POTETOS_SKIP_AUTO_INSTALL=1` or install with `--ignore-scripts` to disable automatic setup.

Modern npm does not provide dependency uninstall lifecycle hooks, so project cleanup is explicit: run `npx potetos uninstall` before `npm uninstall potetos-for-everyone`.
