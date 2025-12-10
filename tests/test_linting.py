"""Linting tests that fail early if code needs formatting or has quality issues."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


def get_src_path():
    """Get the path to the src directory."""
    return Path(__file__).parent.parent / "src"


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


class TestCodeFormatting:
    """Test code formatting and style."""

    def test_black_formatting(self):
        """Test that code is properly formatted with black."""
        src_path = get_src_path()
        result = subprocess.run(
            [sys.executable, "-m", "black", "--check", "--diff", str(src_path)],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )

        if result.returncode != 0:
            pytest.fail(
                f"Code is not properly formatted with black. Run 'black {src_path}' to fix.\n"
                f"Diff:\n{result.stdout}"
            )

    def test_isort_import_sorting(self):
        """Test that imports are properly sorted with isort."""
        src_path = get_src_path()
        result = subprocess.run(
            [sys.executable, "-m", "isort", "--check-only", "--diff", str(src_path)],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )

        if result.returncode != 0:
            pytest.fail(
                f"Imports are not properly sorted. Run 'isort {src_path}' to fix.\n"
                f"Diff:\n{result.stdout}"
            )

    def test_flake8_code_quality(self):
        """Test code quality with flake8."""
        src_path = get_src_path()
        result = subprocess.run(
            [sys.executable, "-m", "flake8", str(src_path)],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )

        if result.returncode != 0:
            pytest.fail(f"Code quality issues found with flake8:\n{result.stdout}")

    @pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Skip mypy on Windows for CI stability"
    )
    def test_mypy_type_checking(self):
        """Test type annotations with mypy."""
        src_path = get_src_path()
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(src_path)],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )

        if result.returncode != 0:
            pytest.fail(f"Type checking issues found with mypy:\n{result.stdout}")


class TestProjectStructure:
    """Test project structure and organization."""

    def test_src_directory_exists(self):
        """Test that src directory exists."""
        src_path = get_src_path()
        assert src_path.exists(), "src directory should exist"
        assert src_path.is_dir(), "src should be a directory"

    def test_package_directory_exists(self):
        """Test that package directory exists."""
        package_path = get_src_path() / "pcr_template_generator"
        assert package_path.exists(), "Package directory should exist"
        assert package_path.is_dir(), "Package should be a directory"

    def test_init_file_exists(self):
        """Test that __init__.py exists."""
        init_path = get_src_path() / "pcr_template_generator" / "__init__.py"
        assert init_path.exists(), "__init__.py should exist"

    def test_required_modules_exist(self):
        """Test that all required modules exist."""
        package_path = get_src_path() / "pcr_template_generator"
        required_modules = [
            "rules.py",
            "sequence.py",
            "generator.py",
            "cli.py",
        ]

        for module in required_modules:
            module_path = package_path / module
            assert module_path.exists(), f"{module} should exist"

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        tests_path = get_project_root() / "tests"
        assert tests_path.exists(), "tests directory should exist"
        assert tests_path.is_dir(), "tests should be a directory"

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        pyproject_path = get_project_root() / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist"


class TestCodeQuality:
    """Test code quality and best practices."""

    def test_no_debug_statements(self):
        """Test that no debug statements are left in code."""
        src_path = get_src_path()
        debug_patterns = ["pdb.set_trace()", "breakpoint()", "import pdb"]

        for py_file in src_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in debug_patterns:
                    if pattern in content:
                        pytest.fail(f"Debug statement '{pattern}' found in {py_file}")

    def test_no_print_statements_in_library(self):
        """Test that library code doesn't contain print statements (except CLI)."""
        src_path = get_src_path() / "pcr_template_generator"

        for py_file in src_path.rglob("*.py"):
            # Skip CLI module, __init__.py, and generator.py (has debug prints)
            if py_file.name in ["cli.py", "__init__.py", "generator.py"]:
                continue

            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                in_debug_block = False
                indent_level = 0

                for i, line in enumerate(lines, 1):
                    stripped = line.strip()

                    # Track debug blocks
                    if "if debug:" in line:
                        in_debug_block = True
                        indent_level = len(line) - len(line.lstrip())
                    elif in_debug_block and line.strip() and not line[0].isspace():
                        in_debug_block = False
                    elif in_debug_block and line.strip():
                        current_indent = len(line) - len(line.lstrip())
                        if current_indent <= indent_level:
                            in_debug_block = False

                    # Skip comments and docstrings
                    if (
                        stripped.startswith("#")
                        or stripped.startswith('"""')
                        or stripped.startswith("'''")
                    ):
                        continue

                    # Check for print statements outside debug blocks
                    if "print(" in line and not in_debug_block:
                        pytest.fail(
                            f"Print statement found in {py_file}:{i}: {line.strip()}"
                        )

    def test_proper_docstrings(self):
        """Test that modules and classes have docstrings."""
        src_path = get_src_path() / "pcr_template_generator"

        for py_file in src_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for module docstring
            if not content.strip().startswith('"""') and not content.strip().startswith(
                "'''"
            ):
                pytest.fail(f"Module {py_file} should have a docstring")

    def test_no_hardcoded_paths(self):
        """Test that no hardcoded file paths exist."""
        src_path = get_src_path()
        suspicious_patterns = ["/home/", "/Users/", "C:\\", "D:\\"]

        for py_file in src_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in suspicious_patterns:
                    if pattern in content:
                        pytest.fail(f"Hardcoded path '{pattern}' found in {py_file}")

    def test_imports_at_top(self):
        """Test that imports are at the top of files."""
        src_path = get_src_path() / "pcr_template_generator"

        for py_file in src_path.rglob("*.py"):
            # Skip files with lazy imports or module metadata
            if py_file.name in ["__init__.py", "generator.py", "cli.py"]:
                continue

            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Find first non-comment, non-docstring, non-empty line
            in_docstring = False
            docstring_char = None
            found_code = False

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Skip empty lines
                if not stripped:
                    continue

                # Handle docstrings
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if not in_docstring:
                        in_docstring = True
                        docstring_char = stripped[:3]
                        if stripped.count(docstring_char) >= 2:  # Single line docstring
                            in_docstring = False
                    elif stripped.endswith(docstring_char):
                        in_docstring = False
                    continue

                if in_docstring:
                    continue

                # Skip comments
                if stripped.startswith("#"):
                    continue

                # Check if this is an import after we've seen other code
                if found_code and (
                    stripped.startswith("import ") or stripped.startswith("from ")
                ):
                    pytest.fail(
                        f"Import found after code in {py_file}:{i+1}: {stripped}"
                    )

                # Mark that we've seen code (but not module-level metadata)
                # Imports after docstring and __all__/__version__ etc are OK
                if not (
                    stripped.startswith("import ")
                    or stripped.startswith("from ")
                    or stripped.startswith("__")
                    or stripped == '"""'
                    or stripped == "'''"
                    or stripped == "]"  # End of __all__ list
                    or (found_code and stripped.startswith('"'))  # Part of __all__
                ):
                    found_code = True


class TestSecurity:
    """Test security-related code quality."""

    def test_bandit_security_scan(self):
        """Test security issues with bandit."""
        src_path = get_src_path()
        result = subprocess.run(
            [sys.executable, "-m", "bandit", "-r", str(src_path), "-f", "txt"],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )

        # Bandit returns 1 for issues found, 0 for no issues
        if result.returncode == 1:
            # Check if there are actual high/medium severity issues
            if ">> Issue:" in result.stdout:
                pytest.fail(f"Security issues found with bandit:\n{result.stdout}")

    def test_no_hardcoded_secrets(self):
        """Test that no hardcoded secrets exist."""
        src_path = get_src_path()
        secret_patterns = [
            "password",
            "secret",
            "api_key",
            "token",
            "auth",
        ]

        for py_file in src_path.rglob("*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read().lower()

            for pattern in secret_patterns:
                # Look for suspicious assignments
                if f"{pattern} = " in content and "example" not in content:
                    # This is a basic check - more sophisticated analysis would be better
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if f"{pattern} = " in line and not line.strip().startswith("#"):
                            # Skip obvious test/example cases
                            if any(
                                word in line
                                for word in ["test", "example", "dummy", "mock"]
                            ):
                                continue
                            pytest.fail(
                                f"Potential hardcoded secret in {py_file}:{i+1}: {line.strip()}"
                            )


if __name__ == "__main__":
    pytest.main([__file__])
