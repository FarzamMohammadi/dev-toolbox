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
  python convert.py my_procedure.sql -v
        """
    )

    parser.add_argument(
        'input_file',
        help='Path to stored procedure SQL file'
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

    try:
        # Validate input file
        logger.info(f"Reading input file: {args.input_file}")
        input_path = validate_file_path(args.input_file)

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

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = get_output_filename(input_path)

        # Write output
        logger.info(f"Writing output to: {output_path}")
        write_sql_file(output_path, standalone_sql)

        logger.info("[SUCCESS] Conversion completed successfully!")
        logger.info(f"[SUCCESS] Output file: {output_path}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except ValueError as e:
        logger.error(f"Parsing error: {e}")
        return 1

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
