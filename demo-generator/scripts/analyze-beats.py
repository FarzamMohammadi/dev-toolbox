#!/usr/bin/env python3
"""
Beat Analysis Script
Analyzes an audio file to detect beats, onsets, and sections.
Outputs a beats.json file for the scene beat-sync system.

Usage:
  uv run python scripts/analyze-beats.py audio/track.mp3
  uv run python scripts/analyze-beats.py audio/track.wav --output output/beats.json
"""

import argparse
import json
import sys
from pathlib import Path

import librosa
import numpy as np


def analyze(audio_path: str, output_path: str = "output/beats.json") -> dict:
    """Analyze audio file and return beat data."""
    print(f"Loading audio: {audio_path}")
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Duration: {duration:.1f}s | Sample rate: {sr}Hz")

    # Beat tracking
    print("Detecting beats...")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # Handle tempo - it may be an array in newer librosa versions
    bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])
    print(f"BPM: {bpm:.1f} | Beats detected: {len(beat_times)}")

    # Onset detection (more granular than beats - captures percussive hits)
    print("Detecting onsets...")
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr).tolist()
    print(f"Onsets detected: {len(onset_times)}")

    # Downbeats (every 4th beat, assuming 4/4 time)
    downbeats = [beat_times[i] for i in range(0, len(beat_times), 4)]

    # Simple section detection via spectral clustering
    print("Detecting sections...")
    sections = detect_sections(y, sr, duration)

    result = {
        "bpm": round(bpm, 1),
        "duration": round(duration, 3),
        "beat_times": [round(t, 3) for t in beat_times],
        "onset_times": [round(t, 3) for t in onset_times],
        "downbeats": [round(t, 3) for t in downbeats],
        "sections": sections,
        "total_beats": len(beat_times),
        "total_onsets": len(onset_times),
    }

    # Write output
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nWrote: {out}")
    print(f"  BPM: {result['bpm']}")
    print(f"  Duration: {result['duration']}s")
    print(f"  Beats: {result['total_beats']}")
    print(f"  Sections: {len(result['sections'])}")
    return result


def detect_sections(y, sr, duration):
    """Detect musical sections using spectral features."""
    try:
        # Use spectral contrast changes to find section boundaries
        hop_length = 512
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
        bounds = librosa.segment.agglomerative(chroma, k=min(6, max(2, int(duration / 15))))
        bound_times = librosa.frames_to_time(bounds, sr=sr, hop_length=hop_length).tolist()

        sections = []
        labels = ["intro", "verse", "chorus", "bridge", "outro", "section"]
        for i in range(len(bound_times)):
            start = round(bound_times[i], 3)
            end = round(bound_times[i + 1], 3) if i + 1 < len(bound_times) else round(duration, 3)
            label = labels[i] if i < len(labels) else f"section_{i + 1}"
            sections.append({"start": start, "end": end, "label": label})

        return sections
    except Exception as e:
        print(f"Section detection warning: {e}")
        return [{"start": 0, "end": round(duration, 3), "label": "full"}]


def main():
    parser = argparse.ArgumentParser(description="Analyze audio beats for demo-generator")
    parser.add_argument("audio_file", help="Path to audio file (mp3, wav, flac, ogg)")
    parser.add_argument("--output", "-o", default="output/beats.json", help="Output JSON path")
    args = parser.parse_args()

    if not Path(args.audio_file).exists():
        print(f"Error: File not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    analyze(args.audio_file, args.output)


if __name__ == "__main__":
    main()
