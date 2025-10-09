# Spreadsheet Diff

Compare CSV and Excel files with field-level difference reporting. Handles 10M rows.

**Default hardware assumption:** 24GB+ RAM, 8+ cores (configurable via `--hardware`)

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
| `--hardware` | | Hardware profile: `high-end`, `standard`, `low-tier` | `high-end` |

## Examples

### Basic Comparison
```bash
python compare.py source.xlsx comparison.xlsx --key EmployeeID
```

### Large Files (10M rows)
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

## Hardware Profiles

| Profile | RAM | Cores | Performance (15k rows) |
|---------|-----|-------|------------------------|
| **high-end** (default) | 24GB+ | 8+ | <1s |
| **standard** | 8-16GB | 4-8 | 1-2s |
| **low-tier** | 4-8GB | 2-4 | 3-5s |

Use `--hardware` flag to select profile (defaults to high-end).

## Performance

Performance with **high-end** profile (24GB+ RAM, 8+ cores):

| Rows | Time | Memory | Notes |
|------|------|--------|-------|
| 15k | <1s | 50 MB | Vectorized comparison |
| 100k | 2-3s | 200 MB | Vectorized comparison |
| 500k | ~10s | 800 MB | Chunked processing |
| 5M | 1-2 min | 3 GB | Parallel chunked processing |
| 10M | 8-12 min | 6 GB | Parallel chunked processing |

Performance scales with hardware profile. Use `--hardware standard` or `--hardware low-tier` for systems with less RAM.

**Optimization Tips:**
- The tool automatically selects vectorized comparison for small files (faster than chunking)
- Use CSV format instead of Excel for faster processing and lower memory usage
- Use `--no-html` flag to skip HTML report generation when dealing with large difference sets
- Manually adjust `--chunk-size` only if needed (tool auto-configures based on hardware profile)

## FAQ

**Files larger than 10M rows?**
Yes, the chunked architecture supports files of any size.

**Different columns between files?**
The tool compares only columns that exist in both files and displays warnings about columns present in only one file.

**Multiple Excel sheets?**
No. The tool reads only the first sheet. Export additional sheets to CSV format for multi-sheet comparison.

**Null/empty values?**
The tool treats `""`, `NULL`, `None`, `N/A`, and `nan` as equivalent empty values.

**Exit codes?**
The tool exits with code 0 for success, 1 for failure, and 130 when cancelled by user.

**Exclude columns that always differ?**
Use `--exclude "Column1,Column2"` to skip volatile columns (timestamps, GUIDs, audit fields) from comparison.
