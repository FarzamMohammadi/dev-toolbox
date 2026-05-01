import { TextAttributes } from "@opentui/core"
import { colors, themeDefinitions, type ThemeId } from "./colors.js"
import { Divider, fitCell, ModalFrame, PlainLine, TextLine } from "./primitives.js"

export interface ThemeModalState {
	readonly open: boolean
	readonly selectedIndex: number
	readonly initialThemeId: ThemeId
}

export const initialThemeModalState: ThemeModalState = {
	open: false,
	selectedIndex: 0,
	initialThemeId: "git-history",
}

export const ThemeModal = ({
	state,
	activeThemeId,
	modalWidth,
	modalHeight,
	offsetLeft,
	offsetTop,
}: {
	state: ThemeModalState
	activeThemeId: ThemeId
	modalWidth: number
	modalHeight: number
	offsetLeft: number
	offsetTop: number
}) => {
	const innerWidth = Math.max(16, modalWidth - 2)
	const contentWidth = Math.max(14, innerWidth - 2)
	const rowWidth = innerWidth
	const maxVisible = Math.max(1, modalHeight - 7)
	const selectedIndex = Math.max(0, Math.min(state.selectedIndex, themeDefinitions.length - 1))
	const selectedTheme = themeDefinitions[selectedIndex]!
	const scrollStart = Math.min(
		Math.max(0, themeDefinitions.length - maxVisible),
		Math.max(0, selectedIndex - maxVisible + 1),
	)
	const visibleThemes = themeDefinitions.slice(scrollStart, scrollStart + maxVisible)
	const countText = `${selectedIndex + 1}/${themeDefinitions.length}`
	const title = "Themes"
	const headerGap = Math.max(1, contentWidth - title.length - countText.length)

	return (
		<ModalFrame left={offsetLeft} top={offsetTop} width={modalWidth} height={modalHeight} junctionRows={[2, modalHeight - 4]}>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.accent} attributes={TextAttributes.BOLD}>{title}</span>
					<span fg={colors.muted}>{" ".repeat(headerGap)}</span>
					<span fg={colors.muted}>{countText}</span>
				</TextLine>
			</box>
			<box height={1} paddingLeft={1} paddingRight={1}>
				<PlainLine text={fitCell(selectedTheme.description, contentWidth)} fg={colors.muted} />
			</box>
			<Divider width={innerWidth} />
			<box height={maxVisible} flexDirection="column">
				{visibleThemes.map((theme, index) => {
					const actualIndex = scrollStart + index
					const isSelected = actualIndex === selectedIndex
					const isActive = theme.id === activeThemeId
					const marker = isActive ? "✓" : " "
					const swatchWidth = 6
					const nameWidth = Math.max(1, rowWidth - swatchWidth - 3)

					return (
						<TextLine key={theme.id} bg={isSelected ? colors.selectedBg : undefined} fg={isSelected ? colors.selectedText : colors.text}>
							<span fg={isActive ? colors.status.passing : colors.muted}>{marker}</span>
							<span> </span>
							<span>{fitCell(theme.name, nameWidth)}</span>
							<span bg={theme.colors.background}> </span>
							<span bg={theme.colors.panel}> </span>
							<span bg={theme.colors.accent}> </span>
							<span bg={theme.colors.status.passing}> </span>
							<span bg={theme.colors.status.failing}> </span>
							<span bg={theme.colors.status.review}> </span>
						</TextLine>
					)
				})}
			</box>
			<Divider width={innerWidth} />
			<box height={1} paddingLeft={1} paddingRight={1}>
				<TextLine>
					<span fg={colors.count}>↑↓</span>
					<span fg={colors.muted}> preview  </span>
					<span fg={colors.count}>enter</span>
					<span fg={colors.muted}> select  </span>
					<span fg={colors.count}>esc</span>
					<span fg={colors.muted}> cancel</span>
				</TextLine>
			</box>
		</ModalFrame>
	)
}
