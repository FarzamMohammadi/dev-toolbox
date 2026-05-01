import { TextAttributes, type ScrollBoxRenderable } from "@opentui/core"
import { useAtomValue } from "@effect/atom-react"
import { useTerminalDimensions } from "@opentui/react"
import * as AsyncResult from "effect/unstable/reactivity/AsyncResult"
import { useEffect, useMemo, useRef } from "react"
import type { BranchItem } from "../domain.js"
import { formatRelativeDate } from "../date.js"
import { colors } from "../ui/colors.js"
import { branchColor } from "../ui/formatters.js"
import { fitCell, PlainLine, SectionTitle, TextLine } from "../ui/primitives.js"
import { branchesAtom, branchSelectedIndexAtom } from "../atoms.js"

const GROUP_ICON = "◆"

const BranchRow = ({
	branch,
	selected,
	contentWidth,
}: {
	branch: BranchItem
	selected: boolean
	contentWidth: number
}) => {
	const age = formatRelativeDate(branch.lastCommitDate)
	const prefix = branch.isCurrent ? "* " : branch.isRemote ? "  " : "  "
	const nameWidth = Math.max(8, contentWidth - prefix.length - age.length - 2)

	return (
		<box height={1}>
			<TextLine fg={selected ? colors.selectedText : colors.text} bg={selected ? colors.selectedBg : undefined}>
				<span fg={branch.isCurrent ? colors.accent : colors.muted}>{prefix}</span>
				<span fg={selected ? colors.accent : branchColor(branch.name)}>{fitCell(branch.name, nameWidth)}</span>
				<span fg={colors.muted}>  {fitCell(age, age.length, "right")}</span>
			</TextLine>
		</box>
	)
}

export const BranchListView = ({
	filterQuery,
	filterMode,
}: {
	filterQuery: string
	filterMode: boolean
}) => {
	const { width, height } = useTerminalDimensions()
	const contentWidth = Math.max(20, width - 2)
	const result = useAtomValue(branchesAtom)
	const selectedIndex = useAtomValue(branchSelectedIndexAtom)
	const listScrollRef = useRef<ScrollBoxRenderable>(null)

	const branches = useMemo(() => {
		const data = AsyncResult.isSuccess(result) ? result.value : []
		if (filterQuery.length === 0) return data
		const lower = filterQuery.toLowerCase()
		return data.filter((b) => b.name.toLowerCase().includes(lower))
	}, [result, filterQuery])

	const localBranches = useMemo(() => branches.filter((b) => !b.isRemote), [branches])
	const remoteBranches = useMemo(() => branches.filter((b) => b.isRemote), [branches])
	const allBranches = useMemo(() => [...localBranches, ...remoteBranches], [localBranches, remoteBranches])

	const safeIndex = allBranches.length > 0 ? Math.max(0, Math.min(selectedIndex, allBranches.length - 1)) : 0

	const isLoading = AsyncResult.isWaiting(result)

	const scrollRow = useMemo(() => {
		const localGroupRows = localBranches.length > 0 ? 1 + localBranches.length : 0
		if (safeIndex < localBranches.length) return (localBranches.length > 0 ? 1 : 0) + safeIndex
		return localGroupRows + (remoteBranches.length > 0 ? 1 : 0) + (safeIndex - localBranches.length)
	}, [safeIndex, localBranches.length, remoteBranches.length])

	useEffect(() => {
		const sb = listScrollRef.current
		if (!sb || allBranches.length === 0) return
		const viewportHeight = sb.viewport.height
		if (viewportHeight <= 0) return
		if (scrollRow < sb.scrollTop) {
			sb.scrollTo({ x: 0, y: scrollRow })
		} else if (scrollRow >= sb.scrollTop + viewportHeight) {
			sb.scrollTo({ x: 0, y: scrollRow - viewportHeight + 1 })
		}
	}, [scrollRow, allBranches.length])

	return (
		<box flexDirection="column" height={height - 4}>
			<SectionTitle title="BRANCHES" />
			{filterMode || filterQuery.length > 0 ? (
				<TextLine>
					<span fg={colors.count}>/</span>
					<span fg={colors.muted}> </span>
					<span fg={filterMode ? colors.text : colors.count}>{filterQuery.length > 0 ? filterQuery : "type to filter..."}</span>
				</TextLine>
			) : null}
			{isLoading && allBranches.length === 0 ? <PlainLine text="- Loading branches..." fg={colors.muted} /> : null}
			{AsyncResult.isFailure(result) ? <PlainLine text="- Could not load branches." fg={colors.error} /> : null}
			{!isLoading && allBranches.length === 0 && AsyncResult.isSuccess(result) ? (
				<PlainLine text={filterQuery.length > 0 ? "- No matching branches." : "- No branches found."} fg={colors.muted} />
			) : null}
			<scrollbox ref={listScrollRef} scrollY scrollX={false} flexGrow={1}>
				{localBranches.length > 0 ? (
					<box flexDirection="column">
						<TextLine>
							<span fg={colors.accent}>{GROUP_ICON} </span>
							<span fg={colors.accent} attributes={TextAttributes.BOLD}>local</span>
						</TextLine>
						{localBranches.map((branch, index) => (
							<BranchRow
								key={branch.name}
								branch={branch}
								selected={index === safeIndex}
								contentWidth={contentWidth}
							/>
						))}
					</box>
				) : null}
				{remoteBranches.length > 0 ? (
					<box flexDirection="column">
						<TextLine>
							<span fg={colors.muted}>{GROUP_ICON} </span>
							<span fg={colors.muted} attributes={TextAttributes.BOLD}>remote</span>
						</TextLine>
						{remoteBranches.map((branch, index) => (
							<BranchRow
								key={`remote-${branch.name}`}
								branch={branch}
								selected={localBranches.length + index === safeIndex}
								contentWidth={contentWidth}
							/>
						))}
					</box>
				) : null}
			</scrollbox>
		</box>
	)
}
