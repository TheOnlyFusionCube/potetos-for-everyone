#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const version = fs.readFileSync(path.join(root, "VERSION"), "utf8").trim();
const errors = [];
if (pkg.name !== "potetos-for-everyone") errors.push(`unexpected package name: ${pkg.name}`);
if (pkg.version !== version) errors.push(`package.json version ${pkg.version} != VERSION ${version}`);
if (pkg.license !== "MIT") errors.push("package license must be MIT");
if (pkg.dependencies && Object.keys(pkg.dependencies).length) errors.push("npm package must remain zero-dependency");
if (!pkg.bin?.potetos || !pkg.bin?.["potetos-for-everyone"]) errors.push("both CLI aliases must be declared");
if (!pkg.scripts?.postinstall) errors.push("npm postinstall integration missing");
for (const rel of ["npm/potetos.mjs", "npm/core.mjs", "skills/poteto-mode/SKILL.md", "NOTICE.md", "LICENSE"]) {
  if (!fs.existsSync(path.join(root, rel))) errors.push(`missing npm package file: ${rel}`);
}
const license = fs.readFileSync(path.join(root, "LICENSE"), "utf8");
if (!license.includes("Copyright (c) 2026 Lauren Tan")) errors.push("Lauren Tan copyright missing from LICENSE");
if (errors.length) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  process.exit(1);
}
console.log(`npm package check: PASS (${pkg.name}@${pkg.version})`);
