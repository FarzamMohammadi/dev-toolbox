const hashColor = (name: string) => {
	let hash = 0
	for (const char of name) {
		hash = (hash * 31 + char.charCodeAt(0)) >>> 0
	}
	const palette = [
		"#60a5fa", "#34d399", "#f472b6", "#f59e0b", "#93c5fd",
		"#a78bfa", "#fb923c", "#4ade80", "#f87171", "#38bdf8",
	]
	return palette[hash % palette.length]!
}

export const branchColor = (name: string) => hashColor(name)
