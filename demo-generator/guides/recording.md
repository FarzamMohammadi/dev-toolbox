# Screen Recording Guide

## Quick Start (macOS QuickTime)
1. Open QuickTime Player
2. File > New Screen Recording
3. Click the dropdown arrow next to the record button
4. Select "None" for microphone (we add music separately)
5. Click Record, then click on the browser window
6. When done: click the Stop button in the menu bar
7. Save the recording

## Recommended Setup
- **Resolution**: 1920x1080 (resize browser window to this size)
- **Frame rate**: 60fps preferred, 30fps acceptable
- **Audio**: Record WITHOUT audio — music is added in assembly
- **Background**: Close all other windows, hide dock, clean desktop

## Recording Workflow Per Scene
1. Open scene in Chrome: `http://localhost:3000/01-hook.html`
2. Make browser fullscreen (Cmd+Shift+F)
3. Press **H** to hide the HUD
4. Start screen recording
5. Wait 1 second (trim later), then press **Space** to play the scene
6. Let animation complete
7. Wait 1 second (trim later), then stop recording
8. Save as `recordings/01-hook.mov` (or similar)
9. Repeat for each scene

## Tips
- Disable macOS notifications: System Settings > Notifications > Do Not Disturb
- Use a consistent browser window size across all scenes
- If a scene has issues, just re-record it — no need to redo everything
- Chrome DevTools > Cmd+Shift+M can force a specific viewport size

## Tools
| Tool | Platform | Cost | Notes |
|------|----------|------|-------|
| QuickTime Player | macOS | Free | Built-in, simple, reliable |
| OBS Studio | All | Free | More control, can set exact resolution/fps |
| ScreenFlow | macOS | $169 | Best quality, also a video editor |
| Kap | macOS | Free | Lightweight, exports to GIF too |
