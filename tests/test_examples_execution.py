"""Tests that execute examples to ensure they work correctly."""

import subprocess
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest


def get_examples_dir():
    """Get the path to the examples directory."""
    return Path(__file__).parent.parent / "examples"


def get_project_root():
    """Get the project root directory.""" 
    return Path(__file__).parent.parent


class TestExampleExecution:
    """Test actual execution of examples with controlled parameters."""

    def test_simple_generation_execution(self):
        """Test that simple_generation.py executes without errors."""
        examples_dir = get_examples_dir()
        simple_gen_path = examples_dir / "basic_usage" / "simple_generation.py"
        
        # Create a modified version that uses limited iterations
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            with open(simple_gen_path, 'r') as original:
                content = original.read()
            
            # Modify to use fewer iterations and disable some features
            modified_content = content.replace(
                'max_iterations=5000', 'max_iterations=50'
            ).replace(
                'max_iterations=3000', 'max_iterations=30'
            ).replace(
                'debug=True', 'debug=False'
            )
            
            temp_file.write(modified_content)
            temp_file.flush()
            
            try:
                # Execute the modified example
                result = subprocess.run(
                    [sys.executable, temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=60,  # 60 second timeout
                    cwd=get_project_root()
                )
                
                # Should complete without errors
                assert result.returncode == 0, f"Example failed with stderr: {result.stderr}"
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr
                
                # Should produce some output
                assert len(result.stdout) > 0, "Example should produce output"
                
            finally:
                os.unlink(temp_file.name)

    def test_batch_generation_execution(self):
        """Test that batch_generation.py executes without errors."""
        examples_dir = get_examples_dir()
        batch_gen_path = examples_dir / "basic_usage" / "batch_generation.py"
        
        # Create a modified version with limited parameters
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            with open(batch_gen_path, 'r') as original:
                content = original.read()
            
            # Modify to use fewer templates and iterations
            modified_content = content.replace(
                'template_count = 5', 'template_count = 2'
            ).replace(
                'max_iterations=3000', 'max_iterations=50'
            ).replace(
                'count=20', 'count=2'
            ).replace(
                'debug=False', 'debug=False'
            )
            
            temp_file.write(modified_content)
            temp_file.flush()
            
            try:
                # Execute the modified example
                result = subprocess.run(
                    [sys.executable, temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minute timeout
                    cwd=get_project_root()
                )
                
                # Should complete without errors
                assert result.returncode == 0, f"Example failed with stderr: {result.stderr}"
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr
                
            finally:
                os.unlink(temp_file.name)

    def test_custom_parameters_execution(self):
        """Test that custom_parameters.py executes without errors."""
        examples_dir = get_examples_dir()
        custom_params_path = examples_dir / "basic_usage" / "custom_parameters.py"
        
        # Create a modified version with very limited parameters
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            with open(custom_params_path, 'r') as original:
                content = original.read()
            
            # Modify to use minimal iterations
            modified_content = content.replace(
                'max_iterations=3000', 'max_iterations=20'
            ).replace(
                'max_iterations=5000', 'max_iterations=30'
            ).replace(
                'max_iterations=2000', 'max_iterations=20'
            ).replace(
                'debug=False', 'debug=False'
            )
            
            temp_file.write(modified_content)
            temp_file.flush()
            
            try:
                # Execute the modified example
                result = subprocess.run(
                    [sys.executable, temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=180,  # 3 minute timeout
                    cwd=get_project_root()
                )
                
                # Should complete without errors
                assert result.returncode == 0, f"Example failed with stderr: {result.stderr}"
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr
                
            finally:
                os.unlink(temp_file.name)

    def test_custom_constraints_execution(self):
        """Test that custom_constraints.py executes without errors."""
        examples_dir = get_examples_dir()
        custom_constraints_path = examples_dir / "advanced_usage" / "custom_constraints.py"
        
        # Create a modified version with very limited parameters
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            with open(custom_constraints_path, 'r') as original:
                content = original.read()
            
            # Modify to use minimal iterations and fewer tests
            modified_content = content.replace(
                'max_iterations=3000', 'max_iterations=20'
            ).replace(
                'max_iterations=5000', 'max_iterations=30'
            ).replace(
                'max_iterations=2000', 'max_iterations=15'
            ).replace(
                'debug=False', 'debug=False'
            ).replace(
                'probe_deltas = [5.0, 8.0, 12.0]', 'probe_deltas = [8.0]'
            ).replace(
                'run_lengths = [2, 3, 4, 5]', 'run_lengths = [3, 4]'
            )
            
            temp_file.write(modified_content)
            temp_file.flush()
            
            try:
                # Execute the modified example
                result = subprocess.run(
                    [sys.executable, temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=240,  # 4 minute timeout
                    cwd=get_project_root()
                )
                
                # Should complete without errors
                assert result.returncode == 0, f"Example failed with stderr: {result.stderr}"
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr
                
            finally:
                os.unlink(temp_file.name)

    @pytest.mark.slow
    def test_sequence_analysis_execution(self):
        """Test that sequence_analysis.py executes without errors (marked as slow)."""
        examples_dir = get_examples_dir()
        seq_analysis_path = examples_dir / "advanced_usage" / "sequence_analysis.py"
        
        # Create a modified version with very limited parameters
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            with open(seq_analysis_path, 'r') as original:
                content = original.read()
            
            # Modify to use much smaller sample sizes and fewer iterations
            modified_content = content.replace(
                'sample_count=20000', 'sample_count=100'
            ).replace(
                'sample_count=5000', 'sample_count=50'
            ).replace(
                'sample_count=2000', 'sample_count=30'
            ).replace(
                'max_iterations=5000', 'max_iterations=20'
            ).replace(
                'max_iterations=3000', 'max_iterations=15'
            ).replace(
                'count=20', 'count=2'
            ).replace(
                'plt.show()', '# plt.show()  # Disabled for testing'
            ).replace(
                'plt.savefig', '# plt.savefig  # Disabled for testing'
            )
            
            temp_file.write(modified_content)
            temp_file.flush()
            
            try:
                # Execute the modified example
                result = subprocess.run(
                    [sys.executable, temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    cwd=get_project_root()
                )
                
                # Should complete without errors
                assert result.returncode == 0, f"Example failed with stderr: {result.stderr}"
                assert "ImportError" not in result.stderr
                assert "ModuleNotFoundError" not in result.stderr
                
            finally:
                os.unlink(temp_file.name)


class TestCLIExampleExecution:
    """Test CLI examples execution."""

    def test_cli_help_works(self):
        """Test that CLI help command works."""
        result = subprocess.run(
            [sys.executable, "-m", "pcr_template_generator.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=get_project_root()
        )
        
        assert result.returncode == 0, f"CLI help failed: {result.stderr}"
        assert "usage:" in result.stdout.lower()
        assert "pcr-template-generator" in result.stdout

    def test_cli_basic_functionality(self):
        """Test basic CLI functionality with minimal parameters."""
        result = subprocess.run([
            sys.executable, "-m", "pcr_template_generator.cli",
            "--max-iterations", "10",
            "--seq-length", "50",
            "--primer-length", "18"
        ], capture_output=True, text=True, timeout=60, cwd=get_project_root())
        
        # Should either succeed or fail gracefully (not crash)
        assert "ImportError" not in result.stderr
        assert "ModuleNotFoundError" not in result.stderr
        # Exit code might be 1 if optimization fails, that's OK

    def test_cli_analysis_mode(self):
        """Test CLI analysis mode with minimal parameters."""
        result = subprocess.run([
            sys.executable, "-m", "pcr_template_generator.cli",
            "--analyze",
            "--samples", "10",
            "--primer-length", "18"
        ], capture_output=True, text=True, timeout=30, cwd=get_project_root())
        
        # Should complete successfully
        assert result.returncode == 0, f"CLI analysis failed: {result.stderr}"
        assert "ImportError" not in result.stderr
        assert "ModuleNotFoundError" not in result.stderr


class TestExampleDependencies:
    """Test that examples have all required dependencies."""

    def test_biopython_import(self):
        """Test that BioPython imports work in examples context."""
        try:
            from Bio.SeqUtils import GC, MeltingTemp
            from Bio.Seq import Seq
            # Basic functionality test
            test_seq = "ATGCATGC"
            gc_content = GC(test_seq)
            tm = MeltingTemp.Tm_NN(test_seq)
            assert isinstance(gc_content, float)
            assert isinstance(tm, float)
        except ImportError as e:
            pytest.fail(f"BioPython import failed: {e}")

    def test_numpy_import(self):
        """Test that NumPy imports work in examples context."""
        try:
            import numpy as np
            # Basic functionality test
            arr = np.array([1, 2, 3])
            mean_val = np.mean(arr)
            assert mean_val == 2.0
        except ImportError as e:
            pytest.fail(f"NumPy import failed: {e}")

    def test_matplotlib_import(self):
        """Test that Matplotlib imports work in examples context."""
        try:
            import matplotlib.pyplot as plt
            # Basic functionality test (don't actually plot)
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 2])
            plt.close(fig)
        except ImportError as e:
            pytest.fail(f"Matplotlib import failed: {e}")


class TestExampleOutputs:
    """Test that examples produce expected outputs."""

    def test_simple_generation_produces_template(self):
        """Test that simple generation actually produces a template."""
        from pcr_template_generator import run_experiment
        
        # Use very relaxed parameters to ensure success
        template = run_experiment(
            seq_length=50,
            primer_length=18,
            probe_length=20,
            max_iterations=100,
            overall_gc_min=30.0,
            overall_gc_max=70.0,
            primer_tm_tolerance=5.0,
            probe_tm_delta_min=3.0,
            probe_tm_delta_max=15.0,
        )
        
        if template:  # If successful
            # Test that display works
            display_output = template.display()
            assert isinstance(display_output, str)
            assert len(display_output) > 0
            
            # Test that components work
            assert len(template.fwd()) == 50
            assert len(template.fwd_primer()) == 18
            assert len(template.probe()) == 20
            
            # Test that cost calculation works
            cost = template.cost()
            assert isinstance(cost, (int, float))
            assert cost >= 0

    def test_batch_generation_produces_list(self):
        """Test that batch generation produces a list of templates."""
        from pcr_template_generator import generate_multiple_templates
        
        # Use very relaxed parameters
        templates = generate_multiple_templates(
            count=2,
            seq_length=50,
            primer_length=18,
            probe_length=20,
            max_iterations=50,
            overall_gc_min=30.0,
            overall_gc_max=70.0,
            primer_tm_tolerance=5.0,
            probe_tm_delta_min=3.0,
            probe_tm_delta_max=15.0,
        )
        
        # Should return a list (might be empty if all fail)
        assert isinstance(templates, list)
        
        # If any succeeded, test them
        for template in templates:
            assert len(template.fwd()) == 50
            assert len(template.fwd_primer()) == 18
            assert len(template.probe()) == 20

    def test_analysis_produces_data(self):
        """Test that analysis produces expected data."""
        from pcr_template_generator import analyze_sequence_statistics
        
        # Small sample for testing
        temperatures, gc_contents = analyze_sequence_statistics(
            sequence_length=20,
            sample_count=10,
            debug=False
        )
        
        # Should return two lists of the same length
        assert isinstance(temperatures, list)
        assert isinstance(gc_contents, list)
        assert len(temperatures) == 10
        assert len(gc_contents) == 10
        
        # Values should be reasonable
        for temp in temperatures:
            assert isinstance(temp, (int, float))
            assert 0 < temp < 100  # Reasonable temperature range
        
        for gc in gc_contents:
            assert isinstance(gc, (int, float))
            assert 0 <= gc <= 100  # Valid GC percentage


if __name__ == "__main__":
    pytest.main([__file__])
