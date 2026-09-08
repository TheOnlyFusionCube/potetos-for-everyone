from __future__ import annotations

import concurrent.futures
import datetime as dt
import json
import os
import re
import secrets
import subprocess
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class RunResult:
    runner: str
    returncode: int
    stdout_file: str
    stderr_file: str
    workspace: str
    branch: str | None
    command: list[str]
    timed_out: bool = False


def _slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value[:48] or "worker"


def _run_id() -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{secrets.token_hex(3)}"


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"runner config not found: {path}. Run setup-pstack or create .potetos/config.json."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    runners = data.get("runners")
    if not isinstance(runners, dict) or not runners:
        raise ValueError("config must contain a non-empty 'runners' object")
    for name, spec in runners.items():
        if not isinstance(spec, dict):
            raise ValueError(f"runner {name!r} must be an object")
        cmd = spec.get("command")
        if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) and x for x in cmd):
            raise ValueError(f"runner {name!r}.command must be a non-empty string array")
        if "environment" in spec and not isinstance(spec["environment"], dict):
            raise ValueError(f"runner {name!r}.environment must be an object")
        if "env_passthrough" in spec and (not isinstance(spec["env_passthrough"], list) or not all(isinstance(x, str) for x in spec["env_passthrough"])):
            raise ValueError(f"runner {name!r}.env_passthrough must be a string array")
    return data


def _git_root(workspace: Path) -> Path:
    p = subprocess.run(
        ["git", "-C", str(workspace), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
    )
    if p.returncode:
        raise RuntimeError(f"--isolate requires a git worktree: {p.stderr.strip()}")
    return Path(p.stdout.strip()).resolve()


def _isolated_worktree(workspace: Path, run_id: str, runner: str) -> tuple[Path, str]:
    root = _git_root(workspace)
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    dirty = []
    for line in status:
        path = line[3:] if len(line) > 3 else line
        if path == ".potetos" or path.startswith(".potetos/"):
            continue
        dirty.append(line)
    if dirty:
        raise RuntimeError(
            "--isolate refuses a dirty base because a new worktree would silently omit uncommitted changes: "
            + "; ".join(dirty[:8])
        )
    parent = Path(tempfile.gettempdir()) / "potetos-worktrees" / _slug(root.name)
    parent.mkdir(parents=True, exist_ok=True)
    dest = parent / f"{run_id}-{_slug(runner)}"
    branch = f"potetos/{run_id}/{_slug(runner)}"
    p = subprocess.run(
        ["git", "-C", str(root), "worktree", "add", "-b", branch, str(dest), "HEAD"],
        text=True,
        capture_output=True,
    )
    if p.returncode:
        raise RuntimeError(f"failed to create isolated worktree: {p.stderr.strip()}")
    return dest, branch


def _render_command(parts: list[str], *, prompt: str, prompt_file: Path, workspace: Path, output_file: Path) -> list[str]:
    values = {
        "prompt": prompt,
        "prompt_file": str(prompt_file),
        "workspace": str(workspace),
        "output_file": str(output_file),
    }
    rendered = []
    for part in parts:
        try:
            rendered.append(part.format_map(values))
        except KeyError as e:
            raise ValueError(f"unknown runner command placeholder: {e.args[0]}") from e
    return rendered


def run_worker(
    *,
    config: dict[str, Any],
    runner: str,
    prompt: str,
    workspace: Path,
    runs_dir: Path,
    run_id: str | None = None,
    isolate: bool = False,
) -> RunResult:
    run_id = run_id or _run_id()
    runners = config["runners"]
    if runner not in runners:
        raise KeyError(f"runner {runner!r} not configured; available: {', '.join(sorted(runners))}")
    spec = runners[runner]

    branch = None
    actual_workspace = workspace.resolve()
    if isolate:
        actual_workspace, branch = _isolated_worktree(actual_workspace, run_id, runner)

    outdir = runs_dir.resolve() / run_id / _slug(runner)
    outdir.mkdir(parents=True, exist_ok=True)
    prompt_file = outdir / "prompt.txt"
    stdout_file = outdir / "stdout.txt"
    stderr_file = outdir / "stderr.txt"
    result_file = outdir / "result.json"
    prompt_file.write_text(prompt, encoding="utf-8")

    command = _render_command(
        spec["command"],
        prompt=prompt,
        prompt_file=prompt_file,
        workspace=actual_workspace,
        output_file=stdout_file,
    )
    env = os.environ.copy()
    env.update({str(k): str(v) for k, v in spec.get("environment", {}).items()})
    for key in spec.get("env_passthrough", []):
        if key not in os.environ:
            raise ValueError(f"runner {runner!r} requires missing environment variable {key}")
        env[key] = os.environ[key]
    timeout = int(spec.get("timeout_seconds", 1800))
    stdin_text = prompt if spec.get("stdin", False) else None

    timed_out = False
    try:
        p = subprocess.run(
            command,
            cwd=actual_workspace,
            input=stdin_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
        returncode = p.returncode
        stdout = p.stdout
        stderr = p.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        returncode = 124
        stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        stderr += f"\npotetos: runner timed out after {timeout}s\n"

    stdout_file.write_text(stdout, encoding="utf-8")
    stderr_file.write_text(stderr, encoding="utf-8")
    result = RunResult(
        runner=runner,
        returncode=returncode,
        stdout_file=str(stdout_file),
        stderr_file=str(stderr_file),
        workspace=str(actual_workspace),
        branch=branch,
        command=command,
        timed_out=timed_out,
    )
    result_file.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
    return result


def run_panel(
    *,
    config: dict[str, Any],
    runner_names: list[str],
    prompt: str,
    workspace: Path,
    runs_dir: Path,
    isolate: bool = False,
    max_parallel: int | None = None,
) -> tuple[str, list[RunResult]]:
    run_id = _run_id()
    names = runner_names or list(config["runners"])
    if not names:
        raise ValueError("panel requires at least one runner")
    if len(set(names)) != len(names):
        raise ValueError("panel runner names must be unique so evidence remains attributable")
    parallel = max_parallel or min(len(names), int(config.get("max_parallel", 4)))
    results: list[RunResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
        futures = {
            pool.submit(
                run_worker,
                config=config,
                runner=name,
                prompt=prompt,
                workspace=workspace,
                runs_dir=runs_dir,
                run_id=run_id,
                isolate=isolate,
            ): name
            for name in names
        }
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda r: names.index(r.runner))
    summary = runs_dir.resolve() / run_id / "panel.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps([asdict(r) for r in results], indent=2) + "\n", encoding="utf-8")
    return run_id, results
