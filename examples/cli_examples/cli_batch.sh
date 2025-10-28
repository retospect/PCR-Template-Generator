#!/bin/bash
# PCR Template Generator - Batch Processing CLI Examples
# 
# This script demonstrates batch processing workflows using the CLI.
# Useful for generating multiple templates with different parameters.
#
# Usage: bash cli_batch.sh

echo "🧬 PCR Template Generator - Batch Processing Examples"
echo "===================================================="

# Check if the command is available
if ! command -v pcr-template-generator &> /dev/null; then
    echo "❌ pcr-template-generator command not found!"
    echo "Please install the package: pip install pcr-template-generator"
    exit 1
fi

# Create output directory
OUTPUT_DIR="batch_results"
mkdir -p "$OUTPUT_DIR"
echo "📁 Created output directory: $OUTPUT_DIR"
echo

# Example 1: Generate templates with different lengths
echo "1️⃣ Generating templates with different lengths..."
echo "----------------------------------------"

for length in 60 75 90; do
    echo "Generating ${length}bp template..."
    pcr-template-generator \
        --seq-length $length \
        --count 2 \
        --max-iterations 3000 \
        > "$OUTPUT_DIR/templates_${length}bp.txt" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ ${length}bp templates saved to $OUTPUT_DIR/templates_${length}bp.txt"
    else
        echo "❌ Failed to generate ${length}bp templates"
    fi
done
echo

# Example 2: Generate templates with different primer lengths
echo "2️⃣ Generating templates with different primer lengths..."
echo "----------------------------------------"

for primer_len in 18 22 25; do
    echo "Generating templates with ${primer_len}bp primers..."
    pcr-template-generator \
        --primer-length $primer_len \
        --count 2 \
        --max-iterations 3000 \
        --verbose \
        > "$OUTPUT_DIR/primers_${primer_len}bp.txt" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Templates with ${primer_len}bp primers saved"
    else
        echo "❌ Failed to generate templates with ${primer_len}bp primers"
    fi
done
echo

# Example 3: Generate templates with different melting temperatures
echo "3️⃣ Generating templates with different melting temperatures..."
echo "----------------------------------------"

for tm in 50.0 54.6 58.0; do
    echo "Generating templates with ${tm}°C primer Tm..."
    pcr-template-generator \
        --primer-melt $tm \
        --count 2 \
        --max-iterations 4000 \
        --verbose \
        > "$OUTPUT_DIR/tm_${tm}C.txt" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Templates with ${tm}°C Tm saved"
    else
        echo "❌ Failed to generate templates with ${tm}°C Tm"
    fi
done
echo

# Example 4: Parallel batch processing (if GNU parallel is available)
echo "4️⃣ Parallel batch processing (if available)..."
echo "----------------------------------------"

if command -v parallel &> /dev/null; then
    echo "GNU parallel detected - running parallel jobs..."
    
    # Create a list of parameter combinations
    cat > "$OUTPUT_DIR/param_combinations.txt" << EOF
--seq-length 70 --primer-length 20 --count 1
--seq-length 75 --primer-length 22 --count 1  
--seq-length 80 --primer-length 24 --count 1
EOF

    # Run in parallel
    parallel -j 3 "pcr-template-generator {} --max-iterations 2000 > $OUTPUT_DIR/parallel_{#}.txt 2>&1" :::: "$OUTPUT_DIR/param_combinations.txt"
    
    echo "✅ Parallel processing completed"
    echo "Results saved in $OUTPUT_DIR/parallel_*.txt"
else
    echo "GNU parallel not available - skipping parallel example"
    echo "Install with: sudo apt-get install parallel (Ubuntu) or brew install parallel (macOS)"
fi
echo

# Example 5: Batch processing with error handling
echo "5️⃣ Batch processing with error handling..."
echo "----------------------------------------"

SUCCESS_COUNT=0
TOTAL_COUNT=0

# Array of parameter sets to test
declare -a PARAM_SETS=(
    "--seq-length 60 --primer-length 18 --max-iterations 2000"
    "--seq-length 75 --primer-length 22 --max-iterations 3000"
    "--seq-length 90 --primer-length 25 --max-iterations 4000"
    "--seq-length 50 --primer-length 15 --max-iterations 1000"  # This might fail
)

for i in "${!PARAM_SETS[@]}"; do
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    PARAMS="${PARAM_SETS[$i]}"
    OUTPUT_FILE="$OUTPUT_DIR/batch_test_$((i+1)).txt"
    
    echo "Testing parameter set $((i+1)): $PARAMS"
    
    if pcr-template-generator $PARAMS --count 1 > "$OUTPUT_FILE" 2>&1; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo "  ✅ Success - saved to $(basename "$OUTPUT_FILE")"
    else
        echo "  ❌ Failed - check $(basename "$OUTPUT_FILE") for details"
    fi
done

echo
echo "📊 Batch processing summary:"
echo "  Total attempts: $TOTAL_COUNT"
echo "  Successful: $SUCCESS_COUNT"
echo "  Failed: $((TOTAL_COUNT - SUCCESS_COUNT))"
echo "  Success rate: $(( SUCCESS_COUNT * 100 / TOTAL_COUNT ))%"
echo

# Example 6: Create a summary report
echo "6️⃣ Creating summary report..."
echo "----------------------------------------"

SUMMARY_FILE="$OUTPUT_DIR/batch_summary.txt"

cat > "$SUMMARY_FILE" << EOF
PCR Template Generator - Batch Processing Summary
================================================

Generated on: $(date)
Output directory: $OUTPUT_DIR

Files generated:
EOF

# List all generated files with sizes
for file in "$OUTPUT_DIR"/*.txt; do
    if [ -f "$file" ] && [ "$file" != "$SUMMARY_FILE" ]; then
        SIZE=$(wc -l < "$file" 2>/dev/null || echo "0")
        echo "  $(basename "$file"): $SIZE lines" >> "$SUMMARY_FILE"
    fi
done

echo "" >> "$SUMMARY_FILE"
echo "Total files: $(find "$OUTPUT_DIR" -name "*.txt" -not -name "batch_summary.txt" | wc -l)" >> "$SUMMARY_FILE"

echo "✅ Summary report created: $(basename "$SUMMARY_FILE")"
echo

echo "🎉 Batch processing examples completed!"
echo
echo "Results saved in: $OUTPUT_DIR/"
echo "Summary report: $OUTPUT_DIR/batch_summary.txt"
echo
echo "Next steps:"
echo "- Review the generated templates in $OUTPUT_DIR/"
echo "- Try cli_analysis.sh for sequence analysis workflows"
echo "- Modify the parameters in this script for your specific needs"
