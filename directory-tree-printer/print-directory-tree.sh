#!/usr/bin/env bash

# Cache for .gitignore contents
declare -A IGNORE_PATTERNS

# Function to normalize path for pattern matching
normalize_path() {
    local path="$1"
    # Remove leading ./
    path="${path#./}"
    # Remove leading /
    path="${path#/}"
    echo "$path"
}

# Find nearest .gitignore file
get_ignore_patterns() {
    local dir="$1"
    local current_dir="$(realpath "$dir")"
    
    # Check cache first
    if [ -n "${IGNORE_PATTERNS[$current_dir]:-}" ]; then
        echo "${IGNORE_PATTERNS[$current_dir]}"
        return
    fi
    
    # Find nearest .gitignore
    while [ "$current_dir" != "/" ] && [ "$current_dir" != "." ]; do
        if [ -f "$current_dir/.gitignore" ]; then
            IGNORE_PATTERNS[$current_dir]="$current_dir/.gitignore"
            echo "$current_dir/.gitignore"
            return
        fi
        current_dir="$(dirname "$current_dir")"
    done
    echo ""
}

# Check if path matches ignore patterns
should_ignore() {
    local path="$1"
    local ignore_file="$2"
    
    [ -z "$ignore_file" ] && return 1
    
    local ignore_dir="$(dirname "$ignore_file")"
    local rel_path="$(normalize_path "${path#$ignore_dir/}")"
    
    while IFS= read -r pattern || [ -n "$pattern" ]; do
        # Skip comments and empty lines
        [[ $pattern =~ ^[[:space:]]*# ]] && continue
        [ -z "${pattern//[[:space:]]/}" ] && continue
        
        # Process the pattern
        pattern="$(normalize_path "$pattern")"
        
        # Direct match
        if [ "$pattern" = "$rel_path" ]; then
            return 0
        fi
        
        # Pattern ends with /
        if [[ $pattern == *"/" ]]; then
            pattern="${pattern%/}"
            if [[ $rel_path == $pattern/* ]]; then
                return 0
            fi
        fi
        
        # Pattern starts with /
        if [[ $pattern == "/"* ]]; then
            pattern="${pattern#/}"
            if [[ $rel_path == $pattern* ]]; then
                return 0
            fi
        fi
        
        # General pattern match
        if [[ $rel_path == *"$pattern"* ]]; then
            return 0
        fi
    done < "$ignore_file"
    
    return 1
}

# Print directory tree
print_tree() {
    local prefix="$1"
    local dir="$2"
    
    # Find applicable ignore file
    local ignore_file=$(get_ignore_patterns "$dir")
    
    # Get directory contents
    local files=()
    while IFS= read -r -d '' file; do
        files+=("$(basename "$file")")
    done < <(find "$dir" -maxdepth 1 -mindepth 1 -print0 2>/dev/null | sort -z)
    
    local total=${#files[@]}
    local count=0
    
    for item in "${files[@]}"; do
        local full_path="$dir/$item"
        
        # Skip ignored files
        if should_ignore "$full_path" "$ignore_file"; then
            ((total--))
            continue
        fi
        
        ((count++))
        local isLast=$([[ $count -eq $total ]] && echo "true" || echo "false")
        
        # Tree formatting
        local current_prefix
        if [[ "$isLast" == "true" ]]; then
            current_prefix="└── "
        else
            current_prefix="├── "
        fi
        
        echo "${prefix}${current_prefix}${item}"
        
        # Recurse into directories
        if [ -d "$full_path" ]; then
            local new_prefix
            if [[ "$isLast" == "true" ]]; then
                new_prefix="${prefix}    "
            else
                new_prefix="${prefix}│   "
            fi
            print_tree "$new_prefix" "$full_path"
        fi
    done
}

# Show help
show_help() {
    echo "Usage: $0 [OPTIONS] [directory]"
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --no-ignore    Ignore .gitignore files (show all files)"
    echo ""
    echo "Examples:"
    echo "  $0                     # Current directory"
    echo "  $0 /path/to/project    # Specific directory"
    echo "  $0 --no-ignore .       # Show all files"
    exit 0
}

# Parse arguments
NO_IGNORE=false
DIR="."

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        --no-ignore)
            NO_IGNORE=true
            shift
            ;;
        *)
            DIR="$1"
            shift
            ;;
    esac
done

# Verify directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: Directory '$DIR' does not exist"
    exit 1
fi

# Convert to absolute path
DIR="$(realpath "$DIR")"

# Create output file name with timestamp
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
OUTPUT_FILE="directory_tree_${TIMESTAMP}.txt"

# Redirect output to both file and terminal
{
    echo "Directory Tree Generated on $(date)"
    echo "Root: $DIR"
    echo "----------------------------------------"
    echo "$(basename "$DIR")"
    print_tree "" "$DIR"
} | tee "$OUTPUT_FILE"

echo -e "\nTree output saved to: $OUTPUT_FILE"