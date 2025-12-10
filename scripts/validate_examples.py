#!/usr/bin/env python3
"""
Quick validation script for examples.

This script performs basic validation of all examples to ensure they
can be imported and have basic structure without running full execution.

Usage:
    python scripts/validate_examples.py
"""

import ast
import sys
from pathlib import Path


def get_examples_dir():
    """Get the examples directory path."""
    return Path(__file__).parent.parent / "examples"


def validate_python_syntax(file_path):
    """Validate Python file syntax."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_imports(file_path):
    """Check if file imports pcr_template_generator."""
    try:
        with open(file_path, "r") as f:
            content = f.read()

        # Check for package imports
        has_import = (
            "from pcr_template_generator import" in content
            or "import pcr_template_generator" in content
        )

        return has_import
    except Exception:
        return False


def check_docstring(file_path):
    """Check if file has a module docstring."""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Skip very short files and __init__.py
        if len(lines) < 5 or file_path.name == "__init__.py":
            return True

        # Look for docstring in first few lines (after shebang/encoding)
        for i, line in enumerate(lines[:5]):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                return True
            # Skip shebang and encoding lines
            if stripped.startswith("#") and (
                "python" in stripped or "coding" in stripped
            ):
                continue
            # If we hit non-comment, non-empty content without docstring, it's missing
            if stripped and not stripped.startswith("#"):
                return False

        return False
    except Exception:
        return False


def main():
    """Run validation on all examples."""
    examples_dir = get_examples_dir()

    if not examples_dir.exists():
        print("❌ Examples directory not found!")
        sys.exit(1)

    print("🔍 Validating examples...")
    print("=" * 50)

    # Find all Python files
    python_files = list(examples_dir.rglob("*.py"))

    if not python_files:
        print("❌ No Python files found in examples!")
        sys.exit(1)

    print(f"Found {len(python_files)} Python files")
    print()

    errors = []
    warnings = []

    for py_file in python_files:
        rel_path = py_file.relative_to(examples_dir)
        print(f"Checking {rel_path}...")

        # Check syntax
        is_valid, error = validate_python_syntax(py_file)
        if not is_valid:
            errors.append(f"❌ {rel_path}: Syntax error - {error}")
            continue

        # Check imports (skip __init__.py and sync script)
        if py_file.name not in ["__init__.py"] and "sync_examples.py" not in str(
            py_file
        ):
            has_import = check_imports(py_file)
            if not has_import:
                warnings.append(
                    f"⚠️  {rel_path}: No pcr_template_generator import found"
                )

        # Check docstring
        has_docstring = check_docstring(py_file)
        if not has_docstring:
            warnings.append(f"⚠️  {rel_path}: Missing module docstring")

        print(f"  ✅ {rel_path}: Syntax OK")

    print()
    print("=" * 50)

    # Report results
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"  {error}")
        print()

    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    # Check required files
    required_files = [
        "README.md",
        "requirements.txt",
        "basic_usage/simple_generation.py",
        "basic_usage/batch_generation.py",
        "basic_usage/custom_parameters.py",
        "advanced_usage/sequence_analysis.py",
        "advanced_usage/custom_constraints.py",
        "cli_examples/cli_basic.sh",
        "cli_examples/cli_batch.sh",
        "cli_examples/cli_analysis.sh",
        "integration/jupyter_notebook.ipynb",
    ]

    missing_files = []
    for req_file in required_files:
        file_path = examples_dir / req_file
        if not file_path.exists():
            missing_files.append(req_file)

    if missing_files:
        print("❌ MISSING REQUIRED FILES:")
        for missing in missing_files:
            print(f"  {missing}")
        print()

    # Summary
    total_files = len(python_files)
    error_count = len(errors)
    warning_count = len(warnings)
    missing_count = len(missing_files)

    print("📊 VALIDATION SUMMARY:")
    print(f"  Total Python files: {total_files}")
    print(f"  Syntax errors: {error_count}")
    print(f"  Warnings: {warning_count}")
    print(f"  Missing files: {missing_count}")

    if error_count == 0 and missing_count == 0:
        print("\n✅ All examples passed validation!")
        if warning_count > 0:
            print(f"   ({warning_count} warnings - consider addressing)")
        return 0
    else:
        print(
            f"\n❌ Validation failed: {error_count} errors, {missing_count} missing files"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
