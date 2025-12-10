#!/usr/bin/env python3
"""
Custom Design Constraints Example

This example demonstrates how to use the configurable design constraint
parameters to customize PCR template generation for specific experimental
requirements.

Requirements:
- pcr-template-generator>=1.0.0
- Python>=3.10

Usage:
    python custom_constraints.py
"""

from Bio.SeqUtils import MeltingTemp, gc_fraction

from pcr_template_generator import Sequence, run_experiment


def main():
    """Demonstrate custom design constraints."""
    print("🧬 PCR Template Generator - Custom Design Constraints")
    print("=" * 60)

    # Example 1: Relaxed constraints for difficult targets
    print("\n1️⃣ Relaxed Constraints (for difficult targets)")
    print("-" * 50)

    relaxed_template = run_experiment(
        seq_length=75,
        primer_length=22,
        probe_length=25,
        primer_melt=54.6,
        debug=False,
        max_iterations=3000,
        # Relaxed constraints
        overall_gc_min=45.0,  # Wider GC range
        overall_gc_max=55.0,
        primer_gc_min=45.0,
        primer_gc_max=55.0,
        primer_tm_tolerance=1.0,  # Allow 1°C difference between primers
        probe_tm_delta_min=6.0,  # Lower probe-primer difference
        probe_tm_delta_max=12.0,  # Higher probe-primer difference
        max_run_length=4,  # Allow longer runs
        unique_end_length=3,  # Shorter unique ends
    )

    if relaxed_template:
        print("✅ Relaxed constraints template:")
        print(relaxed_template.display())
        analyze_template(relaxed_template, "Relaxed")
    else:
        print("❌ Failed to generate relaxed template")

    # Example 2: Strict constraints for high-specificity
    print("\n2️⃣ Strict Constraints (high-specificity)")
    print("-" * 50)

    strict_template = run_experiment(
        seq_length=75,
        primer_length=22,
        probe_length=25,
        primer_melt=54.6,
        debug=False,
        max_iterations=5000,  # More iterations for strict constraints
        # Strict constraints
        overall_gc_min=49.5,  # Narrow GC range
        overall_gc_max=50.5,
        primer_gc_min=49.5,
        primer_gc_max=50.5,
        primer_tm_tolerance=0.2,  # Very tight Tm matching
        probe_tm_delta_min=8.5,  # Narrow probe-primer difference
        probe_tm_delta_max=9.5,
        max_run_length=2,  # No runs longer than 2
        unique_end_length=5,  # Longer unique ends
        max_secondary_length=3,  # Shorter secondary structures
    )

    if strict_template:
        print("✅ Strict constraints template:")
        print(strict_template.display())
        analyze_template(strict_template, "Strict")
    else:
        print("❌ Failed to generate strict template")

    # Example 3: Custom probe temperature difference
    print("\n3️⃣ Custom Probe Temperature Differences")
    print("-" * 50)

    probe_deltas = [5.0, 8.0, 12.0]  # Different probe-primer temperature differences

    for delta in probe_deltas:
        print(f"\nTesting probe ΔTm = {delta}°C...")

        template = run_experiment(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            debug=False,
            max_iterations=3000,
            probe_tm_delta_min=delta - 0.5,
            probe_tm_delta_max=delta + 0.5,
        )

        if template:
            probe_tm = MeltingTemp.Tm_NN(str(template.probe()))
            fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
            rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
            actual_delta = probe_tm - (fwd_tm + rev_tm) / 2

            print(f"  ✅ Success! Actual ΔTm: {actual_delta:.1f}°C")
            print(
                f"     Probe Tm: {probe_tm:.1f}°C, Primer Tm: {(fwd_tm + rev_tm) / 2:.1f}°C"
            )
        else:
            print(f"  ❌ Failed to achieve {delta}°C difference")

    # Example 4: Different run length tolerances
    print("\n4️⃣ Run Length Tolerance Comparison")
    print("-" * 50)

    run_lengths = [2, 3, 4, 5]

    for max_run in run_lengths:
        print(f"\nTesting max run length = {max_run}...")

        template = run_experiment(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            debug=False,
            max_iterations=2000,
            max_run_length=max_run,
        )

        if template:
            # Check actual run lengths in the sequence
            sequence_str = str(template.fwd())
            max_actual_run = find_max_run_length(sequence_str)
            print(f"  ✅ Success! Max actual run: {max_actual_run}")
            print(f"     Cost: {template.cost():.2f}")
        else:
            print(f"  ❌ Failed with max run length {max_run}")

    # Example 5: Comparison of default vs custom constraints
    print("\n5️⃣ Default vs Custom Constraints Comparison")
    print("-" * 50)

    compare_constraints()


def analyze_template(template, name):
    """Analyze and display template properties."""
    fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
    rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
    probe_tm = MeltingTemp.Tm_NN(str(template.probe()))

    print(f"\n{name} template analysis:")
    print(f"Template length: {len(template.fwd())} bp")
    print(f"GC content: {gc_fraction(template.fwd()) * 100:.1f}%")
    print(f"  Forward primer Tm: {fwd_tm:.1f}°C")
    print(f"  Reverse primer Tm: {rev_tm:.1f}°C")
    print(f"  Probe Tm: {probe_tm:.1f}°C")
    print(f"  Primer ΔTm: {abs(fwd_tm - rev_tm):.1f}°C")
    print(f"  Probe-Primer ΔTm: {probe_tm - ((fwd_tm + rev_tm) / 2):.1f}°C")

    # Check for rule violations
    if template.cost() > 0:
        print(f"  Rule violations:")
        violations = template.rule_info().strip().split("\n")
        for violation in violations[:3]:  # Show first 3 violations
            if violation.strip():
                print(f"    - {violation.strip()}")
        if len(violations) > 3:
            print(f"    - ... and {len(violations) - 3} more")


def find_max_run_length(sequence):
    """Find the maximum run length of identical bases in a sequence."""
    if not sequence:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run


def compare_constraints():
    """Compare default vs custom constraints."""
    print("Comparing default vs custom constraints...")

    # Default constraints
    default_template = run_experiment(
        seq_length=75,
        primer_length=22,
        probe_length=25,
        primer_melt=54.6,
        debug=False,
        max_iterations=3000,
    )

    # Custom constraints for AT-rich targets
    at_rich_template = run_experiment(
        seq_length=75,
        primer_length=22,
        probe_length=25,
        primer_melt=52.0,  # Lower melting temperature
        debug=False,
        max_iterations=3000,
        overall_gc_min=35.0,  # Allow lower GC content
        overall_gc_max=45.0,
        primer_gc_min=35.0,
        primer_gc_max=45.0,
        probe_gc_min=35.0,
        probe_gc_max=45.0,
        probe_tm_delta_min=6.0,  # Smaller probe difference
        probe_tm_delta_max=8.0,
    )

    print("\nComparison Results:")
    print("=" * 40)

    if default_template:
        print("Default constraints:")
        analyze_template(default_template, "Default")
    else:
        print("Default constraints: ❌ Failed")

    if at_rich_template:
        print("\nAT-rich optimized constraints:")
        analyze_template(at_rich_template, "AT-rich")
    else:
        print("\nAT-rich optimized constraints: ❌ Failed")

    # Success rate comparison
    print(f"\nSuccess comparison:")
    print(f"  Default constraints: {'✅' if default_template else '❌'}")
    print(f"  AT-rich constraints: {'✅' if at_rich_template else '❌'}")


def demonstrate_constraint_effects():
    """Demonstrate how different constraints affect optimization difficulty."""
    print("\n6️⃣ Constraint Effects on Optimization")
    print("-" * 50)

    constraint_sets = [
        (
            "Very Easy",
            {
                "overall_gc_min": 40.0,
                "overall_gc_max": 60.0,
                "primer_tm_tolerance": 2.0,
                "max_run_length": 5,
                "probe_tm_delta_min": 5.0,
                "probe_tm_delta_max": 15.0,
            },
        ),
        (
            "Easy",
            {
                "overall_gc_min": 45.0,
                "overall_gc_max": 55.0,
                "primer_tm_tolerance": 1.0,
                "max_run_length": 4,
                "probe_tm_delta_min": 6.0,
                "probe_tm_delta_max": 12.0,
            },
        ),
        ("Default", {}),  # Use all defaults
        (
            "Hard",
            {
                "overall_gc_min": 49.5,
                "overall_gc_max": 50.5,
                "primer_tm_tolerance": 0.3,
                "max_run_length": 2,
                "probe_tm_delta_min": 8.5,
                "probe_tm_delta_max": 9.5,
            },
        ),
        (
            "Very Hard",
            {
                "overall_gc_min": 49.8,
                "overall_gc_max": 50.2,
                "primer_tm_tolerance": 0.1,
                "max_run_length": 1,
                "probe_tm_delta_min": 8.9,
                "probe_tm_delta_max": 9.1,
            },
        ),
    ]

    results = []

    for name, constraints in constraint_sets:
        print(f"\nTesting {name} constraints...")

        template = run_experiment(
            seq_length=75,
            primer_length=22,
            probe_length=25,
            primer_melt=54.6,
            debug=False,
            max_iterations=2000,
            **constraints,
        )

        if template:
            cost = template.cost()
            results.append((name, cost, "✅"))
            print(f"  ✅ Success! Cost: {cost:.2f}")
        else:
            results.append((name, float("inf"), "❌"))
            print(f"  ❌ Failed")

    # Summary
    print(f"\nConstraint Difficulty Summary:")
    print("Difficulty | Result | Cost")
    print("-" * 30)

    for name, cost, status in results:
        cost_str = f"{cost:.2f}" if cost != float("inf") else "Failed"
        print(f"{name:<10} | {status:<6} | {cost_str}")


if __name__ == "__main__":
    main()
    demonstrate_constraint_effects()

    print("\n🎉 Custom constraints example completed!")
    print("\nKey insights:")
    print("- Relaxed constraints make optimization easier but may reduce specificity")
    print("- Strict constraints improve specificity but may fail more often")
    print("- Custom probe ΔTm allows optimization for different assay types")
    print("- Run length tolerance affects sequence diversity")
    print("- Constraint difficulty significantly impacts success rate")
    print("\nNext steps:")
    print("- Experiment with different constraint combinations for your targets")
    print("- Use relaxed constraints for initial screening, strict for final design")
    print("- Consider your experimental requirements when setting constraints")
