"""PCR Template Generator - A Python library for generating optimized DNA templates for PCR primers and probes.

This library uses simulated annealing to generate DNA sequences that satisfy
multiple constraints for PCR primer and probe design, including:
- GC content optimization
- Melting temperature matching
- Avoidance of secondary structures
- Primer dimer prevention
- Proper GC clamping

Example:
    >>> from pcr_template_generator import Sequence, run_experiment
    >>> sequence = run_experiment(debug=False)
    >>> if sequence:
    ...     print(sequence.display())
"""

from .rules import (
    Rule,
    GCContent,
    LongRuns,
    MeltingRange,
    SingleMatchOnly,
    SecondaryLimit,
)
from .sequence import Sequence
from .generator import run_experiment, generate_multiple_templates, analyze_sequence_statistics

__version__ = "1.0.0"
__author__ = "Reto"
__email__ = "reto@example.com"

__all__ = [
    "Rule",
    "GCContent", 
    "LongRuns",
    "MeltingRange",
    "SingleMatchOnly",
    "SecondaryLimit",
    "Sequence",
    "run_experiment",
    "generate_multiple_templates",
    "analyze_sequence_statistics",
]
