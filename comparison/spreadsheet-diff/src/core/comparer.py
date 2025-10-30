"""
Main file comparison engine.
Handles large-scale comparisons (10M+ rows) using chunked processing.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
import polars as pl
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..config.settings import ComparisonSettings
from ..io.readers import FileReader
from ..io.writers import ResultWriter
from ..io.format_detector import FormatDetector
from ..utils.validators import FileValidator
from ..utils.performance import PerformanceMonitor
from ..utils.logger import get_logger
from .hash_engine import RowHashEngine
from .diff_tracker import DifferenceTracker


console = Console()
logger = get_logger(__name__)


class FileComparer:
    """
    Main comparison engine for large files.
    Uses streaming and chunked processing for memory efficiency.
    """

    # Constants for row difference formatting
    ALL_FIELDS_INDICATOR = "ALL_FIELDS"
    FIELD_SEPARATOR = "\n"
    NULL_DISPLAY = "(null)"
    EMPTY_DISPLAY = "(empty)"
    MAX_CELL_LENGTH = 32000  # Excel limit is 32,767, leaving some buffer

    def __init__(self, settings: Optional[ComparisonSettings] = None):
        """
        Initialize file comparer.

        Args:
            settings: Comparison settings (uses defaults if None)
        """
        self.settings = settings or ComparisonSettings()
        self.reader = FileReader(self.settings)
        self.writer = ResultWriter(self.settings)
        self.format_detector = FormatDetector()
        self.validator = FileValidator()
        self.hash_engine = RowHashEngine(self.settings.use_fast_hash)

        self.key_column: Optional[str] = None
        self.diff_tracker: Optional[DifferenceTracker] = None

    def _should_use_vectorized_path(self, source_file: Path, comparison_file: Path) -> bool:
        """
        Determine if vectorized comparison path should be used.

        Args:
            source_file: Path to source file
            comparison_file: Path to comparison file

        Returns:
            True if vectorized path should be used
        """
        # Estimate total rows
        source_rows = self.reader.estimate_rows(source_file)
        comparison_rows = self.reader.estimate_rows(comparison_file)
        total_rows = source_rows + comparison_rows

        # Use vectorized path for files below chunking threshold
        return total_rows < self.settings.skip_chunking_threshold

    def _load_full_dataframe(self, filepath: Path) -> pl.DataFrame:
        """Load entire file into DataFrame."""
        # Enable Polars parallelism based on settings
        if self.settings.enable_polars_parallel:
            pl.Config.set_streaming_chunk_size(100000)

        return self.reader.read_file(filepath)

    def _compare_vectorized(
        self,
        source_file: Path,
        comparison_file: Path
    ) -> bool:
        """
        Vectorized comparison for small-to-medium files.
        Loads both files entirely and uses Polars joins for comparison.

        Args:
            source_file: Path to source file
            comparison_file: Path to comparison file

        Returns:
            True if comparison completed successfully
        """
        console.print("[cyan]Using fast vectorized comparison[/cyan]")

        key_columns = self.settings.get_key_columns()
        if not key_columns:
            key_columns = [self.key_column]
        exclude_columns = self.settings.get_exclude_columns()

        # Load both files in parallel
        console.print("[yellow]Loading files...[/yellow]")
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_source = executor.submit(self._load_full_dataframe, source_file)
            future_comparison = executor.submit(self._load_full_dataframe, comparison_file)

            source_df = future_source.result()
            comparison_df = future_comparison.result()

        console.print(f"[green]Loaded {len(source_df):,} source rows, {len(comparison_df):,} comparison rows[/green]")

        # Update summary
        self.diff_tracker.summary.total_source_rows = len(source_df)
        self.diff_tracker.summary.total_comparison_rows = len(comparison_df)

        # Check for duplicate keys
        source_key_counts = source_df.select(key_columns).n_unique()
        has_duplicates = source_key_counts < len(source_df)

        if has_duplicates:
            console.print("[yellow]Duplicate keys detected, using row-by-row comparison[/yellow]")
            # Fall back to index-based comparison for duplicates
            return self._compare_with_index_method(source_file, comparison_file)

        # For unique keys, use optimized join-based comparison
        console.print("[green]Keys are unique, using optimized join comparison[/green]")

        # Perform join on key columns
        join_keys = key_columns if len(key_columns) > 1 else key_columns[0]

        merged = source_df.join(
            comparison_df,
            on=join_keys,
            how="outer",
            suffix="_comparison"
        )

        # Find rows only in source or comparison
        # For rows only in source: comparison columns will be null
        # For rows only in comparison: source columns will be null
        first_non_key_col = source_df.columns[0] if source_df.columns[0] != join_keys else source_df.columns[1]
        only_in_source = merged.filter(pl.col(f"{first_non_key_col}_comparison").is_null())
        only_in_comparison = merged.filter(pl.col(first_non_key_col).is_null())

        self.diff_tracker.summary.only_in_source = len(only_in_source)
        self.diff_tracker.summary.only_in_comparison = len(only_in_comparison)

        # Add rows only in source to detailed output
        for row_dict in only_in_source.iter_rows(named=True):
            key_value = self._extract_key_value(row_dict, key_columns)

            # Extract source columns (without _comparison suffix)
            source_row_dict = {
                col: row_dict[col]
                for col in row_dict.keys()
                if not col.endswith("_comparison")
            }

            self._add_row_difference(
                row_dict=source_row_dict,
                key_columns=key_columns,
                key_value=key_value,
                exclude_columns=exclude_columns,
                diff_type="removed"
            )

        # Add rows only in comparison to detailed output
        for row_dict in only_in_comparison.iter_rows(named=True):
            key_value = self._extract_key_value(row_dict, key_columns)

            # Extract comparison columns and remove _comparison suffix
            comparison_row_dict = {
                col[:-11]: row_dict[col]  # Remove "_comparison" suffix
                for col in row_dict.keys()
                if col.endswith("_comparison")
            }
            # Add key columns
            for col in key_columns:
                if col in row_dict:
                    comparison_row_dict[col] = row_dict[col]

            self._add_row_difference(
                row_dict=comparison_row_dict,
                key_columns=key_columns,
                key_value=key_value,
                exclude_columns=exclude_columns,
                diff_type="added"
            )

        # Compare field values for matching keys
        console.print("[yellow]Comparing field values...[/yellow]")
        self._compare_rows_vectorized(merged, key_columns, exclude_columns)

        console.print(f"[green]Found {len(self.diff_tracker.differences):,} differences[/green]")

        return True

    def _compare_rows_vectorized(
        self,
        merged_df: pl.DataFrame,
        key_columns: List[str],
        exclude_columns: List[str]
    ):
        """
        Compare rows using vectorized operations.

        Args:
            merged_df: Merged DataFrame with both source and comparison data
            key_columns: List of key column names
            exclude_columns: Columns to exclude from comparison
        """
        # Get all column names from source (without _comparison suffix)
        source_columns = [col for col in merged_df.columns if not col.endswith("_comparison") and col not in key_columns]

        exclude_set = set(exclude_columns)

        # Iterate through rows and find differences
        for row_dict in merged_df.iter_rows(named=True):
            key_value = tuple(row_dict[col] for col in key_columns) if len(key_columns) > 1 else row_dict[key_columns[0]]

            has_differences = False
            for col in source_columns:
                if col in exclude_set:
                    continue

                source_val = row_dict.get(col)
                comparison_val = row_dict.get(f"{col}_comparison")

                # Normalize for comparison
                source_norm = self.diff_tracker._normalize_for_comparison(source_val)
                comparison_norm = self.diff_tracker._normalize_for_comparison(comparison_val)

                if source_norm != comparison_norm:
                    self.diff_tracker.add_field_difference(
                        key_value=key_value,
                        field_name=col,
                        source_value=source_val,
                        comparison_value=comparison_val,
                        diff_type="modified"
                    )
                    has_differences = True

            if has_differences:
                self.diff_tracker.summary.modified_rows += 1
            else:
                self.diff_tracker.summary.exact_matches += 1

    def _extract_key_value(self, row_dict: Dict[str, Any], key_columns: List[str]) -> Any:
        """
        Extract key value from a row dictionary.

        Args:
            row_dict: Row data dictionary
            key_columns: List of key column names

        Returns:
            Single key value or tuple for composite keys
        """
        if len(key_columns) == 1:
            return row_dict[key_columns[0]]
        return tuple(row_dict[col] for col in key_columns)

    def _add_row_difference(
        self,
        row_dict: Dict[str, Any],
        key_columns: List[str],
        key_value: Any,
        exclude_columns: List[str],
        diff_type: str
    ):
        """
        Add a single consolidated row difference for rows that only exist in one file.
        All field values are formatted as multi-line "Field: Value" pairs for readability.

        Args:
            row_dict: Row data dictionary
            key_columns: List of key column names to exclude
            key_value: The key value for this row
            exclude_columns: Columns to exclude from comparison
            diff_type: "added" (only in comparison) or "removed" (only in source)

        Example output format:
            Applicant_FirstName: John
            Applicant_LastName: Doe
            Applicant_Email: john@example.com
            ...
        """
        # Validate diff_type
        if diff_type not in ("added", "removed"):
            logger.warning(f"Invalid diff_type '{diff_type}' for key {key_value}. Skipping.")
            return

        # Handle empty row_dict
        if not row_dict:
            logger.warning(f"Empty row_dict for key {key_value} with type {diff_type}. Skipping.")
            return

        exclude_set = set(exclude_columns) | set(key_columns)
        field_value_pairs = []

        # Collect and sort field names for consistent ordering
        field_names = sorted([
            field_name for field_name in row_dict.keys()
            if field_name not in exclude_set and not field_name.endswith("_comparison")
        ])

        for field_name in field_names:
            field_value = row_dict[field_name]

            # Format value with proper null/empty handling
            if field_value is None:
                value_str = self.NULL_DISPLAY
            elif isinstance(field_value, str) and field_value.strip() == "":
                value_str = self.EMPTY_DISPLAY
            else:
                value_str = str(field_value)

            field_value_pairs.append(f"{field_name}: {value_str}")

        # Handle case where all fields were excluded
        if not field_value_pairs:
            logger.warning(
                f"No fields to display for key {key_value} (all excluded). "
                f"Type: {diff_type}"
            )
            return

        # Concatenate with newlines for readability
        concatenated_values = self.FIELD_SEPARATOR.join(field_value_pairs)

        # Check for Excel cell length limit and truncate if needed
        if len(concatenated_values) > self.MAX_CELL_LENGTH:
            truncated_values = concatenated_values[:self.MAX_CELL_LENGTH]
            num_hidden_fields = len(field_value_pairs) - concatenated_values[:self.MAX_CELL_LENGTH].count(self.FIELD_SEPARATOR)
            concatenated_values = f"{truncated_values}\n... ({num_hidden_fields} more fields truncated)"
            logger.warning(
                f"Concatenated value for key {key_value} exceeds Excel limit. "
                f"Truncated {num_hidden_fields} fields."
            )

        # Set source and comparison values based on diff type
        if diff_type == "removed":
            source_value = concatenated_values
            comparison_value = None
        else:  # diff_type == "added"
            source_value = None
            comparison_value = concatenated_values

        # Add single consolidated difference record
        self.diff_tracker.add_field_difference(
            key_value=key_value,
            field_name=self.ALL_FIELDS_INDICATOR,
            source_value=source_value,
            comparison_value=comparison_value,
            diff_type=diff_type
        )

    def _compare_with_index_method(
        self,
        source_file: Path,
        comparison_file: Path
    ) -> bool:
        """
        Use original index-based method for files with duplicate keys.

        Args:
            source_file: Path to source file
            comparison_file: Path to comparison file

        Returns:
            True if successful
        """
        # Build source index
        console.print("\n[bold cyan]Building source file index...[/bold cyan]")
        source_index = self._build_file_index(source_file, "Source")

        # Compare with comparison file
        console.print("\n[bold cyan]Comparing files...[/bold cyan]")
        self._compare_against_index(comparison_file, source_index)

        return True

    def compare_files(
        self,
        source_file: Path,
        comparison_file: Path,
        key_column: Optional[str] = None
    ) -> bool:
        """
        Compare two files and generate difference report.

        Args:
            source_file: Path to source (reference) file
            comparison_file: Path to comparison file
            key_column: Optional key column name (auto-detect if None)

        Returns:
            True if comparison completed successfully
        """
        monitor = PerformanceMonitor("File Comparison")

        try:
            # Step 1: Validate files
            console.print("\n[bold cyan]Step 1: Validating files...[/bold cyan]")
            self._validate_files(source_file, comparison_file)

            # Step 2: Determine key column
            console.print("\n[bold cyan]Step 2: Determining key column...[/bold cyan]")
            self.key_column = self._determine_key_column(source_file, key_column)
            console.print(f"Using key column: [green]{self.key_column}[/green]")

            # Display excluded columns if any
            exclude_columns = self.settings.get_exclude_columns()
            if exclude_columns:
                console.print(f"Excluding columns: [yellow]{', '.join(exclude_columns)}[/yellow]")

            # Initialize diff tracker
            self.diff_tracker = DifferenceTracker(self.key_column)

            # Step 3: Choose comparison strategy
            console.print("\n[bold cyan]Step 3: Analyzing file size and choosing strategy...[/bold cyan]")
            use_vectorized = self._should_use_vectorized_path(source_file, comparison_file)

            if use_vectorized:
                # Fast path: vectorized comparison for small-to-medium files
                console.print("[cyan]Files are small enough for vectorized comparison[/cyan]")
                self._compare_vectorized(source_file, comparison_file)
            else:
                # Chunked path: index-based comparison for large files
                console.print("[cyan]Using chunked comparison for large files[/cyan]")

                # Build source index
                console.print("\n[bold cyan]Step 3a: Building source file index...[/bold cyan]")
                source_index = self._build_file_index(source_file, "Source")
                monitor.update_rows(len(source_index))

                # Compare with comparison file
                console.print("\n[bold cyan]Step 3b: Comparing files...[/bold cyan]")
                self._compare_against_index(comparison_file, source_index)
                monitor.update_rows(self.diff_tracker.summary.total_comparison_rows)

            # Step 5: Generate reports
            console.print("\n[bold cyan]Step 5: Generating reports...[/bold cyan]")
            self._generate_reports(source_file, comparison_file)

            # Complete
            monitor.complete()
            monitor.print_summary()

            # Print final summary
            self.diff_tracker.print_summary()

            if not self.diff_tracker.has_differences():
                console.print("\n[bold green]No differences found! Files are identical.[/bold green]")
            else:
                console.print(f"\n[bold yellow]Found {len(self.diff_tracker.differences):,} differences.[/bold yellow]")

            return True

        except Exception as e:
            console.print(f"\n[bold red]Comparison failed: {e}[/bold red]")
            logger.exception("Comparison error")
            return False

    def _validate_files(self, source_file: Path, comparison_file: Path):
        """Validate input files."""
        # Check source file
        is_valid, error = self.validator.validate_file_exists(source_file)
        if not is_valid:
            raise ValueError(error)

        is_valid, error = self.validator.validate_file_format(source_file)
        if not is_valid:
            raise ValueError(error)

        # Check comparison file
        is_valid, error = self.validator.validate_file_exists(comparison_file)
        if not is_valid:
            raise ValueError(error)

        is_valid, error = self.validator.validate_file_format(comparison_file)
        if not is_valid:
            raise ValueError(error)

        console.print("[green]OK: Files validated successfully[/green]")

    def _determine_key_column(self, filepath: Path, key_column: Optional[str]) -> str:
        """
        Determine which column to use as key.

        Args:
            filepath: Path to file (to read columns from)
            key_column: Optional explicit key column

        Returns:
            Name of key column to use

        Raises:
            ValueError: If key column cannot be determined
        """
        if key_column:
            # Validate that key column exists
            sample_df = self.reader.read_sample(filepath, n_rows=1)
            is_valid, error = self.validator.validate_key_column(
                sample_df, key_column, filepath.name
            )
            if not is_valid:
                raise ValueError(error)
            return key_column

        # Try to auto-detect
        console.print("[yellow]No key column specified, attempting auto-detection...[/yellow]")
        sample_df = self.reader.read_sample(filepath, n_rows=1000)
        detected_key = self.validator.auto_detect_key_column(sample_df)

        if detected_key:
            console.print(f"[green]Auto-detected key column: {detected_key}[/green]")
            return detected_key

        # Fall back to using first column
        first_col = sample_df.columns[0]
        console.print(
            f"[yellow]Could not auto-detect key column. "
            f"Using first column: {first_col}[/yellow]"
        )
        return first_col

    def _build_file_index(self, filepath: Path, label: str) -> Dict[Any, List[Dict[str, Any]]]:
        """
        Build an index of file contents (key -> list of rows).
        Supports multiple rows per key (duplicates).

        Args:
            filepath: Path to file
            label: Label for progress display

        Returns:
            Dictionary mapping key values to list of row data (supports duplicates)
        """
        index = {}
        total_rows = 0
        sort_columns = self.settings.get_sort_columns()

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=False
        ) as progress:

            task = progress.add_task(f"Reading {label} file...", total=None)

            for chunk in self.reader.read_chunked(filepath):
                for row_dict in chunk.iter_rows(named=True):
                    key_value = self._get_composite_key(row_dict)

                    if key_value is not None:
                        # Store row with its hash in a list (supports duplicates)
                        row_hash = self.hash_engine.hash_row(row_dict)
                        row_entry = {
                            "hash": row_hash,
                            "data": row_dict
                        }

                        if key_value not in index:
                            index[key_value] = []
                        index[key_value].append(row_entry)

                    total_rows += 1

                progress.update(task, advance=len(chunk))

            progress.update(task, completed=True, description=f"{label} file indexed")

        # Sort rows within each key group if sort columns specified
        if sort_columns:
            console.print(f"[yellow]Sorting duplicate keys by: {', '.join(sort_columns)}[/yellow]")
            for key_value in index:
                if len(index[key_value]) > 1:
                    index[key_value] = self._sort_rows(index[key_value], sort_columns)

        console.print(f"[green]OK: Indexed {total_rows:,} rows from {label} file[/green]")

        # Report duplicate key statistics
        duplicate_keys = sum(1 for rows in index.values() if len(rows) > 1)
        if duplicate_keys > 0:
            console.print(f"[yellow]Found {duplicate_keys:,} keys with multiple rows[/yellow]")

        # Update summary
        if label == "Source":
            self.diff_tracker.summary.total_source_rows = total_rows
        else:
            self.diff_tracker.summary.total_comparison_rows = total_rows

        return index

    def _compare_against_index(
        self,
        filepath: Path,
        source_index: Dict[Any, List[Dict[str, Any]]]
    ):
        """
        Compare file against source index.
        Handles duplicate keys by matching rows by position.

        Args:
            filepath: Path to comparison file
            source_index: Index built from source file (key -> list of rows)
        """
        # Track which comparison rows we've seen for each key
        comparison_key_counts = {}
        comparison_keys = set()
        exact_matches = 0
        sort_columns = self.settings.get_sort_columns()
        exclude_columns = self.settings.get_exclude_columns()
        key_columns = self.settings.get_key_columns() or [self.key_column]

        # Build comparison index first (needed for sorting duplicates)
        console.print("[yellow]Building comparison index for duplicate handling...[/yellow]")
        comparison_index = self._build_file_index(filepath, "Comparison")

        # Now compare row-by-row with position matching
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=False
        ) as progress:

            task = progress.add_task("Comparing files...", total=len(comparison_index))

            for key_value, comparison_rows in comparison_index.items():
                comparison_keys.add(key_value)

                if key_value in source_index:
                    source_rows = source_index[key_value]

                    # Match rows by position within key group
                    max_rows = max(len(source_rows), len(comparison_rows))

                    for i in range(max_rows):
                        if i < len(source_rows) and i < len(comparison_rows):
                            # Both files have this position - compare them
                            source_row = source_rows[i]
                            comparison_row = comparison_rows[i]

                            source_hash = source_row["hash"]
                            comparison_hash = comparison_row["hash"]

                            if source_hash == comparison_hash:
                                # Exact match
                                exact_matches += 1
                            else:
                                # Row modified - find field-level differences
                                source_data = source_row["data"]
                                comparison_data = comparison_row["data"]
                                diff_count = self.diff_tracker.compare_rows(
                                    key_value,
                                    source_data,
                                    comparison_data,
                                    ignore_columns=exclude_columns
                                )
                                if diff_count > 0:
                                    self.diff_tracker.summary.modified_rows += 1

                        elif i < len(source_rows):
                            # Only in source (extra row in source)
                            self.diff_tracker.summary.only_in_source += 1

                            # Add to detailed output
                            source_row = source_rows[i]
                            self._add_row_difference(
                                row_dict=source_row["data"],
                                key_columns=key_columns,
                                key_value=key_value,
                                exclude_columns=exclude_columns,
                                diff_type="removed"
                            )

                        elif i < len(comparison_rows):
                            # Only in comparison (extra row in comparison)
                            self.diff_tracker.summary.only_in_comparison += 1

                            # Add to detailed output
                            comparison_row = comparison_rows[i]
                            self._add_row_difference(
                                row_dict=comparison_row["data"],
                                key_columns=key_columns,
                                key_value=key_value,
                                exclude_columns=exclude_columns,
                                diff_type="added"
                            )

                else:
                    # Key only in comparison file
                    self.diff_tracker.summary.only_in_comparison += len(comparison_rows)

                    # Add all rows for this key to detailed output
                    for comparison_row in comparison_rows:
                        self._add_row_difference(
                            row_dict=comparison_row["data"],
                            key_columns=key_columns,
                            key_value=key_value,
                            exclude_columns=exclude_columns,
                            diff_type="added"
                        )

                progress.update(task, advance=1)

            progress.update(task, completed=True, description="Comparison complete")

        # Find keys only in source
        source_keys = set(source_index.keys())
        only_in_source_keys = source_keys - comparison_keys
        for key in only_in_source_keys:
            self.diff_tracker.summary.only_in_source += len(source_index[key])

            # Add all rows for this key to detailed output
            for source_row in source_index[key]:
                self._add_row_difference(
                    row_dict=source_row["data"],
                    key_columns=key_columns,
                    key_value=key,
                    exclude_columns=exclude_columns,
                    diff_type="removed"
                )

        self.diff_tracker.summary.exact_matches = exact_matches

        console.print(f"[green]OK: Comparison complete[/green]")
        console.print(f"  Exact matches: {exact_matches:,}")
        console.print(f"  Differences found: {len(self.diff_tracker.differences):,}")

    def _get_composite_key(self, row_dict: Dict[str, Any]) -> Optional[Any]:
        """
        Get composite key value from row.
        Supports both single and multiple key columns.

        Args:
            row_dict: Row data

        Returns:
            Key value (single value or tuple for composite keys)
        """
        key_columns = self.settings.get_key_columns()

        if not key_columns:
            # Use single key column
            return row_dict.get(self.key_column)

        # Build composite key as tuple
        key_parts = []
        for col in key_columns:
            val = row_dict.get(col)
            if val is None:
                return None  # If any part of composite key is None, whole key is invalid
            key_parts.append(val)

        return tuple(key_parts) if len(key_parts) > 1 else key_parts[0]

    def _sort_rows(
        self,
        rows: List[Dict[str, Any]],
        sort_columns: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Sort rows by specified columns.

        Args:
            rows: List of row entries (with 'hash' and 'data' keys)
            sort_columns: Columns to sort by

        Returns:
            Sorted list of rows
        """
        def sort_key(row_entry):
            row_data = row_entry["data"]
            # Create tuple of sort column values
            return tuple(row_data.get(col) for col in sort_columns)

        try:
            return sorted(rows, key=sort_key)
        except Exception as e:
            logger.warning(f"Failed to sort rows: {e}. Using original order.")
            return rows

    def _generate_reports(self, source_file: Path, comparison_file: Path):
        """Generate output reports."""
        if not self.diff_tracker.has_differences():
            console.print("[green]No differences to report[/green]")
            return

        # Get differences as DataFrame
        diff_df = self.diff_tracker.get_differences_dataframe()

        # Get summary stats
        summary_stats = {
            "total_differences": len(self.diff_tracker.differences),
            "unique_keys": len(set(diff.key_value for diff in self.diff_tracker.differences)),
            "exact_matches": self.diff_tracker.summary.exact_matches
        }

        # Write outputs
        output_files = self.writer.write_differences(
            diff_df,
            source_file.name,
            comparison_file.name,
            summary_stats
        )

        console.print(f"\n[bold green]Reports generated successfully![/bold green]")
        for file in output_files:
            console.print(f"  [blue]{file}[/blue]")
