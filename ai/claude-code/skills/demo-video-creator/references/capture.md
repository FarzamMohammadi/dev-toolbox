# Capturing real surfaces at true 4K/8K

Capture pristine, lossless footage of REAL surfaces — no recreation, no quality ceiling.

Read this when: you are about to record any surface (your UI, a third-party web page, a chat app, a
terminal) and want delivery-grade 4K/8K, or you hit mushy/soft video and don't know why.

## The key insight: never use Playwright `recordVideo`

`recordVideo` is the trap everyone hits. Its quality is **not configurable** — for Chromium the bitrate is
**hardcoded at ~1 Mbit/s VP8** (microsoft/playwright#10855). At any resolution it looks mushy: a 4K
`recordVideo` is a soft 4K, not a sharp one. You cannot fix it with flags because there are none. If your
footage "feels 1080p" no matter what you set, this is why.

Capture **lossless PNG stills** instead. Take `page.screenshot()` on a normal-sized CSS viewport but at a
high `deviceScaleFactor`, so the pixel output is 4K/8K while the *layout* stays readable. Then encode the PNG
sequence with ffmpeg at **any** bitrate you want. PNG is lossless, so the encoder is the only quality knob and
you own it completely. This is the whole game: decouple capture (lossless) from encode (your call).

## The proven recipe (real numbers)

Pick a viewport × deviceScaleFactor whose product is your target resolution:

| CSS viewport | deviceScaleFactor | PNG output | Notes |
|---|---|---|---|
| 3840×2160 | 2 | 7680×4320 (8K UHD) | matches the POC; pixel-exact |
| **1920×1080** | **4** | **7680×4320 (8K UHD)** | desktop-natural width → content-dense UI (dashboards, GitHub) reads better at video scale |
| 1920×1080 | 2 | 3840×2160 (4K) | when 8K is overkill |

The DSF-4-on-1920 row is the workhorse for UI: a 1920 CSS width is what a real desktop renders, so the
dashboard and GitHub lay out naturally, and DSF 4 supersamples the result to true 8K. Both 8K rows are valid;
choose by whether layout-naturalness (1920@4) or pixel-exactness (3840@2) matters more for that surface.

**Master at 8K, deliver at 4K.** Render/capture everything at 8K, then *downsample* to 4K for delivery.
Downsampling averages 4 source pixels into 1 (supersampling), giving a razor-sharp 4K that beats a
native-4K capture. True 8K files are enormous and almost nobody plays them back; 4K is the real target.

### Playwright capture (the exact config)

```js
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 4,                 // 1920×4 = 7680 → 8K UHD PNG
});
const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle' });  // see waits caveat below
await page.screenshot({ path: 'frame-0001.png' });   // lossless PNG, NOT recordVideo
await browser.close();
```

The runnable, hardened version is `scripts/capture-8k.mjs` — it adds per-surface readiness waits, row/tab
interactions, and an ffprobe dimension check on every PNG (the 8K verification gate: assert each frame is
exactly `7680×4320` before trusting it).

**Waits matter more than the screenshot.** A clean still depends entirely on the page being *settled*:
- For your own SPA, `networkidle` often **never fires** if it holds a long-lived connection open (SSE/
  websocket for live updates). Use `domcontentloaded`, then wait on an explicit content signal — a nav
  element, a table row, a specific selector — and a short fixed settle (`~1.2s`) for client-side data fetches.
- For third-party pages (GitHub etc.), `networkidle` works but content lazy-loads; wait for a content anchor
  (a header/title) and, if you need something far down, step-scroll the full height to force lazy items to
  render, then scroll back and center your target element before the shot.

### ffmpeg encode (the exact command)

```bash
ffmpeg -framerate 30 -i frame-%04d.png \
  -c:v libx265 -crf 14 -pix_fmt yuv420p out.mp4
```

`-crf 14` is visually lossless; the resulting bitrate lands around ~140 Mbit/s at 8K — roughly **140× the
quality of `recordVideo`** at 4× the resolution. Downsample the 8K master to a sharp 4K delivery with a
Lanczos rescale:

```bash
ffmpeg -i out/master-8k.mov -vf scale=3840:2160:flags=lanczos \
  -c:v libx265 -crf 16 -pix_fmt yuv420p out/delivery-4k.mp4
```

`scripts/encode-and-downsample.sh` is the runnable version (master encode → 4K downsample → optional GIF
derive). If your motion polish lives in Remotion, render its master at 8K (ProRes 4444) and downsample the
same way — same Lanczos step, same delivery target.

## Capture strategy: prefer persistent end-state over live-sync

Capturing live, while the run happens, is fragile — timing drifts, animations stutter, one bad take wastes
the whole run. Prefer capturing the **persistent / historical end-state after the run finishes**. A good
system stores everything it did (a database, an event log, history/timeline views), so post-run you can
navigate to any moment deterministically and re-shoot any frame as many times as you like. The footage is
identical every time, which is exactly what a re-runnable pipeline needs.

Concretely: run the scenario once to populate the data store, then point a read-only server at that store and
screenshot its views. In the worked example, `capture-dashboard.ts` boots the **real** dashboard server (the
same code path the product uses) read-only against the completed run's file-backed DB, so its overview / task
list / timeline / decision-trail / agent-activity views render the entire journey after the fact. Capture is
POST-run and re-runnable; nothing is faked, only replayed.

## Surface by surface

**(a) Your own web UI / dashboard.** Start the *real* server against the run's data store and navigate its
real routes. Don't rebuild surfaces — serve the genuine SPA (in the example, via a `dist/dashboard` symlink so
tsx serves the same built artifact production serves). Because it's DOM/SVG/canvas, DSF screenshots are
pixel-crisp at 8K. To frame a specific moment, drive the real UI deterministically: expand the row, switch to
the tab, scroll the element into center — then shoot.

**(b) Third-party web pages (e.g. GitHub).** Use an **authenticated browser session**, not visibility
toggles. A source run flipped a private repo public to capture it, then restored it — avoid that: it's risky
and only works for content you own. An *anonymous* capture also leaves "Sign up to join" banners and signed-out
chrome in the frame. Inject a logged-in session instead (persistent context, or attach to an authed browser),
and best-effort strip leftover banners (cookie consent, dismissible notices, the signup sticky bar) by
removing those DOM nodes before the screenshot so the footage is the clean page.

**(c) Chat apps (e.g. Telegram).** A fresh Playwright browser isn't logged in, and these apps gate on a
QR/device login a headless run can't perform. Three paths: **(1)** CDP-attach to a logged-in browser
(`chromium.connectOverCDP()` after starting it with `--remote-debugging-port`) and drive the real web client —
powerful but it controls the *real* browser and needs the debug-port launch, so it's fragile; **(2)** log a
dedicated capture browser in **once** via QR using a persistent context (`launchPersistentContext`) so
re-captures reuse the session — this is the cleanest one-time human step; **(3)** render the view from the real
message data in your motion layer, avoiding the browser entirely. The messages themselves stay 100% real and
fire every run; only the *view* capture is deferred to a one-time login. Use the same 8K rig
(1920@DSF4 → 7680×4320) so the frame matches the rest, and verify with ffprobe.

**(d) Terminal / CLI.** Capture the real streaming output. If the CLI's output also streams into your UI (an
activity/agent-calls view), capturing it there gives you a styled, in-product frame for free. Otherwise render
the genuine harvested output (resolved spinners, the real ready/URL lines, the real banners) in a neutral
terminal chrome — the *content* is the real CLI output; only the window frame is presentation, which is all a
terminal ever is.

## Where live motion belongs

A screenshot-per-frame loop can't hit 30–60 fps in real time, so don't try to capture smooth streaming text or
transitions live. Capture high-resolution **stills** of each key state, and ADD the motion (text streaming in,
crossfades, speed-ramps, callouts) as overlays in Remotion over those stills. You get perfectly smooth motion
at any frame rate with zero capture ceiling, and the underlying surfaces stay real. Capture reality; animate in
post.
