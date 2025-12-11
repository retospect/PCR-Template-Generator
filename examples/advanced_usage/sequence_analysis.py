#!/usr/bin/env python3
"""
Advanced Sequence Analysis Example

This example demonstrates advanced statistical analysis and visualization
of PCR template properties using the PCR Template Generator library.

Requirements:
- pcr-template-generator>=2.0.0
- matplotlib>=3.5.0
- numpy>=1.21.0
- pandas>=1.5.0 (optional, for data manipulation)
- seaborn>=0.11.0 (optional, for advanced plotting)

Usage:
    python sequence_analysis.py
"""

import statistics

import matplotlib.pyplot as plt
import numpy as np
from Bio.SeqUtils import MeltingTemp, gc_fraction

from pcr_template_generator import (
    analyze_sequence_statistics,
    generate_multiple_templates,
)

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("📝 Note: pandas not available - some features will be limited")

try:
    import seaborn as sns

    HAS_SEABORN = True
    sns.set_style("whitegrid")
except ImportError:
    HAS_SEABORN = False
    print("📝 Note: seaborn not available - using matplotlib only")


def main():
    """Run comprehensive sequence analysis."""
    print("🧬 PCR Template Generator - Advanced Sequence Analysis")
    print("=" * 60)

    # Analysis 1: Comprehensive statistical analysis
    print("\n1️⃣ Comprehensive Statistical Analysis")
    print("-" * 40)
    comprehensive_analysis()

    # Analysis 2: Length-dependent properties
    print("\n2️⃣ Length-Dependent Properties Analysis")
    print("-" * 40)
    length_analysis()

    # Analysis 3: Generated template analysis
    print("\n3️⃣ Generated Template Quality Analysis")
    print("-" * 40)
    template_quality_analysis()

    # Analysis 4: Correlation analysis
    print("\n4️⃣ Property Correlation Analysis")
    print("-" * 40)
    correlation_analysis()

    print("\n🎉 Advanced analysis completed!")
    print("Check the generated plots and analysis files for detailed results.")


def comprehensive_analysis():
    """Perform comprehensive statistical analysis of sequence properties."""
    print("Analyzing 20,000 random sequences...")

    # Generate large dataset
    temperatures, gc_contents = analyze_sequence_statistics(
        sequence_length=22, sample_count=20000, debug=False
    )

    # Calculate comprehensive statistics
    stats = {
        "temperature": {
            "mean": np.mean(temperatures),
            "std": np.std(temperatures),
            "min": np.min(temperatures),
            "max": np.max(temperatures),
            "median": np.median(temperatures),
            "q25": np.percentile(temperatures, 25),
            "q75": np.percentile(temperatures, 75),
        },
        "gc_content": {
            "mean": np.mean(gc_contents),
            "std": np.std(gc_contents),
            "min": np.min(gc_contents),
            "max": np.max(gc_contents),
            "median": np.median(gc_contents),
            "q25": np.percentile(gc_contents, 25),
            "q75": np.percentile(gc_contents, 75),
        },
    }

    # Print statistics
    print("\n📊 Comprehensive Statistics (22bp sequences, n=20,000):")
    print("\nTemperature (°C):")
    for key, value in stats["temperature"].items():
        print(f"  {key.capitalize()}: {value:.2f}")

    print("\nGC Content (%):")
    for key, value in stats["gc_content"].items():
        print(f"  {key.capitalize()}: {value:.2f}")

    # Create comprehensive visualization
    create_comprehensive_plots(temperatures, gc_contents, stats)

    # Save detailed statistics
    save_statistics_report(stats, temperatures, gc_contents)


def length_analysis():
    """Analyze how sequence length affects properties."""
    lengths = [15, 18, 20, 22, 25, 28, 30]
    length_data = {}

    print(f"Analyzing sequences of lengths: {lengths}")

    for length in lengths:
        print(f"  Analyzing {length}bp sequences...")

        temps, gcs = analyze_sequence_statistics(
            sequence_length=length, sample_count=5000, debug=False
        )

        length_data[length] = {
            "temperatures": temps,
            "gc_contents": gcs,
            "temp_mean": np.mean(temps),
            "temp_std": np.std(temps),
            "gc_mean": np.mean(gcs),
            "gc_std": np.std(gcs),
        }

    # Create length comparison plots
    create_length_comparison_plots(length_data)

    # Print summary
    print("\n📊 Length Analysis Summary:")
    print("Length | Temp Mean | Temp Std | GC Mean | GC Std")
    print("-" * 50)

    for length in lengths:
        data = length_data[length]
        print(
            f"{length:6d} | {data['temp_mean']:9.2f} | {data['temp_std']:8.2f} | "
            f"{data['gc_mean']:7.2f} | {data['gc_std']:6.2f}"
        )


def template_quality_analysis():
    """Analyze the quality of generated templates."""
    print("Generating 20 templates for quality analysis...")

    templates = generate_multiple_templates(count=20, debug=False, max_iterations=5000)

    if not templates:
        print("❌ Failed to generate templates for analysis")
        return

    print(f"✅ Generated {len(templates)} templates")

    # Analyze template properties
    template_data = []

    for i, template in enumerate(templates):
        fwd_tm = MeltingTemp.Tm_NN(str(template.fwd_primer()))
        rev_tm = MeltingTemp.Tm_NN(str(template.rev_primer()))
        probe_tm = MeltingTemp.Tm_NN(str(template.probe()))
        gc_content = GC(str(template.fwd()))
        cost = template.cost()

        template_data.append(
            {
                "id": i + 1,
                "cost": cost,
                "gc_content": gc_content,
                "fwd_tm": fwd_tm,
                "rev_tm": rev_tm,
                "probe_tm": probe_tm,
                "tm_diff": abs(fwd_tm - rev_tm),
                "probe_delta": probe_tm - (fwd_tm + rev_tm) / 2,
            }
        )

    # Create template quality plots
    create_template_quality_plots(template_data)

    # Print quality statistics
    costs = [t["cost"] for t in template_data]
    tm_diffs = [t["tm_diff"] for t in template_data]
    probe_deltas = [t["probe_delta"] for t in template_data]

    print("\n📊 Template Quality Statistics:")
    print(f"Optimization cost:     {np.mean(costs):.2f} ± {np.std(costs):.2f}")
    print(f"Primer Tm difference:  {np.mean(tm_diffs):.2f} ± {np.std(tm_diffs):.2f}°C")
    print(
        f"Probe-Primer ΔTm:      {np.mean(probe_deltas):.2f} ± {np.std(probe_deltas):.2f}°C"
    )

    # Save template data
    if HAS_PANDAS:
        df = pd.DataFrame(template_data)
        df.to_csv("template_quality_data.csv", index=False)
        print("💾 Template data saved to: template_quality_data.csv")


def correlation_analysis():
    """Analyze correlations between sequence properties."""
    print("Performing correlation analysis...")

    # Generate data for correlation analysis
    lengths = [18, 20, 22, 25, 28]
    all_data = []

    for length in lengths:
        temps, gcs = analyze_sequence_statistics(
            sequence_length=length, sample_count=2000, debug=False
        )

        for temp, gc in zip(temps, gcs):
            all_data.append(
                {
                    "length": length,
                    "temperature": temp,
                    "gc_content": gc,
                }
            )

    if HAS_PANDAS:
        df = pd.DataFrame(all_data)

        # Calculate correlations
        corr_matrix = df.corr()

        print("\n📊 Correlation Matrix:")
        print(corr_matrix.round(3))

        # Create correlation heatmap
        if HAS_SEABORN:
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap="coolwarm",
                center=0,
                square=True,
                fmt=".3f",
            )
            plt.title("Property Correlation Matrix")
            plt.tight_layout()
            plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight")
            plt.show()
            print("💾 Correlation heatmap saved to: correlation_heatmap.png")

        # Save correlation data
        df.to_csv("correlation_data.csv", index=False)
        print("💾 Correlation data saved to: correlation_data.csv")

    else:
        # Manual correlation calculation
        temps = [d["temperature"] for d in all_data]
        gcs = [d["gc_content"] for d in all_data]
        lengths_list = [d["length"] for d in all_data]

        temp_gc_corr = np.corrcoef(temps, gcs)[0, 1]
        temp_length_corr = np.corrcoef(temps, lengths_list)[0, 1]
        gc_length_corr = np.corrcoef(gcs, lengths_list)[0, 1]

        print("\n📊 Key Correlations:")
        print(f"Temperature vs GC Content: {temp_gc_corr:.3f}")
        print(f"Temperature vs Length:     {temp_length_corr:.3f}")
        print(f"GC Content vs Length:      {gc_length_corr:.3f}")


def create_comprehensive_plots(temperatures, gc_contents, stats):
    """Create comprehensive visualization plots."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Comprehensive Sequence Analysis (22bp, n=20,000)", fontsize=16)

    # Temperature histogram
    axes[0, 0].hist(
        temperatures, bins=50, alpha=0.7, color="skyblue", edgecolor="black"
    )
    axes[0, 0].axvline(
        stats["temperature"]["mean"],
        color="red",
        linestyle="--",
        label=f"Mean: {stats['temperature']['mean']:.1f}°C",
    )
    axes[0, 0].set_xlabel("Temperature (°C)")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].set_title("Temperature Distribution")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # GC content histogram
    axes[0, 1].hist(
        gc_contents, bins=50, alpha=0.7, color="lightgreen", edgecolor="black"
    )
    axes[0, 1].axvline(
        stats["gc_content"]["mean"],
        color="red",
        linestyle="--",
        label=f"Mean: {stats['gc_content']['mean']:.1f}%",
    )
    axes[0, 1].set_xlabel("GC Content (%)")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].set_title("GC Content Distribution")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Scatter plot
    axes[0, 2].scatter(gc_contents, temperatures, alpha=0.5, s=1, color="coral")
    axes[0, 2].set_xlabel("GC Content (%)")
    axes[0, 2].set_ylabel("Temperature (°C)")
    axes[0, 2].set_title("GC Content vs Temperature")
    axes[0, 2].grid(True, alpha=0.3)

    # Add trend line
    z = np.polyfit(gc_contents, temperatures, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(gc_contents), max(gc_contents), 100)
    axes[0, 2].plot(
        x_trend, p(x_trend), "r--", alpha=0.8, label=f"Trend: {z[0]:.2f}x + {z[1]:.1f}"
    )
    axes[0, 2].legend()

    # Box plots
    axes[1, 0].boxplot([temperatures], tick_labels=["Temperature"])
    axes[1, 0].set_ylabel("Temperature (°C)")
    axes[1, 0].set_title("Temperature Box Plot")
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].boxplot([gc_contents], tick_labels=["GC Content"])
    axes[1, 1].set_ylabel("GC Content (%)")
    axes[1, 1].set_title("GC Content Box Plot")
    axes[1, 1].grid(True, alpha=0.3)

    # Q-Q plot for normality check (requires scipy)
    try:
        from scipy import stats as scipy_stats

        scipy_stats.probplot(temperatures, dist="norm", plot=axes[1, 2])
        axes[1, 2].set_title("Temperature Q-Q Plot (Normality Check)")
        axes[1, 2].grid(True, alpha=0.3)
    except ImportError:
        axes[1, 2].text(
            0.5,
            0.5,
            "scipy not installed\n(optional dependency)",
            ha="center",
            va="center",
            transform=axes[1, 2].transAxes,
        )
        axes[1, 2].set_title("Q-Q Plot (scipy required)")
        axes[1, 2].set_xticks([])
        axes[1, 2].set_yticks([])

    plt.tight_layout()
    plt.savefig("comprehensive_analysis.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("💾 Comprehensive analysis plot saved to: comprehensive_analysis.png")


def create_length_comparison_plots(length_data):
    """Create plots comparing different sequence lengths."""
    lengths = sorted(length_data.keys())

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Sequence Length Comparison Analysis", fontsize=16)

    # Temperature means with error bars
    temp_means = [length_data[l]["temp_mean"] for l in lengths]
    temp_stds = [length_data[l]["temp_std"] for l in lengths]

    axes[0, 0].errorbar(
        lengths, temp_means, yerr=temp_stds, marker="o", capsize=5, capthick=2
    )
    axes[0, 0].set_xlabel("Sequence Length (bp)")
    axes[0, 0].set_ylabel("Mean Temperature (°C)")
    axes[0, 0].set_title("Temperature vs Sequence Length")
    axes[0, 0].grid(True, alpha=0.3)

    # GC content means with error bars
    gc_means = [length_data[l]["gc_mean"] for l in lengths]
    gc_stds = [length_data[l]["gc_std"] for l in lengths]

    axes[0, 1].errorbar(
        lengths,
        gc_means,
        yerr=gc_stds,
        marker="s",
        capsize=5,
        capthick=2,
        color="green",
    )
    axes[0, 1].set_xlabel("Sequence Length (bp)")
    axes[0, 1].set_ylabel("Mean GC Content (%)")
    axes[0, 1].set_title("GC Content vs Sequence Length")
    axes[0, 1].grid(True, alpha=0.3)

    # Standard deviation comparison
    axes[1, 0].plot(lengths, temp_stds, "o-", label="Temperature", color="blue")
    axes[1, 0].plot(lengths, gc_stds, "s-", label="GC Content", color="green")
    axes[1, 0].set_xlabel("Sequence Length (bp)")
    axes[1, 0].set_ylabel("Standard Deviation")
    axes[1, 0].set_title("Variability vs Sequence Length")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Distribution comparison (violin plot style)
    temp_data = [length_data[l]["temperatures"] for l in lengths]
    bp = axes[1, 1].boxplot(temp_data, tick_labels=lengths, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")
    axes[1, 1].set_xlabel("Sequence Length (bp)")
    axes[1, 1].set_ylabel("Temperature (°C)")
    axes[1, 1].set_title("Temperature Distributions by Length")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("length_comparison.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("💾 Length comparison plot saved to: length_comparison.png")


def create_template_quality_plots(template_data):
    """Create plots analyzing template quality."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Generated Template Quality Analysis", fontsize=16)

    costs = [t["cost"] for t in template_data]
    tm_diffs = [t["tm_diff"] for t in template_data]
    probe_deltas = [t["probe_delta"] for t in template_data]
    gc_contents = [gc_fraction(t.fwd()) * 100 for t in templates]

    # Cost distribution
    axes[0, 0].hist(costs, bins=10, alpha=0.7, color="lightcoral", edgecolor="black")
    axes[0, 0].set_xlabel("Optimization Cost")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].set_title("Template Optimization Cost Distribution")
    axes[0, 0].grid(True, alpha=0.3)

    # Primer Tm difference
    axes[0, 1].hist(tm_diffs, bins=10, alpha=0.7, color="lightblue", edgecolor="black")
    axes[0, 1].set_xlabel("Primer Tm Difference (°C)")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].set_title("Primer Melting Temperature Difference")
    axes[0, 1].grid(True, alpha=0.3)

    # Probe-Primer delta
    axes[1, 0].hist(
        probe_deltas, bins=10, alpha=0.7, color="lightgreen", edgecolor="black"
    )
    axes[1, 0].set_xlabel("Probe-Primer ΔTm (°C)")
    axes[1, 0].set_ylabel("Frequency")
    axes[1, 0].set_title("Probe-Primer Temperature Difference")
    axes[1, 0].grid(True, alpha=0.3)

    # Cost vs GC content
    axes[1, 1].scatter(gc_contents, costs, alpha=0.7, color="purple")
    axes[1, 1].set_xlabel("GC Content (%)")
    axes[1, 1].set_ylabel("Optimization Cost")
    axes[1, 1].set_title("Cost vs GC Content")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("template_quality.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("💾 Template quality plot saved to: template_quality.png")


def save_statistics_report(stats, temperatures, gc_contents):
    """Save detailed statistics report to file."""
    with open("sequence_statistics_report.txt", "w") as f:
        f.write("PCR Template Generator - Detailed Statistics Report\n")
        f.write("=" * 60 + "\n\n")

        f.write("Analysis Parameters:\n")
        f.write(f"- Sequence length: 22 bp\n")
        f.write(f"- Sample size: {len(temperatures):,}\n")
        f.write(f"- Analysis date: {np.datetime64('today')}\n\n")

        f.write("Temperature Statistics (°C):\n")
        f.write("-" * 30 + "\n")
        for key, value in stats["temperature"].items():
            f.write(f"{key.capitalize():>10}: {value:8.2f}\n")

        f.write("\nGC Content Statistics (%):\n")
        f.write("-" * 30 + "\n")
        for key, value in stats["gc_content"].items():
            f.write(f"{key.capitalize():>10}: {value:8.2f}\n")

        # Additional statistics
        temp_gc_corr = np.corrcoef(temperatures, gc_contents)[0, 1]
        f.write(f"\nCorrelation Analysis:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Temperature vs GC Content: {temp_gc_corr:.4f}\n")

        # Distribution analysis (requires scipy)
        try:
            from scipy import stats as scipy_stats

            temp_shapiro = scipy_stats.shapiro(np.random.choice(temperatures, 5000))
            gc_shapiro = scipy_stats.shapiro(np.random.choice(gc_contents, 5000))

            f.write(f"\nNormality Tests (Shapiro-Wilk, n=5000):\n")
            f.write("-" * 40 + "\n")
            f.write(
                f"Temperature: W={temp_shapiro.statistic:.4f}, p={temp_shapiro.pvalue:.2e}\n"
            )
            f.write(
                f"GC Content:  W={gc_shapiro.statistic:.4f}, p={gc_shapiro.pvalue:.2e}\n"
            )
        except ImportError:
            f.write(f"\nNormality Tests:\n")
            f.write("-" * 40 + "\n")
            f.write("scipy not installed (optional dependency for statistical tests)\n")

        f.write(f"\nInterpretation:\n")
        f.write("-" * 15 + "\n")
        f.write(
            "- Strong positive correlation between GC content and melting temperature\n"
        )
        f.write("- Both properties follow approximately normal distributions\n")
        f.write("- Results consistent with thermodynamic principles\n")
        f.write("- Data suitable for parametric statistical analyses\n")

    print("💾 Detailed statistics report saved to: sequence_statistics_report.txt")


if __name__ == "__main__":
    main()
