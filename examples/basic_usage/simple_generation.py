#!/usr/bin/env python3
"""
Simple PCR Template Generation Example

This example demonstrates the basic usage of the PCR Template Generator
to create a single optimized DNA template for PCR primers and probes.

Requirements:
- pcr-template-generator>=2.0.0
- Python>=3.10

Usage:
    python simple_generation.py
"""

from pcr_template_generator import Sequence, run_experiment


def main():
    """Generate a single PCR template with default parameters."""
    print("🧬 PCR Template Generator - Simple Example")
    print("=" * 50)

    # Generate a single template with default parameters
    print("Generating optimized PCR template...")
    print("This may take a few moments...")

    template = run_experiment(
        debug=True,  # Show optimization progress
        max_iterations=5000,  # Limit iterations for faster demo
    )

    if template:
        print("\n✅ Successfully generated template!")
        print("\n📊 Template Layout:")
        print(template.display())

        print(f"\n📈 Final optimization cost: {template.cost():.2f}")

        # Show individual components
        print("\n🔬 Template Components:")
        print(f"Forward primer (5'→3'): {template.fwd_primer()}")
        print(f"Reverse primer (5'→3'): {template.rev_primer()}")
        print(f"Probe sequence:         {template.probe()}")
        print(f"Full template:          {template.fwd()}")

        # Show template properties
        from Bio.SeqUtils import MeltingTemp, gc_fraction

        print("\n📋 Template Properties:")
        print(f"Template length:        {len(template.fwd())} bp")
        print(f"GC content:             {gc_fraction(template.fwd()) * 100:.1f}%")
        print(
            f"Forward primer Tm:      {MeltingTemp.Tm_NN(str(template.fwd_primer())):.1f}°C"
        )
        print(
            f"Reverse primer Tm:      {MeltingTemp.Tm_NN(str(template.rev_primer())):.1f}°C"
        )
        print(
            f"Probe Tm:               {MeltingTemp.Tm_NN(str(template.probe())):.1f}°C"
        )

        # Show rule violations (if any)
        if template.cost() > 0:
            print("\n⚠️  Rule Violations:")
            print(template.rule_info())
        else:
            print("\n✅ Perfect template - all design rules satisfied!")

    else:
        print("\n❌ Failed to generate template within iteration limit")
        print("Try increasing max_iterations or adjusting parameters")


def demonstrate_custom_sequence():
    """Demonstrate working with a custom DNA sequence."""
    print("\n" + "=" * 50)
    print("🔬 Custom Sequence Analysis Example")
    print("=" * 50)

    # Create a sequence object with custom DNA
    custom_dna = (
        "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
    )

    sequence = Sequence(sequence=custom_dna)

    print(f"Custom sequence: {custom_dna}")
    print(f"Sequence length: {len(sequence.fwd())} bp")

    # Evaluate the sequence
    cost = sequence.cost()
    print(f"Design cost: {cost:.2f}")

    if cost > 0:
        print("\nRule violations:")
        print(sequence.rule_info())
    else:
        print("Perfect sequence - all design rules satisfied!")

    # Show the layout
    print("\nSequence layout:")
    print(sequence.display())


if __name__ == "__main__":
    main()
    demonstrate_custom_sequence()

    print("\n🎉 Example completed!")
    print("\nNext steps:")
    print("- Try batch_generation.py for multiple templates")
    print("- Try custom_parameters.py for parameter customization")
    print("- Check ../cli_examples/ for command-line usage")
