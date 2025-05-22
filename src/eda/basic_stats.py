# Handles basic statistics

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller

def compute_basic_stats(df):
    """
    Compute basic statistics for each column in the DataFrame.
    Returns a dictionary with stats for each column.
    """
    stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            stats[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                '25%': df[col].quantile(0.25),
                '50%': df[col].quantile(0.5),
                '75%': df[col].quantile(0.75),
                'missing': int(df[col].isnull().sum()),
                'unique': int(df[col].nunique())
            }
        else:
            stats[col] = {
                'missing': int(df[col].isnull().sum()),
                'unique': int(df[col].nunique()),
                'top': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'freq': int(df[col].value_counts().iloc[0]) if not df[col].value_counts().empty else 0
            }
    return stats

def descriptive_stats(df):
    """
    Compute detailed descriptive statistics for numeric columns.
    Returns a dictionary with extended stats for each numeric column.
    """
    desc_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                desc_stats[col] = {
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'std': col_data.std(),
                    'var': col_data.var(),
                    'mode': float(stats.mode(col_data, keepdims=False)[0]) if len(col_data) > 0 else None,
                    'min': col_data.min(),
                    'max': col_data.max(),
                    '25%': col_data.quantile(0.25),
                    '50%': col_data.quantile(0.5),
                    '75%': col_data.quantile(0.75),
                    'count': len(col_data),
                    'missing': int(df[col].isnull().sum()),
                    'missing_pct': round(df[col].isnull().sum() / len(df) * 100, 2)
                }
            else:
                desc_stats[col] = {'error': 'No valid data points'}
    return desc_stats

def distribution_analysis(df):
    """
    Analyze distributions of numeric columns by calculating skewness and kurtosis.
    Returns a dictionary with distribution stats for each numeric column.
    """
    dist_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                dist_stats[col] = {
                    'skewness': stats.skew(col_data),
                    'kurtosis': stats.kurtosis(col_data),
                    'normality_test': stats.normaltest(col_data) if len(col_data) >= 8 else None,
                    'is_normal': 'Unknown' if len(col_data) < 8 else (
                        'Yes' if stats.normaltest(col_data)[1] > 0.05 else 'No'
                    )
                }
            else:
                dist_stats[col] = {'error': 'No valid data points'}
    return dist_stats

def outlier_analysis(df):
    """
    Detect outliers in numeric columns using IQR and Z-score methods.
    Returns a dictionary with outlier stats for each numeric column.
    """
    outlier_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                # IQR method
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                iqr_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

                # Z-score method
                z_scores = np.abs(stats.zscore(col_data))
                z_outliers = df.iloc[np.where(z_scores > 3)[0]]

                outlier_stats[col] = {
                    'iqr_method': {
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'outlier_count': len(iqr_outliers),
                        'outlier_percentage': round(len(iqr_outliers) / len(df) * 100, 2),
                        'outlier_indices': iqr_outliers.index.tolist()[:10]  # Limit to first 10
                    },
                    'z_score_method': {
                        'outlier_count': len(z_outliers),
                        'outlier_percentage': round(len(z_outliers) / len(df) * 100, 2),
                        'outlier_indices': z_outliers.index.tolist()[:10]  # Limit to first 10
                    }
                }
            else:
                outlier_stats[col] = {'error': 'No valid data points'}
    return outlier_stats

def time_series_analysis(df):
    """
    Perform basic time series analysis including trend and seasonality detection.
    Requires a DataFrame with at least one datetime column and OHLC price data.
    """
    ts_stats = {'features': {}, 'stationarity': {}, 'seasonality': {}}

    # Try to identify datetime column
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]

    # Try to identify OHLCV columns
    ohlc_patterns = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col]) and
        any(pat in col.lower() for pat in ['open', 'high', 'low', 'close', 'volume'])
    ]

    # If we don't have datetime or OHLC columns, return with a message
    if not datetime_cols:
        ts_stats['error'] = 'No datetime columns found for time series analysis'
        return ts_stats

    # Use the first datetime column as the index
    date_col = datetime_cols[0]
    df_ts = df.copy()
    df_ts.set_index(date_col, inplace=True)

    # Calculate derived features if we have OHLC data
    if len([col for col in ohlc_patterns if 'high' in col.lower()]) > 0 and len([col for col in ohlc_patterns if 'low' in col.lower()]) > 0:
        high_col = [col for col in ohlc_patterns if 'high' in col.lower()][0]
        low_col = [col for col in ohlc_patterns if 'low' in col.lower()][0]
        ts_stats['features']['daily_range'] = {
            'mean': (df_ts[high_col] - df_ts[low_col]).mean(),
            'median': (df_ts[high_col] - df_ts[low_col]).median(),
            'std': (df_ts[high_col] - df_ts[low_col]).std()
        }

    if len([col for col in ohlc_patterns if 'open' in col.lower()]) > 0 and len([col for col in ohlc_patterns if 'close' in col.lower()]) > 0:
        open_col = [col for col in ohlc_patterns if 'open' in col.lower()][0]
        close_col = [col for col in ohlc_patterns if 'close' in col.lower()][0]
        ts_stats['features']['daily_change'] = {
            'mean': (df_ts[close_col] - df_ts[open_col]).mean(),
            'median': (df_ts[close_col] - df_ts[open_col]).median(),
            'std': (df_ts[close_col] - df_ts[open_col]).std()
        }

    # Stationarity test (ADF)
    for col in ohlc_patterns:
        if df_ts[col].count() > 10:  # Need sufficient data points
            try:
                adf_result = adfuller(df_ts[col].dropna())
                ts_stats['stationarity'][col] = {
                    'test_statistic': adf_result[0],
                    'p_value': adf_result[1],
                    'is_stationary': adf_result[1] < 0.05,
                    'critical_values': adf_result[4]
                }
            except:
                ts_stats['stationarity'][col] = {'error': 'ADF test failed'}

    # Basic seasonality check - day of week patterns
    if hasattr(df_ts.index, 'dayofweek'):
        for col in ohlc_patterns:
            if 'close' in col.lower():
                try:
                    # Calculate mean closing price by day of week
                    day_means = df_ts.groupby(df_ts.index.dayofweek)[col].mean()
                    ts_stats['seasonality']['day_of_week'] = {day: mean for day, mean in enumerate(day_means)}
                except:
                    ts_stats['seasonality']['day_of_week'] = {'error': 'Day of week analysis failed'}

    return ts_stats

def print_descriptive_stats(desc_stats):
    """Print descriptive statistics in a readable format."""
    print("\n\033[1m\033[94mDescriptive Statistics:\033[0m")

    for col, stats in desc_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            max_key_length = max(len(key) for key in stats.keys())
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"  {key.ljust(max_key_length)}: {value:.4f}")
                else:
                    print(f"  {key.ljust(max_key_length)}: {value}")

def print_distribution_analysis(dist_stats):
    """Print distribution analysis in a readable format."""
    print("\n\033[1m\033[94mDistribution Analysis:\033[0m")

    for col, stats in dist_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            print(f"  Skewness: {stats['skewness']:.4f}")
            print(f"  Kurtosis: {stats['kurtosis']:.4f}")
            if stats['normality_test'] is not None:
                print(f"  Normality test p-value: {stats['normality_test'][1]:.4f}")
                print(f"  Distribution appears normal: {stats['is_normal']}")
            else:
                print("  Normality test: Not enough data points")

def print_outlier_analysis(outlier_stats):
    """Print outlier analysis in a readable format."""
    print("\n\033[1m\033[94mOutlier Analysis:\033[0m")

    for col, stats in outlier_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            print("  IQR Method:")
            print(f"    Lower bound: {stats['iqr_method']['lower_bound']:.4f}")
            print(f"    Upper bound: {stats['iqr_method']['upper_bound']:.4f}")
            print(f"    Outlier count: {stats['iqr_method']['outlier_count']}")
            print(f"    Outlier percentage: {stats['iqr_method']['outlier_percentage']}%")

            print("  Z-Score Method:")
            print(f"    Outlier count: {stats['z_score_method']['outlier_count']}")
            print(f"    Outlier percentage: {stats['z_score_method']['outlier_percentage']}%")

            if stats['iqr_method']['outlier_indices']:
                print(f"  Sample outlier indices (IQR): {', '.join(map(str, stats['iqr_method']['outlier_indices']))}")

def print_time_series_analysis(ts_stats):
    """Print time series analysis in a readable format."""
    print("\n\033[1m\033[94mTime Series Analysis:\033[0m")

    if 'error' in ts_stats:
        print(f"  Error: {ts_stats['error']}")
        return

    if 'features' in ts_stats and ts_stats['features']:
        print("\n\033[96mDerived Features:\033[0m")
        for feature, stats in ts_stats['features'].items():
            print(f"  {feature.replace('_', ' ').title()}:")
            for stat, value in stats.items():
                print(f"    {stat.title()}: {value:.4f}")

    if 'stationarity' in ts_stats and ts_stats['stationarity']:
        print("\n\033[96mStationarity Tests (ADF):\033[0m")
        for col, result in ts_stats['stationarity'].items():
            print(f"  {col}:")
            if 'error' in result:
                print(f"    Error: {result['error']}")
            else:
                print(f"    Test statistic: {result['test_statistic']:.4f}")
                print(f"    p-value: {result['p_value']:.4f}")
                print(f"    Is stationary: {'Yes' if result['is_stationary'] else 'No'}")

    if 'seasonality' in ts_stats and ts_stats['seasonality']:
        print("\n\033[96mSeasonality Analysis:\033[0m")
        if 'day_of_week' in ts_stats['seasonality']:
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_stats = ts_stats['seasonality']['day_of_week']
            if 'error' in dow_stats:
                print(f"  Day of Week: {dow_stats['error']}")
            else:
                print("  Average by Day of Week:")
                for day_num, mean_value in dow_stats.items():
                    print(f"    {day_names[day_num]}: {mean_value:.4f}")

