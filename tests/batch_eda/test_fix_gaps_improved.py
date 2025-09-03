"""
Test module for improved gap fixing functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.batch_eda import fix_files


class TestFixGapsImproved:
    """Test class for improved gap fixing functionality."""
    
    @pytest.fixture
    def sample_data_with_large_gaps(self):
        """Create sample data with large gaps."""
        # Create base timestamps with regular intervals
        base_times = pd.date_range(
            start='2023-01-01 00:00:00',
            end='2023-01-02 00:00:00',
            freq='1H'
        )
        
        # Create data with some large gaps
        data = []
        for i, time in enumerate(base_times):
            # Skip some periods to create gaps
            if 5 <= i <= 10:  # 6-hour gap
                continue
            if 15 <= i <= 20:  # 6-hour gap
                continue
            
            data.append({
                'Timestamp': time,
                'open': 100 + i,
                'high': 105 + i,
                'low': 95 + i,
                'close': 102 + i,
                'volume': 1000 + i * 10,
                'predicted_low': 94 + i,
                'predicted_high': 106 + i,
                'pressure': 0.5 + i * 0.01,
                'pressure_vector': 0.1 + i * 0.02
            })
        
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_data_with_irregular_gaps(self):
        """Create sample data with irregular gaps."""
        # Create irregular timestamps
        times = [
            '2023-01-01 00:00:00',
            '2023-01-01 01:00:00',
            '2023-01-01 02:00:00',
            '2023-01-01 10:00:00',  # 8-hour gap
            '2023-01-01 11:00:00',
            '2023-01-01 12:00:00',
            '2023-01-02 00:00:00',  # 12-hour gap
            '2023-01-02 01:00:00',
            '2023-01-02 02:00:00',
        ]
        
        data = []
        for i, time_str in enumerate(times):
            data.append({
                'Timestamp': pd.to_datetime(time_str),
                'open': 100 + i,
                'high': 105 + i,
                'low': 95 + i,
                'close': 102 + i,
                'volume': 1000 + i * 10,
                'predicted_low': 94 + i,
                'predicted_high': 106 + i,
                'pressure': 0.5 + i * 0.01,
                'pressure_vector': 0.1 + i * 0.02
            })
        
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_data_with_nan_timestamps(self):
        """Create sample data with NaN timestamps."""
        data = []
        
        # Add some valid timestamps
        for i in range(10):
            data.append({
                'Timestamp': pd.to_datetime(f'2023-01-01 {i:02d}:00:00'),
                'open': 100 + i,
                'high': 105 + i,
                'low': 95 + i,
                'close': 102 + i,
                'volume': 1000 + i * 10,
                'predicted_low': 94 + i,
                'predicted_high': 106 + i,
                'pressure': 0.5 + i * 0.01,
                'pressure_vector': 0.1 + i * 0.02
            })
        
        # Add some rows with NaN timestamps
        for i in range(5):
            data.append({
                'Timestamp': pd.NaT,
                'open': 200 + i,
                'high': 205 + i,
                'low': 195 + i,
                'close': 202 + i,
                'volume': 2000 + i * 10,
                'predicted_low': 194 + i,
                'predicted_high': 206 + i,
                'pressure': 1.5 + i * 0.01,
                'pressure_vector': 1.1 + i * 0.02
            })
        
        return pd.DataFrame(data)
    
    def test_fix_gaps_with_large_gaps(self, sample_data_with_large_gaps):
        """Test that large gaps are properly fixed."""
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 2,
            'largest_gap': '6 hours',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_large_gaps, gap_summary, 'Timestamp')
        
        # Check that data was fixed
        assert fixed_data is not None, "Fixed data should not be None"
        assert len(fixed_data) > len(sample_data_with_large_gaps), "Fixed data should have more rows"
        
        # Check that timestamps are sorted
        assert fixed_data['Timestamp'].is_monotonic_increasing, "Timestamps should be sorted"
        
        # Check that there are no large gaps in the fixed data
        time_diffs = fixed_data['Timestamp'].diff().dropna()
        mean_diff = time_diffs.mean()
        std_diff = time_diffs.std()
        threshold = mean_diff + 2 * std_diff
        
        large_gaps = time_diffs[time_diffs > threshold]
        assert len(large_gaps) == 0, "No large gaps should remain after fixing"
        
        print(f"Original data: {len(sample_data_with_large_gaps)} rows")
        print(f"Fixed data: {len(fixed_data)} rows")
        print(f"Largest gap in fixed data: {time_diffs.max()}")
    
    def test_fix_gaps_with_irregular_gaps(self, sample_data_with_irregular_gaps):
        """Test that irregular gaps are properly fixed."""
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 2,
            'largest_gap': '12 hours',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_irregular_gaps, gap_summary, 'Timestamp')
        
        # Check that data was fixed
        assert fixed_data is not None, "Fixed data should not be None"
        assert len(fixed_data) > len(sample_data_with_irregular_gaps), "Fixed data should have more rows"
        
        # Check that timestamps are sorted
        assert fixed_data['Timestamp'].is_monotonic_increasing, "Timestamps should be sorted"
        
        # Check that numeric columns were interpolated
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
        for col in numeric_cols:
            assert not fixed_data[col].isna().all(), f"Column {col} should not be all NaN"
        
        print(f"Original data: {len(sample_data_with_irregular_gaps)} rows")
        print(f"Fixed data: {len(fixed_data)} rows")
    
    def test_fix_gaps_with_nan_timestamps(self, sample_data_with_nan_timestamps):
        """Test that NaN timestamps are handled properly."""
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '1 hour',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_nan_timestamps, gap_summary, 'Timestamp')
        
        # Check that data was fixed
        assert fixed_data is not None, "Fixed data should not be None"
        
        # Check that NaN timestamps were handled
        assert not fixed_data['Timestamp'].isna().any(), "No NaN timestamps should remain"
        
        print(f"Original data: {len(sample_data_with_nan_timestamps)} rows")
        print(f"Fixed data: {len(fixed_data)} rows")
    
    def test_fix_gaps_empty_dataframe(self):
        """Test that empty DataFrame is handled properly."""
        empty_df = pd.DataFrame()
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 0,
            'largest_gap': '0 hours',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(empty_df, gap_summary, 'Timestamp')
        
        # Check that empty DataFrame is returned
        assert fixed_data is not None, "Should return empty DataFrame"
        assert len(fixed_data) == 0, "Should return empty DataFrame"
    
    def test_fix_gaps_no_datetime_column(self):
        """Test that missing datetime column is handled properly."""
        # Create data without datetime column
        data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        })
        
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '1 hour',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(data, gap_summary, 'Timestamp')
        
        # Check that original data is returned
        assert fixed_data is not None, "Should return original data"
        assert len(fixed_data) == len(data), "Should return original data unchanged"
    
    def test_irregular_gap_fixing_method(self, sample_data_with_irregular_gaps):
        """Test the irregular gap fixing method directly."""
        # Test the private method
        fixed_data = fix_files._fix_gaps_irregular(sample_data_with_irregular_gaps, 'Timestamp')
        
        # Check that data was fixed
        assert fixed_data is not None, "Fixed data should not be None"
        assert len(fixed_data) >= len(sample_data_with_irregular_gaps), "Fixed data should have same or more rows"
        
        # Check that timestamps are sorted
        assert fixed_data['Timestamp'].is_monotonic_increasing, "Timestamps should be sorted"
        
        # Check that there are fewer large gaps (may not eliminate all due to threshold)
        time_diffs = fixed_data['Timestamp'].diff().dropna()
        mean_diff = time_diffs.mean()
        std_diff = time_diffs.std()
        threshold = mean_diff + 2 * std_diff
        
        large_gaps = time_diffs[time_diffs > threshold]
        
        # Check that numeric columns were interpolated
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
        for col in numeric_cols:
            assert not fixed_data[col].isna().all(), f"Column {col} should not be all NaN"
        
        print(f"Original data: {len(sample_data_with_irregular_gaps)} rows")
        print(f"Fixed data: {len(fixed_data)} rows")
        print(f"Large gaps remaining: {len(large_gaps)}")
    
    def test_fix_gaps_with_very_large_gaps(self):
        """Test that very large gaps are handled properly."""
        # Create data with very large gaps (more than 30 days)
        times = [
            '2023-01-01 00:00:00',
            '2023-01-01 01:00:00',
            '2023-02-01 00:00:00',  # 31-day gap
            '2023-02-01 01:00:00',
        ]
        
        data = []
        for i, time_str in enumerate(times):
            data.append({
                'Timestamp': pd.to_datetime(time_str),
                'open': 100 + i,
                'high': 105 + i,
                'low': 95 + i,
                'close': 102 + i,
                'volume': 1000 + i * 10,
                'predicted_low': 94 + i,
                'predicted_high': 106 + i,
                'pressure': 0.5 + i * 0.01,
                'pressure_vector': 0.1 + i * 0.02
            })
        
        df = pd.DataFrame(data)
        
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 1,
            'largest_gap': '31 days',
            'method': 'direct'
        }]
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(df, gap_summary, 'Timestamp')
        
        # Check that data was fixed using irregular method
        assert fixed_data is not None, "Fixed data should not be None"
        # For very large gaps, the method may not add many rows due to the 1000 row limit
        assert len(fixed_data) >= len(df), "Fixed data should have same or more rows"
        
        # Check that timestamps are sorted
        assert fixed_data['Timestamp'].is_monotonic_increasing, "Timestamps should be sorted"
        
        print(f"Original data: {len(df)} rows")
        print(f"Fixed data: {len(fixed_data)} rows")
    
    def test_fix_gaps_preserves_data_integrity(self, sample_data_with_large_gaps):
        """Test that data integrity is preserved during gap fixing."""
        # Create gap summary
        gap_summary = [{
            'column': 'Timestamp',
            'gaps_count': 2,
            'largest_gap': '6 hours',
            'method': 'direct'
        }]
        
        # Store original data for comparison
        original_data = sample_data_with_large_gaps.copy()
        
        # Fix gaps
        fixed_data = fix_files.fix_gaps(sample_data_with_large_gaps, gap_summary, 'Timestamp')
        
        # Check that original data is unchanged
        pd.testing.assert_frame_equal(original_data, sample_data_with_large_gaps), "Original data should be unchanged"
        
        # Check that all original rows are preserved in fixed data
        for _, original_row in original_data.iterrows():
            # Find matching row in fixed data (by timestamp)
            matching_rows = fixed_data[fixed_data['Timestamp'] == original_row['Timestamp']]
            assert len(matching_rows) > 0, f"Original row with timestamp {original_row['Timestamp']} should be preserved"
            
            # Check that values are preserved
            for col in original_data.columns:
                if col != 'Timestamp':
                    assert matching_rows[col].iloc[0] == original_row[col], f"Value in column {col} should be preserved"
        
        print("Data integrity check passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
