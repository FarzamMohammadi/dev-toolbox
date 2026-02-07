#!/usr/bin/env node

/**
 * Automated Video Assembly
 *
 * Concatenates scene MP4s from output/ and overlays a music track from audio/
 * to produce a single final video.
 *
 * Uses the ffmpeg concat demuxer (no re-encoding) for fast, lossless joining.
 *
 * Usage:
 *   npm run assemble                          # scenes + music → output/final-demo.mp4
 *   npm run assemble -- --no-audio            # video only, no music overlay
 *   npm run assemble -- --audio audio/my.wav  # specify audio file
 *   npm run assemble -- --output out.mp4      # custom output path
 */

import { execSync, spawn } from "node:child_process";
import { readdir, writeFile, unlink } from "node:fs/promises";
import { resolve, join } from "node:path";

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

const NO_AUDIO = hasFlag("no-audio");
const OUTPUT_PATH = flag("output", "output/final-demo.mp4");
const AUDIO_OVERRIDE = flag("audio", null);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = (seconds % 60).toFixed(1);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function getVideoDuration(filePath) {
  const out = execSync(
    `ffprobe -v error -show_entries format=duration -of csv=p=0 "${filePath}"`,
    { encoding: "utf-8" }
  ).trim();
  return parseFloat(out);
}

async function discoverSceneMp4s(outputDir) {
  const files = await readdir(outputDir);
  return files
    .filter((f) => /^\d{2}-.+\.mp4$/.test(f))
    .filter((f) => f !== "final-demo.mp4")
    .sort();
}

async function discoverAudio(audioDir) {
  if (AUDIO_OVERRIDE) return AUDIO_OVERRIDE;

  let files;
  try {
    files = await readdir(audioDir);
  } catch {
    return null;
  }

  const audioExts = [".wav", ".mp3", ".flac", ".ogg", ".aac", ".m4a"];
  const audioFiles = files.filter((f) => {
    const ext = f.toLowerCase().substring(f.lastIndexOf("."));
    return audioExts.includes(ext) && f !== ".gitkeep";
  });

  if (audioFiles.length === 0) return null;
  if (audioFiles.length > 1) {
    console.warn(`  Warning: Multiple audio files found, using: ${audioFiles[0]}`);
  }
  return join(audioDir, audioFiles[0]);
}

// ---------------------------------------------------------------------------
// Assembly
// ---------------------------------------------------------------------------

async function main() {
  console.log("Demo Generator — Video Assembly");
  console.log("===============================\n");

  // Check ffmpeg
  try {
    execSync("ffmpeg -version", { stdio: "ignore" });
  } catch {
    console.error("  Error: ffmpeg not found in PATH");
    console.error("  Install it:  brew install ffmpeg");
    process.exit(1);
  }

  // Discover scene MP4s
  const outputDir = resolve(import.meta.dirname, "..", "output");
  const audioDir = resolve(import.meta.dirname, "..", "audio");
  const sceneMp4s = await discoverSceneMp4s(outputDir);

  if (sceneMp4s.length === 0) {
    console.error("  Error: No scene MP4s found in output/");
    console.error("  Record scenes first:  npm run record");
    process.exit(1);
  }

  console.log(`  Scenes: ${sceneMp4s.length} found`);
  sceneMp4s.forEach((f) => console.log(`          - ${f}`));

  // Calculate total video duration
  let totalDuration = 0;
  for (const f of sceneMp4s) {
    const dur = getVideoDuration(resolve(outputDir, f));
    totalDuration += dur;
  }
  console.log(`  Total video duration: ${formatTime(totalDuration)}`);

  // Discover audio
  let audioPath = null;
  if (!NO_AUDIO) {
    audioPath = await discoverAudio(audioDir);
    if (audioPath) {
      console.log(`  Audio: ${audioPath}`);
    } else {
      console.warn("  Warning: No audio file found in audio/ — producing video only");
    }
  } else {
    console.log("  Audio: skipped (--no-audio)");
  }

  // Write concat list
  const concatListPath = resolve(outputDir, ".concat-list.txt");
  const concatContent = sceneMp4s
    .map((f) => `file '${resolve(outputDir, f)}'`)
    .join("\n");

  try {
    await writeFile(concatListPath, concatContent, "utf-8");

    // Build ffmpeg command
    const outputFile = resolve(OUTPUT_PATH);
    const ffmpegArgs = ["-y", "-f", "concat", "-safe", "0", "-i", concatListPath];

    if (audioPath) {
      ffmpegArgs.push(
        "-i", resolve(audioPath),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-t", String(totalDuration),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest"
      );
    } else {
      ffmpegArgs.push("-c", "copy");
    }

    ffmpegArgs.push(outputFile);

    console.log(`\n  Assembling → ${OUTPUT_PATH}`);

    // Run ffmpeg
    const startTime = Date.now();
    await new Promise((resolveP, reject) => {
      const proc = spawn("ffmpeg", ffmpegArgs, {
        stdio: ["ignore", "pipe", "pipe"],
      });

      let stderr = "";
      proc.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

      proc.on("close", (code) => {
        if (code === 0) resolveP();
        else reject(new Error(`ffmpeg exited with code ${code}\n${stderr}`));
      });
      proc.on("error", reject);
    });

    const wallTime = ((Date.now() - startTime) / 1000).toFixed(1);

    console.log(`\n===============================`);
    console.log(`  Done in ${wallTime}s`);
    console.log(`  Output: ${OUTPUT_PATH}`);
    console.log(`  Duration: ${formatTime(totalDuration)}${audioPath ? " (with audio)" : " (video only)"}`);
  } finally {
    // Clean up temp concat list
    try {
      await unlink(concatListPath);
    } catch {
      // ignore
    }
  }
}

main().catch((err) => {
  console.error("\nFatal error:", err);
  process.exit(1);
});
