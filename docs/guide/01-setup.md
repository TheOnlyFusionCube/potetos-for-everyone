# 1. Setup

The lowest-friction install is from the target repository itself:

```bash
curl -fsSL https://raw.githubusercontent.com/TheOnlyFusionCube/potetos-for-everyone/main/install.sh | sh
```

PowerShell:

```powershell
irm https://raw.githubusercontent.com/TheOnlyFusionCube/potetos-for-everyone/main/install.ps1 | iex
```

The default copies the canonical skills into `.agents/skills/` and writes all supported tiny instruction shims, preserving any content already in those files. This makes the result self-contained and usable by different agents without reinstalling.

If you are developing `potetos-for-everyone` itself from a local clone, use links instead:

```bash
python3 /path/to/potetos-for-everyone/bin/potetos install --target /path/to/project --link --agent universal
```

Re-running the one-line installer updates a clean managed install. It refuses to overwrite locally edited managed skills unless explicitly forced.

After installation, ask the host to **use `poteto-mode`** on a small real task. If native skill discovery is unavailable, the generated instruction shim points directly to `.agents/skills/poteto-mode/SKILL.md`.
