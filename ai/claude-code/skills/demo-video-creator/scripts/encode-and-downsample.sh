#!/usr/bin/env bash
#
# encode-and-downsample.sh — the proven ffmpeg pipeline for a demo video.
# Read this when: you have lossless 8K frames (a PNG sequence) or an 8K master
# and you need to turn them into a delivery 4K and/or README/docs embeds.
#
# WHY master at 8K, deliver at 4K: rendering/capturing at 8K (2x the 4K target)
# and downsampling with a good resampler (lanczos) gives SUPERSAMPLED, razor-sharp
# 4K — every delivery pixel is averaged from four source pixels, so edges, text,
# and UI chrome stay crisp with no shimmer. True 8K files are enormous and barely
# consumed anywhere; 4K is the real delivery target. So: master high, ship 4K.
#
# WHY ffmpeg and NOT Playwright recordVideo: recordVideo's quality is not
# configurable — chromium hardcodes ~1 Mbit/s VP8, mushy at any resolution. The
# real path is a lossless PNG sequence (page.screenshot at a high deviceScaleFactor,
# or a Remotion render) → ffmpeg at any bitrate you want. A captured 8K H.265 at
# crf 14 lands around ~140 Mbit/s — roughly 140x recordVideo's bitrate at 4x the
# pixels. Encode quality is dialed by crf (lower = better/larger), not capped.
#
# Every command below is copy-pasteable. Defaults match the proven run; override
# via args. Requires ffmpeg + ffprobe on PATH.

set -euo pipefail

# --- shared defaults (override per-function via args) ------------------------
FPS="${FPS:-30}"            # master framerate; PNG sequences carry no timing, so set it here
CRF_MASTER="${CRF_MASTER:-14}"   # 8K master quality (lower = sharper/bigger)
CRF_4K="${CRF_4K:-16}"           # 4K delivery quality after downsample
GIF_FPS="${GIF_FPS:-15}"         # README GIFs don't need 30; halve the frames, halve the bytes
GIF_WIDTH="${GIF_WIDTH:-960}"    # GIF width in px; height auto-scales preserving aspect

die() { echo "error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }
need ffmpeg
need ffprobe

# =============================================================================
# (1) encode an 8K lossless PNG sequence -> an 8K master
# =============================================================================
# Input: a directory of zero-padded frames, e.g. frame-0001.png, frame-0002.png …
# (the convention the capture rig writes — page.screenshot per frame).
#
# H.265 (libx265) crf 14 with yuv420p is the delivery-friendly master: tiny vs
# lossless, visually transparent, plays everywhere. yuv420p is the chroma layout
# every player/browser/upload pipeline expects — skip it and some players show a
# green/black frame or refuse the file.
#
# Usage: encode_master <frames_dir> [out.mp4] [glob] [fps] [crf]
#   glob defaults to 'frame-%04d.png' (ffmpeg's printf-style sequence pattern).
encode_master() {
  local frames_dir="${1:?usage: encode_master <frames_dir> [out.mp4] [glob] [fps] [crf]}"
  local out="${2:-master-8k.mp4}"
  local glob="${3:-frame-%04d.png}"
  local fps="${4:-$FPS}"
  local crf="${5:-$CRF_MASTER}"

  [[ -d "$frames_dir" ]] || die "frames dir not found: $frames_dir"

  ffmpeg -y \
    -framerate "$fps" \
    -i "$frames_dir/$glob" \
    -c:v libx265 -crf "$crf" -pix_fmt yuv420p \
    "$out"

  echo "wrote $out"
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,codec_name -of default=nw=1 "$out"
}

# --- ALTERNATIVE: ProRes 4444 edit master ------------------------------------
# Use this when the master feeds a video EDITOR (Premiere/Resolve/Remotion stitch)
# rather than direct delivery. ProRes 4444 is near-lossless intra-frame (every
# frame independently decodable = fast scrubbing) and carries alpha — at the cost
# of being large. Reach for it as the edit/intermediate master; keep H.265 above
# as the deliverable master.
#
# Usage: encode_master_prores <frames_dir> [out.mov] [glob] [fps]
encode_master_prores() {
  local frames_dir="${1:?usage: encode_master_prores <frames_dir> [out.mov] [glob] [fps]}"
  local out="${2:-master-8k.mov}"
  local glob="${3:-frame-%04d.png}"
  local fps="${4:-$FPS}"

  [[ -d "$frames_dir" ]] || die "frames dir not found: $frames_dir"

  ffmpeg -y \
    -framerate "$fps" \
    -i "$frames_dir/$glob" \
    -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le \
    "$out"

  echo "wrote $out"
}

# =============================================================================
# (2) downsample an 8K master -> razor-sharp supersampled 4K delivery
# =============================================================================
# scale=3840:2160 is 4K UHD. flags=lanczos is the high-quality resampler — it's
# what makes the 2x downscale crisp instead of soft; the default bilinear filter
# blurs fine UI text. Re-encode H.265 at crf 16 (delivery quality) with yuv420p.
# This is the exact path the capture POC proved: master 8K, ship 4K.
#
# Works on either master from (1) — the H.265 .mp4 or the ProRes .mov.
#
# Usage: downsample_4k <master> [out.mp4] [crf]
downsample_4k() {
  local master="${1:?usage: downsample_4k <master> [out.mp4] [crf]}"
  local out="${2:-delivery-4k.mp4}"
  local crf="${3:-$CRF_4K}"

  [[ -f "$master" ]] || die "master not found: $master"

  ffmpeg -y \
    -i "$master" \
    -vf "scale=3840:2160:flags=lanczos" \
    -c:v libx265 -crf "$crf" -pix_fmt yuv420p \
    "$out"

  echo "wrote $out"
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,codec_name -of default=nw=1 "$out"
}

# =============================================================================
# (3) derive README / docs embeds from a clip
# =============================================================================
# README and docs can't autoplay a heavyweight 4K mp4. Two lightweight embeds:
#   - a looping GIF (works literally everywhere GitHub renders markdown)
#   - a muted webm (far smaller + sharper than GIF; use where <video> is allowed)
# Cut these from a SHORT hero clip (a few seconds), not the full video.

# --- a palette-based looping GIF (the only sane way to make a GIF) -----------
# Naive GIF = 256 colors picked globally = banded, muddy, huge. The fix is a
# two-pass palette: palettegen builds an OPTIMAL 256-color palette FROM THIS clip,
# then paletteuse maps frames to it with dithering. Drop fps to ~15 and cap width
# (height = -1 preserves aspect) to keep the file embed-friendly. lanczos again
# for the scale so the downscaled GIF stays sharp.
#
# Usage: make_gif <input_clip> [out.gif] [fps] [width]
make_gif() {
  local input="${1:?usage: make_gif <input_clip> [out.gif] [fps] [width]}"
  local out="${2:-demo.gif}"
  local fps="${3:-$GIF_FPS}"
  local width="${4:-$GIF_WIDTH}"
  local palette
  palette="$(mktemp -t demo-palette-XXXXXX).png"

  # pass 1 — build the optimal palette for THIS clip
  ffmpeg -y -i "$input" \
    -vf "fps=$fps,scale=$width:-1:flags=lanczos,palettegen=stats_mode=diff" \
    "$palette"

  # pass 2 — render the GIF against that palette (dither smooths gradients)
  ffmpeg -y -i "$input" -i "$palette" \
    -lavfi "fps=$fps,scale=$width:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3" \
    "$out"

  rm -f "$palette"
  echo "wrote $out"
}

# --- a muted, looping-friendly webm (VP9) ------------------------------------
# Smaller and far sharper than a GIF; use it where the host allows <video> (docs
# sites, GitHub Pages). -an strips audio (a demo loop is silent). crf 32 / VP9 is
# a good quality:size knock-down for an embed; lower crf for sharper/bigger.
#
# Usage: make_webm <input_clip> [out.webm] [width] [crf]
make_webm() {
  local input="${1:?usage: make_webm <input_clip> [out.webm] [width] [crf]}"
  local out="${2:-demo.webm}"
  local width="${3:-1280}"
  local crf="${4:-32}"

  ffmpeg -y -i "$input" \
    -vf "scale=$width:-2:flags=lanczos" \
    -c:v libvpx-vp9 -crf "$crf" -b:v 0 -an \
    "$out"

  echo "wrote $out"
}

# =============================================================================
# dispatch — run a single function from the CLI, or source this file to use them
# =============================================================================
# Examples:
#   ./encode-and-downsample.sh encode_master ./frames master-8k.mp4
#   ./encode-and-downsample.sh downsample_4k master-8k.mp4 delivery-4k.mp4
#   ./encode-and-downsample.sh make_gif hero-clip.mp4 docs/hero.gif
#   # full chain (8K capture -> 4K -> GIF) for a typical README hero:
#   ./encode-and-downsample.sh encode_master ./frames master-8k.mp4 \
#     && ./encode-and-downsample.sh downsample_4k master-8k.mp4 delivery-4k.mp4 \
#     && ./encode-and-downsample.sh make_gif delivery-4k.mp4 hero.gif
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:-}"
  case "$cmd" in
    encode_master|encode_master_prores|downsample_4k|make_gif|make_webm)
      shift; "$cmd" "$@" ;;
    ""|-h|--help|help)
      grep -E '^(# Usage:|encode_master|encode_master_prores|downsample_4k|make_gif|make_webm)\b' "$0" \
        | sed -E 's/\(\) \{//' >&2
      echo >&2
      echo "run a function:  $0 <function> [args…]   (or 'source $0' to load them)" >&2 ;;
    *)
      die "unknown command: $cmd (try: $0 --help)" ;;
  esac
fi
