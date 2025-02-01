import os
import fnmatch
from pathlib import Path
from typing import List, Set, Optional, Dict, Tuple
import re
from datetime import datetime
import json

class GitignoreRule:
    """Represents a single gitignore rule with its source and priority."""
    
    def __init__(self, pattern: str, source_dir: Path, line_num: int):
        self.original_pattern = pattern
        self.source_dir = source_dir
        self.line_num = line_num
        self.is_negation = pattern.startswith('!')
        self.pattern = pattern[1:] if self.is_negation else pattern
        self.is_directory = pattern.endswith('/')
        
        if self.is_directory:
            self.pattern = self.pattern[:-1]
            
        self.regex = self._build_regex()
    
    def _build_regex(self) -> re.Pattern:
        """Convert gitignore pattern to regex, handling all Git's pattern rules."""
        pattern = self.pattern
        
        # Handle directory separator normalization
        pattern = pattern.replace('\\', '/')
        
        # Handle leading slash
        if pattern.startswith('/'):
            pattern = pattern[1:]
            anchored = True
        else:
            anchored = False
            
        # Escape special regex characters, but keep wildcards
        pattern = ''.join([
            c if c in ['*', '?', '/'] else re.escape(c)
            for c in pattern
        ])
        
        # Convert gitignore wildcards to regex
        pattern = pattern.replace('**/', '(.*/)?')  # Match zero or more directories
        pattern = pattern.replace('/**', '(/.*)?')  # Match directory and all subdirs
        pattern = pattern.replace('*', '[^/]*')     # Match any char except /
        pattern = pattern.replace('?', '[^/]')      # Match single char except /
        
        # Handle directory-only matches
        if self.is_directory:
            pattern = pattern + '(/.*)?'
            
        # Build final regex with proper anchoring
        if anchored:
            pattern = '^' + pattern
        else:
            pattern = '(^|.*)/' + pattern
            
        pattern = pattern + '(/.*)?$'
        
        return re.compile(pattern)
    
    def matches(self, path: str, is_dir: bool = False) -> bool:
        """Test if this rule matches a given path."""
        # Normalize path separators
        path = path.replace('\\', '/')
        if path.startswith('./'):
            path = path[2:]
            
        # Make path relative to the rule's source directory
        try:
            rel_path = os.path.relpath(path, self.source_dir)
            rel_path = rel_path.replace('\\', '/')
        except ValueError:
            # Path is not relative to source_dir
            return False
            
        return bool(self.regex.match(rel_path))

class GitignoreManager:
    """Manages multiple .gitignore files and their rules."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.rules_cache: Dict[Path, List[GitignoreRule]] = {}
        
        # Add Git's default ignore rules (these are always applied)
        self.default_rules = [
            GitignoreRule('.git/', self.root_path, 0),
            GitignoreRule('.git/**', self.root_path, 0),
            GitignoreRule('.gitmodules', self.root_path, 0),
            GitignoreRule('.gitattributes', self.root_path, 0),
            GitignoreRule('.git-*', self.root_path, 0),
        ]
        
        self._load_all_gitignores()
    
    def _load_all_gitignores(self) -> None:
        """Load all .gitignore files in the repository."""
        # First load global gitignore
        global_gitignore = self.root_path / '.gitignore'
        if global_gitignore.exists():
            self._load_gitignore(global_gitignore)
        
        # Then load all nested gitignores
        for dirpath, _, filenames in os.walk(self.root_path):
            if '.gitignore' in filenames and dirpath != str(self.root_path):
                gitignore_path = Path(dirpath) / '.gitignore'
                self._load_gitignore(gitignore_path)
    
    def _load_gitignore(self, gitignore_path: Path) -> None:
        """Load rules from a single .gitignore file."""
        try:
            rules = []
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        rule = GitignoreRule(
                            line,
                            gitignore_path.parent,
                            line_num
                        )
                        rules.append(rule)
            self.rules_cache[gitignore_path] = rules
        except Exception as e:
            print(f"Warning: Error loading {gitignore_path}: {e}")
    
    def is_ignored(self, path: Path, is_dir: bool = False) -> bool:
        """
        Check if a path should be ignored using all applicable gitignore rules.
        Follows Git's precedence rules exactly.
        """
        path_str = str(path)
        
        # First check default rules (these take precedence)
        for rule in self.default_rules:
            if rule.matches(path_str, is_dir):
                return True
                
        ignored = False
        
        # Get all relevant .gitignore files from root to the path
        try:
            rel_path = path.relative_to(self.root_path)
        except ValueError:
            return False
            
        # Build list of parent directories up to root
        parents = [self.root_path] + [
            self.root_path / p
            for p in rel_path.parent.parts
        ]
        
        # Check rules from root to target directory
        for parent in parents:
            gitignore_path = parent / '.gitignore'
            if gitignore_path in self.rules_cache:
                for rule in self.rules_cache[gitignore_path]:
                    if rule.matches(path_str, is_dir):
                        ignored = not rule.is_negation
        
        return ignored

class RepositoryAggregator:
    """Aggregates repository content while respecting .gitignore rules."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.gitignore_manager = GitignoreManager(self.root_path)
    
    def _should_ignore(self, path: Path) -> bool:
        """Determine if a path should be ignored based on .gitignore rules."""
        return self.gitignore_manager.is_ignored(path, path.is_dir())
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """
        Check if a file is binary by reading its first few KB.
        More accurate than simple extension checking.
        """
        try:
            chunk_size = 8192
            with open(file_path, 'rb') as f:
                chunk = f.read(chunk_size)
                if not chunk:  # Empty file
                    return False
                    
                # Check for common binary file signatures
                if chunk.startswith(b'%PDF-'):  # PDF
                    return True
                if any(chunk.startswith(sig) for sig in [b'PK\x03\x04', b'PK\x05\x06']):  # ZIP
                    return True
                if chunk.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                    return True
                    
                # Check for null bytes and high concentration of non-ASCII
                text_characters = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
                null_count = chunk.count(b'\x00')
                non_text = len([b for b in chunk if b not in text_characters])
                
                # If more than 30% non-text or contains nulls, probably binary
                return (null_count > 0) or (non_text / len(chunk) > 0.3)
                
        except (IOError, OSError):
            return True
    
    def export_content(self, output_file: str, max_file_size_mb: int = 10) -> None:
        """Export repository content to a formatted file for LLM ingestion."""
        processed_files = 0
        max_size = max_file_size_mb * 1024 * 1024
        
        with open(output_file, 'w', encoding='utf-8') as out:
            # Write metadata header
            metadata = {
                "repository_path": str(self.root_path),
                "export_date": datetime.now().isoformat(),
                "files_processed": 0,
                "export_tool": "Repository Content Aggregator v2.0"
            }
            
            out.write("REPOSITORY CONTENT EXPORT\n")
            out.write("=" * 80 + "\n\n")
            out.write("METADATA:\n")
            out.write(json.dumps(metadata, indent=2))
            out.write("\n\n")
            
            # Track current directory for pretty formatting
            current_dir = None
            
            # Walk the repository
            for dirpath, dirnames, filenames in os.walk(self.root_path):
                dir_path = Path(dirpath)
                
                # Explicitly remove .git directory
                if '.git' in dirnames:
                    dirnames.remove('.git')
                
                # Remove ignored directories from processing
                dirnames[:] = [
                    d for d in dirnames 
                    if not self._should_ignore(dir_path / d) and not d.startswith('.git')
                ]
                
                # Write directory header if we've moved to a new directory
                if dirpath != current_dir:
                    current_dir = dirpath
                    rel_dir = str(Path(dirpath).relative_to(self.root_path))
                    out.write(f"\n{'#' * 80}\n")
                    out.write(f"DIRECTORY: {rel_dir}\n")
                    out.write("#" * 80 + "\n")
                
                # Process files in sorted order for consistency
                for filename in sorted(filenames):
                    file_path = dir_path / filename
                    
                    # Skip ignored files and git files
                    if (self._should_ignore(file_path) or 
                        '.git' in file_path.parts or 
                        file_path.name.startswith('.git')):
                        continue
                    
                    # Skip files that are too large
                    if file_path.stat().st_size > max_size:
                        print(f"Skipping large file: {file_path}")
                        continue
                    
                    # Skip binary files
                    if self._is_binary_file(file_path):
                        print(f"Skipping binary file: {file_path}")
                        continue
                    
                    try:
                        # Write file header
                        rel_path = str(file_path.relative_to(self.root_path))
                        out.write(f"\n{'=' * 80}\n")
                        out.write(f"FILE: {rel_path}\n")
                        out.write(f"ABSOLUTE PATH: {file_path}\n")
                        out.write("=" * 80 + "\n\n")
                        
                        # Write file content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            out.write(f.read())
                            out.write("\n\n")
                        
                        processed_files += 1
                        
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
            
            # Update metadata with final count
            metadata['files_processed'] = processed_files
            
            # Go back to start and update metadata with final count
            out.seek(0)
            out.write("REPOSITORY CONTENT EXPORT\n")
            out.write("=" * 80 + "\n\n")
            out.write("METADATA:\n")
            out.write(json.dumps(metadata, indent=2))

def main():
    """Main function to run the repository content aggregator."""
    import sys
    import argparse

    # First parser to get the directory
    parser = argparse.ArgumentParser(
        description='Repository content aggregator for LLM ingestion with Git-like ignore rules'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to analyze (defaults to current directory)'
    )
    parser.add_argument(
        '--max-size',
        '-m',
        type=int,
        default=10,
        help='Maximum file size in MB (default: 10)'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (defaults to <directory_name>_content.txt)'
    )
    
    args = parser.parse_args()
    
    # If no output specified, create default based on directory name
    if not args.output:
        directory = args.directory.rstrip('/\\')
        args.output = Path(directory).name + '_content.txt'
    
    try:
        print(f"Processing repository: {args.directory}")
        print(f"Output file: {args.output}")
        
        aggregator = RepositoryAggregator(args.directory)
        aggregator.export_content(
            args.output,
            max_file_size_mb=args.max_size
        )
        
        print("\nExport completed successfully!")
        print(f"Content has been written to: {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()