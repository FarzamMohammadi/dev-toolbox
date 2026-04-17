# Gmail Operations

Read, send, draft, and reply to email via `gws gmail`. All write operations require explicit user confirmation before execution.

## Send Email

```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!'
```

### Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--to` | yes | Recipient(s), comma-separated |
| `--subject` | yes | Subject line |
| `--body` | yes | Body (plain text by default) |
| `--cc` | no | CC recipient(s) |
| `--bcc` | no | BCC recipient(s) |
| `--html` | no | Treat `--body` as HTML |
| `--attach` / `-a` | no | Attach a file (repeatable, 25 MB total) |
| `--from` | no | Send-as alias |
| `--draft` | no | Save as draft instead of sending |
| `--dry-run` | no | Print the request without sending |

### Examples

```bash
# Plain text with CC
gws gmail +send --to alice@example.com --subject 'Update' --body 'See below.' --cc bob@example.com

# HTML with formatting
gws gmail +send --to alice@example.com --subject 'Report' --body '<b>Q1</b> results attached.' --html -a q1.pdf

# Multi-line body via heredoc
gws gmail +send --to alice@example.com --subject 'Notes' --body "$(cat <<'EOF'
Hi Alice,

Three updates:
1. ...
2. ...
3. ...

Thanks
EOF
)"

# Save as draft instead of sending
gws gmail +send --to alice@example.com --subject 'Draft' --body 'WIP' --draft
```

## Read Inbox

List recent messages:

```bash
gws gmail messages list --params '{"maxResults":10,"q":"is:unread"}' --format json
```

The `q` parameter accepts Gmail search syntax (`from:`, `subject:`, `has:attachment`, `newer_than:7d`, etc.).

Fetch a specific message:

```bash
gws gmail messages get --id <MESSAGE_ID> --params '{"format":"full"}'
```

## Reply

```bash
gws gmail +reply --id <MESSAGE_ID> --body 'My reply.'
gws gmail +reply-all --id <MESSAGE_ID> --body 'Reply to everyone.'
```

Same flag set as `+send` for body / HTML / attach.

## Forward

```bash
gws gmail +forward --id <MESSAGE_ID> --to alice@example.com --body 'FYI'
```

## Output

After sending, return the message ID and a short confirmation:

```
Sent. Message ID: 18f3a2b... → alice@example.com
```

For drafts, return the draft ID and Gmail draft URL: `https://mail.google.com/mail/u/0/#drafts/<DRAFT_ID>`.
