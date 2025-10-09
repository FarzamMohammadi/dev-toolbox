"""
Configuration settings for the file comparison tool.
Handles both CSV and Excel files with support for large datasets (10M+ rows).
"""

from typing import Optional, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class ComparisonSettings(BaseModel):
    """Configuration settings for file comparison operations."""

    # Performance settings
    chunk_size: int = Field(
        default=100000,
        description="Number of rows to process at once (tune based on available RAM)"
    )

    max_memory_mb: int = Field(
        default=4096,
        description="Maximum memory usage in MB before switching to disk-based processing"
    )

    use_multithreading: bool = Field(
        default=True,
        description="Enable multi-threaded processing for faster comparisons"
    )

    # Comparison settings
    key_column: Optional[str] = Field(
        default=None,
        description="Primary key column(s) for row matching. Supports composite keys as comma-separated string (e.g., 'ID,Date'). Auto-detects if None."
    )

    sort_columns: Optional[str] = Field(
        default=None,
        description="Optional columns to sort by within duplicate key groups (comma-separated)"
    )

    exclude_columns: Optional[str] = Field(
        default=None,
        description="Columns to exclude from comparison (comma-separated)"
    )

    case_sensitive: bool = Field(
        default=True,
        description="Case-sensitive string comparison"
    )

    ignore_whitespace: bool = Field(
        default=False,
        description="Ignore leading/trailing whitespace in comparisons"
    )

    # Output settings
    output_format: Literal["csv", "excel", "both"] = Field(
        default="excel",
        description="Output format for difference reports"
    )

    output_dir: Path = Field(
        default=Path("results"),
        description="Directory for output files"
    )

    include_matches: bool = Field(
        default=False,
        description="Include exact matches in output (not recommended for large files)"
    )

    generate_html_report: bool = Field(
        default=True,
        description="Generate interactive HTML report"
    )

    # Data handling
    handle_missing_columns: Literal["error", "warn", "ignore"] = Field(
        default="warn",
        description="How to handle columns that exist in one file but not the other"
    )

    null_equivalents: list[str] = Field(
        default_factory=lambda: ["", "NULL", "null", "None", "N/A", "nan"],
        description="Values to treat as null/empty"
    )

    # Hash settings
    use_fast_hash: bool = Field(
        default=True,
        description="Use xxhash (faster) instead of hashlib (falls back if unavailable)"
    )

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging verbosity level"
    )

    show_progress: bool = Field(
        default=True,
        description="Show progress bars during processing"
    )

    # Validation
    @field_validator('chunk_size')
    @classmethod
    def validate_chunk_size(cls, v):
        """Validate chunk size is reasonable."""
        if v < 1000:
            raise ValueError("Chunk size must be at least 1000 rows")
        if v > 1000000:
            raise ValueError("Chunk size should not exceed 1M rows (memory concerns)")
        return v

    @field_validator('max_memory_mb')
    @classmethod
    def validate_memory(cls, v):
        """Validate memory limit."""
        if v < 512:
            raise ValueError("Maximum memory must be at least 512 MB")
        return v

    @field_validator('output_dir')
    @classmethod
    def validate_output_dir(cls, v):
        """Ensure output directory is a Path object."""
        if isinstance(v, str):
            return Path(v)
        return v

    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "ComparisonSettings":
        """Create settings from dictionary."""
        return cls(**data)

    def get_key_columns(self) -> list[str]:
        """
        Parse key_column into list of column names.

        Returns:
            List of key column names (handles composite keys)
        """
        if not self.key_column:
            return []
        # Split on comma and strip whitespace
        return [col.strip() for col in self.key_column.split(',') if col.strip()]

    def get_sort_columns(self) -> list[str]:
        """
        Parse sort_columns into list of column names.

        Returns:
            List of sort column names
        """
        if not self.sort_columns:
            return []
        return [col.strip() for col in self.sort_columns.split(',') if col.strip()]

    def get_exclude_columns(self) -> list[str]:
        """
        Parse exclude_columns into list of column names.

        Returns:
            List of columns to exclude from comparison
        """
        if not self.exclude_columns:
            return []
        return [col.strip() for col in self.exclude_columns.split(',') if col.strip()]

    @classmethod
    def for_large_files(cls) -> "ComparisonSettings":
        """Optimized settings for very large files (5M+ rows)."""
        return cls(
            chunk_size=50000,
            max_memory_mb=8192,
            use_multithreading=True,
            output_format="csv",  # CSV is faster for large outputs
            include_matches=False,
            generate_html_report=False  # HTML can be huge for large diffs
        )

    @classmethod
    def for_small_files(cls) -> "ComparisonSettings":
        """Optimized settings for smaller files (<100k rows)."""
        return cls(
            chunk_size=50000,
            max_memory_mb=2048,
            use_multithreading=False,  # Threading overhead not worth it
            output_format="both",
            include_matches=False,
            generate_html_report=True
        )


class FileFormat:
    """Supported file formats and their properties."""

    CSV = "csv"
    EXCEL = "excel"

    # Excel limitations
    EXCEL_MAX_ROWS = 1048576
    EXCEL_MAX_COLS = 16384

    # File extensions
    CSV_EXTENSIONS = {".csv", ".txt", ".tsv"}
    EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".xlsb"}

    @classmethod
    def is_csv(cls, filepath: Path) -> bool:
        """Check if file is CSV format."""
        return filepath.suffix.lower() in cls.CSV_EXTENSIONS

    @classmethod
    def is_excel(cls, filepath: Path) -> bool:
        """Check if file is Excel format."""
        return filepath.suffix.lower() in cls.EXCEL_EXTENSIONS


class DefaultConstants:
    """Default constants and error messages."""

    # Limits
    HASH_CACHE_SIZE = 1000000  # Cache up to 1M row hashes
    MAX_DIFF_DISPLAY = 10000   # Max differences to show in terminal

    # Error messages
    ERROR_FILE_NOT_FOUND = "File not found: {}"
    ERROR_INVALID_FORMAT = "Unsupported file format: {}"
    ERROR_KEY_COLUMN_MISSING = "Key column '{}' not found in file"
    ERROR_MEMORY_EXCEEDED = "Memory limit exceeded. Consider increasing max_memory_mb or reducing chunk_size"
    ERROR_EXCEL_ROW_LIMIT = "Excel file exceeds maximum row limit ({} rows). Use CSV format instead."

    # Success messages
    SUCCESS_COMPARISON_COMPLETE = "Comparison completed successfully"
    SUCCESS_OUTPUT_SAVED = "Results saved to: {}"
