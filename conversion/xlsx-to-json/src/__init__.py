"""
Excel to JSON Converter Package

A robust, modular Python package for converting Excel files to JSON format.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .converter.excel_converter import ExcelToJsonConverter
from .config.settings import ConverterSettings

__all__ = [
    "ExcelToJsonConverter",
    "ConverterSettings",
]
