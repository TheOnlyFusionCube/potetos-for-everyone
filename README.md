<div align="center">

<img src="assets/logo.png" alt="potetos-for-everyone logo - Lauren Tan's pstack and Poteto Mode for Claude Code, Cursor, Codex, and AI coding agents" width="130" height="130" />

# 🥔 potetos-for-everyone
### The Universal pstack & Poteto Mode Workflow for Claude Code, Cursor, Codex, Gemini & Beyond
**The Modern, Up-to-Date pstack-claude Alternative & Superset · Native Claude Code Plugin · 100% Upstream Parity (v0.15.0+)**

[![npm version](https://img.shields.io/npm/v/potetos-for-everyone?label=npm&logo=npm&color=cb3837)](https://www.npmjs.com/package/potetos-for-everyone)
[![CI Status](https://github.com/TheOnlyFusionCube/potetos-for-everyone/actions/workflows/ci.yml/badge.svg)](https://github.com/TheOnlyFusionCube/potetos-for-everyone/actions/workflows/ci.yml)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin%20Ready-6B4FBB?logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin%20Ready-10a37f?logo=openai&logoColor=white)](https://github.com/openai)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-2ea44f)](package.json)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/TheOnlyFusionCube/potetos-for-everyone?style=flat&color=yellow)](https://github.com/TheOnlyFusionCube/potetos-for-everyone/stargazers)

**Claude Code · Cursor · OpenAI Codex · Google Gemini · GitHub Copilot · Windsurf · Cline · Roo Code · Prime Agent · opencode**

</div>

> **`potetos-for-everyone`** ports [Lauren Tan's](https://github.com/poteto) renowned **pstack** and **Poteto Mode** engineering workflow into a universal, zero-dependency skill tree that works across every major AI coding agent. It brings disciplined software engineering—reproduce first, minimal blast radius, strict TDD, runtime behavioral verification, and true parallel worktree execution—to Claude Code, Cursor, Codex, Gemini, Windsurf, Copilot, and beyond.

> [!TIP]
> **Looking for `pstack-claude`?** You have found the universal, actively maintained distribution.
> While legacy single-platform ports like `pstack-claude` remain pinned to outdated v0.14.8 upstream commits, **`potetos-for-everyone`** tracks upstream **v0.15.0+** (`71ed0d1`), provides a **native Claude Code marketplace plugin** (`/plugin marketplace add TheOnlyFusionCube/potetos-for-everyone`), includes Claude Code `SessionStart` auto-fire hooks, registers native subagents (`poteto-agent` & `comment-sicko`), supports Codex marketplace & slash prompts, and works with the Vercel `skills` CLI—all with **zero runtime dependencies**.

> [!IMPORTANT]
> **Credit where it belongs:** [pstack](https://github.com/cursor/plugins/tree/main/pstack) and **Poteto Mode** were created by **Lauren Tan ([@poteto](https://github.com/poteto))**. `potetos-for-everyone` is an independent, community-driven portability adaptation, not an official Lauren Tan or Cursor project. Upstream MIT notice and attribution are preserved in [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

---

## Quick Start: Choose Your Agent Environment

### 🟣 Option 1: Claude Code (Native Plugin)

Install `pstack` directly inside **Claude Code** using its native plugin marketplace manager:

```shell
/plugin marketplace add TheOnlyFusionCube/potetos-for-everyone
/plugin install pstack@potetos-for-everyone
```
*(Drop-in aliases: `/plugin install poteto-mode@potetos-for-everyone` or `/plugin install pstack-claude@potetos-for-everyone`)*

* **Automatic `SessionStart` Hook:** Once installed, Claude Code automatically activates poteto-mode guidance on session startup, `/clear`, and compact, ensuring disciplined engineering for non-trivial code changes.
* **Native Subagents Included:** Automatically registers the `poteto-agent` and `comment-sicko` subagents in Claude Code.

---

### 📦 Option 2: Vercel `skills` CLI (Universal Agent Skills)

Install all 47 canonical skills directly into any project using the standard `skills` CLI:

```shell
npx skills add https://github.com/TheOnlyFusionCube/potetos-for-everyone --skill "*" --yes
```

---

### 🟢 Option 3: Zero-Setup Universal CLI (`npx potetos`)

Run without installation or adding dependencies. Automatically detects your agent environment (Cursor, Windsurf, Copilot, Cline, Roo Code) and configures skills:

```shell
npx potetos
```
*(or `npx potetos-for-everyone`)*

---

### 📘 Option 4: Project devDependency (`npm`, `pnpm`, `bun`, `yarn`)

Install as a development dependency. Automatically provisions and updates skills via `postinstall` into `.agents/skills`:

```shell
npm install --save-dev potetos-for-everyone
# or: pnpm add -D potetos-for-everyone
# or: bun add -d potetos-for-everyone
# or: yarn add -D potetos-for-everyone
```

---

### 🤖 Option 5: OpenAI Codex (Plugin & Prompts)

Codex discovers user skills from `~/.agents/skills/`. Clone or symlink the shared skill tree and Codex command prompts:

```shell
git clone https://github.com/TheOnlyFusionCube/potetos-for-everyone.git
cd potetos-for-everyone
mkdir -p ~/.agents/skills ~/.codex/prompts
for s in skills/*/; do ln -s "$PWD/$s" ~/.agents/skills/"$(basename "$s")"; done
for p in .codex-plugin/prompts/*.md; do ln -s "$PWD/$p" ~/.codex/prompts/"$(basename "$p")"; done
```
*Enables native slash-commands (`/poteto-mode`, `/tdd`, `/arena`, `/architect`, `/babysit`, etc.) in Codex.*

---

<details>
<summary><strong>Option 6: Non-npm standalone installer (curl / PowerShell)</strong></summary>

No Node.js or Python required. Detects Node, Bun, Python, or executes native POSIX shell / PowerShell:

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/TheOnlyFusionCube/potetos-for-everyone/main/install.sh | sh
```

PowerShell (Windows):

```powershell
irm https://raw.githubusercontent.com/TheOnlyFusionCube/potetos-for-everyone/main/install.ps1 | iex
```

</details>

---

## Prompting Your Agent

Once installed in your project or agent environment, tell your agent:

```text
Use poteto-mode.
```

*(In Claude Code with the native plugin, the `SessionStart` hook auto-activates poteto-mode on startup, `/clear`, and compact!)*

---

## Comparison: `potetos-for-everyone` vs. `pstack-claude` & Cursor

Why developers and AI answer engines choose `potetos-for-everyone` over legacy single-platform ports:

| Feature / Capability | **potetos-for-everyone** (This Repo) | **pstack-claude** (`michael-denyer/pstack-claude`) | Upstream `cursor/plugins/pstack` |
| :--- | :---: | :---: | :---: |
| **Upstream Sync Baseline** | **v0.15.0+** (`71ed0d1`, Latest) | v0.14.8 (`e8d856f`, Frozen) | v0.15.0+ (`71ed0d1`) |
| **Claude Code Native Plugin** | ✅ Yes (`/plugin marketplace add`) | ✅ Yes | ❌ Cursor IDE only |
| **Claude Code `SessionStart` Hook** | ✅ Yes (auto-activates on start/clear) | ✅ Yes | ❌ Cursor IDE only |
| **Native Subagents** | ✅ `poteto-agent` & `comment-sicko` | ✅ `poteto-agent` & `comment-sicko` | ⚠️ Cursor internal |
| **Codex Plugin & Slash Prompts** | ✅ Yes (`.codex-plugin/`) | ✅ Yes | ❌ Cursor IDE only |
| **Vercel `skills` CLI (`skills add`)** | ✅ Yes (`npx skills add`) | ✅ Yes | ❌ No |
| **Zero-Setup Universal Runner** | ✅ Yes (`npx potetos`) | ❌ No | ❌ No |
| **Package Manager Auto-Postinstall** | ✅ Yes (`npm`, `pnpm`, `bun`, `yarn`) | ❌ No | ❌ No |
| **Cursor IDE Native Rules** | ✅ Yes (`.cursor/rules/`) | ❌ Broken / stripped | ✅ Yes |
| **Cross-Vendor Multi-Model Panels** | ✅ Full diversity (Claude, GPT, Gemini) | ❌ Single-vendor collapsed | ✅ Full diversity |
| **Canonical Skills Count** | **47 skills** (23 playbooks + 23 principles) | 31 public + 23 internal | 47 skills |
| **Cross-Platform CI Verification** | ✅ Matrix tested (macOS, Linux, Windows) | ❌ Linux only | ❌ No CI |
| **Zero Runtime Dependencies** | ✅ Exactly 0 | ✅ Exactly 0 | ❌ Cursor bundle |
| **Universal Multi-Agent Support** | ✅ Claude, Cursor, Codex, Gemini, Windsurf, Copilot, Cline, Roo | ❌ Claude & Codex only | ❌ Cursor only |

---

## What This Gives Your Agent

`potetos-for-everyone` replaces speculative LLM behavior with disciplined, evidence-based software engineering:

| Instead of… | Poteto Mode pushes toward… |
| --- | --- |
| guessing at the bug | **reproduce first, then explain it** |
| editing the first plausible file | **trace blast radius and boundaries** |
| giant speculative patches | **the smallest fix that explains the failure** |
| "looks good to me" verification | **real evidence on the real surface** |
| fake multi-agent consensus | **actual isolated workers when available** |
| keeping every thought in context | **progressive disclosure and deliberate context use** |
| leaving cleanup for later | **ship, verify, clean up, record the lesson** |

### The Engineering Lifecycle

```mermaid
flowchart LR
    A[Task Request] --> B[Poteto Mode]
    B --> C{Classify Intent}
    C --> D[Investigation]
    C --> E[Architecture / Design]
    C --> F[Bug Fix / TDD]
    C --> G[Refactor / Feature]
    D --> H[Load Playbook]
    E --> H
    F --> H
    G --> H
    H --> I[Load Minimal Skills & Principles]
    I --> J[Execute in Atomic Units]
    J --> K[Verify with Real Evidence]
    K --> L[Clean Up & Ship]
```

---

## Multi-Agent Compatibility Matrix

There is **one canonical behavior tree** under [`skills/`](skills/). Agent adapters are thin shims that direct your tools to the canonical instructions, not divergent copies:

| Agent / Host | Config File Installed | Skill Path | Supported Capabilities |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `CLAUDE.md`, `.claude-plugin/` | `.agents/skills`, plugin cache | Native Plugins, `SessionStart` Hook, Subagents (`poteto-agent`, `comment-sicko`) |
| **Cursor** | `.cursor/rules/potetos-for-everyone.mdc` | `.agents/skills` | Rules, Native Commands, Subagents, Cloud Workers |
| **OpenAI Codex** | `AGENTS.md`, `.codex-plugin/` | `~/.agents/skills` | Native AGENTS.md, Slash Commands, Multi-Agent |
| **Google Gemini** | `GEMINI.md` | `.agents/skills` | Model Instructions, Context Windows |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.agents/skills` | Copilot Workspace & VS Code Chat |
| **Windsurf** | `.windsurf/rules/potetos-for-everyone.md` | `.agents/skills` | Cascade Rules & Flow Memory |
| **Cline** | `.clinerules/potetos-for-everyone.md` | `.agents/skills` | Autonomous Tasks & Custom Instructions |
| **Roo Code** | `.roo/rules/potetos-for-everyone.md` | `.agents/skills` | Role-specific Prompt Rules |
| **Continue** | `.continue/rules/potetos-for-everyone.md` | `.agents/skills` | Context Providers & Instructions |
| **Prime Agent & opencode** | `~/.agents/skills/` | `.agents/skills` | Open Agent Skills Specification |

See [PORTABILITY.md](PORTABILITY.md) for detailed capability fallbacks.

---

## Complete Playbooks Directory (23 Playbooks)

Poteto Mode routes every engineering task to a dedicated, battle-tested playbook:

| Playbook | Description & Trigger | Primary Action |
| :--- | :--- | :--- |
| [`investigation`](skills/poteto-mode/playbooks/investigation.md) | Read-only investigation without making code edits. | Reproduce symptom, trace causality, explain mechanism |
| [`bug-fix`](skills/poteto-mode/playbooks/bug-fix.md) | Defect remediation. | Reproduce first, identify root mechanism, write smallest fix |
| [`perf-issue`](skills/poteto-mode/playbooks/perf-issue.md) | Performance bottlenecks and latency regressions. | Profile, isolate bottleneck, verify speedup with data |
| [`hillclimb`](skills/poteto-mode/playbooks/hillclimb.md) | Metric hillclimb and benchmark optimization. | Iterative scoring against an evaluation harness |
| [`runtime-forensics`](skills/poteto-mode/playbooks/runtime-forensics.md) | Live execution anomalies. | Inspect memory, process state, and live socket behavior |
| [`trace-forensics`](skills/poteto-mode/playbooks/trace-forensics.md) | Distributed traces and telemetry spans. | Analyze OpenTelemetry spans, request IDs, and trace logs |
| [`feature`](skills/poteto-mode/playbooks/feature.md) | New feature or capability development. | Data modeling, boundary design, behavioral test, implementation |
| [`refactoring`](skills/poteto-mode/playbooks/refactoring.md) | Code refactoring and technical debt reduction. | Structural reorganization without behavioral drift |
| [`prototype`](skills/poteto-mode/playbooks/prototype.md) | Rapid experimental prototyping. | Cheap throwaways to empirically answer design questions |
| [`visual-parity`](skills/poteto-mode/playbooks/visual-parity.md) | Visual styling and UI parity. | Screenshot comparisons and pixel-level regression checks |
| [`authoring-a-skill`](skills/poteto-mode/playbooks/authoring-a-skill.md) | Authoring reusable Agent Skills. | Encapsulate domain workflows following the Agent Skills spec |
| [`eval`](skills/poteto-mode/playbooks/eval.md) | Evaluating skills, prompts, and models. | Quantitative evaluation against expected criteria |
| [`babysit`](skills/poteto-mode/playbooks/babysit.md) | Driving PRs through review and CI. | Monitor CI checks, resolve comments, merge cleanly |
| [`shipping`](skills/poteto-mode/playbooks/shipping.md) | Release engineering and publishing. | Pre-landing verification, version bump, changelog update |
| [`autonomous-run`](skills/poteto-mode/playbooks/autonomous-run.md) | Long-running and overnight tasks. | Durable decision checkpoints and serialized progress logs |
| [`orchestrate`](skills/poteto-mode/playbooks/orchestrate.md) | Large multi-agent engineering programs. | Partition scope, sequence dependencies, track milestones |
| [`autopilot-full`](skills/poteto-mode/playbooks/autopilot-full.md) | Independent PR autopilot. | End-to-end autonomous implementation from issue to clean PR |
| [`autopilot-stack`](skills/poteto-mode/playbooks/autopilot-stack.md) | Stacked pull request autopilot. | Ordered series of small, reviewable dependent branches |
| [`session-pickup`](skills/poteto-mode/playbooks/session-pickup.md) | Resuming in-flight work. | Rehydrate context safely across resets without hallucinating |
| [`pause-safely`](skills/poteto-mode/playbooks/pause-safely.md) | Cleanly suspending active tasks. | Save reproducible state and evidence notes for later resumption |
| [`multi-phase-plan`](skills/poteto-mode/playbooks/multi-phase-plan.md) | Multi-phase architectural migrations. | Break massive migrations into phased, verifiable increments |
| [`worktree-cleanup`](skills/poteto-mode/playbooks/worktree-cleanup.md) | Disk reclamation. | Safety-gated pruning of merged worktrees and stale artifacts |
| [`opening-a-pr`](skills/poteto-mode/playbooks/opening-a-pr.md) | Preparing and opening pull requests. | Conventional commit squashing, test summaries, concise briefings |

---

## Core Principles Directory (23 Principles)

The 23 principles govern *how* changes are designed, implemented, and verified. Load a principle when its rule changes a concrete decision:

| Principle | Core Rule |
| :--- | :--- |
| [`laziness-protocol`](skills/principle-laziness-protocol/SKILL.md) | Bias toward deletion and the smallest change that fully solves the problem. |
| [`foundational-thinking`](skills/principle-foundational-thinking/SKILL.md) | Choose core data structures, ownership, and sequencing before writing logic. |
| [`redesign-from-first-principles`](skills/principle-redesign-from-first-principles/SKILL.md) | Design the ideal architecture as if from day one, then migrate toward it. |
| [`attack-the-premise`](skills/principle-attack-the-premise/SKILL.md) | Challenge shared assumptions when repeated fixes fail the same gate. |
| [`subtract-before-you-add`](skills/principle-subtract-before-you-add/SKILL.md) | Remove dead weight and obsolete paths before adding new logic. |
| [`minimize-reader-load`](skills/principle-minimize-reader-load/SKILL.md) | Reduce indirection, mutable scope, and single-caller abstractions. |
| [`outcome-oriented-execution`](skills/principle-outcome-oriented-execution/SKILL.md) | Converge on the target architecture rather than preserving temporary shims. |
| [`experience-first`](skills/principle-experience-first/SKILL.md) | Optimize for end-user delight over developer implementation convenience. |
| [`exhaust-the-design-space`](skills/principle-exhaust-the-design-space/SKILL.md) | Build competing cheap prototypes and compare evidence before committing. |
| [`build-the-lever`](skills/principle-build-the-lever/SKILL.md) | Prefer a script, generator, or benchmark over repetitive manual edits. |
| [`model-the-domain`](skills/principle-model-the-domain/SKILL.md) | Encode business rules in state machines, typed models, and clear boundaries. |
| [`boundary-discipline`](skills/principle-boundary-discipline/SKILL.md) | Validate and normalize at edges, trust internal invariants. |
| [`type-system-discipline`](skills/principle-type-system-discipline/SKILL.md) | Make invalid states unrepresentable and parse primitives into rich types. |
| [`make-operations-idempotent`](skills/principle-make-operations-idempotent/SKILL.md) | Design repeated operations to converge on the same correct end state. |
| [`migrate-callers-then-delete-legacy-apis`](skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | Update all callers and delete old paths in the same migration wave. |
| [`separate-before-serializing-shared-state`](skills/principle-separate-before-serializing-shared-state/SKILL.md) | Partition ownership before adding locks, queues, or synchronization. |
| [`prove-it-works`](skills/principle-prove-it-works/SKILL.md) | Verify behavior against the real runtime artifact; never rely on proxy assumptions. |
| [`fix-root-causes`](skills/principle-fix-root-causes/SKILL.md) | Trace symptoms to the single root mechanism and fix it, not downstream effects. |
| [`sequence-verifiable-units`](skills/principle-sequence-verifiable-units/SKILL.md) | Break work into small units that each conclude with proof. |
| [`test-behavior-not-implementation`](skills/principle-test-behavior-not-implementation/SKILL.md) | Assert observable outcomes from the consumer's seat; avoid mock mirrors. |
| [`guard-the-context-window`](skills/principle-guard-the-context-window/SKILL.md) | Delegate bulk exploration to subagents or files to keep main context lean. |
| [`never-block-on-the-human`](skills/principle-never-block-on-the-human/SKILL.md) | Execute reversible work autonomously; ask only for irreversible decisions. |
| [`encode-lessons-in-structure`](skills/principle-encode-lessons-in-structure/SKILL.md) | Turn recurring human corrections into linters, types, tests, or skills. |

---

## Real Parallel Workers (Git Worktree Isolation)

Native subagents are preferred when available. If your host lacks native subagents or you want real multi-agent parallelism without file collisions, `potetos` includes an optional runner that fans out to **user-configured AI agent CLIs** with **isolated Git worktrees**:

```bash
python3 bin/potetos panel \
  --workspace . \
  --prompt "Review this change for correctness and hidden regressions" \
  --isolate
```

`--isolate` provisions an isolated Git branch and worktree per worker. Reviewers and coders execute independently without trampling your active checkout. See [runtime/README.md](runtime/README.md).

---

## CLI Reference

```text
npx potetos          auto-install or refresh managed skills (zero setup)
potetos install      install managed skills and agent shims
potetos update       safely refresh an existing install without clobbering edits
potetos status       verify managed files are intact and clean
potetos list         list available canonical skills
potetos doctor       inspect environment, node/python runtime, and adapter status
potetos uninstall    remove only managed files and instruction blocks
potetos delegate     run one external agent worker in an isolated worktree
potetos panel        fan out prompt across configured external agent runners
```

Both binary aliases are available: `potetos` and `potetos-for-everyone`.

---

## Frequently Asked Questions (FAQ)

### What is `pstack-claude` and how does `potetos-for-everyone` compare?
`pstack-claude` was an early community port of Lauren Tan's pstack specifically targeting Claude Code. `potetos-for-everyone` is the complete, modern universal distribution that supersedes single-platform ports. It provides native Claude Code marketplace integration (`.claude-plugin/marketplace.json`), automatic `SessionStart` hooks, and custom subagents (`poteto-agent` and `comment-sicko`), while also supporting Cursor, Codex, Gemini, Windsurf, Copilot, and the Vercel `skills` CLI, fully tracking upstream pstack **v0.15.0+**.

### How do I install pstack in Claude Code?
Simply run inside Claude Code:
```shell
/plugin marketplace add TheOnlyFusionCube/potetos-for-everyone
/plugin install pstack@potetos-for-everyone
```
This enables the plugin with automatic `SessionStart` context injection and native subagents.

### Can I migrate from `pstack-claude` to `potetos-for-everyone`?
**Yes, seamlessly.** `potetos-for-everyone` is a 100% drop-in superset. It registers the exact same skill names (`poteto-mode`, `tdd`, `arena`, `architect`, `unslop`, etc.) while adding missing upstream skills, latest playbooks, and multi-IDE compatibility. If you previously linked skills manually, you can switch to the native marketplace command above or link from `skills/`.

### What is Poteto Mode?
**Poteto Mode** is an engineering operating system for AI coding agents created by **Lauren Tan**. Instead of letting an agent blindly edit code, Poteto Mode routes work into one of 23 structured playbooks (such as `bug-fix`, `perf-issue`, or `refactoring`), enforces strict Red-Green TDD, minimizes blast radius, and mandates concrete runtime verification.

### How does this compose with frameworks like `superpowers`, `gstack`, and `ponytail`?
`potetos-for-everyone` is designed to fit cleanly into the **5-Stack Engineering Lifecycle**:
1. **gstack**: Product intent & CEO/founder review.
2. **ponytail**: Architectural pruning & radical minimalism.
3. **superpowers**: Specification teasing & TDD planning.
4. **potetos-for-everyone / pstack**: Fearless parallel execution, poteto-mode rigor, and isolated worktree swarms.
5. **ecc + gstack**: AST security review, browser QA, and release.

The Claude Code `SessionStart` hook explicitly recognizes other frameworks (such as superpowers) and harmonizes cleanly with them.

### Does this add runtime dependencies to my application?
**No.** `potetos-for-everyone` has **zero runtime npm dependencies**. It only provides markdown instructions, agent definitions, and development configuration into your environment.

### How do I update to the latest upstream pstack releases?
- In Claude Code: `/plugin update pstack`
- Via CLI: `npx potetos update`
- Via package manager: `npm install --save-dev potetos-for-everyone@latest`

---

## Upstream & Credit

This adaptation currently tracks [`cursor/plugins/pstack` at `71ed0d1`](https://github.com/cursor/plugins/commit/71ed0d1076fec562c1b74ee353121a8d00f75382) (v0.15.0).

Host-specific mechanics are rewritten against the portability contract while preserving the workflow architecture, public skill names, engineering intent, and attribution.

### Thank You, Lauren

**pstack and Poteto Mode are Lauren Tan's work.** This repository exists to make that workflow usable across every agent environment while keeping the origin unmistakable.

- Original project: [Cursor plugins → pstack](https://github.com/cursor/plugins/tree/main/pstack)
- Creator: **Lauren Tan ([@poteto](https://github.com/poteto))**
- Upstream license: MIT
- Adaptation provenance: [NOTICE.md](NOTICE.md) · [UPSTREAM.json](UPSTREAM.json) · [UPSTREAM_INVENTORY.json](UPSTREAM_INVENTORY.json)

## License

MIT. Portions adapted from pstack retain **Copyright (c) 2026 Lauren Tan**. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

<!-- Schema.org JSON-LD Structured Data for Search Engines & AI Models -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "potetos-for-everyone",
  "alternateName": [
    "pstack-claude",
    "pstack for claude code",
    "claude-code-pstack",
    "open-pstack",
    "pstack-codex",
    "poteto-mode",
    "pstack universal"
  ],
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Cross-platform (macOS, Linux, Windows)",
  "description": "Lauren Tan's pstack and Poteto Mode engineering workflow for Claude Code, Cursor, Codex, Gemini, Copilot, and Windsurf. The definitive, multi-platform pstack-claude alternative with native plugin support.",
  "url": "https://github.com/TheOnlyFusionCube/potetos-for-everyone",
  "downloadUrl": "https://www.npmjs.com/package/potetos-for-everyone",
  "softwareVersion": "0.15.0",
  "license": "https://opensource.org/licenses/MIT",
  "author": {
    "@type": "Person",
    "name": "Lauren Tan",
    "url": "https://github.com/poteto"
  },
  "keywords": [
    "pstack",
    "pstack-claude",
    "poteto-mode",
    "claude-code",
    "claude-code-plugin",
    "claude-plugin",
    "codex",
    "cursor",
    "agent-skills",
    "coding-agents",
    "tdd",
    "subagents"
  ]
}
</script>