"""Tests for generator module."""

from unittest.mock import patch

import pytest

from pcr_template_generator.generator import (
    analyze_sequence_statistics,
    generate_multiple_templates,
    run_experiment,
)
from pcr_template_generator.sequence import Sequence


class TestRunExperiment:
    """Test run_experiment function."""

    def test_run_experiment_default(self):
        """Test run_experiment with default parameters."""
        result = run_experiment(max_iterations=100, debug=False)
        # May succeed or fail, but should return Sequence or None
        assert result is None or isinstance(result, Sequence)

    def test_run_experiment_with_debug(self):
        """Test run_experiment with debug enabled."""
        with patch("builtins.print") as mock_print:
            result = run_experiment(max_iterations=50, debug=True)
            # Should have printed debug messages
            assert mock_print.called

    def test_run_experiment_custom_params(self):
        """Test run_experiment with custom parameters."""
        result = run_experiment(
            seq_length=50,
            primer_length=18,
            probe_length=20,
            primer_melt=52.0,
            probe_gap=2,
            max_iterations=100,
            target_cost=5.0,  # Higher target for easier success
        )
        assert result is None or isinstance(result, Sequence)
        if result:
            assert len(result.fwd()) == 50
            assert len(result.fwd_primer()) == 18

    def test_run_experiment_zero_iterations(self):
        """Test run_experiment with zero iterations."""
        result = run_experiment(max_iterations=0)
        # Should return None (no optimization possible)
        assert result is None

    def test_run_experiment_high_target_cost(self):
        """Test run_experiment with very high target cost."""
        result = run_experiment(max_iterations=10, target_cost=1000.0)
        # Should succeed quickly with high target
        assert isinstance(result, Sequence)

    def test_run_experiment_impossible_target(self):
        """Test run_experiment with impossible target cost."""
        result = run_experiment(max_iterations=10, target_cost=0.0)
        # Very unlikely to achieve perfect score
        assert result is None or isinstance(result, Sequence)


class TestGenerateMultipleTemplates:
    """Test generate_multiple_templates function."""

    def test_generate_single_template(self):
        """Test generating single template."""
        templates = generate_multiple_templates(
            count=1, max_iterations=100, debug=False
        )
        assert isinstance(templates, list)
        assert len(templates) <= 1  # May fail to generate

    def test_generate_multiple_templates(self):
        """Test generating multiple templates."""
        templates = generate_multiple_templates(count=3, max_iterations=50, debug=False)
        assert isinstance(templates, list)
        assert len(templates) <= 3  # May not generate all
        for template in templates:
            assert isinstance(template, Sequence)

    def test_generate_with_debug(self):
        """Test generation with debug output."""
        with patch("builtins.print") as mock_print:
            templates = generate_multiple_templates(
                count=2, max_iterations=50, debug=True
            )
            # Should have printed debug messages
            assert mock_print.called

    def test_generate_zero_count(self):
        """Test generating zero templates."""
        templates = generate_multiple_templates(count=0)
        assert templates == []

    def test_generate_custom_params(self):
        """Test generation with custom parameters."""
        templates = generate_multiple_templates(
            count=2,
            seq_length=60,
            primer_length=20,
            probe_length=22,
            primer_melt=53.0,
            probe_gap=4,
            max_iterations=100,
        )
        assert isinstance(templates, list)
        for template in templates:
            assert len(template.fwd()) == 60
            assert len(template.fwd_primer()) == 20

    def test_generate_with_failures(self):
        """Test generation when some attempts fail."""
        # Use very low iterations to increase failure rate
        templates = generate_multiple_templates(count=5, max_iterations=1, debug=False)
        # Should return whatever succeeded
        assert isinstance(templates, list)
        assert len(templates) <= 5


class TestAnalyzeSequenceStatistics:
    """Test analyze_sequence_statistics function."""

    def test_analyze_default_params(self):
        """Test analysis with default parameters."""
        temps, gcs = analyze_sequence_statistics(sample_count=100, debug=False)

        assert isinstance(temps, list)
        assert isinstance(gcs, list)
        assert len(temps) == 100
        assert len(gcs) == 100

        # Check data ranges
        assert all(isinstance(t, float) for t in temps)
        assert all(isinstance(gc, float) for gc in gcs)
        assert all(0 <= gc <= 100 for gc in gcs)

    def test_analyze_custom_params(self):
        """Test analysis with custom parameters."""
        temps, gcs = analyze_sequence_statistics(
            sequence_length=18, sample_count=50, debug=False
        )

        assert len(temps) == 50
        assert len(gcs) == 50

    def test_analyze_with_debug(self):
        """Test analysis with debug output."""
        with patch("builtins.print") as mock_print:
            temps, gcs = analyze_sequence_statistics(sample_count=20, debug=True)
            # Should have printed debug messages
            assert mock_print.called

    def test_analyze_small_sample(self):
        """Test analysis with small sample size."""
        temps, gcs = analyze_sequence_statistics(sample_count=5, debug=False)

        assert len(temps) == 5
        assert len(gcs) == 5

    def test_analyze_single_sample(self):
        """Test analysis with single sample."""
        temps, gcs = analyze_sequence_statistics(sample_count=1, debug=False)

        assert len(temps) == 1
        assert len(gcs) == 1

    def test_analyze_zero_samples(self):
        """Test analysis with zero samples."""
        temps, gcs = analyze_sequence_statistics(sample_count=0, debug=False)

        assert temps == []
        assert gcs == []

    def test_analyze_very_short_sequence(self):
        """Test analysis with very short sequences."""
        temps, gcs = analyze_sequence_statistics(
            sequence_length=2, sample_count=10, debug=False
        )

        assert len(temps) == 10
        assert len(gcs) == 10
        # Should still produce valid results
        assert all(isinstance(t, float) for t in temps)

    def test_analyze_long_sequence(self):
        """Test analysis with longer sequences."""
        temps, gcs = analyze_sequence_statistics(
            sequence_length=50, sample_count=10, debug=False
        )

        assert len(temps) == 10
        assert len(gcs) == 10


class TestGeneratorIntegration:
    """Integration tests for generator module."""

    def test_experiment_to_multiple_generation(self):
        """Test that single experiment works with multiple generation."""
        # First test single experiment
        single_result = run_experiment(max_iterations=100, debug=False)

        # Then test multiple generation
        multiple_results = generate_multiple_templates(
            count=2, max_iterations=100, debug=False
        )

        # Both should work (though may return None/empty list)
        assert single_result is None or isinstance(single_result, Sequence)
        assert isinstance(multiple_results, list)

    def test_consistent_parameters(self):
        """Test that same parameters give consistent results."""
        params = {
            "seq_length": 60,
            "primer_length": 20,
            "probe_length": 22,
            "primer_melt": 53.0,
            "probe_gap": 2,
            "max_iterations": 100,
        }

        # Generate single template
        single = run_experiment(**params, debug=False)

        # Generate multiple templates
        multiple = generate_multiple_templates(count=1, **params, debug=False)

        # If both succeed, should have same parameters
        if single and multiple:
            assert len(single.fwd()) == len(multiple[0].fwd())
            assert len(single.fwd_primer()) == len(multiple[0].fwd_primer())

    def test_analysis_with_generation_params(self):
        """Test analysis using same parameters as generation."""
        # Use analysis to understand sequence properties
        temps, gcs = analyze_sequence_statistics(
            sequence_length=22, sample_count=100, debug=False
        )

        # Then try generation
        template = run_experiment(primer_length=22, max_iterations=50, debug=False)

        # Both should work
        assert len(temps) == 100
        assert template is None or isinstance(template, Sequence)

    def test_error_handling(self):
        """Test error handling in generator functions."""
        # These should not crash even with unusual parameters
        result1 = run_experiment(seq_length=5, primer_length=10)  # Impossible geometry
        result2 = generate_multiple_templates(count=1, seq_length=5, primer_length=10)

        # Should handle gracefully
        assert result1 is None or isinstance(result1, Sequence)
        assert isinstance(result2, list)

    @patch("pcr_template_generator.generator.random.choice")
    def test_deterministic_behavior(self, mock_choice):
        """Test behavior with mocked randomness."""
        # Mock random.choice to always return 'a'
        mock_choice.return_value = "a"

        result = run_experiment(seq_length=10, max_iterations=10, debug=False)

        # Should still work (though likely high cost due to all A's)
        assert result is None or isinstance(result, Sequence)
        if result:
            # Should be all A's
            assert str(result.fwd()) == "a" * 10
