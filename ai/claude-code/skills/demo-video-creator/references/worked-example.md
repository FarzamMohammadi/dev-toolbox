# Worked example — demoing The Engineer (an autonomous coding agent)

This is the concrete grounding for the method. The other references state the pattern in the abstract; this one walks one real system end to end so you can see how each abstract move lands. Read it after `SKILL.md` and the method references, when you want a worked instance to copy the *shape* of — not the specifics.

The general references it points back to:
- `architecture.md` — the "fake exactly ONE thing" pattern, the adapter-stub mechanics, and (§5) real-content seeding: recording a real run and replaying it through the stub.
- `capture.md` — the lossless-PNG 8K path and the `recordVideo` trap.
- `remotion-polish.md` — polish-over-real-footage, never surface recreation.
- `orchestration.md` — staging to de-risk, the verify discipline, and the failure modes.

---

## 1. The system under demo

**The Engineer** is an autonomous software-engineering agent. A human files a GitHub issue; the agent picks it up, runs it through a pipeline, opens a real pull request, reworks it on feedback, and merges it — talking to the human over chat when it gets stuck. It has a **plugin architecture** with four adapter seams:

- **Trigger** — where work comes from (a GitHub issue poller).
- **LLM / agent** — the "brain" that reasons and edits code (normally the real `claude` CLI).
- **Communication** — how it reaches the human (Telegram).
- **Git hosting** — where PRs live (GitHub via Octokit).

The brain drives a five-stage **RRPIR pipeline** — Requirements → Research → Planning → Implementation → Review — plus delivery (open PR, await review, auto-merge). A **dashboard** renders the live run: task timeline, routing decisions, and an **Agent Calls** tab that streams the brain's thinking and tool calls.

This matters for the demo because *the feature set is the pipeline plus the four real integrations firing*. The demo has to show all of them genuinely working — so the one thing we're allowed to fake has to be small enough to keep everything else real.

## 2. The scenario — 12 beats

The human-chosen storyline. It's deliberately not a clean happy path; it shows the agent getting stuck, reaching out, and being corrected, because *that* is the product.

1. `engineer start` — the real daemon + real dashboard come up on `:3847`.
2. A **deliberately vague** issue is filed (`gh issue create`, title "Update scene 1", empty body). The ambiguity is the trigger for beat 4.
3. The real trigger polls, picks it up, creates a task, enters the pipeline.
4. **Requirements blocks (the headline human-in-the-loop):** the brain returns `needs_human` with a calm, specific clarifying question. Task → `blocked(need_more_info)`; the question is delivered over **real Telegram**.
5. The owner **answers in the dashboard** (`POST /api/messages/:taskId/respond`); the response-poller unblocks the task and re-dispatches, carrying the answer.
6. **Auto-skip:** the resumed requirements pass scopes the task `complexity:"trivial"`, so Research and Planning *skip* — the routing trail shows the skips.
7. **Implement → self-review:** the brain writes the real diff to the worktree and commits; the verify gate passes; review self-reviews and ships. The **live tail streams** to the Agent Calls tab.
8. **"PR ready"** Telegram milestone fires; the real PR opens on GitHub.
9. A **PR comment asks for more** (`gh pr comment` "also update scene 2…"); the real hosting plugin detects it and re-enters the pipeline.
10. **Rework** loops through fast; a second real diff is pushed; back to await-review.
11. **`/approve`** (`gh pr comment "/approve"` from the authorized owner) promotes the PR to ready-to-merge.
12. **Auto-merge → branch deleted → final main.** Real Octokit merge; the workspace reaper deletes the branch; task `completed`.

## 3. The plugin matrix — fake exactly one thing

This is the whole method in one table. Only the brain is stubbed; the three external integrations stay real, driven by deterministic scripted inputs.

| Adapter | Plugin | Real? | Why |
|---|---|---|---|
| LLM / agent | **`demo-agent`** (new, scripted + seeded) | **STUB** | The sole big non-determinism source. Returns scripted per-beat outcomes, writes the real diff, streams a seeded-but-real live tail. |
| Trigger | `github-trigger` | **REAL** | Really polls a real issue. |
| Communication | `telegram-comm` | **REAL** | Really sends the clarify + "PR ready" messages to the owner's phone. |
| Git hosting | `github-hosting` | **REAL** | Really opens / comments / merges a real PR via Octokit. |
| Human inputs | — | **REAL** | `gh issue create`, the dashboard answer POST, `gh pr comment` rework + `/approve` — actual events, not mocks. |

Determinism comes from stubbing the brain and controlling the repo state — **not** from faking the integrations. That's what keeps the take both controllable *and* genuinely real. The only deviations from a production install are: the stub agent; an **isolated demo `ENGINEER_HOME`** (its own config + DB, trigger pointed only at the disposable `learnaholic-demo` repo) so the owner's real `~/.engineer` is never touched; `enable_comment_approval: true` (to *showcase* the real `/approve` feature, default-off); and short poll intervals purely to speed recording (final pacing is set later in Remotion, so it's invisible). No demo-only labels, no fake markers — the real `engineer` label and default configs everywhere else.

**How the stub stays honest** (`src/plugins/agent/demo-agent/demo-agent.ts`): it implements the exact same `AgentAdapter` contract as the real agent, so the real production daemon loads and drives it through the real pipeline. The orchestrator always names an absolute `…/<phase>/session-result.json` path in the prompt and expects the agent to report its outcome by *writing that file* (a real CLI agent does the same). So the stub parses the path out of the prompt, infers the sub-phase from the directory name, and writes the scripted handoff. On the first requirements pass it writes `needs_human` + an outreach file; on the resume pass it writes `complexity:"trivial"`; on implement it writes a real diff and commits; on review it writes `verdict:"ship"`. The `content` it returns is cosmetic — the orchestrator routes only on what landed in `session-result.json`.

To make the real daemon load a non-production plugin, it's registered as a builtin on the disposable branch (one entry + a config yaml) — the smallest possible hook, not a parallel test harness. The rejected alternative was the project's in-memory integration-test context: it uses a fake clock and all-fakes and an in-memory DB the dashboard can't read — that's the *test* path, not real surfaces.

## 4. Driving it — the scenario-driver

The beats are driven by two plain Node scripts (`demo-harness/slice-a.mjs` for beats 1–5, `demo-harness/slice-b.mjs` for all 12), each a narrated, **idempotent** runner: wipe the demo DB, close any prior open demo issues/PRs, `engineer start`, then perform each human action for real and *poll the file-backed DB* to confirm the expected state before narrating the next step. The scenario constants live at the top — the issue title, the empty body, the owner's dashboard answer, the rework comment — so the storyline is one editable block. Building beats 1–5 first as a separate slice was the deliberate de-risk: it proves the hardest integrations (custom-plugin registration, real trigger pickup, real Telegram send, dashboard unblock-and-resume) on a small slice before extending to the PR half.

## 5. The live-tail harvest — a real tail through the stub

The Agent Calls tab is the most visually load-bearing surface and the trap most likely to look fake. The stub can't *think*, so where does an authentic-looking stream come from?

Answer: **harvest it from one real run.** The real agent streams `AgentActivityEvent`s only when its capabilities report `supports_activity_streaming: true`; the stock test-fake reports `false` and streams nothing. So the demo-agent (a) reports `true`, (b) replays a seeded event list back through `request.on_activity` with realistic pacing (~700ms between events, slow enough to be watchable), and (c) writes the run's raw transcript to `trace_output_path` — exactly the three things the real agent does.

The seed is *not invented*. `demo-harness/harvest-activity.ts` takes the NDJSON of an actual `claude` run on this exact task (captured with the same flags the real agent uses) and runs each line through **Core's own `activityEventsFromLine` mapper** — the same function the real agent calls — so the baked `AgentActivityEvent[]` is byte-for-byte what the real agent would have emitted. Worktree-specific absolute paths are normalized to a `__WORKTREE__` token and rewritten to the real demo `cwd` at replay. The result (`src/plugins/agent/demo-agent/activity-seed.json`, ~36 events of thinking + Read/Edit/Bash + the real diff) streams as a genuine tail, not an empty stub. Provenance is recorded alongside it.

## 6. Capture + polish

**8K capture** (`demo-harness/capture/capture-8k.mjs`): lossless `page.screenshot()` PNGs of every real surface — **never** Playwright `recordVideo`, whose hardcoded ~1 Mbit/s VP8 is the quality trap. A 1920×1080 CSS viewport at `deviceScaleFactor: 4` supersamples to a true 7680×4320 PNG (1920@DSF4 reads better for content-dense UI than the POC's 3840@DSF2). The surfaces are all real: the dashboard SPA served read-only against the *completed run's* file-backed DB (stateful, so its overview/timeline/decisions/Agent-Calls views show the whole journey post-run, deterministically), the real github.com issue/PR/main pages, the real `engineer start` terminal output, and the CLI tail captured *from* the dashboard's Agent Calls tab where the harvested stream lives. The capture also exports the run's **real trace timings** to `remotion/data/timeline.timings.json` so each beat's start and duration reflect the actual moments.

**Remotion polish** (`demo-harness/remotion/`): overlays *over* the real footage — captions, callouts, transitions, speed-ramps, intro/outro — synced to that real timeline. It never recreates a surface. The look (palette, type, motion, hero) lives in swappable neutral theme tokens (`src/theme/tokens.ts`) so taste is tuned with the human, section by section, without touching the composition.

## 7. What it produced and what was learned

It produced a first-draft cut (`demo-harness/remotion/out/demo-draft.mp4`) of all 12 beats over real 8K footage with real trace timings; the hero (implement) and approve frames eyeballed as real and legible.

Lessons worth carrying to the next system:

- **The stub surfaces real bugs.** Driving the *real* pipeline (not a mock) flushed out two genuine Core defects — `/approve` was permanently broken on any repo with no CI, and a transient "head out of date" merge rejection looped clean PRs in rework forever. A faked pipeline would have hidden both. These were unit-tested and earmarked to port back to the product before release; **don't let real fixes die with the disposable branch.**
- **Isolation is load-bearing and easy to get wrong.** An early slice leaked a repo clone and task branches into the owner's real home; the fix was an explicit `workspace_root` under the demo `ENGINEER_HOME`. Verify isolation, don't assume it.
- **Authenticity gaps are the polish backlog.** The dashboard showed the stub's model id (`demo-agent-scripted-v1`) instead of the real model the tail came from; a header read "Daemon stopped" because capture happened post-run; GitHub pages were the anonymous (signed-out) view with a signup banner. None break the take, all are "looks-identical-bar" calls left for the human — capture with an authenticated session and a live daemon next time.
- **One surface stayed parked for the human:** Telegram view-capture needs a one-time QR login of the capture browser. The messages *fire for real every run*; only the screenshot of them was deferred. Know which deferrals are cosmetic (the view) versus real (the send) and say so.
