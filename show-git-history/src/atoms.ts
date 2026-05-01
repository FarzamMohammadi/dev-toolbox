import { Layer } from "effect"
import * as Atom from "effect/unstable/reactivity/Atom"
import type { DiffMode } from "./domain.js"
import { Observability } from "./observability.js"
import { GitService } from "./services/GitService.js"

export const gitRuntime = Atom.runtime(GitService.layer.pipe(Layer.provideMerge(Observability.layer)))

export const branchesAtom = gitRuntime.atom(
	GitService.use((git) => git.listBranches()),
).pipe(Atom.keepAlive)

export const filesAtom = gitRuntime.atom(
	GitService.use((git) => git.listFiles()),
).pipe(Atom.keepAlive)

export const loadCommitsAtom = gitRuntime.fn<string>()(
	(branch) => GitService.use((git) => git.listCommits(branch)),
).pipe(Atom.keepAlive)

export const loadFileHistoryAtom = gitRuntime.fn<string>()(
	(filepath) => GitService.use((git) => git.listFileHistory(filepath)),
).pipe(Atom.keepAlive)

export const loadCommitDiffAtom = gitRuntime.fn<{ hash: string; filepath?: string }>()(
	(input) => GitService.use((git) =>
		input.filepath
			? git.getCommitFileDiff(input.hash, input.filepath)
			: git.getCommitDiff(input.hash),
	),
).pipe(Atom.keepAlive)

export const loadFileHistoryDiffAtom = gitRuntime.fn<{ hash: string; filepath: string; mode: DiffMode }>()(
	(input) => GitService.use((git) =>
		input.mode === "file-scoped"
			? git.getCommitFileDiff(input.hash, input.filepath)
			: git.getCommitDiff(input.hash),
	),
).pipe(Atom.keepAlive)

export const branchSelectedIndexAtom = Atom.make(0).pipe(Atom.keepAlive)
export const commitSelectedIndexAtom = Atom.make(0).pipe(Atom.keepAlive)
export const fileSelectedIndexAtom = Atom.make(0).pipe(Atom.keepAlive)
export const fileHistorySelectedIndexAtom = Atom.make(0).pipe(Atom.keepAlive)

export const currentBranchAtom = gitRuntime.atom(
	GitService.use((git) => git.getCurrentBranch()),
).pipe(Atom.keepAlive)

export const defaultBranchAtom = gitRuntime.atom(
	GitService.use((git) => git.getDefaultBranch()),
).pipe(Atom.keepAlive)

export const loadBranchReviewDiffAtom = gitRuntime.fn<{ targetBranch?: string }>()(
	(input) => GitService.use((git) => git.getBranchReviewDiff(input.targetBranch)),
).pipe(Atom.keepAlive)

export const loadCommitsAheadAtom = gitRuntime.fn<{ targetBranch?: string }>()(
	(input) => GitService.use((git) => git.getCommitsAhead(input.targetBranch)),
).pipe(Atom.keepAlive)

export const branchReviewCommitIndexAtom = Atom.make(0).pipe(Atom.keepAlive)
