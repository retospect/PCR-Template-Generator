# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-28

### Added
- Initial release of PCR Template Generator
- Core sequence optimization using simulated annealing
- Comprehensive rule-based evaluation system for PCR design constraints
- Command-line interface for template generation and analysis
- Support for Python 3.10, 3.11, 3.12, and 3.13
- Multi-platform CI/CD with GitHub Actions
- Comprehensive test suite with 90%+ coverage
- Type annotations throughout codebase
- Professional documentation and examples
- Interactive Jupyter notebook with library integration
- Security scanning with Bandit
- Code quality enforcement with Black, isort, flake8, and mypy
- Pre-commit hooks for development workflow
- Automated PyPI publishing with Trusted Publishing

### Features
- **Sequence Generation**: Generate optimized DNA templates for PCR
- **Rule-Based Optimization**: Enforce molecular biology constraints
  - GC content optimization (49-51% overall, primers)
  - Melting temperature matching (±0.5°C between primers)
  - GC clamping (3/5 bases G/C at 3' end)
  - Long run prevention (max 3 identical bases)
  - Secondary structure avoidance (max 4bp complementarity)
  - Primer dimer prevention (unique 4bp 3' ends)
  - Probe optimization (+8°C above primer Tm)
- **Analysis Tools**: Statistical analysis of sequence properties
- **CLI Interface**: Command-line tool for batch processing
- **Library API**: Programmatic access for integration
- **Interactive Examples**: Jupyter notebook with live examples

### Technical
- Modern Python package structure with src/ layout
- Poetry for dependency management
- Comprehensive testing with pytest
- Type safety with mypy
- Code formatting with Black and isort
- Security scanning with Bandit
- Multi-platform CI testing (Ubuntu, macOS, Windows)
- Automated releases and PyPI publishing
- Professional documentation and examples
