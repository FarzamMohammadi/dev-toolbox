"""
File handling utilities for the Excel to JSON converter.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """Utility class for file operations."""

    @staticmethod
    def validate_excel_file(file_path: Path) -> bool:
        """
        Validate that a file exists and has .xlsx extension.

        Args:
            file_path: Path to the file to validate

        Returns:
            True if valid Excel file, False otherwise
        """
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False

        if not file_path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            return False

        if file_path.suffix.lower() not in ['.xlsx', '.xls']:
            logger.error(f"File is not an Excel file: {file_path}")
            return False

        if file_path.stat().st_size == 0:
            logger.error(f"File is empty: {file_path}")
            return False

        return True

    @staticmethod
    def write_json(
        file_path: Path,
        data: Union[Dict, list],
        indent: Optional[int] = 2
    ) -> None:
        """
        Write data to a JSON file.

        Args:
            file_path: Path where to write the JSON file
            data: Data to write (dict or list)
            indent: Indentation level for pretty printing
        """
        try:
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Clean NaN values before JSON serialization
            cleaned_data = FileHandler._clean_nan_values(data)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    cleaned_data,
                    f,
                    indent=indent,
                    ensure_ascii=False,
                    default=str  # Convert non-serializable objects to string
                )

            logger.info(f"Successfully wrote JSON to {file_path}")

        except Exception as e:
            logger.error(f"Failed to write JSON to {file_path}: {e}")
            raise

    @staticmethod
    def _clean_nan_values(obj):
        """
        Recursively clean NaN values from nested data structures.

        Args:
            obj: Object to clean (dict, list, or other)

        Returns:
            Cleaned object with NaN values replaced by None
        """
        import math
        import numpy as np

        if isinstance(obj, dict):
            return {key: FileHandler._clean_nan_values(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [FileHandler._clean_nan_values(item) for item in obj]
        elif isinstance(obj, float) and math.isnan(obj):
            return None
        elif isinstance(obj, np.floating) and np.isnan(obj):
            return None
        else:
            return obj

    @staticmethod
    def read_json(file_path: Path) -> Union[Dict, list]:
        """
        Read data from a JSON file.

        Args:
            file_path: Path to the JSON file to read

        Returns:
            Parsed JSON data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"Successfully read JSON from {file_path}")
            return data

        except Exception as e:
            logger.error(f"Failed to read JSON from {file_path}: {e}")
            raise

    @staticmethod
    def ensure_directory(dir_path: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            dir_path: Path to the directory
        """
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {dir_path}")
