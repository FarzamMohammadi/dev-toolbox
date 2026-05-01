import type { ScrollBoxRenderable } from "@opentui/core"
import { useAtomValue } from "@effect/atom-react"
import { useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import { useEffect, useMemo, useRef } from "react"
import type { FileEntry } from "../domain.js"
import { colors } from "../ui/colors.js"
import { fitCell, PlainLine, SectionTitle, TextLine } from "../ui/primitives.js"
import { filesAtom, fileSelectedIndexAtom } from "../atoms.js"

const FileRow = ({
	file,
	selected,
	contentWidth,
}: {
	file: FileEntry
	selected: boolean
	contentWidth: number
}) => (
	<box height={1}>
		<TextLine fg={selected ? colors.selectedText : colors.text} bg={selected ? colors.selectedBg : undefined}>
			<span fg={selected ? colors.accent : colors.muted}>  </span>
			<span>{fitCell(file.path, contentWidth - 2)}</span>
		</TextLine>
	</box>
)

export const FileBrowserView = ({
	filterQuery,
	filterMode,
}: {
	filterQuery: string
	filterMode: boolean
}) => {
	const { width, height } = useTerminalDimensions()
	const contentWidth = Math.max(20, width - 2)
	const result = useAtomValue(filesAtom)
	const selectedIndex = useAtomValue(fileSelectedIndexAtom)
	const listScrollRef = useRef<ScrollBoxRenderable>(null)

	const files = useMemo(() => {
		const data = AsyncResult.isSuccess(result) ? result.value : []
		if (filterQuery.length === 0) return data
		const lower = filterQuery.toLowerCase()
		return data.filter((f) => f.path.toLowerCase().includes(lower))
	}, [result, filterQuery])

	const safeIndex = files.length > 0 ? Math.max(0, Math.min(selectedIndex, files.length - 1)) : 0
	const isLoading = AsyncResult.isWaiting(result)

	useEffect(() => {
		const sb = listScrollRef.current
		if (!sb || files.length === 0) return
		const viewportHeight = sb.viewport.height
		if (viewportHeight <= 0) return
		if (safeIndex < sb.scrollTop) {
			sb.scrollTo({ x: 0, y: safeIndex })
		} else if (safeIndex >= sb.scrollTop + viewportHeight) {
			sb.scrollTo({ x: 0, y: safeIndex - viewportHeight + 1 })
		}
	}, [safeIndex, files.length])

	return (
		<box flexDirection="column" height={height - 4}>
			<SectionTitle title="FILES" />
			{filterMode || filterQuery.length > 0 ? (
				<TextLine>
					<span fg={colors.count}>/</span>
					<span fg={colors.muted}> </span>
					<span fg={filterMode ? colors.text : colors.count}>{filterQuery.length > 0 ? filterQuery : "type to filter..."}</span>
				</TextLine>
			) : null}
			{isLoading && files.length === 0 ? <PlainLine text="- Loading files..." fg={colors.muted} /> : null}
			{AsyncResult.isFailure(result) ? <PlainLine text="- Could not load files." fg={colors.error} /> : null}
			{!isLoading && files.length === 0 && AsyncResult.isSuccess(result) ? (
				<PlainLine text={filterQuery.length > 0 ? "- No matching files." : "- No files found."} fg={colors.muted} />
			) : null}
			<scrollbox ref={listScrollRef} scrollY scrollX={false} flexGrow={1}>
				{files.map((file, index) => (
					<FileRow
						key={file.path}
						file={file}
						selected={index === safeIndex}
						contentWidth={contentWidth}
					/>
				))}
			</scrollbox>
		</box>
	)
}
