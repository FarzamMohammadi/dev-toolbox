"""
Data validation utilities for the Excel to JSON converter.
"""

import re
from typing import Any, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Utility class for data validation."""

    def __init__(self):
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []

    def validate_json_structure(self, data: Union[Dict, List]) -> List[str]:
        """
        Validate the structure of converted JSON data.

        Args:
            data: JSON data to validate

        Returns:
            List of validation messages (warnings/errors)
        """
        self.validation_errors = []
        self.validation_warnings = []

        if isinstance(data, dict):
            self._validate_dict(data)
        elif isinstance(data, list):
            self._validate_list(data)
        else:
            self.validation_errors.append(
                f"Root data must be dict or list, got {type(data).__name__}"
            )

        return self.validation_warnings + self.validation_errors

    def _validate_dict(self, data: Dict, path: str = "") -> None:
        """
        Recursively validate dictionary structure.

        Args:
            data: Dictionary to validate
            path: Current path in the data structure
        """
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            # Check for invalid key names
            if not self._is_valid_key(key):
                self.validation_warnings.append(
                    f"Key '{current_path}' contains special characters"
                )

            # Recursively validate nested structures
            if isinstance(value, dict):
                self._validate_dict(value, current_path)
            elif isinstance(value, list):
                self._validate_list(value, current_path)

    def _validate_list(self, data: List, path: str = "") -> None:
        """
        Recursively validate list structure.

        Args:
            data: List to validate
            path: Current path in the data structure
        """
        if not data:
            self.validation_warnings.append(f"Empty list at '{path or 'root'}'")
            return

        # Check for consistent structure in list items
        first_type = type(data[0])
        inconsistent = False

        for i, item in enumerate(data):
            item_path = f"{path}[{i}]" if path else f"[{i}]"

            if type(item) != first_type:
                inconsistent = True

            if isinstance(item, dict):
                self._validate_dict(item, item_path)
            elif isinstance(item, list):
                self._validate_list(item, item_path)

        if inconsistent:
            self.validation_warnings.append(
                f"Inconsistent data types in list at '{path or 'root'}'"
            )

    def _is_valid_key(self, key: str) -> bool:
        """
        Check if a key name is valid (alphanumeric, underscore, dash).

        Args:
            key: Key name to validate

        Returns:
            True if valid, False otherwise
        """
        # Allow alphanumeric, underscore, dash, and space
        pattern = re.compile(r'^[a-zA-Z0-9_\-\s]+$')
        return bool(pattern.match(str(key)))

    def validate_field_names(self, field_names: List[str]) -> List[str]:
        """
        Validate Excel column names that will become JSON field names.

        Args:
            field_names: List of field names to validate

        Returns:
            List of validation messages
        """
        messages = []
        seen_names = set()

        for name in field_names:
            # Check for duplicates
            if name in seen_names:
                messages.append(f"Duplicate field name: '{name}'")
            seen_names.add(name)

            # Check for empty names
            if not name or name.strip() == "":
                messages.append("Empty field name detected")

            # Check for names that might cause issues
            if name.startswith("__"):
                messages.append(f"Field name starts with double underscore: '{name}'")

        return messages

    def sanitize_field_name(self, name: str) -> str:
        """
        Sanitize a field name to make it JSON-compatible.

        Args:
            name: Original field name

        Returns:
            Sanitized field name
        """
        # Convert to string if not already
        name = str(name)

        # Replace spaces with underscores
        name = name.replace(' ', '_')

        # Remove or replace special characters
        name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)

        # Ensure it doesn't start with a number
        if name and name[0].isdigit():
            name = f"field_{name}"

        # Handle empty result
        if not name:
            name = "unnamed_field"

        return name