#!/usr/bin/env bun

import { createCliRenderer } from "@opentui/core"
import { RegistryProvider } from "@effect/atom-react"
import { createRoot } from "@opentui/react"
import { App } from "./App.js"

process.env.OTUI_USE_ALTERNATE_SCREEN = "true"

const FOCUS_REPORTING_ENABLE = "\x1b[?1004h"
const FOCUS_REPORTING_DISABLE = "\x1b[?1004l"

const renderer = await createCliRenderer({
	exitOnCtrlC: false,
	screenMode: "alternate-screen",
	externalOutputMode: "passthrough",
	onDestroy: () => {
		process.stdout.write(FOCUS_REPORTING_DISABLE)
		process.exit(0)
	},
})

process.stdout.write(FOCUS_REPORTING_ENABLE)

createRoot(renderer).render(
	<RegistryProvider>
		<App />
	</RegistryProvider>,
)
