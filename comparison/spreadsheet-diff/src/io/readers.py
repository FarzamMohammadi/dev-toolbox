"""
File readers with chunked processing support for large files.
Supports both CSV and Excel formats.
"""

from pathlib import Path
from typing import Iterator, Optional
import polars as pl
from rich.console import Console

from ..config.settings import FileFormat, ComparisonSettings
from .format_detector import FormatDetector


console = Console()


class FileReader:
    """
    Chunked file reader for CSV and Excel files.
    Supports streaming for memory-efficient processing of large files.
    """

    def __init__(self, settings: ComparisonSettings):
        """
        Initialize file reader.

        Args:
            settings: Comparison settings
        """
        self.settings = settings
        self.format_detector = FormatDetector()

    def read_file(
        self,
        filepath: Path,
        chunk_size: Optional[int] = None
    ) -> pl.DataFrame:
        """
        Read entire file into memory.
        Use only for small files or when chunking is not needed.

        Args:
            filepath: Path to file
            chunk_size: Optional chunk size override

        Returns:
            Polars DataFrame
        """
        file_format = self.format_detector.detect_format(filepath)

        if file_format == FileFormat.CSV:
            delimiter = self.format_detector.detect_delimiter(filepath)
            return pl.read_csv(
                filepath,
                separator=delimiter,
                infer_schema_length=10000,
                null_values=self.settings.null_equivalents
            )
        else:  # Excel
            return pl.read_excel(filepath)

    def read_chunked(
        self,
        filepath: Path,
        chunk_size: Optional[int] = None
    ) -> Iterator[pl.DataFrame]:
        """
        Read file in chunks for memory-efficient processing.

        Args:
            filepath: Path to file
            chunk_size: Number of rows per chunk (uses settings default if None)

        Yields:
            DataFrame chunks
        """
        if chunk_size is None:
            chunk_size = self.settings.chunk_size

        file_format = self.format_detector.detect_format(filepath)

        if file_format == FileFormat.CSV:
            yield from self._read_csv_chunked(filepath, chunk_size)
        else:  # Excel
            yield from self._read_excel_chunked(filepath, chunk_size)

    def _read_csv_chunked(self, filepath: Path, chunk_size: int) -> Iterator[pl.DataFrame]:
        """
        Read CSV file in chunks.

        Args:
            filepath: Path to CSV file
            chunk_size: Number of rows per chunk

        Yields:
            DataFrame chunks
        """
        delimiter = self.format_detector.detect_delimiter(filepath)

        # Polars CSV reader with lazy reading
        try:
            # Use scan_csv for lazy reading (Polars lazy API)
            lazy_df = pl.scan_csv(
                filepath,
                separator=delimiter,
                null_values=self.settings.null_equivalents,
                infer_schema_length=10000
            )

            # Process in chunks
            offset = 0
            while True:
                chunk = lazy_df.slice(offset, chunk_size).collect()

                if len(chunk) == 0:
                    break

                yield chunk
                offset += chunk_size

                if len(chunk) < chunk_size:
                    # Last chunk
                    break

        except Exception as e:
            console.print(f"[red]Error reading CSV file {filepath}: {e}[/red]")
            raise

    def _read_excel_chunked(self, filepath: Path, chunk_size: int) -> Iterator[pl.DataFrame]:
        """
        Read Excel file in chunks.
        Note: Excel reading is less memory-efficient than CSV.

        Args:
            filepath: Path to Excel file
            chunk_size: Number of rows per chunk

        Yields:
            DataFrame chunks
        """
        try:
            # For Excel, we have to read the whole file first
            # Then chunk it in memory
            df = pl.read_excel(filepath)

            total_rows = len(df)
            for start_idx in range(0, total_rows, chunk_size):
                end_idx = min(start_idx + chunk_size, total_rows)
                yield df.slice(start_idx, end_idx - start_idx)

        except Exception as e:
            console.print(f"[red]Error reading Excel file {filepath}: {e}[/red]")
            raise

    def get_columns(self, filepath: Path) -> list[str]:
        """
        Get column names from file without reading all data.

        Args:
            filepath: Path to file

        Returns:
            List of column names
        """
        file_format = self.format_detector.detect_format(filepath)

        if file_format == FileFormat.CSV:
            delimiter = self.format_detector.detect_delimiter(filepath)
            df = pl.read_csv(
                filepath,
                separator=delimiter,
                n_rows=0,  # Just headers
                infer_schema_length=0
            )
        else:  # Excel
            df = pl.read_excel(filepath, read_options={"n_rows": 0})

        return df.columns

    def estimate_rows(self, filepath: Path) -> int:
        """
        Estimate number of rows in file.

        Args:
            filepath: Path to file

        Returns:
            Estimated row count
        """
        return self.format_detector.estimate_row_count(filepath)

    def read_sample(self, filepath: Path, n_rows: int = 100) -> pl.DataFrame:
        """
        Read a sample of rows from file.

        Args:
            filepath: Path to file
            n_rows: Number of rows to read

        Returns:
            DataFrame with sample rows
        """
        file_format = self.format_detector.detect_format(filepath)

        if file_format == FileFormat.CSV:
            delimiter = self.format_detector.detect_delimiter(filepath)
            return pl.read_csv(
                filepath,
                separator=delimiter,
                n_rows=n_rows,
                null_values=self.settings.null_equivalents
            )
        else:  # Excel
            return pl.read_excel(filepath, read_options={"n_rows": n_rows})
