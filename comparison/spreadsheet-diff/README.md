# Spreadsheet Diff

Compare CSV and Excel files with field-level difference reporting. Handles 10M+ rows efficiently.

## Setup

```bash
python -m venv venv

# Activate
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install
pip install -r requirements.txt
```

## Usage

```bash
# Basic
python compare.py source.csv comparison.csv

# With key column
python compare.py data1.xlsx data2.xlsx --key CustomerID

# Custom output
python compare.py file1.csv file2.csv --output-dir ./results
```

## Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--key` | `-k` | Key column(s) for row matching (comma-separated for composite) | Auto-detect |
| `--sort-by` | | Sort columns for duplicate key matching (comma-separated) | None |
| `--exclude` | | Columns to exclude from comparison (comma-separated) | None |
| `--output-dir` | `-o` | Output directory | `results` |
| `--format` | `-f` | Output format: `csv`, `excel`, `both` | `excel` |
| `--chunk-size` | `-c` | Rows per chunk | `100000` |
| `--no-html` | | Skip HTML report | False |
| `--case-insensitive` | | Case-insensitive comparison | False |
| `--ignore-whitespace` | | Ignore whitespace | False |
| `--log-level` | | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

## Examples

### Basic Comparison
```bash
python compare.py source.xlsx comparison.xlsx --key EmployeeID
```

### Large Files (10M+ rows)
```bash
python compare.py large1.csv large2.csv \
  --key ID \
  --chunk-size 50000 \
  --format csv \
  --no-html
```

### Composite Keys
```bash
# Multiple columns as key
python compare.py sales1.xlsx sales2.xlsx \
  --key "CustomerID,Date"
```

### Duplicate Keys
```bash
# Sort duplicates before matching
python compare.py transactions.csv transactions2.csv \
  --key CustomerID \
  --sort-by "Date,Time"

# Position-based matching (no sorting)
python compare.py logs1.csv logs2.csv --key SessionID
```

### Case-Insensitive
```bash
python compare.py file1.csv file2.csv \
  --case-insensitive \
  --ignore-whitespace
```

### All Output Formats
```bash
python compare.py data1.csv data2.csv \
  --key OrderID \
  --format both \
  --output-dir ./reports
```

### Exclude Columns
```bash
# Exclude timestamp and audit columns
python compare.py data1.csv data2.csv \
  --key ID \
  --exclude "LastModified,UpdatedAt,CreatedBy"

# Exclude generated IDs
python compare.py file1.xlsx file2.xlsx \
  --key CustomerID \
  --exclude "RecordGUID,SessionID,Version"
```

## Output Files

Generated in output directory (default: `results/`):

1. **CSV** - `differences_YYYYMMDD_HHMMSS.csv`
   - No row limit
   - Best for large diff sets

2. **Excel** - `differences_YYYYMMDD_HHMMSS.xlsx`
   - Color-coded (red = source, green = comparison)
   - Limit: 1,048,576 rows

3. **HTML** - `differences_report_YYYYMMDD_HHMMSS.html`
   - Interactive table with search/sort
   - Best for <50k differences

### Output Columns

| Column | Description |
|--------|-------------|
| `<key_column>` | Key value |
| `field` | Field name that differs |
| `source_value` | Value in source file |
| `comparison_value` | Value in comparison file |
| `type` | `modified`, `added`, `removed` |

## Key Column Detection

When `--key` not specified:
1. Auto-detect (looks for `id`, `key`, `pk`, `_id`, etc.)
2. Validate uniqueness
3. Falls back to **first column**

**Best practice:** Always specify `--key` for predictable results.

## Duplicate Key Behavior

When same key appears multiple times:
- **With `--sort-by`**: Sorts rows by specified columns before matching
- **Without `--sort-by`**: Matches by position (1st → 1st, 2nd → 2nd)
- **Different counts**: Extra rows marked as "only in source" or "only in comparison"

## Supported Formats

### CSV
- Extensions: `.csv`, `.txt`, `.tsv`
- Auto-detects delimiter
- No row limit

### Excel
- Extensions: `.xlsx`, `.xls`, `.xlsm`, `.xlsb`
- Reads first/active sheet only
- Limit: 1,048,576 rows

## Requirements

- Python 3.8+
- polars (1.19.0)
- openpyxl (3.1.5)
- click (8.1.8)
- rich (13.9.4)
- xxhash (3.5.0)
- pydantic (2.10.4)

## Performance

Typical on modern hardware:

| Rows | Time | Memory |
|------|------|--------|
| 500k | ~15s | 500 MB |
| 5M | 2-3 min | 2 GB |
| 10M | 10-15 min | 4-6 GB |

**Tips:**
- Reduce `--chunk-size` if low memory
- Use CSV format (faster than Excel)
- Use `--no-html` for huge diffs
- Increase chunk size if RAM available

## FAQ

**Files larger than 10M rows?**
Yes, chunked architecture handles any size.

**Different columns?**
Compares common columns, warns about differences.

**Multiple Excel sheets?**
No. Reads first sheet only. Export to CSV for multi-sheet.

**Null/empty values?**
Treats `""`, `NULL`, `None`, `N/A`, `nan` as equivalent.

**Exit codes?**
0 = success, 1 = failure, 130 = cancelled.

**Exclude columns that always differ?**
Use `--exclude "Column1,Column2"` to skip volatile columns (timestamps, GUIDs, audit fields).
