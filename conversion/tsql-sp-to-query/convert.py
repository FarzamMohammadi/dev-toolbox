#!/usr/bin/env python3
"""
T-SQL Stored Procedure to Query Converter
Converts T-SQL stored procedures to standalone executable queries
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.parser import SPParser
from src.generator import SQLGenerator
from src.utils import (
    setup_logging,
    validate_file_path,
    read_sql_file,
    write_sql_file,
    get_output_filename
)


def main():
    """Main entry point for the converter"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Convert T-SQL stored procedures to standalone readonly queries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert.py my_procedure.sql
  python convert.py my_procedure.sql -o output.sql
  python convert.py file1.sql file2.sql file3.sql
  python convert.py *.sql
  python convert.py *.sql -v
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        help='Path(s) to stored procedure SQL file(s)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: <input>_READONLY.sql)',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging(args.verbose)

    # Track results
    total_files = len(args.input_files)
    success_count = 0
    error_count = 0
    errors = []

    # Process each file
    for idx, input_file in enumerate(args.input_files, 1):
        try:
            # Show progress
            if total_files > 1:
                logger.info(f"\n[{idx}/{total_files}] Processing: {input_file}")
            else:
                logger.info(f"Reading input file: {input_file}")

            # Validate input file
            input_path = validate_file_path(input_file)

            # Read SQL content
            sql_content = read_sql_file(input_path)
            logger.debug(f"Read {len(sql_content)} characters from input file")

            # Parse stored procedure
            logger.info("Parsing stored procedure...")
            parameters, body = SPParser.parse(sql_content)
            procedure_name = SPParser.get_procedure_name(sql_content)

            logger.info(f"Found procedure: {procedure_name}")
            logger.info(f"Extracted {len(parameters)} parameter(s)")

            if args.verbose:
                for param in parameters:
                    default_info = f" = {param.default_value}" if param.default_value else ""
                    logger.debug(f"  {param.name} {param.data_type}{default_info}")

            # Generate standalone query
            logger.info("Generating standalone query...")
            standalone_sql = SQLGenerator.generate(procedure_name, parameters, body)

            # Determine output path (ignore -o for multiple files)
            if args.output and total_files == 1:
                output_path = Path(args.output)
            else:
                output_path = get_output_filename(input_path)

            # Write output
            logger.info(f"Writing output to: {output_path}")
            write_sql_file(output_path, standalone_sql)

            logger.info("[SUCCESS] Conversion completed!")
            success_count += 1

        except FileNotFoundError as e:
            logger.error(f"[ERROR] File not found: {e}")
            error_count += 1
            errors.append((input_file, str(e)))

        except ValueError as e:
            logger.error(f"[ERROR] Parsing error: {e}")
            error_count += 1
            errors.append((input_file, str(e)))

        except Exception as e:
            logger.error(f"[ERROR] Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            error_count += 1
            errors.append((input_file, str(e)))

    # Show summary for multiple files
    if total_files > 1:
        logger.info(f"\n{'='*60}")
        logger.info(f"SUMMARY: Converted {success_count}/{total_files} files successfully")
        if error_count > 0:
            logger.info(f"Errors: {error_count}")
            if not args.verbose:
                logger.info("Run with -v to see detailed errors")
        logger.info(f"{'='*60}")

    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
