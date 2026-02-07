# Recording Guide

## Automated Recording (Default)

The project includes a headless recorder that renders each scene to a deterministic 1080p 60fps MP4. It virtualizes all browser timing so output is frame-perfect and reproducible.

### Prerequisites
- Dev server running: `npm run dev` (in a separate terminal)
- ffmpeg installed: `brew install ffmpeg`
- Puppeteer installed: `npm install` (one-time)

### Usage

```bash
npm run record                     # record all scenes
npm run record -- --scene 01       # record a single scene
npm run record -- --fps 30         # lower fps (faster, smaller files)
npm run record -- --width 1920 --height 1080  # custom resolution (default)
```

Output MP4s land in `output/` alongside the HTML files (e.g. `output/01-hook.mp4`).

### What It Does
1. Discovers scene HTML files in `output/` (named `NN-name.html`)
2. Extracts each scene's duration from `initScene({ duration: N })`
3. Launches headless Chromium, injects a virtual clock that overrides `performance.now`, `requestAnimationFrame`, `setTimeout`, `setInterval`, and `Element.prototype.animate` (WAAPI)
4. Hides the HUD, presses play, then advances one virtual frame at a time
5. Screenshots each frame as PNG and pipes to ffmpeg for H.264 encoding
6. Outputs `output/NN-name.mp4` per scene

### Tips
- If a single scene needs re-recording, use `--scene NN` instead of re-recording everything
- Use `--fps 30` for faster iteration when checking timing; switch to 60 for final output
- The extra 0.5s of padding at the end captures any settling animations

---

## Manual Recording (Fallback)

If the automated recorder doesn't work for a particular scene (e.g. a scene uses a browser API that the virtual clock doesn't cover), fall back to manual screen recording.

### Quick Start (macOS QuickTime)
1. Open QuickTime Player
2. File > New Screen Recording
3. Click the dropdown arrow next to the record button
4. Select "None" for microphone (we add music separately)
5. Click Record, then click on the browser window
6. When done: click the Stop button in the menu bar
7. Save the recording

### Setup
- **Resolution**: 1920x1080 (resize browser window to this size)
- **Frame rate**: 60fps preferred, 30fps acceptable
- **Audio**: Record WITHOUT audio — music is added in assembly
- **Background**: Close all other windows, hide dock, clean desktop

### Workflow Per Scene
1. Open scene in Chrome: `http://localhost:3000/output/01-hook.html`
2. Make browser fullscreen (Cmd+Shift+F)
3. Press **H** to hide the HUD
4. Start screen recording
5. Wait 1 second (trim later), then press **Space** to play the scene
6. Let animation complete
7. Wait 1 second (trim later), then stop recording
8. Save the file
9. Repeat for each scene

### Tips
- Disable macOS notifications: System Settings > Notifications > Do Not Disturb
- Use a consistent browser window size across all scenes
- If a scene has issues, just re-record it — no need to redo everything
- Chrome DevTools > Cmd+Shift+M can force a specific viewport size

### Screen Recording Tools
| Tool | Platform | Cost | Notes |
|------|----------|------|-------|
| QuickTime Player | macOS | Free | Built-in, simple, reliable |
| OBS Studio | All | Free | More control, can set exact resolution/fps |
| ScreenFlow | macOS | $169 | Best quality, also a video editor |
| Kap | macOS | Free | Lightweight, exports to GIF too |
