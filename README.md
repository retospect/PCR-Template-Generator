# PCR Template Generator

<!-- Dynamic PyPI badges -->
[![PyPI version](https://img.shields.io/pypi/v/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)
[![PyPI - Status](https://img.shields.io/pypi/status/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)

<!-- Dynamic CI/CD and test status badges -->
[![CI](https://github.com/retospect/PCR-Template-Generator/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/PCR-Template-Generator/actions/workflows/check.yml)
[![CodeQL](https://github.com/retospect/PCR-Template-Generator/actions/workflows/codeql.yml/badge.svg)](https://github.com/retospect/PCR-Template-Generator/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/retospect/PCR-Template-Generator/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/retospect/PCR-Template-Generator)
[![Tests](https://img.shields.io/github/actions/workflow/status/retospect/PCR-Template-Generator/check.yml?branch=main&label=tests)](https://github.com/retospect/PCR-Template-Generator/actions/workflows/check.yml)

<!-- Quality and maintenance badges -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

<!-- License and documentation badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-GitHub-blue.svg)](https://github.com/retospect/PCR-Template-Generator)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/retospect/PCR-Template-Generator/blob/main/PCR_Template_Generator.ipynb)

<!-- Repository stats and activity -->
[![GitHub stars](https://img.shields.io/github/stars/retospect/PCR-Template-Generator.svg?style=social&label=Star)](https://github.com/retospect/PCR-Template-Generator)
[![GitHub forks](https://img.shields.io/github/forks/retospect/PCR-Template-Generator.svg?style=social&label=Fork)](https://github.com/retospect/PCR-Template-Generator/fork)
[![GitHub issues](https://img.shields.io/github/issues/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator/pulls)
[![GitHub last commit](https://img.shields.io/github/last-commit/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator/commits/main)
[![GitHub release date](https://img.shields.io/github/release-date/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator/releases)

<!-- Additional package info -->
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pcr-template-generator.svg)](https://pypi.org/project/pcr-template-generator/)
[![GitHub repo size](https://img.shields.io/github/repo-size/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator)
[![Lines of code](https://img.shields.io/tokei/lines/github/retospect/PCR-Template-Generator.svg)](https://github.com/retospect/PCR-Template-Generator)

A Python library for generating optimized DNA templates for PCR primers and probes using simulated annealing.

---

## 📊 Badge Status Guide

### 📦 Package Information
| Badge | Description | Updates |
|-------|-------------|---------|
| ![PyPI version](https://img.shields.io/pypi/v/pcr-template-generator.svg) | Latest version on PyPI | When new version is published |
| ![PyPI downloads](https://img.shields.io/pypi/dm/pcr-template-generator.svg) | Monthly downloads from PyPI | Daily |
| ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pcr-template-generator.svg) | Supported Python versions | When pyproject.toml changes |
| ![PyPI - Status](https://img.shields.io/pypi/status/pcr-template-generator.svg) | Development status (Alpha/Beta/Stable) | When package metadata changes |
| ![PyPI - Wheel](https://img.shields.io/pypi/wheel/pcr-template-generator.svg) | Wheel distribution availability | When package is built |

### 🧪 Testing & Quality
| Badge | Description | Updates |
|-------|-------------|---------|
| ![CI](https://github.com/retospect/PCR-Template-Generator/actions/workflows/check.yml/badge.svg) | Continuous integration status | On every commit/PR |
| ![CodeQL](https://github.com/retospect/PCR-Template-Generator/actions/workflows/codeql.yml/badge.svg) | Security analysis status | Weekly + on commits |
| ![codecov](https://codecov.io/gh/retospect/PCR-Template-Generator/branch/main/graph/badge.svg) | Test coverage percentage | After CI runs |
| ![Tests](https://img.shields.io/github/actions/workflow/status/retospect/PCR-Template-Generator/check.yml?branch=main&label=tests) | Latest test run status | On every commit |

### 🔧 Code Quality
| Badge | Description | Updates |
|-------|-------------|---------|
| ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg) | Code formatting standard | Static |
| ![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336) | Import sorting standard | Static |
| ![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg) | Type checking enabled | Static |
| ![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg) | Security scanning enabled | Static |

### 📊 Repository Stats
| Badge | Description | Updates |
|-------|-------------|---------|
| ![GitHub stars](https://img.shields.io/github/stars/retospect/PCR-Template-Generator.svg) | Repository stars | Real-time |
| ![GitHub issues](https://img.shields.io/github/issues/retospect/PCR-Template-Generator.svg) | Open issues count | Real-time |
| ![GitHub last commit](https://img.shields.io/github/last-commit/retospect/PCR-Template-Generator.svg) | Last commit date | On every commit |
| ![Lines of code](https://img.shields.io/tokei/lines/github/retospect/PCR-Template-Generator.svg) | Total lines of code | Daily |

> **🔄 Dynamic Updates**: All badges automatically reflect the current state of the repository and PyPI package. No manual updates required!

---

## 🧬 Overview

PCR Template Generator creates DNA sequences that satisfy multiple constraints for PCR primer and probe design, including:

- **GC content optimization** - Maintains optimal GC content for primers and probes
- **Melting temperature matching** - Ensures primers have similar Tm values
- **Secondary structure avoidance** - Prevents hairpins and self-complementarity
- **Primer dimer prevention** - Ensures unique 3' ends to avoid primer dimers
- **GC clamping** - Adds proper GC clamps to primer 3' ends
- **Probe design** - Optimizes probe Tm to be ~8°C higher than primers

## 🚀 Quick Start

### Installation

```bash
pip install pcr-template-generator
```

### Basic Usage

```python
from pcr_template_generator import run_experiment

# Generate a single optimized template
template = run_experiment(debug=True)
if template:
    print(template.display())
```

### Command Line Interface

```bash
# Generate a single template
pcr-template-generator

# Generate multiple templates
pcr-template-generator --count 5

# Custom parameters
pcr-template-generator --seq-length 80 --primer-length 20 --debug

# Analyze sequence statistics
pcr-template-generator --analyze --samples 1000
```

### 📁 Comprehensive Examples

Explore the **[examples/](examples/)** directory for detailed usage examples:

- **[Basic Usage](examples/basic_usage/)** - Get started with simple template generation
- **[Advanced Usage](examples/advanced_usage/)** - Statistical analysis and custom rules  
- **[CLI Examples](examples/cli_examples/)** - Shell scripts for batch processing
- **[Integration](examples/integration/)** - Jupyter notebooks and library integration
- **[Real-World](examples/real_world/)** - Complete workflows for common tasks

Each example includes:
- ✅ **Tested code** that works with the current package version
- 📖 **Detailed documentation** and comments
- 🎯 **Specific use cases** and applications
- 📊 **Expected outputs** and results

**Quick start with examples:**
```bash
# Clone the repository or download examples
cd examples/basic_usage
python simple_generation.py

# Or try the CLI examples
cd ../cli_examples  
bash cli_basic.sh
```

## 📖 Detailed Usage

### Library API

```python
from pcr_template_generator import Sequence, run_experiment, generate_multiple_templates

# Generate single template with custom parameters
template = run_experiment(
    seq_length=75,           # Total template length
    primer_length=22,        # Primer length
    probe_length=25,         # Probe length  
    primer_melt=54.6,        # Target primer Tm (°C)
    probe_gap=3,             # Gap between probe and reverse primer
    max_iterations=10000,    # Maximum optimization iterations
    debug=True               # Enable debug output
)

# Generate template with custom design constraints
custom_template = run_experiment(
    seq_length=75,
    primer_length=22,
    probe_length=25,
    primer_melt=54.6,
    # Configurable design constraints
    probe_tm_delta_min=6.0,     # Minimum probe-primer Tm difference (°C)
    probe_tm_delta_max=8.0,     # Maximum probe-primer Tm difference (°C)
    primer_tm_tolerance=0.3,    # Allowed primer Tm difference (°C)
    max_run_length=2,           # Maximum run of identical bases
    overall_gc_min=48.0,        # Minimum overall GC content (%)
    overall_gc_max=52.0,        # Maximum overall GC content (%)
    debug=True
)

if template:
    print("Generated template:")
    print(template.display())
    print(f"Final cost: {template.cost():.2f}")
    
    # Access individual components
    print(f"Forward primer: {template.fwd_primer()}")
    print(f"Reverse primer: {template.rev_primer()}")
    print(f"Probe: {template.probe()}")

# Generate multiple templates
templates = generate_multiple_templates(count=10, debug=True)
for i, template in enumerate(templates, 1):
    print(f"Template {i}:")
    print(template.display())
    print()
```

### Working with Sequences

```python
from pcr_template_generator import Sequence

# Create sequence with custom DNA
seq = Sequence(sequence="atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc")

# Evaluate design quality
cost = seq.cost()
print(f"Design cost: {cost}")

# View rule violations
if cost > 0:
    print("Rule violations:")
    print(seq.rule_info())

# Mutate sequence
seq.mutate(how_many=5)
new_cost = seq.cost()
print(f"New cost after mutation: {new_cost}")
```

### Template Structure

The generated templates follow this structure:

```
Forward-primer---CLAMP   -----probe---------------
123456789 123456789 12   123456789 123456789 12345
atgcatgcatgcatgcatgcag   ttgaagcacgccgttgtttgccaca
atgcatgcatgcatgcatgcagtagttgaagcacgccgttgtttgccacagtagcagattccgccctttatccat
tacgtacgtacgtacgtacgtcatcaacttcgtgcggcaacaaacggtgtcatcgtctaaggcgggaaataggta
                                                     cgtctaaggcgggaaataggta
                                                     CLAMP---Reverse-primer
                                                     21 987654321 987654321
```

## 🔬 Algorithm

The generator uses **simulated annealing** optimization:

1. **Initialize** with a random DNA sequence
2. **Evaluate** sequence against design rules (GC content, Tm, secondary structures, etc.)
3. **Mutate** random bases in the sequence
4. **Accept** mutations that improve the design cost
5. **Repeat** until an acceptable solution is found

### Design Rules

The algorithm enforces these molecular biology constraints:

| Rule | Purpose | Target |
|------|---------|--------|
| GC Content | Optimal amplification | 49-51% overall, primers |
| Melting Temperature | Primer matching | ±0.5°C between primers |
| GC Clamp | Primer stability | 3/5 bases G/C at 3' end |
| Long Runs | Avoid polymerase slippage | Max 3 identical bases |
| Secondary Structure | Prevent hairpins | Max 4bp complementarity |
| Primer Dimers | Unique 3' ends | 4bp 3' ends appear once |
| Probe Tm | Optimal probe binding | +8°C above primer Tm |

## 📊 Analysis Tools

### Sequence Statistics

```python
from pcr_template_generator import analyze_sequence_statistics

# Analyze random sequences
temperatures, gc_contents = analyze_sequence_statistics(
    sequence_length=22,
    sample_count=10000,
    debug=True
)

# Results show relationship between GC content and melting temperature
print(f"Mean temperature: {np.mean(temperatures):.1f}°C")
print(f"Mean GC content: {np.mean(gc_contents):.1f}%")
```

### Interactive Analysis

Try the interactive Jupyter notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/retospect/PCR-Template-Generator/blob/main/PCR_Template_Generator.ipynb)

## 🛠 Development

### Setup

```bash
git clone https://github.com/retospect/PCR-Template-Generator.git
cd PCR-Template-Generator
poetry install --with dev
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=pcr_template_generator --cov-report=html

# Run linting tests
poetry run pytest tests/test_linting.py -v
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/

# Sort imports  
poetry run isort src/ tests/

# Lint code
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Security scan
poetry run bandit -r src/
```

### Pre-commit Hooks

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## 📚 Scientific Background

This tool implements established PCR design principles:

- **Primer Design**: Based on guidelines from IDT DNA and other molecular biology resources
- **Melting Temperature**: Uses BioPython's nearest-neighbor thermodynamic calculations
- **Secondary Structure**: Prevents formations that interfere with amplification
- **Probe Design**: Follows TaqMan probe design principles for qPCR

### References

- SantaLucia, J. (1998). A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics. PNAS.
- Kibbe, W.A. (2007). OligoCalc: an online oligonucleotide properties calculator. Nucleic Acids Research.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`poetry run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **BioPython** for molecular biology calculations
- **NumPy** for numerical operations
- **Poetry** for dependency management
- The molecular biology community for PCR design principles

## 📞 Support

- 📖 [Documentation](https://github.com/retospect/PCR-Template-Generator)
- 🐛 [Bug Reports](https://github.com/retospect/PCR-Template-Generator/issues)
- 💡 [Feature Requests](https://github.com/retospect/PCR-Template-Generator/issues)
- 💬 [Discussions](https://github.com/retospect/PCR-Template-Generator/discussions)

---

**Made with ❤️ for the molecular biology community**
