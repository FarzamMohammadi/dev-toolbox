# Google Docs Operations

Create, read, append, and convert markdown to formatted Docs via `gws docs` and `gws drive`. All write operations require explicit user confirmation.

## Create a Blank Doc

```bash
gws docs documents create --json '{"title":"My Doc"}' --format json
```

Returns `{"documentId":"...","title":"..."}`. The Doc URL is `https://docs.google.com/document/d/<DOC_ID>/edit`.

## Append Plain Text

```bash
gws docs +write --document <DOC_ID> --text 'Hello world.'
```

Inserts at the end of the body. Plain text only, no formatting.

## Markdown → Formatted Doc (recommended path)

Use Drive's auto-conversion for headings, bold, italic, lists, links, and code blocks. This is the default path for the user's "store this md as a google doc with proper formatting" workflow.

```bash
# Write the markdown to a temp file, then upload with --convert
TMP=$(mktemp -t google-doc.XXXXXX.md)
cat > "$TMP" <<'EOF'
# My Title

Some **bold** text and a [link](https://example.com).

- bullet one
- bullet two
EOF

gws drive +upload "$TMP" --name "My Doc Title" --convert --format json
rm "$TMP"
```

`--convert` tells Drive to import the `.md` as a native Google Doc (not store it as a raw markdown file). The response includes the `id` (Doc ID) and `webViewLink` (shareable URL).

To share the resulting Doc with a specific account, see [drive.md](drive.md) → "Share with a Specific Email".

## Markdown → Formatted Doc (advanced, fine control)

When you need exact control over styles (custom fonts, indentation, colored text), use `documents batchUpdate` with `insertText` + `updateTextStyle` + `updateParagraphStyle` requests:

```bash
gws docs documents batchUpdate --document <DOC_ID> --json '{
  "requests": [
    {"insertText": {"location": {"index": 1}, "text": "My Heading\n"}},
    {"updateParagraphStyle": {
      "range": {"startIndex": 1, "endIndex": 11},
      "paragraphStyle": {"namedStyleType": "HEADING_1"},
      "fields": "namedStyleType"
    }}
  ]
}'
```

For a markdown document, build the `requests` array programmatically. Quick Python sketch:

```python
import json, sys, re
text = sys.stdin.read()
requests = []
idx = 1
for line in text.splitlines(keepends=True):
    m = re.match(r'^(#{1,6}) (.*)', line)
    style = f"HEADING_{len(m.group(1))}" if m else "NORMAL_TEXT"
    content = (m.group(2) + "\n") if m else line
    requests.append({"insertText": {"location": {"index": idx}, "text": content}})
    end = idx + len(content)
    if m:
        requests.append({"updateParagraphStyle": {
            "range": {"startIndex": idx, "endIndex": end},
            "paragraphStyle": {"namedStyleType": style},
            "fields": "namedStyleType"
        }})
    idx = end
print(json.dumps({"requests": requests}))
```

Pipe its output into `--json @-` (or write to a file and pass the path). For most cases the `--convert` upload path above is simpler and produces a clean result.

## Read Doc Contents

```bash
gws docs documents get --document <DOC_ID> --format json
```

The body content is under `.body.content[]`. To extract plain text:

```bash
gws docs documents get --document <DOC_ID> --format json | jq -r '.body.content[] | .paragraph?.elements[]?.textRun?.content // empty'
```

## Output

After create/upload, return the Doc URL: `https://docs.google.com/document/d/<DOC_ID>/edit`. After share (via drive.md), confirm who was added and at what role.
