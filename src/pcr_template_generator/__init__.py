"""PCR Template Generator.

A Python library for generating optimized DNA templates for PCR
primers and probes.

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

from importlib.metadata import version

from .generator import (
    analyze_sequence_statistics,
    generate_multiple_templates,
    run_experiment,
)
from .rules import (
    GC,
    GCContent,
    LongRuns,
    MeltingRange,
    Rule,
    SecondaryLimit,
    SingleMatchOnly,
)
from .sequence import Sequence

__version__ = version("pcr-template-generator")

__all__ = [
    "GC",
    "GCContent",
    "LongRuns",
    "MeltingRange",
    "Rule",
    "SecondaryLimit",
    "Sequence",
    "SingleMatchOnly",
    "analyze_sequence_statistics",
    "generate_multiple_templates",
    "run_experiment",
]
