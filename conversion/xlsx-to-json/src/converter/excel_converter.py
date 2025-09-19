"""
Excel to JSON Converter Module

This module provides functionality to convert Excel (.xlsx) files to JSON format,
using column headers as field names.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging

from ..utils.file_handler import FileHandler
from ..utils.validators import DataValidator
from ..config.settings import ConverterSettings


logger = logging.getLogger(__name__)
console = Console()


class ConversionResult(BaseModel):
    """Model for conversion result data"""

    source_file: str
    output_file: str
    sheet_name: Optional[str] = None
    rows_converted: int = 0
    success: bool = True
    error: Optional[str] = None


class ExcelToJsonConverter:
    """
    Main converter class for Excel to JSON transformation.

    Attributes:
        settings: Configuration settings for the converter
        file_handler: Utility for file operations
        validator: Data validation utility
    """

    def __init__(self, settings: Optional[ConverterSettings] = None):
        """Initialize the converter with optional settings."""
        self.settings = settings or ConverterSettings()
        self.file_handler = FileHandler()
        self.validator = DataValidator()
        self.results: List[ConversionResult] = []

    def convert_file(
        self,
        file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        sheet_name: Optional[Union[str, int]] = None
    ) -> ConversionResult:
        """
        Convert a single Excel file to JSON format.

        Args:
            file_path: Path to the input Excel file
            output_path: Optional custom output path for JSON file
            sheet_name: Specific sheet to convert (name or index)

        Returns:
            ConversionResult object with conversion details
        """
        file_path = Path(file_path)

        # Validate input file
        if not self.file_handler.validate_excel_file(file_path):
            return ConversionResult(
                source_file=str(file_path),
                output_file="",
                success=False,
                error=f"Invalid or non-existent Excel file: {file_path}"
            )

        # Determine output path
        if output_path is None:
            output_path = self._generate_output_path(file_path)
        else:
            output_path = Path(output_path)

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Converting {file_path.name}...[/cyan]",
                    total=None
                )

                # Read Excel file
                if sheet_name is not None:
                    df_dict = {sheet_name: pd.read_excel(file_path, sheet_name=sheet_name)}
                else:
                    # Read all sheets
                    df_dict = pd.read_excel(file_path, sheet_name=None)

                # Convert to JSON structure
                json_data = self._dataframe_to_json(df_dict)

                # Validate data if enabled
                if self.settings.validate_data:
                    validation_errors = self.validator.validate_json_structure(json_data)
                    if validation_errors:
                        # Group validation errors by field name
                        unique_fields = {}
                        for error in validation_errors:
                            # Extract field name from error message
                            if "contains special characters" in error:
                                # Extract the field name between quotes
                                import re
                                match = re.search(r"\[(\d+)\]\.(.*?)' contains", error)
                                if match:
                                    field_name = match.group(2)
                                    if field_name not in unique_fields:
                                        unique_fields[field_name] = 0
                                    unique_fields[field_name] += 1

                        # Display grouped warnings
                        if unique_fields:
                            console.print("\n[yellow]Validation Warnings:[/yellow]")
                            console.print("[dim]Fields with special characters:[/dim]")
                            for field, count in unique_fields.items():
                                console.print(f"  - {field} (in {count} rows)")
                            console.print()  # Add blank line after warnings

                # Write JSON file
                self.file_handler.write_json(output_path, json_data, self.settings.indent)

                progress.update(task, completed=True)

                # Count total rows
                if isinstance(json_data, list):
                    total_rows = len(json_data)
                elif isinstance(json_data, dict):
                    total_rows = sum(
                        len(data) if isinstance(data, list) else 1
                        for data in json_data.values()
                    )
                else:
                    total_rows = 0

                result = ConversionResult(
                    source_file=str(file_path),
                    output_file=str(output_path),
                    sheet_name=sheet_name if isinstance(sheet_name, str) else None,
                    rows_converted=total_rows,
                    success=True
                )

                console.print(
                    f"[green]Success[/green] Converted: {file_path.name} -> {output_path.name} "
                    f"({total_rows} rows)"
                )

        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            logger.error(error_msg)
            console.print(f"[red]Failed[/red]: {file_path.name} - {str(e)}")

            result = ConversionResult(
                source_file=str(file_path),
                output_file=str(output_path),
                success=False,
                error=error_msg
            )

        self.results.append(result)
        return result

    def convert_multiple(
        self,
        file_paths: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None
    ) -> List[ConversionResult]:
        """
        Convert multiple Excel files to JSON format.

        Args:
            file_paths: List of paths to Excel files
            output_dir: Optional directory for output files

        Returns:
            List of ConversionResult objects
        """
        results = []

        console.print(f"\n[bold cyan]Converting {len(file_paths)} files...[/bold cyan]\n")

        for file_path in file_paths:
            if output_dir:
                output_path = Path(output_dir) / self._generate_output_path(Path(file_path)).name
            else:
                output_path = None

            result = self.convert_file(file_path, output_path)
            results.append(result)

        # Print summary
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        console.print(f"\n[bold]Conversion Summary:[/bold]")
        console.print(f"  [green]Successful: {successful}[/green]")
        if failed > 0:
            console.print(f"  [red]Failed: {failed}[/red]")

        return results

    def _dataframe_to_json(self, df_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Convert pandas DataFrames to JSON-serializable dictionary.

        Args:
            df_dict: Dictionary of sheet names to DataFrames

        Returns:
            JSON-serializable dictionary
        """
        result = {}

        for sheet_name, df in df_dict.items():
            # Handle NaN values based on settings
            if self.settings.handle_nan_as_null:
                df = df.where(pd.notnull(df), None)

                # Also handle empty strings and string representations of NaN
                import math
                def clean_empty_values(x):
                    if x is None:
                        return None
                    # Handle numeric NaN (float)
                    if isinstance(x, float) and math.isnan(x):
                        return None
                    # Handle string representations
                    if isinstance(x, str):
                        # Strip whitespace and check for empty or NaN representations
                        cleaned = str(x).strip()
                        if cleaned == "" or cleaned.lower() in ["nan", "n/a", "null", "none"]:
                            return None
                    return x

                # Apply cleaning to all columns (using map instead of deprecated applymap)
                df = df.map(clean_empty_values)
            else:
                df = df.fillna(self.settings.nan_replacement)

            # Convert datetime objects to strings if needed
            if self.settings.stringify_dates:
                for col in df.select_dtypes(include=['datetime64']).columns:
                    df[col] = df[col].dt.strftime(self.settings.date_format)

            # Convert to dictionary
            if len(df_dict) == 1:
                # Single sheet - return list directly
                result = df.to_dict('records')
            else:
                # Multiple sheets - use sheet names as keys
                result[sheet_name] = df.to_dict('records')

        return result

    def _generate_output_path(self, input_path: Path) -> Path:
        """Generate output path based on input file path."""
        return input_path.parent / f"{input_path.stem}.json"

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all conversion results."""
        return {
            "total_files": len(self.results),
            "successful": sum(1 for r in self.results if r.success),
            "failed": sum(1 for r in self.results if not r.success),
            "total_rows": sum(r.rows_converted for r in self.results if r.success),
            "results": [r.model_dump() for r in self.results]
        }