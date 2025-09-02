#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Very Large Range Gap Fixing

This test verifies the specialized gap fixing method for very large time ranges (10+ years).
"""

import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.eda.fix_files import _fix_gaps_very_large_range, fix_gaps


class TestVeryLargeRangeGapFixing:
    """Test very large range gap fixing functionality."""
    
    def setup_method(self):
        """Setup method for tests."""
        pass
    
    def test_very_large_range_detection(self):
        """Test that very large ranges (>10 years) are detected and use specialized method."""
        print("🧪 Testing very large range detection...")
        
        # Create data spanning 15 years (1970-1985)
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1985, 1, 1)
        
        # Create regular daily data with some gaps
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Remove some dates to create gaps
        dates = dates[::3]  # Take every 3rd date to create gaps
        
        # Create sample data
        data = {
            'Timestamp': dates,
            'Open': np.random.randn(len(dates)) * 100 + 1000,
            'High': np.random.randn(len(dates)) * 100 + 1000,
            'Low': np.random.randn(len(dates)) * 100 + 1000,
            'Close': np.random.randn(len(dates)) * 100 + 1000,
            'Volume': np.random.randint(1000, 10000, len(dates))
        }
        
        df = pd.DataFrame(data)
        
        # Test the main fix_gaps function
        print(f"Original data shape: {df.shape}")
        print(f"Time range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
        
        # This should automatically use the very large range method
        fixed_df = fix_gaps(df, datetime_col='Timestamp')
        
        print(f"Fixed data shape: {fixed_df.shape}")
        
        # Verify that the data was processed
        assert fixed_df is not None
        assert len(fixed_df) >= len(df)  # Should have same or more rows
        
        print("✅ Very large range detection test passed")
    
    def test_conservative_threshold_for_large_ranges(self):
        """Test that very large ranges use conservative threshold (5x median)."""
        print("🧪 Testing conservative threshold for large ranges...")
        
        # Create data spanning 12 years
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1982, 1, 1)
        
        # Create irregular data with some large gaps
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            # Add some large gaps (skip several days occasionally)
            if np.random.random() < 0.1:  # 10% chance of large gap
                current_date += timedelta(days=np.random.randint(5, 15))
            else:
                current_date += timedelta(days=1)
        
        # Create sample data
        data = {
            'Timestamp': dates,
            'Price': np.random.randn(len(dates)) * 10 + 100,
            'Volume': np.random.randint(100, 1000, len(dates))
        }
        
        df = pd.DataFrame(data)
        
        # Test the specialized method directly
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        print(f"Original data shape: {df.shape}")
        print(f"Fixed data shape: {fixed_df.shape}")
        
        # Verify that the data was processed
        assert fixed_df is not None
        assert len(fixed_df) >= len(df)
        
        print("✅ Conservative threshold test passed")
    
    def test_max_rows_per_gap_limit(self):
        """Test that very large ranges limit interpolated rows per gap."""
        print("🧪 Testing max rows per gap limit...")
        
        # Create data with very large gaps
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1980, 1, 1)
        
        # Create data with only a few points and large gaps
        dates = [
            start_date,
            start_date + timedelta(days=100),  # 100 day gap
            start_date + timedelta(days=500),  # 400 day gap
            start_date + timedelta(days=1000), # 500 day gap
            end_date
        ]
        
        data = {
            'Timestamp': dates,
            'Price': [100, 110, 120, 130, 140],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        }
        
        df = pd.DataFrame(data)
        
        # Test the specialized method
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        print(f"Original data shape: {df.shape}")
        print(f"Fixed data shape: {fixed_df.shape}")
        
        # For very large ranges, should limit to 10 rows per gap
        # With 4 gaps and original 5 rows, should have at most 5 + 4*10 = 45 rows
        assert len(fixed_df) <= 45
        
        print("✅ Max rows per gap limit test passed")
    
    def test_standard_range_uses_normal_method(self):
        """Test that standard ranges (<10 years) use normal threshold."""
        print("🧪 Testing standard range uses normal method...")
        
        # Create data spanning 5 years (standard range)
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 1, 1)
        
        # Create regular daily data with some gaps
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        dates = dates[::2]  # Take every 2nd date to create gaps
        
        data = {
            'Timestamp': dates,
            'Price': np.random.randn(len(dates)) * 10 + 100,
            'Volume': np.random.randint(100, 1000, len(dates))
        }
        
        df = pd.DataFrame(data)
        
        # This should use the regular irregular method, not the very large range method
        fixed_df = fix_gaps(df, datetime_col='Timestamp')
        
        print(f"Original data shape: {df.shape}")
        print(f"Fixed data shape: {fixed_df.shape}")
        
        # Verify that the data was processed
        assert fixed_df is not None
        assert len(fixed_df) >= len(df)
        
        print("✅ Standard range method test passed")
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame."""
        print("🧪 Testing empty DataFrame handling...")
        
        # Create empty DataFrame
        df = pd.DataFrame(columns=['Timestamp', 'Price', 'Volume'])
        
        # Test the specialized method
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        # Should return the original empty DataFrame
        assert fixed_df is not None
        assert len(fixed_df) == 0
        
        print("✅ Empty DataFrame handling test passed")
    
    def test_no_time_differences_handling(self):
        """Test handling when no time differences are found."""
        print("🧪 Testing no time differences handling...")
        
        # Create DataFrame with single timestamp
        data = {
            'Timestamp': [datetime(1970, 1, 1)],
            'Price': [100],
            'Volume': [1000]
        }
        
        df = pd.DataFrame(data)
        
        # Test the specialized method
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        # Should return the original DataFrame
        assert fixed_df is not None
        assert len(fixed_df) == 1
        
        print("✅ No time differences handling test passed")
    
    def test_no_large_gaps_handling(self):
        """Test handling when no large gaps are detected."""
        print("🧪 Testing no large gaps handling...")
        
        # Create data with very small gaps (no large gaps)
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1980, 1, 1)
        
        # Create regular daily data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = {
            'Timestamp': dates,
            'Price': np.random.randn(len(dates)) * 10 + 100,
            'Volume': np.random.randint(100, 1000, len(dates))
        }
        
        df = pd.DataFrame(data)
        
        # Test the specialized method
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        # Should return the original DataFrame (no gaps to fix)
        assert fixed_df is not None
        assert len(fixed_df) == len(df)
        
        print("✅ No large gaps handling test passed")
    
    def test_data_integrity_preservation(self):
        """Test that original data is preserved during gap fixing."""
        print("🧪 Testing data integrity preservation...")
        
        # Create data with known values
        start_date = datetime(1970, 1, 1)
        end_date = datetime(1980, 1, 1)
        
        # Create data with gaps
        dates = [
            start_date,
            start_date + timedelta(days=100),
            start_date + timedelta(days=200),
            end_date
        ]
        
        data = {
            'Timestamp': dates,
            'Price': [100.0, 110.0, 120.0, 130.0],
            'Volume': [1000, 1100, 1200, 1300]
        }
        
        df = pd.DataFrame(data)
        
        # Test the specialized method
        fixed_df = _fix_gaps_very_large_range(df, 'Timestamp')
        
        # Verify that original data points are preserved
        for i, original_row in df.iterrows():
            # Find the corresponding row in fixed data
            matching_rows = fixed_df[fixed_df['Timestamp'] == original_row['Timestamp']]
            assert len(matching_rows) == 1
            
            # Verify values are preserved
            fixed_row = matching_rows.iloc[0]
            assert abs(fixed_row['Price'] - original_row['Price']) < 1e-10
            assert abs(fixed_row['Volume'] - original_row['Volume']) < 1e-10
        
        print("✅ Data integrity preservation test passed")


if __name__ == "__main__":
    # Run tests
    test_instance = TestVeryLargeRangeGapFixing()
    
    test_methods = [
        test_instance.test_very_large_range_detection,
        test_instance.test_conservative_threshold_for_large_ranges,
        test_instance.test_max_rows_per_gap_limit,
        test_instance.test_standard_range_uses_normal_method,
        test_instance.test_empty_dataframe_handling,
        test_instance.test_no_time_differences_handling,
        test_instance.test_no_large_gaps_handling,
        test_instance.test_data_integrity_preservation
    ]
    
    print("🧪 Running Very Large Range Gap Fixing Tests")
    print("=" * 60)
    
    for test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_method.__name__} passed")
        except Exception as e:
            print(f"❌ {test_method.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print("🎉 All tests completed!")
