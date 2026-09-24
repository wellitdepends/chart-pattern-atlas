// Build the site into public/.
// Today this just copies index.html. If the page ever needs a real build
// (bundling, minifying, generating HTML from the CSVs), do it here and write
// the results into OUT_DIR. Everything in OUT_DIR is what gets published.
import { rm, mkdir, copyFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = join(ROOT, "public");

// Files copied as-is from the project root into public/.
const STATIC_FILES = ["index.html"];

await rm(OUT_DIR, { recursive: true, force: true });
await mkdir(OUT_DIR, { recursive: true });

for (const file of STATIC_FILES) {
  await copyFile(join(ROOT, file), join(OUT_DIR, file));
  console.log(`copied ${file} -> public/${file}`);
}

console.log("Build complete: public/ is ready to publish.");
