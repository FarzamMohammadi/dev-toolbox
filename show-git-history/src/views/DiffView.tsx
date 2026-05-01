import type { ScrollBoxRenderable } from "@opentui/core"
import { useMemo, type Ref } from "react"
import type { DiffMode } from "../domain.js"
import { colors, type ThemeId } from "../ui/colors.js"
import { createDiffSyntaxStyle, patchRenderableLineCount, type DiffState } from "../ui/diff.js"
import { LoadingPane, StatusCard } from "../ui/DetailsPane.js"
import { Divider, fitCell, PlainLine, TextLine } from "../ui/primitives.js"

export const DiffView = ({
	diffState,
	fileIndex,
	view,
	wrapMode,
	paneWidth,
	height,
	loadingIndicator,
	scrollRef,
	themeId,
	title,
	diffMode,
}: {
	diffState: DiffState | undefined
	fileIndex: number
	view: "unified" | "split"
	wrapMode: "none" | "word"
	paneWidth: number
	height: number
	loadingIndicator: string
	scrollRef: Ref<ScrollBoxRenderable>
	themeId: ThemeId
	title: string
	diffMode?: DiffMode
}) => {
	const readyFiles = diffState?.status === "ready" ? diffState.files : []
	const safeIndex = readyFiles.length > 0 ? Math.max(0, Math.min(fileIndex, readyFiles.length - 1)) : 0
	const file = readyFiles[safeIndex] ?? null
	const diffHeight = useMemo(
		() => file ? patchRenderableLineCount(file.patch, view, wrapMode, paneWidth) : 1,
		[file?.patch, view, wrapMode, paneWidth],
	)
	const syntaxStyle = useMemo(() => createDiffSyntaxStyle(), [themeId])

	const headerWidth = Math.max(24, paneWidth - 2)
	const modeLabel = diffMode === "file-scoped" ? "file only" : diffMode === "full-commit" ? "full commit" : ""

	if (!diffState || diffState.status === "loading") {
		return (
			<box height={height} flexDirection="column">
				<box height={1} paddingLeft={1} paddingRight={1}>
					<TextLine>
						<span fg={colors.count}>{title}</span>
					</TextLine>
				</box>
				<Divider width={paneWidth} />
				<LoadingPane content={{ title: `${loadingIndicator} Loading diff`, hint: "Fetching patch" }} width={paneWidth} height={Math.max(1, height - 2)} />
			</box>
		)
	}

	if (diffState.status === "error") {
		return (
			<box height={height} flexDirection="column">
				<box height={1} paddingLeft={1} paddingRight={1}>
					<PlainLine text={`${title} diff`} fg={colors.count} bold />
				</box>
				<Divider width={paneWidth} />
				<StatusCard content={{ title: "Could not load diff", hint: diffState.error }} width={paneWidth} />
			</box>
		)
	}

	if (readyFiles.length === 0 || !file) {
		return <LoadingPane content={{ title: "No diff", hint: "This commit has no patch contents" }} width={paneWidth} height={height} />
	}

	const fileCounter = `${safeIndex + 1}/${readyFiles.length}`
	const fileNameWidth = Math.max(8, headerWidth - fileCounter.length - modeLabel.length - 4)

	return (
		<box height={height} flexDirection="column">
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.count}>{title}</span>
					{modeLabel.length > 0 ? (
						<>
							<span fg={colors.muted}>{"  ".padEnd(Math.max(2, headerWidth - title.length - modeLabel.length))}</span>
							<span fg={colors.accent}>{modeLabel}</span>
						</>
					) : null}
				</TextLine>
			</box>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.text}>{fitCell(file.name, fileNameWidth)}</span>
					<span fg={colors.muted}>  {fileCounter}</span>
				</TextLine>
			</box>
			<Divider width={paneWidth} />
			<scrollbox ref={scrollRef} focused flexGrow={1} scrollY scrollX={false}>
				<diff
					key={`${title}-${safeIndex}-${view}-${wrapMode}-${diffMode ?? ""}`}
					diff={file.patch}
					view={view}
					syncScroll
					filetype={file.filetype ?? "text"}
					syntaxStyle={syntaxStyle}
					showLineNumbers
					wrapMode={wrapMode}
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
