"""
Tests for fix_files.py

This module tests the functions in the fix_files.py module that handle
fixing various data quality issues in pandas DataFrames and parquet files.
"""

import os
import sys
import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, Mock

# Add the src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.eda.fix_files import (
    fix_nan, fix_duplicates, fix_gaps, fix_zeros, fix_negatives, fix_infs,
    fix_file, batch_fix_files
)


# Fixtures
@pytest.fixture
def sample_df_with_nan():
    """Create a sample DataFrame with NaN values."""
    return pd.DataFrame({
        'numeric': [1.0, np.nan, 3.0, np.nan],
        'string': ['a', np.nan, 'c', 'd'],
        'datetime': pd.to_datetime(['2022-01-01', np.nan, '2022-01-03', '2022-01-04']),
        'all_good': [1, 2, 3, 4]
    })


@pytest.fixture
def sample_df_with_duplicates():
    """Create a sample DataFrame with duplicate rows."""
    return pd.DataFrame({
        'A': [1, 2, 3, 1, 2],
        'B': ['a', 'b', 'c', 'a', 'b'],
        'C': [10, 20, 30, 10, 20]
    })


@pytest.fixture
def sample_df_with_gaps():
    """Create a sample DataFrame with gaps in time series."""
    dates = pd.date_range(start='2022-01-01', end='2022-01-10', freq='D')
    # Create gaps by removing some dates
    dates = dates[dates.day != 5]  # Remove day 5
    dates = dates[dates.day != 8]  # Remove day 8
    return pd.DataFrame({
        'date': dates,
        'value': np.random.rand(len(dates))
    })


@pytest.fixture
def sample_df_with_zeros():
    """Create a sample DataFrame with zero values."""
    return pd.DataFrame({
        'price': [10.5, 0.0, 12.3, 11.0],
        'close': [105.5, 106.0, 0.0, 107.8],
        'volume': [1000, 0, 1200, 900],
        'other': [1, 2, 3, 0]
    })


@pytest.fixture
def sample_df_with_negatives():
    """Create a sample DataFrame with negative values."""
    return pd.DataFrame({
        'open': [10.5, -1.2, 12.3, 11.0],
        'close': [105.5, 106.0, -3.2, 107.8],
        'volume': [1000, -5, 1200, 900],
        'other': [1, -2, 3, 4]
    })


@pytest.fixture
def sample_df_with_infs():
    """Create a sample DataFrame with infinite values."""
    return pd.DataFrame({
        'A': [1.0, np.inf, 3.0, 4.0],
        'B': [5.0, 6.0, -np.inf, 8.0],
        'C': [np.inf, 10.0, 11.0, -np.inf]
    })


# Tests for fix_nan
def test_fix_nan_fills_numeric_with_median(sample_df_with_nan):
    """Test that fix_nan properly fills numeric columns with median values."""
    fixed_df = fix_nan(sample_df_with_nan)

    # Check that NaNs in numeric column are filled with the median
    assert not fixed_df['numeric'].isna().any()
    assert fixed_df['numeric'].iloc[1] == 2.0  # Median of [1.0, 3.0]
    assert fixed_df['numeric'].iloc[3] == 2.0  # Same median


def test_fix_nan_fills_string_with_mode(sample_df_with_nan):
    """Test that fix_nan properly fills string columns with mode values."""
    fixed_df = fix_nan(sample_df_with_nan)

    # Check that NaNs in string column are filled
    assert not fixed_df['string'].isna().any()


def test_fix_nan_fills_datetime_with_ffill_bfill(sample_df_with_nan):
    """Test that fix_nan properly fills datetime columns with ffill and bfill."""
    fixed_df = fix_nan(sample_df_with_nan)

    # Check that NaNs in datetime column are filled
    assert not fixed_df['datetime'].isna().any()


def test_fix_nan_with_nan_summary(sample_df_with_nan):
    """Test fix_nan with a provided nan_summary."""
    nan_summary = [{'column': 'numeric'}]
    fixed_df = fix_nan(sample_df_with_nan, nan_summary)

    # Only the numeric column should be fixed
    assert not fixed_df['numeric'].isna().any()
    assert fixed_df['string'].isna().any()  # Not fixed
    assert fixed_df['datetime'].isna().any()  # Not fixed


# Tests for fix_duplicates
def test_fix_duplicates_removes_duplicate_rows(sample_df_with_duplicates):
    """Test that fix_duplicates properly removes duplicate rows."""
    fixed_df = fix_duplicates(sample_df_with_duplicates)

    # Check that duplicates are removed
    assert len(fixed_df) == 3
    assert not fixed_df.duplicated().any()


def test_fix_duplicates_with_summary(sample_df_with_duplicates):
    """Test fix_duplicates with a provided duplicate summary."""
    dupe_summary = [
        {'type': 'full_row', 'count': 2},
        {'type': 'column', 'column': 'A', 'count': 1}
    ]
    fixed_df = fix_duplicates(sample_df_with_duplicates, dupe_summary)

    # Check that duplicates are removed
    assert len(fixed_df) == 3


# Tests for fix_gaps
def test_fix_gaps_fills_timeseries_gaps(sample_df_with_gaps):
    """Test that fix_gaps properly fills gaps in time series."""
    original_len = len(sample_df_with_gaps)
    fixed_df = fix_gaps(sample_df_with_gaps, datetime_col='date')

    # Check that gaps are filled
    assert len(fixed_df) > original_len

    # The fixed dataframe should have a continuous date range
    expected_dates = pd.date_range(
        start=sample_df_with_gaps['date'].min(),
        end=sample_df_with_gaps['date'].max(),
        freq='D'
    )
    assert len(fixed_df) == len(expected_dates)


def test_fix_gaps_auto_detection():
    """Test that fix_gaps can automatically detect datetime columns."""
    dates = pd.date_range(start='2022-01-01', end='2022-01-10', freq='D')
    # Create gaps by removing some dates
    dates = dates[dates.day != 5]  # Remove day 5
    df = pd.DataFrame({
        'timestamp': dates,  # Different name than the previous test
        'value': np.random.rand(len(dates))
    })

    # Don't specify datetime_col, let it auto-detect
    original_len = len(df)
    fixed_df = fix_gaps(df)

    # Check that gaps are filled
    assert len(fixed_df) > original_len


def test_fix_gaps_with_numeric_timestamp():
    """Test that fix_gaps can handle numeric timestamp columns."""
    # Create timestamps as unix timestamps (seconds since epoch)
    timestamps = pd.date_range(
        start='2022-01-01', end='2022-01-10', freq='D'
    ).astype(int) // 10**9  # Convert to unix seconds

    # Remove some days to create gaps
    timestamps = timestamps[np.array([0, 1, 2, 4, 6, 8, 9])]

    df = pd.DataFrame({
        'unix_time': timestamps,
        'value': np.random.rand(len(timestamps))
    })

    original_len = len(df)
    fixed_df = fix_gaps(df)

    # Check that gaps are filled
    assert len(fixed_df) > original_len


# Tests for fix_zeros
def test_fix_zeros_fills_price_columns(sample_df_with_zeros):
    """Test that fix_zeros properly fills zero values in price columns."""
    fixed_df = fix_zeros(sample_df_with_zeros)

    # Check that zeros in price and close are fixed
    assert not (fixed_df['price'] == 0).any()
    assert not (fixed_df['close'] == 0).any()

    # Volume may still have zeros, as it's not flagged as an anomaly by default
    assert (fixed_df['volume'] == 0).sum() == 1


def test_fix_zeros_with_zero_summary(sample_df_with_zeros):
    """Test fix_zeros with a provided zero summary."""
    # Mark volume column as an anomaly that should be fixed
    zero_summary = [
        {'column': 'volume', 'anomaly': True},
        {'column': 'other', 'anomaly': False}
    ]

    fixed_df = fix_zeros(sample_df_with_zeros, zero_summary)

    # Check that zeros in volume are fixed (because we marked it as an anomaly)
    assert not (fixed_df['volume'] == 0).any()

    # 'other' should not be fixed as it's marked as not an anomaly
    assert (fixed_df['other'] == 0).sum() == 1


# Tests for fix_negatives
def test_fix_negatives_handles_ohlc_columns(sample_df_with_negatives):
    """Test that fix_negatives properly handles negative values in OHLC columns."""
    fixed_df = fix_negatives(sample_df_with_negatives)

    # Check that negatives in open and close are fixed by taking absolute values
    assert not (fixed_df['open'] < 0).any()
    assert not (fixed_df['close'] < 0).any()
    assert fixed_df['open'].iloc[1] == 1.2  # Absolute value of -1.2
    assert fixed_df['close'].iloc[2] == 3.2  # Absolute value of -3.2

    # Check that negatives in volume are fixed (likely by interpolation)
    assert not (fixed_df['volume'] < 0).any()


def test_fix_negatives_with_summary(sample_df_with_negatives):
    """Test fix_negatives with a provided negative summary."""
    # Only include certain columns in the fix
    negative_summary = [{'column': 'open'}, {'column': 'other'}]

    fixed_df = fix_negatives(sample_df_with_negatives, negative_summary)

    # Check that negatives in open are fixed
    assert not (fixed_df['open'] < 0).any()

    # Check that other is fixed
    assert not (fixed_df['other'] < 0).any()

    # Close and volume should still have negatives (not in the summary)
    assert (fixed_df['close'] < 0).any()
    assert (fixed_df['volume'] < 0).any()


# Tests for fix_infs
def test_fix_infs_replaces_infinite_values(sample_df_with_infs):
    """Test that fix_infs properly replaces infinite values."""
    fixed_df = fix_infs(sample_df_with_infs)

    # Check that there are no more infs
    assert not np.isinf(fixed_df).any().any()


def test_fix_infs_with_summary(sample_df_with_infs):
    """Test fix_infs with a provided inf summary."""
    # Only include certain columns in the fix
    inf_summary = [{'column': 'A'}, {'column': 'C'}]

    fixed_df = fix_infs(sample_df_with_infs, inf_summary)

    # Check that infs in A and C are fixed
    assert not np.isinf(fixed_df['A']).any()
    assert not np.isinf(fixed_df['C']).any()

    # B should still have infs (not in the summary)
    assert np.isinf(fixed_df['B']).any()


# Tests for file operations
@pytest.fixture
def temp_parquet_file(tmp_path):
    """Create a temporary parquet file for testing."""
    file_path = tmp_path / "test.parquet"
    df = pd.DataFrame({
        'numeric': [1.0, np.nan, 3.0, np.nan],
        'price': [10.0, 0.0, 15.0, 20.0]
    })
    df.to_parquet(str(file_path))
    return str(file_path)


@patch('builtins.print')
def test_fix_file(mock_print, temp_parquet_file):
    """Test fix_file function properly processes a parquet file."""
    result = fix_file(
        temp_parquet_file,
        fix_nan_flag=True,
        fix_zeros_flag=True
    )

    # Check that the file was fixed and the backup was created
    assert result is True
    assert os.path.exists(temp_parquet_file + ".bak")

    # Read the fixed file and check that issues were fixed
    fixed_df = pd.read_parquet(temp_parquet_file)
    assert not fixed_df['numeric'].isna().any()  # NaNs should be fixed
    assert not (fixed_df['price'] == 0).any()  # Zeros should be fixed


@patch('builtins.print')
@patch('src.eda.fix_files.fix_file')
def test_batch_fix_files(mock_fix_file, mock_print, tmp_path):
    """Test batch_fix_files function properly processes multiple parquet files."""
    # Create a few test parquet files
    for i in range(3):
        file_path = tmp_path / f"test_{i}.parquet"
        df = pd.DataFrame({'value': [i, i+1, i+2]})
        df.to_parquet(str(file_path))

    # Set up the mock to return True (indicating file was fixed)
    mock_fix_file.return_value = True

    # Run batch fix
    fixed_count, total_count = batch_fix_files(
        str(tmp_path),
        fix_nan_flag=True,
        fix_zeros_flag=True
    )

    # Check the results
    assert fixed_count == 3  # All 3 files should be "fixed"
    assert total_count == 3  # Total count should be 3

    # The fix_file function should have been called 3 times
    assert mock_fix_file.call_count == 3
