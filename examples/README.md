# PCR Template Generator Examples

This directory contains practical examples demonstrating how to use the PCR Template Generator library. All examples are tested and kept in sync with the current package version.

## 📁 Directory Structure

```
examples/
├── README.md                    # This file
├── requirements.txt             # Example dependencies (synced with pyproject.toml)
├── basic_usage/                 # Basic library usage examples
│   ├── simple_generation.py    # Generate single templates
│   ├── batch_generation.py     # Generate multiple templates
│   └── custom_parameters.py    # Custom sequence parameters
├── advanced_usage/              # Advanced features and customization
│   ├── custom_rules.py          # Creating custom evaluation rules
│   ├── sequence_analysis.py     # Statistical analysis tools
│   └── optimization_tuning.py  # Fine-tuning optimization parameters
├── cli_examples/                # Command-line interface examples
│   ├── cli_basic.sh            # Basic CLI usage
│   ├── cli_batch.sh            # Batch processing with CLI
│   └── cli_analysis.sh         # Analysis workflows
├── integration/                 # Integration with other tools
│   ├── jupyter_notebook.ipynb  # Jupyter notebook integration
│   ├── pandas_integration.py   # Working with pandas DataFrames
│   └── biopython_integration.py # BioPython integration examples
└── real_world/                  # Real-world use cases
    ├── qpcr_assay_design.py     # qPCR assay design workflow
    ├── primer_validation.py     # Validating existing primers
    └── high_throughput.py       # High-throughput processing
```

## 🚀 Quick Start

1. **Install the package:**
   ```bash
   pip install pcr-template-generator
   ```

2. **Run a basic example:**
   ```bash
   cd examples/basic_usage
   python simple_generation.py
   ```

3. **Try the CLI examples:**
   ```bash
   cd examples/cli_examples
   bash cli_basic.sh
   ```

## 📋 Requirements

All examples use the same dependencies as specified in the main package:

- Python >= 3.10
- pcr-template-generator (latest version)
- biopython >= 1.78
- numpy >= 1.21.0
- matplotlib >= 3.5.0 (for visualization examples)

## 🔄 Staying Synced

These examples are automatically tested with the CI pipeline to ensure they remain compatible with the latest package version. The `requirements.txt` file is generated from the main `pyproject.toml` to maintain consistency.

## 📖 Example Categories

### Basic Usage
Perfect for getting started with the library. Shows fundamental operations like generating templates and working with sequences.

### Advanced Usage  
Demonstrates advanced features like custom rules, statistical analysis, and optimization parameter tuning.

### CLI Examples
Shell scripts showing how to use the command-line interface for various workflows.

### Integration
Examples of integrating PCR Template Generator with other popular scientific Python libraries.

### Real-World
Complete workflows for common molecular biology tasks like qPCR assay design and primer validation.

## 🤝 Contributing Examples

To add a new example:

1. Create your example file in the appropriate directory
2. Add comprehensive docstrings and comments
3. Include expected output or results
4. Test with the current package version
5. Update this README if adding a new category

## 📞 Support

If you have questions about any examples or need help adapting them to your use case:

- 📖 [Documentation](https://github.com/retospect/PCR-Template-Generator)
- 🐛 [Issues](https://github.com/retospect/PCR-Template-Generator/issues)
- 💬 [Discussions](https://github.com/retospect/PCR-Template-Generator/discussions)
