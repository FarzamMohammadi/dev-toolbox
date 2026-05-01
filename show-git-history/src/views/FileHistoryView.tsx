import type { ScrollBoxRenderable } from "@opentui/core"
import { useAtomValue } from "@effect/atom-react"
import { useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import { useEffect, useMemo, useRef } from "react"
import type { CommitItem, DiffMode } from "../domain.js"
import { formatRelativeDate } from "../date.js"
import { colors } from "../ui/colors.js"
import { splitPatchFiles, patchRenderableLineCount, createDiffSyntaxStyle, type DiffState } from "../ui/diff.js"
import { Divider, fitCell, PlainLine, SectionTitle, TextLine } from "../ui/primitives.js"
import { LoadingPane, StatusCard } from "../ui/DetailsPane.js"
import { loadFileHistoryAtom, fileHistorySelectedIndexAtom, loadFileHistoryDiffAtom } from "../atoms.js"

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

const FileDiffPreview = ({
	diffState,
	paneWidth,
	height,
	diffMode,
	themeId,
}: {
	diffState: DiffState | undefined
	paneWidth: number
	height: number
	diffMode: DiffMode
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
		return <LoadingPane content={{ title: "Loading diff", hint: diffMode === "file-scoped" ? "File-scoped diff" : "Full commit diff" }} width={paneWidth} height={height} />
	}

	if (diffState.status === "error") {
		return <StatusCard content={{ title: "Could not load diff", hint: diffState.error }} width={paneWidth} />
	}

	if (readyFiles.length === 0 || !file) {
		return <LoadingPane content={{ title: "No changes", hint: "This commit has no diff for this file" }} width={paneWidth} height={height} />
	}

	const modeLabel = diffMode === "file-scoped" ? "file only" : `all files (${readyFiles.length})`

	return (
		<box flexDirection="column" height={height}>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.text}>{fitCell(file.name, Math.max(8, paneWidth - modeLabel.length - 4))}</span>
					<span fg={colors.muted}>  {modeLabel}</span>
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

export const FileHistoryView = ({
	filepath,
	filterQuery,
	filterMode,
	diffMode,
	themeId,
}: {
	filepath: string
	filterQuery: string
	filterMode: boolean
	diffMode: DiffMode
	themeId: string
}) => {
	const { width, height } = useTerminalDimensions()
	const isWide = width >= 100
	const result = useAtomValue(loadFileHistoryAtom)
	const selectedIndex = useAtomValue(fileHistorySelectedIndexAtom)
	const diffResult = useAtomValue(loadFileHistoryDiffAtom)
	const listScrollRef = useRef<ScrollBoxRenderable>(null)

	const commits = useMemo(() => {
		const data = AsyncResult.isSuccess(result) ? result.value : []
		if (filterQuery.length === 0) return data
		const lower = filterQuery.toLowerCase()
		return data.filter((c) =>
			c.subject.toLowerCase().includes(lower) ||
			c.shortHash.toLowerCase().includes(lower) ||
			c.author.toLowerCase().includes(lower),
		)
	}, [result, filterQuery])

	const safeIndex = commits.length > 0 ? Math.max(0, Math.min(selectedIndex, commits.length - 1)) : 0
	const selectedCommit = commits[safeIndex] ?? null
	const isLoading = AsyncResult.isWaiting(result)

	const listWidth = isWide ? Math.floor(width * 0.4) : width
	const detailWidth = isWide ? width - listWidth - 1 : width

	const filename = filepath.split("/").at(-1) ?? filepath
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

	return (
		<box flexDirection="row" height={height - 4}>
			<box width={listWidth} flexDirection="column">
				<SectionTitle title={`HISTORY  ${filename}`} />
				{filterMode || filterQuery.length > 0 ? (
					<TextLine>
						<span fg={colors.count}>/</span>
						<span fg={colors.muted}> </span>
						<span fg={filterMode ? colors.text : colors.count}>{filterQuery.length > 0 ? filterQuery : "type to filter..."}</span>
					</TextLine>
				) : null}
				<box height={1} paddingLeft={1}>
					<TextLine>
						<span fg={colors.muted}>{filepath}</span>
					</TextLine>
				</box>
				{isLoading && commits.length === 0 ? <PlainLine text="- Loading file history..." fg={colors.muted} /> : null}
				{AsyncResult.isFailure(result) ? <PlainLine text="- Could not load file history." fg={colors.error} /> : null}
				{!isLoading && commits.length === 0 && AsyncResult.isSuccess(result) ? (
					<PlainLine text={filterQuery.length > 0 ? "- No matching commits." : "- No history found."} fg={colors.muted} />
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
			{isWide && selectedCommit ? (
				<>
					<box width={1} flexDirection="column">
						{Array.from({ length: Math.max(1, height - 4) }, (_, index) => (
							<PlainLine key={index} text="│" fg={colors.separator} />
						))}
					</box>
					<box width={detailWidth} flexDirection="column">
						<FileDiffPreview
							diffState={diffState}
							paneWidth={detailWidth}
							height={Math.max(1, height - 4)}
							diffMode={diffMode}
							themeId={themeId}
						/>
					</box>
				</>
			) : null}
		</box>
	)
}
