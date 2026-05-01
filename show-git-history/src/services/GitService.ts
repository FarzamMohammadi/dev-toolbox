import { Context, Effect, Layer } from "effect"
import { config } from "../config.js"
import type { BranchItem, CommitItem, FileEntry } from "../domain.js"
import { CommandRunner, type CommandError } from "./CommandRunner.js"

const parseBranches = (stdout: string, currentBranch: string): BranchItem[] => {
	const branches: BranchItem[] = []
	for (const line of stdout.trim().split("\n")) {
		if (line.length === 0) continue
		const parts = line.split("\t")
		if (parts.length < 3) continue
		const rawName = parts[0]!.trim()
		if (rawName === "" || rawName.includes("HEAD")) continue
		const name = rawName.replace(/^origin\//, "")
		const isRemote = rawName.startsWith("origin/")
		if (isRemote && branches.some((b) => !b.isRemote && b.name === name)) continue
		const hash = parts[1]!
		const dateStr = parts[2]!
		const tracking = parts[3]?.trim() || null
		branches.push({
			name,
			isRemote,
			isCurrent: name === currentBranch,
			lastCommitHash: hash,
			lastCommitDate: new Date(dateStr),
			trackingBranch: tracking,
		})
	}
	return branches.sort((a, b) => {
		if (a.isCurrent) return -1
		if (b.isCurrent) return 1
		if (a.isRemote !== b.isRemote) return a.isRemote ? 1 : -1
		return a.name.localeCompare(b.name)
	})
}

const parseCommits = (stdout: string): CommitItem[] => {
	const commits: CommitItem[] = []
	for (const line of stdout.trim().split("\n")) {
		if (line.length === 0) continue
		const parts = line.split("\t")
		if (parts.length < 5) continue
		commits.push({
			hash: parts[0]!,
			shortHash: parts[1]!,
			subject: parts[2]!,
			author: parts[3]!,
			date: new Date(parts[4]!),
			refs: parts[5] ?? "",
		})
	}
	return commits
}

const parseFiles = (stdout: string): FileEntry[] =>
	stdout.trim().split("\n").filter((line) => line.length > 0).map((path) => ({ path })).sort((a, b) => a.path.localeCompare(b.path))

export class GitService extends Context.Service<GitService, {
	readonly getCurrentBranch: () => Effect.Effect<string, CommandError>
	readonly listBranches: () => Effect.Effect<readonly BranchItem[], CommandError>
	readonly listCommits: (branch: string, limit?: number) => Effect.Effect<readonly CommitItem[], CommandError>
	readonly getCommitDiff: (hash: string) => Effect.Effect<string, CommandError>
	readonly getCommitFileDiff: (hash: string, filepath: string) => Effect.Effect<string, CommandError>
	readonly listFiles: () => Effect.Effect<readonly FileEntry[], CommandError>
	readonly listFileHistory: (filepath: string, limit?: number) => Effect.Effect<readonly CommitItem[], CommandError>
	readonly getDefaultBranch: () => Effect.Effect<string, CommandError>
	readonly getBranchReviewDiff: (targetBranch?: string) => Effect.Effect<string, CommandError>
	readonly getCommitsAhead: (targetBranch?: string) => Effect.Effect<readonly CommitItem[], CommandError>
}>()("git-history/GitService") {
	static readonly layerNoDeps = Layer.effect(
		GitService,
		Effect.gen(function*() {
			const command = yield* CommandRunner

			const getCurrentBranch = Effect.fn("GitService.getCurrentBranch")(function*() {
				const result = yield* command.run("git", ["branch", "--show-current"])
				return result.stdout.trim()
			})

			const listBranches = Effect.fn("GitService.listBranches")(function*() {
				const current = yield* getCurrentBranch()
				const result = yield* command.run("git", [
					"branch", "-a",
					"--format=%(refname:short)\t%(objectname:short)\t%(committerdate:iso-strict)\t%(upstream:short)",
				])
				return parseBranches(result.stdout, current)
			})

			const listCommits = Effect.fn("GitService.listCommits")(function*(branch: string, limit?: number) {
				const result = yield* command.run("git", [
					"log",
					"--format=%H\t%h\t%s\t%an\t%aI\t%D",
					`-n`, String(limit ?? config.commitLimit),
					branch,
				])
				return parseCommits(result.stdout)
			})

			const isRootCommit = Effect.fn("GitService.isRootCommit")(function*(hash: string) {
				const result = yield* command.run("git", ["rev-parse", "--verify", `${hash}~1`]).pipe(
					Effect.map(() => false),
					Effect.catch(() => Effect.succeed(true)),
				)
				return result
			})

			const getCommitDiff = Effect.fn("GitService.getCommitDiff")(function*(hash: string) {
				const isRoot = yield* isRootCommit(hash)
				const args = isRoot
					? ["diff", "-M", "--root", hash]
					: ["diff", "-M", `${hash}~1..${hash}`]
				const result = yield* command.run("git", args)
				return result.stdout
			})

			const getCommitFileDiff = Effect.fn("GitService.getCommitFileDiff")(function*(hash: string, filepath: string) {
				const isRoot = yield* isRootCommit(hash)
				const args = isRoot
					? ["diff", "--root", hash, "--", filepath]
					: ["diff", `${hash}~1..${hash}`, "--", filepath]
				const result = yield* command.run("git", args)
				if (result.stdout.trim().length > 0) return result.stdout

				// File-scoped diff empty — file was likely renamed/moved at this commit.
				// Fall back to full commit diff with rename detection.
				const fullArgs = isRoot
					? ["diff", "-M", "--root", hash]
					: ["diff", "-M", `${hash}~1..${hash}`]
				const fullResult = yield* command.run("git", fullArgs)
				return fullResult.stdout
			})

			const listFiles = Effect.fn("GitService.listFiles")(function*() {
				const result = yield* command.run("git", ["ls-tree", "-r", "--name-only", "HEAD"])
				return parseFiles(result.stdout)
			})

			const listFileHistory = Effect.fn("GitService.listFileHistory")(function*(filepath: string, limit?: number) {
				const result = yield* command.run("git", [
					"log", "--follow",
					"--format=%H\t%h\t%s\t%an\t%aI\t%D",
					`-n`, String(limit ?? config.fileHistoryLimit),
					"--", filepath,
				])
				return parseCommits(result.stdout)
			})

			const getDefaultBranch = Effect.fn("GitService.getDefaultBranch")(function*() {
				return yield* command.run("git", ["rev-parse", "--verify", "main"]).pipe(
					Effect.map(() => "main"),
					Effect.catch(() =>
						command.run("git", ["rev-parse", "--verify", "master"]).pipe(
							Effect.map(() => "master"),
							Effect.catch(() =>
								command.run("git", ["symbolic-ref", "refs/remotes/origin/HEAD"]).pipe(
									Effect.map((r) => r.stdout.trim().replace("refs/remotes/origin/", "")),
									Effect.catch(() => Effect.succeed("main")),
								),
							),
						),
					),
				)
			})

			const getBranchReviewDiff = Effect.fn("GitService.getBranchReviewDiff")(function*(targetBranch?: string) {
				const target = targetBranch ?? (yield* getDefaultBranch())
				const result = yield* command.run("git", ["diff", `${target}...HEAD`])
				return result.stdout
			})

			const getCommitsAhead = Effect.fn("GitService.getCommitsAhead")(function*(targetBranch?: string) {
				const target = targetBranch ?? (yield* getDefaultBranch())
				const result = yield* command.run("git", [
					"log",
					"--format=%H\t%h\t%s\t%an\t%aI\t%D",
					`${target}..HEAD`,
				])
				return parseCommits(result.stdout)
			})

			return GitService.of({
				getCurrentBranch,
				listBranches,
				listCommits,
				getCommitDiff,
				getCommitFileDiff,
				listFiles,
				listFileHistory,
				getDefaultBranch,
				getBranchReviewDiff,
				getCommitsAhead,
			})
		}),
	)

	static readonly layer = GitService.layerNoDeps.pipe(Layer.provide(CommandRunner.layer))
}
