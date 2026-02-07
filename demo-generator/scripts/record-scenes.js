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
 *   npm run record                          # record all scenes (final quality)
 *   npm run record -- --fast                # all optimizations: JPEG, HW encoder, parallel
 *   npm run record -- --scene 01            # record a single scene
 *   npm run record -- --fps 30              # lower fps
 *   npm run record -- --quality draft       # JPEG capture + fast encoder
 *   npm run record -- --parallel 4          # 4 scenes simultaneously
 *   npm run record -- --width 1920 --height 1080
 */

import { launch } from "puppeteer";
import { spawn, execSync } from "node:child_process";
import { readdir, readFile } from "node:fs/promises";
import { resolve, basename } from "node:path";

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);

function flag(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] && !args[idx + 1].startsWith("--")
    ? args[idx + 1]
    : fallback;
}

function hasFlag(name) {
  return args.includes(`--${name}`);
}

const FAST = hasFlag("fast");
const FPS = parseInt(flag("fps", "60"), 10);
const WIDTH = parseInt(flag("width", "1920"), 10);
const HEIGHT = parseInt(flag("height", "1080"), 10);
const SCENE_FILTER = flag("scene", null);
const QUALITY = FAST ? "draft" : flag("quality", "final"); // draft | final
const PARALLEL = parseInt(flag("parallel", FAST ? "3" : "1"), 10);
const EXTRA_SECONDS = 0.5;
const BASE_URL = "http://localhost:3000";

// Derived config
const USE_JPEG = QUALITY === "draft";

// ---------------------------------------------------------------------------
// Hardware detection
// ---------------------------------------------------------------------------

function detectHWEncoder() {
  try {
    const out = execSync("ffmpeg -hide_banner -encoders 2>/dev/null", { encoding: "utf-8" });
    return out.includes("h264_videotoolbox");
  } catch {
    return false;
  }
}

const HW_ENCODER_AVAILABLE = detectHWEncoder();
const USE_HW_ENCODER = USE_JPEG && HW_ENCODER_AVAILABLE;

// ---------------------------------------------------------------------------
// Time-virtualization injection script (runs in page context BEFORE any JS)
// ---------------------------------------------------------------------------

function buildInjectionScript(fps) {
  return /* js */ `
(() => {
  // ---- Virtual clock state ----
  let virtualTime = 0;            // ms
  let frameMs = ${(1000 / fps).toFixed(6)};

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
    const tracked = trackedAnimations.find(t => t.animation === this);
    if (tracked) return; // No-op: we manage its time via currentTime
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
    const due = [];
    for (let i = timerQueue.length - 1; i >= 0; i--) {
      const t = timerQueue[i];
      if (t.cancelled) { timerQueue.splice(i, 1); continue; }
      if (virtualTime >= t.fireAt) {
        due.push(t);
        if (t.interval > 0) {
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
        trackedAnimations.splice(i, 1);
      }
    }
  }

  window.__recording = { advanceFrame, getTime: () => virtualTime };
})();
`;
}

const INJECTION_SCRIPT = buildInjectionScript(FPS);

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
  const match = html.match(/initScene\s*\(\s*\{[^}]*duration\s*:\s*(\d+(?:\.\d+)?)/s);
  return match ? parseFloat(match[1]) : 10;
}

function spawnFFmpeg(outputPath) {
  const inputArgs = USE_JPEG
    ? ["-f", "image2pipe", "-vcodec", "mjpeg"]
    : ["-f", "image2pipe", "-vcodec", "png"];

  const encoderArgs = USE_HW_ENCODER
    ? ["-c:v", "h264_videotoolbox", "-q:v", "68", "-profile:v", "high"]
    : QUALITY === "draft"
      ? ["-c:v", "libx264", "-preset", "fast", "-crf", "18"]
      : ["-c:v", "libx264", "-preset", "slow", "-crf", "18"];

  const ffmpegArgs = [
    "-y",
    ...inputArgs,
    "-framerate", String(FPS),
    "-i", "pipe:0",
    ...encoderArgs,
    "-pix_fmt", "yuv420p",
    outputPath,
  ];

  const proc = spawn("ffmpeg", ffmpegArgs, {
    stdio: ["pipe", "pipe", "pipe"],
  });

  let stderr = "";
  proc.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

  return { proc, stderr: () => stderr };
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = (seconds % 60).toFixed(1);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function buildLaunchArgs() {
  const launchArgs = [
    `--window-size=${WIDTH},${HEIGHT}`,
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--force-device-scale-factor=1",
  ];

  // Use Metal rendering on macOS for GPU acceleration
  if (process.platform === "darwin") {
    launchArgs.push("--use-angle=metal", "--enable-gpu", "--use-gl=angle");
  } else {
    launchArgs.push("--disable-gpu-compositing");
  }

  return launchArgs;
}

// ---------------------------------------------------------------------------
// Frame capture
// ---------------------------------------------------------------------------

async function captureFrame(cdp) {
  if (USE_JPEG) {
    // CDP direct: faster, bypasses Puppeteer's screenshot queue
    const { data } = await cdp.send("Page.captureScreenshot", {
      format: "jpeg",
      quality: 90,
      optimizeForSpeed: true,
    });
    return Buffer.from(data, "base64");
  }
  // For final quality, CDP with PNG (no optimizeForSpeed for best quality)
  const { data } = await cdp.send("Page.captureScreenshot", {
    format: "png",
  });
  return Buffer.from(data, "base64");
}

// ---------------------------------------------------------------------------
// Scene recording
// ---------------------------------------------------------------------------

async function recordScene(browser, sceneFile, outputDir, label) {
  const sceneName = basename(sceneFile, ".html");
  const filePath = resolve(outputDir, sceneFile);
  const outputPath = resolve(outputDir, `${sceneName}.mp4`);
  const url = `${BASE_URL}/output/${sceneFile}`;

  const duration = await extractDuration(filePath);
  const totalFrames = Math.ceil((duration + EXTRA_SECONDS) * FPS);

  console.log(`\n  ${label}Recording: ${sceneName}`);
  console.log(`  ${label}Duration:  ${duration}s (+${EXTRA_SECONDS}s padding)`);
  console.log(`  ${label}Frames:    ${totalFrames} @ ${FPS}fps`);

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  // Inject time virtualization BEFORE any page JS runs
  await page.evaluateOnNewDocument(INJECTION_SCRIPT);

  // Navigate and wait for everything to load
  await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  // Advance a few frames to let initial JS execute
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => window.__recording.advanceFrame());
  }

  // Hide HUD
  await page.keyboard.press("KeyH");
  await page.evaluate(() => window.__recording.advanceFrame());

  // Trigger play
  await page.keyboard.press("Space");
  await page.evaluate(() => window.__recording.advanceFrame());

  // Open CDP session for direct screenshot capture
  const cdp = await page.createCDPSession();

  // Start ffmpeg
  const { proc: ffmpeg, stderr: getStderr } = spawnFFmpeg(outputPath);

  const ffmpegDone = new Promise((resolve, reject) => {
    ffmpeg.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with code ${code}\n${getStderr()}`));
    });
    ffmpeg.on("error", reject);
  });

  // Frame capture loop
  const startTime = Date.now();
  for (let frame = 0; frame < totalFrames; frame++) {
    await page.evaluate(() => window.__recording.advanceFrame());

    const screenshot = await captureFrame(cdp);

    const canWrite = ffmpeg.stdin.write(screenshot);
    if (!canWrite) {
      await new Promise((r) => ffmpeg.stdin.once("drain", r));
    }

    if ((frame + 1) % FPS === 0 || frame === totalFrames - 1) {
      const pct = Math.round(((frame + 1) / totalFrames) * 100);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      process.stdout.write(`\r  ${label}Progress:  ${pct}% (${frame + 1}/${totalFrames} frames, ${elapsed}s elapsed)`);
    }
  }

  ffmpeg.stdin.end();
  await ffmpegDone;

  const wallTime = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\n  ${label}Done:      ${wallTime}s → ${sceneName}.mp4`);

  await cdp.detach();
  await page.close();
  return { sceneName, outputPath, duration, wallTime: parseFloat(wallTime) };
}

// ---------------------------------------------------------------------------
// Parallel recording helpers
// ---------------------------------------------------------------------------

function distributeScenes(scenes, numWorkers) {
  const chunks = Array.from({ length: numWorkers }, () => []);
  scenes.forEach((scene, i) => {
    chunks[i % numWorkers].push(scene);
  });
  return chunks.filter((c) => c.length > 0);
}

async function recordChunk(browser, sceneFiles, outputDir, workerLabel) {
  const results = [];
  for (const sceneFile of sceneFiles) {
    const result = await recordScene(browser, sceneFile, outputDir, workerLabel);
    results.push(result);
  }
  return results;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log("Demo Generator — Automated Scene Recorder");
  console.log("==========================================");
  console.log(`  Resolution: ${WIDTH}x${HEIGHT} @ ${FPS}fps`);
  console.log(`  Quality:    ${QUALITY}${FAST ? " (--fast)" : ""}`);
  console.log(`  Capture:    ${USE_JPEG ? "JPEG q90 + optimizeForSpeed via CDP" : "PNG via CDP"}`);
  console.log(`  Encoder:    ${USE_HW_ENCODER ? "h264_videotoolbox (hardware)" : QUALITY === "draft" ? "libx264 (fast preset)" : "libx264 (slow preset)"}`);
  console.log(`  Parallel:   ${PARALLEL} browser instance${PARALLEL > 1 ? "s" : ""}`);

  // Check dev server
  const serverUp = await checkServer();
  if (!serverUp) {
    console.error(`\n  Error: Dev server not running at ${BASE_URL}`);
    console.error("  Start it first:  npm run dev");
    process.exit(1);
  }

  // Check ffmpeg
  try {
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

  const launchArgs = buildLaunchArgs();
  const launchOpts = { headless: true, args: launchArgs };

  let results;

  if (PARALLEL > 1 && scenes.length > 1) {
    // Parallel: launch N browser instances, distribute scenes
    const workerCount = Math.min(PARALLEL, scenes.length);
    const chunks = distributeScenes(scenes, workerCount);

    console.log(`\n  Launching ${workerCount} parallel workers...`);

    const browsers = await Promise.all(
      Array.from({ length: workerCount }, () => launch(launchOpts))
    );

    try {
      const chunkResults = await Promise.all(
        chunks.map((chunk, i) =>
          recordChunk(browsers[i], chunk, outputDir, `[W${i + 1}] `)
        )
      );
      results = chunkResults.flat();
    } finally {
      await Promise.all(browsers.map((b) => b.close()));
    }

    // Sort results back into scene order
    results.sort((a, b) => a.sceneName.localeCompare(b.sceneName));
  } else {
    // Sequential: single browser
    const browser = await launch(launchOpts);
    results = [];
    try {
      for (const sceneFile of scenes) {
        const result = await recordScene(browser, sceneFile, outputDir, "");
        results.push(result);
      }
    } finally {
      await browser.close();
    }
  }

  // Summary
  console.log("\n==========================================");
  console.log("Recording complete!\n");
  const totalDuration = results.reduce((s, r) => s + r.duration, 0);
  const totalWall = Math.max(...results.map((r) => r.wallTime)); // parallel = max, not sum
  results.forEach((r) => {
    console.log(`  ${r.sceneName}.mp4  (${formatTime(r.duration)})`);
  });
  console.log(`\n  Total video:  ${formatTime(totalDuration)}`);
  console.log(`  Wall time:    ${formatTime(PARALLEL > 1 ? totalWall : results.reduce((s, r) => s + r.wallTime, 0))}`);
  console.log(`\n  Files are in: output/`);
}

main().catch((err) => {
  console.error("\nFatal error:", err);
  process.exit(1);
});
