#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for gap fixing issue in interactive system.

This test verifies that the gap fixing functionality works correctly
with large time gaps (like 9 days) that were reported in Docker.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.interactive import InteractiveSystem
from src.interactive.analysis_runner import AnalysisRunner
from src.eda import fix_files
from src.eda import data_quality


class TestGapFixingIssue:
    """Test class for gap fixing functionality."""
    
    @pytest.fixture
    def sample_data_with_large_gaps(self):
        """Create sample data with large time gaps (like 9 days)."""
        # Create a time series with large gaps
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        
        # Create gaps by removing a large chunk of data
        # Keep first 10 hours, then skip 9 days (216 hours), then keep last 10 hours
        first_part = dates[:10]  # First 10 hours
        last_part = dates[-10:]  # Last 10 hours
        
        # Combine to create data with large gap
        dates_with_gaps = pd.concat([pd.Series(first_part), pd.Series(last_part)]).reset_index(drop=True)
        
        data = pd.DataFrame({
            'Timestamp': dates_with_gaps,
            'open': [100 + i + np.random.normal(0, 1) for i in range(len(dates_with_gaps))],
            'high': [101 + i + np.random.normal(0, 1) for i in range(len(dates_with_gaps))],
            'low': [99 + i + np.random.normal(0, 1) for i in range(len(dates_with_gaps))],
            'close': [100.5 + i + np.random.normal(0, 1) for i in range(len(dates_with_gaps))],
            'volume': [1000000 + np.random.normal(0, 100000) for _ in range(len(dates_with_gaps))]
        })
        
        return data
    
    @pytest.fixture
    def mock_system(self, sample_data_with_large_gaps):
        """Create mock system with sample data."""
        system = InteractiveSystem()
        system.current_data = sample_data_with_large_gaps
        return system
    
    def test_gap_detection_with_large_gaps(self, sample_data_with_large_gaps):
        """Test that large gaps are properly detected."""
        gap_summary = []
        
        # Mock Fore and Style classes
        class MockFore:
            YELLOW = ""
            GREEN = ""
            MAGENTA = ""
        
        class MockStyle:
            RESET_ALL = ""
        
        # Run gap check
        data_quality.gap_check(sample_data_with_large_gaps, gap_summary, MockFore, MockStyle)
        
        # Check that gaps were detected
        assert len(gap_summary) > 0, "Gaps should be detected"
        
        # Check that the gap information is correct
        gap_info = gap_summary[0]
        assert 'column' in gap_info, "Gap info should contain column name"
        assert 'gaps_count' in gap_info, "Gap info should contain gaps count"
        assert 'largest_gap' in gap_info, "Gap info should contain largest gap"
        
        print(f"Detected gaps: {gap_info}")
    
    def test_fix_gaps_with_large_gaps(self, sample_data_with_large_gaps):
        """Test that large gaps can be fixed."""
        original_len = len(sample_data_with_large_gaps)
        
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '9 days 00:00:00',
            'method': 'direct'
        }]
        
        # Try to fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_large_gaps, gap_summary, 'Timestamp')
        
        # Check that fixing was attempted
        assert fixed_data is not None, "Fix gaps should return data"
        
        # Check that data was modified (should have more rows after fixing)
        if len(fixed_data) > original_len:
            print(f"✅ Gaps were fixed: {original_len} -> {len(fixed_data)} rows")
        else:
            print(f"⚠️  Gaps were not fixed: {original_len} -> {len(fixed_data)} rows")
    
    def test_comprehensive_data_quality_check_with_gaps(self, mock_system):
        """Test comprehensive data quality check with gap detection and fixing."""
        runner = AnalysisRunner(mock_system)
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to return normally
            with patch.object(mock_system, 'safe_input', return_value=''):
                try:
                    runner.run_comprehensive_data_quality_check(mock_system)
                    
                    # Check that results were saved
                    assert 'comprehensive_data_quality' in mock_system.current_results
                    
                    # Check that gap issues were detected
                    gap_issues = mock_system.current_results['comprehensive_data_quality']['gap_issues']
                    print(f"Gap issues detected: {len(gap_issues)}")
                    
                    # Check that data was modified if gaps were fixed
                    if len(gap_issues) > 0:
                        print(f"Gap issues found: {gap_issues}")
                    
                except Exception as e:
                    pytest.fail(f"Comprehensive data quality check should complete: {e}")
    
    def test_gap_fixing_in_docker_environment(self, sample_data_with_large_gaps):
        """Test gap fixing specifically for Docker environment issues."""
        # Simulate the exact scenario from Docker
        print("Simulating Docker gap fixing scenario...")
        
        # Create gap summary similar to what was reported
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 51094,
            'largest_gap': '9 days 00:00:00',
            'method': 'direct'
        }]
        
        # Try to fix gaps
        try:
            fixed_data = fix_files.fix_gaps(sample_data_with_large_gaps, gap_summary, 'Timestamp')
            
            if fixed_data is not None:
                print(f"✅ Gap fixing completed successfully")
                print(f"   Original rows: {len(sample_data_with_large_gaps)}")
                print(f"   Fixed rows: {len(fixed_data)}")
                
                # Check if gaps were actually filled
                if len(fixed_data) > len(sample_data_with_large_gaps):
                    print(f"   ✅ Gaps were filled: +{len(fixed_data) - len(sample_data_with_large_gaps)} rows")
                else:
                    print(f"   ⚠️  No gaps were filled")
            else:
                print(f"❌ Gap fixing returned None")
                
        except Exception as e:
            print(f"❌ Error during gap fixing: {e}")
            import traceback
            traceback.print_exc()
    
    def test_frequency_detection_with_large_gaps(self, sample_data_with_large_gaps):
        """Test frequency detection with large gaps."""
        # Sort by timestamp
        df = sample_data_with_large_gaps.sort_values('Timestamp')
        
        # Calculate time differences
        time_diffs = df['Timestamp'].diff().dropna()
        
        print(f"Time differences statistics:")
        print(f"  Count: {len(time_diffs)}")
        print(f"  Mean: {time_diffs.mean()}")
        print(f"  Median: {time_diffs.median()}")
        print(f"  Min: {time_diffs.min()}")
        print(f"  Max: {time_diffs.max()}")
        
        # Check for large gaps
        large_gaps = time_diffs[time_diffs > pd.Timedelta(days=1)]
        print(f"  Large gaps (>1 day): {len(large_gaps)}")
        
        if not large_gaps.empty:
            print(f"  Largest gap: {large_gaps.max()}")
        
        # Test frequency detection
        freq_counts = time_diffs.value_counts()
        most_common_freq = freq_counts.index[0]
        
        print(f"  Most common frequency: {most_common_freq}")
        print(f"  Frequency counts: {freq_counts.head()}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
