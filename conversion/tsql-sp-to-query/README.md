# T-SQL Stored Procedure to Query Converter

Converts T-SQL stored procedures to standalone executable queries for testing in readonly environments.

## Supported Files

- **SQL Server (T-SQL)** `.sql` files containing `CREATE OR ALTER PROCEDURE` statements
- **NOT supported:** PostgreSQL, MySQL, Oracle, SQLite (different stored procedure syntax)

## Usage

```bash
python convert.py <input-file.sql>
```

### Options

- `-o, --output <file>` - Specify output file (default: `<input>_READONLY.sql`)
- `-v, --verbose` - Enable verbose logging

### Examples

```bash
# Basic conversion
python convert.py ../my_sp.sql

# Custom output file
python convert.py my_procedure.sql -o test_query.sql

# Verbose mode
python convert.py my_procedure.sql -v
```

## Output

Generates a standalone SQL query file with:

1. **Header** - Metadata and instructions
2. **Parameters** - `DECLARE` statements with editable placeholder values
3. **Body** - Original procedure logic (without `CREATE PROCEDURE` wrapper)
4. **Footer** - End marker

You can then:
- Edit parameter values at the top
- Modify query logic for testing
- Execute entire script in SSMS or any SQL client
- No `CREATE/ALTER` permissions required (readonly access only)

## Requirements

- Python 3.8+ (no external packages required)
