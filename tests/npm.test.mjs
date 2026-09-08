import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { install, update, status, uninstall, doctor, listSkills } from "../npm/core.mjs";

test("npm core: listSkills returns 47 skills", () => {
  const skills = listSkills();
  assert.equal(skills.length, 47);
  assert.ok(skills.includes("poteto-mode"));
  assert.ok(skills.includes("arena"));
  assert.ok(skills.includes("unslop"));
});

test("npm core: install, status, update, uninstall lifecycle", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "potetos-npm-test-"));
  try {
    // 1. Install
    const installRes = install({ target: tmp, agent: "all" });
    assert.equal(installRes.installed, 47);
    assert.ok(fs.existsSync(path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md")));
    assert.ok(fs.existsSync(path.join(tmp, ".potetos", "install.json")));
    assert.ok(fs.existsSync(path.join(tmp, "AGENTS.md")));

    // 2. Status clean
    const statusClean = status({ target: tmp });
    assert.equal(statusClean.installed, true);
    assert.equal(statusClean.clean, true);
    assert.equal(statusClean.count, 47);

    // 3. Status modified after editing
    const skillPath = path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md");
    fs.writeFileSync(skillPath, "modified", "utf8");
    const statusMod = status({ target: tmp });
    assert.equal(statusMod.clean, false);

    // Update without force should fail
    assert.throws(() => update({ target: tmp, force: false }));

    // Update with force should succeed
    const updateRes = update({ target: tmp, force: true });
    assert.equal(updateRes.installed, 47);
    assert.notEqual(fs.readFileSync(skillPath, "utf8"), "modified");

    // 4. Doctor
    const doc = doctor({ target: tmp });
    assert.equal(doc.canonicalSkills, 47);
    assert.equal(doc.install.clean, true);

    // 5. Uninstall
    const unRes = uninstall({ target: tmp });
    assert.equal(unRes.target, path.resolve(tmp));
    assert.ok(!fs.existsSync(path.join(tmp, ".potetos")));
    assert.ok(!fs.existsSync(path.join(tmp, ".agents", "skills")));
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});
