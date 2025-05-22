import pytest
import pandas as pd
import numpy as np
from io import StringIO
import sys

from src.eda import basic_stats

# Test data fixtures
@pytest.fixture
def sample_numeric_df():
    """Create a simple dataframe with numeric columns for testing."""
    return pd.DataFrame({
        'open': [10.5, 11.2, 10.8, 11.5, np.nan],
        'high': [11.5, 11.8, 11.2, 12.0, 11.9],
        'low': [10.2, 10.9, 10.5, 11.2, 11.0],
        'close': [11.0, 11.5, 11.0, 11.8, 11.5],
        'volume': [1000, 1200, 800, 1500, 1100]
    })

@pytest.fixture
def sample_mixed_df():
    """Create a dataframe with mixed data types."""
    return pd.DataFrame({
        'open': [10.5, 11.2, 10.8, 11.5, np.nan],
        'high': [11.5, 11.8, 11.2, 12.0, 11.9],
        'symbol': ['AAPL', 'AAPL', 'AAPL', 'MSFT', 'MSFT'],
        'date': pd.date_range(start='2023-01-01', periods=5)
    })

@pytest.fixture
def sample_time_series_df():
    """Create a dataframe specifically for time series analysis."""
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=30),
        'open': np.linspace(100, 120, 30) + np.random.normal(0, 1, 30),
        'high': np.linspace(102, 122, 30) + np.random.normal(0, 1, 30),
        'low': np.linspace(98, 118, 30) + np.random.normal(0, 1, 30),
        'close': np.linspace(101, 121, 30) + np.random.normal(0, 1, 30),
        'volume': np.random.randint(1000, 2000, 30)
    })
    # Add a non-stationary trend
    df['trend'] = np.linspace(10, 50, 30)
    # Add a stationary column
    df['stationary'] = np.random.normal(0, 1, 30)
    return df

# Tests for compute_basic_stats
def test_compute_basic_stats_numeric(sample_numeric_df):
    """Test compute_basic_stats with numeric data."""
    result = basic_stats.compute_basic_stats(sample_numeric_df)

    # Check that all columns are present
    assert set(result.keys()) == set(sample_numeric_df.columns)

    # Check numeric column statistics
    for col in ['open', 'high', 'low', 'close', 'volume']:
        assert 'mean' in result[col]
        assert 'median' in result[col]
        assert 'std' in result[col]
        assert 'min' in result[col]
        assert 'max' in result[col]
        assert 'missing' in result[col]

    # Check specific values
    assert result['open']['missing'] == 1
    assert result['high']['missing'] == 0
    assert result['volume']['mean'] == 1120.0

def test_compute_basic_stats_mixed(sample_mixed_df):
    """Test compute_basic_stats with mixed data types."""
    result = basic_stats.compute_basic_stats(sample_mixed_df)

    # Check numeric vs non-numeric handling
    assert 'mean' in result['open']
    assert 'std' in result['high']

    # Check categorical stats
    assert 'mean' not in result['symbol']
    assert 'unique' in result['symbol']
    assert 'top' in result['symbol']
    assert 'freq' in result['symbol']

    # Check specific values
    assert result['symbol']['unique'] == 2
    assert result['symbol']['top'] == 'AAPL'
    assert result['symbol']['freq'] == 3

# Tests for descriptive_stats
def test_descriptive_stats(sample_numeric_df):
    """Test descriptive_stats function."""
    result = basic_stats.descriptive_stats(sample_numeric_df)

    # Check that columns are present
    assert set(result.keys()) == set(sample_numeric_df.columns)

    # Check all expected stats
    for col in result:
        assert 'mean' in result[col]
        assert 'median' in result[col]
        assert 'std' in result[col]
        assert 'var' in result[col]
        assert 'mode' in result[col]
        assert '25%' in result[col]
        assert '75%' in result[col]
        assert 'missing' in result[col]
        assert 'missing_pct' in result[col]

    # Check specific values
    assert result['open']['missing'] == 1
    assert result['open']['missing_pct'] == 20.0  # 1 missing out of 5 = 20%
    assert isinstance(result['high']['mode'], float)

def test_descriptive_stats_all_missing():
    """Test descriptive_stats with a column that has all missing values."""
    df = pd.DataFrame({'all_missing': [np.nan, np.nan, np.nan]})
    result = basic_stats.descriptive_stats(df)

    assert 'all_missing' in result
    assert 'error' in result['all_missing']

# Tests for distribution_analysis
def test_distribution_analysis(sample_numeric_df):
    """Test distribution_analysis function."""
    result = basic_stats.distribution_analysis(sample_numeric_df)

    # Check that only numeric columns are analyzed
    assert set(result.keys()) == set(sample_numeric_df.columns)

    # Check expected statistics
    for col in result:
        if 'error' not in result[col]:
            assert 'skewness' in result[col]
            assert 'kurtosis' in result[col]
            # Normality test might be None if not enough data points
            if result[col]['normality_test'] is not None:
                assert len(result[col]['normality_test']) == 2
                assert 'is_normal' in result[col]

def test_distribution_analysis_with_small_dataset():
    """Test distribution_analysis with a small dataset (< 8 items)."""
    df = pd.DataFrame({'small': [1, 2, 3, 4, 5]})
    result = basic_stats.distribution_analysis(df)

    assert 'small' in result
    assert result['small']['normality_test'] is None
    assert result['small']['is_normal'] == 'Unknown'

# Tests for outlier_analysis
def test_outlier_analysis(sample_numeric_df):
    """Test outlier_analysis function."""
    result = basic_stats.outlier_analysis(sample_numeric_df)

    # Check that only numeric columns are analyzed
    assert set(result.keys()) == set(sample_numeric_df.columns)

    # Check IQR method
    for col in result:
        if 'error' not in result[col]:
            assert 'iqr_method' in result[col]
            assert 'lower_bound' in result[col]['iqr_method']
            assert 'upper_bound' in result[col]['iqr_method']
            assert 'outliers_count' in result[col]['iqr_method']
            assert 'outlier_percentage' in result[col]['iqr_method']
            assert 'outlier_indices' in result[col]['iqr_method']

            # Check Z-score method
            assert 'z_score_method' in result[col]
            assert 'outliers_count' in result[col]['z_score_method']
            assert 'outlier_percentage' in result[col]['z_score_method']
            assert 'outlier_indices' in result[col]['z_score_method']

def test_outlier_analysis_with_outliers():
    """Test outlier_analysis with a dataset containing clear outliers."""
    # Create a DataFrame with a more extreme outlier to ensure Z-score > 3.
    # For a standard Z-score (threshold=3), N must be at least 11 for an outlier
    # to potentially exceed this threshold (max Z-score is sqrt(N-1)).
    # Original data (N=6) had max Z-score of sqrt(5) ~ 2.236.
    # New data has N=11. The outlier 1000 is at index 10.
    data_values = [10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 1000]
    df = pd.DataFrame({'with_outliers': data_values})
    result = basic_stats.outlier_analysis(df)

    assert result['with_outliers']['iqr_method']['outliers_count'] >= 1
    assert result['with_outliers']['z_score_method']['outliers_count'] >= 1

    # Check that the index of the outlier (1000) is correctly identified
    # The value 1000 is at index 10 in data_values.
    outlier_index = 10
    assert outlier_index in result['with_outliers']['iqr_method']['outlier_indices']
    assert outlier_index in result['with_outliers']['z_score_method']['outlier_indices']

# Tests for time_series_analysis
def test_time_series_analysis(sample_time_series_df):
    """Test time_series_analysis function with datetime index."""
    result = basic_stats.time_series_analysis(sample_time_series_df)

    # Check for the components
    assert 'features' in result
    assert 'stationarity' in result
    assert 'seasonality' in result

    # Check stationarity test results - trend should be non-stationary,
    # stationary column should be stationary (though this is probabilistic)
    if 'trend' in result['stationarity']:
        assert not result['stationarity']['trend']['is_stationary']

    # Test for price range calculation
    if 'price_range' in result['features']:
        assert 'mean' in result['features']['price_range']
        assert 'median' in result['features']['price_range']
        assert 'std' in result['features']['price_range']

def test_time_series_analysis_no_datetime():
    """Test time_series_analysis function without datetime columns."""
    df = pd.DataFrame({
        'open': [10, 11, 12],
        'high': [12, 13, 14],
        'low': [9, 10, 11],
        'close': [11, 12, 13]
    })
    result = basic_stats.time_series_analysis(df)

    # Should create synthetic datetime index
    assert 'warning' in result
    assert 'synthetic' in result['warning']

# Tests for print functions (checking they don't error)
def test_print_basic_stats_summary():
    """Test print_basic_stats_summary doesn't raise exceptions."""
    stats = {
        'open': {'mean': 10.5, 'median': 10.0, 'std': 1.0, 'min': 9.0, 'max': 11.0,
                '25%': 9.5, '50%': 10.0, '75%': 10.8, 'missing': 1, 'unique': 4},
        'close': {'mean': 11.5, 'median': 11.0, 'std': 1.0, 'min': 10.0, 'max': 12.0,
                 '25%': 10.5, '50%': 11.0, '75%': 11.8, 'missing': 0, 'unique': 5},
        'symbol': {'missing': 0, 'unique': 2, 'top': 'AAPL', 'freq': 3}
    }

    # Redirect stdout to capture print output
    captured_output = StringIO()
    sys.stdout = captured_output

    # Call function
    basic_stats.print_basic_stats_summary(stats)

    # Reset stdout
    sys.stdout = sys.__stdout__

    # Check that output contains expected strings
    output = captured_output.getvalue()
    assert "Summary and Recommendations" in output
    assert "numeric and" in output  # Should mention numeric and non-numeric columns

def test_print_descriptive_stats():
    """Test print_descriptive_stats doesn't raise exceptions and prints expected content."""
    stats_data = {
        'open': {
            'mean': 10.5, 'median': 10.0, 'std': 1.0, 'var': 1.0,
            'min': 9.0, 'max': 11.0, 'mode': 10.0,
            '25%': 9.5, '75%': 10.8,  # '50%' key removed
            # 'iqr': 1.3,  # Removed, print_descriptive_stats will calculate it
            # 'range': 2.0, # Removed, print_descriptive_stats will calculate it
            'coef_variation': 1.0 / 10.5,
            'data_points': 4,
            'missing': 1, 'missing_pct': 20.0
        }
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    basic_stats.print_descriptive_stats(stats_data)
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Descriptive Statistics" in output  # Main title, no leading spaces
    assert "\n\033[93mColumn: open\033[0m" in output  # Check with color codes for more precision
    assert "  Mean: 10.5000" in output
    assert "  Median: 10.0000" in output
    assert "  Mode: 10.0" in output  # Mode is printed as a string
    assert "  Range: 2.0000 (Min: 9.0000, Max: 11.0000)" in output
    assert "  IQR: 1.3000 (Q1: 9.5000, Q3: 10.8000)" in output
    assert f"  Coefficient of Variation: {(1.0/10.5):.4f}" in output
    assert "  Data Points: 4 (Missing: 1 - 20.00%)" in output

def test_print_distribution_analysis():
    """Test print_distribution_analysis doesn't raise exceptions."""
    stats = {
        'open': {'skewness': 0.1, 'kurtosis': -0.5,
                 'normality_test': (0.1, 0.8), 'is_normal': 'Yes'},
        'close': {'skewness': 1.5, 'kurtosis': 4.0,
                  'normality_test': (0.5, 0.01), 'is_normal': 'No'},
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    basic_stats.print_distribution_analysis(stats)
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Distribution Analysis" in output
    assert "skewed" in output.lower()
    assert "Slightly positive skewed" in output  # For open with skewness 0.1
    assert "Highly positive skewed" in output  # For close with skewness 1.5
    assert "Leptokurtic" in output  # For close with kurtosis 4.0

def test_print_outlier_analysis():
    """Test print_outlier_analysis doesn't raise exceptions."""
    stats = {
        'price': {
            'iqr_method': {
                'lower_bound': 8.0, 'upper_bound': 12.0,
                'outliers_count': 2, 'outlier_percentage': 10.0,
                'outlier_indices': [4, 9]
            },
            'z_score_method': {
                'outliers_count': 1, 'outlier_percentage': 5.0,
                'outlier_indices': [9]
            }
        }
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    basic_stats.print_outlier_analysis(stats)
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Outlier Analysis" in output

def test_print_time_series_analysis():
    """Test print_time_series_analysis doesn't raise exceptions."""
    ts_stats = {
        'features': {
            'price_range': {'mean': 1.0, 'median': 0.9, 'std': 0.2},
            'price_change': {'mean': 0.1, 'median': 0.05, 'std': 0.3}
        },
        'stationarity': {
            'close': {'test_statistic': -3.5, 'p_value': 0.01, 'is_stationary': True,
                      'critical_values': {'1%': -3.4, '5%': -2.8, '10%': -2.5}},
            'trend': {'test_statistic': -1.5, 'p_value': 0.4, 'is_stationary': False,
                     'critical_values': {'1%': -3.4, '5%': -2.8, '10%': -2.5}}
        },
        'seasonality': {
            'day_of_week': {0: 11.2, 1: 11.4, 2: 11.3, 3: 11.5, 4: 11.7}
        }
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    basic_stats.print_time_series_analysis(ts_stats)
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Time Series Analysis" in output
    assert "Stationarity" in output
