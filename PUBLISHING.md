# Publishing

The repository is prepared for publication as:

- **GitHub repository:** `TheOnlyFusionCube/potetos-for-everyone`
- **npm package:** `potetos-for-everyone`
- **Visibility:** public
- **Description:** `Lauren Tan's pstack engineering workflow, made portable across AI coding agents.`
- **License:** MIT, preserving Lauren Tan's original 2026 copyright notice
- **Default branch:** `main`
- **Suggested topics:** `pstack`, `agent-skills`, `ai-agents`, `coding-agents`, `cursor`, `claude-code`, `codex`, `developer-tools`

## Pre-publish

From the repository root:

```bash
python3 scripts/verify.py
python3 scripts/publish_check.py
npm pack --dry-run --ignore-scripts
```

All must pass on a clean worktree. `package.json` and `VERSION` must match exactly.

## Create and push GitHub

If `gh` is authenticated as `TheOnlyFusionCube` and the remote repository does not exist yet:

```bash
gh repo create TheOnlyFusionCube/potetos-for-everyone \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Lauren Tan's pstack engineering workflow, made portable across AI coding agents."
```

Then set discoverability metadata:

```bash
gh repo edit TheOnlyFusionCube/potetos-for-everyone \
  --add-topic pstack \
  --add-topic agent-skills \
  --add-topic ai-agents \
  --add-topic coding-agents \
  --add-topic cursor \
  --add-topic claude-code \
  --add-topic codex \
  --add-topic developer-tools
```

Recommended repository settings after creation:

- enable Issues;
- enable private vulnerability reporting;
- allow GitHub Actions to create releases;
- protect `main` after the initial push with CI required;
- keep squash merge enabled; optionally disable other merge styles if you want one canonical history style.

## First npm publication

`potetos-for-everyone` is an **unscoped public package**. Before publishing, confirm the name is still available:

```bash
npm view potetos-for-everyone
```

If npm returns `E404`, the name is unclaimed at that moment. Log in with the npm account that should own the package and publish the first version from the clean `main` commit:

```bash
npm login
npm publish --access public
```

The package is zero-dependency and `prepack` validates its name, version, CLI entry points, bundled Poteto Mode files, and Lauren Tan attribution before npm creates the tarball.

### Configure tokenless GitHub Actions publishing

After the package exists on npm, configure a **Trusted Publisher** for it. Current npm guidance recommends OIDC trusted publishing instead of long-lived publish tokens. Configure:

- provider: **GitHub Actions**;
- GitHub user/org: `TheOnlyFusionCube`;
- repository: `potetos-for-everyone`;
- workflow filename: `release.yml`;
- allowed action: **npm publish**.

The release workflow already grants `id-token: write`, uses Node 24, and runs `npm publish` with no npm token. Trusted publishing automatically attaches npm provenance for a public package from a public GitHub repository.

With npm CLI 11.5.1+ you can also create the trust relationship from the command line after the package exists:

```bash
npm trust github potetos-for-everyone \
  --file release.yml \
  --repo TheOnlyFusionCube/potetos-for-everyone \
  --allow-publish \
  --yes
```

## First GitHub release

After CI is green, npm ownership/trusted publishing is configured, and `CHANGELOG.md` is ready, change `Unreleased` to the release date, commit, then:

```bash
git tag -a v0.1.0 -m "potetos-for-everyone v0.1.0"
git push origin v0.1.0
```

The tag workflow validates the repo and package, creates GitHub `.zip` / `.tar.gz` source archives, creates the GitHub Release, and publishes the same version to npm through OIDC. If that version was manually published already (as is typical for the first npm release), the npm job detects it and skips the duplicate publish.

## Post-publish smoke tests

Test the normal npm path from an unrelated repository:

```bash
mkdir /tmp/potetos-smoke && cd /tmp/potetos-smoke
npm init -y
npm install --save-dev potetos-for-everyone
test -f .agents/skills/poteto-mode/SKILL.md
npx potetos status
```

Test the global CLI path:

```bash
npm install --global potetos-for-everyone
potetos --version
```

Then clean the generated project files explicitly before removing the local package:

```bash
npx potetos uninstall
npm uninstall potetos-for-everyone
```

The standalone curl/PowerShell bootstraps remain a fallback for environments without Node/npm.
