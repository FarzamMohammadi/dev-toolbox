# Repository Content Aggregator

Exports repository content into a single text file for LLM ingestion, respecting .gitignore rules.

## Usage

Run the script:
```sh
# Basic usage:
python main.py <repo_path>

# Optional: Set maximum file size in MB
python main.py <repo_path> -m 20
```

## Output
- Creates `<directory_name>_content.txt` in current directory
- Formats content with directory structure and file paths
- Includes repository metadata

## Features
- Full .gitignore support (all Git pattern types)
- Handles nested .gitignore files
- Auto-skips binary and large files
- Preserves directory structure
- Git-like pattern matching