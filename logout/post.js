const { spawnSync } = require("node:child_process");

const result = spawnSync("tessl", ["logout"], { stdio: "inherit" });

if (result.error) {
  if (result.error.code === "ENOENT") {
    console.log("tessl binary not found; skipping logout");
  } else {
    console.log(`Tessl logout (best effort) failed to start: ${result.error.message}`);
  }
} else if (result.status !== 0) {
  console.log(`Tessl logout (best effort) exited with code ${result.status}`);
}

process.exit(0);
