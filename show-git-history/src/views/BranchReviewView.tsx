import type { ScrollBoxRenderable } from "@opentui/core"
import { useAtomValue } from "@effect/atom-react"
import { useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import { useEffect, useMemo, useRef } from "react"
import type { CommitItem } from "../domain.js"
import { formatRelativeDate } from "../date.js"
import { colors } from "../ui/colors.js"
import { splitPatchFiles, patchRenderableLineCount, createDiffSyntaxStyle, type DiffState } from "../ui/diff.js"
import { Divider, fitCell, PlainLine, SectionTitle, TextLine } from "../ui/primitives.js"
import { LoadingPane, StatusCard } from "../ui/DetailsPane.js"
import {
	currentBranchAtom,
	defaultBranchAtom,
	loadCommitsAheadAtom,
	loadBranchReviewDiffAtom,
	branchReviewCommitIndexAtom,
} from "../atoms.js"

const CommitRow = ({
	commit,
	selected,
	contentWidth,
}: {
	commit: CommitItem
	selected: boolean
	contentWidth: number
}) => {
	const age = formatRelativeDate(commit.date)
	const hashWidth = 8
	const ageWidth = age.length
	const subjectWidth = Math.max(8, contentWidth - hashWidth - ageWidth - 3)

	return (
		<box height={1}>
			<TextLine fg={selected ? colors.selectedText : colors.text} bg={selected ? colors.selectedBg : undefined}>
				<span fg={selected ? colors.accent : colors.count}>{fitCell(commit.shortHash, hashWidth)}</span>
				<span> </span>
				<span>{fitCell(commit.subject, subjectWidth)}</span>
				<span fg={colors.muted}> {fitCell(age, ageWidth, "right")}</span>
			</TextLine>
		</box>
	)
}

const BranchDiffPreview = ({
	diffState,
	paneWidth,
	height,
	themeId,
}: {
	diffState: DiffState | undefined
	paneWidth: number
	height: number
	themeId: string
}) => {
	const readyFiles = diffState?.status === "ready" ? diffState.files : []
	const file = readyFiles[0] ?? null
	const syntaxStyle = useMemo(() => createDiffSyntaxStyle(), [themeId])
	const diffHeight = useMemo(
		() => file ? patchRenderableLineCount(file.patch, "split", "none", paneWidth) : 1,
		[file?.patch, paneWidth],
	)

	if (!diffState || diffState.status === "loading") {
		return <LoadingPane content={{ title: "Loading diff", hint: "Branch review diff" }} width={paneWidth} height={height} />
	}

	if (diffState.status === "error") {
		return <StatusCard content={{ title: "Could not load diff", hint: diffState.error }} width={paneWidth} />
	}

	if (readyFiles.length === 0 || !file) {
		return <LoadingPane content={{ title: "No changes", hint: "This branch has no diff against the target" }} width={paneWidth} height={height} />
	}

	const fileCount = `${readyFiles.length} file${readyFiles.length === 1 ? "" : "s"} changed`

	return (
		<box flexDirection="column" height={height}>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.text}>{fitCell(file.name, Math.max(8, paneWidth - fileCount.length - 4))}</span>
					<span fg={colors.muted}>  {fileCount}</span>
				</TextLine>
			</box>
			<Divider width={paneWidth} />
			<scrollbox focused={false} flexGrow={1} scrollY scrollX={false}>
				<diff
					diff={file.patch}
					view="split"
					syncScroll
					filetype={file.filetype ?? "text"}
					syntaxStyle={syntaxStyle}
					showLineNumbers
					wrapMode="none"
					addedBg={colors.diff.addedBg}
					removedBg={colors.diff.removedBg}
					contextBg={colors.diff.contextBg}
					addedSignColor={colors.status.passing}
					removedSignColor={colors.status.failing}
					lineNumberFg={colors.muted}
					lineNumberBg={colors.diff.lineNumberBg}
					addedLineNumberBg={colors.diff.addedLineNumberBg}
					removedLineNumberBg={colors.diff.removedLineNumberBg}
					selectionBg={colors.selectedBg}
					selectionFg={colors.selectedText}
					height={diffHeight}
					style={{ flexShrink: 0 }}
				/>
			</scrollbox>
		</box>
	)
}

export const BranchReviewView = ({
	filterQuery,
	filterMode,
	themeId,
}: {
	filterQuery: string
	filterMode: boolean
	themeId: string
}) => {
	const { width, height } = useTerminalDimensions()
	const isWide = width >= 100

	const currentBranchResult = useAtomValue(currentBranchAtom)
	const defaultBranchResult = useAtomValue(defaultBranchAtom)
	const commitsResult = useAtomValue(loadCommitsAheadAtom)
	const diffResult = useAtomValue(loadBranchReviewDiffAtom)
	const selectedIndex = useAtomValue(branchReviewCommitIndexAtom)
	const listScrollRef = useRef<ScrollBoxRenderable>(null)

	const branchName = AsyncResult.isSuccess(currentBranchResult) ? currentBranchResult.value : null
	const targetName = AsyncResult.isSuccess(defaultBranchResult) ? defaultBranchResult.value : "main"

	const commits = useMemo(() => {
		const data = AsyncResult.isSuccess(commitsResult) ? commitsResult.value : []
		if (filterQuery.length === 0) return data
		const lower = filterQuery.toLowerCase()
		return data.filter((c) =>
			c.subject.toLowerCase().includes(lower) ||
			c.shortHash.toLowerCase().includes(lower) ||
			c.author.toLowerCase().includes(lower),
		)
	}, [commitsResult, filterQuery])

	const isOnDefault = branchName !== null && branchName === targetName
	const safeIndex = commits.length > 0 ? Math.max(0, Math.min(selectedIndex, commits.length - 1)) : 0
	const isLoading = AsyncResult.isWaiting(commitsResult)

	const listWidth = isWide ? Math.floor(width * 0.4) : width
	const detailWidth = isWide ? width - listWidth - 1 : width
	const contentHeight = Math.max(1, height - 4)

	const diffState: DiffState | undefined = useMemo(() => {
		if (AsyncResult.isWaiting(diffResult)) return { status: "loading" as const }
		if (AsyncResult.isSuccess(diffResult)) {
			const files = splitPatchFiles(diffResult.value)
			return { status: "ready" as const, patch: diffResult.value, files }
		}
		if (AsyncResult.isFailure(diffResult)) return { status: "error" as const, error: "Failed to load diff" }
		return undefined
	}, [diffResult])

	useEffect(() => {
		const sb = listScrollRef.current
		if (!sb || commits.length === 0) return
		const viewportHeight = sb.viewport.height
		if (viewportHeight <= 0) return
		if (safeIndex < sb.scrollTop) {
			sb.scrollTo({ x: 0, y: safeIndex })
		} else if (safeIndex >= sb.scrollTop + viewportHeight) {
			sb.scrollTo({ x: 0, y: safeIndex - viewportHeight + 1 })
		}
	}, [safeIndex, commits.length])

	if (isOnDefault && !isLoading) {
		return (
			<LoadingPane
				content={{ title: `On ${targetName}`, hint: "Nothing to review" }}
				width={width}
				height={contentHeight}
			/>
		)
	}

	const commitCountLabel = commits.length === 1 ? "1 commit ahead" : `${commits.length} commits ahead`

	return (
		<box flexDirection="row" height={height - 4}>
			<box width={listWidth} flexDirection="column">
				<SectionTitle title="BRANCH REVIEW" />
				{branchName ? (
					<box height={1} paddingLeft={1}>
						<TextLine>
							<span fg={colors.accent}>{branchName}</span>
							<span fg={colors.muted}> → {targetName}</span>
							{!isLoading && commits.length > 0 ? (
								<span fg={colors.muted}>  {commitCountLabel}</span>
							) : null}
						</TextLine>
					</box>
				) : null}
				{filterMode || filterQuery.length > 0 ? (
					<TextLine>
						<span fg={colors.count}>/</span>
						<span fg={colors.muted}> </span>
						<span fg={filterMode ? colors.text : colors.count}>{filterQuery.length > 0 ? filterQuery : "type to filter..."}</span>
					</TextLine>
				) : null}
				{isLoading && commits.length === 0 ? <PlainLine text="- Loading branch review..." fg={colors.muted} /> : null}
				{AsyncResult.isFailure(commitsResult) ? <PlainLine text="- Could not load branch review." fg={colors.error} /> : null}
				{!isLoading && commits.length === 0 && AsyncResult.isSuccess(commitsResult) && !isOnDefault ? (
					<PlainLine text={filterQuery.length > 0 ? "- No matching commits." : "- No commits ahead."} fg={colors.muted} />
				) : null}
				<scrollbox ref={listScrollRef} scrollY scrollX={false} flexGrow={1}>
					{commits.map((commit, index) => (
						<CommitRow
							key={commit.hash}
							commit={commit}
							selected={index === safeIndex}
							contentWidth={listWidth - 2}
						/>
					))}
				</scrollbox>
			</box>
			{isWide && diffState ? (
				<>
					<box width={1} flexDirection="column">
						{Array.from({ length: contentHeight }, (_, index) => (
							<PlainLine key={index} text="│" fg={colors.separator} />
						))}
					</box>
					<box width={detailWidth} flexDirection="column">
						<BranchDiffPreview
							diffState={diffState}
							paneWidth={detailWidth}
							height={contentHeight}
							themeId={themeId}
						/>
					</box>
				</>
			) : null}
		</box>
	)
}
