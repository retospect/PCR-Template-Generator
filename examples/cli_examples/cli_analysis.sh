#!/bin/bash
# PCR Template Generator - Analysis CLI Examples
# 
# This script demonstrates sequence analysis workflows using the CLI.
# Shows how to analyze sequence properties and statistics.
#
# Usage: bash cli_analysis.sh

echo "🧬 PCR Template Generator - Analysis Examples"
echo "============================================="

# Check if the command is available
if ! command -v pcr-template-generator &> /dev/null; then
    echo "❌ pcr-template-generator command not found!"
    echo "Please install the package: pip install pcr-template-generator"
    exit 1
fi

# Create output directory for analysis results
ANALYSIS_DIR="analysis_results"
mkdir -p "$ANALYSIS_DIR"
echo "📁 Created analysis directory: $ANALYSIS_DIR"
echo

# Example 1: Basic sequence analysis
echo "1️⃣ Basic sequence statistics analysis..."
echo "Command: pcr-template-generator --analyze --samples 1000"
echo "----------------------------------------"
pcr-template-generator --analyze --samples 1000 > "$ANALYSIS_DIR/basic_analysis.txt" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Basic analysis completed"
    echo "Results saved to: $ANALYSIS_DIR/basic_analysis.txt"
    
    # Show a summary of the results
    echo "📊 Analysis Summary:"
    grep -E "(Temperature|GC content|range)" "$ANALYSIS_DIR/basic_analysis.txt" | head -5
else
    echo "❌ Basic analysis failed"
fi
echo

# Example 2: Large-scale analysis
echo "2️⃣ Large-scale sequence analysis..."
echo "Command: pcr-template-generator --analyze --samples 10000 --verbose"
echo "----------------------------------------"
pcr-template-generator --analyze --samples 10000 --verbose > "$ANALYSIS_DIR/large_scale_analysis.txt" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Large-scale analysis completed"
    echo "Results saved to: $ANALYSIS_DIR/large_scale_analysis.txt"
    
    # Check if plot was generated
    if [ -f "sequence_analysis.png" ]; then
        mv "sequence_analysis.png" "$ANALYSIS_DIR/"
        echo "📈 Analysis plot saved to: $ANALYSIS_DIR/sequence_analysis.png"
    fi
else
    echo "❌ Large-scale analysis failed"
fi
echo

# Example 3: Analysis with different sequence lengths
echo "3️⃣ Comparative analysis across sequence lengths..."
echo "----------------------------------------"

for length in 18 22 25 30; do
    echo "Analyzing ${length}bp sequences..."
    
    # Note: The --analyze mode analyzes random sequences of the specified primer length
    # This gives us insights into how sequence length affects properties
    pcr-template-generator \
        --analyze \
        --samples 5000 \
        --primer-length $length \
        > "$ANALYSIS_DIR/analysis_${length}bp.txt" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✅ ${length}bp analysis completed"
        
        # Extract key statistics
        TEMP_MEAN=$(grep "Temperature:" "$ANALYSIS_DIR/analysis_${length}bp.txt" | grep -o '[0-9]\+\.[0-9]\+°C' | head -1)
        GC_MEAN=$(grep "GC content:" "$ANALYSIS_DIR/analysis_${length}bp.txt" | grep -o '[0-9]\+\.[0-9]\+%' | head -1)
        
        echo "    Mean temperature: $TEMP_MEAN"
        echo "    Mean GC content: $GC_MEAN"
    else
        echo "  ❌ ${length}bp analysis failed"
    fi
done
echo

# Example 4: Create comparative analysis report
echo "4️⃣ Creating comparative analysis report..."
echo "----------------------------------------"

REPORT_FILE="$ANALYSIS_DIR/comparative_report.txt"

cat > "$REPORT_FILE" << EOF
PCR Template Generator - Comparative Analysis Report
===================================================

Generated on: $(date)

This report compares sequence statistics across different lengths
to help understand the relationship between sequence length and
melting temperature/GC content properties.

Analysis Results:
-----------------

EOF

# Extract and format results from each analysis
for length in 18 22 25 30; do
    ANALYSIS_FILE="$ANALYSIS_DIR/analysis_${length}bp.txt"
    
    if [ -f "$ANALYSIS_FILE" ]; then
        echo "${length}bp sequences:" >> "$REPORT_FILE"
        
        # Extract temperature and GC statistics
        grep -E "(Temperature|GC content)" "$ANALYSIS_FILE" | while read line; do
            echo "  $line" >> "$REPORT_FILE"
        done
        
        echo "" >> "$REPORT_FILE"
    fi
done

cat >> "$REPORT_FILE" << EOF

Interpretation:
--------------

- Longer sequences generally have more stable melting temperatures
- GC content distribution becomes more centered around 50% with length
- Temperature ranges narrow as sequence length increases
- These patterns help explain why longer primers are often more reliable

Recommendations:
---------------

- For routine PCR: 20-25bp primers with ~50% GC content
- For high-stringency applications: 22-25bp primers
- For multiplex PCR: Ensure all primers have similar Tm values
- Consider sequence length when designing primer sets

EOF

echo "✅ Comparative report created: $(basename "$REPORT_FILE")"
echo

# Example 5: Quick analysis for different applications
echo "5️⃣ Application-specific analysis..."
echo "----------------------------------------"

# Define common PCR applications with their typical parameters
declare -A APPLICATIONS=(
    ["standard_pcr"]="22"
    ["qpcr"]="20"
    ["long_range"]="25"
    ["multiplex"]="24"
)

APP_REPORT="$ANALYSIS_DIR/application_analysis.txt"

cat > "$APP_REPORT" << EOF
PCR Template Generator - Application-Specific Analysis
=====================================================

Generated on: $(date)

This analysis examines sequence properties for different PCR applications:

EOF

for app in "${!APPLICATIONS[@]}"; do
    length="${APPLICATIONS[$app]}"
    
    echo "Analyzing $app (${length}bp primers)..."
    
    # Run quick analysis
    pcr-template-generator \
        --analyze \
        --samples 2000 \
        --primer-length $length \
        > "$ANALYSIS_DIR/temp_${app}.txt" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✅ $app analysis completed"
        
        # Add to report
        echo "$app (${length}bp primers):" >> "$APP_REPORT"
        echo "$(echo "$app" | tr '[:lower:]' '[:upper:]' | sed 's/./-/g')" >> "$APP_REPORT"
        
        grep -E "(Temperature|GC content)" "$ANALYSIS_DIR/temp_${app}.txt" | while read line; do
            echo "$line" >> "$APP_REPORT"
        done
        
        echo "" >> "$APP_REPORT"
        
        # Clean up temp file
        rm "$ANALYSIS_DIR/temp_${app}.txt"
    else
        echo "  ❌ $app analysis failed"
    fi
done

echo "✅ Application-specific analysis completed"
echo "Report saved to: $(basename "$APP_REPORT")"
echo

# Example 6: Generate analysis summary
echo "6️⃣ Generating final analysis summary..."
echo "----------------------------------------"

FINAL_SUMMARY="$ANALYSIS_DIR/analysis_summary.txt"

cat > "$FINAL_SUMMARY" << EOF
PCR Template Generator - Analysis Session Summary
================================================

Session Date: $(date)
Analysis Directory: $ANALYSIS_DIR

Files Generated:
---------------

EOF

# List all analysis files with descriptions
for file in "$ANALYSIS_DIR"/*.txt; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")
        SIZE=$(wc -l < "$file" 2>/dev/null || echo "0")
        
        case "$BASENAME" in
            "basic_analysis.txt")
                echo "📊 $BASENAME ($SIZE lines) - Basic sequence statistics (1,000 samples)" >> "$FINAL_SUMMARY"
                ;;
            "large_scale_analysis.txt")
                echo "📈 $BASENAME ($SIZE lines) - Large-scale analysis (10,000 samples)" >> "$FINAL_SUMMARY"
                ;;
            "analysis_"*"bp.txt")
                LENGTH=$(echo "$BASENAME" | grep -o '[0-9]\+')
                echo "🔬 $BASENAME ($SIZE lines) - ${LENGTH}bp sequence analysis" >> "$FINAL_SUMMARY"
                ;;
            "comparative_report.txt")
                echo "📋 $BASENAME ($SIZE lines) - Comparative analysis across lengths" >> "$FINAL_SUMMARY"
                ;;
            "application_analysis.txt")
                echo "🎯 $BASENAME ($SIZE lines) - Application-specific analysis" >> "$FINAL_SUMMARY"
                ;;
            *)
                echo "📄 $BASENAME ($SIZE lines)" >> "$FINAL_SUMMARY"
                ;;
        esac
    fi
done

# Check for plots
if [ -f "$ANALYSIS_DIR/sequence_analysis.png" ]; then
    echo "📈 sequence_analysis.png - Statistical plots and visualizations" >> "$FINAL_SUMMARY"
fi

cat >> "$FINAL_SUMMARY" << EOF

Total Analysis Files: $(find "$ANALYSIS_DIR" -name "*.txt" | wc -l)
Total Samples Analyzed: ~28,000 sequences

Key Insights:
------------

1. Sequence length significantly affects melting temperature stability
2. GC content distribution becomes more predictable with longer sequences  
3. Different PCR applications benefit from different primer lengths
4. Statistical analysis helps optimize primer design parameters

Next Steps:
----------

- Review individual analysis files for detailed statistics
- Use insights to guide primer design for your specific application
- Consider running additional analyses with custom parameters
- Apply findings to real primer design workflows

EOF

echo "✅ Final summary created: $(basename "$FINAL_SUMMARY")"
echo

echo "🎉 Analysis examples completed!"
echo
echo "📁 All results saved in: $ANALYSIS_DIR/"
echo "📋 Start with: $ANALYSIS_DIR/analysis_summary.txt"
echo
echo "Key files:"
echo "  - analysis_summary.txt: Overview of all analyses"
echo "  - comparative_report.txt: Length comparison insights"
echo "  - application_analysis.txt: Application-specific recommendations"
echo "  - sequence_analysis.png: Statistical visualizations (if generated)"
echo
echo "Next steps:"
echo "- Review the analysis results to understand sequence properties"
echo "- Use insights for your primer design workflows"
echo "- Try the Python examples in ../basic_usage/ for programmatic access"
