# Setup: Google Workspace CLI (gws)

Install and authenticate the `gws` CLI so the `/gws` skill can run.

## Install

Pick one:

```bash
brew install googleworkspace-cli       # macOS, recommended
npm install -g @googleworkspace/cli    # cross-platform
```

Verify:

```bash
gws --version
```

## Authenticate (interactive OAuth, recommended)

Two steps, both run once:

```bash
gws auth setup     # creates a Google Cloud project, enables required APIs
gws auth login     # opens browser for OAuth consent
gws auth whoami    # verify
```

`auth setup` is one-time per machine. `auth login` is one-time per Google account; re-run if tokens expire.

## Authenticate (service account, optional)

For non-interactive use (CI, servers):

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

The service account must have domain-wide delegation if accessing other users' data. For personal use, stick with OAuth.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `command not found: gws` | Re-run install. Check `which gws` and `$PATH`. |
| `unauthenticated` / `401` | Run `gws auth login` again. Tokens may have expired. |
| `403 insufficient scope` | Re-run `gws auth login` and accept all requested scopes in the browser. |
| `API has not been enabled` | Run `gws auth setup` again. Enables Drive/Docs/Sheets/Gmail APIs on your Cloud project. |
| `quota exceeded` | Wait, or check your Cloud project's quota in Google Cloud Console. |
| `zsh: event not found` near `!` in a range | Quote the range with double quotes: `--range "Sheet1!A1"`. |

## After Setup

Return to [skill.md](skill.md) and re-run the pre-flight check. Once `gws auth whoami` returns your email, all sub-skills are ready.
