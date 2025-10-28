"""Tests for rule classes."""

import pytest
from Bio.Seq import Seq

from pcr_template_generator.rules import (
    Rule,
    GCContent,
    LongRuns,
    MeltingRange,
    SingleMatchOnly,
    SecondaryLimit,
)


class TestRule:
    """Test base Rule class."""

    def test_init_default(self):
        """Test default initialization."""
        rule = Rule()
        assert rule.get_name() == "BaseRule"
        assert rule.get_note() == ""
        assert rule.get_cost() == 0.0

    def test_init_with_params(self):
        """Test initialization with parameters."""
        rule = Rule(name="TestRule", sequence="atgc", note="Test note")
        assert rule.get_name() == "TestRule"
        assert rule.get_note() == "Test note"
        assert rule.get_cost() == 0.0


class TestGCContent:
    """Test GCContent rule."""

    def test_gc_content_within_range(self):
        """Test sequence with GC content within acceptable range."""
        # 50% GC content: 2 G/C out of 4 bases
        rule = GCContent(sequence="atgc", min_gc=45, max_gc=55)
        assert rule.get_cost() == 0.0

    def test_gc_content_too_low(self):
        """Test sequence with GC content too low."""
        # 25% GC content: 1 G/C out of 4 bases
        rule = GCContent(sequence="attc", min_gc=45, max_gc=55)
        assert rule.get_cost() > 0
        assert "GC_Content: 25.0%" in rule.get_note()

    def test_gc_content_too_high(self):
        """Test sequence with GC content too high."""
        # 100% GC content: 4 G/C out of 4 bases
        rule = GCContent(sequence="gcgc", min_gc=45, max_gc=55)
        assert rule.get_cost() > 0
        assert "GC_Content: 100.0%" in rule.get_note()

    def test_empty_sequence(self):
        """Test with empty sequence."""
        rule = GCContent(sequence="", min_gc=45, max_gc=55)
        assert rule.get_cost() == 0.0

    def test_all_at_sequence(self):
        """Test sequence with no GC content."""
        rule = GCContent(sequence="aaattt", min_gc=45, max_gc=55)
        assert rule.get_cost() > 0


class TestLongRuns:
    """Test LongRuns rule."""

    def test_no_long_runs(self):
        """Test sequence without long runs."""
        rule = LongRuns(sequence="atgcatgc", max_len=3)
        assert rule.get_cost() == 0.0

    def test_long_run_detected(self):
        """Test sequence with long run."""
        rule = LongRuns(sequence="aaaatgc", max_len=3)
        assert rule.get_cost() > 0

    def test_multiple_long_runs(self):
        """Test sequence with multiple long runs."""
        rule = LongRuns(sequence="aaaatttt", max_len=3)
        assert rule.get_cost() > 0

    def test_exact_max_length(self):
        """Test sequence with run exactly at max length."""
        rule = LongRuns(sequence="aaatgc", max_len=3)
        assert rule.get_cost() == 0.0

    def test_empty_sequence(self):
        """Test with empty sequence."""
        rule = LongRuns(sequence="", max_len=3)
        assert rule.get_cost() == 0.0


class TestMeltingRange:
    """Test MeltingRange rule."""

    def test_melting_temp_calculation(self):
        """Test that melting temperature is calculated."""
        # Use a known sequence
        rule = MeltingRange(sequence="atgcatgcatgcatgc", min_temp=50, max_temp=60)
        # Should either pass or fail, but cost should be calculated
        assert isinstance(rule.get_cost(), float)

    def test_empty_sequence(self):
        """Test with empty sequence."""
        rule = MeltingRange(sequence="", min_temp=50, max_temp=60)
        assert rule.get_cost() == 0.0

    def test_very_short_sequence(self):
        """Test with very short sequence."""
        rule = MeltingRange(sequence="at", min_temp=50, max_temp=60)
        assert isinstance(rule.get_cost(), float)


class TestSingleMatchOnly:
    """Test SingleMatchOnly rule."""

    def test_pattern_appears_once(self):
        """Test pattern that appears exactly once."""
        rule = SingleMatchOnly(sequence="atgcatgc", pattern="atgc")
        # Pattern appears twice, so should have cost
        assert rule.get_cost() > 0

    def test_pattern_unique(self):
        """Test pattern that appears only once."""
        rule = SingleMatchOnly(sequence="atgctttt", pattern="atgc")
        assert rule.get_cost() == 0.0

    def test_pattern_not_found(self):
        """Test pattern that doesn't appear."""
        rule = SingleMatchOnly(sequence="aaaa", pattern="tttt")
        assert rule.get_cost() == 0.0

    def test_empty_pattern(self):
        """Test with empty pattern."""
        rule = SingleMatchOnly(sequence="atgc", pattern="")
        assert rule.get_cost() == 0.0

    def test_empty_sequence(self):
        """Test with empty sequence."""
        rule = SingleMatchOnly(sequence="", pattern="atgc")
        assert rule.get_cost() == 0.0


class TestSecondaryLimit:
    """Test SecondaryLimit rule."""

    def test_no_secondary_structures(self):
        """Test sequence without secondary structures."""
        # Simple sequence unlikely to have complementarity
        rule = SecondaryLimit(sequence="atatatatatat", max_len=4)
        # May or may not have cost, but should not crash
        assert isinstance(rule.get_cost(), float)

    def test_empty_sequence(self):
        """Test with empty sequence."""
        rule = SecondaryLimit(sequence="", max_len=4)
        assert rule.get_cost() == 0.0

    def test_short_sequence(self):
        """Test with sequence shorter than max_len."""
        rule = SecondaryLimit(sequence="atgc", max_len=10)
        assert rule.get_cost() == 0.0

    def test_palindromic_sequence(self):
        """Test sequence with potential hairpin structure."""
        # This sequence has some complementarity
        rule = SecondaryLimit(sequence="atgcgcatatgcgcat", max_len=4)
        assert isinstance(rule.get_cost(), float)


class TestRuleIntegration:
    """Integration tests for rules."""

    def test_all_rules_with_realistic_sequence(self):
        """Test all rules with a realistic PCR primer sequence."""
        primer_seq = "atgcatgcatgcatgcatgcat"
        
        rules = [
            GCContent(sequence=primer_seq, min_gc=45, max_gc=55),
            LongRuns(sequence=primer_seq, max_len=3),
            MeltingRange(sequence=primer_seq, min_temp=50, max_temp=60),
            SingleMatchOnly(sequence=primer_seq * 2, pattern=primer_seq[:4]),
            SecondaryLimit(sequence=primer_seq, max_len=4),
        ]
        
        for rule in rules:
            assert isinstance(rule.get_cost(), float)
            assert isinstance(rule.get_name(), str)
            assert isinstance(rule.get_note(), str)

    def test_rules_with_problematic_sequence(self):
        """Test rules with a sequence designed to violate constraints."""
        bad_seq = "aaaaaaggggggcccccctttttt"  # Long runs, extreme GC regions
        
        rules = [
            GCContent(sequence=bad_seq, min_gc=45, max_gc=55),
            LongRuns(sequence=bad_seq, max_len=3),
            MeltingRange(sequence=bad_seq, min_temp=50, max_temp=60),
        ]
        
        # At least some rules should detect problems
        total_cost = sum(rule.get_cost() for rule in rules)
        assert total_cost > 0
