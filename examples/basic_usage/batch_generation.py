#!/usr/bin/env python3
"""
Batch PCR Template Generation Example

This example demonstrates how to generate multiple PCR templates
and analyze their properties for comparison and selection.

Requirements:
- pcr-template-generator>=1.0.0
- Python>=3.10

Usage:
    python batch_generation.py
"""

from pcr_template_generator import generate_multiple_templates
from Bio.SeqUtils import GC, MeltingTemp
import statistics


def main():
    """Generate multiple PCR templates and analyze them."""
    print("🧬 PCR Template Generator - Batch Generation Example")
    print("=" * 60)
    
    # Generate multiple templates
    template_count = 5
    print(f"Generating {template_count} optimized PCR templates...")
    print("This may take a few moments...")
    
    templates = generate_multiple_templates(
        count=template_count,
        debug=False,           # Disable debug for cleaner output
        max_iterations=3000    # Reasonable limit for demo
    )
    
    if not templates:
        print("❌ Failed to generate any templates")
        return
    
    print(f"\n✅ Successfully generated {len(templates)} templates!")
    
    # Display all templates
    print("\n📊 Generated Templates:")
    print("=" * 60)
    
    template_data = []
    
    for i, template in enumerate(templates, 1):
        print(f"\nTemplate {i}:")
        print("-" * 40)
        print(template.display())
        
        # Calculate properties
        fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
        rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
        probe_tm = MeltingTemp.Tm_NN(str(template.probe()))
        gc_content = GC(str(template.fwd()))
        cost = template.cost()
        
        template_data.append({
            'template': i,
            'cost': cost,
            'gc_content': gc_content,
            'fwd_tm': fwd_tm,
            'rev_tm': rev_tm,
            'probe_tm': probe_tm,
            'tm_diff': abs(fwd_tm - rev_tm),
            'sequence': template
        })
        
        print(f"Cost: {cost:.2f} | GC: {gc_content:.1f}% | "
              f"Primer Tm: {fwd_tm:.1f}°C/{rev_tm:.1f}°C | "
              f"Probe Tm: {probe_tm:.1f}°C")
    
    # Analyze the batch
    analyze_batch(template_data)
    
    # Recommend best template
    recommend_best_template(template_data)


def analyze_batch(template_data):
    """Analyze the batch of generated templates."""
    print("\n📈 Batch Analysis:")
    print("=" * 40)
    
    costs = [t['cost'] for t in template_data]
    gc_contents = [t['gc_content'] for t in template_data]
    tm_diffs = [t['tm_diff'] for t in template_data]
    
    print(f"Cost statistics:")
    print(f"  Mean: {statistics.mean(costs):.2f}")
    print(f"  Min:  {min(costs):.2f}")
    print(f"  Max:  {max(costs):.2f}")
    
    print(f"\nGC content statistics:")
    print(f"  Mean: {statistics.mean(gc_contents):.1f}%")
    print(f"  Min:  {min(gc_contents):.1f}%")
    print(f"  Max:  {max(gc_contents):.1f}%")
    
    print(f"\nPrimer Tm difference statistics:")
    print(f"  Mean: {statistics.mean(tm_diffs):.2f}°C")
    print(f"  Min:  {min(tm_diffs):.2f}°C")
    print(f"  Max:  {max(tm_diffs):.2f}°C")


def recommend_best_template(template_data):
    """Recommend the best template based on multiple criteria."""
    print("\n🏆 Template Recommendation:")
    print("=" * 40)
    
    # Sort by cost (lower is better)
    best_by_cost = min(template_data, key=lambda x: x['cost'])
    
    # Find template with most balanced primer Tm
    best_by_tm_balance = min(template_data, key=lambda x: x['tm_diff'])
    
    # Find template closest to 50% GC
    best_by_gc = min(template_data, key=lambda x: abs(x['gc_content'] - 50.0))
    
    print(f"Best by optimization cost: Template {best_by_cost['template']} (cost: {best_by_cost['cost']:.2f})")
    print(f"Best by primer Tm balance: Template {best_by_tm_balance['template']} (ΔTm: {best_by_tm_balance['tm_diff']:.2f}°C)")
    print(f"Best by GC content:        Template {best_by_gc['template']} (GC: {best_by_gc['gc_content']:.1f}%)")
    
    # Overall recommendation (weighted score)
    print("\n🎯 Overall Recommendation:")
    
    for template in template_data:
        # Calculate weighted score (lower is better)
        score = (
            template['cost'] * 1.0 +           # Cost weight
            template['tm_diff'] * 2.0 +        # Tm balance weight  
            abs(template['gc_content'] - 50.0) * 0.1  # GC content weight
        )
        template['score'] = score
    
    best_overall = min(template_data, key=lambda x: x['score'])
    
    print(f"Recommended template: Template {best_overall['template']}")
    print(f"  Overall score: {best_overall['score']:.2f}")
    print(f"  Cost: {best_overall['cost']:.2f}")
    print(f"  GC content: {best_overall['gc_content']:.1f}%")
    print(f"  Primer Tm difference: {best_overall['tm_diff']:.2f}°C")
    
    print("\nRecommended template layout:")
    print(best_overall['sequence'].display())


def save_templates_to_file(templates, filename="generated_templates.txt"):
    """Save generated templates to a file for later use."""
    print(f"\n💾 Saving templates to {filename}...")
    
    with open(filename, 'w') as f:
        f.write("PCR Template Generator - Batch Results\n")
        f.write("=" * 50 + "\n\n")
        
        for i, template in enumerate(templates, 1):
            f.write(f"Template {i}:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Forward primer: {template.fwd_primer()}\n")
            f.write(f"Reverse primer: {template.rev_primer()}\n")
            f.write(f"Probe:          {template.probe()}\n")
            f.write(f"Full sequence:  {template.fwd()}\n")
            f.write(f"Cost:           {template.cost():.2f}\n")
            f.write(f"GC content:     {GC(str(template.fwd())):.1f}%\n")
            f.write("\nLayout:\n")
            f.write(template.display())
            f.write("\n\n")
    
    print(f"✅ Templates saved to {filename}")


if __name__ == "__main__":
    main()
    
    print("\n🎉 Batch generation example completed!")
    print("\nNext steps:")
    print("- Try custom_parameters.py for parameter customization")
    print("- Check ../advanced_usage/ for more sophisticated examples")
    print("- Use the recommended template for your PCR experiments")
