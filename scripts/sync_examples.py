#!/usr/bin/env python3
"""
Sync Examples with pyproject.toml

This script keeps the examples directory synchronized with the main package
configuration, ensuring that dependencies and version information stay current.

Usage:
    python scripts/sync_examples.py
"""

import os
import re
import sys
from pathlib import Path

import toml


def main():
    """Sync examples with pyproject.toml configuration."""
    print("🔄 Syncing examples with pyproject.toml...")

    # Get project root
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"
    examples_dir = project_root / "examples"

    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found at {pyproject_path}")
        sys.exit(1)

    # Load pyproject.toml
    try:
        with open(pyproject_path, "r") as f:
            pyproject_data = toml.load(f)
    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        sys.exit(1)

    # Extract relevant information
    package_info = extract_package_info(pyproject_data)

    # Update examples
    update_requirements_txt(examples_dir, package_info)
    update_example_files(examples_dir, package_info)

    print("✅ Examples synchronized successfully!")


def extract_package_info(pyproject_data):
    """Extract relevant package information from pyproject.toml."""
    poetry_section = pyproject_data.get("tool", {}).get("poetry", {})

    package_info = {
        "name": poetry_section.get("name", "pcr-template-generator"),
        "version": poetry_section.get("version", "1.0.0"),
        "description": poetry_section.get("description", ""),
        "python_requires": poetry_section.get("dependencies", {}).get(
            "python", ">=3.10"
        ),
        "dependencies": {},
        "dev_dependencies": {},
    }

    # Extract main dependencies
    deps = poetry_section.get("dependencies", {})
    for dep_name, dep_spec in deps.items():
        if dep_name != "python":
            package_info["dependencies"][dep_name] = dep_spec

    # Extract dev dependencies
    dev_deps = poetry_section.get("group", {}).get("dev", {}).get("dependencies", {})
    for dep_name, dep_spec in dev_deps.items():
        package_info["dev_dependencies"][dep_name] = dep_spec

    return package_info


def update_requirements_txt(examples_dir, package_info):
    """Update the examples/requirements.txt file."""
    requirements_path = examples_dir / "requirements.txt"

    print(f"📝 Updating {requirements_path.relative_to(examples_dir.parent)}...")

    content = [
        "# PCR Template Generator Examples Requirements",
        "# This file is synced with pyproject.toml dependencies",
        "# Generated automatically - do not edit manually",
        "",
        "# Main package (install from PyPI)",
        f"{package_info['name']}>={package_info['version']}",
        "",
        "# Core dependencies (from pyproject.toml [tool.poetry.dependencies])",
    ]

    # Add main dependencies
    for dep_name, dep_spec in package_info["dependencies"].items():
        if isinstance(dep_spec, str):
            content.append(f"{dep_name}{dep_spec}")
        elif isinstance(dep_spec, dict) and "version" in dep_spec:
            content.append(f"{dep_name}{dep_spec['version']}")

    content.extend(
        [
            "",
            "# Additional dependencies for examples",
            "pandas>=1.5.0,<3.0.0          # For data manipulation examples",
            "seaborn>=0.11.0,<1.0.0         # For advanced plotting",
            "jupyter>=1.0.0,<2.0.0          # For notebook examples",
            "ipywidgets>=8.0.0,<9.0.0       # For interactive notebooks",
            "scipy>=1.9.0,<2.0.0            # For statistical analysis",
            "",
            "# Development/testing (optional)",
        ]
    )

    # Add relevant dev dependencies
    dev_deps_to_include = ["pytest", "black"]
    for dep_name in dev_deps_to_include:
        if dep_name in package_info["dev_dependencies"]:
            dep_spec = package_info["dev_dependencies"][dep_name]
            if isinstance(dep_spec, str):
                content.append(
                    f"{dep_name}{dep_spec}           # For running example tests"
                    if dep_name == "pytest"
                    else f"{dep_name}{dep_spec}          # For code formatting"
                )

    # Write the file
    with open(requirements_path, "w") as f:
        f.write("\n".join(content) + "\n")

    print(f"  ✅ Updated requirements.txt")


def update_example_files(examples_dir, package_info):
    """Update version references in example files."""
    print("📝 Updating version references in example files...")

    # Find all Python files in examples
    python_files = list(examples_dir.rglob("*.py"))

    updated_count = 0

    for py_file in python_files:
        if update_file_version_refs(py_file, package_info):
            updated_count += 1

    print(f"  ✅ Updated {updated_count} Python files")

    # Update shell scripts
    shell_files = list(examples_dir.rglob("*.sh"))

    for sh_file in shell_files:
        if update_shell_file_refs(sh_file, package_info):
            updated_count += 1

    print(f"  ✅ Updated shell script references")


def update_file_version_refs(file_path, package_info):
    """Update version references in a Python file."""
    try:
        with open(file_path, "r") as f:
            content = f.read()

        original_content = content

        # Update version requirements in docstrings
        version_pattern = r"(pcr-template-generator)>=[\d\.]+"
        replacement = f"{package_info['name']}>={package_info['version']}"
        content = re.sub(version_pattern, replacement, content)

        # Update Python version requirements
        python_pattern = r"Python>=[\d\.]+"
        python_req = package_info["python_requires"].replace(">=", "")
        content = re.sub(python_pattern, f"Python>={python_req}", content)

        # Write back if changed
        if content != original_content:
            with open(file_path, "w") as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  ⚠️  Warning: Could not update {file_path}: {e}")
        return False


def update_shell_file_refs(file_path, package_info):
    """Update package references in shell files."""
    try:
        with open(file_path, "r") as f:
            content = f.read()

        original_content = content

        # Update installation commands
        install_pattern = r"pip install pcr-template-generator"
        replacement = f"pip install {package_info['name']}"
        content = re.sub(install_pattern, replacement, content)

        # Write back if changed
        if content != original_content:
            with open(file_path, "w") as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  ⚠️  Warning: Could not update {file_path}: {e}")
        return False


def validate_examples():
    """Validate that examples are properly structured."""
    print("🔍 Validating examples structure...")

    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"

    required_dirs = [
        "basic_usage",
        "advanced_usage",
        "cli_examples",
    ]

    required_files = [
        "README.md",
        "requirements.txt",
        "basic_usage/simple_generation.py",
        "basic_usage/batch_generation.py",
        "basic_usage/custom_parameters.py",
        "cli_examples/cli_basic.sh",
        "cli_examples/cli_batch.sh",
        "cli_examples/cli_analysis.sh",
        "advanced_usage/sequence_analysis.py",
    ]

    # Check directories
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = examples_dir / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)

    # Check files
    missing_files = []
    for file_name in required_files:
        file_path = examples_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)

    # Report results
    if missing_dirs:
        print(f"  ❌ Missing directories: {', '.join(missing_dirs)}")

    if missing_files:
        print(f"  ❌ Missing files: {', '.join(missing_files)}")

    if not missing_dirs and not missing_files:
        print("  ✅ All required examples files and directories present")
        return True

    return False


if __name__ == "__main__":
    main()

    # Also validate structure
    print()
    validate_examples()

    print("\n🎉 Sync completed!")
    print("\nNext steps:")
    print("- Test the examples to ensure they work with current package version")
    print("- Update example content if new features have been added")
    print("- Run this script after any changes to pyproject.toml")
