import type { ScrollBoxRenderable } from "@opentui/core"
import { useAtomValue } from "@effect/atom-react"
import { useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import { useEffect, useMemo, useRef } from "react"
import type { CommitItem } from "../domain.js"
import { formatRelativeDate } from "../date.js"
import { colors } from "../ui/colors.js"
import { Divider, fitCell, PlainLine, SectionTitle, TextLine } from "../ui/primitives.js"
import { wrapText } from "../ui/DetailsPane.js"
import { loadCommitsAtom, commitSelectedIndexAtom } from "../atoms.js"

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
	const authorWidth = Math.min(16, commit.author.length)
	const subjectWidth = Math.max(8, contentWidth - hashWidth - ageWidth - authorWidth - 4)

	return (
		<box height={1}>
			<TextLine fg={selected ? colors.selectedText : colors.text} bg={selected ? colors.selectedBg : undefined}>
				<span fg={selected ? colors.accent : colors.count}>{fitCell(commit.shortHash, hashWidth)}</span>
				<span> </span>
				<span>{fitCell(commit.subject, subjectWidth)}</span>
				<span fg={colors.muted}> {fitCell(commit.author, authorWidth)}</span>
				<span fg={colors.muted}> {fitCell(age, ageWidth, "right")}</span>
			</TextLine>
		</box>
	)
}

const CommitDetail = ({
	commit,
	contentWidth,
	paneWidth,
}: {
	commit: CommitItem
	contentWidth: number
	paneWidth: number
}) => {
	const wrappedSubject = wrapText(commit.subject, Math.max(1, paneWidth - 2))
	const age = formatRelativeDate(commit.date)
	const dateStr = commit.date.toLocaleString()

	return (
		<box flexDirection="column">
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.count}>{commit.shortHash}</span>
					<span fg={colors.muted}>  {commit.author}</span>
					<span fg={colors.muted}>{"  ".padEnd(Math.max(2, contentWidth - commit.shortHash.length - commit.author.length - age.length - 4))}</span>
					<span fg={colors.muted}>{age}</span>
				</TextLine>
			</box>
			<box height={wrappedSubject.length} flexDirection="column" paddingLeft={1} paddingRight={1}>
				{wrappedSubject.map((line, index) => (
					<PlainLine key={index} text={line} bold />
				))}
			</box>
			{commit.refs.length > 0 ? (
				<box height={1} paddingLeft={1} paddingRight={1}>
					<TextLine>
						<span fg={colors.accent}>{commit.refs}</span>
					</TextLine>
				</box>
			) : null}
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.muted}>{commit.hash}</span>
				</TextLine>
			</box>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.muted}>{dateStr}</span>
				</TextLine>
			</box>
			<Divider width={paneWidth} />
		</box>
	)
}

export const CommitHistoryView = ({
	branch,
	filterQuery,
	filterMode,
}: {
	branch: string
	filterQuery: string
	filterMode: boolean
}) => {
	const { width, height } = useTerminalDimensions()
	const isWide = width >= 100
	const result = useAtomValue(loadCommitsAtom)
	const selectedIndex = useAtomValue(commitSelectedIndexAtom)
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

	const listWidth = isWide ? Math.floor(width * 0.55) : width
	const detailWidth = isWide ? width - listWidth - 1 : width

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
				<SectionTitle title={`COMMITS  ${branch}`} />
				{filterMode || filterQuery.length > 0 ? (
					<TextLine>
						<span fg={colors.count}>/</span>
						<span fg={colors.muted}> </span>
						<span fg={filterMode ? colors.text : colors.count}>{filterQuery.length > 0 ? filterQuery : "type to filter..."}</span>
					</TextLine>
				) : null}
				{isLoading && commits.length === 0 ? <PlainLine text="- Loading commits..." fg={colors.muted} /> : null}
				{AsyncResult.isFailure(result) ? <PlainLine text="- Could not load commits." fg={colors.error} /> : null}
				{!isLoading && commits.length === 0 && AsyncResult.isSuccess(result) ? (
					<PlainLine text={filterQuery.length > 0 ? "- No matching commits." : "- No commits found."} fg={colors.muted} />
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
						<CommitDetail commit={selectedCommit} contentWidth={detailWidth - 2} paneWidth={detailWidth} />
					</box>
				</>
			) : null}
		</box>
	)
}
