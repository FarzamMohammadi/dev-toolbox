"""
Validation utilities for file inputs and comparison parameters.
"""

from pathlib import Path
from typing import Tuple, Optional
import polars as pl
from rich.console import Console

from ..config.settings import FileFormat


console = Console()


class FileValidator:
    """Validates input files and comparison parameters."""

    @staticmethod
    def validate_file_exists(filepath: Path) -> Tuple[bool, Optional[str]]:
        """
        Check if file exists and is accessible.

        Args:
            filepath: Path to file

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filepath.exists():
            return False, f"File not found: {filepath}"

        if not filepath.is_file():
            return False, f"Path is not a file: {filepath}"

        if filepath.stat().st_size == 0:
            return False, f"File is empty: {filepath}"

        return True, None

    @staticmethod
    def validate_file_format(filepath: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate file format is supported (CSV or Excel).

        Args:
            filepath: Path to file

        Returns:
            Tuple of (is_valid, error_message)
        """
        if FileFormat.is_csv(filepath):
            return True, None

        if FileFormat.is_excel(filepath):
            return True, None

        supported = FileFormat.CSV_EXTENSIONS | FileFormat.EXCEL_EXTENSIONS
        return False, f"Unsupported file format '{filepath.suffix}'. Supported: {supported}"

    @staticmethod
    def validate_key_column(
        df: pl.DataFrame,
        key_column: str,
        filename: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that key column(s) exist in dataframe.
        Supports both single columns and composite keys (comma-separated).

        Args:
            df: Polars DataFrame
            key_column: Name of key column or comma-separated composite key
            filename: Name of file (for error messages)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Parse composite keys
        key_columns = [col.strip() for col in key_column.split(',') if col.strip()]

        # Check each column exists
        missing_columns = []
        for col in key_columns:
            if col not in df.columns:
                missing_columns.append(col)

        if missing_columns:
            available_cols = ", ".join(df.columns[:10])
            if len(df.columns) > 10:
                available_cols += f"... ({len(df.columns)} total)"

            if len(missing_columns) == 1:
                msg = f"Key column '{missing_columns[0]}' not found in {filename}."
            else:
                msg = f"Key columns {missing_columns} not found in {filename}."

            return False, (
                f"{msg} "
                f"Available columns: {available_cols}"
            )

        return True, None

    @staticmethod
    def check_file_compatibility(
        df1: pl.DataFrame,
        df2: pl.DataFrame,
        file1_name: str,
        file2_name: str
    ) -> Tuple[bool, list[str]]:
        """
        Check if two files are compatible for comparison.

        Args:
            df1: First DataFrame
            df2: Second DataFrame
            file1_name: Name of first file
            file2_name: Name of second file

        Returns:
            Tuple of (is_compatible, list_of_warnings)
        """
        warnings = []

        # Check for column differences
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)

        only_in_first = cols1 - cols2
        only_in_second = cols2 - cols1

        if only_in_first:
            warnings.append(
                f"Columns only in {file1_name}: {', '.join(sorted(only_in_first))}"
            )

        if only_in_second:
            warnings.append(
                f"Columns only in {file2_name}: {', '.join(sorted(only_in_second))}"
            )

        # Still compatible even with different columns
        is_compatible = len(cols1 & cols2) > 0

        if not is_compatible:
            warnings.append("No common columns found between files!")

        return is_compatible, warnings

    @staticmethod
    def auto_detect_key_column(df: pl.DataFrame) -> Optional[str]:
        """
        Attempt to auto-detect a key column from common patterns.

        Args:
            df: Polars DataFrame

        Returns:
            Name of detected key column, or None if not found
        """
        # Common key column name patterns (case-insensitive)
        common_key_patterns = [
            "id", "key", "pk", "primary_key",
            "identifier", "uuid", "guid",
            "_id", "_key"
        ]

        # First, try exact matches (case-insensitive)
        for col in df.columns:
            if col.lower() in common_key_patterns:
                return col

        # Next, try columns ending with common patterns
        for col in df.columns:
            col_lower = col.lower()
            for pattern in ["_id", "_key", "_pk"]:
                if col_lower.endswith(pattern):
                    return col

        # Look for columns with "id" or "key" anywhere in name
        for col in df.columns:
            col_lower = col.lower()
            if "id" in col_lower or "key" in col_lower:
                # Check if it's likely to be unique (sample first 1000 rows)
                sample_size = min(1000, len(df))
                sample = df.head(sample_size)
                if sample[col].n_unique() == len(sample):
                    return col

        return None

    @staticmethod
    def check_excel_row_limit(row_count: int, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Check if row count exceeds Excel limits.

        Args:
            row_count: Number of rows
            filename: Name of file

        Returns:
            Tuple of (is_within_limit, warning_message)
        """
        if row_count > FileFormat.EXCEL_MAX_ROWS:
            return False, (
                f"{filename} has {row_count:,} rows, exceeding Excel's limit "
                f"of {FileFormat.EXCEL_MAX_ROWS:,} rows. "
                "Results will be saved in CSV format."
            )

        return True, None
