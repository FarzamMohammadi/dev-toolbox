# The harness: fake exactly the LLM, keep everything else real

The core architectural move of a demo video that is both deterministic AND honest: stub the one thing that
is non-deterministic (the AI brain), and let the entire real system run around it.

Read this when you are deciding *what* to fake and *what* to keep real — before you write any capture or
Remotion code. Get the seam wrong and you either record a flaky live system (un-reshootable) or a fake
recreation (dishonest, and it looks fake). Get it right and every surface in the video is the genuine product.

---

## The one rule

**Fake exactly one thing: the LLM. Keep everything else real.**

A modern software system that uses AI has exactly one large source of non-determinism — the model's
words and decisions. Everything else (the engine, the pipeline, the database, the UI, the integrations
with GitHub / Slack / a chat app / an issue tracker) is deterministic given its inputs. So:

- Stub *only* the AI, with a double that returns scripted-but-real-looking outputs.
- Run *everything else* unchanged, driven to a known state by deterministic scripted inputs.

The payoff is a take you can re-run to a byte-identical lifecycle while still being able to say, truthfully,
"this is the real system; only the AI's lines were pre-recorded for a clean shot." Determinism comes from
**stubbing the non-deterministic AI, not from faking the integrations.** Faking the integrations is what
would make it both dishonest and fragile-looking. Keeping them real is what makes it both controllable and
genuine.

---

## 1. Find the seam

Before faking anything, map the system's **real integration boundaries** — the points where it talks to
something it doesn't fully control. In a well-built system these are explicit: an adapter / plugin / driver
layer, or named external-service clients. Each boundary is a candidate seam.

Now classify each boundary by determinism:

- **The AI/LLM boundary** — almost always the single biggest source of non-determinism. Same prompt, different
  words; sometimes a different *decision* (route, verdict, tool call). This is the seam you cut.
- **Every other boundary** (git host, chat, issue tracker, the UI, the datastore) — deterministic given its
  inputs. Keep these real; control them by controlling their inputs, not by replacing them.

In the source run the system had a clean adapter layer with four types (LLM, trigger, communication, git
hosting). Only the LLM adapter was stubbed. The trigger polled a real issue, the comm plugin sent real chat
messages, the hosting plugin opened a real pull request — all unchanged.

If the system has *no* clean seam at the AI boundary, that is the first thing to build: a single interface the
real code already calls for "ask the model," so you have one place to swap. Don't fake at a deeper or shallower
layer than the model call — you'll either drag real logic into the stub or leave non-determinism in.

---

## 2. Stub the AI with a real-contract double

The stub is a plugin/double that **implements the exact same interface as the real AI adapter** and registers
through the real plugin path — so the real engine loads it and drives it identically, never knowing it's
scripted. It differs only in the body: instead of calling a model, it returns deterministic outputs keyed by
*which step is running*.

This is what makes every decision genuinely exercised. The real pipeline still routes on the stub's output, so
an auto-skip really skips, a "needs human" really blocks, a "ship" verdict really ships. You are not bypassing
the engine — you are feeding it controlled answers and watching it react for real.

Key design points, drawn from the source `demo-agent` plugin:

- **Key behavior off the live step, not a call counter.** The source infers the current sub-phase from a path
  the engine names in every prompt (the `…/<phase>/session-result.json` it expects the agent to write), then
  `switch`es on the phase name. Robust to retries and re-entry; a bare "Nth call returns X" counter is not.
- **Report your outcome through the real channel.** A real agent reports by writing its result file; the stub
  writes the same file the same way. The engine routes on the file's contents (e.g. `status: needs_human`,
  `complexity: trivial`, `verdict: ship`), not on any cosmetic return string. Match the real contract exactly.
- **Produce real side effects.** When the real agent would change code, the stub writes a **real diff** to the
  worktree and commits it — so the downstream verify gate, PR open, and merge all operate on genuine content.
- **Drive the interesting routes.** Script per-step outputs so the run exercises the features you want to show:
  a block-and-reach-out, an auto-skip of phases that don't apply, a rework re-entry, an approval gate. Each is
  a real engine behavior triggered by a scripted-but-real-looking answer.
- **Carry realistic telemetry.** Return non-zero cost/tokens/duration so the dashboard's cost and usage widgets
  show believable numbers, not zeros that scream "stub."

---

## 3. Keep real: engine, integrations, UI, artifacts

Everything except the model call runs unmodified:

- **The core engine / pipeline** — the real orchestrator, scheduler, event bus, state machine. The whole point
  is to show *this* working.
- **The real external integrations**, driven by **deterministic scripted inputs.** The git-hosting plugin opens
  a real PR; you drive it by scripting the real `gh issue create` / `gh pr comment` / dashboard API calls that a
  human would make. The chat plugin sends real messages. The trigger polls a real (disposable) repo. You are
  not faking these — you are scripting the *human/external side* so they reach a known state on cue.
- **The real UI / dashboard** — render the actual app reading the actual database over its real API/SSE. Never
  recreate a surface; you'll capture the genuine one (see the capture reference).
- **The real persisted data and artifacts** — a file-backed database (so the UI can read it), real commits, a
  real PR, real messages. These are what you film.

Speed-only tuning of real config (short poll intervals so the recording isn't slow) is fine — the viewer never
sees it, because final pacing lives in the polish layer. **Add no demo-only markers, fake labels, or gratuitous
config deviations.** The fewer the deviations from production, the stronger the "it's real" story. Deviate only
where strictly necessary: the AI stub, the isolated home, an opt-in feature toggle you want to showcase, and
recording-speed intervals.

---

## 4. Isolation: a dedicated, disposable environment

Run the entire demo against a **dedicated, disposable environment** so the user's real setup is never touched
and every run is a clean wipe-and-replay:

- **Separate config/home directory via an env var.** The source points `ENGINEER_HOME` at an in-repo
  `demo-harness/.engineer-home/` holding its own config, plugins, and database. The driver spawns the app with
  `env: { ...process.env, ENGINEER_HOME }`. Nothing reads or writes the real home.
- **A throwaway branch** for any demo-only code (the stub, the config), so it never pollutes mainline.
- **A disposable test repo** as the integration target — create and destroy issues/PRs freely; don't be precious.
- **Wipe-and-replay each run.** The driver deletes the demo database and resets external state (close prior
  issues, reset branches) at the start of every take, so each run is clean and idempotent.

**Set the workspace/data ROOTS to the isolated home — all of them.** This is the one isolation bug that bites
hardest. In the source run, an early take leaked a repo clone and task branches into the user's *real* home
because only the config home was redirected, not the **workspace root** where the engine clones and creates
worktrees. The fix was an explicit `workspace_root: "${ENGINEER_HOME}/workspaces"` in the demo config. Audit
*every* root the system writes to — config, data/DB, workspaces, logs, caches — and point all of them inside
the isolated home. Then verify with a clean home: run once, then check that nothing appeared outside it.

---

## 5. Real-content seeding: harvest once, replay deterministically

A stub that *invents* the AI's words reads as invented. Instead, **harvest a real AI run's output exactly once**
and bake it into the stub, so the replayed content is genuinely real — just pre-recorded.

What to harvest, from the source:

- **The reasoning/activity stream** — the model's thinking and tool calls (Read / Edit / Bash) as a live tail.
- **The real diffs** the run produced.
- **The real messages** it wrote (clarifications, PR narrative).

How the source did it (`harvest-activity.ts` + `activity-seed.json` + a `PROVENANCE.md`):

1. Cut a throwaway worktree at the same commit the demo runs against.
2. Run the **real** AI CLI on it with the **exact** flags the production adapter uses, capturing its raw output
   stream. (No push, no real PR — a local harvest only.)
3. Map that raw stream through the **same parser the real adapter uses**, so the baked events are byte-for-byte
   what the real agent would have emitted — not a hand-authored approximation.
4. Keep the raw transcript verbatim as the blob the UI displays.
5. **Normalize absolute paths to a token** (the source used `__WORKTREE__`) and rewrite it to the *current*
   run's real path at replay, so the tail reads with the demo's real paths every time.

Then **replay it deterministically with realistic pacing.** Stream the harvested events back through the same
`on_activity`/trace hooks the real adapter uses, with a deliberate inter-event delay (the source used ~700ms)
so the live tail is watchable on camera. The streaming is observation-only — it must never affect the scripted
outcome, so a hiccup in the tail can't break the take. Crucially, the stub must **report the same streaming
capability the real adapter does** (e.g. `supports_activity_streaming: true`), or the engine won't wire up the
live feed at all and the tail will be empty.

Write a `PROVENANCE.md` next to the seed recording exactly how it was harvested and how to re-harvest, so the
seed is auditable and regenerable — never hand-edited.

---

## 6. The honesty framing

State it plainly, in the video and anywhere you describe how it was made:

> This is the real system running. The real pipeline, the real integrations, the real UI, the real PR and
> messages — all genuine. The only thing pre-recorded is the AI's words and decisions, captured from an actual
> run and replayed deterministically so the take is clean and repeatable.

That sentence is true because of the architecture above: you faked exactly one thing, and you faked it with
real harvested content. Everything a viewer sees on screen — every surface, every artifact, every state
transition — is the genuine product doing the genuine work. The determinism that makes it a clean shoot comes
entirely from stubbing the non-deterministic AI, never from faking the things that make it real.
