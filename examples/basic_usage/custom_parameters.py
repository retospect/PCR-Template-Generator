#!/usr/bin/env python3
"""
Custom Parameters PCR Template Generation Example

This example demonstrates how to customize sequence generation parameters
to meet specific experimental requirements.

Requirements:
- pcr-template-generator>=2.0.0
- Python>=3.10

Usage:
    python custom_parameters.py
"""

from Bio.SeqUtils import MeltingTemp, gc_fraction

from pcr_template_generator import Sequence, run_experiment


def main():
    """Demonstrate custom parameter usage."""
    print("🧬 PCR Template Generator - Custom Parameters Example")
    print("=" * 60)

    # Example 1: Short template for limited space
    print("\n1️⃣ Short Template (60bp total)")
    print("-" * 40)

    short_template = run_experiment(
        seq_length=60,  # Shorter total length
        primer_length=18,  # Shorter primers
        probe_length=20,  # Shorter probe
        primer_melt=52.0,  # Lower melting temperature
        probe_gap=2,  # Smaller gap
        debug=False,
        max_iterations=3000,
    )

    if short_template:
        print("✅ Short template generated:")
        print(short_template.display())
        print(f"Cost: {short_template.cost():.2f}")
        analyze_template(short_template, "Short")

    # Example 2: Long template for robust amplification
    print("\n2️⃣ Long Template (100bp total)")
    print("-" * 40)

    long_template = run_experiment(
        seq_length=100,  # Longer total length
        primer_length=25,  # Longer primers
        probe_length=30,  # Longer probe
        primer_melt=58.0,  # Higher melting temperature
        probe_gap=5,  # Larger gap
        debug=False,
        max_iterations=3000,
    )

    if long_template:
        print("✅ Long template generated:")
        print(long_template.display())
        print(f"Cost: {long_template.cost():.2f}")
        analyze_template(long_template, "Long")

    # Example 3: High-stringency template with custom constraints
    print("\n3️⃣ High-Stringency Template (Custom Constraints)")
    print("-" * 40)

    high_stringency = run_experiment(
        seq_length=80,
        primer_length=22,
        probe_length=25,
        primer_melt=60.0,  # High melting temperature
        probe_gap=3,
        debug=False,
        max_iterations=5000,  # More iterations for difficult constraints
        # Custom design constraints for high stringency
        overall_gc_min=49.5,  # Tighter GC control
        overall_gc_max=50.5,
        primer_tm_tolerance=0.3,  # Very tight primer Tm matching
        probe_tm_delta_min=8.5,  # Narrow probe-primer difference
        probe_tm_delta_max=9.5,
        max_run_length=2,  # No runs longer than 2 bases
        unique_end_length=5,  # Longer unique ends for specificity
    )

    if high_stringency:
        print("✅ High-stringency template generated:")
        print(high_stringency.display())
        print(f"Cost: {high_stringency.cost():.2f}")
        analyze_template(high_stringency, "High-stringency")

    # Example 4: Compare different optimization efforts
    print("\n4️⃣ Optimization Effort Comparison")
    print("-" * 40)

    compare_optimization_efforts()


def analyze_template(template, name):
    """Analyze and display template properties."""
    fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
    rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
    probe_tm = MeltingTemp.Tm_NN(str(template.probe()))

    print(f"{name} template properties:")
    print(f"Template length: {len(template.fwd())} bp")
    print(f"GC content: {gc_fraction(template.fwd()) * 100:.1f}%")
    print(f"  Forward primer Tm: {fwd_tm:.1f}°C")
    print(f"  Reverse primer Tm: {rev_tm:.1f}°C")
    print(f"  Probe Tm: {probe_tm:.1f}°C")
    print(f"  Primer ΔTm: {abs(fwd_tm - rev_tm):.1f}°C")
    print(f"  Probe-Primer ΔTm: {probe_tm - ((fwd_tm + rev_tm) / 2):.1f}°C")


def compare_optimization_efforts():
    """Compare templates generated with different optimization efforts."""
    efforts = [("Quick", 1000), ("Standard", 5000), ("Thorough", 10000)]

    results = []

    for name, max_iter in efforts:
        print(f"\nGenerating {name} optimization ({max_iter} iterations)...")

        template = run_experiment(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            probe_gap=3,
            debug=False,
            max_iterations=max_iter,
        )

        if template:
            cost = template.cost()
            results.append((name, max_iter, cost, template))
            print(f"  Cost: {cost:.2f}")
        else:
            results.append((name, max_iter, float("inf"), None))
            print(f"  Failed to generate")

    # Summary
    print("\nOptimization Effort Summary:")
    print("Method      | Iterations | Cost   | Success")
    print("-" * 40)

    for name, iterations, cost, template in results:
        success = "✅" if template else "❌"
        cost_str = f"{cost:.2f}" if cost != float("inf") else "Failed"
        print(f"{name:<11} | {iterations:<10} | {cost_str:<6} | {success}")

    # Show best result
    successful_results = [
        (name, cost, template) for name, _, cost, template in results if template
    ]
    if successful_results:
        best_name, best_cost, best_template = min(
            successful_results, key=lambda x: x[1]
        )
        print(f"\nBest result: {best_name} optimization (cost: {best_cost:.2f})")


def demonstrate_constraint_parameters():
    """Demonstrate the new configurable design constraint parameters."""
    print("\n5️⃣ Configurable Design Constraints")
    print("-" * 40)

    print("Testing different probe-primer temperature differences...")

    # Test different probe temperature deltas
    probe_deltas = [6.0, 8.0, 12.0]

    for delta in probe_deltas:
        print(f"\nProbe ΔTm = {delta}°C:")

        template = run_experiment(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            debug=False,
            max_iterations=2000,
            probe_tm_delta_min=delta - 0.5,
            probe_tm_delta_max=delta + 0.5,
        )

        if template:
            from Bio.SeqUtils import MeltingTemp

            probe_tm = MeltingTemp.Tm_NN(str(template.probe()))
            fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
            rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
            actual_delta = probe_tm - (fwd_tm + rev_tm) / 2

            print(f"  ✅ Success! Actual ΔTm: {actual_delta:.1f}°C")
            print(f"     Cost: {template.cost():.2f}")
        else:
            print(f"  ❌ Failed to achieve {delta}°C difference")


def demonstrate_parameter_effects():
    """Demonstrate how different parameters affect the results."""
    print("\n6️⃣ Parameter Effects Demonstration")
    print("-" * 40)

    base_params = {
        "seq_length": 75,
        "primer_length": 22,
        "probe_length": 25,
        "primer_melt": 54.6,
        "probe_gap": 3,
        "debug": False,
        "max_iterations": 3000,
    }

    # Test different primer melting temperatures
    print("\nTesting different primer melting temperatures:")

    for tm in [50.0, 54.6, 60.0]:
        params = base_params.copy()
        params["primer_melt"] = tm

        template = run_experiment(**params)
        if template:
            fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
            rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
            print(
                f"  Target: {tm}°C → Actual: {fwd_tm:.1f}°C/{rev_tm:.1f}°C (Cost: {template.cost():.2f})"
            )
        else:
            print(f"  Target: {tm}°C → Failed to generate")


if __name__ == "__main__":
    main()
    demonstrate_constraint_parameters()
    demonstrate_parameter_effects()

    print("\n🎉 Custom parameters example completed!")
    print("\nKey takeaways:")
    print("- Shorter sequences are generally easier to optimize")
    print("- Higher melting temperatures require more optimization effort")
    print("- More iterations usually lead to better results")
    print("- Balance your requirements with computational time")
    print("\nNext steps:")
    print("- Try ../advanced_usage/ for custom rules and analysis")
    print("- Check ../cli_examples/ for batch processing workflows")
