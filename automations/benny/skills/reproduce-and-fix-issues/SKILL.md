---
name: reproduce-and-fix-issues
description: Reproduce a confirmed issue on the closest real surface, find root cause, and optionally prepare a minimal draft fix with evidence. Use after issue triage has enough information to attempt reproduction.
---
# Reproduce and fix issues

1. Work in an isolated branch/worktree/sandbox when the host can provide one.
2. Reproduce the exact reported behavior and save the smallest durable evidence.
3. If reproduction fails, vary only evidence-backed environment assumptions; return the blocker instead of guessing.
4. Trace root cause. If a cheap behavioral regression test exists, see it fail for the same reason.
5. Make the smallest fix that explains the reproduction, then rerun the reproduction and targeted checks.
6. Prepare a draft change/PR only when authorized. Post status back to the source thread/ticket with proof and remaining uncertainty.
