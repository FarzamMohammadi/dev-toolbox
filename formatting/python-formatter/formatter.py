#!/usr/bin/env python3
"""
Python Code Formatter - Standalone Tool

A self-contained Python code formatter that handles:
- Unused import removal
- Import sorting (Google style)
- Basic code formatting
- Common linting checks

Usage:
    python formatter.py .                    # Format current directory
    python formatter.py ./project-dir       # Format external project
    python formatter.py file.py             # Format single file
    python formatter.py . --check           # Check only, no changes
    python formatter.py . --verbose         # Show detailed output

Author: Python Code Formatter
Version: 1.0.0
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

import click
from typing import List

from formatter.core.config import DEFAULT_CONFIG
from formatter.core.code_formatter import CodeFormatter
from formatter.utils.file_handler import FileHandler
from formatter.utils.logger import Logger


class FormatterApp:
    """Main application class for the Python formatter."""

    def __init__(self, config=None, verbose=False):
        self.config = config or DEFAULT_CONFIG
        self.logger = Logger(verbose=verbose)
        self.file_handler = FileHandler(self.config)
        self.formatter = CodeFormatter(self.config)
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'issues_found': 0,
            'errors': 0
        }

    def format_target(self, target_path: Path, check_only: bool = False) -> bool:
        """
        Format a file or directory.

        Args:
            target_path: Path to format (file or directory)
            check_only: If True, only check for issues without modifying files

        Returns:
            True if successful, False if errors occurred
        """
        if not target_path.exists():
            self.logger.error(f"Path does not exist: {target_path}")
            return False

        # Find all Python files
        python_files = list(self.file_handler.find_python_files(target_path))

        if not python_files:
            self.logger.warning("No Python files found to process")
            return True

        self.logger.info(f"Found {len(python_files)} Python file(s) to process")

        # Process files with progress tracking
        with self.logger.create_progress("Formatting files") as progress:
            for i, file_path in enumerate(python_files):
                relative_path = self.file_handler.get_relative_path(file_path, target_path)
                progress.update(i, len(python_files), relative_path)

                success = self._process_file(file_path, check_only)
                if not success:
                    self.stats['errors'] += 1

                self.stats['files_processed'] += 1

            # Final update
            progress.update(len(python_files), len(python_files), "Complete")

        self._print_summary(check_only)
        return self.stats['errors'] == 0

    def _process_file(self, file_path: Path, check_only: bool) -> bool:
        """Process a single Python file."""
        try:
            # Read file content
            content = self.file_handler.read_file(file_path)
            if content is None:
                self.logger.error(f"Failed to read {file_path}")
                return False

            if check_only:
                # Check mode: only report issues
                issues = self.formatter.check_code(content)
                if issues:
                    self._report_issues(file_path, issues)
                    self.stats['issues_found'] += len(issues)
                    return True
                else:
                    self.logger.debug(f"{file_path} - No issues found")
                    return True

            else:
                # Format mode: modify files
                formatted_content = self.formatter.format_code(content, file_path)

                if formatted_content != content:
                    # Content changed, write it back
                    if self.file_handler.write_file(file_path, formatted_content):
                        self.logger.success(f"Formatted {file_path}")
                        self.stats['files_modified'] += 1
                        return True
                    else:
                        self.logger.error(f"Failed to write {file_path}")
                        return False
                else:
                    self.logger.debug(f"{file_path} - No changes needed")
                    return True

        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return False

    def _report_issues(self, file_path: Path, issues: List[dict]):
        """Report issues found in a file."""
        self.logger.warning(f"Issues found in {file_path}:")
        for issue in issues:
            line = issue.get('line', '?')
            code = issue.get('code', 'UNKNOWN')
            message = issue.get('message', 'Unknown issue')
            self.logger.info(f"  Line {line}: {code} - {message}")

    def _print_summary(self, check_only: bool):
        """Print processing summary."""
        mode = "checked" if check_only else "processed"
        self.logger.info(f"\nSummary:")
        self.logger.info(f"Files {mode}: {self.stats['files_processed']}")

        if check_only:
            if self.stats['issues_found'] > 0:
                self.logger.warning(f"Issues found: {self.stats['issues_found']}")
            else:
                self.logger.success("No issues found!")
        else:
            self.logger.info(f"Files modified: {self.stats['files_modified']}")

        if self.stats['errors'] > 0:
            self.logger.error(f"Errors encountered: {self.stats['errors']}")


@click.command()
@click.argument('target', type=click.Path(exists=True, path_type=Path))
@click.option('--check', is_flag=True, help='Check files for issues without modifying them')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.option('--version', is_flag=True, help='Show version information')
def main(target: Path, check: bool, verbose: bool, version: bool):
    """
    Python Code Formatter - Format Python files with import sorting and cleanup.

    TARGET can be a file or directory to format.
    Use '.' to format the current directory.
    """
    if version:
        click.echo("Python Code Formatter v1.0.0")
        click.echo("A standalone Python code formatter")
        return

    # Create and run formatter
    app = FormatterApp(verbose=verbose)

    try:
        success = app.format_target(target, check_only=check)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        app.logger.warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()