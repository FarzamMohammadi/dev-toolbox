# Music Selection Guide

## Why Music Matters
Music drives the entire demo rhythm. Animations sync to beats. Scene transitions land on downbeats. The right track sets the emotional tone before a single word is read.

## How to Choose

### 1. Match the Mood
| Mood | BPM Range | Genre Examples |
|------|-----------|----------------|
| Thoughtful, elegant | 70-95 | Lo-fi, ambient, piano |
| Confident, professional | 95-115 | Synth-pop, indie electronic |
| Energetic, exciting | 115-135 | Synthwave, electro, indie rock |
| Intense, dramatic | 135+ | EDM, drum & bass, industrial |

### 2. Instrumental Only
Lyrics compete with your text content. Always choose instrumental tracks or tracks with minimal vocals.

### 3. Strong Beat Structure
The beat analysis script needs clear rhythmic patterns. Look for:
- Clear kick drum or bass hits
- Consistent tempo (no tempo changes)
- Defined sections (intro, verse, chorus)

### 4. Duration
Match your target demo length:
- 30s demo → find a 30-45s segment or a short track
- 60s demo → most tracks work, use intro through first chorus
- 90s+ → use a longer section or the full track

## Where to Find Music

### Free (No License Needed)
- **YouTube Audio Library** — huge selection, free for any use
- **Pixabay Music** — royalty-free, no attribution needed
- **Free Music Archive** — Creative Commons tracks

### Paid (Higher Quality, Cleaner Licenses)
- **Artlist** — subscription, unlimited downloads
- **Epidemic Sound** — subscription, great curation
- **Musicbed** — premium tracks

### Tips
- Search for "synthwave instrumental" or "cinematic electronic" for tech demos
- Aaron Francis used "First Night in Paris" by The Midnight — that synthwave vibe works great for dev tools
- Download the track, place it in the `audio/` directory
- If the track is too long, trim it with ffmpeg:
  ```
  ffmpeg -i audio/original.mp3 -ss 0 -t 60 audio/track.mp3
  ```

## Workflow
1. Browse music sources, find 2-3 candidates
2. Listen to each while imagining your demo scenes
3. Pick the one that makes you feel the energy you want the viewer to feel
4. Download and place in `audio/`
5. Run beat analysis: `npm run beats -- audio/track.mp3`
6. Review `output/beats.json` to see BPM and beat structure
