#!/usr/bin/env node
/**
 * ============================================================================
 *  capture-8k.mjs — reusable lossless 8K surface-capture helper (Playwright).
 * ============================================================================
 *
 *  Capture a REAL web surface (a real URL — your dashboard, a real GitHub page,
 *  any rendered HTML) as a LOSSLESS PNG at true 8K resolution. Hand the PNGs to
 *  ffmpeg or Remotion to encode at any bitrate you like.
 *
 *  THE 8K-VIA-deviceScaleFactor TRICK
 *  ----------------------------------
 *  You do NOT render an enormous CSS viewport. You render a NORMAL desktop
 *  viewport (1920x1080) and tell the browser to draw it at a higher pixel
 *  density — `deviceScaleFactor: 4`. The CSS layout stays at 1920 wide (so the
 *  UI is laid out and legible exactly as a human sees it on a desktop), but each
 *  CSS pixel is rasterized into a 4x4 block of real device pixels. The resulting
 *  screenshot is 1920*4 x 1080*4 = 7680x4320 = 8K UHD, supersampled and razor
 *  sharp. DSF 2 on a 3840 viewport also hits 8K, but driving a natural 1920 CSS
 *  width keeps content-dense UI readable at video scale; DSF 4 supersamples it.
 *
 *  WHY NEVER recordVideo
 *  ---------------------
 *  Playwright's `recordVideo` is the quality trap. Its bitrate is NOT
 *  configurable; for chromium it is hardcoded at ~1 Mbit/s VP8
 *  (microsoft/playwright#10855). At ANY resolution the result looks mushy — it
 *  is the wall everyone hits when their "4K" demo still feels like 1080p. A PNG
 *  via `page.screenshot()` is lossless, then ffmpeg/Remotion encode it at e.g.
 *  ~142 Mbit/s ProRes/H.265 — roughly 140x the quality. Always capture stills;
 *  never record.
 *
 *  PRO MOVE: master at 8K, deliver at 4K. Downsampling 8K → 4K gives a
 *  supersampled, razor-sharp 4K file (true 8K files are enormous and rarely
 *  consumed). Capture at 8K here regardless of the delivery target.
 *
 *  USAGE (CLI)
 *  -----------
 *    # Single still of a live surface (default 1920x1080 @ DSF4 → 8K):
 *    node capture-8k.mjs --url http://127.0.0.1:3000/tasks --out ./footage/pickup.png
 *
 *    # Wait for a content signal before the shot (data has loaded), full page:
 *    node capture-8k.mjs --url https://github.com/owner/repo/pull/42 \
 *      --out ./footage/pr.png --wait "h1, bdi" --full-page
 *
 *    # A held "sequence" — duplicate the frame N times so ffmpeg has a clip:
 *    node capture-8k.mjs --url http://127.0.0.1:3000 --out-dir ./footage/intro \
 *      --frames 90
 *
 *    # Custom resolution (4K viewport at DSF2 also yields 8K):
 *    node capture-8k.mjs --url http://localhost:3000 --out ./shot.png \
 *      --width 3840 --height 2160 --dsf 2
 *
 *  USAGE (as a module)
 *  -------------------
 *    import { capture8k } from "./capture-8k.mjs";
 *    const { path, dims } = await capture8k({
 *      url: "http://127.0.0.1:3000/tasks",
 *      out: "./footage/pickup.png",
 *      waitFor: "table",          // optional content-ready selector
 *      prep: async (page) => {    // optional: expand a row, switch a tab, scroll
 *        await page.click("button.expand");
 *      },
 *    });
 *
 *  PREREQUISITE: `npm i -D playwright` (and `npx playwright install chromium`).
 *  ffprobe (from ffmpeg) is optional — used only to print/verify pixel dims.
 * ============================================================================
 */

import { chromium } from "playwright";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";

// ── Defaults ─────────────────────────────────────────────────────────────────
// A natural desktop CSS viewport, supersampled x4 → 7680x4320 (8K UHD) PNG.
const DEFAULTS = {
  width: 1920,
  height: 1080,
  dsf: 4,
  frames: 1, // >1 duplicates the single shot into a held N-frame clip
  fullPage: false, // viewport shot by default; --full-page captures the whole scroll height
  // How long to wait for the page to settle. networkidle is ideal for static
  // pages, but a surface that holds a long-lived connection (SSE/websocket)
  // NEVER fires networkidle — pass `settle: "domcontentloaded"` for those and
  // lean on `waitFor` (a content-ready selector) instead.
  settle: "networkidle",
  settleTimeoutMs: 30_000,
  waitTimeoutMs: 20_000,
};

/**
 * Capture one lossless 8K still of a real surface.
 *
 * @param {object} opts
 * @param {string}  opts.url            Target URL (or a `file://` / data URL).
 * @param {string} [opts.out]          Output PNG path. Defaults to <out-dir>/frame-0001.png.
 * @param {string} [opts.outDir]       Output dir (for held sequences). Required if `out` is omitted.
 * @param {number} [opts.width]        CSS viewport width  (default 1920).
 * @param {number} [opts.height]       CSS viewport height (default 1080).
 * @param {number} [opts.dsf]          deviceScaleFactor   (default 4 → 8K from 1080p).
 * @param {number} [opts.frames]       Duplicate the shot into N held frames (default 1).
 * @param {boolean}[opts.fullPage]     Capture the full scroll height vs. just the viewport.
 * @param {string} [opts.waitFor]      Optional selector to await before shooting (content-ready signal).
 * @param {string} [opts.settle]       Load state to await: "networkidle" | "load" | "domcontentloaded".
 * @param {(page: import('playwright').Page) => Promise<void>} [opts.prep]
 *        Optional hook run AFTER the page settles and BEFORE the shot — expand a
 *        row, switch a tab, scroll a comment into frame, dismiss a cookie banner.
 * @returns {Promise<{ path: string, dims: string }>}  the written path + "WxH" pixel dims.
 */
export async function capture8k(opts) {
  const o = { ...DEFAULTS, ...opts };
  if (!o.url) {
    throw new Error("capture8k: `url` is required.");
  }
  const outPath = o.out ?? (o.outDir ? join(o.outDir, "frame-0001.png") : null);
  if (!outPath) {
    throw new Error("capture8k: pass either `out` (a PNG path) or `outDir`.");
  }
  mkdirSync(dirname(outPath), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  try {
    // The DSF lives on the CONTEXT, not the screenshot call — every shot from
    // this context is rasterized at <width*dsf> x <height*dsf> device pixels.
    const context = await browser.newContext({
      viewport: { width: o.width, height: o.height },
      deviceScaleFactor: o.dsf,
    });
    const page = await context.newPage();

    await page.goto(o.url, { waitUntil: o.settle, timeout: o.settleTimeoutMs }).catch((err) => {
      // networkidle legitimately times out on surfaces with a persistent
      // connection; don't abort — `waitFor` below is the real readiness gate.
      if (o.settle === "networkidle") {
        log(`  (networkidle did not fire — continuing; relying on waitFor) ${err.message.split("\n")[0]}`);
      } else {
        throw err;
      }
    });

    // Wait for the content that actually matters in frame (data loaded, a tab
    // rendered) rather than a blank shell. Best-effort: capture anyway on miss.
    if (o.waitFor) {
      await page.waitForSelector(o.waitFor, { timeout: o.waitTimeoutMs }).catch(() => {
        log(`  (waitFor "${o.waitFor}" not seen in ${o.waitTimeoutMs}ms — capturing current state)`);
      });
    }

    // Hook for per-surface staging: expand/click/scroll/dismiss before the shot.
    if (o.prep) {
      await o.prep(page);
    }
    await page.waitForTimeout(500); // let any expand/scroll/animation settle

    await page.screenshot({ path: outPath, fullPage: o.fullPage });
    const dims = probeDims(outPath);

    // A "sequence" is just the same lossless still held for N frames — enough
    // for ffmpeg to build a clip of a static surface. (For genuine UI MOTION,
    // step the UI deterministically and capture each state, or animate it in
    // Remotion OVER this still — don't try to record real-time motion here.)
    if (o.frames > 1 && o.outDir) {
      for (let i = 2; i <= o.frames; i++) {
        copyFileSync(outPath, join(o.outDir, `frame-${String(i).padStart(4, "0")}.png`));
      }
    }

    log(`captured ${outPath}  (${dims}${o.frames > 1 ? `, x${o.frames} frames` : ""})`);
    return { path: outPath, dims };
  } finally {
    await browser.close();
  }
}

/** Probe a PNG's real pixel dimensions with ffprobe — the 8K verification gate. Returns "WxH" or "?". */
function probeDims(file) {
  const out = spawnSync(
    "ffprobe",
    ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", file],
    { encoding: "utf-8" },
  );
  const csv = (out.stdout || "").trim(); // e.g. "7680,4320"
  return csv ? csv.replace(",", "x") : "? (ffprobe unavailable)";
}

function log(msg) {
  process.stdout.write(`${msg}\n`);
}

// ── CLI ────────────────────────────────────────────────────────────────────────

/** Minimal `--flag value` / `--bool` parser — no dependency needed. */
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) {
      continue;
    }
    const key = a.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) {
      args[key] = true; // boolean flag, e.g. --full-page
    } else {
      args[key] = next;
      i++;
    }
  }
  return args;
}

async function cli() {
  const a = parseArgs(process.argv.slice(2));
  if (!a.url || (!a.out && !a["out-dir"])) {
    process.stderr.write(
      "Usage: node capture-8k.mjs --url <URL> (--out <file.png> | --out-dir <dir>)\n" +
        "       [--width 1920] [--height 1080] [--dsf 4] [--frames N]\n" +
        "       [--wait <selector>] [--settle networkidle|load|domcontentloaded] [--full-page]\n",
    );
    process.exit(1);
  }
  await capture8k({
    url: a.url,
    out: a.out,
    outDir: a["out-dir"],
    width: a.width ? Number(a.width) : undefined,
    height: a.height ? Number(a.height) : undefined,
    dsf: a.dsf ? Number(a.dsf) : undefined,
    frames: a.frames ? Number(a.frames) : undefined,
    fullPage: Boolean(a["full-page"]),
    waitFor: a.wait,
    settle: a.settle,
  });
}

// Run as a script only when invoked directly (not when imported as a module).
if (import.meta.url === `file://${process.argv[1]}`) {
  cli().catch((err) => {
    process.stderr.write(`\nCAPTURE FAILED: ${err.message}\n`);
    process.exit(1);
  });
}
