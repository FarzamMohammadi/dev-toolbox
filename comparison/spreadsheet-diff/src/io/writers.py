"""
Output writers for comparison results.
Supports CSV, Excel, and HTML formats.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, List
import polars as pl
from rich.console import Console

from ..config.settings import ComparisonSettings, FileFormat


console = Console()


class ResultWriter:
    """
    Write comparison results to various output formats.
    """

    def __init__(self, settings: ComparisonSettings):
        """
        Initialize result writer.

        Args:
            settings: Comparison settings
        """
        self.settings = settings
        self.output_dir = settings.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_differences(
        self,
        differences: pl.DataFrame,
        source_file: str,
        comparison_file: str,
        summary_stats: Optional[dict] = None
    ) -> List[Path]:
        """
        Write comparison differences to output files.

        Args:
            differences: DataFrame containing differences
            source_file: Name of source file
            comparison_file: Name of comparison file
            summary_stats: Optional summary statistics

        Returns:
            List of output file paths
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = []

        if self.settings.output_format in ["csv", "both"]:
            csv_file = self._write_csv(differences, timestamp)
            output_files.append(csv_file)

        if self.settings.output_format in ["excel", "both"]:
            excel_file = self._write_excel(differences, timestamp)
            output_files.append(excel_file)

        if self.settings.generate_html_report:
            html_file = self._write_html_report(
                differences,
                source_file,
                comparison_file,
                timestamp,
                summary_stats
            )
            output_files.append(html_file)

        return output_files

    def _write_csv(self, df: pl.DataFrame, timestamp: str) -> Path:
        """Write differences to CSV file."""
        output_file = self.output_dir / f"differences_{timestamp}.csv"

        df.write_csv(output_file)

        console.print(f"[green]CSV saved:[/green] {output_file}")
        return output_file

    def _write_excel(self, df: pl.DataFrame, timestamp: str) -> Path:
        """Write differences to Excel file with formatting."""
        output_file = self.output_dir / f"differences_{timestamp}.xlsx"

        # Check row limit
        if len(df) > FileFormat.EXCEL_MAX_ROWS:
            console.print(
                f"[yellow]Warning: {len(df):,} differences exceed Excel's "
                f"{FileFormat.EXCEL_MAX_ROWS:,} row limit. "
                f"Truncating to fit Excel format.[/yellow]"
            )
            df = df.head(FileFormat.EXCEL_MAX_ROWS)

        # Write using xlsxwriter for better formatting control
        with pl.Config() as cfg:
            df.write_excel(
                output_file,
                worksheet="Differences",
                autofit=True
            )

        # Apply conditional formatting if possible
        try:
            self._apply_excel_formatting(output_file, df)
        except Exception as e:
            console.print(f"[yellow]Note: Could not apply Excel formatting: {e}[/yellow]")

        console.print(f"[green]Excel saved:[/green] {output_file}")
        return output_file

    def _apply_excel_formatting(self, filepath: Path, df: pl.DataFrame):
        """Apply conditional formatting to Excel file."""
        from openpyxl import load_workbook
        from openpyxl.styles import PatternFill

        wb = load_workbook(filepath)
        ws = wb.active

        # Define fill colors
        source_fill = PatternFill(start_color='FFCDD2', end_color='FFCDD2', fill_type='solid')
        comparison_fill = PatternFill(start_color='C8E6C9', end_color='C8E6C9', fill_type='solid')

        # Find columns (assuming standard naming)
        header_row = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]

        source_col_idx = None
        comparison_col_idx = None

        for idx, header in enumerate(header_row, 1):
            if header and 'SOURCE' in str(header).upper():
                source_col_idx = idx
            elif header and ('COMPARISON' in str(header).upper() or 'NEW' in str(header).upper()):
                comparison_col_idx = idx

        # Apply formatting
        for row_idx in range(2, len(df) + 2):  # Skip header
            if source_col_idx:
                ws.cell(row=row_idx, column=source_col_idx).fill = source_fill
            if comparison_col_idx:
                ws.cell(row=row_idx, column=comparison_col_idx).fill = comparison_fill

        wb.save(filepath)

    def _write_html_report(
        self,
        df: pl.DataFrame,
        source_file: str,
        comparison_file: str,
        timestamp: str,
        summary_stats: Optional[dict] = None
    ) -> Path:
        """Generate interactive HTML report with DataTables."""
        output_file = self.output_dir / f"differences_report_{timestamp}.html"

        # Limit rows for HTML (performance)
        max_html_rows = 50000
        is_truncated = False
        if len(df) > max_html_rows:
            console.print(
                f"[yellow]HTML report limited to {max_html_rows:,} rows "
                f"(file has {len(df):,} differences)[/yellow]"
            )
            df = df.head(max_html_rows)
            is_truncated = True

        # Generate table rows
        table_rows = ""
        for row in df.iter_rows(named=True):
            row_html = "<tr>"
            for value in row.values():
                # Sanitize HTML
                str_value = str(value) if value is not None else ""
                str_value = str_value.replace("<", "&lt;").replace(">", "&gt;")
                row_html += f"<td>{str_value}</td>"
            row_html += "</tr>"
            table_rows += row_html

        # Generate table headers
        table_headers = ""
        for col in df.columns:
            table_headers += f"<th>{col}</th>"

        # Generate stats
        stats_html = ""
        if summary_stats:
            stats_html = f"""
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{summary_stats.get('total_differences', 0):,}</div>
                    <div class="stat-label">Total Differences</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{summary_stats.get('unique_keys', 0):,}</div>
                    <div class="stat-label">Unique Records</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{summary_stats.get('exact_matches', 0):,}</div>
                    <div class="stat-label">Exact Matches (Excluded)</div>
                </div>
            </div>
            """

        truncation_warning = ""
        if is_truncated:
            truncation_warning = f"""
            <div class="warning-box">
                Note: This report shows only the first {max_html_rows:,} differences.
                See CSV/Excel files for complete results.
            </div>
            """

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>File Comparison Report</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .info {{
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            flex: 1;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .warning-box {{
            padding: 15px;
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            margin-bottom: 20px;
            color: #856404;
        }}
        table.dataTable {{
            width: 100% !important;
        }}
        table.dataTable thead th {{
            background: #2c3e50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        table.dataTable tbody td {{
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        .dataTables_wrapper {{
            padding: 20px 0;
        }}
        .dataTables_filter {{
            margin-bottom: 20px;
        }}
        .dataTables_length {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>File Comparison Report</h1>
        <div class="info">
            <strong>Source File:</strong> {source_file}<br>
            <strong>Compared to:</strong> {comparison_file}<br>
            <strong>Generated at:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>

        {stats_html}

        <div class="info" style="margin-top: 15px;">
            <em>💡 Tip: Hold Shift and click column headers to sort by multiple columns</em>
        </div>

        {truncation_warning}

        <table id="diffTable" class="display">
            <thead>
                <tr>{table_headers}</tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>

    <script>
        $(document).ready(function() {{
            $('#diffTable').DataTable({{
                pageLength: 50,
                order: [[0, 'asc'], [1, 'asc']],
                responsive: true
            }});
        }});
    </script>
</body>
</html>
        """

        output_file.write_text(html, encoding='utf-8')
        console.print(f"[green]HTML report saved:[/green] {output_file}")
        return output_file
