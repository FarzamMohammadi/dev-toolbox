# Excel to JSON Converter

Convert Excel (.xlsx) files to JSON format using column headers as field names.

## Setup

```bash
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

## Usage

```bash
# Single file
python main.py data.xlsx

# Multiple files
python main.py file1.xlsx file2.xlsx file3.xlsx

# With output directory
python main.py --output-dir ./json_output data.xlsx

# Specific sheet
python main.py --sheet "Sheet1" data.xlsx
```

## Parameters

| Parameter | Short | Description | Values/Type |
|-----------|-------|-------------|-------------|
| `--output-dir` | `-o` | Directory for output JSON files | Path (e.g., `./output`) |
| `--sheet` | `-s` | Specific sheet to convert | Sheet name (string) or index (integer) |
| `--indent` | `-i` | JSON indentation spaces | Integer (default: 2) |
| `--compact` | `-c` | Output minified JSON (no indentation) | Flag (no value needed) |

**Note:** The `-c` flag doesn't take a value. It's enabled by its presence.

## Examples

```bash
# Basic conversion
python main.py data.xlsx

# Custom output directory and minified JSON
python main.py --output-dir ./json_output --compact data.xlsx

# Convert specific sheet with custom indentation
python main.py --sheet "Sheet1" --indent 4 data.xlsx

# Multiple files with options
python main.py -o ./output -c file1.xlsx file2.xlsx file3.xlsx
```