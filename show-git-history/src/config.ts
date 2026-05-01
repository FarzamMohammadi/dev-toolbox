import { Config, Effect } from "effect"

const positiveIntOr = (fallback: number) => (value: number) => Number.isFinite(value) && value > 0 ? value : fallback

const appConfig = Config.all({
	commitLimit: Config.int("GIT_HISTORY_COMMIT_LIMIT").pipe(
		Config.withDefault(500),
		Config.map(positiveIntOr(500)),
	),
	fileHistoryLimit: Config.int("GIT_HISTORY_FILE_HISTORY_LIMIT").pipe(
		Config.withDefault(200),
		Config.map(positiveIntOr(200)),
	),
})

export const config = Effect.runSync(Effect.gen(function*() {
	return yield* appConfig
}))
