# Git Visualizer

A standalone tool for generating animated git repository history visualizations using gource.

## Quick Start

```bash
# Edit config if needed
vim config.sh

# Run (handles everything: tool checking, installation, video generation)
./run.sh

# Check output
ls output/gource/
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
│   └── gource/              # history.mp4
├── README.md                 # This file
└── .gitignore
```

## Configuration

Edit `config.sh`:

| Option | Default | Description |
|--------|---------|-------------|
| `PROJECT_NAME` | - | Project name for titles |
| `GOURCE_TITLE` | `${PROJECT_NAME} Evolution` | Title in visualization |
| `GOURCE_RESOLUTION` | `"800x600"` | Window size (WxH) |
| `GOURCE_SECONDS_PER_DAY` | `"0.5"` | Playback speed (lower = faster) |
| `GOURCE_VIDEO_DURATION` | `60` | Video length in seconds. Use `-1` for full history |
| `GOURCE_LIVE_PREVIEW` | `"false"` | `"true"` = live window, `"false"` = export video |

**Note:** If video doesn't capture full git history, increase `GOURCE_VIDEO_DURATION` in config.sh.

## Output Files

After running, check the `output/gource/` directory:
- `history.mp4` - Animated repository history video

## Portability

To use on another project:

1. Copy the entire `git-visualizer/` directory
2. Edit `config.sh` with new project settings
3. Run `./run.sh`

## Troubleshooting

### Gource not found
- Install gource: `brew install gource`
- Or let the script install it for you

### No video generated (live preview only)
- Install ffmpeg: `brew install ffmpeg`
- Or set `GOURCE_LIVE_PREVIEW="true"` in config.sh for live preview mode

### Video generation window appears
- This is expected! Gource requires OpenGL rendering
- Do not close the window - it will close automatically when complete
