"""
File format detection and metadata extraction.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import polars as pl
from rich.console import Console

from ..config.settings import FileFormat


console = Console()


class FormatDetector:
    """Detect and analyze file formats for comparison."""

    @staticmethod
    def detect_format(filepath: Path) -> str:
        """
        Detect file format (CSV or Excel).

        Args:
            filepath: Path to file

        Returns:
            Format type: 'csv' or 'excel'

        Raises:
            ValueError: If format is not supported
        """
        if FileFormat.is_csv(filepath):
            return FileFormat.CSV

        if FileFormat.is_excel(filepath):
            return FileFormat.EXCEL

        raise ValueError(
            f"Unsupported file format: {filepath.suffix}. "
            f"Supported formats: CSV ({', '.join(FileFormat.CSV_EXTENSIONS)}) "
            f"or Excel ({', '.join(FileFormat.EXCEL_EXTENSIONS)})"
        )

    @staticmethod
    def get_file_info(filepath: Path) -> Dict[str, Any]:
        """
        Get detailed information about a file.

        Args:
            filepath: Path to file

        Returns:
            Dictionary with file metadata
        """
        file_size = filepath.stat().st_size
        file_format = FormatDetector.detect_format(filepath)

        info = {
            "path": str(filepath),
            "name": filepath.name,
            "format": file_format,
            "size_bytes": file_size,
            "size_mb": file_size / (1024 * 1024),
        }

        return info

    @staticmethod
    def detect_delimiter(filepath: Path, sample_size: int = 5) -> str:
        """
        Detect CSV delimiter by analyzing first few lines.

        Args:
            filepath: Path to CSV file
            sample_size: Number of lines to sample

        Returns:
            Detected delimiter character
        """
        # Common delimiters to try
        delimiters = [',', '\t', ';', '|']

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            sample_lines = [f.readline() for _ in range(sample_size)]

        # Count occurrences of each delimiter
        delimiter_counts = {}
        for delim in delimiters:
            counts = [line.count(delim) for line in sample_lines if line.strip()]
            if counts and all(c == counts[0] for c in counts) and counts[0] > 0:
                # Delimiter appears consistent number of times
                delimiter_counts[delim] = counts[0]

        if delimiter_counts:
            # Return delimiter with highest consistent count
            return max(delimiter_counts, key=delimiter_counts.get)

        # Default to comma
        return ','

    @staticmethod
    def estimate_row_count(filepath: Path, sample_rows: int = 1000) -> int:
        """
        Estimate total row count for a file (faster than reading entire file).

        Args:
            filepath: Path to file
            sample_rows: Number of rows to sample for estimation

        Returns:
            Estimated row count
        """
        file_format = FormatDetector.detect_format(filepath)

        try:
            if file_format == FileFormat.CSV:
                # For CSV, read a sample and estimate based on file size
                delimiter = FormatDetector.detect_delimiter(filepath)

                # Read small sample to get average row size
                try:
                    sample_df = pl.read_csv(
                        filepath,
                        separator=delimiter,
                        n_rows=sample_rows,
                        infer_schema_length=100
                    )
                    sample_count = len(sample_df)
                except Exception:
                    # If Polars fails, fall back to counting lines
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        sample_count = sum(1 for _ in zip(range(sample_rows), f))

                if sample_count == 0:
                    return 0

                # Estimate based on file size
                file_size = filepath.stat().st_size
                bytes_per_row = file_size / sample_count

                # Rough estimate of total rows
                estimated_rows = int(file_size / bytes_per_row)
                return max(1, estimated_rows)

            else:  # Excel
                # For Excel, we need to actually read to get accurate count
                # Read just the first chunk to get started
                df = pl.read_excel(filepath, read_options={"n_rows": None})
                return len(df)

        except Exception as e:
            console.print(f"[yellow]Warning: Could not estimate row count: {e}[/yellow]")
            return 0

    @staticmethod
    def get_column_info(filepath: Path, file_format: Optional[str] = None) -> Dict[str, Any]:
        """
        Get column information from file.

        Args:
            filepath: Path to file
            file_format: Optional format override

        Returns:
            Dictionary with column metadata
        """
        if file_format is None:
            file_format = FormatDetector.detect_format(filepath)

        try:
            if file_format == FileFormat.CSV:
                delimiter = FormatDetector.detect_delimiter(filepath)
                df = pl.read_csv(
                    filepath,
                    separator=delimiter,
                    n_rows=0,  # Just read headers
                    infer_schema_length=0
                )
            else:  # Excel
                df = pl.read_excel(filepath, read_options={"n_rows": 0})

            return {
                "columns": df.columns,
                "column_count": len(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
            }

        except Exception as e:
            console.print(f"[yellow]Warning: Could not read column info: {e}[/yellow]")
            return {
                "columns": [],
                "column_count": 0,
                "dtypes": {}
            }
