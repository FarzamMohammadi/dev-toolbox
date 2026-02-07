# Video Assembly Guide

## Overview
After recording each scene, assemble them into a final video with music.

## Steps

### 1. Import Everything
- Open your video editor (ScreenFlow, DaVinci Resolve, iMovie)
- Import all scene recordings from `recordings/`
- Import your music track from `audio/`

### 2. Arrange Scenes
- Place scenes on the timeline in order: hook → problem → solution → demo → results → cta
- Trim the 1-second padding at the start and end of each recording
- Butt the clips together (no gaps)

### 3. Add Music
- Drag the music track onto the audio timeline
- It should run as one continuous track under all scenes
- If you trimmed the song earlier, use that trimmed version

### 4. Align to Beats
- Use `output/beats.json` as reference for beat timestamps
- Scene transitions should land on beat boundaries
- If a cut feels off, nudge it a frame or two to hit the beat

### 5. Transitions (Optional)
- Simple cuts work great (Aaron Francis used mostly hard cuts)
- If adding transitions: cross-dissolve or fade-through-black are safest
- Keep transitions SHORT (0.2-0.5s max)
- Don't overdo it — the animations in the scenes are the visual interest

### 6. Export
- **Format**: H.264 or H.265 (MP4)
- **Resolution**: 1920x1080
- **Frame rate**: Match your recording (60fps or 30fps)
- **Bitrate**: 10-20 Mbps for high quality
- **Audio**: AAC, 256kbps

## Free Video Editors
| Editor | Platform | Notes |
|--------|----------|-------|
| DaVinci Resolve | All | Professional, free version is very capable |
| iMovie | macOS | Simple, built-in, good enough for this |
| Kdenlive | All | Open source, decent timeline editor |
| CapCut | All | Free, good for quick edits |

## Tips
- Export a draft version first at lower quality to check timing
- Watch the full video with fresh eyes before final export
- If posting to X/Twitter: keep under 2:20 for auto-play
- If posting to LinkedIn: square (1080x1080) or 4:5 gets more views
