export const formatRelativeDate = (date: Date): string => {
	const days = Math.max(0, Math.floor((Date.now() - date.getTime()) / (24 * 60 * 60 * 1000)))
	if (days === 0) return "today"
	if (days === 1) return "yesterday"
	if (days < 7) return `${days} days ago`
	if (days < 14) return "last week"
	if (days < 30) return `${Math.floor(days / 7)} weeks ago`
	if (days < 60) return "last month"
	return `${Math.floor(days / 30)} months ago`
}
