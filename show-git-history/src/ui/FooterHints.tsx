import type { ViewId } from "../domain.js"
import { colors } from "./colors.js"
import { TextLine } from "./primitives.js"

const Hint = ({ shortcut, label }: { shortcut: string; label: string }) => (
	<>
		<span fg={colors.count}>{shortcut}</span>
		<span fg={colors.muted}> {label}  </span>
	</>
)

export const FooterHints = ({
	view,
	filterEditing,
	showFilterClear,
	diffFullView,
	isFileHistory,
	hasSelection,
	isLoading,
	loadingIndicator,
}: {
	view: ViewId
	filterEditing: boolean
	showFilterClear: boolean
	diffFullView: boolean
	isFileHistory: boolean
	hasSelection: boolean
	isLoading: boolean
	loadingIndicator: string
}) => {
	if (filterEditing) {
		return (
			<TextLine>
				<Hint shortcut="search" label="typing" />
				<Hint shortcut="↑↓" label="move" />
				<Hint shortcut="enter" label="apply" />
				<Hint shortcut="esc" label="cancel" />
				<Hint shortcut="ctrl-u" label="clear" />
				<Hint shortcut="ctrl-w" label="word" />
			</TextLine>
		)
	}

	if (diffFullView) {
		return (
			<TextLine>
				<Hint shortcut="esc" label="back" />
				<Hint shortcut="j/k" label="scroll" />
				<Hint shortcut="v" label="view" />
				<Hint shortcut="w" label="wrap" />
				<Hint shortcut="[]" label="files" />
				{isFileHistory ? <Hint shortcut="f" label="scope" /> : null}
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	const loadingHint = isLoading ? (
		<>
			<span fg={colors.status.pending}>{loadingIndicator}</span>
			<span fg={colors.muted}> loading  </span>
		</>
	) : null

	if (view === "branches") {
		return (
			<TextLine>
				<Hint shortcut="/" label="filter" />
				<Hint shortcut="T" label="theme" />
				{showFilterClear ? <Hint shortcut="esc" label="clear" /> : null}
				{loadingHint}
				<Hint shortcut="enter" label="commits" />
				<Hint shortcut="r" label="refresh" />
				<Hint shortcut="1" label="branches" />
				<Hint shortcut="2" label="files" />
				<Hint shortcut="3" label="review" />
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	if (view === "commits") {
		return (
			<TextLine>
				<Hint shortcut="/" label="filter" />
				<Hint shortcut="T" label="theme" />
				{showFilterClear ? <Hint shortcut="esc" label="clear" /> : null}
				{loadingHint}
				{hasSelection ? (
					<>
						<Hint shortcut="d" label="diff" />
						<Hint shortcut="y" label="copy" />
					</>
				) : null}
				<Hint shortcut="r" label="refresh" />
				<Hint shortcut="1" label="branches" />
				<Hint shortcut="2" label="files" />
				<Hint shortcut="3" label="review" />
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	if (view === "files") {
		return (
			<TextLine>
				<Hint shortcut="/" label="filter" />
				<Hint shortcut="T" label="theme" />
				{showFilterClear ? <Hint shortcut="esc" label="clear" /> : null}
				{loadingHint}
				<Hint shortcut="enter" label="history" />
				<Hint shortcut="r" label="refresh" />
				<Hint shortcut="1" label="branches" />
				<Hint shortcut="2" label="files" />
				<Hint shortcut="3" label="review" />
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	if (view === "file-history") {
		return (
			<TextLine>
				<Hint shortcut="/" label="filter" />
				<Hint shortcut="T" label="theme" />
				{showFilterClear ? <Hint shortcut="esc" label="clear" /> : null}
				{loadingHint}
				{hasSelection ? (
					<>
						<Hint shortcut="d" label="diff" />
						<Hint shortcut="f" label="scope" />
					</>
				) : null}
				<Hint shortcut="r" label="refresh" />
				<Hint shortcut="esc" label="back" />
				<Hint shortcut="1" label="branches" />
				<Hint shortcut="2" label="files" />
				<Hint shortcut="3" label="review" />
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	if (view === "branch-review") {
		return (
			<TextLine>
				<Hint shortcut="/" label="filter" />
				<Hint shortcut="T" label="theme" />
				{showFilterClear ? <Hint shortcut="esc" label="clear" /> : null}
				{loadingHint}
				{hasSelection ? (
					<Hint shortcut="d" label="diff" />
				) : null}
				<Hint shortcut="r" label="refresh" />
				<Hint shortcut="1" label="branches" />
				<Hint shortcut="2" label="files" />
				<Hint shortcut="3" label="review" />
				<Hint shortcut="q" label="quit" />
			</TextLine>
		)
	}

	return (
		<TextLine>
			<Hint shortcut="q" label="quit" />
		</TextLine>
	)
}
