"""
Type mapper module - Maps SQL Server data types to placeholder values
"""

from typing import Dict


class TypeMapper:
    """Maps SQL Server data types to appropriate placeholder values"""

    # Type mapping: SQL type keyword -> placeholder value
    TYPE_MAPPINGS: Dict[str, str] = {
        # String types
        'NVARCHAR': "''",
        'VARCHAR': "''",
        'NCHAR': "''",
        'CHAR': "''",
        'TEXT': "''",
        'NTEXT': "''",

        # Numeric types
        'INT': '0',
        'INTEGER': '0',
        'BIGINT': '0',
        'SMALLINT': '0',
        'TINYINT': '0',
        'DECIMAL': '0.0',
        'NUMERIC': '0.0',
        'FLOAT': '0.0',
        'REAL': '0.0',
        'MONEY': '0.0',
        'SMALLMONEY': '0.0',

        # Boolean
        'BIT': '0',

        # Date/Time types
        'DATE': 'GETDATE()',
        'DATETIME': 'GETDATE()',
        'DATETIME2': 'GETDATE()',
        'SMALLDATETIME': 'GETDATE()',
        'TIME': 'GETDATE()',
        'DATETIMEOFFSET': 'SYSDATETIMEOFFSET()',

        # GUID
        'UNIQUEIDENTIFIER': "'00000000-0000-0000-0000-000000000000'",

        # Binary types
        'BINARY': '0x',
        'VARBINARY': '0x',
        'IMAGE': '0x',

        # XML
        'XML': "''",
    }

    @classmethod
    def get_placeholder(cls, sql_type: str) -> str:
        """
        Get placeholder value for a SQL type

        Args:
            sql_type: SQL Server data type (e.g., 'NVARCHAR(100)', 'INT', 'UNIQUEIDENTIFIER')

        Returns:
            Placeholder value as string
        """
        # Extract base type (remove size/precision)
        base_type = sql_type.upper().split('(')[0].strip()

        # Return mapped placeholder or NULL as fallback
        return cls.TYPE_MAPPINGS.get(base_type, 'NULL')

    @classmethod
    def format_declare(cls, param_name: str, sql_type: str, placeholder: str = None) -> str:
        """
        Format a DECLARE statement with placeholder value

        Args:
            param_name: Parameter name (including @)
            sql_type: SQL Server data type
            placeholder: Optional custom placeholder value

        Returns:
            Complete DECLARE statement
        """
        if placeholder is None:
            placeholder = cls.get_placeholder(sql_type)

        return f"DECLARE {param_name} {sql_type} = {placeholder};"
