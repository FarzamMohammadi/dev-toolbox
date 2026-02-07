#!/usr/bin/env node

/**
 * Automated Scene Recorder
 *
 * Renders each scene HTML to a deterministic 1080p 60fps MP4 by:
 * 1. Injecting a virtual clock that overrides ALL browser timing APIs
 * 2. Intercepting WAAPI (Web Animations API) so Motion.dev animations are frame-synced
 * 3. Capturing screenshots frame-by-frame and piping to ffmpeg
 *
 * Usage:
 *   npm run record                     # record all scenes
 *   npm run record -- --scene 01       # record a single scene
 *   npm run record -- --fps 30         # lower fps (faster, smaller)
 *   npm run record -- --width 1920 --height 1080
 */

import { launch } from "puppeteer";
import { spawn } from "node:child_process";
import { readdir, readFile } from "node:fs/promises";
import { resolve, basename } from "node:path";

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);

function flag(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const FPS = parseInt(flag("fps", "60"), 10);
const WIDTH = parseInt(flag("width", "1920"), 10);
const HEIGHT = parseInt(flag("height", "1080"), 10);
const SCENE_FILTER = flag("scene", null); // e.g. "01" or "03-solution"
const EXTRA_SECONDS = 0.5; // extra capture time after scene duration
const BASE_URL = "http://localhost:3000";

// ---------------------------------------------------------------------------
// Time-virtualization injection script (runs in page context BEFORE any JS)
// ---------------------------------------------------------------------------

const INJECTION_SCRIPT = /* js */ `
(() => {
  // ---- Virtual clock state ----
  let virtualTime = 0;            // ms
  let frameMs = ${(1000 / FPS).toFixed(6)};

  // ---- rAF virtualization ----
  const rafQueue = [];            // current-frame callbacks
  let nextRafQueue = [];          // next-frame callbacks (from nested rAFs)
  let rafIdCounter = 1;
  const rafCancelled = new Set();

  const _origRAF = window.requestAnimationFrame;
  const _origCAF = window.cancelAnimationFrame;

  window.requestAnimationFrame = function (cb) {
    const id = rafIdCounter++;
    nextRafQueue.push({ id, cb });
    return id;
  };
  window.cancelAnimationFrame = function (id) {
    rafCancelled.add(id);
  };

  // ---- setTimeout / setInterval virtualization ----
  const timerQueue = [];          // { id, cb, fireAt, interval, cancelled }
  let timerIdCounter = 100000;    // offset to avoid collision with real timer IDs

  const _origSetTimeout = window.setTimeout;
  const _origClearTimeout = window.clearTimeout;
  const _origSetInterval = window.setInterval;
  const _origClearInterval = window.clearInterval;

  window.setTimeout = function (cb, delay = 0, ...args) {
    const id = timerIdCounter++;
    timerQueue.push({ id, cb, fireAt: virtualTime + delay, interval: 0, cancelled: false, args });
    return id;
  };
  window.clearTimeout = function (id) {
    const t = timerQueue.find(t => t.id === id);
    if (t) t.cancelled = true;
  };
  window.setInterval = function (cb, interval = 0, ...args) {
    const id = timerIdCounter++;
    timerQueue.push({ id, cb, fireAt: virtualTime + Math.max(interval, 1), interval: Math.max(interval, 1), cancelled: false, args });
    return id;
  };
  window.clearInterval = function (id) {
    const t = timerQueue.find(t => t.id === id);
    if (t) t.cancelled = true;
  };

  // ---- performance.now / Date.now virtualization ----
  const _origPerfNow = performance.now.bind(performance);

  Object.defineProperty(performance, 'now', {
    value: () => virtualTime,
    writable: true,
    configurable: true,
  });
  Date.now = () => Math.floor(virtualTime);

  // ---- WAAPI interception ----
  const trackedAnimations = [];   // { animation, createdAt }

  const _origAnimate = Element.prototype.animate;
  Element.prototype.animate = function (...args) {
    const animation = _origAnimate.apply(this, args);
    animation.pause();  // immediately pause so we control time
    trackedAnimations.push({ animation, createdAt: virtualTime });
    return animation;
  };

  // Prevent Motion.dev from calling .play() and resuming real-time playback
  const _origPlay = Animation.prototype.play;
  Animation.prototype.play = function () {
    // Check if this is a tracked (intercepted) animation
    const tracked = trackedAnimations.find(t => t.animation === this);
    if (tracked) {
      // No-op: we manage its time via currentTime
      return;
    }
    // Untracked animations (e.g. CSS blink cursor) can play normally
    return _origPlay.call(this);
  };

  // ---- Frame advance (called from Puppeteer per-frame) ----
  function advanceFrame() {
    virtualTime += frameMs;

    // 1. Promote next-frame rAF queue to current, clear next
    rafQueue.length = 0;
    rafQueue.push(...nextRafQueue);
    nextRafQueue = [];

    // Flush rAF queue (callbacks may schedule new rAFs into nextRafQueue)
    for (const entry of rafQueue) {
      if (rafCancelled.has(entry.id)) {
        rafCancelled.delete(entry.id);
        continue;
      }
      try { entry.cb(virtualTime); } catch (e) { console.error('[rec] rAF error:', e); }
    }

    // 2. Fire due timers
    // Sort by fireAt so we process in order
    const due = [];
    for (let i = timerQueue.length - 1; i >= 0; i--) {
      const t = timerQueue[i];
      if (t.cancelled) { timerQueue.splice(i, 1); continue; }
      if (virtualTime >= t.fireAt) {
        due.push(t);
        if (t.interval > 0) {
          // Reschedule interval
          t.fireAt += t.interval;
        } else {
          timerQueue.splice(i, 1);
        }
      }
    }
    due.sort((a, b) => a.fireAt - b.fireAt);
    for (const t of due) {
      if (t.cancelled) continue;
      try { t.cb(...(t.args || [])); } catch (e) { console.error('[rec] timer error:', e); }
    }

    // 3. Sync WAAPI animations
    for (let i = trackedAnimations.length - 1; i >= 0; i--) {
      const { animation, createdAt } = trackedAnimations[i];
      if (animation.playState === 'idle') {
        trackedAnimations.splice(i, 1);
        continue;
      }
      const localTime = virtualTime - createdAt;
      try {
        animation.currentTime = localTime;
      } catch {
        // Animation may have been cancelled/removed
        trackedAnimations.splice(i, 1);
      }
    }
  }

  window.__recording = { advanceFrame, getTime: () => virtualTime };
})();
`;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function checkServer() {
  try {
    const res = await fetch(BASE_URL);
    return res.ok;
  } catch {
    return false;
  }
}

async function discoverScenes(outputDir) {
  const files = await readdir(outputDir);
  let scenes = files
    .filter((f) => /^\d{2}-.+\.html$/.test(f))
    .sort();

  if (SCENE_FILTER) {
    scenes = scenes.filter((f) => f.includes(SCENE_FILTER));
  }
  return scenes;
}

async function extractDuration(filePath) {
  const html = await readFile(filePath, "utf-8");
  // Match initScene({ ... duration: N ... })
  const match = html.match(/initScene\s*\(\s*\{[^}]*duration\s*:\s*(\d+(?:\.\d+)?)/s);
  return match ? parseFloat(match[1]) : 10;
}

function spawnFFmpeg(outputPath) {
  const ffmpegArgs = [
    "-y",
    "-f", "image2pipe",
    "-framerate", String(FPS),
    "-i", "pipe:0",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "slow",
    "-crf", "18",
    outputPath,
  ];

  const proc = spawn("ffmpeg", ffmpegArgs, {
    stdio: ["pipe", "pipe", "pipe"],
  });

  // Collect stderr for error reporting
  let stderr = "";
  proc.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

  return { proc, stderr: () => stderr };
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = (seconds % 60).toFixed(1);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

// ---------------------------------------------------------------------------
// Main recording loop
// ---------------------------------------------------------------------------

async function recordScene(browser, sceneFile, outputDir) {
  const sceneName = basename(sceneFile, ".html");
  const filePath = resolve(outputDir, sceneFile);
  const outputPath = resolve(outputDir, `${sceneName}.mp4`);
  const url = `${BASE_URL}/output/${sceneFile}`;

  const duration = await extractDuration(filePath);
  const totalFrames = Math.ceil((duration + EXTRA_SECONDS) * FPS);

  console.log(`\n  Recording: ${sceneName}`);
  console.log(`  Duration:  ${duration}s (+${EXTRA_SECONDS}s padding)`);
  console.log(`  Frames:    ${totalFrames} @ ${FPS}fps`);
  console.log(`  Output:    ${outputPath}`);

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  // Inject time virtualization BEFORE any page JS runs
  await page.evaluateOnNewDocument(INJECTION_SCRIPT);

  // Navigate and wait for everything to load
  await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  // Give a moment for module imports to settle
  // Advance a few frames to let initial JS execute
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => window.__recording.advanceFrame());
  }

  // Hide HUD
  await page.keyboard.press("KeyH");
  // One more frame to apply the HUD hide transition
  await page.evaluate(() => window.__recording.advanceFrame());

  // Trigger play (Space key)
  await page.keyboard.press("Space");
  // Advance one frame so onPlay callbacks fire
  await page.evaluate(() => window.__recording.advanceFrame());

  // Start ffmpeg
  const { proc: ffmpeg, stderr: getStderr } = spawnFFmpeg(outputPath);

  const ffmpegDone = new Promise((resolve, reject) => {
    ffmpeg.proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with code ${code}\n${getStderr()}`));
    });
    ffmpeg.proc.on("error", reject);
  });

  // Frame capture loop
  const startTime = Date.now();
  for (let frame = 0; frame < totalFrames; frame++) {
    // Advance virtual time
    await page.evaluate(() => window.__recording.advanceFrame());

    // Capture screenshot as PNG buffer
    const screenshot = await page.screenshot({ type: "png", omitBackground: false });

    // Write to ffmpeg stdin
    const canWrite = ffmpeg.proc.stdin.write(screenshot);
    if (!canWrite) {
      await new Promise((r) => ffmpeg.proc.stdin.once("drain", r));
    }

    // Progress indicator (every 60 frames = ~1 second of video)
    if ((frame + 1) % FPS === 0 || frame === totalFrames - 1) {
      const pct = Math.round(((frame + 1) / totalFrames) * 100);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      process.stdout.write(`\r  Progress:  ${pct}% (${frame + 1}/${totalFrames} frames, ${elapsed}s elapsed)`);
    }
  }

  // Close ffmpeg stdin and wait for encoding to finish
  ffmpeg.proc.stdin.end();
  await ffmpegDone;

  const wallTime = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n  Done:      ${wallTime}s wall time → ${outputPath}`);

  await page.close();
  return { sceneName, outputPath, duration, wallTime: parseFloat(wallTime) };
}

async function main() {
  console.log("Demo Generator — Automated Scene Recorder");
  console.log("==========================================");
  console.log(`  Resolution: ${WIDTH}x${HEIGHT} @ ${FPS}fps`);

  // Check dev server
  const serverUp = await checkServer();
  if (!serverUp) {
    console.error(`\n  Error: Dev server not running at ${BASE_URL}`);
    console.error("  Start it first:  npm run dev");
    process.exit(1);
  }

  // Check ffmpeg
  try {
    const { execSync } = await import("node:child_process");
    execSync("ffmpeg -version", { stdio: "ignore" });
  } catch {
    console.error("\n  Error: ffmpeg not found in PATH");
    console.error("  Install it:  brew install ffmpeg");
    process.exit(1);
  }

  // Discover scenes
  const outputDir = resolve(import.meta.dirname, "..", "output");
  const scenes = await discoverScenes(outputDir);

  if (scenes.length === 0) {
    console.error("\n  Error: No scene files found in output/");
    console.error("  Scene files should be named like: 01-hook.html, 02-problem.html, etc.");
    process.exit(1);
  }

  console.log(`  Scenes:    ${scenes.length} found`);
  scenes.forEach((s) => console.log(`             - ${s}`));

  // Launch browser
  const browser = await launch({
    headless: true,
    args: [
      `--window-size=${WIDTH},${HEIGHT}`,
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-gpu-compositing",
      "--force-device-scale-factor=1",
    ],
  });

  const results = [];
  try {
    for (const sceneFile of scenes) {
      const result = await recordScene(browser, sceneFile, outputDir);
      results.push(result);
    }
  } finally {
    await browser.close();
  }

  // Summary
  console.log("\n==========================================");
  console.log("Recording complete!\n");
  const totalDuration = results.reduce((s, r) => s + r.duration, 0);
  const totalWall = results.reduce((s, r) => s + r.wallTime, 0);
  results.forEach((r) => {
    console.log(`  ${r.sceneName}.mp4  (${formatTime(r.duration)})`);
  });
  console.log(`\n  Total video:  ${formatTime(totalDuration)}`);
  console.log(`  Total time:   ${formatTime(totalWall)}`);
  console.log(`\n  Files are in: output/`);
}

main().catch((err) => {
  console.error("\nFatal error:", err);
  process.exit(1);
});
