#!/usr/bin/env python
"""
File Comparison Tool - CLI

High-performance comparison tool for large CSV and Excel files.
Handles 10M+ rows using chunked processing and streaming.

Usage:
    python compare.py source.csv comparison.csv
    python compare.py source.xlsx comparison.xlsx --key CustomerID
    python compare.py file1.csv file2.csv --output-dir ./results --format both
"""

import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.comparer import FileComparer
from src.config.settings import ComparisonSettings
from src.utils.logger import setup_logger


console = Console()
logger = setup_logger(__name__)


@click.command()
@click.argument(
    'source_file',
    type=click.Path(exists=True, path_type=Path),
    required=True
)
@click.argument(
    'comparison_file',
    type=click.Path(exists=True, path_type=Path),
    required=True
)
@click.option(
    '--key', '-k',
    type=str,
    help='Key column(s) for row matching. Supports composite keys (comma-separated: "ID,Date"). Auto-detects if not specified.'
)
@click.option(
    '--sort-by',
    type=str,
    help='Optional: Sort columns for duplicate key matching (comma-separated: "Date,Time")'
)
@click.option(
    '--exclude',
    type=str,
    help='Columns to exclude from comparison (comma-separated: "LastModified,UpdatedAt")'
)
@click.option(
    '--output-dir', '-o',
    type=click.Path(path_type=Path),
    default='results',
    help='Output directory for results (default: results)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['csv', 'excel', 'both'], case_sensitive=False),
    default='excel',
    help='Output format (default: excel)'
)
@click.option(
    '--chunk-size', '-c',
    type=int,
    default=100000,
    help='Number of rows to process at once (default: 100000)'
)
@click.option(
    '--no-html',
    is_flag=True,
    help='Skip HTML report generation'
)
@click.option(
    '--case-insensitive',
    is_flag=True,
    help='Perform case-insensitive comparison'
)
@click.option(
    '--ignore-whitespace',
    is_flag=True,
    help='Ignore leading/trailing whitespace'
)
@click.option(
    '--log-level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    default='INFO',
    help='Logging level (default: INFO)'
)
@click.option(
    '--hardware',
    type=click.Choice(['high-end', 'standard', 'low-tier'], case_sensitive=False),
    default='high-end',
    help='Hardware profile: high-end (24GB+ RAM, 8+ cores), standard (8-16GB, 4-8 cores), low-tier (4-8GB, 2-4 cores). Default: high-end'
)
def main(
    source_file: Path,
    comparison_file: Path,
    key: Optional[str],
    sort_by: Optional[str],
    exclude: Optional[str],
    output_dir: Path,
    format: str,
    chunk_size: int,
    no_html: bool,
    case_insensitive: bool,
    ignore_whitespace: bool,
    log_level: str,
    hardware: str
):
    """
    Compare two files (CSV or Excel) and generate difference report.

    SOURCE_FILE: Path to source/reference file (the "truth")
    COMPARISON_FILE: Path to file to compare against source

    Examples:

        Basic comparison:
        $ python compare.py source.csv comparison.csv

        With explicit key column:
        $ python compare.py data1.xlsx data2.xlsx --key CustomerID

        With composite key (unique combination):
        $ python compare.py data1.xlsx data2.xlsx --key "CustomerID,Date"

        Handle duplicates with sort:
        $ python compare.py data1.xlsx data2.xlsx --key ID --sort-by "Date,Time"

        Custom output:
        $ python compare.py file1.csv file2.csv -o ./output -f both

        Large files (10M+ rows):
        $ python compare.py large1.csv large2.csv --chunk-size 50000
    """

    # Display header
    console.print(
        Panel.fit(
            "[bold cyan]File Comparison Tool[/bold cyan]\n"
            "[dim]High-performance comparison for large CSV and Excel files[/dim]",
            border_style="cyan"
        )
    )

    # Configure settings from hardware profile
    settings = ComparisonSettings.from_hardware_profile(
        hardware.lower(),
        key_column=key,
        sort_columns=sort_by,
        exclude_columns=exclude,
        output_dir=output_dir,
        output_format=format.lower(),
        generate_html_report=not no_html,
        case_sensitive=not case_insensitive,
        ignore_whitespace=ignore_whitespace,
        log_level=log_level.upper()
    )

    # Allow chunk_size override if explicitly provided
    if chunk_size != 100000:  # User specified custom chunk size
        settings.chunk_size = chunk_size

    # Display configuration
    console.print("\n[bold]Configuration:[/bold]")
    console.print(f"  Hardware profile: [cyan]{hardware}[/cyan] ({settings.get_effective_workers()} workers)")
    console.print(f"  Source file:      [blue]{source_file}[/blue]")
    console.print(f"  Comparison file:  [blue]{comparison_file}[/blue]")
    if key:
        console.print(f"  Key column:       [green]{key}[/green]")
    else:
        console.print(f"  Key column:       [yellow]Auto-detect[/yellow]")
    if exclude:
        console.print(f"  Excluding:        [yellow]{exclude}[/yellow]")
    console.print(f"  Output directory: [blue]{output_dir}[/blue]")
    console.print(f"  Output format:    {format}")
    console.print(f"  Chunk size:       {settings.chunk_size:,} rows")
    console.print(f"  HTML report:      {'No' if no_html else 'Yes'}")

    # Estimate file sizes
    source_size_mb = source_file.stat().st_size / (1024 * 1024)
    comparison_size_mb = comparison_file.stat().st_size / (1024 * 1024)

    console.print(f"\n[dim]Source file size: {source_size_mb:.1f} MB[/dim]")
    console.print(f"[dim]Comparison file size: {comparison_size_mb:.1f} MB[/dim]")

    # Large file warning
    total_size_mb = source_size_mb + comparison_size_mb
    if total_size_mb > 500:
        console.print(
            f"\n[yellow]Note: Processing {total_size_mb:.0f} MB of data. "
            f"This may take several minutes...[/yellow]"
        )

    # Create comparer and run
    try:
        comparer = FileComparer(settings)
        success = comparer.compare_files(source_file, comparison_file, key)

        if success:
            console.print("\n[bold green]Comparison completed successfully![/bold green]")
            sys.exit(0)
        else:
            console.print("\n[bold red]Comparison failed![/bold red]")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Comparison cancelled by user.[/yellow]")
        sys.exit(130)

    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == '__main__':
    main()
