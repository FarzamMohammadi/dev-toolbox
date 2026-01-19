#!/usr/bin/env python3
"""
Python AST Pattern Analyzer
============================
Analyzes Python code to detect common design patterns and architectural elements.

Detects:
- Singleton pattern
- Factory pattern
- Decorator usage
- Entry points (if __name__ == "__main__")
- Class hierarchies
- Abstract base classes
- Dataclasses
- Protocol/Interface definitions

Usage:
    python analyze.py <target_repo> <output_dir>
"""

import ast
import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional
from collections import defaultdict


@dataclass
class PatternMatch:
    """Represents a detected pattern in the codebase."""
    pattern_type: str
    file_path: str
    line_number: int
    name: str
    details: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result for a codebase."""
    target_repo: str
    files_analyzed: int
    patterns: List[PatternMatch] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    class_hierarchy: Dict[str, List[str]] = field(default_factory=dict)
    decorators_used: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    imports_summary: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


class PatternVisitor(ast.NodeVisitor):
    """AST visitor that detects common patterns."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.patterns: List[PatternMatch] = []
        self.entry_points: List[str] = []
        self.class_hierarchy: Dict[str, List[str]] = {}
        self.decorators_used: Dict[str, int] = defaultdict(int)
        self.imports: Dict[str, int] = defaultdict(int)
        self._current_class: Optional[str] = None

    def visit_ClassDef(self, node: ast.ClassDef):
        """Analyze class definitions for patterns."""
        class_name = node.name

        # Track class hierarchy
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{self._get_attr_name(base)}")

        if bases:
            self.class_hierarchy[class_name] = bases

        # Check for ABC (Abstract Base Class)
        if "ABC" in bases or "abc.ABC" in bases:
            self.patterns.append(PatternMatch(
                pattern_type="abstract_base_class",
                file_path=self.file_path,
                line_number=node.lineno,
                name=class_name,
                details="Inherits from ABC"
            ))

        # Check for Protocol (typing.Protocol)
        if "Protocol" in bases or "typing.Protocol" in bases:
            self.patterns.append(PatternMatch(
                pattern_type="protocol",
                file_path=self.file_path,
                line_number=node.lineno,
                name=class_name,
                details="Defines a Protocol interface"
            ))

        # Check decorators
        for decorator in node.decorator_list:
            dec_name = self._get_decorator_name(decorator)
            self.decorators_used[dec_name] += 1

            # Detect dataclass
            if dec_name in ("dataclass", "dataclasses.dataclass"):
                self.patterns.append(PatternMatch(
                    pattern_type="dataclass",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    name=class_name,
                    details="@dataclass decorator"
                ))

        # Check for Singleton pattern (class with _instance attribute and __new__)
        has_instance = False
        has_new = False
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "_instance":
                        has_instance = True
            elif isinstance(item, ast.FunctionDef) and item.name == "__new__":
                has_new = True

        if has_instance and has_new:
            self.patterns.append(PatternMatch(
                pattern_type="singleton",
                file_path=self.file_path,
                line_number=node.lineno,
                name=class_name,
                details="Uses _instance and __new__"
            ))

        # Check for Factory pattern (method returning instances)
        self._current_class = class_name
        self.generic_visit(node)
        self._current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Analyze function definitions."""
        # Check for factory methods
        if node.name.startswith("create_") or node.name.startswith("make_") or node.name == "factory":
            self.patterns.append(PatternMatch(
                pattern_type="factory_method",
                file_path=self.file_path,
                line_number=node.lineno,
                name=node.name,
                details=f"In class {self._current_class}" if self._current_class else "Module-level"
            ))

        # Track decorators
        for decorator in node.decorator_list:
            dec_name = self._get_decorator_name(decorator)
            self.decorators_used[dec_name] += 1

            # Common decorator patterns
            if dec_name in ("property", "staticmethod", "classmethod",
                          "abstractmethod", "abc.abstractmethod"):
                pass  # Just count them
            elif dec_name.startswith("app.") or dec_name.startswith("router."):
                self.patterns.append(PatternMatch(
                    pattern_type="route_handler",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    name=node.name,
                    details=f"@{dec_name}"
                ))

        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        """Detect entry points."""
        # Check for if __name__ == "__main__":
        if isinstance(node.test, ast.Compare):
            if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
                left = node.test.left
                if isinstance(left, ast.Name) and left.id == "__name__":
                    comparators = node.test.comparators
                    if len(comparators) == 1:
                        comp = comparators[0]
                        if isinstance(comp, ast.Constant) and comp.value == "__main__":
                            self.entry_points.append(self.file_path)
                            self.patterns.append(PatternMatch(
                                pattern_type="entry_point",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                name="__main__",
                                details="Script entry point"
                            ))

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """Track imports."""
        for alias in node.names:
            module = alias.name.split('.')[0]
            self.imports[module] += 1

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports."""
        if node.module:
            module = node.module.split('.')[0]
            self.imports[module] += 1

    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return self._get_attr_name(decorator)
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return "unknown"

    def _get_attr_name(self, node: ast.Attribute) -> str:
        """Get full attribute name (e.g., 'module.Class')."""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return '.'.join(reversed(parts))


def analyze_file(file_path: Path) -> Optional[PatternVisitor]:
    """Analyze a single Python file."""
    try:
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source, filename=str(file_path))
        visitor = PatternVisitor(str(file_path))
        visitor.visit(tree)
        return visitor
    except SyntaxError:
        print(f"  [WARN] Syntax error in {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [WARN] Error analyzing {file_path}: {e}", file=sys.stderr)
        return None


def analyze_repository(target_repo: Path, output_dir: Path) -> AnalysisResult:
    """Analyze all Python files in a repository."""
    result = AnalysisResult(
        target_repo=str(target_repo),
        files_analyzed=0,
        class_hierarchy={},
        decorators_used=defaultdict(int),
        imports_summary=defaultdict(int)
    )

    # Find all Python files
    python_files = list(target_repo.rglob("*.py"))

    # Filter out common non-source directories
    exclude_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__',
                   'build', 'dist', '.eggs', '.tox', 'site-packages'}

    python_files = [
        f for f in python_files
        if not any(excluded in f.parts for excluded in exclude_dirs)
    ]

    print(f"Analyzing {len(python_files)} Python files...")

    for file_path in python_files:
        visitor = analyze_file(file_path)
        if visitor:
            result.files_analyzed += 1
            result.patterns.extend(visitor.patterns)
            result.entry_points.extend(visitor.entry_points)
            result.class_hierarchy.update(visitor.class_hierarchy)

            for dec, count in visitor.decorators_used.items():
                result.decorators_used[dec] += count
            for imp, count in visitor.imports.items():
                result.imports_summary[imp] += count

    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <target_repo> [output_dir]")
        sys.exit(1)

    target_repo = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("./output")

    if not target_repo.exists():
        print(f"Error: Target repository not found: {target_repo}")
        sys.exit(1)

    python_output = output_dir / "python"
    python_output.mkdir(parents=True, exist_ok=True)

    print()
    print("Python AST Pattern Analyzer")
    print("============================")
    print()
    print(f"Target: {target_repo}")
    print(f"Output: {python_output}")
    print()

    result = analyze_repository(target_repo, output_dir)

    # Convert to JSON-serializable format
    output_data = {
        "target_repo": result.target_repo,
        "files_analyzed": result.files_analyzed,
        "patterns": [asdict(p) for p in result.patterns],
        "entry_points": result.entry_points,
        "class_hierarchy": result.class_hierarchy,
        "decorators_used": dict(result.decorators_used),
        "imports_summary": dict(result.imports_summary)
    }

    # Write JSON output
    output_file = python_output / "patterns.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    # Print summary
    print()
    print("Pattern Summary:")
    print("-" * 40)

    pattern_counts = defaultdict(int)
    for pattern in result.patterns:
        pattern_counts[pattern.pattern_type] += 1

    for pattern_type, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
        print(f"  {pattern_type}: {count}")

    print()
    print(f"Entry points found: {len(result.entry_points)}")
    print(f"Classes with inheritance: {len(result.class_hierarchy)}")
    print(f"Unique decorators used: {len(result.decorators_used)}")

    # Top decorators
    if result.decorators_used:
        print()
        print("Top decorators:")
        for dec, count in sorted(result.decorators_used.items(), key=lambda x: -x[1])[:10]:
            print(f"  @{dec}: {count}")

    # Top imports
    if result.imports_summary:
        print()
        print("Top imports:")
        for imp, count in sorted(result.imports_summary.items(), key=lambda x: -x[1])[:10]:
            print(f"  {imp}: {count}")

    print()
    print(f"[OK] Analysis complete: {output_file}")
    print()


if __name__ == "__main__":
    main()
