"""
Parser module - Extracts stored procedure parameters and body
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SPParameter:
    """Represents a stored procedure parameter"""
    name: str  # Including @
    data_type: str  # e.g., 'NVARCHAR(10)', 'UNIQUEIDENTIFIER'
    default_value: Optional[str] = None  # If parameter has default value


class SPParser:
    """Parses SQL Server stored procedure definitions"""

    # Regex to match CREATE/ALTER PROCEDURE
    PROC_HEADER_PATTERN = re.compile(
        r'^\s*CREATE\s+(?:OR\s+)?ALTER\s+PROCEDURE\s+(\[?[^\s\]]+\]?)\.?(\[?[^\s\]]+\]?)',
        re.IGNORECASE | re.MULTILINE
    )

    # Regex to match parameters (handles multi-line, optional defaults)
    # Matches: @ParamName DataType(size) = default,
    PARAM_PATTERN = re.compile(
        r'(@\w+)\s+([A-Z0-9_]+(?:\s*\([^)]+\))?)\s*(?:=\s*([^\s,]+))?',
        re.IGNORECASE | re.DOTALL
    )

    # Regex to find AS keyword marking start of procedure body
    AS_KEYWORD_PATTERN = re.compile(r'\bAS\b', re.IGNORECASE)

    @classmethod
    def parse(cls, sql_content: str) -> Tuple[List[SPParameter], str]:
        """
        Parse stored procedure to extract parameters and body

        Args:
            sql_content: Full SQL stored procedure text

        Returns:
            Tuple of (parameters list, procedure body without CREATE wrapper)

        Raises:
            ValueError: If not a valid stored procedure
        """
        # Validate it's a stored procedure
        if not cls.PROC_HEADER_PATTERN.search(sql_content):
            raise ValueError("Not a valid CREATE OR ALTER PROCEDURE statement")

        # Extract parameters and body
        parameters = cls._extract_parameters(sql_content)
        body = cls._extract_body(sql_content)

        return parameters, body

    @classmethod
    def _extract_parameters(cls, sql_content: str) -> List[SPParameter]:
        """
        Extract parameters from stored procedure

        Args:
            sql_content: SQL content

        Returns:
            List of SPParameter objects
        """
        parameters = []

        # Find the section between procedure name and AS keyword
        as_match = cls.AS_KEYWORD_PATTERN.search(sql_content)
        if not as_match:
            return parameters

        # Get text from start to AS keyword
        header_section = sql_content[:as_match.start()]

        # Find where parameters start (after procedure name)
        proc_match = cls.PROC_HEADER_PATTERN.search(header_section)
        if not proc_match:
            return parameters

        # Extract parameter section
        param_section = header_section[proc_match.end():]

        # Parse individual parameters
        for match in cls.PARAM_PATTERN.finditer(param_section):
            param_name = match.group(1)
            data_type = match.group(2).strip()
            default_value = match.group(3).strip() if match.group(3) else None

            parameters.append(SPParameter(
                name=param_name,
                data_type=data_type,
                default_value=default_value
            ))

        return parameters

    @classmethod
    def _extract_body(cls, sql_content: str) -> str:
        """
        Extract procedure body (everything after AS keyword)

        Args:
            sql_content: SQL content

        Returns:
            Procedure body without CREATE wrapper
        """
        # Find AS keyword
        as_match = cls.AS_KEYWORD_PATTERN.search(sql_content)
        if not as_match:
            raise ValueError("Could not find AS keyword in stored procedure")

        # Get everything after AS
        body = sql_content[as_match.end():].strip()

        return body

    @classmethod
    def get_procedure_name(cls, sql_content: str) -> str:
        """
        Extract stored procedure name

        Args:
            sql_content: SQL content

        Returns:
            Procedure name (without schema)
        """
        match = cls.PROC_HEADER_PATTERN.search(sql_content)
        if not match:
            return "unknown_procedure"

        # Return procedure name (second group), remove brackets if present
        proc_name = match.group(2).strip('[]')
        return proc_name
