# Directory Tree Printer

Generates a visual tree of your directory structure that respects .gitignore rules. Output is displayed in terminal and saved to a text file.

## Quick Start

```bash
# Make executable
chmod +x print-directory-tree.sh

# Run
./print-directory-tree.sh [directory]  # Specific directory
./print-directory-tree.sh              # Current directory
./print-directory-tree.sh --no-ignore  # Show all files
```

## Requirements
- Bash (use Git Bash on Windows)

Output is automatically saved to `directory_tree_[timestamp].txt`