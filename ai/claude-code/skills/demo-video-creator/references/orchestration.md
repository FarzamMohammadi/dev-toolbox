# Orchestration & the verification discipline

Purpose: how to actually *run* this build so the result is trustworthy — stage it to de-risk, delegate the heavy lifting, and verify every claim yourself. This is the meta-method; it is what makes "it's real" defensible.

Read this when: you're about to kick off the build, you're handing a slice to a subagent, something a subagent reports "done" feels too clean, or you're deciding what's safe to let the harness touch.

You are the single owner and the final quality gate. Subagents and scripts produce artifacts; *you* certify them. "Captured successfully," "tests green," "PR merged" are claims, not proof — treat them that way.

## Stage it to de-risk: prove the hardest integrations on one vertical slice first

Don't build the whole scenario and capture at the end. Build in stages, each independently runnable and independently verifiable, ordered so the riskiest unknowns die first:

1. **Spine slice — the first few beats, end to end on the real system.** Pick the segment that exercises the scariest integrations (real external pickup → the AI stub driving a real human-in-the-loop block → a real outbound message → a real resume). If that runs, the architecture is sound. In the source run this was "beats 1–5": custom-plugin registration into the real daemon path, real trigger pickup of a real issue, the scripted agent driving to a block, a *real* outbound message, a programmatic answer, and resume. Everything downstream is variations on the same mechanics.
2. **Full-scenario slice — the rest of the beats.** Extend the scripted brain to cover the remaining lifecycle (real artifact creation, re-entry on a real external comment, approval gate, auto-merge, cleanup). Same verification bar.
3. **Capture slice — real footage at true 8K.** Only once the scenario reliably produces the right *state* do you capture the surfaces. Lossless PNG at a high `deviceScaleFactor`, never `recordVideo`.
4. **Polish slice — Remotion overlays, iterated live with the owner.** Captions/callouts/transitions over the real footage, synced to the real trace timeline.

Why this order: capture and polish are expensive and assume a working scenario. If you capture before the scenario is solid, you re-capture. Each slice gets its own runnable driver script (e.g. `slice-a.mjs`, `slice-b.mjs`) so you can replay just that segment in isolation while iterating.

## Delegate-and-verify

Delegate the heavy, context-heavy builds (a whole slice, the capture rig, the Remotion composition) to subagents so the orchestrator stays at the meta level — owning sequencing, the spec, and the quality bar rather than drowning in implementation detail. But a subagent's self-report is the *start* of verification, never the end. For every delegated unit, do all of:

- **Re-run it yourself.** Execute the slice driver, the capture script, the render. Watch it actually happen.
- **Read the diff — especially any change to shared/core code.** A demo harness that edits the real engine is a red flag until proven benign. Read those hunks line by line. Distinguish a *legitimate bug fix the demo surfaced* (port it) from a *hack that bends the product to make the demo pass* (reject it).
- **Hand-check the real data.** Open the DB / event log and read the actual state transitions, the real PR/issue, the real messages, the real commits. Confirm the *system* did the thing — don't infer it from a script's stdout.
- **Literally view the captured frames.** Open the image. "Captured successfully" tells you a file exists, not that it shows the right surface at the right moment with the right content and the right resolution. Probe the real pixel dimensions (`ffprobe -show_entries stream=width,height`) and eyeball the hero frames for legibility. This is non-negotiable; it is the single easiest place to ship something wrong.

## Failure modes this approach hits (real incidents — each with its catch)

These all happened on the source run. They will tempt your build too.

- **Over-aggressive idempotent cleanup destroys real work.** A "start clean each take" reset closed prior items by a *shared marker* — and that marker also matched a genuine, unrelated issue, which it closed. **Catch:** scope every cleanup to *only what the harness itself created*. Track the ids/handles you create this run (or stamp a harness-run-unique id) and delete exactly those. Never sweep by a label/marker the real system also uses. (Concretely: a `closePriorDemoIssues()` that does `gh issue list --label engineer --state open` and closes all of them is the bug — `engineer` is the *real* trigger label.)
- **The harness leaks into the user's real home directory.** A workspace/data root that wasn't pinned to the isolated home caused a repo clone + task worktrees + copied files to land in the user's *real* `~/.engineer/`. **Catch:** pin every root (workspace, data, config) to the isolated demo home, e.g. `workspace_root: "${ENGINEER_HOME}/workspaces"`, and **verify isolation by inspecting the real home after a run** — it should be untouched. Clean up any leak with the owner's okay before moving on.
- **An agent toggled a private repo to public to capture it.** To screenshot the hosting pages, a subagent flipped repo visibility to public, captured, and flipped it back. That's a window where private code is exposed, and it relies on the restore succeeding. **Catch:** prefer an *authenticated capture session* (inject a logged-in cookie/session into the capture browser) so you never change visibility. If a toggle is ever unavoidable, **verify the repo is private again afterward**, explicitly.
- **The demo build surfaces genuine bugs in the real product.** Running the real engine end to end on a real scenario is an excellent stress test — the source run found two real Core defects (an approval path broken on repos with no CI; a transient-merge rejection that looped a clean change in rework forever). **Catch:** when this happens, *capture the find, flag it loudly, and decide with the owner whether to port the fix back to main* — and if you port, port **only** the real fix (src + test), never the demo-only scaffolding. Don't let a real fix die when the disposable branch is deleted.
- **An agent invents a "DEMO-only" fake label/marker.** Tempting, but it pollutes the "it's all real" story and creates surfaces a viewer might notice. **Catch:** keep it real. No fake markers, no demo-only labels, minimal deviation from the real/default config. Only stub what's *strictly* necessary (the AI brain) and the few isolation knobs (an isolated home; pacing that's invisible because final timing lives in the overlay layer). Every deviation is a debt you defend later.

## Collaboration checkpoints — lock the human calls FIRST

Some decisions are genuinely the owner's and must be settled *before* the build, not discovered mid-stream. Present each as a recommendation with reasoning, not a neutral menu:

- **How-real:** which surfaces are real-captured vs rendered, and how much gets faked. The default is "fake exactly the AI brain, keep everything else real" — confirm the owner agrees and that no surface is being recreated.
- **The scenario / beats:** the exact lifecycle the video tells, modeled on a real task. This is the narrative spine; lock it before scripting the brain.
- **The look (taste) — above all.** Never decide aesthetics alone. Iterate the palette, type, motion, and hero treatment **live against real viewable renders, section by section.** The owner owns the look; you own making options viewable fast.

Note which things genuinely block on the owner and can't be automated (e.g. a one-time QR/auth login of the capture browser for a personal-account surface). Stub a clean placeholder so the rest of the pipeline renders today, and document the exact manual step for when they're at the machine — don't let one human-only capture hold the whole build hostage.

## Real side effects are expected — isolate them and watch the user's back

This approach *will* produce real side effects on the disposable target: real external items created, real outbound messages sent, real repo writes, real merges. That's the point — it's what makes the footage real. The discipline is:

- **Isolate everything** to the disposable target and the isolated home. The real account/home is off-limits.
- **Clean up after**, scoped to only what this run created (see the cleanup failure mode).
- **Watch the user's back** on anything that touches their real accounts: their real home, their real (possibly private) repos, real messages to real people. When in doubt, surface it and let the owner call it.

The throughline: determinism comes from stubbing the one non-deterministic thing (the AI), **not** from faking the integrations. Faking integrations is what *loses* you the realness; keeping them real on an isolated, cleaned-up, owner-aware target is what makes the demo both controllable and genuinely true. You are the one who guarantees that — by verifying, not trusting.
