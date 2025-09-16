"""
Tests for the gap tracking system.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import shutil

from src.data.gap_tracker import GapTracker


class TestGapTracker:
    """Test cases for GapTracker class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.gap_tracker = GapTracker(Path(self.temp_dir))
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_gap_tracker_initialization(self):
        """Test gap tracker initialization."""
        assert self.gap_tracker.checked_gaps == {}
        # File is created only when data is saved, not on initialization
        assert self.gap_tracker.gap_tracker_file.parent.exists()
    
    def test_mark_and_check_gap(self):
        """Test marking a gap as checked and checking if it's checked."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        gap_start = pd.Timestamp("2017-01-01 00:00:00")
        gap_end = pd.Timestamp("2017-01-01 01:00:00")
        
        # Initially, gap should not be checked
        assert not self.gap_tracker.is_gap_checked(ticker, interval, source, gap_start, gap_end)
        
        # Mark gap as checked
        self.gap_tracker.mark_gap_checked(ticker, interval, source, gap_start, gap_end)
        
        # Now gap should be checked
        assert self.gap_tracker.is_gap_checked(ticker, interval, source, gap_start, gap_end)
    
    def test_filter_checked_gaps(self):
        """Test filtering out checked gaps."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        
        # Create some gaps
        gaps = [
            (pd.Timestamp("2017-01-01 00:00:00"), pd.Timestamp("2017-01-01 01:00:00")),
            (pd.Timestamp("2017-01-02 00:00:00"), pd.Timestamp("2017-01-02 01:00:00")),
            (pd.Timestamp("2017-01-03 00:00:00"), pd.Timestamp("2017-01-03 01:00:00")),
        ]
        
        # Mark first gap as checked
        self.gap_tracker.mark_gap_checked(ticker, interval, source, gaps[0][0], gaps[0][1])
        
        # Filter gaps
        unchecked_gaps = self.gap_tracker.filter_checked_gaps(ticker, interval, source, gaps)
        
        # Should return only unchecked gaps
        assert len(unchecked_gaps) == 2
        assert unchecked_gaps[0] == gaps[1]
        assert unchecked_gaps[1] == gaps[2]
    
    def test_mark_gaps_from_failed_fetch(self):
        """Test marking gaps as checked from failed fetch results."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        
        gaps = [
            (pd.Timestamp("2017-01-01 00:00:00"), pd.Timestamp("2017-01-01 01:00:00")),
            (pd.Timestamp("2017-01-02 00:00:00"), pd.Timestamp("2017-01-02 01:00:00")),
            (pd.Timestamp("2017-01-03 00:00:00"), pd.Timestamp("2017-01-03 01:00:00")),
        ]
        
        # Simulate fetch results: first two failed, third succeeded
        fetch_results = [False, False, True]
        
        self.gap_tracker.mark_gaps_as_checked_from_failed_fetch(
            ticker, interval, source, gaps, fetch_results
        )
        
        # First two gaps should be marked as checked
        assert self.gap_tracker.is_gap_checked(ticker, interval, source, gaps[0][0], gaps[0][1])
        assert self.gap_tracker.is_gap_checked(ticker, interval, source, gaps[1][0], gaps[1][1])
        
        # Third gap should not be marked as checked (it succeeded)
        assert not self.gap_tracker.is_gap_checked(ticker, interval, source, gaps[2][0], gaps[2][1])
    
    def test_clear_instrument_gaps(self):
        """Test clearing gaps for a specific instrument."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        
        gap_start = pd.Timestamp("2017-01-01 00:00:00")
        gap_end = pd.Timestamp("2017-01-01 01:00:00")
        
        # Mark gap as checked
        self.gap_tracker.mark_gap_checked(ticker, interval, source, gap_start, gap_end)
        assert self.gap_tracker.is_gap_checked(ticker, interval, source, gap_start, gap_end)
        
        # Clear gaps for this instrument
        self.gap_tracker.clear_instrument_gaps(ticker, interval, source)
        
        # Gap should no longer be checked
        assert not self.gap_tracker.is_gap_checked(ticker, interval, source, gap_start, gap_end)
    
    def test_persistence(self):
        """Test that gap data persists across tracker instances."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        gap_start = pd.Timestamp("2017-01-01 00:00:00")
        gap_end = pd.Timestamp("2017-01-01 01:00:00")
        
        # Mark gap as checked with first tracker
        self.gap_tracker.mark_gap_checked(ticker, interval, source, gap_start, gap_end)
        
        # Create new tracker instance
        new_tracker = GapTracker(Path(self.temp_dir))
        
        # Gap should still be marked as checked
        assert new_tracker.is_gap_checked(ticker, interval, source, gap_start, gap_end)
    
    def test_get_stats(self):
        """Test getting gap tracking statistics."""
        ticker = "BTCUSDT"
        interval = "M5"
        source = "binance"
        
        # Initially no stats
        stats = self.gap_tracker.get_stats()
        assert len(stats) == 0
        
        # Add some gaps
        gaps = [
            (pd.Timestamp("2017-01-01 00:00:00"), pd.Timestamp("2017-01-01 01:00:00")),
            (pd.Timestamp("2017-01-02 00:00:00"), pd.Timestamp("2017-01-02 01:00:00")),
        ]
        
        for gap_start, gap_end in gaps:
            self.gap_tracker.mark_gap_checked(ticker, interval, source, gap_start, gap_end)
        
        # Check stats
        stats = self.gap_tracker.get_stats()
        key = f"{source}_{ticker}_{interval}"
        assert key in stats
        assert stats[key] == 2
