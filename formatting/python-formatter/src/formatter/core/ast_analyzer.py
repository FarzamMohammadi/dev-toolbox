"""
AST-based analysis for Python code.
Handles import analysis, unused import detection, and code structure parsing.
"""

import ast
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class ImportInfo:
    """Information about an import statement."""

    def __init__(self, name: str, alias: Optional[str] = None, module: Optional[str] = None):
        self.name = name
        self.alias = alias
        self.module = module
        self.line_number = 0
        self.is_from_import = module is not None

    def __repr__(self):
        if self.is_from_import:
            return f"from {self.module} import {self.name}" + (f" as {self.alias}" if self.alias else "")
        return f"import {self.name}" + (f" as {self.alias}" if self.alias else "")

    @property
    def display_name(self) -> str:
        """The name this import is referenced by in the code."""
        return self.alias if self.alias else self.name


class ASTAnalyzer:
    """Analyzes Python code using Abstract Syntax Trees."""

    def __init__(self):
        self.imports: List[ImportInfo] = []
        self.used_names: Set[str] = set()
        self.defined_names: Set[str] = set()

    def analyze_code(self, code: str) -> Dict:
        """
        Analyze Python code and return analysis results.

        Args:
            code: Python source code to analyze

        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                'error': f"Syntax error: {e}",
                'imports': [],
                'unused_imports': [],
                'used_names': set(),
                'issues': []
            }

        self.imports = []
        self.used_names = set()
        self.defined_names = set()

        # First pass: collect imports and definitions
        self._collect_imports_and_definitions(tree)

        # Second pass: collect usage
        self._collect_usage(tree)

        # Analyze unused imports
        unused_imports = self._find_unused_imports()

        # Find common issues
        issues = self._find_issues(tree)

        return {
            'imports': self.imports,
            'unused_imports': unused_imports,
            'used_names': self.used_names,
            'defined_names': self.defined_names,
            'issues': issues
        }

    def _collect_imports_and_definitions(self, tree: ast.AST):
        """Collect import statements and function/class definitions."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_info = ImportInfo(alias.name, alias.asname)
                    import_info.line_number = node.lineno
                    self.imports.append(import_info)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    import_info = ImportInfo(alias.name, alias.asname, module)
                    import_info.line_number = node.lineno
                    self.imports.append(import_info)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.defined_names.add(node.name)

            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.defined_names.add(target.id)

    def _collect_usage(self, tree: ast.AST):
        """Collect all name usage in the code."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                self.used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # For attribute access like 'module.function', track 'module'
                if isinstance(node.value, ast.Name):
                    self.used_names.add(node.value.id)

    def _find_unused_imports(self) -> List[ImportInfo]:
        """Find imports that are not used in the code."""
        unused = []
        for import_info in self.imports:
            display_name = import_info.display_name

            # Skip star imports
            if import_info.name == '*':
                continue

            # Check if the import is used
            if display_name not in self.used_names:
                unused.append(import_info)

        return unused

    def _get_attribute_usage(self) -> Set[str]:
        """Get all attribute usage patterns from the code."""
        # This is a simplified version - in a full implementation,
        # we'd need to track attribute access more carefully
        return set()

    def _find_issues(self, tree: ast.AST) -> List[Dict]:
        """Find common code issues."""
        issues = []

        for node in ast.walk(tree):
            # Check for f-strings without placeholders
            if isinstance(node, ast.JoinedStr) and not node.values:
                issues.append({
                    'code': 'F541',
                    'line': node.lineno,
                    'message': 'f-string is missing placeholders'
                })

            # Check for type comparisons (should use isinstance)
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, (ast.Is, ast.IsNot)):
                        # Check if comparing types
                        if (isinstance(node.left, ast.Call) and
                            isinstance(node.left.func, ast.Name) and
                            node.left.func.id == 'type'):
                            issues.append({
                                'code': 'E721',
                                'line': node.lineno,
                                'message': 'do not compare types, use isinstance()'
                            })

        return issues

    def get_import_groups(self) -> Dict[str, List[ImportInfo]]:
        """Group imports by category (future, stdlib, third-party, etc.)."""
        groups = {
            'future': [],
            'stdlib': [],
            'third_party': [],
            'first_party': [],
            'local': []
        }

        stdlib_modules = self._get_stdlib_modules()

        for import_info in self.imports:
            module_name = import_info.module if import_info.is_from_import else import_info.name
            root_module = module_name.split('.')[0] if module_name else ''

            if module_name and module_name.startswith('__future__'):
                groups['future'].append(import_info)
            elif root_module in stdlib_modules:
                groups['stdlib'].append(import_info)
            elif module_name and ('.' in module_name or module_name.startswith('.')):
                groups['local'].append(import_info)
            else:
                groups['third_party'].append(import_info)

        return groups

    def _get_stdlib_modules(self) -> Set[str]:
        """Get a set of standard library module names."""
        # A subset of Python standard library modules
        # In a full implementation, this could be more comprehensive
        return {
            'os', 'sys', 'json', 'time', 'datetime', 'math', 'random',
            'collections', 'itertools', 'functools', 'operator',
            'pathlib', 'typing', 'dataclasses', 'enum', 'abc',
            'asyncio', 'threading', 'multiprocessing',
            'urllib', 'http', 'email', 'html', 'xml',
            'sqlite3', 'csv', 'configparser', 'logging',
            'unittest', 'doctest', 'argparse', 'shutil',
            'glob', 'fnmatch', 'tempfile', 'gzip', 'zipfile',
            'pickle', 'copy', 'pprint', 'textwrap', 'string',
            'io', 'struct', 'codecs', 'locale', 'calendar'
        }