# Remotion as the polish layer (over real footage, never recreation)

Purpose: how to use Remotion to POLISH a demo — captions, callouts, transitions, intro/outro, speed-ramps — laid OVER the real captured footage, synced to the run's real trace timestamps, rendered at 8K.

Read this when: you have real captured footage (the capture step is done) and need to assemble it into a finished video, OR you're scaffolding the composition before footage exists so the data-wiring is a no-code swap later.

## The one rule: polish, never recreate

Remotion's job is to compose, annotate, and pace the REAL footage you captured of the real surfaces. It does NOT rebuild those surfaces as React. The moment you recreate a dashboard or a GitHub page in JSX, the demo stops being real and becomes a mockup — which defeats the entire "fake exactly one thing" philosophy. The footage is sacred; Remotion only adds the layer a human editor would add in a timeline: lower-thirds, "what just happened" badges, cross-cuts, a title card, and deliberate pacing.

(Recreation is sometimes the documented escape hatch for a single surface you genuinely cannot capture — e.g. a logged-in chat app behind QR auth. Treat it as a last resort, render it from the surface's REAL data, and prefer deferring that one beat over faking it.)

The established lineage: capture UI flows with Playwright (lossless screenshots, never `recordVideo`), then polish with Remotion. The **Remotion Recorder** template is purpose-built for exactly this — base footage plus programmatic B-roll, captions, transitions, branding — and is the natural starting point.

## Architecture: a generic, data-driven composition

Structure the project so NOTHING about the specific demo lives in the React components. The components are a generic rendering engine; two data files describe the actual video. This is what makes the footage handoff and the look-tuning each a one-file change.

```
remotion/
├── data/
│   ├── timeline.ts              THE timeline data — every beat as data
│   ├── timeline.timings.json    real trace timings (generated, see below)
│   └── load-trace-timings.mjs   reads the run's DB → writes the timings JSON
├── public/footage/<beat>/       real captured PNG sequences drop in here
├── src/
│   ├── Root.tsx                 registers the composition; resolution env-driven
│   ├── DemoVideo.tsx            sequences intro + beats + outro on the timeline
│   ├── theme/tokens.ts          DESIGN TOKENS — the human's iteration surface
│   ├── beats/BeatScene.tsx      composites ONE beat; generic for all beats
│   └── components/
│       ├── SurfaceFootage.tsx   the real-footage slot (PNG seq / still / mp4)
│       ├── CaptionLowerThird.tsx
│       ├── FeatureCallout.tsx
│       ├── Transition.tsx       cut / fade / slide cross-surface transitions
│       └── IntroOutro.tsx       title cards (intro + outro hero)
```

`DemoVideo.tsx` maps over the beats and drops each into a `<Sequence>` placed at `intro + beat.startSec` for `beat.durationSec`; `BeatScene.tsx` layers a single beat (footage at the back, transition on top of that, then captions, then callouts). Both read entirely from `timeline.ts` + `tokens.ts`. Adding or retiming a beat is a data edit; the total frame count derives from the data, so duration updates with no code change.

## 1. The timeline data file — the single source

One file declares each beat as a record: which real surface the viewer sees, the footage slot backing it, its captions and callouts, and its start/duration. The components render whatever is here. Concretely:

```ts
export interface Beat {
  n: number;                  // beat number
  id: string;                 // stable slug — also the footage dir + timing key
  surface: 'dashboard' | 'github' | 'telegram' | 'cli';
  startSec: number;           // placeholder until real timings overlay it
  durationSec: number;
  footage: { surface; src: string | null; frameCount?: number; placeholderLabel: string };
  captions: { kicker: string; text: string; atSec?: number; holdSec?: number }[];
  callouts: { label: string; status?: 'ok' | 'info' | 'warn'; atSec?: number; holdSec?: number }[];
  transitionIn?: 'cut' | 'fade' | 'slide';
}
```

Write the caption/callout TEXT from the REAL take (the real issue title, the real owner reply, the real `/approve`) — not lorem ipsum — so even the placeholder preview reads like the actual demo. Bookend the beats with a small `intro` and `outro` record (the outro can use a captured hero still as a dimmed backdrop).

## 2. Real trace timings drive WHEN overlays land

Hand-aligning overlays to footage is the classic editing pain. Skip it entirely: the run already emitted a timestamped trace (events, state transitions, decision points) into its DB. Export those real timestamps and let them position every overlay, so captions land on the exact real moment a feature fired.

A small loader script (`load-trace-timings.mjs`) reads the run's file DB READ-ONLY, finds each beat's real anchor moment, and writes `timeline.timings.json`. The timeline file imports that JSON and overlays the real `startSec`/`durationSec` onto the readable literals (literals stay as a working fallback; the JSON is the source of truth for timing):

```ts
import timings from './timeline.timings.json';
const realById = new Map(timings.beats.map((b) => [b.id, b]));
for (const beat of beats) {
  const real = realById.get(beat.id);
  if (real) { beat.startSec = real.startSec; beat.durationSec = real.durationSec; }
}
```

Key moves in the loader:
- **Map each beat to a real anchor predicate** — beat N → a specific transition/event/decision (e.g. `block` → the `active→blocked(awaiting_human)` transition; `merge` → the `pr_merged` event; `auto-skip` → the `skip:research` decision). Document the mapping in the script's header.
- **Fail loudly if any anchor is missing** — a missing anchor means that feature never fired in the take, i.e. an incomplete run. Don't silently paper over it.
- **Preserve real ORDER, clamp the HOLDS.** Raw poll-interval gaps are tight and uneven. Keep the real relative ordering, derive each hold from the real gap (scaled), but clamp to a watchable `[MIN_HOLD, MAX_HOLD]` window and lay beats back-to-back. Carry the real wall-clock anchor (`atISO`) so any later re-pacing can re-derive from ground truth.

Re-running the loader after a fresh take re-syncs the whole video. Final fine-pacing is still Remotion's to tune.

## 3. Design tokens — the human's one iteration surface

Isolate ALL taste in one clearly-marked file: color, type, spacing, motion, canvas sizes. Components import from it and never hardcode a color, size, or duration. This is deliberate division of labor: the machine owns the structure, the human owns the look — and the human retunes the entire video by editing this one object.

Ship NEUTRAL, legibility-first defaults (grayscale brand/accent, system font stack, calm linear motion) explicitly marked as placeholders, not decisions. The human then iterates palette, typeface, motion personality, hero treatment, and letterbox against real renders, section by section. Motion durations live in FRAMES at the project fps so they're consistent across resolutions. Keep contrast high — captions sit over busy real footage, so include a scrim token and let legibility win every tie.

Do NOT bake in richer transitions (`@remotion/transitions` `TransitionSeries`), speed-ramps, or a signature motion feel as defaults — those are look decisions, surfaced as a later human-driven step.

## 4. Resolution is env-driven (draft → 4K → 8K)

Register the composition once, sized from an env var, so the SAME composition renders at every target. A fast low-res DRAFT for iteration; 4K for delivery; 8K for the master.

```ts
const QUALITY = (process.env.REMOTION_QUALITY ?? 'draft') as keyof typeof CANVAS;
const { width, height } = CANVAS[QUALITY] ?? CANVAS.draft;
// CANVAS = { draft: 1280x720, delivery: 3840x2160, master: 7680x4320 }
```

Iterate at draft (seconds per render); only render 4K/8K when you actually need to inspect or ship. Tokens reference sizes at a 1080-tall design reference and scale by canvas height, so layouts hold at every resolution.

## 5. Render flow: 8K master → 4K delivery → embeddable loop

Render the master at 8K ProRes, downsample to a razor-sharp supersampled 4K for delivery, then derive a small looping asset for README/docs embedding:

```bash
# 8K MASTER (ProRes 4444) — slow + huge; render once
REMOTION_QUALITY=master npx remotion render DemoVideo out/demo-8k.mov \
  --codec=prores --prores-profile=4444 --concurrency=2

# downsample to supersampled 4K delivery (lanczos)
ffmpeg -i out/demo-8k.mov -vf scale=3840:2160:flags=lanczos \
  -c:v libx265 -crf 16 -pix_fmt yuv420p out/demo-4k.mp4

# derive a muted, looping webm / GIF for README + docs hero
ffmpeg -i out/demo-4k.mp4 -an -vf scale=1280:-2 -c:v libvpx-vp9 -crf 32 -b:v 0 out/demo-loop.webm
```

Remotion renders ProRes/H.265 at any bitrate, so there is no quality ceiling on the render side either (mastering at 8K then downsampling buys you supersampled sharpness at the delivery resolution). True 8K files are enormous and barely consumed — 4K is the real delivery target.

## 6. The footage handoff: a zero-component-change swap

Scaffold the whole composition BEFORE footage exists, using a placeholder stand-in. `SurfaceFootage.tsx` renders a clearly-marked, drab placeholder (solid tint + label + hatch, so it never reads as a design choice) whenever `footage.src` is null. When capture lands, drop each beat's lossless PNGs into `public/footage/<beat>/` as `frame-0001.png …` and flip that beat's `src` from `null` to `'footage/<beat>/'`. No component changes — the slot plays a single still (`frameCount: 1`, held for the beat) or a multi-frame sequence (`<Series>`), with a commented `<OffthreadVideo>` branch for clip-style mp4s.

This lets you build, render, and review the entire video on placeholders, then make it real one data line at a time. Defer-by-design works too: if one surface can't be captured yet, leave its `src` null and it renders an obvious placeholder rather than blocking the cut.

## Why this holds together

Two data files (timeline + tokens) and one generic component tree mean: the content/timing changes in one place, the look changes in another, and the real footage slots in without touching code. The real trace timestamps remove the hand-sync pain, the env-driven resolution makes iteration cheap and delivery pristine, and the polish-only discipline keeps every frame the viewer sees genuinely real — exactly one thing was ever faked, and it isn't on screen.
