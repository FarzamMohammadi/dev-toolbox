"""
Logging utilities for the Python formatter.
Provides colored console output and progress tracking.
"""

from enum import Enum
from typing import Optional

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

import colorama
from colorama import Fore, Style


class LogLevel(Enum):
    """Log levels for output."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class Logger:
    """Logger with colored output support."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.console = Console() if RICH_AVAILABLE else None

        # Initialize colorama for Windows support
        colorama.init()

    def debug(self, message: str):
        """Log debug message (only in verbose mode)."""
        if self.verbose:
            self._log(LogLevel.DEBUG, message)

    def info(self, message: str):
        """Log info message."""
        self._log(LogLevel.INFO, message)

    def warning(self, message: str):
        """Log warning message."""
        self._log(LogLevel.WARNING, message)

    def error(self, message: str):
        """Log error message."""
        self._log(LogLevel.ERROR, message)

    def success(self, message: str):
        """Log success message."""
        self._log(LogLevel.SUCCESS, message)

    def _log(self, level: LogLevel, message: str):
        """Internal logging method."""
        if RICH_AVAILABLE and self.console:
            self._rich_log(level, message)
        else:
            self._simple_log(level, message)

    def _rich_log(self, level: LogLevel, message: str):
        """Log using rich formatting."""
        color_map = {
            LogLevel.DEBUG: "dim white",
            LogLevel.INFO: "blue",
            LogLevel.WARNING: "yellow",
            LogLevel.ERROR: "red",
            LogLevel.SUCCESS: "green"
        }

        text = Text(f"[{level.value}] {message}", style=color_map[level])
        self.console.print(text)

    def _simple_log(self, level: LogLevel, message: str):
        """Log using simple colored output."""
        color_map = {
            LogLevel.DEBUG: Fore.WHITE + Style.DIM,
            LogLevel.INFO: Fore.BLUE,
            LogLevel.WARNING: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
            LogLevel.SUCCESS: Fore.GREEN
        }

        color = color_map[level]
        print(f"{color}[{level.value}] {message}{Style.RESET_ALL}")

    def create_progress(self, description: str = "Processing...") -> Optional['ProgressTracker']:
        """Create a progress tracker."""
        if RICH_AVAILABLE and self.console:
            return RichProgressTracker(description)
        else:
            return SimpleProgressTracker(description)


class ProgressTracker:
    """Base class for progress tracking."""

    def __init__(self, description: str):
        self.description = description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def update(self, current: int, total: int, current_file: str = ""):
        """Update progress."""
        pass


class RichProgressTracker(ProgressTracker):
    """Progress tracker using rich."""

    def __init__(self, description: str):
        super().__init__(description)
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=Console()
        )
        self.task_id = None

    def __enter__(self):
        self.progress.__enter__()
        self.task_id = self.progress.add_task(self.description, total=100)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.__exit__(exc_type, exc_val, exc_tb)

    def update(self, current: int, total: int, current_file: str = ""):
        """Update progress with current status."""
        if self.task_id is not None and total > 0:
            percentage = (current / total) * 100
            description = f"{self.description}"
            if current_file:
                description += f" - {current_file}"

            self.progress.update(self.task_id, completed=percentage, description=description)


class SimpleProgressTracker(ProgressTracker):
    """Simple progress tracker without rich."""

    def __init__(self, description: str):
        super().__init__(description)
        self.last_percentage = -1

    def update(self, current: int, total: int, current_file: str = ""):
        """Update progress with simple output."""
        if total > 0:
            percentage = int((current / total) * 100)
            if percentage != self.last_percentage:
                status = f"{self.description} - {percentage}% ({current}/{total})"
                if current_file:
                    status += f" - {current_file}"
                print(status)
                self.last_percentage = percentage