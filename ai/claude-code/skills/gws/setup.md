# Setup: Google Workspace CLI (gws)

Install and authenticate the `gws` CLI so the `/gws` skill can run.

## Prerequisites

### gcloud CLI (required for `gws auth setup`)

`gws auth setup` shells out to `gcloud`. Install it first:

```bash
brew install --cask google-cloud-sdk
gcloud --version   # verify
```

### Homebrew PATH (macOS)

Homebrew's `/opt/homebrew/bin` must come before `/usr/bin` in `$PATH`. If it doesn't, `brew shellenv` is probably missing from your shell config. Add this **at the top** of `~/.zshrc` (before NVM or other PATH changes):

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Then reload: `source ~/.zshrc`.

## Install

Pick one:

```bash
brew install googleworkspace-cli       # macOS, recommended
npm install -g @googleworkspace/cli    # cross-platform
```

**Important:** There is a separate Homebrew formula called `gws` (a git workspace manager) that also installs a `gws` binary. Do **not** install that one — it will conflict. The correct formula is `googleworkspace-cli`.

Verify:

```bash
gws --version
# Expected: "gws 0.x.x" + "This is not an officially supported Google product."
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
| `gws` runs but shows `Not in a workspace` | You installed the wrong formula (`gws` instead of `googleworkspace-cli`). Run `brew uninstall gws && brew install googleworkspace-cli`. |
| `declare: -A: invalid option` | `gws` (the wrong formula) is running under macOS's Bash 3.2. Uninstall it and install `googleworkspace-cli` instead. |
| `gcloud CLI not found` during `gws auth setup` | Install gcloud first: `brew install --cask google-cloud-sdk`. |
| `conflicting formulae are installed` (brew) | `gws` and `googleworkspace-cli` both install a `gws` binary. Unlink or uninstall the one you don't need: `brew unlink gws` or `brew uninstall gws`. |
| `unauthenticated` / `401` | Run `gws auth login` again. Tokens may have expired. |
| `403 insufficient scope` | Re-run `gws auth login` and accept all requested scopes in the browser. |
| `API has not been enabled` | Run `gws auth setup` again. Enables Drive/Docs/Sheets/Gmail APIs on your Cloud project. |
| `quota exceeded` | Wait, or check your Cloud project's quota in Google Cloud Console. |
| `zsh: event not found` near `!` in a range | Quote the range with double quotes: `--range "Sheet1!A1"`. |

## After Setup

Return to [skill.md](skill.md) and re-run the pre-flight check. Once `gws auth whoami` returns your email, all sub-skills are ready.
