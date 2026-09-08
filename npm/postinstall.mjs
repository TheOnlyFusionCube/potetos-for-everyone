import process from "node:process";
import { autoInstall, isPackageDevelopmentInstall } from "./core.mjs";

const skip = process.env.POTETOS_SKIP_AUTO_INSTALL === "1" || process.env.POTETOS_SKIP_AUTO_INSTALL === "true";
const globalInstall = process.env.npm_config_global === "true" || process.env.npm_config_global === "1";
const execInstall = process.env.npm_command === "exec";
const target = process.env.INIT_CWD;

if (skip || globalInstall || execInstall || !target || isPackageDevelopmentInstall(target)) {
  if (globalInstall) console.log("potetos: global CLI installed; run `potetos install` inside a project.");
  process.exit(0);
}

try {
  const { action, result } = autoInstall({ target, agent: process.env.POTETOS_AGENT || "all" });
  console.log(`potetos: ${action} ${result.installed} skills in ${result.target}`);
  console.log("potetos: ready - ask your agent to use poteto-mode");
} catch (err) {
  console.error(`potetos: automatic project setup failed safely: ${err?.message || err}`);
  console.error("potetos: no differing managed files were overwritten. Resolve the conflict or reinstall with POTETOS_SKIP_AUTO_INSTALL=1 and run the CLI manually.");
  process.exitCode = 1;
}
