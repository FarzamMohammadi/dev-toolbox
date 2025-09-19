"""
Configuration settings for the Excel to JSON converter.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ConverterSettings(BaseModel):
    """Configuration settings for the Excel to JSON converter."""

    # JSON output settings
    indent: Optional[int] = Field(
        default=2,
        description="Number of spaces for JSON indentation (None for compact)"
    )

    # Data handling settings
    handle_nan_as_null: bool = Field(
        default=True,
        description="Convert NaN values to null in JSON"
    )

    nan_replacement: str = Field(
        default="",
        description="String to replace NaN values with (if not using null)"
    )

    # Date handling
    stringify_dates: bool = Field(
        default=True,
        description="Convert datetime objects to strings"
    )

    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date format string for datetime conversion"
    )

    # Validation settings
    validate_data: bool = Field(
        default=True,
        description="Perform data validation after conversion"
    )

    sanitize_field_names: bool = Field(
        default=False,
        description="Automatically sanitize field names to be JSON-compatible"
    )

    # Performance settings
    chunk_size: int = Field(
        default=10000,
        description="Number of rows to process at once for large files"
    )

    max_file_size_mb: int = Field(
        default=500,
        description="Maximum file size in MB to process"
    )

    # Output settings
    preserve_formulas: bool = Field(
        default=False,
        description="Preserve Excel formulas instead of calculated values"
    )

    include_metadata: bool = Field(
        default=False,
        description="Include metadata about the conversion in output"
    )

    @field_validator('indent')
    @classmethod
    def validate_indent(cls, v):
        """Validate indent value."""
        if v is not None and v < 0:
            raise ValueError("Indent must be non-negative or None")
        return v

    @field_validator('chunk_size')
    @classmethod
    def validate_chunk_size(cls, v):
        """Validate chunk size."""
        if v < 1:
            raise ValueError("Chunk size must be at least 1")
        return v

    @field_validator('max_file_size_mb')
    @classmethod
    def validate_max_file_size(cls, v):
        """Validate maximum file size."""
        if v < 1:
            raise ValueError("Maximum file size must be at least 1 MB")
        return v

    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "ConverterSettings":
        """Create settings from dictionary."""
        return cls(**data)


class DefaultSettings:
    """Default settings constants."""

    # File extensions
    EXCEL_EXTENSIONS = {'.xlsx', '.xls', '.xlsm', '.xlsb'}
    JSON_EXTENSION = '.json'

    # Limits
    MAX_SHEET_NAME_LENGTH = 31
    MAX_COLUMN_WIDTH = 16384
    MAX_ROW_COUNT = 1048576

    # Default paths
    DEFAULT_OUTPUT_DIR = "json_output"
    DEFAULT_LOG_DIR = "logs"

    # Error messages
    ERROR_FILE_NOT_FOUND = "File not found: {}"
    ERROR_INVALID_FORMAT = "Invalid file format: {}"
    ERROR_CONVERSION_FAILED = "Conversion failed: {}"
    ERROR_WRITE_FAILED = "Failed to write output file: {}"
