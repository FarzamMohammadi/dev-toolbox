"""
Performance monitoring utilities for tracking memory and time usage.
"""

import time
import psutil
from typing import Optional
from contextlib import contextmanager
from dataclasses import dataclass, field
from rich.console import Console


console = Console()


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""

    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    peak_memory_mb: float = 0.0
    start_memory_mb: float = 0.0
    rows_processed: int = 0
    operation_name: str = "Operation"

    @property
    def duration_seconds(self) -> float:
        """Get duration in seconds."""
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    @property
    def memory_used_mb(self) -> float:
        """Get memory used in MB."""
        return self.peak_memory_mb - self.start_memory_mb

    @property
    def rows_per_second(self) -> float:
        """Calculate processing speed."""
        duration = self.duration_seconds
        if duration > 0 and self.rows_processed > 0:
            return self.rows_processed / duration
        return 0.0

    def summary(self) -> str:
        """Generate performance summary string."""
        duration = self.duration_seconds
        hours, remainder = divmod(int(duration), 3600)
        minutes, seconds = divmod(remainder, 60)

        time_str = ""
        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"

        summary_parts = [
            f"{self.operation_name} completed in {time_str}"
        ]

        if self.rows_processed > 0:
            summary_parts.append(
                f"  Rows processed: {self.rows_processed:,} ({self.rows_per_second:,.0f} rows/sec)"
            )

        if self.memory_used_mb > 0:
            summary_parts.append(
                f"  Memory used: {self.memory_used_mb:.1f} MB (peak: {self.peak_memory_mb:.1f} MB)"
            )

        return "\n".join(summary_parts)


class PerformanceMonitor:
    """
    Monitor performance metrics during file comparison operations.
    """

    def __init__(self, operation_name: str = "Operation"):
        """
        Initialize performance monitor.

        Args:
            operation_name: Name of the operation being monitored
        """
        self.operation_name = operation_name
        self.metrics = PerformanceMetrics(operation_name=operation_name)
        self.process = psutil.Process()
        self._update_memory()
        self.metrics.start_memory_mb = self._get_memory_mb()

    def _get_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        try:
            return self.process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0.0

    def _update_memory(self):
        """Update peak memory usage."""
        current_memory = self._get_memory_mb()
        if current_memory > self.metrics.peak_memory_mb:
            self.metrics.peak_memory_mb = current_memory

    def update_rows(self, count: int):
        """
        Update the number of rows processed.

        Args:
            count: Number of rows processed
        """
        self.metrics.rows_processed += count
        self._update_memory()

    def complete(self):
        """Mark operation as complete."""
        self.metrics.end_time = time.time()
        self._update_memory()

    def get_metrics(self) -> PerformanceMetrics:
        """Get current metrics."""
        return self.metrics

    def print_summary(self):
        """Print performance summary to console."""
        console.print(f"\n[bold green]{self.metrics.summary()}[/bold green]")

    @contextmanager
    def track_operation(self, operation_name: str):
        """
        Context manager for tracking sub-operations.

        Args:
            operation_name: Name of sub-operation

        Yields:
            PerformanceMonitor instance for the sub-operation
        """
        sub_monitor = PerformanceMonitor(operation_name)
        try:
            yield sub_monitor
        finally:
            sub_monitor.complete()


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable string.

    Args:
        bytes_value: Number of bytes

    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def format_number(number: int) -> str:
    """
    Format large numbers with thousands separators.

    Args:
        number: Number to format

    Returns:
        Formatted string (e.g., "1,234,567")
    """
    return f"{number:,}"


def estimate_memory_required(row_count: int, column_count: int, avg_cell_size: int = 50) -> int:
    """
    Estimate memory required for processing a dataset.

    Args:
        row_count: Number of rows
        column_count: Number of columns
        avg_cell_size: Average size per cell in bytes

    Returns:
        Estimated memory in MB
    """
    total_cells = row_count * column_count
    estimated_bytes = total_cells * avg_cell_size
    # Add 50% overhead for processing
    estimated_bytes = int(estimated_bytes * 1.5)
    return estimated_bytes // (1024 * 1024)
