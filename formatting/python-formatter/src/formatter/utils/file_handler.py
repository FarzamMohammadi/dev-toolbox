"""
File handling utilities for the Python formatter.
Handles file discovery, reading, and writing operations.
"""

import os
from pathlib import Path
from typing import Generator, List, Optional

from ..core.config import FormatterConfig


class FileHandler:
    """Handles file operations for the Python formatter."""

    def __init__(self, config: FormatterConfig):
        self.config = config

    def find_python_files(self, target_path: Path) -> Generator[Path, None, None]:
        """
        Find all Python files in the target path.

        Args:
            target_path: Path to search (file or directory)

        Yields:
            Path objects for Python files to process
        """
        if target_path.is_file():
            if self._is_python_file(target_path) and not self.config.should_exclude_path(target_path):
                yield target_path
            return

        if target_path.is_dir():
            for root, dirs, files in os.walk(target_path):
                # Modify dirs in-place to skip excluded directories
                dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

                for file in files:
                    file_path = Path(root) / file
                    if self._is_python_file(file_path) and not self.config.should_exclude_path(file_path):
                        yield file_path

    def read_file(self, file_path: Path) -> Optional[str]:
        """
        Read a Python file and return its contents.

        Args:
            file_path: Path to the file to read

        Returns:
            File contents as string, or None if reading fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, UnicodeDecodeError) as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def write_file(self, file_path: Path, content: str) -> bool:
        """
        Write content to a Python file.

        Args:
            file_path: Path to the file to write
            content: Content to write

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except IOError as e:
            print(f"Error writing {file_path}: {e}")
            return False

    def backup_file(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of a file before modifying it.

        Args:
            file_path: Path to the file to backup

        Returns:
            Path to backup file, or None if backup fails
        """
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        try:
            content = self.read_file(file_path)
            if content is not None:
                if self.write_file(backup_path, content):
                    return backup_path
        except Exception as e:
            print(f"Error creating backup for {file_path}: {e}")
        return None

    def _is_python_file(self, file_path: Path) -> bool:
        """Check if a file is a Python file."""
        return file_path.suffix == '.py'

    def get_relative_path(self, file_path: Path, base_path: Path) -> str:
        """Get relative path for display purposes."""
        try:
            return str(file_path.relative_to(base_path))
        except ValueError:
            # If file_path is not relative to base_path
            return str(file_path)