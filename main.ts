// gta6-meme-x-01-v3 entrypoint: copies the meme image and the post record
// into the grader output directory. Node 22, stdlib only, no network.
//
// Deliberately CommonJS require() rather than ESM import: with no
// package.json declaring a module type, an import would make Node emit a
// MODULE_TYPELESS_PACKAGE_JSON warning on stderr and break the
// silent-output requirement for the grader run.
const fs = require("node:fs");
const path = require("node:path");

const botDir = process.env.MAKEFUN_BOT_DIR || ".";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || path.join(botDir, "output");

fs.mkdirSync(outputDir, { recursive: true });

// Each entry is [path inside the bot dir, filename in the output dir].
const files = [
  [path.join("assets", "meme.png"), "meme.png"],
  ["POST.json", "POST.json"],
];

for (const [source, name] of files) {
  fs.copyFileSync(path.join(botDir, source), path.join(outputDir, name));
}
