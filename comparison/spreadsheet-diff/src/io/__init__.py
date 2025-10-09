"""I/O module for reading and writing large files."""

from .readers import FileReader
from .writers import ResultWriter
from .format_detector import FormatDetector

__all__ = ["FileReader", "ResultWriter", "FormatDetector"]
