# T-SQL Stored Procedure to Query Converter

Converts T-SQL stored procedures to standalone executable queries for testing in readonly environments.

## Supported Files

- **SQL Server (T-SQL)** `.sql` files containing `CREATE OR ALTER PROCEDURE` statements
- **NOT supported:** PostgreSQL, MySQL, Oracle, SQLite (different stored procedure syntax)

## Usage

```bash
# Single file
python convert.py <input-file.sql>

# Multiple files
python convert.py file1.sql file2.sql file3.sql

# Batch convert with wildcards
python convert.py *.sql
```

### Options

- `-o, --output <file>` - Specify output file (single file only, default: `<input>_READONLY.sql`)
- `-v, --verbose` - Enable verbose logging

### Examples

```bash
# Single file conversion
python convert.py my_procedure.sql

# Custom output file (single file only)
python convert.py my_procedure.sql -o test_query.sql

# Multiple files
python convert.py sp1.sql sp2.sql sp3.sql

# Batch convert all procedures
python convert.py *.sql

# Verbose mode
python convert.py *.sql -v
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
