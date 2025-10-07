import os
from pathlib import Path
from typing import Dict, List
import re
from datetime import datetime
import json

class GitignoreRule:
    def __init__(self, pattern: str, source_dir: Path):
        self.pattern = pattern[1:] if pattern.startswith('!') else pattern
        self.is_negation = pattern.startswith('!')
        self.is_directory = pattern.endswith('/')
        self.source_dir = source_dir
        self.regex = self._build_regex()
    
    def _build_regex(self) -> re.Pattern:
        pattern = self.pattern.rstrip('/')
        pattern = pattern.replace('\\', '/')
        anchored = pattern.startswith('/')
        pattern = pattern[1:] if anchored else pattern
        
        # Convert to regex, preserving wildcards
        pattern = ''.join([
            c if c in ['*', '?', '/'] else re.escape(c)
            for c in pattern
        ])
        
        # Handle gitignore pattern types
        pattern = pattern.replace('**/', '(.*/)?')
        pattern = pattern.replace('/**', '(/.*)?')
        pattern = pattern.replace('*', '[^/]*')
        pattern = pattern.replace('?', '[^/]')
        
        # Handle directory-only matches
        if self.is_directory:
            pattern += '(/.*)?'
            
        # Build final pattern
        pattern = f"^{pattern}" if anchored else f"(^|.*/)/{pattern}"
        pattern += '(/.*)?$'
        
        return re.compile(pattern)
    
    def matches(self, path: str) -> bool:
        path = path.replace('\\', '/')
        path = path[2:] if path.startswith('./') else path
        
        try:
            rel_path = os.path.relpath(path, self.source_dir)
            rel_path = rel_path.replace('\\', '/')
            return bool(self.regex.match(rel_path))
        except ValueError:
            return False

class GitignoreManager:
    DEFAULT_IGNORES = [
        '.git/', '.git/**', '.gitmodules',
        '.gitattributes', '.git-*'
    ]
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.rules_cache: Dict[Path, List[GitignoreRule]] = {}
        self.default_rules = [
            GitignoreRule(pattern, root_path)
            for pattern in self.DEFAULT_IGNORES
        ]
        self._load_all_gitignores()
    
    def _load_all_gitignores(self) -> None:
        if (self.root_path / '.gitignore').exists():
            self._load_gitignore(self.root_path / '.gitignore')
        
        for dirpath, _, filenames in os.walk(self.root_path):
            if '.gitignore' in filenames and dirpath != str(self.root_path):
                self._load_gitignore(Path(dirpath) / '.gitignore')
    
    def _load_gitignore(self, path: Path) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.rules_cache[path] = [
                    GitignoreRule(line.strip(), path.parent)
                    for line in f
                    if line.strip() and not line.startswith('#')
                ]
        except Exception as e:
            print(f"Warning: Error loading {path}: {e}")
    
    def is_ignored(self, path: Path) -> bool:
        path_str = str(path)
        
        if any(rule.matches(path_str) for rule in self.default_rules):
            return True
            
        try:
            rel_path = path.relative_to(self.root_path)
            parents = [self.root_path] + [
                self.root_path / p
                for p in rel_path.parent.parts
            ]
            
            ignored = False
            for parent in parents:
                gitignore_path = parent / '.gitignore'
                if gitignore_path in self.rules_cache:
                    for rule in self.rules_cache[gitignore_path]:
                        if rule.matches(path_str):
                            ignored = not rule.is_negation
            return ignored
            
        except ValueError:
            return False

class RepositoryAggregator:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.gitignore_manager = GitignoreManager(self.root_path)
    
    def _is_binary_file(self, file_path: Path) -> bool:
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                if not chunk:  # Empty file
                    return False
                    
                # Check common binary signatures
                if any([
                    chunk.startswith(b'%PDF-'),
                    chunk.startswith(b'PK\x03\x04'),  # ZIP
                    chunk.startswith(b'PK\x05\x06'),  # ZIP empty
                    chunk.startswith(b'\x89PNG\r\n\x1a\n'),  # PNG
                    chunk.startswith(b'GIF87a'),  # GIF
                    chunk.startswith(b'GIF89a'),  # GIF
                    chunk.startswith(bytes([0xFF, 0xD8])),  # JPEG
                ]):
                    return True
                    
                # Check for binary content
                text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
                non_text = [b for b in chunk if b not in text_chars]
                return bool(chunk.count(b'\x00') > 0 or
                          (len(non_text) / len(chunk) > 0.3 if chunk else False))
                    
        except (IOError, OSError):
            return True
    
    def export_content(self, output_file: str, max_file_size_mb: int = 10) -> None:
        processed_files = 0
        max_size = max_file_size_mb * 1024 * 1024
        
        with open(output_file, 'w', encoding='utf-8') as out:
            metadata = {
                "repository_path": str(self.root_path),
                "export_date": datetime.now().isoformat(),
                "files_processed": 0,
                "export_tool": "Repository Content Aggregator v2.0"
            }
            
            self._write_header(out, metadata)
            current_dir = None
            
            for dirpath, dirnames, filenames in os.walk(self.root_path):
                dir_path = Path(dirpath)
                
                # Skip .git directories
                if '.git' in dirnames:
                    dirnames.remove('.git')
                
                # Filter ignored directories
                dirnames[:] = [
                    d for d in dirnames 
                    if not self.gitignore_manager.is_ignored(dir_path / d)
                    and not d.startswith('.git')
                ]
                
                # Write directory header
                if dirpath != current_dir:
                    current_dir = dirpath
                    rel_dir = str(Path(dirpath).relative_to(self.root_path))
                    self._write_directory_header(out, rel_dir)
                
                # Process files
                for filename in sorted(filenames):
                    file_path = dir_path / filename
                    
                    # Skip ignored and git files
                    if (self.gitignore_manager.is_ignored(file_path) or
                        '.git' in file_path.parts or
                        file_path.name.startswith('.git')):
                        continue
                    
                    # Skip large files
                    if file_path.stat().st_size > max_size:
                        print(f"Skipping large file: {file_path}")
                        continue
                    
                    # Skip binary files
                    if self._is_binary_file(file_path):
                        print(f"Skipping binary file: {file_path}")
                        continue
                    
                    try:
                        processed_files += self._write_file_content(out, file_path)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
            
            # Update final metadata
            metadata['files_processed'] = processed_files
            out.seek(0)
            self._write_header(out, metadata)
    
    def _write_header(self, out, metadata: dict) -> None:
        out.write("REPOSITORY CONTENT EXPORT\n")
        out.write("=" * 80 + "\n\n")
        out.write("METADATA:\n")
        out.write(json.dumps(metadata, indent=2))
        out.write("\n\n")
    
    def _write_directory_header(self, out, rel_dir: str) -> None:
        out.write(f"\n{'#' * 80}\n")
        out.write(f"DIRECTORY: {rel_dir}\n")
        out.write("#" * 80 + "\n")
    
    def _write_file_content(self, out, file_path: Path) -> int:
        rel_path = str(file_path.relative_to(self.root_path))
        out.write(f"\n{'=' * 80}\n")
        out.write(f"FILE: {rel_path}\n")
        out.write(f"ABSOLUTE PATH: {file_path}\n")
        out.write("=" * 80 + "\n\n")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            out.write(f.read())
            out.write("\n\n")
        
        return 1

def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Repository content aggregator for LLM ingestion'
    )
    parser.add_argument(
        'directory',
        help='Directory to analyze'
    )
    parser.add_argument(
        '--max-size',
        '-m',
        type=int,
        default=10,
        help='Maximum file size in MB (default: 10)'
    )
    
    args = parser.parse_args()
    output_file = Path(args.directory.rstrip('/\\')).name + '_content.txt'
    
    try:
        print(f"Processing repository: {args.directory}")
        print(f"Output file: {output_file}")
        
        # Check if output directory exists
        output_path = Path(output_file)
        if output_path.parent != Path('.'):
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        aggregator = RepositoryAggregator(args.directory)
        aggregator.export_content(
            output_file,
            max_file_size_mb=args.max_size
        )
        
        print("\nExport completed successfully!")
        print(f"Content has been written to: {output_file}")
        
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()