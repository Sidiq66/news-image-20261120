// news-image-20261120 entry program.
//
// The picture beside this file, entry.png, is the entry: one image
// that sums up the world news of Friday 20 November 2026, drawn as a
// newspaper front page (build_image.py in this repository draws it).
// The grader runs this program with no network; its job is to put
// those bytes at the output path, unchanged, so every run hands the
// judge the same picture.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The gate takes a whole PNG or JPEG of at most 1 MiB. Check the
// picture against that before copying, so a bad build fails here,
// in the open, instead of at the gate.
const bytes = readFileSync(source);
const isPng = bytes.length > 4 && bytes[0] === 0x89 && bytes[1] === 0x50
  && bytes[2] === 0x4e && bytes[3] === 0x47;
const isJpeg = bytes.length > 2 && bytes[0] === 0xff && bytes[1] === 0xd8;
if (!isPng && !isJpeg) {
  throw new Error('entry.png is neither a PNG nor a JPEG');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
