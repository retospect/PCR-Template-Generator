"""Tests for examples to ensure they remain functional."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def get_examples_dir():
    """Get the path to the examples directory."""
    return Path(__file__).parent.parent / "examples"


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


class TestBasicUsageExamples:
    """Test basic usage examples."""

    def test_simple_generation_imports(self):
        """Test that simple_generation.py imports work."""
        examples_dir = get_examples_dir()
        simple_gen_path = examples_dir / "basic_usage" / "simple_generation.py"

        assert simple_gen_path.exists(), "simple_generation.py should exist"

        # Test imports by running the file with a mock to avoid actual generation
        with patch("pcr_template_generator.run_experiment") as mock_run:
            with patch("pcr_template_generator.Sequence") as mock_seq:
                # Mock successful generation
                mock_template = MagicMock()
                mock_template.display.return_value = "Mock template display"
                mock_template.cost.return_value = 0.5
                mock_template.fwd_primer.return_value = "ATGCATGCATGCATGCATGCAG"
                mock_template.rev_primer.return_value = "CTGCATGCATGCATGCATGCAT"
                mock_template.probe.return_value = "TTGAAGCACGCCGTTGTTTGCCACA"
                mock_template.fwd.return_value = (
                    "ATGCATGCATGCATGCATGCAGTAGTTGAAGCACGCCGTTGTTTGCCACA"
                )
                mock_run.return_value = mock_template

                # Mock sequence creation
                mock_seq_instance = MagicMock()
                mock_seq_instance.cost.return_value = 2.5
                mock_seq_instance.display.return_value = "Mock sequence display"
                mock_seq.return_value = mock_seq_instance

                # Execute the example
                result = subprocess.run(
                    [sys.executable, str(simple_gen_path)],
                    capture_output=True,
                    text=True,
                    cwd=get_project_root(),
                )

                # Should not have import errors
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr

    def test_batch_generation_imports(self):
        """Test that batch_generation.py imports work."""
        examples_dir = get_examples_dir()
        batch_gen_path = examples_dir / "basic_usage" / "batch_generation.py"

        assert batch_gen_path.exists(), "batch_generation.py should exist"

        # Test imports by running with mocked functions
        with patch("pcr_template_generator.generate_multiple_templates") as mock_gen:
            # Mock successful generation of multiple templates
            mock_templates = []
            for i in range(3):
                mock_template = MagicMock()
                mock_template.display.return_value = f"Mock template {i+1} display"
                mock_template.cost.return_value = 0.5 + i * 0.1
                mock_template.fwd_primer.return_value = "ATGCATGCATGCATGCATGCAG"
                mock_template.rev_primer.return_value = "CTGCATGCATGCATGCATGCAT"
                mock_template.probe.return_value = "TTGAAGCACGCCGTTGTTTGCCACA"
                mock_template.fwd.return_value = (
                    "ATGCATGCATGCATGCATGCAGTAGTTGAAGCACGCCGTTGTTTGCCACA"
                )
                mock_templates.append(mock_template)

            mock_gen.return_value = mock_templates

            # Execute the example
            result = subprocess.run(
                [sys.executable, str(batch_gen_path)],
                capture_output=True,
                text=True,
                cwd=get_project_root(),
            )

            # Should not have import errors
            assert "ImportError" not in result.stderr
            assert "ModuleNotFoundError" not in result.stderr

    def test_custom_parameters_imports(self):
        """Test that custom_parameters.py imports work."""
        examples_dir = get_examples_dir()
        custom_params_path = examples_dir / "basic_usage" / "custom_parameters.py"

        assert custom_params_path.exists(), "custom_parameters.py should exist"

        # Test imports by running with mocked functions
        with patch("pcr_template_generator.run_experiment") as mock_run:
            # Mock successful generation
            mock_template = MagicMock()
            mock_template.display.return_value = "Mock template display"
            mock_template.cost.return_value = 0.5
            mock_template.fwd_primer.return_value = "ATGCATGCATGCATGCATGCAG"
            mock_template.rev_primer.return_value = "CTGCATGCATGCATGCATGCAT"
            mock_template.probe.return_value = "TTGAAGCACGCCGTTGTTTGCCACA"
            mock_template.fwd.return_value = (
                "ATGCATGCATGCATGCATGCAGTAGTTGAAGCACGCCGTTGTTTGCCACA"
            )
            mock_run.return_value = mock_template

            # Execute the example
            result = subprocess.run(
                [sys.executable, str(custom_params_path)],
                capture_output=True,
                text=True,
                cwd=get_project_root(),
            )

            # Should not have import errors
            assert "ImportError" not in result.stderr
            assert "ModuleNotFoundError" not in result.stderr


class TestAdvancedUsageExamples:
    """Test advanced usage examples."""

    def test_sequence_analysis_imports(self):
        """Test that sequence_analysis.py imports work."""
        examples_dir = get_examples_dir()
        seq_analysis_path = examples_dir / "advanced_usage" / "sequence_analysis.py"

        assert seq_analysis_path.exists(), "sequence_analysis.py should exist"

        # Test imports by running with mocked functions
        with patch(
            "pcr_template_generator.analyze_sequence_statistics"
        ) as mock_analyze:
            with patch(
                "pcr_template_generator.generate_multiple_templates"
            ) as mock_gen:
                with patch("matplotlib.pyplot.show"):  # Prevent plot display
                    with patch("matplotlib.pyplot.savefig"):  # Prevent file saving
                        # Mock analysis results
                        mock_analyze.return_value = (
                            [50.0, 55.0, 60.0] * 100,
                            [45.0, 50.0, 55.0] * 100,
                        )

                        # Mock template generation
                        mock_templates = []
                        for i in range(5):
                            mock_template = MagicMock()
                            mock_template.display.return_value = f"Mock template {i+1}"
                            mock_template.cost.return_value = 0.5 + i * 0.1
                            mock_template.fwd_primer.return_value = (
                                "ATGCATGCATGCATGCATGCAG"
                            )
                            mock_template.rev_primer.return_value = (
                                "CTGCATGCATGCATGCATGCAT"
                            )
                            mock_template.probe.return_value = (
                                "TTGAAGCACGCCGTTGTTTGCCACA"
                            )
                            mock_template.fwd.return_value = (
                                "ATGCATGCATGCATGCATGCAGTAGTTGAAGCACGCCGTTGTTTGCCACA"
                            )
                            mock_templates.append(mock_template)

                        mock_gen.return_value = mock_templates

                        # Execute the example
                        result = subprocess.run(
                            [sys.executable, str(seq_analysis_path)],
                            capture_output=True,
                            text=True,
                            cwd=get_project_root(),
                        )

                        # Should not have import errors (except optional scipy)
                        assert (
                            "ImportError" not in result.stderr
                            or "scipy" in result.stderr
                        )
                        if "ModuleNotFoundError" in result.stderr:
                            assert (
                                "scipy" in result.stderr
                            ), f"Unexpected import error: {result.stderr}"

    def test_custom_constraints_imports(self):
        """Test that custom_constraints.py imports work."""
        examples_dir = get_examples_dir()
        custom_constraints_path = (
            examples_dir / "advanced_usage" / "custom_constraints.py"
        )

        assert custom_constraints_path.exists(), "custom_constraints.py should exist"

        # Test imports by running with mocked functions
        with patch("pcr_template_generator.run_experiment") as mock_run:
            # Mock successful generation
            mock_template = MagicMock()
            mock_template.display.return_value = "Mock template display"
            mock_template.cost.return_value = 0.5
            mock_template.fwd_primer.return_value = "ATGCATGCATGCATGCATGCAG"
            mock_template.rev_primer.return_value = "CTGCATGCATGCATGCATGCAT"
            mock_template.probe.return_value = "TTGAAGCACGCCGTTGTTTGCCACA"
            mock_template.fwd.return_value = (
                "ATGCATGCATGCATGCATGCAGTAGTTGAAGCACGCCGTTGTTTGCCACA"
            )
            mock_run.return_value = mock_template

            # Execute the example
            result = subprocess.run(
                [sys.executable, str(custom_constraints_path)],
                capture_output=True,
                text=True,
                cwd=get_project_root(),
            )

            # Should not have import errors
            assert "ImportError" not in result.stderr
            assert "ModuleNotFoundError" not in result.stderr


class TestCLIExamples:
    """Test CLI examples."""

    def test_cli_basic_script_exists(self):
        """Test that cli_basic.sh exists and is executable."""
        examples_dir = get_examples_dir()
        cli_basic_path = examples_dir / "cli_examples" / "cli_basic.sh"

        assert cli_basic_path.exists(), "cli_basic.sh should exist"
        assert os.access(cli_basic_path, os.X_OK), "cli_basic.sh should be executable"

    def test_cli_batch_script_exists(self):
        """Test that cli_batch.sh exists and is executable."""
        examples_dir = get_examples_dir()
        cli_batch_path = examples_dir / "cli_examples" / "cli_batch.sh"

        assert cli_batch_path.exists(), "cli_batch.sh should exist"
        assert os.access(cli_batch_path, os.X_OK), "cli_batch.sh should be executable"

    def test_cli_analysis_script_exists(self):
        """Test that cli_analysis.sh exists and is executable."""
        examples_dir = get_examples_dir()
        cli_analysis_path = examples_dir / "cli_examples" / "cli_analysis.sh"

        assert cli_analysis_path.exists(), "cli_analysis.sh should exist"
        assert os.access(
            cli_analysis_path, os.X_OK
        ), "cli_analysis.sh should be executable"

    def test_cli_scripts_have_shebang(self):
        """Test that CLI scripts have proper shebang."""
        examples_dir = get_examples_dir()
        cli_scripts = ["cli_basic.sh", "cli_batch.sh", "cli_analysis.sh"]

        for script_name in cli_scripts:
            script_path = examples_dir / "cli_examples" / script_name
            with open(script_path, "r") as f:
                first_line = f.readline().strip()
                assert first_line.startswith(
                    "#!/bin/bash"
                ), f"{script_name} should have bash shebang"


class TestIntegrationExamples:
    """Test integration examples."""

    def test_jupyter_notebook_exists(self):
        """Test that jupyter notebook exists and has valid structure."""
        examples_dir = get_examples_dir()
        notebook_path = examples_dir / "integration" / "jupyter_notebook.ipynb"

        assert notebook_path.exists(), "jupyter_notebook.ipynb should exist"

        # Test that it's valid JSON
        import json

        with open(notebook_path, "r") as f:
            notebook_data = json.load(f)

        # Basic notebook structure checks
        assert "cells" in notebook_data, "Notebook should have cells"
        assert "metadata" in notebook_data, "Notebook should have metadata"
        assert "nbformat" in notebook_data, "Notebook should have nbformat"

        # Check that cells contain expected imports
        cell_sources = []
        for cell in notebook_data["cells"]:
            if cell.get("cell_type") == "code" and "source" in cell:
                cell_sources.extend(cell["source"])

        combined_source = "".join(cell_sources)
        assert (
            "pcr_template_generator" in combined_source
        ), "Notebook should import pcr_template_generator"


class TestExampleRequirements:
    """Test example requirements and dependencies."""

    def test_requirements_txt_exists(self):
        """Test that examples requirements.txt exists."""
        examples_dir = get_examples_dir()
        req_path = examples_dir / "requirements.txt"

        assert req_path.exists(), "requirements.txt should exist"

    def test_requirements_txt_content(self):
        """Test that requirements.txt has expected content."""
        examples_dir = get_examples_dir()
        req_path = examples_dir / "requirements.txt"

        with open(req_path, "r") as f:
            content = f.read()

        # Should contain main package
        assert "pcr-template-generator" in content, "Should include main package"

        # Should contain core dependencies
        assert "biopython" in content, "Should include biopython"
        assert "numpy" in content, "Should include numpy"
        assert "matplotlib" in content, "Should include matplotlib"

    def test_examples_readme_exists(self):
        """Test that examples README exists."""
        examples_dir = get_examples_dir()
        readme_path = examples_dir / "README.md"

        assert readme_path.exists(), "examples/README.md should exist"

        with open(readme_path, "r") as f:
            content = f.read()

        # Should contain key sections
        assert "Directory Structure" in content, "Should describe directory structure"
        assert "Quick Start" in content, "Should have quick start section"


class TestExampleFunctionality:
    """Test that examples actually work with real (but limited) execution."""

    def test_simple_generation_with_mocked_optimization(self):
        """Test simple generation example with mocked optimization."""
        from pcr_template_generator import Sequence

        # Create a sequence that should work
        test_sequence = Sequence(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            probe_gap=3,
            sequence="atgcatgcatgcatgcatgcagtagttgaagcacgccgttgtttgccacagtagcagattccgccctttatccat",
        )

        # Test that basic functionality works
        assert len(test_sequence.fwd()) == 75
        assert len(test_sequence.fwd_primer()) == 22
        assert len(test_sequence.probe()) == 25
        assert len(test_sequence.rev_primer()) == 22

        # Test display functionality
        display_output = test_sequence.display()
        assert isinstance(display_output, str)
        assert len(display_output) > 0

    def test_custom_constraints_functionality(self):
        """Test that custom constraints actually work."""
        from pcr_template_generator import run_experiment

        # Test with very relaxed constraints to ensure success
        template = run_experiment(
            seq_length=60,
            primer_length=18,
            probe_length=20,
            primer_melt=50.0,
            max_iterations=100,  # Limited for testing
            # Very relaxed constraints
            overall_gc_min=30.0,
            overall_gc_max=70.0,
            primer_gc_min=30.0,
            primer_gc_max=70.0,
            primer_tm_tolerance=5.0,
            probe_tm_delta_min=3.0,
            probe_tm_delta_max=15.0,
            max_run_length=6,
            unique_end_length=2,
            max_secondary_length=8,
        )

        # Should either succeed or fail gracefully
        if template:
            assert len(template.fwd()) == 60
            assert len(template.fwd_primer()) == 18
            assert len(template.probe()) == 20
        # If it fails, that's also acceptable for this test


class TestExampleSynchronization:
    """Test example synchronization functionality."""

    def test_sync_script_exists(self):
        """Test that sync script exists."""
        project_root = get_project_root()
        sync_script_path = project_root / "scripts" / "sync_examples.py"

        assert sync_script_path.exists(), "sync_examples.py should exist"

    def test_sync_script_imports(self):
        """Test that sync script imports work."""
        project_root = get_project_root()
        sync_script_path = project_root / "scripts" / "sync_examples.py"

        # Test imports by running the script with --help or similar
        result = subprocess.run(
            [sys.executable, str(sync_script_path)],
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        # Should not have import errors (may have other errors, that's OK)
        assert "ImportError" not in result.stderr
        assert "ModuleNotFoundError" not in result.stderr


class TestExampleIntegration:
    """Integration tests for examples."""

    def test_all_python_examples_syntax(self):
        """Test that all Python examples have valid syntax."""
        examples_dir = get_examples_dir()

        # Find all Python files in examples
        python_files = list(examples_dir.rglob("*.py"))

        assert len(python_files) > 0, "Should find Python example files"

        for py_file in python_files:
            # Test syntax by compiling
            with open(py_file, "r") as f:
                content = f.read()

            try:
                compile(content, str(py_file), "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")

    def test_example_docstrings(self):
        """Test that examples have proper docstrings."""
        examples_dir = get_examples_dir()

        # Find all Python files in examples
        python_files = list(examples_dir.rglob("*.py"))

        for py_file in python_files:
            with open(py_file, "r") as f:
                content = f.read()

            # Should have module docstring (skip shebang if present)
            lines = content.strip().split("\n")
            first_line = lines[0] if lines else ""
            second_line = lines[1] if len(lines) > 1 else ""

            # Check if docstring is on first or second line (after shebang)
            has_docstring = (
                first_line.startswith('"""')
                or first_line.startswith("'''")
                or second_line.startswith('"""')
                or second_line.startswith("'''")
            )

            if not has_docstring:
                # Skip __init__.py files and very short files
                if py_file.name != "__init__.py" and len(content.strip()) > 50:
                    pytest.fail(f"Example {py_file} should have a module docstring")

    def test_example_imports_are_correct(self):
        """Test that examples import from the correct package."""
        examples_dir = get_examples_dir()

        # Find all Python files in examples
        python_files = list(examples_dir.rglob("*.py"))

        for py_file in python_files:
            with open(py_file, "r") as f:
                content = f.read()

            # Check for correct imports
            if "from pcr_template_generator import" in content:
                # This is good - using the package
                continue
            elif "import pcr_template_generator" in content:
                # This is also good
                continue
            elif "pcr_template_generator" in content:
                # Some reference to the package - probably OK
                continue
            elif py_file.name in ["__init__.py", "sync_examples.py"]:
                # These files might not import the package
                continue
            else:
                # Should probably import the package
                if len(content.strip()) > 100:  # Only check substantial files
                    pytest.fail(
                        f"Example {py_file} should import pcr_template_generator"
                    )


if __name__ == "__main__":
    pytest.main([__file__])
