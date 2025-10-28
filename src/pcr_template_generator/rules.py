"""Rule classes for evaluating DNA sequence quality in PCR template generation.

This module contains various rule classes that evaluate different aspects
of DNA sequences to ensure they meet PCR primer and probe design criteria.
"""

from typing import List
import numpy as np
from Bio.Seq import Seq
try:
    from Bio.SeqUtils import GC
except ImportError:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    # Fallback for newer BioPython versions
    def GC(sequence):
        """Calculate GC content of a DNA sequence."""
        sequence = str(sequence).upper()
        gc_count = sequence.count('G') + sequence.count('C')
        total_count = len(sequence)
        if total_count == 0:
            return 0.0
        return (gc_count / total_count) * 100.0

from Bio.SeqUtils import MeltingTemp


BASES: List[str] = ["a", "t", "g", "c"]


class Rule:
    """Base rule class for evaluating DNA sequence constraints.
    
    All specific rule implementations should inherit from this class
    and implement their evaluation logic in the constructor.
    """
    
    def __init__(self, name: str = "BaseRule", sequence: str = "", note: str = "") -> None:
        """Initialize a rule with name, sequence, and optional note.
        
        Args:
            name: Human-readable name for this rule
            sequence: DNA sequence to evaluate
            note: Additional information about the rule evaluation
        """
        self._name = name
        self._note = note
        self._cost = 0.0

    def get_name(self) -> str:
        """Get the rule name."""
        return self._name

    def get_note(self) -> str:
        """Get the rule note/description."""
        return self._note

    def get_cost(self) -> float:
        """Get the penalty cost for this rule."""
        return self._cost


class GCContent(Rule):
    """Rule for evaluating GC content within specified range.
    
    Penalizes sequences whose GC content falls outside the target range.
    The penalty is proportional to the distance from the target range.
    """
    
    def __init__(
        self, 
        name: str = "GCContent", 
        min_gc: float = 45, 
        max_gc: float = 55, 
        sequence: str = "", 
        note: str = ""
    ) -> None:
        """Initialize GC content rule.
        
        Args:
            name: Rule name
            min_gc: Minimum acceptable GC percentage
            max_gc: Maximum acceptable GC percentage
            sequence: DNA sequence to evaluate
            note: Additional note
        """
        super().__init__(name=name, sequence=sequence, note=note)
        if sequence:
            gc_content = GC(sequence)
            target_gc = np.average([min_gc, max_gc])
            if gc_content < min_gc or gc_content > max_gc:
                self._cost = abs(gc_content - target_gc)
                self._note += f" GC_Content: {gc_content:.1f}%"


class LongRuns(Rule):
    """Rule for penalizing long runs of identical bases.
    
    Sequences with runs of identical bases longer than the threshold
    are penalized to avoid issues with PCR amplification.
    """
    
    def __init__(
        self, 
        name: str = "LongRuns", 
        max_len: int = 3, 
        sequence: str = "", 
        note: str = ""
    ) -> None:
        """Initialize long runs rule.
        
        Args:
            name: Rule name
            max_len: Maximum allowed length of identical base runs
            sequence: DNA sequence to evaluate
            note: Additional note
        """
        super().__init__(name=name, sequence=sequence, note=note)
        if sequence:
            for base in BASES:
                if sequence.find(base * (max_len + 1)) != -1:
                    self._cost += max_len
                    self._note += f" Found run of {base * (max_len + 1)}"


class MeltingRange(Rule):
    """Rule for evaluating melting temperature within target range.
    
    Penalizes sequences whose melting temperature falls outside
    the specified range. Uses BioPython's nearest-neighbor method.
    """
    
    def __init__(
        self,
        name: str = "MeltingRange",
        min_temp: float = 45,
        max_temp: float = 55,
        sequence: str = "",
        note: str = ""
    ) -> None:
        """Initialize melting temperature rule.
        
        Args:
            name: Rule name
            min_temp: Minimum acceptable melting temperature (°C)
            max_temp: Maximum acceptable melting temperature (°C)
            sequence: DNA sequence to evaluate
            note: Additional note
        """
        super().__init__(name=name, sequence=sequence, note=note)
        if sequence:
            melting_temp = MeltingTemp.Tm_NN(sequence)
            target_temp = np.average([min_temp, max_temp])
            if melting_temp < min_temp or melting_temp > max_temp:
                self._cost = abs(melting_temp - target_temp)
                self._note += f" Tm: {melting_temp:.1f}°C"


class SingleMatchOnly(Rule):
    """Rule ensuring a pattern appears exactly once in the sequence.
    
    This rule is used to prevent primer dimers by ensuring that
    3' ends of primers and probes are unique within the template.
    """
    
    def __init__(
        self, 
        name: str = "SingleMatchOnly", 
        sequence: str = "", 
        pattern: str = "", 
        note: str = ""
    ) -> None:
        """Initialize single match rule.
        
        Args:
            name: Rule name
            sequence: DNA sequence to search in
            pattern: Pattern that should appear exactly once
            note: Additional note
        """
        super().__init__(name=name, sequence=sequence, note=note)
        if sequence and pattern:
            # Convert to Seq object to use count_overlap method
            seq_obj = Seq(sequence)
            if hasattr(seq_obj, 'count_overlap'):
                count = seq_obj.count_overlap(pattern)
            else:
                # Fallback for older BioPython versions
                count = sequence.count(pattern)
            
            if count > 1:
                self._cost = 2.0
                self._note += f" Pattern '{pattern}' found {count} times"


class SecondaryLimit(Rule):
    """Rule for limiting secondary structure formation.
    
    Penalizes sequences that can form secondary structures
    (hairpins, self-complementarity) longer than the threshold.
    """
    
    def __init__(
        self, 
        name: str = "SecondaryLimit", 
        sequence: str = "", 
        max_len: int = 10, 
        note: str = ""
    ) -> None:
        """Initialize secondary structure rule.
        
        Args:
            name: Rule name
            sequence: DNA sequence to evaluate
            max_len: Maximum allowed length of complementary regions
            note: Additional note
        """
        super().__init__(name=name, sequence=sequence, note=note)
        if sequence:
            seq_obj = Seq(sequence)
            for i in range(len(sequence) - max_len):
                substr = sequence[i:i + max_len]
                substr_seq = Seq(substr)
                
                # Check for complement matches
                if sequence.find(str(substr_seq.complement())) > -1:
                    self._cost += 1
                    
                # Check for reverse complement matches (hairpins)
                if sequence.find(str(substr_seq.reverse_complement())) > -1:
                    self._cost += 1
                    
            if self._cost > 0:
                self._note += f" Secondary structures detected"
