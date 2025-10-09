"""
Difference tracker for managing and storing comparison results.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import polars as pl
from rich.console import Console


console = Console()


@dataclass
class DifferenceRecord:
    """Single field-level difference."""

    key_value: Any
    field_name: str
    source_value: Any
    comparison_value: Any
    difference_type: str = "modified"  # modified, added, removed

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "key": self.key_value,
            "field": self.field_name,
            "source_value": self.source_value,
            "comparison_value": self.comparison_value,
            "type": self.difference_type
        }


@dataclass
class ComparisonSummary:
    """Summary statistics for comparison."""

    total_source_rows: int = 0
    total_comparison_rows: int = 0
    exact_matches: int = 0
    modified_rows: int = 0
    only_in_source: int = 0
    only_in_comparison: int = 0
    field_differences: int = 0
    unique_keys_with_differences: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_source_rows": self.total_source_rows,
            "total_comparison_rows": self.total_comparison_rows,
            "exact_matches": self.exact_matches,
            "modified_rows": self.modified_rows,
            "only_in_source": self.only_in_source,
            "only_in_comparison": self.only_in_comparison,
            "field_differences": self.field_differences,
            "unique_keys_with_differences": self.unique_keys_with_differences
        }


class DifferenceTracker:
    """
    Track and manage differences found during comparison.
    """

    def __init__(self, key_column: str):
        """
        Initialize difference tracker.

        Args:
            key_column: Name of key column for grouping differences (can be comma-separated for composite keys)
        """
        self.key_column = key_column
        self.differences: List[DifferenceRecord] = []
        self.summary = ComparisonSummary()

    def add_field_difference(
        self,
        key_value: Any,
        field_name: str,
        source_value: Any,
        comparison_value: Any,
        diff_type: str = "modified"
    ):
        """
        Add a field-level difference.

        Args:
            key_value: Value of the key column
            field_name: Name of the field that differs
            source_value: Value in source file
            comparison_value: Value in comparison file
            diff_type: Type of difference (modified, added, removed)
        """
        diff = DifferenceRecord(
            key_value=key_value,
            field_name=field_name,
            source_value=source_value,
            comparison_value=comparison_value,
            difference_type=diff_type
        )
        self.differences.append(diff)

    def compare_rows(
        self,
        key_value: Any,
        source_row: Dict[str, Any],
        comparison_row: Dict[str, Any],
        ignore_columns: List[str] = None
    ) -> int:
        """
        Compare two rows and record all field differences.

        Args:
            key_value: Value of the key column
            source_row: Source row data
            comparison_row: Comparison row data
            ignore_columns: Columns to ignore in comparison

        Returns:
            Number of differences found
        """
        if ignore_columns is None:
            ignore_columns = []

        differences_found = 0

        # Get all columns (union of both rows)
        all_columns = set(source_row.keys()) | set(comparison_row.keys())

        for column in all_columns:
            if column in ignore_columns or column == self.key_column:
                continue

            source_val = source_row.get(column)
            comparison_val = comparison_row.get(column)

            # Normalize values for comparison
            source_normalized = self._normalize_for_comparison(source_val)
            comparison_normalized = self._normalize_for_comparison(comparison_val)

            if source_normalized != comparison_normalized:
                # Record the difference
                self.add_field_difference(
                    key_value=key_value,
                    field_name=column,
                    source_value=source_val,
                    comparison_value=comparison_val,
                    diff_type="modified"
                )
                differences_found += 1

        return differences_found

    def _normalize_for_comparison(self, value: Any) -> Any:
        """
        Normalize a value for comparison.
        Optimized to avoid creating Polars Series objects.

        Args:
            value: Value to normalize

        Returns:
            Normalized value
        """
        # Handle None
        if value is None:
            return None

        # Handle strings
        if isinstance(value, str):
            # Strip whitespace
            normalized = value.strip()
            # Treat common null representations as None
            if not normalized or normalized in ("None", "NULL", "null", "N/A", "nan", "NaN"):
                return None
            return normalized

        # Handle float NaN (avoid Polars overhead)
        if isinstance(value, float):
            import math
            if math.isnan(value):
                return None

        return value

    def get_differences_dataframe(self) -> pl.DataFrame:
        """
        Convert differences to Polars DataFrame.

        Returns:
            DataFrame of all differences
        """
        if not self.differences:
            # Return empty DataFrame with correct schema
            return pl.DataFrame({
                self.key_column: [],
                "field": [],
                "source_value": [],
                "comparison_value": [],
                "type": []
            })

        # Convert to list of dicts with all values as strings (avoid type inference issues)
        records = []
        for diff in self.differences:
            records.append({
                "key": str(diff.key_value) if diff.key_value is not None else "",
                "field": str(diff.field_name),
                "source_value": str(diff.source_value) if diff.source_value is not None else "",
                "comparison_value": str(diff.comparison_value) if diff.comparison_value is not None else "",
                "type": diff.difference_type
            })

        # Create DataFrame with explicit schema
        df = pl.DataFrame(
            records,
            schema={
                "key": pl.String,
                "field": pl.String,
                "source_value": pl.String,
                "comparison_value": pl.String,
                "type": pl.String
            }
        )

        # Rename 'key' column to actual key column name
        df = df.rename({"key": self.key_column})

        return df

    def get_summary(self) -> ComparisonSummary:
        """
        Get comparison summary statistics.

        Returns:
            ComparisonSummary object
        """
        # Update field differences count
        self.summary.field_differences = len(self.differences)

        # Count unique keys with differences
        if self.differences:
            unique_keys = set(diff.key_value for diff in self.differences)
            self.summary.unique_keys_with_differences = len(unique_keys)

        return self.summary

    def print_summary(self):
        """Print a formatted summary to console."""
        summary = self.get_summary()

        console.print("\n[bold]Comparison Summary[/bold]")
        console.print("=" * 60)
        console.print(f"Source file rows:       {summary.total_source_rows:,}")
        console.print(f"Comparison file rows:   {summary.total_comparison_rows:,}")
        console.print(f"Exact matches:          {summary.exact_matches:,}")
        console.print()
        console.print(f"[yellow]Modified rows:          {summary.modified_rows:,}[/yellow]")
        console.print(f"[yellow]Only in source:         {summary.only_in_source:,}[/yellow]")
        console.print(f"[yellow]Only in comparison:     {summary.only_in_comparison:,}[/yellow]")
        console.print()
        console.print(f"[bold red]Field-level differences: {summary.field_differences:,}[/bold red]")
        console.print(f"[bold red]Unique records affected: {summary.unique_keys_with_differences:,}[/bold red]")
        console.print("=" * 60)

    def has_differences(self) -> bool:
        """
        Check if any differences were found.

        Returns:
            True if differences exist
        """
        return len(self.differences) > 0

    def clear(self):
        """Clear all tracked differences."""
        self.differences.clear()
        self.summary = ComparisonSummary()
