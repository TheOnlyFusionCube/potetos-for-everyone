# Portable runner protocol

Hosts with native subagents should use them. When native delegation is missing, `potetos-for-everyone` can run arbitrary user-configured AI agent CLIs without knowing their vendor syntax.

Create `.potetos/config.json` from `config.example.json`. Each runner supplies an argv array. Supported placeholders are `{prompt}`, `{prompt_file}`, `{workspace}`, and `{output_file}`. Set `stdin: true` when the CLI accepts the prompt on stdin. Prefer `env_passthrough` for credential variable names; do not commit secret values into `environment`.

Run one worker:

```bash
./bin/potetos delegate --workspace . --runner default --prompt-file task.md
```

Run an independent panel:

```bash
./bin/potetos panel --workspace . --runners default,reviewer --prompt-file review.md
```

Add `--isolate` for code-writing workers. It refuses a dirty base (except `.potetos/` runtime state), creates a separate Git worktree and `potetos/<run-id>/<runner>` branch per worker, and leaves that worktree intact for review. Outputs and metadata are stored under `.potetos/runs/` by default.

The runner never invokes a shell implicitly: `command` is an argv array executed directly. Any program named there is explicitly user-configured and runs with the permissions of the current process.
