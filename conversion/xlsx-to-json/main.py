#!/usr/bin/env python
"""
Excel to JSON Converter CLI

Command-line interface for converting Excel (.xlsx) files to JSON format.
Uses column headers as field names.

Usage:
    python convert_xlsx_to_json.py file1.xlsx [file2.xlsx ...]
    python convert_xlsx_to_json.py --output-dir ./output file1.xlsx file2.xlsx
    python convert_xlsx_to_json.py --sheet "Sheet1" data.xlsx
"""

import sys
from pathlib import Path
from typing import List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import logging

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.converter.excel_converter import ExcelToJsonConverter
from src.config.settings import ConverterSettings
from src.utils.logger import setup_logger


console = Console()
logger = setup_logger(__name__)


@click.command()
@click.argument(
    'files',
    nargs=-1,
    required=True,
    type=click.Path(exists=True, path_type=Path)
)
@click.option(
    '--output-dir', '-o',
    type=click.Path(path_type=Path),
    help='Directory for output JSON files (default: same as input)'
)
@click.option(
    '--sheet', '-s',
    help='Specific sheet to convert (name or index)'
)
@click.option(
    '--indent', '-i',
    type=int,
    default=2,
    help='JSON indentation spaces (default: 2)'
)
@click.option(
    '--compact', '-c',
    is_flag=True,
    help='Output minified JSON without indentation'
)
def main(
    files: tuple,
    output_dir: Optional[Path],
    sheet: Optional[str],
    indent: int,
    compact: bool
):
    """
    Convert Excel (.xlsx) files to JSON format.

    FILES: One or more Excel files to convert.

    Examples:

        Single file:
        $ python convert_xlsx_to_json.py data.xlsx

        Multiple files:
        $ python convert_xlsx_to_json.py file1.xlsx file2.xlsx file3.xlsx

        With options:
        $ python convert_xlsx_to_json.py --output-dir ./json_output --indent 4 *.xlsx
    """

    # Configure logging
    logging.getLogger().setLevel(logging.WARNING)

    # Display header
    console.print(
        Panel.fit(
            "[bold cyan]Excel to JSON Converter[/bold cyan]\n"
            "[dim]Converting Excel files with column headers as field names[/dim]",
            border_style="cyan"
        )
    )

    # Configure settings
    settings = ConverterSettings(
        indent=None if compact else indent,
        handle_nan_as_null=True,  # Always handle as null
        date_format='%Y-%m-%d %H:%M:%S',  # Use sensible default
        validate_data=True,  # Always validate
        stringify_dates=True
    )

    # Create converter
    converter = ExcelToJsonConverter(settings)

    # Create output directory if specified
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"Output directory: [blue]{output_dir}[/blue]\n")

    # Convert sheet parameter
    sheet_param = None
    if sheet:
        try:
            sheet_param = int(sheet)  # Try as index
        except ValueError:
            sheet_param = sheet  # Use as name

    # Process files
    file_list = list(files)

    if len(file_list) == 1:
        # Single file conversion
        result = converter.convert_file(
            file_list[0],
            output_path=output_dir / f"{file_list[0].stem}.json" if output_dir else None,
            sheet_name=sheet_param
        )

        if result.success:
            console.print(f"\n[green]Conversion completed successfully![/green]")
            console.print(f"  Output: [blue]{result.output_file}[/blue]")
            console.print(f"  Rows: {result.rows_converted}")
        else:
            console.print(f"\n[red]Conversion failed![/red]")
            console.print(f"  Error: {result.error}")
            sys.exit(1)

    else:
        # Multiple file conversion
        results = converter.convert_multiple(file_list, output_dir)

        # Display summary table
        console.print("\n")
        table = Table(title="Conversion Results", show_header=True, header_style="bold cyan")
        table.add_column("File", style="dim")
        table.add_column("Status", justify="center")
        table.add_column("Rows", justify="right")
        table.add_column("Output")

        for result in results:
            status = "[green]OK[/green]" if result.success else "[red]FAIL[/red]"
            file_name = Path(result.source_file).name
            output_name = Path(result.output_file).name if result.output_file else "N/A"
            rows = str(result.rows_converted) if result.success else "0"

            table.add_row(
                file_name,
                status,
                rows,
                output_name if result.success else f"[red]{result.error}[/red]"
            )

        console.print(table)

        # Print final summary
        summary = converter.get_summary()
        console.print(f"\n[bold]Total Summary:[/bold]")
        console.print(f"  Files processed: {summary['total_files']}")
        console.print(f"  [green]Successful: {summary['successful']}[/green]")
        if summary['failed'] > 0:
            console.print(f"  [red]Failed: {summary['failed']}[/red]")
            sys.exit(1)
        console.print(f"  Total rows converted: {summary['total_rows']}")

    console.print("\n[dim]Conversion complete.[/dim]")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Conversion cancelled by user.[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        logger.exception("Unexpected error occurred")
        sys.exit(1)