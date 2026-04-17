# Google Drive Operations

Upload files, share with specific accounts, generate shareable links, and find files via `gws drive`. All write operations require explicit user confirmation.

## Upload a File

```bash
gws drive +upload /path/to/file.pdf --format json
```

Auto-detects MIME type. Returns `{"id":"...","name":"...","webViewLink":"..."}`.

### Optional flags

| Flag | Description |
|------|-------------|
| `--name "..."` | Override the uploaded filename |
| `--parent <FOLDER_ID>` | Upload into a specific folder |
| `--convert` | Convert importable formats (.md, .docx, .csv, .xlsx) to native Google formats (Docs/Sheets) |

### Examples

```bash
# Upload md as a native Google Doc
gws drive +upload notes.md --name "Meeting Notes" --convert

# Upload csv as a native Google Sheet
gws drive +upload data.csv --name "Q1 Data" --convert

# Upload to a specific folder
gws drive +upload report.pdf --parent <FOLDER_ID>
```

## Share with a Specific Email

```bash
gws drive permissions create --file-id <FILE_ID> --json '{
  "type": "user",
  "role": "writer",
  "emailAddress": "alice@example.com"
}' --params '{"sendNotificationEmail":true}'
```

### Roles

| Role | Permission |
|------|------------|
| `reader` | View only |
| `commenter` | View + comment |
| `writer` | Edit |
| `owner` | Transfer ownership (sender loses ownership) |

Use `"sendNotificationEmail":false` in `--params` to share silently.

## Make Link-Shareable (anyone with link)

```bash
gws drive permissions create --file-id <FILE_ID> --json '{
  "type": "anyone",
  "role": "reader"
}'
```

After this, the `webViewLink` from the upload step is shareable with anyone.

## Get a File's Shareable URL

```bash
gws drive files get --file-id <FILE_ID> --params '{"fields":"id,name,webViewLink,mimeType"}' --format json
```

URL patterns by file type (when you only have the ID):

| Type | URL |
|------|-----|
| Doc | `https://docs.google.com/document/d/<ID>/edit` |
| Sheet | `https://docs.google.com/spreadsheets/d/<ID>/edit` |
| Slides | `https://docs.google.com/presentation/d/<ID>/edit` |
| Other (PDF, image, etc.) | `https://drive.google.com/file/d/<ID>/view` |

## List / Search Files

```bash
gws drive files list --params '{"q":"name contains '\''report'\''","pageSize":10,"fields":"files(id,name,mimeType,modifiedTime)"}' --format json
```

The `q` parameter uses Drive search syntax: `mimeType='application/vnd.google-apps.document'`, `'<FOLDER_ID>' in parents`, `modifiedTime > '2026-01-01T00:00:00'`, etc.

## Get File ID from a URL

| URL pattern | ID location |
|-------------|-------------|
| `.../document/d/<ID>/edit` | After `/d/` |
| `.../spreadsheets/d/<ID>/edit` | After `/d/` |
| `.../file/d/<ID>/view` | After `/d/` |
| `.../open?id=<ID>` | Query param `id` |

## Delete (use with caution)

```bash
gws drive files delete --file-id <FILE_ID>
```

Always confirm with the user before delete. This trashes the file (recoverable for 30 days); a follow-up `files emptyTrash` permanently deletes.

## Output

After upload, return the `webViewLink`. After share, confirm recipient + role. After list, present a short table (name, type, modified, link).
