# Git Visualizer

A standalone tool for interactive git repository history visualization using gource.

## Quick Start

```bash
# Edit config if needed
vim config.sh

# Run (handles everything: tool checking, installation, visualization)
./run.sh

# Check output
ls output/repo-evolution/
```

## Requirements

- **gource**: For repository visualization
- **ffmpeg**: For video export (optional - without it, shows live preview only)

The script will offer to install missing tools via Homebrew if available.

## Directory Structure

```
git-visualizer/
├── run.sh                    # Main script (does everything)
├── config.sh                 # Configuration file
├── output/                   # Generated files (gitignored)
│   └── repo-evolution/      # history.mp4
├── README.md                 # This file
└── .gitignore
```

## Configuration

Edit `config.sh`:

| Option | Default | Description |
|--------|---------|-------------|
| `PROJECT_NAME` | - | Project name for titles |
| `GOURCE_TITLE` | `${PROJECT_NAME} Evolution - DON'T CLOSE...` | Title in visualization window |
| `GOURCE_RESOLUTION` | `"960x720"` | Window size (WxH) |
| `GOURCE_SECONDS_PER_DAY` | `"0.5"` | Playback speed (lower = faster) |
| `GOURCE_VIDEO_DURATION` | `60` | Video length in seconds. Use `-1` for full history |

**Note:** If video doesn't capture full git history, increase `GOURCE_VIDEO_DURATION` in config.sh.

## Interactive Window

The visualization window is **fully interactive while recording**. Navigate in real-time:

- **Space** - Pause/resume the timeline
- **+/-** - Speed up/slow down
- **Arrow keys** - Pan the camera
- **Mouse drag** - Move around
- **Scroll** - Zoom in/out

Everything you do is captured in the final video. When complete, the recording saves automatically.

**Do not close the window early** - let it finish to capture the full history.

## Output Files

After the window closes, check `output/repo-evolution/`:
- `history.mp4` - Recorded repository history video

## Portability

To use on another project:

1. Copy the entire `git-visualizer/` directory
2. Edit `config.sh` with new project settings
3. Run `./run.sh`

## Troubleshooting

### Gource not found
- Install gource: `brew install gource`
- Or let the script install it for you

### Video not generating?
- Install ffmpeg: `brew install ffmpeg`

### Window appears during generation
- This is expected! The window is interactive - you can navigate while it records
- Do not close the window - it will close automatically when complete
