# Demo Generator

Generate animated web-based demo videos with Claude. No motion graphics software needed — Claude builds beat-synced scene web apps that you screen-record and assemble into polished demo videos.

> Inspired by [Aaron Francis's approach](https://x.com/aarondfrancis/status/2019864355039269128) to creating his Solo launch video entirely with Claude.

## Quick Start

```bash
# Install dependencies
npm install

# Check external tools
npm run check

# Install Python deps (for beat analysis)
uv sync

# Start a Claude session in this directory
# Tell Claude what you want to demo — it handles the rest
```

## How It Works

1. You `cd demo-generator` and start a Claude session
2. Provide your topic and context (blog post, product docs, README)
3. Claude reads the `CLAUDE.md` instructions and walks you through a 7-phase workflow:
   - **Intake** — Gather topic, audience, tone, music
   - **Beat Analysis** — Analyze music beats with librosa for animation sync
   - **Scene Design** — Design scenes with narrative arc (hook → problem → solution → demo → results → CTA)
   - **Build** — Generate standalone HTML scene files with Motion.dev animations
   - **Review** — Open scenes in browser, fine-tune timing with the HUD
   - **Record** — Screen-record each scene (Claude guides you step by step)
   - **Assemble** — Combine recordings with music in a video editor

Each scene is a standalone HTML file. No build tools, no React — just open in a browser and press play.

## What's Inside

```
scaffolding/
├── js/
│   ├── beat-sync.js          # Beat timeline and scheduling
│   ├── scene-controller.js   # Scene lifecycle (play/pause/restart)
│   ├── hud.js                # Fine-tuning overlay (H to toggle)
│   └── animations/
│       ├── text-scramble.js   # Character-by-character decode
│       ├── typewriter.js      # Terminal typing effect
│       ├── svg-tracer.js      # SVG path drawing with glow
│       ├── ripple.js          # Expanding concentric circles
│       ├── fade-slide.js      # Directional fade entrance
│       └── counter.js         # Number counting animation
├── styles/
│   ├── core.css              # Typography, layout, CSS variables
│   └── effects.css           # Glow, neon, scanlines, glass, gradients
└── base.html                 # Base scene template
```

Animation engine uses [Motion.dev](https://motion.dev/) free tier (MIT, 2.3kb) via CDN. Text scramble is a custom implementation replacing paid plugins.

## Requirements

| Tool | Purpose | Install |
|------|---------|---------|
| Node.js >= 18 | Dev server | `brew install node` |
| Python 3 >= 3.10 | Beat analysis | `brew install python3` |
| uv | Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ffmpeg | Audio conversion | `brew install ffmpeg` |

### Optional

| Tool | Purpose |
|------|---------|
| Screen recorder | QuickTime (built-in), OBS (free), or ScreenFlow |
| Video editor | iMovie (built-in), DaVinci Resolve (free), or ScreenFlow |

Run `npm run check` to verify what's installed.

## Guides

- [Music Selection](./guides/music-selection.md) — How to pick the right track
- [Recording](./guides/recording.md) — Screen recording walkthrough
- [Assembly](./guides/assembly.md) — Final video editing guide
