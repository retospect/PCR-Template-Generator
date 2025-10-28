#!/bin/bash
# PCR Template Generator - Basic CLI Examples
# 
# This script demonstrates basic command-line usage of the PCR Template Generator.
# Make sure the package is installed: pip install pcr-template-generator
#
# Usage: bash cli_basic.sh

echo "🧬 PCR Template Generator - Basic CLI Examples"
echo "=============================================="

# Check if the command is available
if ! command -v pcr-template-generator &> /dev/null; then
    echo "❌ pcr-template-generator command not found!"
    echo "Please install the package: pip install pcr-template-generator"
    exit 1
fi

echo "✅ PCR Template Generator is installed"
echo

# Example 1: Generate a single template with default parameters
echo "1️⃣ Generating single template with default parameters..."
echo "Command: pcr-template-generator"
echo "----------------------------------------"
pcr-template-generator
echo

# Example 2: Generate template with debug output
echo "2️⃣ Generating template with debug output..."
echo "Command: pcr-template-generator --debug"
echo "----------------------------------------"
pcr-template-generator --debug
echo

# Example 3: Generate template with custom parameters
echo "3️⃣ Generating template with custom parameters..."
echo "Command: pcr-template-generator --seq-length 80 --primer-length 20 --verbose"
echo "----------------------------------------"
pcr-template-generator --seq-length 80 --primer-length 20 --verbose
echo

# Example 4: Generate multiple templates
echo "4️⃣ Generating multiple templates..."
echo "Command: pcr-template-generator --count 3 --verbose"
echo "----------------------------------------"
pcr-template-generator --count 3 --verbose
echo

# Example 5: Quick generation with limited iterations
echo "5️⃣ Quick generation (limited iterations)..."
echo "Command: pcr-template-generator --max-iterations 1000 --debug"
echo "----------------------------------------"
pcr-template-generator --max-iterations 1000 --debug
echo

# Example 6: High-stringency template
echo "6️⃣ High-stringency template..."
echo "Command: pcr-template-generator --primer-melt 58.0 --max-iterations 5000 --verbose"
echo "----------------------------------------"
pcr-template-generator --primer-melt 58.0 --max-iterations 5000 --verbose
echo

echo "🎉 Basic CLI examples completed!"
echo
echo "Next steps:"
echo "- Try cli_batch.sh for batch processing examples"
echo "- Try cli_analysis.sh for sequence analysis workflows"
echo "- Run 'pcr-template-generator --help' for all available options"
