#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test TimedeltaIndex fix in GapFixer.

This test verifies that the TimedeltaIndex.mode() error has been resolved.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


class TestTimedeltaIndexFix:
    """Test that TimedeltaIndex issues are resolved in GapFixer."""
    
    def test_timedelta_index_gap_detection(self):
        """Test that gap detection works with TimedeltaIndex."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            
            # Create test data with TimedeltaIndex
            dates = pd.date_range('2023-01-01', periods=100, freq='1min')
            df = pd.DataFrame({
                'value': np.random.randn(100),
                'timestamp': dates
            })
            
            # Test gap detection
            gap_info = gap_fixer.utils.detect_gaps(df, 'timestamp')
            
            # Verify that gap detection completed without errors
            assert isinstance(gap_info, dict)
            assert 'has_gaps' in gap_info
            assert 'expected_frequency' in gap_info
            
            # Check that expected_frequency is a Timedelta
            assert isinstance(gap_info['expected_frequency'], pd.Timedelta)
            
        except Exception as e:
            pytest.fail(f"Gap detection failed with TimedeltaIndex: {e}")
    
    def test_timedelta_index_with_gaps(self):
        """Test gap detection with actual gaps in data."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            
            # Create test data with gaps
            dates = []
            values = []
            
            # Create regular intervals with some gaps
            current_time = pd.Timestamp('2023-01-01 00:00:00')
            for i in range(100):
                if i not in [25, 50, 75]:  # Create gaps at these indices
                    dates.append(current_time)
                    values.append(np.random.randn())
                current_time += pd.Timedelta(minutes=1)
            
            df = pd.DataFrame({
                'value': values,
                'timestamp': dates
            })
            
            # Test gap detection
            gap_info = gap_fixer.utils.detect_gaps(df, 'timestamp')
            
            # Verify gap detection results
            assert isinstance(gap_info, dict)
            assert gap_info['has_gaps'] == True
            assert gap_info['gap_count'] > 0
            assert len(gap_info['gap_details']) > 0
            
        except Exception as e:
            pytest.fail(f"Gap detection with gaps failed: {e}")
    
    def test_empty_timedelta_index(self):
        """Test gap detection with empty TimedeltaIndex."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            
            # Create test data with only one row
            df = pd.DataFrame({
                'value': [1.0],
                'timestamp': [pd.Timestamp('2023-01-01 00:00:00')]
            })
            
            # Test gap detection
            gap_info = gap_fixer.utils.detect_gaps(df, 'timestamp')
            
            # Verify that it handles single row correctly
            assert isinstance(gap_info, dict)
            assert gap_info['has_gaps'] == False
            assert gap_info['gap_count'] == 0
            
        except Exception as e:
            pytest.fail(f"Gap detection with single row failed: {e}")
    
    def test_timedelta_index_edge_cases(self):
        """Test gap detection with edge cases."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            
            # Test with irregular intervals
            dates = [
                pd.Timestamp('2023-01-01 00:00:00'),
                pd.Timestamp('2023-01-01 00:01:00'),
                pd.Timestamp('2023-01-01 00:03:00'),  # Gap of 2 minutes
                pd.Timestamp('2023-01-01 00:04:00'),
                pd.Timestamp('2023-01-01 00:07:00'),  # Gap of 3 minutes
            ]
            
            df = pd.DataFrame({
                'value': np.random.randn(len(dates)),
                'timestamp': dates
            })
            
            # Test gap detection
            gap_info = gap_fixer.utils.detect_gaps(df, 'timestamp')
            
            # Verify results
            assert isinstance(gap_info, dict)
            assert gap_info['has_gaps'] == True
            assert gap_info['gap_count'] > 0
            
        except Exception as e:
            pytest.fail(f"Gap detection with edge cases failed: {e}")
    
    def test_timedelta_index_frequency_calculation(self):
        """Test that expected frequency calculation works correctly."""
        try:
            from src.data.gap_fixing import GapFixer
            gap_fixer = GapFixer(memory_limit_mb=1024)
            
            # Create test data with known frequency
            dates = pd.date_range('2023-01-01', periods=50, freq='5min')
            df = pd.DataFrame({
                'value': np.random.randn(50),
                'timestamp': dates
            })
            
            # Test gap detection
            gap_info = gap_fixer.utils.detect_gaps(df, 'timestamp')
            
            # Verify expected frequency
            assert isinstance(gap_info['expected_frequency'], pd.Timedelta)
            # Should be close to 5 minutes (allowing for small floating point differences)
            expected_minutes = 5
            actual_minutes = gap_info['expected_frequency'].total_seconds() / 60
            assert abs(actual_minutes - expected_minutes) < 0.1
            
        except Exception as e:
            pytest.fail(f"Frequency calculation failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
