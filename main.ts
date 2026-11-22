// gta6-meme-x-01 entrypoint (Node 22, standard library only).
//
// The entry itself is the X post: an agent-made GTA 6 meme, posted from a
// public X account with make.fun (a link or written out) and/or @makefunai
// plus the entrant's play code in its text, and named by POST.json at the
// repository root. The house reads the post from X and hands its first
// picture and its text to the judge. Nothing this program writes about the
// post is judged, so its only job is to hand POST.json over to the grader:
// read it from the repository and write it out to the output directory.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const SOURCE = join(BOT_DIR, "POST.json");
const TARGET = join(OUTPUT_DIR, "POST.json");

mkdirSync(OUTPUT_DIR, { recursive: true });

let raw: string;
try {
  raw = readFileSync(SOURCE, "utf8");
} catch (err) {
  console.error(`could not read ${SOURCE}: ${(err as Error).message}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(raw);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (
  typeof post !== "object" ||
  post === null ||
  typeof (post as { url?: unknown }).url !== "string" ||
  !(post as { url: string }).url.startsWith("http")
) {
  console.error("POST.json must be an object with an http(s) url string");
  process.exit(1);
}

// Re-serialise canonically so the output is byte-identical on every run,
// whatever whitespace the repository's POST.json was written with.
const canonical = JSON.stringify(post) + "\n";
writeFileSync(TARGET, canonical);
const url = (post as { url: string }).url;
if (url.includes("<handle>") || url.includes("<id>")) {
  console.warn(
    "warning: POST.json still holds the placeholder address — " +
      "replace it with the real X post URL before submitting",
  );
}
console.log(`wrote ${TARGET} (${canonical.length} bytes, url: ${url})`);
