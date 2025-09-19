"""
Core code formatting functionality.
Handles import sorting, unused import removal, and basic code formatting.
"""

import re
from typing import List, Optional, Union
from pathlib import Path

from .ast_analyzer import ASTAnalyzer, ImportInfo
from .config import FormatterConfig


class CodeFormatter:
    """Main code formatting class."""

    def __init__(self, config: FormatterConfig):
        self.config = config
        self.analyzer = ASTAnalyzer()

    def format_code(self, code: str, file_path: Optional[Union[str, Path]] = None) -> str:
        """
        Format Python code according to configuration.

        Args:
            code: Python source code to format
            file_path: Optional file path for context

        Returns:
            Formatted Python code
        """
        # Analyze the code
        analysis = self.analyzer.analyze_code(code)

        if 'error' in analysis:
            # Return original code if there are syntax errors
            return code

        # Split code into lines for processing
        lines = code.splitlines(keepends=True)

        # Remove unused imports (unless it's __init__.py)
        used_imports = analysis['imports']
        if file_path:
            path_obj = Path(file_path) if isinstance(file_path, str) else file_path
            if not self.config.should_allow_unused_imports(path_obj):
                lines = self._remove_unused_imports(lines, analysis['unused_imports'])
                # Filter imports list to only include used imports
                unused_lines = {imp.line_number for imp in analysis['unused_imports']}
                used_imports = [imp for imp in analysis['imports'] if imp.line_number not in unused_lines]

        # Sort imports (only the used ones)
        lines = self._sort_imports(lines, used_imports)

        # Basic formatting
        lines = self._format_lines(lines)

        return ''.join(lines)

    def _remove_unused_imports(self, lines: List[str], unused_imports: List[ImportInfo]) -> List[str]:
        """Remove unused import statements."""
        if not unused_imports:
            return lines

        # Get line numbers of unused imports (1-indexed)
        unused_lines = {imp.line_number for imp in unused_imports}

        # Filter out unused import lines
        filtered_lines = []
        for i, line in enumerate(lines, 1):
            if i not in unused_lines:
                filtered_lines.append(line)

        return filtered_lines

    def _sort_imports(self, lines: List[str], imports: List[ImportInfo]) -> List[str]:
        """Sort import statements according to Google style."""
        if not imports:
            return lines

        # Find import section boundaries
        import_start, import_end = self._find_import_section(lines, imports)

        if import_start == -1:
            return lines

        # Extract non-import parts
        before_imports = lines[:import_start]
        after_imports = lines[import_end:]

        # Group imports
        groups = self.analyzer.get_import_groups()

        # Generate sorted import lines
        sorted_import_lines = []
        for section in self.config.import_sections:
            section_key = section.lower().replace('folder', '')
            if section_key == 'localfolder':
                section_key = 'local'

            if section_key in groups and groups[section_key]:
                # Sort imports within the section
                section_imports = sorted(groups[section_key], key=lambda x: x.name.lower())

                for imp in section_imports:
                    sorted_import_lines.append(str(imp) + '\n')

                # Add blank line after section (except for the last section)
                if section_key != 'local' and sorted_import_lines:
                    sorted_import_lines.append('\n')

        # Combine all parts
        return before_imports + sorted_import_lines + after_imports

    def _find_import_section(self, lines: List[str], imports: List[ImportInfo]) -> tuple[int, int]:
        """Find the start and end of the import section."""
        if not imports:
            return -1, -1

        # Find first and last import lines
        import_lines = {imp.line_number for imp in imports}
        first_import = min(import_lines)
        last_import = max(import_lines)

        # Convert to 0-indexed
        start_idx = first_import - 1
        end_idx = last_import

        # Extend to include any blank lines or comments between imports
        while end_idx < len(lines) and (
            lines[end_idx].strip() == '' or
            lines[end_idx].strip().startswith('#')
        ):
            end_idx += 1

        return start_idx, end_idx

    def _format_lines(self, lines: List[str]) -> List[str]:
        """Apply basic formatting to code lines."""
        formatted_lines = []

        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()

            # Ensure proper line endings
            if line:
                formatted_lines.append(line + '\n')
            else:
                formatted_lines.append('\n')

        # Ensure file ends with newline
        if formatted_lines and not formatted_lines[-1].endswith('\n'):
            formatted_lines[-1] += '\n'

        return self._fix_line_length(formatted_lines)

    def _fix_line_length(self, lines: List[str]) -> List[str]:
        """Fix lines that exceed maximum line length."""
        fixed_lines = []

        for line in lines:
            if len(line.rstrip()) <= self.config.max_line_length:
                fixed_lines.append(line)
            else:
                # Basic line breaking for long lines
                # This is a simplified version - a full formatter would handle this more sophisticatedly
                fixed_lines.extend(self._break_long_line(line))

        return fixed_lines

    def _break_long_line(self, line: str) -> List[str]:
        """Break a long line into multiple lines."""
        # This is a very basic implementation
        # A full formatter would need to understand Python syntax better

        stripped = line.rstrip()
        if len(stripped) <= self.config.max_line_length:
            return [line]

        # Try to break at logical points
        break_points = [', ', ' and ', ' or ', ' + ', ' - ', ' * ', ' / ']

        for break_point in break_points:
            if break_point in stripped:
                parts = stripped.split(break_point)
                if len(parts) > 1:
                    # Reconstruct with line breaks
                    result = []
                    current_line = parts[0]

                    for part in parts[1:]:
                        test_line = current_line + break_point + part
                        if len(test_line) <= self.config.max_line_length:
                            current_line = test_line
                        else:
                            result.append(current_line + break_point.rstrip() + '\n')
                            current_line = ' ' * self.config.indent_size + part.lstrip()

                    result.append(current_line + '\n')
                    return result

        # Fallback: just return the original line
        return [line]

    def check_code(self, code: str) -> List[dict]:
        """
        Check code for issues without modifying it.

        Args:
            code: Python source code to check

        Returns:
            List of issues found
        """
        analysis = self.analyzer.analyze_code(code)

        if 'error' in analysis:
            return [{'code': 'E999', 'line': 1, 'message': analysis['error']}]

        issues = analysis.get('issues', [])

        # Add unused import warnings
        for unused_import in analysis.get('unused_imports', []):
            issues.append({
                'code': 'F401',
                'line': unused_import.line_number,
                'message': f"'{unused_import.display_name}' imported but unused"
            })

        return issues