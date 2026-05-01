import type { ScrollBoxRenderable } from "@opentui/core"
import { useAtom, useAtomRefresh, useAtomSet, useAtomValue } from "@effect/atom-react"
import { useKeyboard, useRenderer, useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import * as Atom from "effect/unstable/reactivity/Atom"
import { useEffect, useMemo, useRef, useState } from "react"
import type { DiffMode, ViewId } from "./domain.js"
import { colors, setActiveTheme, themeDefinitions, type ThemeId } from "./ui/colors.js"
import { splitPatchFiles, type DiffState } from "./ui/diff.js"
import { LoadingPane } from "./ui/DetailsPane.js"
import { FooterHints } from "./ui/FooterHints.js"
import { Divider, TextLine } from "./ui/primitives.js"
import { initialThemeModalState, ThemeModal } from "./ui/modals.js"
import {
	branchesAtom,
	filesAtom,
	loadCommitsAtom,
	loadFileHistoryAtom,
	loadCommitDiffAtom,
	loadFileHistoryDiffAtom,
	branchSelectedIndexAtom,
	commitSelectedIndexAtom,
	fileSelectedIndexAtom,
	fileHistorySelectedIndexAtom,
	loadBranchReviewDiffAtom,
	loadCommitsAheadAtom,
	branchReviewCommitIndexAtom,
} from "./atoms.js"
import { BranchListView } from "./views/BranchListView.js"
import { CommitHistoryView } from "./views/CommitHistoryView.js"
import { FileBrowserView } from "./views/FileBrowserView.js"
import { FileHistoryView } from "./views/FileHistoryView.js"
import { BranchReviewView } from "./views/BranchReviewView.js"
import { DiffView } from "./views/DiffView.js"

const LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"] as const

const activeViewAtom = Atom.make<ViewId>("branches").pipe(Atom.keepAlive)
const selectedBranchAtom = Atom.make<string | null>(null).pipe(Atom.keepAlive)
const selectedFileAtom = Atom.make<string | null>(null).pipe(Atom.keepAlive)
const selectedCommitAtom = Atom.make<string | null>(null).pipe(Atom.keepAlive)
const diffModeAtom = Atom.make<DiffMode>("file-scoped").pipe(Atom.keepAlive)
const themeIdAtom = Atom.make<ThemeId>("git-history").pipe(Atom.keepAlive)
const themeModalAtom = Atom.make(initialThemeModalState).pipe(Atom.keepAlive)
const noticeAtom = Atom.make<string | null>(null).pipe(Atom.keepAlive)
const filterQueryAtom = Atom.make("").pipe(Atom.keepAlive)
const filterModeAtom = Atom.make(false).pipe(Atom.keepAlive)
const pendingGAtom = Atom.make(false).pipe(Atom.keepAlive)

const diffFullViewAtom = Atom.make(false).pipe(Atom.keepAlive)
const diffFileIndexAtom = Atom.make(0).pipe(Atom.keepAlive)
const diffRenderViewAtom = Atom.make<"unified" | "split">("split").pipe(Atom.keepAlive)
const diffWrapModeAtom = Atom.make<"none" | "word">("none").pipe(Atom.keepAlive)

const deleteLastWord = (value: string) => value.replace(/\s*\S+\s*$/, "")

const clipboardCommands = (): readonly (readonly string[])[] => {
	if (process.platform === "darwin") return [["pbcopy"]]
	if (process.platform === "linux") {
		return [
			...(process.env.WAYLAND_DISPLAY ? [["wl-copy"]] : []),
			["xclip", "-selection", "clipboard"],
			["xsel", "--clipboard", "--input"],
		]
	}
	return []
}

const copyToClipboard = async (text: string) => {
	const commands = clipboardCommands()
	for (const command of commands) {
		try {
			const proc = Bun.spawn({ cmd: [...command], stdin: "pipe", stdout: "ignore", stderr: "pipe" })
			proc.stdin.write(text)
			proc.stdin.end()
			const exitCode = await proc.exited
			if (exitCode === 0) return
		} catch {
			continue
		}
	}
	throw new Error("Clipboard is not available")
}

const viewLabel = (view: ViewId) => {
	if (view === "branches") return "Branches"
	if (view === "commits") return "Commits"
	if (view === "files") return "Files"
	if (view === "file-history") return "File History"
	if (view === "branch-review") return "Branch Review"
	return ""
}

export const App = () => {
	const renderer = useRenderer()
	const { width, height } = useTerminalDimensions()
	const [activeView, setActiveView] = useAtom(activeViewAtom)
	const [selectedBranch, setSelectedBranch] = useAtom(selectedBranchAtom)
	const [selectedFile, setSelectedFile] = useAtom(selectedFileAtom)
	const [selectedCommit, setSelectedCommit] = useAtom(selectedCommitAtom)
	const [diffMode, setDiffMode] = useAtom(diffModeAtom)
	const [themeId, setThemeId] = useAtom(themeIdAtom)
	const [themeModal, setThemeModal] = useAtom(themeModalAtom)
	const [notice, setNotice] = useAtom(noticeAtom)
	const [filterQuery, setFilterQuery] = useAtom(filterQueryAtom)
	const [filterMode, setFilterMode] = useAtom(filterModeAtom)
	const [pendingG, setPendingG] = useAtom(pendingGAtom)
	const [diffFullView, setDiffFullView] = useAtom(diffFullViewAtom)
	const [diffFileIndex, setDiffFileIndex] = useAtom(diffFileIndexAtom)
	const [diffRenderView, setDiffRenderView] = useAtom(diffRenderViewAtom)
	const [diffWrapMode, setDiffWrapMode] = useAtom(diffWrapModeAtom)

	const branchResult = useAtomValue(branchesAtom)
	const commitResult = useAtomValue(loadCommitsAtom)
	const fileResult = useAtomValue(filesAtom)
	const fileHistoryResult = useAtomValue(loadFileHistoryAtom)
	const commitDiffResult = useAtomValue(loadCommitDiffAtom)
	const fileHistoryDiffResult = useAtomValue(loadFileHistoryDiffAtom)
	const branchReviewDiffResult = useAtomValue(loadBranchReviewDiffAtom)
	const commitsAheadResult = useAtomValue(loadCommitsAheadAtom)

	const refreshBranches = useAtomRefresh(branchesAtom)
	const refreshFiles = useAtomRefresh(filesAtom)

	const branchSelectedIndex = useAtomValue(branchSelectedIndexAtom)
	const commitSelectedIndex = useAtomValue(commitSelectedIndexAtom)
	const fileSelectedIndex = useAtomValue(fileSelectedIndexAtom)
	const fileHistorySelectedIndex = useAtomValue(fileHistorySelectedIndexAtom)
	const branchReviewCommitIndex = useAtomValue(branchReviewCommitIndexAtom)

	const setBranchSelectedIndex = useAtomSet(branchSelectedIndexAtom)
	const setCommitSelectedIndex = useAtomSet(commitSelectedIndexAtom)
	const setFileSelectedIndex = useAtomSet(fileSelectedIndexAtom)
	const setFileHistorySelectedIndex = useAtomSet(fileHistorySelectedIndexAtom)
	const setBranchReviewCommitIndex = useAtomSet(branchReviewCommitIndexAtom)

	const triggerLoadCommits = useAtomSet(loadCommitsAtom)
	const triggerLoadFileHistory = useAtomSet(loadFileHistoryAtom)
	const triggerLoadCommitDiff = useAtomSet(loadCommitDiffAtom)
	const triggerLoadFileHistoryDiff = useAtomSet(loadFileHistoryDiffAtom)
	const triggerLoadBranchReviewDiff = useAtomSet(loadBranchReviewDiffAtom)
	const triggerLoadCommitsAhead = useAtomSet(loadCommitsAheadAtom)

	const scrollRef = useRef<ScrollBoxRenderable>(null)
	const [loadingFrame, setLoadingFrame] = useState(0)
	const loadingIndicator = LOADING_FRAMES[loadingFrame % LOADING_FRAMES.length]!

	setActiveTheme(themeId)

	const filterLower = filterQuery.toLowerCase()

	const filteredBranches = useMemo(() => {
		const data = AsyncResult.isSuccess(branchResult) ? branchResult.value : []
		if (filterQuery.length === 0) return data
		return data.filter((b) => b.name.toLowerCase().includes(filterLower))
	}, [branchResult, filterQuery])

	const filteredCommits = useMemo(() => {
		const data = AsyncResult.isSuccess(commitResult) ? commitResult.value : []
		if (filterQuery.length === 0) return data
		return data.filter((c) =>
			c.subject.toLowerCase().includes(filterLower) ||
			c.shortHash.toLowerCase().includes(filterLower) ||
			c.author.toLowerCase().includes(filterLower))
	}, [commitResult, filterQuery])

	const filteredFiles = useMemo(() => {
		const data = AsyncResult.isSuccess(fileResult) ? fileResult.value : []
		if (filterQuery.length === 0) return data
		return data.filter((f) => f.path.toLowerCase().includes(filterLower))
	}, [fileResult, filterQuery])

	const filteredFileHistory = useMemo(() => {
		const data = AsyncResult.isSuccess(fileHistoryResult) ? fileHistoryResult.value : []
		if (filterQuery.length === 0) return data
		return data.filter((c) =>
			c.subject.toLowerCase().includes(filterLower) ||
			c.shortHash.toLowerCase().includes(filterLower) ||
			c.author.toLowerCase().includes(filterLower))
	}, [fileHistoryResult, filterQuery])

	const filteredCommitsAhead = useMemo(() => {
		const data = AsyncResult.isSuccess(commitsAheadResult) ? commitsAheadResult.value : []
		if (filterQuery.length === 0) return data
		return data.filter((c) =>
			c.subject.toLowerCase().includes(filterLower) ||
			c.shortHash.toLowerCase().includes(filterLower) ||
			c.author.toLowerCase().includes(filterLower))
	}, [commitsAheadResult, filterQuery])

	useEffect(() => {
		const interval = setInterval(() => setLoadingFrame((f) => f + 1), 100)
		return () => clearInterval(interval)
	}, [])

	useEffect(() => {
		if (notice) {
			const timer = setTimeout(() => setNotice(null), 2500)
			return () => clearTimeout(timer)
		}
	}, [notice])

	useEffect(() => {
		if (activeView === "file-history") {
			const commit = filteredFileHistory[fileHistorySelectedIndex]
			if (commit && selectedFile) {
				triggerLoadFileHistoryDiff({ hash: commit.hash, filepath: selectedFile, mode: diffMode })
			}
		}
	}, [fileHistorySelectedIndex, activeView])

	const currentDiffState: DiffState | undefined = useMemo(() => {
		const result = activeView === "file-history"
			? fileHistoryDiffResult
			: activeView === "branch-review"
				? branchReviewDiffResult
				: commitDiffResult
		if (AsyncResult.isWaiting(result)) return { status: "loading" as const }
		if (AsyncResult.isSuccess(result)) {
			const files = splitPatchFiles(result.value)
			return { status: "ready" as const, patch: result.value, files }
		}
		if (AsyncResult.isFailure(result)) return { status: "error" as const, error: "Failed to load diff" }
		return undefined
	}, [activeView, commitDiffResult, fileHistoryDiffResult, branchReviewDiffResult])

	const getListLength = (): number => {
		if (activeView === "branches") return filteredBranches.length
		if (activeView === "commits") return filteredCommits.length
		if (activeView === "files") return filteredFiles.length
		if (activeView === "file-history") return filteredFileHistory.length
		if (activeView === "branch-review") return filteredCommitsAhead.length
		return 0
	}

	const getSelectedIndex = (): number => {
		if (activeView === "branches") return branchSelectedIndex
		if (activeView === "commits") return commitSelectedIndex
		if (activeView === "files") return fileSelectedIndex
		if (activeView === "file-history") return fileHistorySelectedIndex
		if (activeView === "branch-review") return branchReviewCommitIndex
		return 0
	}

	const setSelectedIndex = (index: number) => {
		if (activeView === "branches") setBranchSelectedIndex(index)
		else if (activeView === "commits") setCommitSelectedIndex(index)
		else if (activeView === "files") setFileSelectedIndex(index)
		else if (activeView === "file-history") setFileHistorySelectedIndex(index)
		else if (activeView === "branch-review") setBranchReviewCommitIndex(index)
	}

	const moveSelection = (delta: number) => {
		const length = getListLength()
		if (length === 0) return
		const current = getSelectedIndex()
		setSelectedIndex(Math.max(0, Math.min(length - 1, current + delta)))
	}

	const handleEnter = () => {
		if (activeView === "branches") {
			const branch = filteredBranches[branchSelectedIndex]
			if (branch) {
				setSelectedBranch(branch.name)
				triggerLoadCommits(branch.name)
				setActiveView("commits")
				setFilterQuery("")
				setFilterMode(false)
			}
		} else if (activeView === "commits") {
			const commit = filteredCommits[commitSelectedIndex]
			if (commit) {
				openCommitDiff(commit.hash)
			}
		} else if (activeView === "files") {
			const file = filteredFiles[fileSelectedIndex]
			if (file) {
				setSelectedFile(file.path)
				triggerLoadFileHistory(file.path)
				setActiveView("file-history")
				setFilterQuery("")
				setFilterMode(false)
			}
		} else if (activeView === "file-history") {
			const commit = filteredFileHistory[fileHistorySelectedIndex]
			if (commit && selectedFile) {
				openFileHistoryDiff(commit.hash)
			}
		} else if (activeView === "branch-review") {
			setDiffFileIndex(0)
			setDiffFullView(true)
		}
	}

	const openCommitDiff = (hash: string) => {
		setSelectedCommit(hash)
		setDiffFileIndex(0)
		setDiffFullView(true)
		triggerLoadCommitDiff({ hash })
	}

	const openFileHistoryDiff = (hash: string) => {
		setSelectedCommit(hash)
		setDiffFileIndex(0)
		setDiffFullView(true)
		if (selectedFile) {
			triggerLoadFileHistoryDiff({ hash, filepath: selectedFile, mode: diffMode })
		}
	}

	useKeyboard((key) => {
		if (key.name === "q" || (key.ctrl && key.name === "c")) {
			if (themeModal.open) {
				setActiveTheme(themeModal.initialThemeId)
				setThemeId(themeModal.initialThemeId)
				setThemeModal(initialThemeModalState)
				return
			}
			renderer.destroy()
			return
		}

		if (themeModal.open) {
			if (key.name === "escape") {
				setActiveTheme(themeModal.initialThemeId)
				setThemeId(themeModal.initialThemeId)
				setThemeModal(initialThemeModalState)
				return
			}
			if (key.name === "return" || key.name === "enter") {
				const selected = themeDefinitions[themeModal.selectedIndex]
				if (selected) {
					setThemeId(selected.id)
					setActiveTheme(selected.id)
				}
				setThemeModal(initialThemeModalState)
				return
			}
			if (key.name === "up" || key.name === "k") {
				const newIndex = Math.max(0, themeModal.selectedIndex - 1)
				setThemeModal({ ...themeModal, selectedIndex: newIndex })
				const theme = themeDefinitions[newIndex]
				if (theme) setActiveTheme(theme.id)
				return
			}
			if (key.name === "down" || key.name === "j") {
				const newIndex = Math.min(themeDefinitions.length - 1, themeModal.selectedIndex + 1)
				setThemeModal({ ...themeModal, selectedIndex: newIndex })
				const theme = themeDefinitions[newIndex]
				if (theme) setActiveTheme(theme.id)
				return
			}
			return
		}

		if (filterMode) {
			if (key.name === "escape") {
				setFilterMode(false)
				setFilterQuery("")
				return
			}
			if (key.name === "return" || key.name === "enter") {
				setFilterMode(false)
				return
			}
			if (key.name === "backspace") {
				setFilterQuery((q) => q.slice(0, -1))
				return
			}
			if (key.ctrl && key.name === "u") {
				setFilterQuery("")
				return
			}
			if (key.ctrl && key.name === "w") {
				setFilterQuery(deleteLastWord)
				return
			}
			if (key.name === "up") { moveSelection(-1); return }
			if (key.name === "down") { moveSelection(1); return }
			if (!key.ctrl && !key.meta && key.sequence.length === 1 && key.name !== "return") {
				setFilterQuery((q) => q + key.sequence)
				return
			}
			return
		}

		if (diffFullView) {
			if (key.name === "escape") {
				setDiffFullView(false)
				return
			}
			if (key.name === "up" || key.name === "k") {
				scrollRef.current?.scrollBy({ x: 0, y: -1 })
				return
			}
			if (key.name === "down" || key.name === "j") {
				scrollRef.current?.scrollBy({ x: 0, y: 1 })
				return
			}
			if (key.ctrl && key.name === "u") {
				scrollRef.current?.scrollBy({ x: 0, y: -Math.floor(height / 2) })
				return
			}
			if (key.ctrl && (key.name === "d" || key.name === "v")) {
				scrollRef.current?.scrollBy({ x: 0, y: Math.floor(height / 2) })
				return
			}
			if (key.name === "home") {
				scrollRef.current?.scrollTo({ x: 0, y: 0 })
				return
			}
			if (key.name === "end") {
				scrollRef.current?.scrollTo({ x: 0, y: Number.MAX_SAFE_INTEGER })
				return
			}
			if (key.name === "pageup") {
				scrollRef.current?.scrollBy({ x: 0, y: -Math.floor(height / 2) })
				return
			}
			if (key.name === "pagedown") {
				scrollRef.current?.scrollBy({ x: 0, y: Math.floor(height / 2) })
				return
			}
			if (key.name === "v") {
				setDiffRenderView((v) => v === "unified" ? "split" : "unified")
				return
			}
			if (key.name === "w") {
				setDiffWrapMode((m) => m === "none" ? "word" : "none")
				return
			}
			if (key.name === "]" || key.name === "right" || key.name === "l") {
				const fileCount = currentDiffState?.status === "ready" ? currentDiffState.files.length : 0
				setDiffFileIndex((i) => Math.min(fileCount - 1, i + 1))
				scrollRef.current?.scrollTo({ x: 0, y: 0 })
				return
			}
			if (key.name === "[" || key.name === "left" || key.name === "h") {
				setDiffFileIndex((i) => Math.max(0, i - 1))
				scrollRef.current?.scrollTo({ x: 0, y: 0 })
				return
			}
			if (key.name === "f" && activeView === "file-history") {
				const newMode: DiffMode = diffMode === "file-scoped" ? "full-commit" : "file-scoped"
				setDiffMode(newMode)
				if (selectedCommit && selectedFile) {
					triggerLoadFileHistoryDiff({ hash: selectedCommit, filepath: selectedFile, mode: newMode })
				}
				return
			}
			if (key.name === "G" || (key.name === "g" && key.shift)) {
				scrollRef.current?.scrollTo({ x: 0, y: Number.MAX_SAFE_INTEGER })
				setPendingG(false)
				return
			}
			if (key.name === "g") {
				if (pendingG) {
					scrollRef.current?.scrollTo({ x: 0, y: 0 })
					setPendingG(false)
				} else {
					setPendingG(true)
					setTimeout(() => setPendingG(false), 500)
				}
				return
			}
			return
		}

		if (key.name === "T" || (key.name === "t" && key.shift)) {
			const currentIndex = themeDefinitions.findIndex((t) => t.id === themeId)
			setThemeModal({ open: true, selectedIndex: Math.max(0, currentIndex), initialThemeId: themeId })
			return
		}

		if (key.name === "/") {
			setFilterMode(true)
			return
		}

		if (key.name === "escape") {
			if (filterQuery.length > 0) {
				setFilterQuery("")
				return
			}
			if (activeView === "commits") {
				setActiveView("branches")
				return
			}
			if (activeView === "file-history") {
				setActiveView("files")
				return
			}
			return
		}

		if (key.name === "1") { setActiveView("branches"); setFilterQuery(""); setFilterMode(false); return }
		if (key.name === "2") { setActiveView("files"); setFilterQuery(""); setFilterMode(false); return }
		if (key.name === "3") {
			setActiveView("branch-review")
			setFilterQuery("")
			setFilterMode(false)
			triggerLoadCommitsAhead({})
			triggerLoadBranchReviewDiff({})
			return
		}

		if (key.name === "b" && activeView === "commits") {
			setActiveView("branches")
			return
		}

		if (key.name === "r") {
			if (activeView === "branches") refreshBranches()
			else if (activeView === "commits" && selectedBranch) triggerLoadCommits(selectedBranch)
			else if (activeView === "files") refreshFiles()
			else if (activeView === "file-history" && selectedFile) triggerLoadFileHistory(selectedFile)
			else if (activeView === "branch-review") {
				triggerLoadCommitsAhead({})
				triggerLoadBranchReviewDiff({})
			}
			return
		}

		if (key.name === "G" || (key.name === "g" && key.shift)) {
			const length = getListLength()
			if (length > 0) setSelectedIndex(length - 1)
			return
		}

		if (key.name === "g") {
			if (pendingG) {
				setSelectedIndex(0)
				setPendingG(false)
				return
			}
			setPendingG(true)
			setTimeout(() => setPendingG(false), 500)
			return
		}

		if (key.name === "up" || key.name === "k") { moveSelection(-1); return }
		if (key.name === "down" || key.name === "j") { moveSelection(1); return }

		if (key.ctrl && key.name === "u") { moveSelection(-Math.floor(height / 2)); return }
		if (key.ctrl && key.name === "d") { moveSelection(Math.floor(height / 2)); return }

		if (key.name === "return" || key.name === "enter") { handleEnter(); return }

		if ((key.name === "d" || key.name === "p") && (activeView === "commits" || activeView === "file-history" || activeView === "branch-review")) {
			handleEnter()
			return
		}

		if (key.name === "f" && activeView === "file-history") {
			const newMode: DiffMode = diffMode === "file-scoped" ? "full-commit" : "file-scoped"
			setDiffMode(newMode)
			const commit = filteredFileHistory[fileHistorySelectedIndex]
			if (commit && selectedFile) {
				triggerLoadFileHistoryDiff({ hash: commit.hash, filepath: selectedFile, mode: newMode })
			}
			return
		}

		if (key.name === "y" && activeView === "commits") {
			const commit = filteredCommits[commitSelectedIndex]
			if (commit) {
				const text = `${commit.shortHash} ${commit.subject}`
				void copyToClipboard(text)
					.then(() => setNotice("Copied to clipboard"))
					.catch(() => setNotice("Copy failed"))
			}
			return
		}
	})

	const contentHeight = Math.max(1, height - 3)

	const diffTitle = activeView === "branch-review"
		? "Branch Review"
		: selectedCommit
			? activeView === "file-history" && selectedFile
				? `${selectedCommit.slice(0, 8)}  ${selectedFile.split("/").at(-1) ?? selectedFile}`
				: selectedCommit.slice(0, 8)
			: ""

	const hasSelection = getListLength() > 0
	const isLoading = activeView === "branches" ? AsyncResult.isWaiting(branchResult)
		: activeView === "commits" ? AsyncResult.isWaiting(commitResult)
		: activeView === "files" ? AsyncResult.isWaiting(fileResult)
		: activeView === "file-history" ? AsyncResult.isWaiting(fileHistoryResult)
		: activeView === "branch-review" ? AsyncResult.isWaiting(commitsAheadResult)
		: false

	const modalWidth = Math.min(60, width - 4)
	const modalHeight = Math.min(20, height - 4)
	const modalLeft = Math.floor((width - modalWidth) / 2)
	const modalTop = Math.floor((height - modalHeight) / 2)

	return (
		<box width={width} height={height} flexDirection="column" backgroundColor={colors.background}>
			<box height={1}>
				<TextLine fg={colors.muted}>
					<span fg={colors.accent}> GIT HISTORY</span>
					<span fg={colors.separator}> │ </span>
					<span fg={colors.text}>{viewLabel(activeView)}</span>
					{notice ? (
						<>
							<span fg={colors.separator}> │ </span>
							<span fg={colors.accent}>{notice}</span>
						</>
					) : null}
				</TextLine>
			</box>
			<Divider width={width} />

			{diffFullView ? (
				<box flexGrow={1}>
					<DiffView
						diffState={currentDiffState}
						fileIndex={diffFileIndex}
						view={diffRenderView}
						wrapMode={diffWrapMode}
						paneWidth={width}
						height={contentHeight}
						loadingIndicator={loadingIndicator}
						scrollRef={scrollRef}
						themeId={themeId}
						title={diffTitle}
						{...(activeView === "file-history" ? { diffMode } : {})}
					/>
				</box>
			) : (
				<box flexGrow={1}>
					{activeView === "branches" ? (
						<BranchListView
							filterQuery={filterQuery}
							filterMode={filterMode}
						/>
					) : activeView === "commits" && selectedBranch ? (
						<CommitHistoryView
							branch={selectedBranch}
							filterQuery={filterQuery}
							filterMode={filterMode}
						/>
					) : activeView === "files" ? (
						<FileBrowserView
							filterQuery={filterQuery}
							filterMode={filterMode}
						/>
					) : activeView === "file-history" && selectedFile ? (
						<FileHistoryView
							filepath={selectedFile}
							filterQuery={filterQuery}
							filterMode={filterMode}
							diffMode={diffMode}
							themeId={themeId}
						/>
					) : activeView === "branch-review" ? (
						<BranchReviewView
							filterQuery={filterQuery}
							filterMode={filterMode}
							themeId={themeId}
						/>
					) : (
						<LoadingPane content={{ title: "Git History", hint: "Select a view with 1, 2, or 3" }} width={width} height={contentHeight} />
					)}
				</box>
			)}

			<Divider width={width} />
			<box height={1}>
				<FooterHints
					view={activeView}
					filterEditing={filterMode}
					showFilterClear={filterQuery.length > 0}
					diffFullView={diffFullView}
					isFileHistory={activeView === "file-history"}
					hasSelection={hasSelection}
					isLoading={isLoading}
					loadingIndicator={loadingIndicator}
				/>
			</box>

			{themeModal.open ? (
				<ThemeModal
					state={themeModal}
					activeThemeId={themeId}
					modalWidth={modalWidth}
					modalHeight={modalHeight}
					offsetLeft={modalLeft}
					offsetTop={modalTop}
				/>
			) : null}
		</box>
	)
}
