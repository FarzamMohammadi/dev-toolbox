import { Context, Effect, Layer, Schema } from "effect"

interface CommandResult {
	readonly stdout: string
	readonly stderr: string
	readonly exitCode: number
}

export class CommandError extends Schema.TaggedErrorClass<CommandError>()("CommandError", {
	command: Schema.String,
	args: Schema.Array(Schema.String),
	detail: Schema.String,
	cause: Schema.Defect,
}) {}

const readStream = async (stream: ReadableStream | null | undefined) => {
	if (!stream) return ""
	return Bun.readableStreamToText(stream)
}

export class CommandRunner extends Context.Service<CommandRunner, {
	readonly run: (command: string, args: readonly string[]) => Effect.Effect<CommandResult, CommandError>
}>()("git-history/CommandRunner") {
	static readonly layer = Layer.effect(
		CommandRunner,
		Effect.gen(function*() {
			const runProcess = Effect.fn("CommandRunner.runProcess")((command: string, args: readonly string[]) =>
				Effect.tryPromise({
					async try() {
						const proc = Bun.spawn({
							cmd: [command, ...args],
							stdout: "pipe",
							stderr: "pipe",
						})

						const [exitCode, stdout, stderr] = await Promise.all([proc.exited, readStream(proc.stdout), readStream(proc.stderr)])
						return { stdout, stderr, exitCode }
					},
					catch: (cause) => new CommandError({ command, args: [...args], detail: `Failed to run ${command}`, cause }),
				})
			)

			const run = Effect.fn("CommandRunner.run")(function*(command: string, args: readonly string[]) {
				const result = yield* runProcess(command, args).pipe(Effect.withSpan("git-history.command.runProcess", {
					attributes: {
						"process.command": command,
						"process.argv.count": args.length,
					},
				}))
				if (result.exitCode !== 0) {
					const detail = result.stderr.trim() || result.stdout.trim() || `exit code ${result.exitCode}`
					return yield* new CommandError({ command, args: [...args], detail, cause: detail })
				}
				return result
			})

			return CommandRunner.of({ run })
		}),
	)
}
