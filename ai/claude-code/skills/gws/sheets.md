# Google Sheets Operations

Create, append rows, and read ranges via `gws sheets`. All write operations require explicit user confirmation.

Note: zsh expands `!` in unquoted strings. Always wrap ranges in double quotes: `--range "Sheet1!A1"`.

## Create a Spreadsheet

```bash
gws sheets spreadsheets create --json '{"properties":{"title":"Q1 Budget"}}' --format json
```

Returns `{"spreadsheetId":"...","spreadsheetUrl":"..."}`. The URL is `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit`.

## Append a Single Row

```bash
gws sheets +append --spreadsheet <SHEET_ID> --values "alice,42,active"
```

Comma-separated values land in the next empty row of the first sheet.

## Append Multiple Rows

```bash
gws sheets +append --spreadsheet <SHEET_ID> --json-values '[["alice",42,"active"],["bob",17,"pending"]]'
```

Each inner array is one row.

## Append to a Specific Tab

```bash
gws sheets +append --spreadsheet <SHEET_ID> --range "Sheet2!A1" --values "x,y,z"
```

## Read a Range

```bash
gws sheets spreadsheets values get --spreadsheet <SHEET_ID> --range "Sheet1!A1:C10" --format json
```

Extract just the values:

```bash
gws sheets spreadsheets values get --spreadsheet <SHEET_ID> --range "Sheet1!A1:C10" --format json | jq '.values'
```

## Update a Range (overwrite)

```bash
gws sheets spreadsheets values update --spreadsheet <SHEET_ID> --range "Sheet1!A1" --params '{"valueInputOption":"USER_ENTERED"}' --json '{"values":[["new","data","here"]]}'
```

`USER_ENTERED` parses formulas and dates. Use `RAW` to insert literal strings.

## Add a New Tab

```bash
gws sheets spreadsheets batchUpdate --spreadsheet <SHEET_ID> --json '{"requests":[{"addSheet":{"properties":{"title":"NewTab"}}}]}'
```

## Share

To share the sheet with a specific account, see [drive.md](drive.md) → "Share with a Specific Email" (Sheets are Drive files).

## Output

After create, return the spreadsheet URL. After append/update, confirm row count and target range.
