import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const PACKAGE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const MANIFEST = ".potetos/install.json";
export const BEGIN = "<!-- potetos-for-everyone:begin -->";
export const END = "<!-- potetos-for-everyone:end -->";
export const GITIGNORE_BEGIN = "# potetos-for-everyone:begin";
export const GITIGNORE_END = "# potetos-for-everyone:end";

const BLOCK = `${BEGIN}\n## potetos-for-everyone\n\nFor non-trivial engineering work, use the Agent Skill at \`.agents/skills/poteto-mode/SKILL.md\`.\nIt routes the task to a playbook, loads supporting skills progressively, prefers simple changes,\nand requires evidence against the real artifact. Canonical skills are adapted from Lauren Tan's pstack.\nIf native skill discovery is unavailable, read that SKILL.md and its selected playbook manually.\n${END}`;
const GITIGNORE_BLOCK = `${GITIGNORE_BEGIN}\n.potetos/\n${GITIGNORE_END}`;

export function registry() {
  return JSON.parse(fs.readFileSync(path.join(PACKAGE_ROOT, "adapters", "registry.json"), "utf8"));
}

function die(message) {
  const err = new Error(message);
  err.isPotetos = true;
  throw err;
}

function readText(file) {
  return fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
}

function mergeMarkedBlock(file, begin, end, block) {
  const old = readText(file);
  let next;
  if (old.includes(begin) && old.includes(end)) {
    const start = old.indexOf(begin);
    const finish = old.indexOf(end, start) + end.length;
    const pre = old.slice(0, start).replace(/\s+$/, "");
    const post = old.slice(finish);
    next = pre + (pre.trim() ? "\n\n" : "") + block + post;
  } else {
    next = old.replace(/\s+$/, "") + (old.trim() ? "\n\n" : "") + block + "\n";
  }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, next, "utf8");
}

function removeMarkedBlock(file, begin, end) {
  if (!fs.existsSync(file)) return;
  const old = fs.readFileSync(file, "utf8");
  const start = old.indexOf(begin);
  if (start < 0) return;
  const endStart = old.indexOf(end, start);
  if (endStart < 0) return;
  const finish = endStart + end.length;
  const pre = old.slice(0, start).replace(/\s+$/, "");
  const post = old.slice(finish).replace(/^\s+/, "");
  const next = (pre + (pre && post ? "\n\n" : "") + post).replace(/\s+$/, "") + "\n";
  if (next.trim()) fs.writeFileSync(file, next, "utf8");
  else fs.rmSync(file, { force: true });
}

function selectedAgents(selection, reg) {
  if (selection === "all") {
    return ["universal", ...Object.keys(reg).filter((name) => !["generic", "universal"].includes(name))];
  }
  if (!reg[selection]) die(`unknown agent ${JSON.stringify(selection)}; choose one of: all, ${Object.keys(reg).sort().join(", ")}`);
  return [selection];
}

function skillDestination(target, agents, reg) {
  const dirs = new Set(agents.map((name) => reg[name].skill_dir));
  if (dirs.size !== 1) die("adapter registry uses multiple skill directories; one canonical install is required");
  return path.join(target, [...dirs][0]);
}

function instructionFiles(agents, reg) {
  return [...new Set(["AGENTS.md", ...agents.map((name) => reg[name].instruction_file)])];
}

function copyDir(src, dst) {
  fs.cpSync(src, dst, { recursive: true, force: false, errorOnExist: true });
}

const TEXT_HASH_EXTENSIONS = new Set([".md", ".mdc", ".txt", ".json", ".yml", ".yaml", ".js", ".mjs", ".py", ".sh", ".ps1"]);

function hashBytes(file) {
  const data = fs.readFileSync(file);
  if (!TEXT_HASH_EXTENSIONS.has(path.extname(file).toLowerCase())) return data;
  return Buffer.from(data.toString("utf8").replace(/\r\n?/g, "\n"), "utf8");
}

function hashTree(root) {
  const hash = crypto.createHash("sha512");
  const walk = (dir, prefix = "") => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = path.join(dir, entry.name);
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) walk(full, rel);
      else if (entry.isFile()) {
        hash.update(rel);
        hash.update("\0");
        hash.update(hashBytes(full));
        hash.update("\0");
      }
    }
  };
  walk(root);
  return hash.digest("hex");
}

function removePath(file) {
  fs.rmSync(file, { recursive: true, force: true });
}

function pruneEmptyParents(start, stop) {
  const stopAbs = path.resolve(stop);
  let current = path.resolve(start);
  while (current !== stopAbs && current.startsWith(stopAbs + path.sep)) {
    if (!fs.existsSync(current)) {
      current = path.dirname(current);
      continue;
    }
    if (fs.readdirSync(current).length) break;
    fs.rmdirSync(current);
    current = path.dirname(current);
  }
}

function loadManifest(target) {
  const file = path.join(target, MANIFEST);
  if (!fs.existsSync(file)) die(`no install manifest at ${file}`);
  try {
    return [file, JSON.parse(fs.readFileSync(file, "utf8"))];
  } catch (err) {
    die(`cannot read install manifest: ${err.message}`);
  }
}

export function modifiedManagedPaths(target, meta) {
  const skillDir = path.join(target, meta.skill_dir || ".agents/skills");
  if (!fs.existsSync(skillDir)) return [`${meta.skill_dir || ".agents/skills"} (missing)`];
  const checksums = meta.checksums || {};
  if (meta.mode === "copy" && Object.keys(checksums).length) {
    const modified = [];
    for (const rel of meta.installed || []) {
      const item = path.join(target, rel);
      if (!fs.existsSync(item)) modified.push(`${rel} (missing)`);
      else if (checksums[rel] && hashTree(item) !== checksums[rel]) modified.push(rel);
    }
    return modified;
  }
  if (meta.mode === "copy" && meta.tree_checksum) {
    return hashTree(skillDir) === meta.tree_checksum ? [] : [`${meta.skill_dir || ".agents/skills"} (content changed)`];
  }
  const modified = [];
  for (const rel of meta.installed || []) {
    const item = path.join(target, rel);
    if (!fs.existsSync(item)) modified.push(`${rel} (missing)`);
  }
  return modified;
}

export function install({ target = process.cwd(), agent = "all", force = false, manageGitignore = true } = {}) {
  target = path.resolve(target);
  if (!fs.existsSync(target)) die(`target does not exist: ${target}`);
  const reg = registry();
  const agents = selectedAgents(agent, reg);
  const skillsDst = skillDestination(target, agents, reg);
  fs.mkdirSync(skillsDst, { recursive: true });
  const installed = [];
  const srcRoot = path.join(PACKAGE_ROOT, "skills");
  const sources = fs.readdirSync(srcRoot).sort().filter((name) => {
    const src = path.join(srcRoot, name);
    return fs.statSync(src).isDirectory() && fs.existsSync(path.join(src, "SKILL.md"));
  });
  const identicalExisting = new Set();
  if (!force) {
    const collisions = [];
    for (const name of sources) {
      const src = path.join(srcRoot, name);
      const dst = path.join(skillsDst, name);
      if (!fs.existsSync(dst)) continue;
      let identical = false;
      try {
        identical = fs.statSync(dst).isDirectory() && hashTree(dst) === hashTree(src);
      } catch {
        identical = false;
      }
      if (identical) identicalExisting.add(name);
      else collisions.push(name);
    }
    if (collisions.length) {
      const preview = collisions.slice(0, 5).map((name) => path.join(skillsDst, name)).join(", ");
      const more = collisions.length > 5 ? ` (+${collisions.length - 5} more)` : "";
      die(`skill destinations already exist with different content: ${preview}${more}; use --force to replace them`);
    }
  }
  for (const name of sources) {
    const src = path.join(srcRoot, name);
    const dst = path.join(skillsDst, name);
    if (!identicalExisting.has(name)) {
      if (fs.existsSync(dst)) removePath(dst);
      copyDir(src, dst);
    }
    installed.push(path.relative(target, dst).split(path.sep).join("/"));
  }
  const instructions = instructionFiles(agents, reg);
  for (const rel of instructions) mergeMarkedBlock(path.join(target, rel), BEGIN, END, BLOCK);
  if (manageGitignore) mergeMarkedBlock(path.join(target, ".gitignore"), GITIGNORE_BEGIN, GITIGNORE_END, GITIGNORE_BLOCK);
  const meta = {
    source: PACKAGE_ROOT,
    package: "potetos-for-everyone",
    package_version: packageVersion(),
    installer: "node",
    agent_selection: agent,
    agents,
    mode: "copy",
    skill_dir: path.relative(target, skillsDst).split(path.sep).join("/"),
    instruction_files: instructions,
    gitignore_managed: manageGitignore,
    installed,
    checksums: Object.fromEntries(installed.map((rel) => [rel, hashTree(path.join(target, rel))])),
    tree_checksum: hashTree(skillsDst)
  };
  const manifest = path.join(target, MANIFEST);
  fs.mkdirSync(path.dirname(manifest), { recursive: true });
  fs.writeFileSync(manifest, JSON.stringify(meta, null, 2) + "\n", "utf8");
  return { target, installed: installed.length, agent, agents, skills: meta.skill_dir };
}

export function update({ target = process.cwd(), force = false } = {}) {
  target = path.resolve(target);
  const [, meta] = loadManifest(target);
  const modified = modifiedManagedPaths(target, meta);
  if (modified.length && !force) {
    const sample = modified.slice(0, 5).join(", ");
    const more = modified.length > 5 ? ` (+${modified.length - 5} more)` : "";
    die(`managed skills were edited or removed: ${sample}${more}; rerun with --force to replace them`);
  }
  for (const rel of meta.installed || []) removePath(path.join(target, rel));
  return install({
    target,
    agent: meta.agent_selection || "universal",
    force: false,
    manageGitignore: meta.gitignore_managed !== false
  });
}

export function autoInstall({ target = process.cwd(), agent = "all" } = {}) {
  const manifest = path.join(path.resolve(target), MANIFEST);
  if (!fs.existsSync(manifest)) return { action: "installed", result: install({ target, agent }) };
  return { action: "updated", result: update({ target }) };
}

export function uninstall({ target = process.cwd() } = {}) {
  target = path.resolve(target);
  const [manifest, meta] = loadManifest(target);
  for (const rel of meta.installed || []) removePath(path.join(target, rel));
  const skillDir = path.join(target, meta.skill_dir || ".agents/skills");
  pruneEmptyParents(skillDir, target);
  for (const rel of meta.instruction_files || ["AGENTS.md"]) {
    const file = path.join(target, rel);
    removeMarkedBlock(file, BEGIN, END);
    if (!fs.existsSync(file)) pruneEmptyParents(path.dirname(file), target);
  }
  if (meta.gitignore_managed) removeMarkedBlock(path.join(target, ".gitignore"), GITIGNORE_BEGIN, GITIGNORE_END);
  fs.rmSync(manifest, { force: true });
  pruneEmptyParents(path.dirname(manifest), target);
  return { target };
}

export function status({ target = process.cwd() } = {}) {
  target = path.resolve(target);
  const manifest = path.join(target, MANIFEST);
  if (!fs.existsSync(manifest)) return { installed: false, target, clean: false };
  const [, meta] = loadManifest(target);
  const modified = modifiedManagedPaths(target, meta);
  return {
    installed: true,
    target,
    clean: modified.length === 0,
    modified,
    count: (meta.installed || []).length,
    agent: meta.agent_selection || "unknown",
    mode: meta.mode || "unknown",
    packageVersion: meta.package_version || null
  };
}

export function listSkills() {
  const srcRoot = path.join(PACKAGE_ROOT, "skills");
  return fs.readdirSync(srcRoot).filter((name) => fs.existsSync(path.join(srcRoot, name, "SKILL.md"))).sort();
}

export function doctor({ target = process.cwd() } = {}) {
  const reg = registry();
  const state = status({ target });
  return {
    packageRoot: PACKAGE_ROOT,
    packageVersion: packageVersion(),
    target: path.resolve(target),
    canonicalSkills: listSkills().length,
    install: state,
    adapters: Object.fromEntries(Object.entries(reg).map(([name, spec]) => [name, {
      skillDir: spec.skill_dir,
      instructionFile: spec.instruction_file,
      present: fs.existsSync(path.join(path.resolve(target), spec.instruction_file))
    }]))
  };
}

export function packageVersion() {
  return JSON.parse(fs.readFileSync(path.join(PACKAGE_ROOT, "package.json"), "utf8")).version;
}

export function isPackageDevelopmentInstall(initCwd) {
  if (!initCwd) return false;
  return path.resolve(initCwd) === PACKAGE_ROOT;
}
