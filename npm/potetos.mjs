#!/usr/bin/env node
import childProcess from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { PACKAGE_ROOT, doctor, install, listSkills, status, uninstall, update } from "./core.mjs";

function fail(message, code = 2) {
  console.error(`potetos: ${message}`);
  process.exit(code);
}

function parse(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith("--")) { out._.push(arg); continue; }
    const key = arg.slice(2);
    if (["force", "no-gitignore", "copy", "link", "help", "version"].includes(key)) out[key] = true;
    else {
      if (i + 1 >= argv.length) fail(`missing value for --${key}`);
      out[key] = argv[++i];
    }
  }
  return out;
}

function help() {
  console.log(`potetos-for-everyone

Usage:
  npx potetos                     # auto-installs or updates in current repo
  potetos install [--target .] [--agent all] [--force]
  potetos update [--target .] [--force]
  potetos status [--target .]
  potetos uninstall [--target .]
  potetos list
  potetos doctor [--target .]
  potetos delegate ...            # forwards to bundled Python runner
  potetos panel ...               # forwards to bundled Python runner

Package manager zero-config install:
  npm install --save-dev potetos-for-everyone
  pnpm add -D potetos-for-everyone
  bun add -d potetos-for-everyone
  yarn add -D potetos-for-everyone

Local npm installs auto-install/update the skills. Set POTETOS_SKIP_AUTO_INSTALL=1 to disable that lifecycle behavior.`);
}

function printInstall(result, verb = "installed") {
  console.log(`${verb} ${result.installed} skills in ${result.target}`);
  console.log(`compatibility: ${result.agent} (${result.agents.join(", ")})`);
  console.log(`mode: copy`);
  console.log(`skills: ${result.skills}`);
  console.log("ready: ask your agent to use poteto-mode");
}

function forwardPython(command, rest) {
  const script = path.join(PACKAGE_ROOT, "bin", "potetos");
  const candidates = process.platform === "win32" ? [["py", ["-3"]], ["python", []], ["python3", []]] : [["python3", []], ["python", []]];
  for (const [exe, prefix] of candidates) {
    const probe = childProcess.spawnSync(exe, [...prefix, "--version"], { stdio: "ignore" });
    if (!probe.error && probe.status === 0) {
      const run = childProcess.spawnSync(exe, [...prefix, script, command, ...rest], { stdio: "inherit" });
      process.exit(run.status ?? 1);
    }
  }
  fail(`${command} needs Python 3.10+ for the external-agent runner. Core install/update/status/uninstall commands do not require Python.`);
}

const argv = process.argv.slice(2);

if (argv.includes("--help") || argv.includes("-h") || argv[0] === "help") {
  help();
  process.exit(0);
}

if (argv.includes("--version") || argv.includes("-v") || argv[0] === "version") {
  const { packageVersion } = await import("./core.mjs");
  console.log(packageVersion());
  process.exit(0);
}

let command = argv[0];
if (!command || command.startsWith("--")) {
  command = "auto";
} else {
  command = argv.shift();
}

if (["delegate", "panel"].includes(command)) forwardPython(command, argv);

const args = parse(argv);
const target = args.target || ".";
if (args.link) fail("the npm CLI installs self-contained copies only; use a source checkout with the Python CLI for development symlinks");
try {
  switch (command) {
    case "auto": {
      const manifestPath = path.join(path.resolve(target), ".potetos", "install.json");
      if (fs.existsSync(manifestPath)) {
        printInstall(update({ target, force: !!args.force }), "updated");
      } else {
        printInstall(install({ target, agent: args.agent || "all", force: !!args.force, manageGitignore: !args["no-gitignore"] }));
      }
      break;
    }
    case "install":
      printInstall(install({ target, agent: args.agent || "all", force: !!args.force, manageGitignore: !args["no-gitignore"] }));
      break;
    case "update":
      printInstall(update({ target, force: !!args.force }), "updated");
      break;
    case "uninstall": {
      const result = uninstall({ target });
      console.log(`uninstalled potetos-for-everyone from ${result.target}`);
      break;
    }
    case "status": {
      const state = status({ target });
      if (!state.installed) fail(`not installed in ${state.target}`, 1);
      console.log(`installed: ${state.count} skills`);
      console.log(`compatibility: ${state.agent}`);
      console.log(`mode: ${state.mode}`);
      if (state.packageVersion) console.log(`package: ${state.packageVersion}`);
      if (!state.clean) {
        console.log(`state: modified (${state.modified.length} managed paths differ)`);
        for (const rel of state.modified.slice(0, 10)) console.log(`  ${rel}`);
        process.exit(1);
      }
      console.log("state: clean");
      break;
    }
    case "list":
      for (const name of listSkills()) console.log(name);
      break;
    case "doctor":
      console.log(JSON.stringify(doctor({ target }), null, 2));
      break;
    default:
      fail(`unknown command ${JSON.stringify(command)}; run potetos --help`);
  }
} catch (err) {
  fail(err?.message || String(err));
}
