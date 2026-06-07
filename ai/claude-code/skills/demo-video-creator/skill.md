---
name: demo-video-creator
description: >-
  Produce a dope, almost-professional, deterministic-yet-REAL automated product-demo video of a
  software system — real surfaces, real footage at true 4K/8K, the AI/LLM as the only stubbed piece,
  polished in Remotion. Use this whenever the goal is a marketing/launch/portfolio demo film of a
  running product (a CLI, agent, web app, pipeline) that must SHOW the real system working end-to-end,
  reproducibly, at the highest quality — not a slide deck, not a screen-recording, not a mockup. Covers
  the full pipeline: harness architecture, 8K browser capture (never recordVideo), Remotion polish,
  and the orchestrate-and-verify discipline. Heavy and side-effecting — invoke it deliberately.
disable-model-invocation: true
---

# Demo Video

A playbook for producing a **deterministic-yet-real** product-demo video: the real system runs end to
end, every showcased feature genuinely fires, real artifacts are produced — and yet the whole thing is
scripted, repeatable, and renders at true 4K/8K. You direct; this drives.

**What you'll ship:** a ~2–3 min 4K (8K-mastered) film of the product running a real scenario, plus a
GIF/webm for README/docs embedding, produced by a **re-runnable pipeline** you can fire again forever.

---

## The core idea — fake exactly ONE thing

The instinct is a false binary: "real (live, fragile, non-deterministic)" vs "fake (controllable, but
looks staged)." Reject it. The move that dissolves it:

> **Stub the AI/LLM brain. Keep absolutely everything else real.**

The LLM is the one big source of non-determinism (timing, content, whether it even hits your beats). So
replace *only* the LLM with a real-contract double that replays **scripted + real-harvested** output.
Everything else — the real engine/pipeline, the real external integrations (git hosting, chat, trackers)
driven by deterministic inputs, the real UI, the real persisted artifacts (PRs, messages, commits) —
**runs for real.** The result genuinely *is* the system working; only the AI's words were pre-recorded
from a real run for a clean take. That's an honest, defensible story *and* total control. (See
`references/architecture.md`.)

Two corollaries that flow from this and matter just as much:

- **Real footage, never recreation.** Capture the *real* surfaces at 8K. Remotion is *polish* —
  captions, callouts, transitions over real footage — it never rebuilds a UI as React. The moment you
  recreate a surface, you're back to "looks fake."
- **Keep it real everywhere.** No demo-only labels, no fake markers, minimal deviation from the
  real/default config. Every gratuitous "demo-ism" is a tell. Deviate *only* where strictly necessary
  (the LLM stub; pointing the system at a disposable target; one flag needed to showcase a real feature).

---

## Five principles (thread these through every phase)

1. **Real workflow > live services.** "Real" means the real *workflow and features* firing, rendered
   identical to life — not that external calls must be live. Deterministic and real are not enemies.
2. **Isolate ruthlessly.** Dedicated config/home dir, throwaway branch, disposable test repo. The user's
   real environment is never touched; every run is a clean wipe-and-replay.
3. **Master at 8K, deliver at 4K.** Capture lossless, render at 8K, downsample to 4K — supersampled,
   razor-sharp. **Never** Playwright `recordVideo` (hardcoded ~1 Mbit/s — the quality trap).
4. **Delegate the build, verify everything yourself.** Subagents do the heavy lifting; you re-run, read
   diffs, hand-check data, and *look at the actual frames*. Never trust a self-report.
5. **The human owns taste.** How-real, the scenario, and above all *the look* are the human's calls.
   Present recommendations; iterate the aesthetic live against real renders. Never decide taste alone.

---

## Prerequisites

- The product runs locally and has an interface worth filming (a dashboard/UI, a CLI, real integrations).
- You can reach the real integrations on a **disposable** target (a throwaway repo, a test chat/bot).
- Tooling: Playwright (+ chromium), ffmpeg, Node, and Remotion (installed per-project on a throwaway
  branch is fine). Confirm these before promising anything.

---

## The workflow

Run these in order. Each phase is independently runnable and verifiable. Stage the work so the *hardest*
risks are proven *first* (Phase 2), not discovered after you've built everything.

### Phase 0 — Lock the human decisions (do NOT skip)
Before any code, lock the calls that are genuinely the human's, leading with your recommendation:
- **How real, per surface** — which surfaces are real-captured vs (rarely) rendered. Default: all real.
- **The scenario / beats** — the exact end-to-end story the product will perform. Write it out as an
  ordered beat list; the ambiguity/edge moments are the point (they show the product's intelligence).
- **The look** — flag now that you'll iterate it live in Phase 5; don't try to settle taste up front.

Reconcile these into a single source-of-truth spec you and every subagent work from. When a decision
shifts mid-build, update the spec *first* so nothing drifts.

### Phase 1 — Build the harness (fake only the LLM)
Stand up the real system in an **isolated** environment with the AI swapped for a scripted+seeded
double. Prefer the *real production entry path* (the real daemon/server + real DB), changing only the
AI plugin — so the only deviation from production is the one thing you must control. Drive the scenario's
human/external inputs programmatically (real CLI calls, real API posts). → `references/architecture.md`.

### Phase 2 — De-risk on a vertical slice
Build and prove the **first few beats end-to-end** before anything else: the riskiest integrations
(plugin registration, real external calls, the stub driving the real pipeline) on the smallest coherent
slice. Run it; verify the real artifacts appear (the real message sends, the task blocks/resumes). Only
then expand. This is where most surprises live — surface them cheap. → `references/orchestration.md`.

### Phase 3 — The full scenario
Extend the stub + driver through every beat to a clean, **re-runnable** full take that produces the real
artifacts (open→merge a real PR, send real messages, etc.). Make it idempotent (wipe state, reset the
target, fresh run each time). Verify the whole lifecycle in the data and on the real services yourself.

**Real-content seeding (the live-AI look):** harvest a real AI run *once* (its reasoning/activity stream,
real diffs) and replay it through the stub with realistic pacing — so any "live AI output" surface reads
genuinely real, not invented. → `references/architecture.md`.

### Phase 4 — Capture at 8K
Capture the real surfaces as lossless 8K stills/sequences. **Never `recordVideo`.** Lossless
`page.screenshot()` at `deviceScaleFactor` 2–4 → 7680×4320. Prefer capturing *persistent/historical*
state post-run (deterministic) over fragile live-sync. Organize footage into the Remotion slots and
export the run's **real trace timings** so overlays sync to real moments. → `references/capture.md` +
`scripts/capture-8k.mjs`, `scripts/encode-and-downsample.sh`. **View the frames you capture** — confirm
each shows the right thing; "captured successfully" is not proof.

### Phase 5 — Polish in Remotion (iterate the look WITH the human)
Compose the real footage with captions/callouts/transitions/intro-outro, synced to the real timings.
Keep all aesthetics in one tokens file; render a fast draft, then **iterate the look live with the
human** against real renders, section by section. → `references/remotion-polish.md`.

### Phase 6 — Master, embed, ship
Render the 8K master → downsample to 4K → derive a GIF/webm. Embed in the README/docs hero. Hand the
human the deliverables. The pipeline is reusable — re-run it any time the product changes.

---

## Orchestration & verification (the discipline that makes it trustworthy)

This pipeline spans many subagents and touches real services — quality comes from *how* you run it:

- **Delegate to stay at the meta level**, but you are the single owner + final quality gate. After every
  delegated step: re-run it, read the diff (especially any change to shared/core code), hand-check the
  real data and artifacts, and **open the captured images**.
- **Watch the user's back.** Real side effects are expected on the disposable target — but isolate them,
  clean up after, and surface anything that touched the real environment. Known failure modes to guard
  against (each bit someone during the source run): over-aggressive cleanups closing *real* issues;
  clones leaking into the user's *real* home; an agent flipping a private repo public; fake "demo" labels
  creeping in; and — a feature, not a bug — the build **surfacing genuine product bugs** worth porting
  back. Catches and fixes for each are in `references/orchestration.md`. **Read it before delegating.**

---

## Reference & script map

| File | Read it when |
|------|--------------|
| `references/architecture.md` | Designing the harness — what to stub, isolation, real-content seeding |
| `references/capture.md` | Capturing surfaces at 8K — the recordVideo trap, Playwright/ffmpeg, surface-by-surface |
| `references/remotion-polish.md` | Building the polish layer — tokens, timeline sync, 8K→4K→GIF |
| `references/orchestration.md` | Before delegating — the staging, the verify discipline, the failure modes |
| `references/worked-example.md` | Want a concrete end-to-end example (demoing an autonomous coding agent) |
| `scripts/capture-8k.mjs` | A reusable lossless 8K Playwright capture |
| `scripts/encode-and-downsample.sh` | ffmpeg: 8K master → razor-sharp 4K → GIF |

---

Take your time on Phase 0 and Phase 5 (the human's domain) and on verification (yours). The rest is
mechanical once the architecture is right. Make it incredible.
