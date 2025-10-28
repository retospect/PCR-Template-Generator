"""DNA sequence class for PCR template generation.

This module contains the main Sequence class that represents a DNA template
with associated primers and probe, along with methods for evaluation and mutation.
"""

import random
from typing import List, Tuple, Optional
import numpy as np
from Bio.Seq import Seq

from .rules import (
    Rule,
    GCContent,
    LongRuns,
    MeltingRange,
    SingleMatchOnly,
    SecondaryLimit,
    BASES,
)


class Sequence:
    """Represents a DNA sequence template with primers and probe for PCR.
    
    This class manages a DNA template sequence and provides methods to:
    - Extract forward/reverse primers and probe regions
    - Calculate cost based on various design rules
    - Mutate the sequence for optimization
    - Display the template layout
    """
    
    def __init__(
        self,
        seq_length: int = 75,
        primer_length: int = 22,
        probe_length: int = 25,
        primer_melt: float = 54.6,
        probe_gap: int = 3,
        sequence: str = "",
        debug: bool = False,
        # Design constraint parameters
        overall_gc_min: float = 49.0,
        overall_gc_max: float = 51.0,
        primer_gc_min: float = 49.0,
        primer_gc_max: float = 51.0,
        primer_tm_tolerance: float = 0.5,
        gc_clamp_min: float = 55.0,
        gc_clamp_max: float = 79.0,
        probe_tm_delta_min: float = 8.0,
        probe_tm_delta_max: float = 10.0,
        probe_gc_min: float = 48.0,
        probe_gc_max: float = 52.0,
        max_run_length: int = 3,
        unique_end_length: int = 4,
        max_secondary_length: int = 4,
    ) -> None:
        """Initialize a DNA sequence template.
        
        Args:
            seq_length: Total length of the template sequence
            primer_length: Length of forward and reverse primers
            probe_length: Length of the probe
            primer_melt: Target melting temperature for primers (°C)
            probe_gap: Gap between probe and reverse primer
            sequence: Initial sequence (random if empty)
            debug: Enable debug output
            
            # Design constraint parameters:
            overall_gc_min: Minimum overall GC content (%)
            overall_gc_max: Maximum overall GC content (%)
            primer_gc_min: Minimum primer GC content (%)
            primer_gc_max: Maximum primer GC content (%)
            primer_tm_tolerance: Allowed primer Tm difference (°C)
            gc_clamp_min: Minimum GC clamp content (%)
            gc_clamp_max: Maximum GC clamp content (%)
            probe_tm_delta_min: Minimum probe-primer Tm difference (°C)
            probe_tm_delta_max: Maximum probe-primer Tm difference (°C)
            probe_gc_min: Minimum probe GC content (%)
            probe_gc_max: Maximum probe GC content (%)
            max_run_length: Maximum allowed run of identical bases
            unique_end_length: Length of unique 3' ends for primer dimer prevention
            max_secondary_length: Maximum allowed secondary structure length
        """
        self._primer_length = primer_length
        self._probe_length = probe_length
        self._seq_length = seq_length
        self._primer_melt = primer_melt
        self._probe_gap = probe_gap
        self._cost_comment = ""
        self._debug = debug
        self._rules: List[Rule] = []
        
        # Store design constraint parameters
        self._overall_gc_min = overall_gc_min
        self._overall_gc_max = overall_gc_max
        self._primer_gc_min = primer_gc_min
        self._primer_gc_max = primer_gc_max
        self._primer_tm_tolerance = primer_tm_tolerance
        self._gc_clamp_min = gc_clamp_min
        self._gc_clamp_max = gc_clamp_max
        self._probe_tm_delta_min = probe_tm_delta_min
        self._probe_tm_delta_max = probe_tm_delta_max
        self._probe_gc_min = probe_gc_min
        self._probe_gc_max = probe_gc_max
        self._max_run_length = max_run_length
        self._unique_end_length = unique_end_length
        self._max_secondary_length = max_secondary_length
        
        if not sequence:
            sequence = "".join([random.choice(BASES) for _ in range(seq_length)])
        self._sequence = Seq(sequence)

    def set_sequence(self, new_sequence: str) -> None:
        """Set a new sequence string."""
        self._sequence = Seq(str(new_sequence))

    def fwd(self) -> Seq:
        """Get forward sequence 5'-3'."""
        return self._sequence

    def rev(self) -> Seq:
        """Get reverse sequence 5'-3'."""
        return self._sequence.reverse_complement()

    def fwd_primer(self) -> Seq:
        """Get forward primer 5'-3'."""
        return self._sequence[:self._primer_length]

    def probe(self) -> Seq:
        """Get the probe sequence."""
        probe_start = self._seq_length - self._primer_length - self._probe_length - self._probe_gap
        probe_end = self._seq_length - self._primer_length - self._probe_gap
        return self._sequence[probe_start:probe_end]

    def rev_primer(self) -> Seq:
        """Get reverse primer 5'-3'."""
        return self._sequence[-self._primer_length:].reverse_complement()

    def three_prime_ends(self, end_length: int = 4) -> List[Seq]:
        """Get all 3' ends of sequences and primers.
        
        Args:
            end_length: Length of 3' end to extract
            
        Returns:
            List of 3' end sequences for forward template, reverse template,
            forward primer, and reverse primer
        """
        return [
            self.fwd()[-end_length:],
            self.rev()[-end_length:],
            self.fwd_primer()[-end_length:],
            self.rev_primer()[-end_length:],
        ]

    def mutate(self, how_many: int = 3) -> None:
        """Replace random base pairs with random bases.
        
        Args:
            how_many: Number of bases to mutate
        """
        sequence_str = str(self._sequence)
        indices = random.sample(range(len(sequence_str)), min(how_many, len(sequence_str)))
        
        sequence_list = list(sequence_str)
        for index in indices:
            sequence_list[index] = random.choice(BASES)
        
        self._sequence = Seq("".join(sequence_list))

    def cost_message(self) -> str:
        """Get string describing cost contributors from last evaluation."""
        return self._cost_comment

    def display(self) -> str:
        """Get multi-line string showing primers, probe, and template layout.
        
        Returns:
            Formatted string showing the template structure with primers and probe
        """
        template_spacing = (
            self._seq_length - 2 * self._primer_length - self._probe_length - self._probe_gap
        )
        
        lines = []
        # Forward primer and probe line
        lines.append(str(self.fwd_primer()) + (" " * template_spacing) + str(self.probe()))
        
        # Forward template
        lines.append(str(self.fwd()))
        
        # Reverse complement template
        lines.append(str(self.fwd().complement()))
        
        # Reverse primer line (aligned to right)
        primer_spacing = " " * (self._seq_length - self._primer_length)
        lines.append(primer_spacing + str(self.rev_primer())[::-1])
        
        return "\n".join(lines)

    def rule_info(self, verbose: bool = False) -> str:
        """Get information about rule violations.
        
        Args:
            verbose: Show all rules, not just those with cost > 0
            
        Returns:
            String describing rule costs and violations
        """
        msg = ""
        for rule in self._rules:
            if rule.get_cost() > 0 or verbose:
                msg += f"{rule.get_cost():.1f} {rule.get_name()} {rule.get_note()}\n"
        return msg

    def cost(self) -> float:
        """Calculate total cost based on all design rules.
        
        Returns:
            Total penalty cost for this sequence
        """
        rules: List[Rule] = []
        
        # Overall sequence rules
        rules.append(LongRuns(sequence=str(self.fwd()), max_len=self._max_run_length, 
                             note=f"No runs longer than {self._max_run_length}"))
        rules.append(GCContent(sequence=str(self.fwd()), min_gc=self._overall_gc_min, 
                              max_gc=self._overall_gc_max, note="Overall"))

        # Primer rules
        for primer in [self.fwd_primer(), self.rev_primer()]:
            primer_str = str(primer)
            rules.append(GCContent(sequence=primer_str, min_gc=self._primer_gc_min, 
                                  max_gc=self._primer_gc_max, note="Primer"))
            
            primer_temp = self._primer_melt
            rules.append(
                MeltingRange(
                    sequence=primer_str,
                    min_temp=primer_temp - self._primer_tm_tolerance,
                    max_temp=primer_temp + self._primer_tm_tolerance,
                    note="Primer",
                )
            )

            # GC clamp rules
            for clamp_length in [5, 11]:
                clamp_seq = primer_str[-clamp_length:]
                rules.append(
                    GCContent(sequence=clamp_seq, min_gc=self._gc_clamp_min, 
                             max_gc=self._gc_clamp_max, note="GC Clamp")
                )

            # 3' end should be G or C
            rules.append(
                GCContent(sequence=primer_str[-1:], min_gc=99, max_gc=101, note="3' primer end")
            )

        # Unique 3' ends to prevent primer dimers
        full_length = str(self.fwd()) + str(self.rev())

        for the_end in self.three_prime_ends(self._unique_end_length):
            rules.append(
                SingleMatchOnly(
                    sequence=full_length, pattern=str(the_end), note="Unique 3' ends"
                )
            )

        # Template 3' ends should not be G or C
        for template in [self.fwd(), self.rev()]:
            template_str = str(template)
            rules.append(
                GCContent(sequence=template_str[-1:], min_gc=-1, max_gc=1, note="3' template ends")
            )

            # Primer forcing: bases after primers should not be GC
            primer_forcing_seq = template_str[self._primer_length:self._primer_length + 2]
            rules.append(
                GCContent(sequence=primer_forcing_seq, min_gc=-1, max_gc=1, note="Primer Forcing")
            )

        # Probe rules
        offset = self._probe_gap
        probe_start = -(self._probe_length + self._primer_length + offset)
        probe_end = -(self._primer_length + offset)
        probe_seq = str(self.fwd()[probe_start:probe_end])
        
        primer_temp = self._primer_melt
        rules.append(
            MeltingRange(
                sequence=probe_seq,
                min_temp=primer_temp + self._probe_tm_delta_min,
                max_temp=primer_temp + self._probe_tm_delta_max,
                note="Probe Tm",
            )
        )
        rules.append(GCContent(sequence=probe_seq, min_gc=self._probe_gc_min, 
                              max_gc=self._probe_gc_max, note="Probe GC"))
        rules.append(
            SingleMatchOnly(
                sequence=full_length, pattern=probe_seq[-self._unique_end_length:], 
                note="Unique probe end"
            )
        )
        # 5' end of probe should not be G
        rules.append(
            GCContent(sequence=probe_seq[:1], min_gc=-1, max_gc=1, note="Probe 5' end")
        )

        # Secondary structure limits
        rules.append(SecondaryLimit(sequence=str(self.fwd()), max_len=self._max_secondary_length, 
                                   note="Secondary structures"))

        self._rules = rules

        total_cost = sum(rule.get_cost() for rule in rules)
        return total_cost
