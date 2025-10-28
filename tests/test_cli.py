"""Tests for CLI module."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

from pcr_template_generator.cli import main, run_generation, run_analysis
from pcr_template_generator.sequence import Sequence


class TestCLIMain:
    """Test main CLI function."""

    def test_main_help(self):
        """Test CLI help output."""
        with patch.object(sys, 'argv', ['pcr-template-generator', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_default_args(self):
        """Test CLI with default arguments."""
        with patch.object(sys, 'argv', ['pcr-template-generator']):
            with patch('pcr_template_generator.cli.run_generation') as mock_run:
                main()
                mock_run.assert_called_once()

    def test_main_analyze_mode(self):
        """Test CLI in analysis mode."""
        with patch.object(sys, 'argv', ['pcr-template-generator', '--analyze']):
            with patch('pcr_template_generator.cli.run_analysis') as mock_run:
                main()
                mock_run.assert_called_once()

    def test_main_keyboard_interrupt(self):
        """Test CLI handling of keyboard interrupt."""
        with patch.object(sys, 'argv', ['pcr-template-generator']):
            with patch('pcr_template_generator.cli.run_generation', side_effect=KeyboardInterrupt):
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1
                    mock_print.assert_called_with("\nOperation cancelled by user")

    def test_main_exception_handling(self):
        """Test CLI handling of general exceptions."""
        with patch.object(sys, 'argv', ['pcr-template-generator']):
            with patch('pcr_template_generator.cli.run_generation', side_effect=ValueError("Test error")):
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1


class TestRunGeneration:
    """Test run_generation function."""

    def test_run_generation_single_success(self):
        """Test successful single template generation."""
        mock_args = MagicMock()
        mock_args.count = 1
        mock_args.debug = False
        mock_args.verbose = False
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        mock_sequence = MagicMock(spec=Sequence)
        mock_sequence.display.return_value = "test display"
        mock_sequence.cost.return_value = 0.5

        with patch('pcr_template_generator.cli.run_experiment', return_value=mock_sequence):
            with patch('builtins.print') as mock_print:
                run_generation(mock_args)
                mock_print.assert_called_with("test display")

    def test_run_generation_single_failure(self):
        """Test failed single template generation."""
        mock_args = MagicMock()
        mock_args.count = 1
        mock_args.debug = False
        mock_args.verbose = False
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        with patch('pcr_template_generator.cli.run_experiment', return_value=None):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    run_generation(mock_args)
                assert exc_info.value.code == 1
                mock_print.assert_called_with("Failed to generate template within iteration limit")

    def test_run_generation_multiple_success(self):
        """Test successful multiple template generation."""
        mock_args = MagicMock()
        mock_args.count = 3
        mock_args.debug = False
        mock_args.verbose = False
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        mock_sequences = []
        for i in range(3):
            mock_seq = MagicMock(spec=Sequence)
            mock_seq.display.return_value = f"template {i+1}"
            mock_seq.cost.return_value = 0.5
            mock_sequences.append(mock_seq)

        with patch('pcr_template_generator.cli.generate_multiple_templates', return_value=mock_sequences):
            with patch('builtins.print') as mock_print:
                run_generation(mock_args)
                # Should print each template
                assert mock_print.call_count >= 3

    def test_run_generation_multiple_failure(self):
        """Test failed multiple template generation."""
        mock_args = MagicMock()
        mock_args.count = 3
        mock_args.debug = False
        mock_args.verbose = False
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        with patch('pcr_template_generator.cli.generate_multiple_templates', return_value=[]):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    run_generation(mock_args)
                assert exc_info.value.code == 1
                mock_print.assert_called_with("Failed to generate any templates")

    def test_run_generation_verbose_output(self):
        """Test verbose output in generation."""
        mock_args = MagicMock()
        mock_args.count = 1
        mock_args.debug = False
        mock_args.verbose = True
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        mock_sequence = MagicMock(spec=Sequence)
        mock_sequence.display.return_value = "test display"
        mock_sequence.cost.return_value = 0.5

        with patch('pcr_template_generator.cli.run_experiment', return_value=mock_sequence):
            with patch('builtins.print') as mock_print:
                run_generation(mock_args)
                # Should print header and final cost
                assert mock_print.call_count >= 2

    def test_run_generation_debug_output(self):
        """Test debug output in generation."""
        mock_args = MagicMock()
        mock_args.count = 1
        mock_args.debug = True
        mock_args.verbose = False
        mock_args.seq_length = 75
        mock_args.primer_length = 22
        mock_args.probe_length = 25
        mock_args.primer_melt = 54.6
        mock_args.probe_gap = 3
        mock_args.max_iterations = 1000

        mock_sequence = MagicMock(spec=Sequence)
        mock_sequence.display.return_value = "test display"
        mock_sequence.cost.return_value = 0.5

        with patch('pcr_template_generator.cli.run_experiment', return_value=mock_sequence):
            with patch('builtins.print') as mock_print:
                run_generation(mock_args)
                # Should print header due to debug=True
                assert mock_print.call_count >= 2


class TestRunAnalysis:
    """Test run_analysis function."""

    def test_run_analysis_basic(self):
        """Test basic analysis run."""
        mock_args = MagicMock()
        mock_args.samples = 100
        mock_args.primer_length = 22
        mock_args.debug = False
        mock_args.verbose = False

        mock_temps = [50.0, 55.0, 60.0] * 33 + [52.0]  # 100 values
        mock_gcs = [45.0, 50.0, 55.0] * 33 + [48.0]    # 100 values

        with patch('pcr_template_generator.cli.analyze_sequence_statistics', 
                   return_value=(mock_temps, mock_gcs)):
            with patch('builtins.print') as mock_print:
                run_analysis(mock_args)
                # Should print analysis results
                assert mock_print.call_count >= 4

    def test_run_analysis_verbose(self):
        """Test analysis with verbose output and plotting."""
        mock_args = MagicMock()
        mock_args.samples = 50
        mock_args.primer_length = 22
        mock_args.debug = False
        mock_args.verbose = True

        mock_temps = [50.0, 55.0] * 25  # 50 values
        mock_gcs = [45.0, 50.0] * 25    # 50 values

        # Mock matplotlib
        mock_plt = MagicMock()
        mock_fig = MagicMock()
        mock_axes = [MagicMock(), MagicMock()]
        mock_plt.subplots.return_value = (mock_fig, mock_axes)

        with patch('pcr_template_generator.cli.analyze_sequence_statistics', 
                   return_value=(mock_temps, mock_gcs)):
            with patch.dict('sys.modules', {'matplotlib.pyplot': mock_plt}):
                with patch('builtins.print') as mock_print:
                    run_analysis(mock_args)
                    # Should create plots and save figure
                    mock_plt.subplots.assert_called_once()
                    mock_plt.savefig.assert_called_once()

    def test_run_analysis_no_matplotlib(self):
        """Test analysis when matplotlib is not available."""
        mock_args = MagicMock()
        mock_args.samples = 50
        mock_args.primer_length = 22
        mock_args.debug = False
        mock_args.verbose = True

        mock_temps = [50.0, 55.0] * 25
        mock_gcs = [45.0, 50.0] * 25

        with patch('pcr_template_generator.cli.analyze_sequence_statistics', 
                   return_value=(mock_temps, mock_gcs)):
            with patch.dict('sys.modules', {'matplotlib.pyplot': None}):
                with patch('builtins.print') as mock_print:
                    run_analysis(mock_args)
                    # Should print message about matplotlib not being available
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any("Matplotlib not available" in call for call in calls)

    def test_run_analysis_debug(self):
        """Test analysis with debug output."""
        mock_args = MagicMock()
        mock_args.samples = 10
        mock_args.primer_length = 22
        mock_args.debug = True
        mock_args.verbose = False

        mock_temps = [50.0] * 10
        mock_gcs = [45.0] * 10

        with patch('pcr_template_generator.cli.analyze_sequence_statistics', 
                   return_value=(mock_temps, mock_gcs)):
            with patch('builtins.print') as mock_print:
                run_analysis(mock_args)
                # Should print header due to debug=True
                assert mock_print.call_count >= 2


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_cli_argument_parsing(self):
        """Test that CLI arguments are parsed correctly."""
        test_args = [
            'pcr-template-generator',
            '--count', '2',
            '--seq-length', '80',
            '--primer-length', '20',
            '--probe-length', '30',
            '--primer-melt', '55.0',
            '--probe-gap', '5',
            '--max-iterations', '500',
            '--verbose'
        ]

        with patch.object(sys, 'argv', test_args):
            with patch('pcr_template_generator.cli.run_generation') as mock_run:
                main()
                
                # Check that arguments were parsed correctly
                args = mock_run.call_args[0][0]
                assert args.count == 2
                assert args.seq_length == 80
                assert args.primer_length == 20
                assert args.probe_length == 30
                assert args.primer_melt == 55.0
                assert args.probe_gap == 5
                assert args.max_iterations == 500
                assert args.verbose is True

    def test_cli_analysis_arguments(self):
        """Test CLI analysis mode arguments."""
        test_args = [
            'pcr-template-generator',
            '--analyze',
            '--samples', '500',
            '--debug'
        ]

        with patch.object(sys, 'argv', test_args):
            with patch('pcr_template_generator.cli.run_analysis') as mock_run:
                main()
                
                args = mock_run.call_args[0][0]
                assert args.analyze is True
                assert args.samples == 500
                assert args.debug is True

    def test_cli_error_propagation(self):
        """Test that errors in sub-functions propagate correctly."""
        with patch.object(sys, 'argv', ['pcr-template-generator']):
            with patch('pcr_template_generator.cli.run_generation', 
                       side_effect=RuntimeError("Test error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
