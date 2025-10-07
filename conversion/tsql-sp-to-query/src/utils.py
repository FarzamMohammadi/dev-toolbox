"""
Utility functions for the SP converter
"""

import logging
import sys
from pathlib import Path


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Set up logging configuration

    Args:
        verbose: If True, set log level to DEBUG

    Returns:
        Configured logger instance
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    return logging.getLogger('sp-converter')


def validate_file_path(file_path: str) -> Path:
    """
    Validate that a file path exists and is readable

    Args:
        file_path: Path to validate

    Returns:
        Path object if valid

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If path is not a file
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return path


def read_sql_file(file_path: Path) -> str:
    """
    Read SQL file content with UTF-8 encoding (handles BOM)

    Args:
        file_path: Path to SQL file

    Returns:
        File content as string
    """
    # Try UTF-8 with BOM first, then UTF-8
    try:
        return file_path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        return file_path.read_text(encoding='utf-8')


def write_sql_file(file_path: Path, content: str) -> None:
    """
    Write SQL content to file with UTF-8 encoding

    Args:
        file_path: Output file path
        content: SQL content to write
    """
    file_path.write_text(content, encoding='utf-8')


def get_output_filename(input_path: Path, suffix: str = '_READONLY') -> Path:
    """
    Generate output filename based on input filename

    Args:
        input_path: Input file path
        suffix: Suffix to add before extension

    Returns:
        Output file path
    """
    stem = input_path.stem
    extension = input_path.suffix

    output_name = f"{stem}{suffix}{extension}"
    return input_path.parent / output_name
