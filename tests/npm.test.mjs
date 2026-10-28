import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { install, update, status, uninstall, doctor, listSkills } from "../npm/core.mjs";

test("npm core: listSkills returns 57 skills", () => {
  const skills = listSkills();
  assert.equal(skills.length, 57);
  assert.ok(skills.includes("poteto-mode"));
  assert.ok(skills.includes("arena"));
  assert.ok(skills.includes("unslop"));
});

test("npm core: install, status, update, uninstall lifecycle", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "potetos-npm-test-"));
  try {
    // 1. Install
    const installRes = install({ target: tmp, agent: "all" });
    assert.equal(installRes.installed, 57);
    assert.ok(fs.existsSync(path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md")));
    assert.ok(fs.existsSync(path.join(tmp, ".potetos", "install.json")));
    assert.ok(fs.existsSync(path.join(tmp, "AGENTS.md")));

    // 2. Status clean
    const statusClean = status({ target: tmp });
    assert.equal(statusClean.installed, true);
    assert.equal(statusClean.clean, true);
    assert.equal(statusClean.count, 57);

    // 3. Status modified after editing
    const skillPath = path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md");
    fs.writeFileSync(skillPath, "modified", "utf8");
    const statusMod = status({ target: tmp });
    assert.equal(statusMod.clean, false);

    // Update without force should fail
    assert.throws(() => update({ target: tmp, force: false }));

    // Update with force should succeed
    const updateRes = update({ target: tmp, force: true });
    assert.equal(updateRes.installed, 57);
    assert.notEqual(fs.readFileSync(skillPath, "utf8"), "modified");

    // 4. Doctor
    const doc = doctor({ target: tmp });
    assert.equal(doc.canonicalSkills, 57);
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

test("npm core: Kiro standalone and default all expose native skills and clean up safely", () => {
  for (const agent of ["kiro", "all"]) {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "potetos-kiro-npm-"));
    try {
      install({ target: tmp, agent });
      const native = path.join(tmp, ".kiro", "skills", "poteto-mode", "SKILL.md");
      assert.ok(fs.existsSync(native));
      if (agent === "all") assert.ok(fs.existsSync(path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md")));
      const manifest = JSON.parse(fs.readFileSync(path.join(tmp, ".potetos", "install.json"), "utf8"));
      assert.ok(manifest.installed.includes(".kiro/skills/poteto-mode"));
      assert.equal(status({ target: tmp }).count, 57);
      assert.equal(status({ target: tmp }).clean, true);
      fs.appendFileSync(native, "\nuser modification\n");
      assert.equal(status({ target: tmp }).clean, false);
      assert.throws(() => update({ target: tmp }), /edited or removed/);
      assert.throws(() => uninstall({ target: tmp }), /edited or removed/);
      assert.ok(fs.existsSync(native));
      update({ target: tmp, force: true });
      assert.equal(status({ target: tmp }).clean, true);
      const unrelated = path.join(tmp, ".kiro", "skills", "custom", "SKILL.md");
      fs.mkdirSync(path.dirname(unrelated), { recursive: true });
      fs.writeFileSync(unrelated, "user-owned");
      uninstall({ target: tmp });
      assert.equal(fs.readFileSync(unrelated, "utf8"), "user-owned");
      assert.equal(fs.existsSync(native), false);
    } finally { fs.rmSync(tmp, { recursive: true, force: true }); }
  }
});

test("npm core: update preflights native skill collisions", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "potetos-kiro-collision-"));
  try {
    install({ target: tmp, agent: "all" });
    const metaPath = path.join(tmp, ".potetos", "install.json");
    const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));
    // Simulate an earlier manifest, before Kiro was included in all.
    for (const rel of meta.installed.filter(x => x.startsWith(".kiro/"))) fs.rmSync(path.join(tmp, rel), { recursive: true });
    meta.installed = meta.installed.filter(x => !x.startsWith(".kiro/"));
    delete meta.skill_dirs;
    delete meta.skill_count;
    for (const key of Object.keys(meta.checksums)) if (key.startsWith(".kiro/")) delete meta.checksums[key];
    fs.writeFileSync(metaPath, JSON.stringify(meta));
    const native = path.join(tmp, ".kiro", "skills", "poteto-mode", "SKILL.md");
    fs.mkdirSync(path.dirname(native), { recursive: true });
    fs.writeFileSync(native, "user-owned");
    assert.throws(() => update({ target: tmp }), /already exist/);
    assert.ok(fs.existsSync(path.join(tmp, ".agents", "skills", "poteto-mode", "SKILL.md")));
    assert.equal(fs.readFileSync(native, "utf8"), "user-owned");
  } finally { fs.rmSync(tmp, { recursive: true, force: true }); }
});
