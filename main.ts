// Entry for make.fun bounty "Post the Meme, Win the Feed" (program/v1, Node 22,
// standard library only): it copies POST.json from the repository root to
// /output/POST.json, where the gate reads it. That is all the program has to do.
// The entry is the X post itself: my agent made the meme picture (meme.png, drawn
// by render_meme.py in this session), the post goes up on X from a public account
// with @_myronera and one of the account's play codes in its text, POST.json names
// the post, and the house reads the post's counts from X. Nothing this program
// writes about the post is scored.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in
// for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postPath = join(BOT_DIR, 'POST.json');
const post = JSON.parse(readFileSync(postPath, 'utf8')) as { url?: unknown };
if (typeof post.url !== 'string' || !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/\d+/.test(post.url)) {
  console.error('POST.json does not name a valid X post URL');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
const outPath = join(OUTPUT_DIR, 'POST.json');
try {
  copyFileSync(postPath, outPath);
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

// Read-back check: the copy must be byte-identical to the source.
const copied = readFileSync(outPath);
const original = readFileSync(postPath);
if (!copied.equals(original)) {
  console.error('POST.json copy differs from the source');
  process.exit(1);
}
console.log(`POST.json copied to ${outPath} for post ${post.url}`);
