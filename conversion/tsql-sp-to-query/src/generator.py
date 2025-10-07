"""
Generator module - Creates standalone SQL query from parsed SP
"""

from typing import List
from datetime import datetime
from .parser import SPParameter
from .type_mapper import TypeMapper


class SQLGenerator:
    """Generates standalone SQL query from stored procedure components"""

    @classmethod
    def generate(cls, procedure_name: str, parameters: List[SPParameter], body: str) -> str:
        """
        Generate standalone SQL query

        Args:
            procedure_name: Name of the stored procedure
            parameters: List of parsed parameters
            body: Procedure body (without CREATE wrapper)

        Returns:
            Complete standalone SQL query
        """
        sections = [
            cls._generate_header(procedure_name),
            cls._generate_parameter_section(parameters),
            cls._generate_body(body),
            cls._generate_footer()
        ]

        return '\n\n'.join(filter(None, sections))

    @classmethod
    def _generate_header(cls, procedure_name: str) -> str:
        """Generate header comment"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return f"""-- ============================================================================
-- Standalone Readonly Query
-- Generated from: {procedure_name}
-- Generated on: {timestamp}
-- ============================================================================
--
-- INSTRUCTIONS:
-- 1. Edit parameter values in the section below
-- 2. Execute this entire script to get results
-- 3. No stored procedure creation required (readonly access only)
--
-- ============================================================================"""

    @classmethod
    def _generate_parameter_section(cls, parameters: List[SPParameter]) -> str:
        """Generate parameter DECLARE statements"""
        if not parameters:
            return ""

        lines = [
            "-- ============================================================================",
            "-- PARAMETERS - Edit values below as needed",
            "-- ============================================================================",
            ""
        ]

        for param in parameters:
            # Use default value if provided, otherwise generate placeholder
            placeholder = param.default_value if param.default_value else None
            declare_stmt = TypeMapper.format_declare(
                param.name,
                param.data_type,
                placeholder
            )
            lines.append(declare_stmt)

        lines.append("")
        lines.append("-- ============================================================================")
        lines.append("-- PROCEDURE BODY (You can modify below for testing)")
        lines.append("-- ============================================================================")

        return '\n'.join(lines)

    @classmethod
    def _generate_body(cls, body: str) -> str:
        """
        Generate procedure body

        Args:
            body: Original procedure body

        Returns:
            Cleaned procedure body
        """
        # Remove leading/trailing whitespace
        body = body.strip()

        # Remove BEGIN...END wrapper if present (optional, for cleaner output)
        # We'll keep it for now to maintain original structure

        return body

    @classmethod
    def _generate_footer(cls) -> str:
        """Generate footer comment"""
        return """-- ============================================================================
-- END OF QUERY
-- ============================================================================"""
