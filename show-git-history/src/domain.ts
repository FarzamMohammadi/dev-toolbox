export type ViewId = "branches" | "commits" | "files" | "file-history" | "branch-review"

export type DiffMode = "file-scoped" | "full-commit"

export interface BranchItem {
	readonly name: string
	readonly isRemote: boolean
	readonly isCurrent: boolean
	readonly lastCommitHash: string
	readonly lastCommitDate: Date
	readonly trackingBranch: string | null
}

export interface CommitItem {
	readonly hash: string
	readonly shortHash: string
	readonly subject: string
	readonly author: string
	readonly date: Date
	readonly refs: string
}

export interface FileEntry {
	readonly path: string
}
