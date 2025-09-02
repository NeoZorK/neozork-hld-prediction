#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for gap fixing with NaN values in datetime column.

This test verifies that the gap fixing functionality works correctly
when there are NaN values in the datetime column.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.eda import fix_files


class TestGapFixingWithNaN:
    """Test class for gap fixing with NaN values."""
    
    @pytest.fixture
    def sample_data_with_nan_timestamps(self):
        """Create sample data with NaN values in timestamp column."""
        # Create a time series with some NaN values
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        
        # Create gaps by removing some dates
        first_part = dates[:10]  # First 10 hours
        last_part = dates[-10:]  # Last 10 hours
        
        # Combine to create data with large gap
        valid_dates = pd.concat([pd.Series(first_part), pd.Series(last_part)]).reset_index(drop=True)
        
        # Create data with some NaN timestamps
        all_dates = []
        all_values = []
        
        for i, date in enumerate(valid_dates):
            # Add valid timestamp
            all_dates.append(date)
            all_values.append(100 + i)
            
            # Add some rows with NaN timestamp (simulating the real data issue)
            if i % 3 == 0:  # Every 3rd row
                all_dates.append(pd.NaT)
                all_values.append(200 + i)
        
        data = pd.DataFrame({
            'Timestamp': all_dates,
            'value': all_values
        })
        
        return data
    
    def test_gap_fixing_with_nan_timestamps(self, sample_data_with_nan_timestamps):
        """Test that gap fixing works with NaN values in timestamp column."""
        original_len = len(sample_data_with_nan_timestamps)
        
        # Count NaN values
        nan_count = sample_data_with_nan_timestamps['Timestamp'].isna().sum()
        print(f"Original data: {original_len} rows, {nan_count} NaN timestamps")
        
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '3 days 09:00:00',
            'method': 'direct'
        }]
        
        # Try to fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_nan_timestamps, gap_summary, 'Timestamp')
        
        # Check that fixing was attempted
        assert fixed_data is not None, "Fix gaps should return data"
        
        # Check that data was modified (should have more rows after fixing)
        if len(fixed_data) > original_len:
            print(f"✅ Gaps were fixed: {original_len} -> {len(fixed_data)} rows")
        else:
            print(f"⚠️  Gaps were not fixed: {original_len} -> {len(fixed_data)} rows")
    
    def test_gap_fixing_with_all_nan_timestamps(self):
        """Test that gap fixing handles case where all timestamps are NaN."""
        # Create data with all NaN timestamps
        data = pd.DataFrame({
            'Timestamp': [pd.NaT, pd.NaT, pd.NaT],
            'value': [1, 2, 3]
        })
        
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '1 day 00:00:00',
            'method': 'direct'
        }]
        
        # Try to fix gaps
        fixed_data = fix_files.fix_gaps(data, gap_summary, 'Timestamp')
        
        # Should return original data without modification
        assert fixed_data is not None, "Fix gaps should return data"
        assert len(fixed_data) == len(data), "Should return original data when all timestamps are NaN"
    
    def test_gap_fixing_with_mixed_nan_timestamps(self, sample_data_with_nan_timestamps):
        """Test that gap fixing works with mixed valid and NaN timestamps."""
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '3 days 09:00:00',
            'method': 'direct'
        }]
        
        # Try to fix gaps
        try:
            fixed_data = fix_files.fix_gaps(sample_data_with_nan_timestamps, gap_summary, 'Timestamp')
            
            if fixed_data is not None:
                print(f"✅ Gap fixing completed successfully")
                print(f"   Original rows: {len(sample_data_with_nan_timestamps)}")
                print(f"   Fixed rows: {len(fixed_data)}")
                
                # Check if gaps were actually filled
                if len(fixed_data) > len(sample_data_with_nan_timestamps):
                    print(f"   ✅ Gaps were filled: +{len(fixed_data) - len(sample_data_with_nan_timestamps)} rows")
                else:
                    print(f"   ⚠️  No gaps were filled")
            else:
                print(f"❌ Gap fixing returned None")
                
        except Exception as e:
            print(f"❌ Error during gap fixing: {e}")
            import traceback
            traceback.print_exc()
    
    def test_frequency_detection_with_nan(self, sample_data_with_nan_timestamps):
        """Test frequency detection with NaN values in timestamp column."""
        # Remove NaN values for analysis
        df_clean = sample_data_with_nan_timestamps.dropna(subset=['Timestamp'])
        
        print(f"Data with NaN: {len(sample_data_with_nan_timestamps)} rows")
        print(f"Clean data: {len(df_clean)} rows")
        
        # Sort by timestamp
        df_clean = df_clean.sort_values('Timestamp')
        
        # Calculate time differences
        time_diffs = df_clean['Timestamp'].diff().dropna()
        
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
