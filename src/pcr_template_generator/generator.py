"""Main generator module for PCR template optimization.

This module contains the main optimization algorithm that uses simulated
annealing to generate DNA sequences that satisfy PCR design constraints.
"""

import random
from typing import Optional, List, Tuple

from .sequence import Sequence


def run_experiment(
    seq_length: int = 75,
    primer_length: int = 22,
    probe_length: int = 25,
    primer_melt: float = 54.6,
    probe_gap: int = 3,
    debug: bool = False,
    max_iterations: int = 10000,
    target_cost: float = 1.0,
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
) -> Optional[Sequence]:
    """Run simulated annealing optimization to generate optimal PCR template.
    
    This function uses a simplified simulated annealing approach:
    1. Start with a random sequence
    2. Calculate cost based on design rules
    3. Mutate sequence randomly
    4. Keep mutations that improve the cost
    5. Repeat until cost is acceptable or max iterations reached
    
    Args:
        seq_length: Total length of template sequence
        primer_length: Length of primers
        probe_length: Length of probe
        primer_melt: Target melting temperature for primers (°C)
        probe_gap: Gap between probe and reverse primer
        debug: Enable debug output
        max_iterations: Maximum number of optimization iterations
        target_cost: Target cost to achieve (optimization stops when reached)
        
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
        
    Returns:
        Optimized Sequence object if successful, None if failed
    """
    # Initialize with random sequence
    best_sequence = Sequence(
        seq_length=seq_length,
        primer_length=primer_length,
        probe_length=probe_length,
        primer_melt=primer_melt,
        probe_gap=probe_gap,
        debug=debug,
        overall_gc_min=overall_gc_min,
        overall_gc_max=overall_gc_max,
        primer_gc_min=primer_gc_min,
        primer_gc_max=primer_gc_max,
        primer_tm_tolerance=primer_tm_tolerance,
        gc_clamp_min=gc_clamp_min,
        gc_clamp_max=gc_clamp_max,
        probe_tm_delta_min=probe_tm_delta_min,
        probe_tm_delta_max=probe_tm_delta_max,
        probe_gc_min=probe_gc_min,
        probe_gc_max=probe_gc_max,
        max_run_length=max_run_length,
        unique_end_length=unique_end_length,
        max_secondary_length=max_secondary_length,
    )
    best_cost = best_sequence.cost()

    # Working sequence for mutations
    mutant_sequence = Sequence(
        seq_length=seq_length,
        primer_length=primer_length,
        probe_length=probe_length,
        primer_melt=primer_melt,
        probe_gap=probe_gap,
        debug=debug,
        overall_gc_min=overall_gc_min,
        overall_gc_max=overall_gc_max,
        primer_gc_min=primer_gc_min,
        primer_gc_max=primer_gc_max,
        primer_tm_tolerance=primer_tm_tolerance,
        gc_clamp_min=gc_clamp_min,
        gc_clamp_max=gc_clamp_max,
        probe_tm_delta_min=probe_tm_delta_min,
        probe_tm_delta_max=probe_tm_delta_max,
        probe_gc_min=probe_gc_min,
        probe_gc_max=probe_gc_max,
        max_run_length=max_run_length,
        unique_end_length=unique_end_length,
        max_secondary_length=max_secondary_length,
    )

    iteration = 0
    time_since_improvement = 0

    if debug:
        print(f"Starting optimization with initial cost: {best_cost:.2f}")

    # Optimization loop
    while best_cost > target_cost and iteration < max_iterations:
        # Create mutant from current best
        mutant_sequence.set_sequence(str(best_sequence.fwd()))
        
        # Mutate between 1 and 8 bases
        mutation_count = random.randint(1, 8)
        mutant_sequence.mutate(how_many=mutation_count)
        
        # Evaluate mutant
        mutant_cost = mutant_sequence.cost()
        
        # Keep if better
        if mutant_cost < best_cost:
            best_sequence.set_sequence(str(mutant_sequence.fwd()))
            best_cost = mutant_cost
            time_since_improvement = 0
            
            if debug:
                print(f"Reduced cost to {best_cost:6.2f} at cycle {iteration:5d}")
                print(mutant_sequence.rule_info())
        
        iteration += 1
        time_since_improvement += 1
        
        # Early termination if no improvement for too long
        if time_since_improvement > max_iterations // 10:
            if debug:
                print(f"No improvement for {time_since_improvement} iterations, stopping early")
            break

    if best_cost <= target_cost:
        if debug:
            print(f"SUCCESS: Found solution with cost {best_cost:.2f} in {iteration} iterations")
        return best_sequence
    else:
        if debug:
            print(f"FAILURE: Could not reach target cost {target_cost} in {iteration} iterations")
            print(f"Best cost achieved: {best_cost:.2f}")
        return None


def generate_multiple_templates(
    count: int = 10,
    seq_length: int = 75,
    primer_length: int = 22,
    probe_length: int = 25,
    primer_melt: float = 54.6,
    probe_gap: int = 3,
    debug: bool = False,
    max_iterations: int = 10000,
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
) -> List[Sequence]:
    """Generate multiple optimized PCR templates.
    
    Args:
        count: Number of templates to generate
        seq_length: Total length of template sequence
        primer_length: Length of primers
        probe_length: Length of probe
        primer_melt: Target melting temperature for primers (°C)
        probe_gap: Gap between probe and reverse primer
        debug: Enable debug output
        max_iterations: Maximum iterations per template
        
    Returns:
        List of successfully generated Sequence objects
    """
    templates = []
    generated = 0
    attempts = 0
    max_attempts = count * 3  # Allow some failures
    
    if debug:
        print(f"Generating {count} PCR templates...")
    
    while generated < count and attempts < max_attempts:
        template = run_experiment(
            seq_length=seq_length,
            primer_length=primer_length,
            probe_length=probe_length,
            primer_melt=primer_melt,
            probe_gap=probe_gap,
            debug=False,  # Disable debug for batch generation
            max_iterations=max_iterations,
            overall_gc_min=overall_gc_min,
            overall_gc_max=overall_gc_max,
            primer_gc_min=primer_gc_min,
            primer_gc_max=primer_gc_max,
            primer_tm_tolerance=primer_tm_tolerance,
            gc_clamp_min=gc_clamp_min,
            gc_clamp_max=gc_clamp_max,
            probe_tm_delta_min=probe_tm_delta_min,
            probe_tm_delta_max=probe_tm_delta_max,
            probe_gc_min=probe_gc_min,
            probe_gc_max=probe_gc_max,
            max_run_length=max_run_length,
            unique_end_length=unique_end_length,
            max_secondary_length=max_secondary_length,
        )
        
        attempts += 1
        
        if template is not None:
            templates.append(template)
            generated += 1
            if debug:
                print(f"Generated template {generated}/{count}")
        elif debug:
            print(f"Failed to generate template (attempt {attempts})")
    
    if debug:
        print(f"Successfully generated {len(templates)} templates out of {count} requested")
    
    return templates


def analyze_sequence_statistics(
    sequence_length: int = 22,
    sample_count: int = 10000,
    debug: bool = False,
) -> Tuple[List[float], List[float]]:
    """Analyze melting temperature and GC content statistics for random sequences.
    
    This function generates random sequences and analyzes their properties
    to understand the relationship between GC content and melting temperature.
    
    Args:
        sequence_length: Length of sequences to analyze
        sample_count: Number of random sequences to generate
        debug: Enable debug output
        
    Returns:
        Tuple of (temperatures, gc_contents) lists
    """
    from Bio.SeqUtils import MeltingTemp, GC
    import numpy as np
    
    temperatures = []
    gc_contents = []
    
    if debug:
        print(f"Analyzing {sample_count} random sequences of length {sequence_length}")
    
    for i in range(sample_count):
        # Generate random sequence
        sequence = "".join([random.choice(['a', 't', 'g', 'c']) for _ in range(sequence_length)])
        
        # Calculate properties
        temp = MeltingTemp.Tm_NN(sequence)
        gc_content = GC(sequence)
        
        temperatures.append(temp)
        gc_contents.append(gc_content)
        
        if debug and (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{sample_count} sequences")
    
    if debug:
        temp_mean = np.mean(temperatures)
        gc_mean = np.mean(gc_contents)
        print(f"Temperature: {temp_mean:.2f}°C mean")
        print(f"GC content: {gc_mean:.2f}% mean")
    
    return temperatures, gc_contents
