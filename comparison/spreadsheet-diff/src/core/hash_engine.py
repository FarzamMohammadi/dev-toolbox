"""
Row hashing engine for efficient comparison.
Uses xxhash for performance, falls back to hashlib if unavailable.
"""

import hashlib
from typing import Any, List, Dict
import polars as pl

try:
    import xxhash
    HAS_XXHASH = True
except ImportError:
    HAS_XXHASH = False


class RowHashEngine:
    """
    Efficiently compute row hashes for comparison.
    """

    def __init__(self, use_fast_hash: bool = True):
        """
        Initialize hash engine.

        Args:
            use_fast_hash: Use xxhash if available (faster than hashlib)
        """
        self.use_xxhash = use_fast_hash and HAS_XXHASH
        self.hash_enabled = True  # Can be disabled for unique keys

    def should_hash(self, keys_have_duplicates: bool) -> bool:
        """
        Determine if hashing is needed based on key uniqueness.

        Args:
            keys_have_duplicates: Whether keys have duplicate values

        Returns:
            True if hashing should be performed
        """
        return keys_have_duplicates

    def set_hash_enabled(self, enabled: bool):
        """Enable or disable hashing for performance optimization."""
        self.hash_enabled = enabled

    def hash_value(self, value: Any) -> str:
        """
        Hash a single value.
        Optimized to avoid creating Polars Series objects.

        Args:
            value: Value to hash

        Returns:
            Hex string hash
        """
        # Normalize value to string
        if value is None:
            str_value = "NULL"
        elif isinstance(value, float):
            # Handle NaN specially (avoid Polars overhead)
            import math
            if math.isnan(value):
                str_value = "NULL"
            else:
                # Format float to avoid floating point precision issues
                str_value = f"{value:.10f}"
        else:
            str_value = str(value)

        # Compute hash
        if self.use_xxhash:
            return xxhash.xxh64(str_value.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(str_value.encode('utf-8')).hexdigest()

    def hash_row(self, row: Dict[str, Any]) -> str:
        """
        Compute hash for an entire row.

        Args:
            row: Dictionary of column_name: value

        Returns:
            Hex string hash of entire row
        """
        # Sort columns for consistent hashing
        sorted_keys = sorted(row.keys())

        # Concatenate all values
        combined = "|".join(
            self._normalize_value(row[key]) for key in sorted_keys
        )

        # Hash the combined string
        if self.use_xxhash:
            return xxhash.xxh64(combined.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(combined.encode('utf-8')).hexdigest()

    def hash_dataframe_rows(self, df: pl.DataFrame) -> pl.Series:
        """
        Compute hashes for all rows in a DataFrame.

        Args:
            df: Polars DataFrame

        Returns:
            Series of row hashes
        """
        # Create hash for each row
        # Use Polars native operations for speed
        def row_hash_func(row_dict):
            return self.hash_row(row_dict)

        # Convert to list of dicts and hash
        hashes = []
        for row in df.iter_rows(named=True):
            hashes.append(self.hash_row(row))

        return pl.Series("_row_hash", hashes)

    def hash_key_value(self, key_value: Any, row: Dict[str, Any]) -> str:
        """
        Create composite hash of key + row values.

        Args:
            key_value: Value of the key column
            row: Dictionary of all column values

        Returns:
            Composite hash string
        """
        key_str = self._normalize_value(key_value)
        row_hash = self.hash_row(row)

        combined = f"{key_str}:{row_hash}"

        if self.use_xxhash:
            return xxhash.xxh64(combined.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(combined.encode('utf-8')).hexdigest()

    def _normalize_value(self, value: Any) -> str:
        """
        Normalize value to string for hashing.
        Optimized to avoid creating Polars Series objects.

        Args:
            value: Value to normalize

        Returns:
            Normalized string representation
        """
        if value is None:
            return "NULL"
        elif isinstance(value, float):
            import math
            if math.isnan(value):
                return "NULL"
            else:
                return f"{value:.10f}"
        elif isinstance(value, str):
            # Optionally strip whitespace
            return value.strip()
        else:
            return str(value)

    def create_row_fingerprint(
        self,
        df: pl.DataFrame,
        key_column: str,
        exclude_columns: List[str] = None
    ) -> pl.DataFrame:
        """
        Create fingerprints for all rows based on key + data hash.

        Args:
            df: DataFrame to fingerprint
            key_column: Name of key column
            exclude_columns: Optional columns to exclude from hash

        Returns:
            DataFrame with added '_fingerprint' column
        """
        if exclude_columns is None:
            exclude_columns = []

        # Select columns for hashing
        hash_columns = [col for col in df.columns if col not in exclude_columns]

        # Create subset for hashing
        hash_df = df.select(hash_columns)

        # Compute hashes
        fingerprints = []
        for row in hash_df.iter_rows(named=True):
            key_val = row.get(key_column)
            fingerprints.append(self.hash_key_value(key_val, row))

        # Add fingerprint column
        return df.with_columns(
            pl.Series("_fingerprint", fingerprints)
        )

    def get_hash_stats(self) -> Dict[str, Any]:
        """
        Get information about hash engine configuration.

        Returns:
            Dictionary with hash engine stats
        """
        return {
            "hash_algorithm": "xxhash64" if self.use_xxhash else "md5",
            "xxhash_available": HAS_XXHASH,
            "using_fast_hash": self.use_xxhash
        }
