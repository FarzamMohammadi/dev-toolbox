"""
Configuration settings for the Python formatter.
Centralizes all formatting rules and exclusion patterns.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Set


@dataclass
class FormatterConfig:
    """Configuration class for the Python code formatter."""

    # Line formatting
    max_line_length: int = 88
    indent_size: int = 4

    # Import sorting
    import_sections: List[str] = None
    known_first_party: List[str] = None

    # Exclusion patterns
    exclude_dirs: Set[str] = None
    exclude_files: Set[str] = None

    # Flake8-style ignores
    ignore_codes: Set[str] = None

    # Special handling
    allow_unused_imports_in_init: bool = True

    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.import_sections is None:
            self.import_sections = [
                "FUTURE",
                "STDLIB",
                "THIRDPARTY",
                "FIRSTPARTY",
                "LOCALFOLDER"
            ]

        if self.known_first_party is None:
            self.known_first_party = []

        if self.exclude_dirs is None:
            self.exclude_dirs = {
                "__pycache__",
                ".git",
                ".venv",
                "venv",
                ".env",
                "env",
                "build",
                "dist",
                "migrations",
                ".pytest_cache",
                "node_modules",
                ".mypy_cache"
            }

        if self.exclude_files is None:
            self.exclude_files = {
                ".pyc",
                ".pyo",
                ".pyd",
                "__pycache__"
            }

        if self.ignore_codes is None:
            # Based on your .flake8 configuration
            self.ignore_codes = {
                "E203",  # whitespace before ':'
                "W503",  # line break before binary operator
                "E501",  # line too long (handled by our formatter)
                "C901"   # complexity checks (disabled)
            }

    def should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded from formatting."""
        # Check if any part of the path matches excluded directories
        for part in path.parts:
            if part in self.exclude_dirs:
                return True

        # Check file extension
        if path.suffix in self.exclude_files:
            return True

        return False

    def should_allow_unused_imports(self, file_path: Path) -> bool:
        """Check if unused imports should be allowed in this file."""
        return self.allow_unused_imports_in_init and file_path.name == "__init__.py"


# Default configuration instance
DEFAULT_CONFIG = FormatterConfig()