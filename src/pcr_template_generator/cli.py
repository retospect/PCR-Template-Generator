"""Command-line interface for PCR Template Generator.

This module provides a CLI for generating optimized PCR templates
with various customization options.
"""

import argparse
import sys

from .generator import (
    analyze_sequence_statistics,
    generate_multiple_templates,
    run_experiment,
)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=("Generate optimized DNA templates for PCR primers " "and probes"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a single template with default settings
  pcr-template-generator

  # Generate 5 templates with custom primer length
  pcr-template-generator --count 5 --primer-length 20

  # Generate template with debug output
  pcr-template-generator --debug

  # Analyze sequence statistics
  pcr-template-generator --analyze --samples 1000
        """,
    )

    # Main operation mode
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of templates to generate (default: 1)",
    )

    # Sequence parameters
    parser.add_argument(
        "--seq-length",
        type=int,
        default=75,
        help="Total template sequence length (default: 75)",
    )
    parser.add_argument(
        "--primer-length",
        type=int,
        default=22,
        help="Primer length (default: 22)",
    )
    parser.add_argument(
        "--probe-length",
        type=int,
        default=25,
        help="Probe length (default: 25)",
    )
    parser.add_argument(
        "--primer-melt",
        type=float,
        default=54.6,
        help="Target primer melting temperature in °C (default: 54.6)",
    )
    parser.add_argument(
        "--probe-gap",
        type=int,
        default=3,
        help="Gap between probe and reverse primer (default: 3)",
    )

    # Optimization parameters
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10000,
        help="Maximum optimization iterations (default: 10000)",
    )

    # Design constraint parameters
    parser.add_argument(
        "--overall-gc-min",
        type=float,
        default=49.0,
        help="Minimum overall GC content %% (default: 49.0)",
    )
    parser.add_argument(
        "--overall-gc-max",
        type=float,
        default=51.0,
        help="Maximum overall GC content %% (default: 51.0)",
    )
    parser.add_argument(
        "--primer-gc-min",
        type=float,
        default=49.0,
        help="Minimum primer GC content %% (default: 49.0)",
    )
    parser.add_argument(
        "--primer-gc-max",
        type=float,
        default=51.0,
        help="Maximum primer GC content %% (default: 51.0)",
    )
    parser.add_argument(
        "--primer-tm-tolerance",
        type=float,
        default=0.5,
        help="Allowed primer Tm difference in °C (default: 0.5)",
    )
    parser.add_argument(
        "--probe-tm-delta-min",
        type=float,
        default=8.0,
        help="Minimum probe-primer Tm difference in °C (default: 8.0)",
    )
    parser.add_argument(
        "--probe-tm-delta-max",
        type=float,
        default=10.0,
        help="Maximum probe-primer Tm difference in °C (default: 10.0)",
    )
    parser.add_argument(
        "--max-run-length",
        type=int,
        default=3,
        help="Maximum allowed run of identical bases (default: 3)",
    )
    parser.add_argument(
        "--unique-end-length",
        type=int,
        default=4,
        help=("Length of unique 3' ends for primer dimer prevention " "(default: 4)"),
    )

    # Output options
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    # Analysis mode
    parser.add_argument(
        "--analyze",
        action="store_true",
        help=("Run sequence statistics analysis instead of generating " "templates"),
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=10000,
        help="Number of samples for analysis (default: 10000)",
    )

    args = parser.parse_args()

    try:
        if args.analyze:
            run_analysis(args)
        else:
            run_generation(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run_generation(args: argparse.Namespace) -> None:
    """Run template generation based on CLI arguments."""
    if args.verbose or args.debug:
        print("PCR Template Generator")
        print("=" * 50)
        print(f"Generating {args.count} template(s) with parameters:")
        print(f"  Sequence length: {args.seq_length}")
        print(f"  Primer length: {args.primer_length}")
        print(f"  Probe length: {args.probe_length}")
        print(f"  Target primer Tm: {args.primer_melt}°C")
        print(f"  Probe gap: {args.probe_gap}")
        print(f"  Max iterations: {args.max_iterations}")
        print()

    if args.count == 1:
        # Generate single template
        template = run_experiment(
            seq_length=args.seq_length,
            primer_length=args.primer_length,
            probe_length=args.probe_length,
            primer_melt=args.primer_melt,
            probe_gap=args.probe_gap,
            debug=args.debug,
            max_iterations=args.max_iterations,
            overall_gc_min=args.overall_gc_min,
            overall_gc_max=args.overall_gc_max,
            primer_gc_min=args.primer_gc_min,
            primer_gc_max=args.primer_gc_max,
            primer_tm_tolerance=args.primer_tm_tolerance,
            probe_tm_delta_min=args.probe_tm_delta_min,
            probe_tm_delta_max=args.probe_tm_delta_max,
            max_run_length=args.max_run_length,
            unique_end_length=args.unique_end_length,
        )

        if template:
            print(template.display())
            if args.verbose:
                print(f"\nFinal cost: {template.cost():.2f}")
                if template.cost() > 0:
                    print("Rule violations:")
                    print(template.rule_info())
        else:
            print("Failed to generate template within iteration limit")
            sys.exit(1)

    else:
        # Generate multiple templates
        templates = generate_multiple_templates(
            count=args.count,
            seq_length=args.seq_length,
            primer_length=args.primer_length,
            probe_length=args.probe_length,
            primer_melt=args.primer_melt,
            probe_gap=args.probe_gap,
            debug=args.debug,
            max_iterations=args.max_iterations,
            overall_gc_min=args.overall_gc_min,
            overall_gc_max=args.overall_gc_max,
            primer_gc_min=args.primer_gc_min,
            primer_gc_max=args.primer_gc_max,
            primer_tm_tolerance=args.primer_tm_tolerance,
            probe_tm_delta_min=args.probe_tm_delta_min,
            probe_tm_delta_max=args.probe_tm_delta_max,
            max_run_length=args.max_run_length,
            unique_end_length=args.unique_end_length,
        )

        if not templates:
            print("Failed to generate any templates")
            sys.exit(1)

        for i, template in enumerate(templates, 1):
            print(f"Template {i}:")
            print(template.display())
            if args.verbose:
                print(f"Cost: {template.cost():.2f}")
            print()

        if args.verbose:
            success_rate = len(templates) / args.count * 100
            print(
                f"Generated {len(templates)}/{args.count} templates "
                f"({success_rate:.1f}% success rate)"
            )


def run_analysis(args: argparse.Namespace) -> None:
    """Run sequence statistics analysis."""
    if args.verbose or args.debug:
        print("PCR Template Generator - Sequence Analysis")
        print("=" * 50)
        print(
            f"Analyzing {args.samples} random sequences of length "
            f"{args.primer_length}"
        )
        print()

    temperatures, gc_contents = analyze_sequence_statistics(
        sequence_length=args.primer_length,
        sample_count=args.samples,
        debug=args.debug,
    )

    # Calculate statistics
    import numpy as np

    temp_mean = np.mean(temperatures)
    temp_std = np.std(temperatures)
    gc_mean = np.mean(gc_contents)
    gc_std = np.std(gc_contents)

    print(f"Analysis Results for {args.primer_length}bp sequences:")
    print(f"Temperature: {temp_mean:.2f} ± {temp_std:.2f}°C")
    print(f"GC content: {gc_mean:.2f} ± {gc_std:.2f}%")
    print(f"Temperature range: {min(temperatures):.1f} - " f"{max(temperatures):.1f}°C")
    print(f"GC content range: {min(gc_contents):.1f} - " f"{max(gc_contents):.1f}%")

    # Optional: save data for plotting
    if args.verbose:
        try:
            import matplotlib.pyplot as plt

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # Temperature histogram
            ax1.hist(temperatures, bins=30, alpha=0.7, edgecolor="black")
            ax1.set_xlabel("Melting Temperature (°C)")
            ax1.set_ylabel("Frequency")
            ax1.set_title("Distribution of Melting Temperatures")
            ax1.axvline(
                temp_mean,
                color="red",
                linestyle="--",
                label=f"Mean: {temp_mean:.1f}°C",
            )
            ax1.legend()

            # GC vs Temperature scatter
            ax2.scatter(gc_contents, temperatures, alpha=0.5, s=1)
            ax2.set_xlabel("GC Content (%)")
            ax2.set_ylabel("Melting Temperature (°C)")
            ax2.set_title("GC Content vs Melting Temperature")

            plt.tight_layout()
            plt.savefig("sequence_analysis.png", dpi=150, bbox_inches="tight")
            print("\nPlot saved as 'sequence_analysis.png'")

        except ImportError:
            print("\nMatplotlib not available for plotting")


if __name__ == "__main__":
    main()
