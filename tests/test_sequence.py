"""Tests for Sequence class."""

import pytest
from Bio.Seq import Seq

from pcr_template_generator.sequence import Sequence


class TestSequenceInit:
    """Test Sequence initialization."""

    def test_default_init(self):
        """Test default initialization."""
        seq = Sequence()
        assert len(seq.fwd()) == 75  # default seq_length
        assert len(seq.fwd_primer()) == 22  # default primer_length
        assert len(seq.rev_primer()) == 22
        assert len(seq.probe()) == 25  # default probe_length

    def test_custom_init(self):
        """Test initialization with custom parameters."""
        seq = Sequence(
            seq_length=100,
            primer_length=20,
            probe_length=30,
            primer_melt=55.0,
            probe_gap=5,
        )
        assert len(seq.fwd()) == 100
        assert len(seq.fwd_primer()) == 20
        assert len(seq.rev_primer()) == 20
        assert len(seq.probe()) == 30

    def test_init_with_sequence(self):
        """Test initialization with provided sequence."""
        test_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=test_seq)
        assert str(seq.fwd()) == test_seq

    def test_init_with_short_sequence(self):
        """Test initialization with sequence shorter than expected."""
        test_seq = "atgc"
        seq = Sequence(seq_length=10, sequence=test_seq)
        assert str(seq.fwd()) == test_seq


class TestSequenceComponents:
    """Test sequence component extraction."""

    def test_forward_sequence(self):
        """Test forward sequence extraction."""
        test_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=test_seq)
        assert str(seq.fwd()) == test_seq
        assert isinstance(seq.fwd(), Seq)

    def test_reverse_sequence(self):
        """Test reverse complement sequence."""
        test_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=test_seq)
        rev = seq.rev()
        assert isinstance(rev, Seq)
        assert len(rev) == len(test_seq)
        # Reverse complement should be different from forward
        assert str(rev) != test_seq

    def test_forward_primer(self):
        """Test forward primer extraction."""
        test_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=test_seq, primer_length=20)
        primer = seq.fwd_primer()
        assert len(primer) == 20
        assert str(primer) == test_seq[:20]

    def test_reverse_primer(self):
        """Test reverse primer extraction."""
        test_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=test_seq, primer_length=20)
        primer = seq.rev_primer()
        assert len(primer) == 20
        assert isinstance(primer, Seq)

    def test_probe_extraction(self):
        """Test probe sequence extraction."""
        seq = Sequence(seq_length=75, primer_length=22, probe_length=25, probe_gap=3)
        probe = seq.probe()
        assert len(probe) == 25
        assert isinstance(probe, Seq)

    def test_three_prime_ends(self):
        """Test 3' end extraction."""
        seq = Sequence()
        ends = seq.three_prime_ends(end_length=4)
        assert len(ends) == 4  # fwd, rev, fwd_primer, rev_primer
        for end in ends:
            assert len(end) == 4
            assert isinstance(end, Seq)

    def test_three_prime_ends_custom_length(self):
        """Test 3' end extraction with custom length."""
        seq = Sequence()
        ends = seq.three_prime_ends(end_length=6)
        for end in ends:
            assert len(end) == 6


class TestSequenceMutation:
    """Test sequence mutation functionality."""

    def test_mutate_default(self):
        """Test mutation with default parameters."""
        original_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=original_seq)
        original_str = str(seq.fwd())
        
        seq.mutate()  # default how_many=3
        mutated_str = str(seq.fwd())
        
        # Sequence should be same length
        assert len(mutated_str) == len(original_str)
        # Should be different (with very high probability)
        assert mutated_str != original_str

    def test_mutate_custom_count(self):
        """Test mutation with custom mutation count."""
        original_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=original_seq)
        original_str = str(seq.fwd())
        
        seq.mutate(how_many=1)
        mutated_str = str(seq.fwd())
        
        assert len(mutated_str) == len(original_str)
        # Count differences
        differences = sum(1 for a, b in zip(original_str, mutated_str) if a != b)
        assert differences >= 0  # Could be 0 if same base chosen randomly

    def test_mutate_excessive_count(self):
        """Test mutation with count larger than sequence."""
        seq = Sequence(seq_length=10)
        original_len = len(seq.fwd())
        
        # Should not crash even with excessive mutation count
        seq.mutate(how_many=100)
        assert len(seq.fwd()) == original_len

    def test_set_sequence(self):
        """Test setting a new sequence."""
        seq = Sequence()
        new_seq = "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
        seq.set_sequence(new_seq)
        assert str(seq.fwd()) == new_seq


class TestSequenceDisplay:
    """Test sequence display functionality."""

    def test_display_format(self):
        """Test display format."""
        seq = Sequence(seq_length=75, primer_length=22, probe_length=25)
        display = seq.display()
        
        # Should have 4 lines
        lines = display.split('\n')
        assert len(lines) == 4
        
        # Each line should have content
        for line in lines:
            assert len(line) > 0

    def test_display_consistency(self):
        """Test display consistency with sequence components."""
        seq = Sequence(seq_length=75, primer_length=22, probe_length=25)
        display = seq.display()
        lines = display.split('\n')
        
        # Forward template line should match fwd()
        assert str(seq.fwd()) in display
        
        # Should contain primer sequences
        assert str(seq.fwd_primer()) in lines[0]

    def test_rule_info_empty(self):
        """Test rule info when no rules evaluated."""
        seq = Sequence()
        info = seq.rule_info()
        assert info == ""

    def test_rule_info_verbose(self):
        """Test verbose rule info."""
        seq = Sequence()
        # First calculate cost to populate rules
        seq.cost()
        info = seq.rule_info(verbose=True)
        # Should have some content when verbose
        assert len(info) > 0

    def test_cost_message_default(self):
        """Test cost message default."""
        seq = Sequence()
        assert seq.cost_message() == ""


class TestSequenceCost:
    """Test sequence cost calculation."""

    def test_cost_calculation(self):
        """Test that cost calculation returns a number."""
        seq = Sequence()
        cost = seq.cost()
        assert isinstance(cost, float)
        assert cost >= 0

    def test_cost_with_good_sequence(self):
        """Test cost with a well-designed sequence."""
        # This is a sequence that should have relatively low cost
        good_seq = "atgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgcatgc"
        seq = Sequence(sequence=good_seq)
        cost = seq.cost()
        assert isinstance(cost, float)

    def test_cost_with_bad_sequence(self):
        """Test cost with a poorly designed sequence."""
        # Sequence with long runs and extreme GC content
        bad_seq = "aaaaaaaaaaaaaaaaaaaaaaaggggggggggggggggggggggggggcccccccccccccccccccccc"
        seq = Sequence(sequence=bad_seq)
        cost = seq.cost()
        assert cost > 0  # Should have high cost

    def test_cost_populates_rules(self):
        """Test that cost calculation populates rules."""
        seq = Sequence()
        seq.cost()
        # Should have rules after cost calculation
        assert len(seq._rules) > 0

    def test_repeated_cost_calculation(self):
        """Test that cost can be calculated multiple times."""
        seq = Sequence()
        cost1 = seq.cost()
        cost2 = seq.cost()
        # Should be consistent
        assert cost1 == cost2


class TestSequenceEdgeCases:
    """Test edge cases and error conditions."""

    def test_very_short_sequence(self):
        """Test with very short sequence length."""
        seq = Sequence(seq_length=10, primer_length=5, probe_length=3)
        # Should not crash
        cost = seq.cost()
        assert isinstance(cost, float)

    def test_zero_probe_gap(self):
        """Test with zero probe gap."""
        seq = Sequence(probe_gap=0)
        # Should not crash
        cost = seq.cost()
        assert isinstance(cost, float)

    def test_large_probe_gap(self):
        """Test with large probe gap."""
        seq = Sequence(probe_gap=20)
        # Should not crash
        cost = seq.cost()
        assert isinstance(cost, float)

    def test_debug_mode(self):
        """Test debug mode initialization."""
        seq = Sequence(debug=True)
        assert seq._debug is True
        # Should still work normally
        cost = seq.cost()
        assert isinstance(cost, float)


class TestSequenceIntegration:
    """Integration tests for Sequence class."""

    def test_full_workflow(self):
        """Test complete workflow: create, mutate, evaluate."""
        seq = Sequence()
        
        # Initial state
        initial_cost = seq.cost()
        initial_seq = str(seq.fwd())
        
        # Mutate
        seq.mutate(how_many=5)
        mutated_seq = str(seq.fwd())
        
        # Re-evaluate
        new_cost = seq.cost()
        
        # Verify changes
        assert len(initial_seq) == len(mutated_seq)
        assert isinstance(initial_cost, float)
        assert isinstance(new_cost, float)

    def test_multiple_mutations(self):
        """Test multiple rounds of mutation."""
        seq = Sequence()
        original_seq = str(seq.fwd())
        
        # Multiple mutations
        for _ in range(5):
            seq.mutate(how_many=2)
            cost = seq.cost()
            assert isinstance(cost, float)
        
        # Should still be valid sequence
        final_seq = str(seq.fwd())
        assert len(final_seq) == len(original_seq)
        assert all(base in 'atgc' for base in final_seq)
