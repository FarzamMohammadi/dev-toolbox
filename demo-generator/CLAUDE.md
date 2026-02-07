# Demo Generator

Generate animated web-based demo videos for any topic. The user provides context about what they're working on. You design creative scenes, build them as web apps, and guide the user through recording.

Inspired by Aaron Francis's approach: Claude builds web apps with animated scenes synced to music beats. The user screen-records each scene. Final assembly happens in a video editor.

---

## Principles

1. **Every demo is unique.** Study the topic deeply. Find the most compelling visual metaphors. Never produce cookie-cutter output. The scaffolding provides animation primitives — your creativity composes them differently every time.

2. **Guide the user at every step.** The user does not want to learn the internals. Walk them through everything: what to install, what to click, when to record, how to assemble. Be specific and concrete.

3. **Plans before code.** Always present the scene plan and get approval before building any HTML files. The user must see exactly what each scene will contain before you write a line.

4. **Keep it simple.** No build tools. No React. Plain HTML files served locally. The user opens a browser, presses play, and records.

---

## Phase 1: Intake

When the user activates you in this directory, begin here.

### Clean Up

If there are existing files in `output/` from a previous project, run:

```bash
npm run clean
```

This removes generated HTML, Markdown, and JSON files from `output/`, giving you a fresh start. Confirm with the user before running if you see existing output files.

### Gather

Ask the user for:

1. **Topic**: What is the demo about? (product launch, blog post, concept, tutorial)
2. **Context source**: Path to the content (blog post, README, docs). Read it thoroughly. Extract key concepts, technical terms, visual elements, data points, workflow steps, comparisons.
3. **Target audience**: Developers? General public? Decision-makers?
4. **Key messages**: What 3-5 things must the viewer take away?
5. **Tone**: Professional, playful, dramatic, minimal, cyberpunk, elegant?
6. **Duration target**: 30s, 60s, 90s?
7. **Music**: Do they have a track? If yes, have them place it in `audio/`. If no, point them to `guides/music-selection.md` and help them choose.

### Read and Extract

Read the context source files. Identify:

- The core problem being solved
- The "aha moment" — what makes this exciting
- Visual concepts that could be animated (architecture diagrams, data flows, transformations, before/after)
- Specific numbers, stats, or metrics worth highlighting
- Technical terms that look cool when scrambled/typed

### Output

Write a project brief to `output/project-brief.md` with your analysis. Confirm with the user before proceeding.

---

## Phase 2: Beat Analysis

### If Music Is Provided

1. Check dependencies:
   ```bash
   bash setup/check-dependencies.sh
   ```

2. If ffmpeg conversion is needed (non-WAV input is fine for librosa, but if issues arise):
   ```bash
   ffmpeg -i audio/[filename] -ar 22050 -ac 1 audio/track.wav
   ```

3. Run beat analysis:
   ```bash
   uv run python scripts/analyze-beats.py audio/[filename]
   ```

4. Present the results:
   - BPM and total beats
   - Detected sections with timestamps
   - Suggested scene boundaries based on musical sections
   - Total duration

### If No Music

Create fixed beats. The scenes will use `createFixedBeats()` from `beat-sync.js`:

```javascript
const beats = createFixedBeats({ bpm: 120, duration: 30 });
```

Tell the user they can always add music later and re-sync.

---

## Phase 3: Scene Design

### Narrative Arc

Design scenes following a narrative arc. Not every demo needs all types — choose what fits:

1. **Hook** (3-8s) — Grab attention. See `templates/scene-plans/hook.md`
2. **Problem** (5-15s) — Show the pain. See `templates/scene-plans/problem.md`
3. **Solution** (10-30s) — Introduce what was built. See `templates/scene-plans/solution.md`
4. **Demo** (15-45s) — Show it working. See `templates/scene-plans/demo.md`
5. **Results** (5-15s) — Metrics and outcomes. See `templates/scene-plans/results.md`
6. **CTA** (3-8s) — Call to action. See `templates/scene-plans/cta.md`

Read the relevant template files before designing each scene. They contain specific guidance on content formulas, animation choices, and beat alignment.

### Be Creative

This is where your design skills matter. For each demo, think about:

- **Visual metaphor**: What does this topic *look like*? Receipt processing = chaos → order. Dev tools = terminal magic. AI = data flowing through networks.
- **Color palette**: Match the mood. Cyberpunk neons? Clean minimal whites? Warm gradients? Each demo should have a distinct visual identity.
- **Animation variety**: Don't use the same animation type for every scene. Mix text-scramble, typewriter, SVG tracing, counters, ripples. The variety keeps viewers engaged.
- **Pacing**: Fast scenes for energy, slow scenes for impact. Vary the rhythm.
- **Surprise moments**: One unexpected visual per demo — something the viewer didn't see coming.

### Document the Plan

For each scene, write to `output/scene-plan.md`:

```markdown
## Scene [N]: [Name]
- **Type**: hook / problem / solution / demo / results / cta
- **Duration**: Xs
- **Text content**: [exact strings that will display]
- **Visual elements**: [background, colors, layout, effects]
- **Animations**:
  - [element] → [animation type] at beat [N] ([T]s)
  - [element] → [animation type] at beat [N] ([T]s)
- **Mood/notes**: [creative direction notes]
```

> **Beat numbering**: Use LOCAL beat indices per scene, starting from 0. Each scene file has its own independent BeatTimeline that starts at beat 0 / time 0s. Do NOT use global beat numbers across the full demo. Including the time in seconds (e.g., "at beat 4 (2.0s)") helps verify alignment during implementation.

### Quality Gate

Present the full scene plan to the user. Do NOT proceed to building until they explicitly approve it. Ask:
- Does this capture what you want to show?
- Any text changes?
- Happy with the scene count and flow?

---

## Phase 4: Build Scenes

### Setup

Ensure the dev server is ready:

```bash
npm install
npm run dev
```

The server runs at `http://localhost:3000` and serves the project root. Scene files are at `http://localhost:3000/output/[filename].html`.

### Build Each Scene

For each scene in the approved plan:

1. Create `output/[NN]-[scene-name].html`
2. Start from `scaffolding/base.html` as the structural reference
3. Include these in the `<head>`:
   ```html
   <link rel="stylesheet" href="../scaffolding/styles/reset.css">
   <link rel="stylesheet" href="../scaffolding/styles/core.css">
   <link rel="stylesheet" href="../scaffolding/styles/effects.css">
   ```
4. Import Motion.dev and scaffolding modules:
   ```javascript
   import { animate, stagger } from "https://cdn.jsdelivr.net/npm/motion@12/+esm";
   import { BeatTimeline, loadBeats, createFixedBeats } from "../scaffolding/js/beat-sync.js";
   import { initScene } from "../scaffolding/js/scene-controller.js";
   import { initHUD } from "../scaffolding/js/hud.js";
   ```
5. Import relevant animation modules:
   ```javascript
   import { scrambleText } from "../scaffolding/js/animations/text-scramble.js";
   import { typewrite } from "../scaffolding/js/animations/typewriter.js";
   import { traceSVG } from "../scaffolding/js/animations/svg-tracer.js";
   import { ripple } from "../scaffolding/js/animations/ripple.js";
   import { fadeSlide } from "../scaffolding/js/animations/fade-slide.js";
   import { countUp } from "../scaffolding/js/animations/counter.js";
   ```
6. Wire up the scene controller and HUD
7. Implement the animations per the scene plan
8. Handle `scene.onRestart()` to reset all elements for replay

### Scene File Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scene: [Name]</title>
  <link rel="stylesheet" href="../scaffolding/styles/reset.css">
  <link rel="stylesheet" href="../scaffolding/styles/core.css">
  <link rel="stylesheet" href="../scaffolding/styles/effects.css">
  <style>/* Scene-specific styles */</style>
</head>
<body>
  <div id="scene" class="scene">
    <!-- Scene content -->
  </div>
  <div id="hud"></div>
  <script type="module">
    import { animate, stagger } from "https://cdn.jsdelivr.net/npm/motion@12/+esm";
    import { BeatTimeline, createFixedBeats } from "../scaffolding/js/beat-sync.js";
    import { initScene } from "../scaffolding/js/scene-controller.js";
    import { initHUD } from "../scaffolding/js/hud.js";
    // Import animation modules as needed

    const scene = initScene({ name: '[Name]', duration: [N] });
    const beats = createFixedBeats({ bpm: 120, duration: scene.duration });
    // OR: const beats = await loadBeats('beats.json');
    const timeline = new BeatTimeline(beats);
    initHUD(scene, timeline);

    scene.onPlay(() => {
      // Animation sequence
    });

    scene.onRestart(() => {
      // Reset elements
    });
  </script>
</body>
</html>
```

### Important Notes

- Each scene file must be **self-contained** and work by navigating to it in the browser
- Use relative paths to scaffolding: `../scaffolding/...`
- Pin Motion.dev to `@12` (not `@latest`) for stability
- All elements that animate should start with `opacity: 0` (use `.hidden` class) and be revealed by animations
- Test each scene in the browser before moving to the next

> **Beat index convention**: `timeline.at(index)` is 0-indexed. Beat 0 is the first beat of the scene (time 0s). If your scene plan says "at beat 4 (2.0s)", use `timeline.at(3, ...)`. Alternatively, `timeline.atTime(seconds)` schedules by absolute time within the scene, which avoids index math: `timeline.atTime(2.0, ...)`.

### Animation Cleanup in onRestart()

Each animation primitive requires specific cleanup to avoid stale state on replay. Store animation instances in variables and clean them up in `onRestart()`:

| Animation | Cleanup required |
|-----------|-----------------|
| `scrambleText` | Call `.cancel()` to clear the interval timer. Reset `element.textContent` to original value. |
| `typewrite` / `typewriteLines` | Call `.cancel()` to stop the timeout chain and remove the cursor element. Clear `element.textContent`. For `typewriteLines`, also remove dynamically created `<div>` children from the container via `container.innerHTML = ''`. |
| `ripple` | Remove SVG elements from the DOM: `container.querySelectorAll('svg').forEach(el => el.remove())`. Each `ripple()` call appends a new SVG overlay; without removal they accumulate. |
| `countUp` | Call `.cancel()` to stop the requestAnimationFrame loop. Reset `element.textContent`. |
| `fadeSlide` / `fadeSlideOut` | Reset `element.style.opacity = '0'` and `element.style.transform = ''`. |
| `traceSVG` | Reset path elements: set `pathLength` style back to 0, remove glow filters if added. |

**Example pattern:**
```javascript
let scramble1, typer1, counter1;

scene.onPlay(() => {
  scramble1 = scrambleText(titleEl, { duration: 1200 });
  scramble1.play();
  // ...
});

scene.onRestart(() => {
  scramble1?.cancel();
  typer1?.cancel();
  counter1?.cancel();
  // Remove ripple SVGs
  rippleContainer.querySelectorAll('svg').forEach(el => el.remove());
  // Reset all animated elements
  document.querySelectorAll('[data-animate]').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = '';
  });
});
```

---

## Phase 5: Review and Refine

### Guide the User

For each scene:

1. Tell them: "Open http://localhost:3000/output/[NN]-[scene-name].html in Chrome"
2. Tell them: "Press Space to play, R to restart, H to hide the HUD"
3. Ask: "Does the timing feel right? Any text changes? Want different colors?"
4. Make adjustments based on feedback
5. Tell them to use the speed controls (0.25x, 0.5x) to check details

### Self-Check Before Presenting

Before showing the user each scene, verify:
- No console errors in the browser
- All text is readable (contrast, size, timing)
- Animations complete within the scene duration
- HUD works (play/pause/restart)
- Restart cleanly resets everything for replay

---

## Phase 6: Recording (Automated)

Use the automated recorder as the default. It renders each scene to a deterministic 1080p 60fps MP4 by virtualizing all browser timing APIs and capturing frame-by-frame.

### Prerequisites

- Dev server running: `npm run dev` (in a separate terminal)
- ffmpeg installed: `brew install ffmpeg`
- Puppeteer installed: `npm install` (one-time)

### Run

```bash
npm run record                     # record all scenes
npm run record -- --scene 01       # record a single scene
npm run record -- --fps 30         # lower fps (faster, smaller files)
npm run record -- --width 1920 --height 1080  # custom resolution
```

Output MP4s land in `output/` alongside the HTML files (e.g. `output/01-hook.mp4`).

### How It Works

The recorder injects a virtual clock before page JS runs, overriding `performance.now()`, `Date.now()`, `requestAnimationFrame`, `setTimeout`, `setInterval`, and `Element.prototype.animate` (WAAPI). Every frame advance is deterministic — no timing drift, no dropped frames.

This covers all animation types in the project:
- **JS-timed**: `scrambleText` (setInterval + performance.now), `typewrite` (setTimeout chain), `countUp` (rAF + performance.now)
- **WAAPI-based**: `fadeSlide`, `ripple`, `traceSVG` (Motion.dev's `animate()` → Element.prototype.animate)
- **Scene/timeline**: `scene-controller` and `BeatTimeline` (rAF + performance.now)

### After Recording

Check the MP4s play correctly — animations should be smooth and match what you see in the browser. If a single scene needs re-recording, use `--scene NN` to redo just that one.

### Fallback: Manual Recording

If automated recording isn't working for a particular scene, fall back to manual screen recording:

1. "Open Chrome and go to http://localhost:3000/output/01-hook.html"
2. "Press Cmd+Shift+F to go fullscreen"
3. "Press H to hide the HUD"
4. "Open QuickTime > File > New Screen Recording (or your preferred recorder)"
5. "Start recording"
6. "Press Space to play the scene"
7. "Wait for it to finish, then stop recording"
8. "Save the file. Let's do the next scene."

### Key Points
- Record WITHOUT audio — music is added in assembly as one continuous track
- Each scene is recorded separately for flexibility
- If a recording is bad, just redo that one scene

---

## Phase 7: Assembly

Guide the user through video editing. Read `guides/assembly.md`, then walk them through:

1. Import all recordings into their video editor
2. Import the music track
3. Arrange scenes in order on the timeline
4. Trim the padding at the start/end of each recording
5. Align cuts to beat boundaries (reference `output/beats.json`)
6. Export as 1080p MP4

---

## Animation Primitives Reference

### text-scramble
```javascript
import { scrambleText, scrambleStagger } from "../scaffolding/js/animations/text-scramble.js";
const s = scrambleText(element, { duration: 1500, characters: 'ABC...xyz' });
s.play();
await s.promise;
```

### typewriter
```javascript
import { typewrite, typewriteLines } from "../scaffolding/js/animations/typewriter.js";
const tw = typewrite(element, "Hello, world!", { speed: 50, cursor: true });
tw.play();
await tw.promise;
```

### svg-tracer
```javascript
import { traceSVG } from "../scaffolding/js/animations/svg-tracer.js";
traceSVG(svgElement, { duration: 2, glowColor: '#06b6d4', stagger: 0.3 }, animate);
```

### ripple
```javascript
import { ripple } from "../scaffolding/js/animations/ripple.js";
const r = ripple(container, { count: 3, duration: 1.5, color: 'rgba(59,130,246,0.4)' }, animate);
r.play();
```

### fade-slide
```javascript
import { fadeSlide, fadeSlideOut } from "../scaffolding/js/animations/fade-slide.js";
fadeSlide('.items', { direction: 'up', stagger: 0.1 }, animate);
```

### counter
```javascript
import { countUp } from "../scaffolding/js/animations/counter.js";
const c = countUp(element, 0, 97, { duration: 1500, suffix: '%' });
c.play();
await c.promise;
```

### Motion.dev (direct)
```javascript
import { animate, stagger } from "https://cdn.jsdelivr.net/npm/motion@12/+esm";

// Single element
animate(element, { opacity: [0, 1], y: [20, 0] }, { duration: 0.6 });

// Sequence/timeline
animate([
  [".title", { opacity: 1 }, { duration: 0.5 }],
  [".subtitle", { opacity: 1, y: [20, 0] }, { duration: 0.5, at: "+0.2" }],
  [".logo path", { pathLength: [0, 1] }, { duration: 1.5, at: "+0.3" }],
]);

// Stagger
animate(".items", { opacity: [0, 1] }, { delay: stagger(0.1) });

// SVG path drawing
animate("path", { pathLength: [0, 1] }, { duration: 2 });
```

**Timing "at" options:**
- `"+0.5"` — 0.5s after previous ends
- `"-0.2"` — 0.2s before previous ends (overlap)
- `"<"` — same start as previous
- `1.5` — absolute time 1.5s from start

### BeatTimeline
```javascript
import { BeatTimeline, createFixedBeats, loadBeats } from "../scaffolding/js/beat-sync.js";

const beats = createFixedBeats({ bpm: 120, duration: 10 });
const timeline = new BeatTimeline(beats);

// Schedule by beat index (0-indexed: beat 0 = first beat)
timeline.at(0, () => { /* fires at first beat */ });
timeline.at(3, () => { /* fires at fourth beat */ });

// Schedule by absolute time in seconds
timeline.atTime(2.5, () => { /* fires at 2.5s */ });

// Schedule by downbeat index (0-indexed, every 4th beat)
timeline.atDownbeat(0, () => { /* first downbeat */ });

// Fire on every beat
timeline.onBeat((beatIndex, time) => { /* pulse effect, etc. */ });

// Control
timeline.play();
timeline.pause();
timeline.restart();
timeline.speed = 0.5; // half speed
```

> **Indexing**: All `at()`, `atDownbeat()`, and `onBeat()` indices are 0-based. The first beat is index 0, not 1.

---

## CSS Classes Reference

### Typography
`.display` `.heading-1` `.heading-2` `.heading-3` `.body-lg` `.body` `.caption` `.mono` `.mono-sm`

### Layout
`.scene` `.center` `.flex-col` `.flex-row` `.gap-{1,2,4,6,8}` `.text-center` `.absolute-fill` `.relative`

### Colors
`.text-muted` `.text-secondary` `.text-{blue,cyan,green,purple,orange,pink}`
`.text-gradient` `.text-gradient-warm` `.text-gradient-cool`

### Effects
`.glow-{blue,cyan,green,purple,orange,pink}` `.glow-{color}-strong`
`.box-glow-{blue,cyan,green,purple}`
`.neon` `.scanlines` `.grain` `.pulse`
`.glass` `.glass-strong`
`.terminal` `.terminal-header` `.terminal-body` `.terminal-prompt`
`.card` `.divider`
`.svg-glow` `.svg-glow-{blue,green,purple,orange}`

### Backgrounds
`.gradient-bg-midnight` `.gradient-bg-aurora` `.gradient-bg-ember` `.gradient-bg-ocean` `.gradient-bg-shift`

### Visibility
`.hidden` (opacity: 0) `.invisible` (visibility: hidden)

---

## File Paths

```
scaffolding/base.html          — Base template reference
scaffolding/styles/             — reset.css, core.css, effects.css
scaffolding/js/                 — beat-sync.js, scene-controller.js, hud.js
scaffolding/js/animations/      — text-scramble, typewriter, svg-tracer, ripple, fade-slide, counter
templates/scene-plans/          — Scene type templates
guides/                         — recording.md, assembly.md, music-selection.md
scripts/analyze-beats.py        — Beat detection script (run via uv)
output/                         — Generated scenes, beats.json, project-brief.md, scene-plan.md
audio/                          — User's music files
```
