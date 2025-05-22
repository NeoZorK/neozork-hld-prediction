# Handles basic statistics

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
from matplotlib.figure import Figure
from io import BytesIO
import base64
import webbrowser

# Suppress matplotlib warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Set seaborn style for better looking plots
sns.set(style="whitegrid")

def ensure_plots_directory():
    """Ensure plots directory exists for saving visualizations."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    plots_dir = os.path.join(base_dir, 'results', 'plots')

    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    return plots_dir

def open_last_plot_in_browser(plot_path):
    """Open the last created plot in the default web browser."""
    if os.path.exists(plot_path):
        webbrowser.open(f'file://{os.path.abspath(plot_path)}')
        print(f"\033[93m[INFO]\033[0m Last plot opened in your default browser: {plot_path}")
    else:
        print(f"\033[91m[ERROR]\033[0m Plot file not found: {plot_path}")

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

def print_basic_stats_summary(stats_result):
    """Print summary and recommendations for basic statistics."""
    # Identify columns with high missing values
    high_missing_cols = []
    numeric_cols = []
    categorical_cols = []
    high_cardinality_cols = []
    low_cardinality_cols = []

    for col, stats in stats_result.items():
        # Check for numeric columns
        if 'std' in stats:
            numeric_cols.append(col)

            # Check for high missing values
            if stats['missing'] > 0:
                missing_pct = stats['missing'] / (stats['missing'] + stats['unique']) * 100
                if missing_pct > 5:
                    high_missing_cols.append((col, missing_pct))
        else:
            categorical_cols.append(col)
            # Check cardinality
            if stats['unique'] > 100:
                high_cardinality_cols.append((col, stats['unique']))
            elif stats['unique'] < 5 and stats['unique'] > 1:
                low_cardinality_cols.append((col, stats['unique']))

    # Print summary
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print(f"  • Dataset contains {len(numeric_cols)} numeric and {len(categorical_cols)} non-numeric columns")

    if high_missing_cols:
        print(f"  • {len(high_missing_cols)} columns have significant missing values (>5%):")
        for col, pct in sorted(high_missing_cols, key=lambda x: x[1], reverse=True)[:5]:  # Show top 5
            print(f"    - {col}: {pct:.1f}% missing")
        if len(high_missing_cols) > 5:
            print(f"    - ... and {len(high_missing_cols) - 5} more columns")
        print("  • Consider handling missing values with imputation or feature removal")

    if high_cardinality_cols:
        print(f"  • High cardinality categorical features: {len(high_cardinality_cols)} columns")
        print("  • Consider encoding methods like target encoding for these columns")

    if low_cardinality_cols:
        print(f"  • Low cardinality features: {len(low_cardinality_cols)} columns")
        print("  • These might be good candidates for one-hot encoding")

    print("  • Next steps:")
    print("    - Run --descriptive-stats for more detailed statistics")
    print("    - Check distributions with --distribution-analysis")
    print("    - Run --correlation-analysis to understand relationships between features")

    # Visualization for basic stats
    plots_dir = ensure_plots_directory()
    numeric_cols = [col for col, s in stats_result.items() if 'std' in s]
    if numeric_cols:
        plt.figure(figsize=(10, 6))
        means = [stats_result[col]['mean'] for col in numeric_cols]
        stds = [stats_result[col]['std'] for col in numeric_cols]
        sns.barplot(x=numeric_cols, y=means, color='skyblue', edgecolor='black')
        plt.xticks(rotation=45)
        plt.ylabel('Mean Value')
        plt.title('Mean of Numeric Columns (Basic Stats)')
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'basic_stats_means.png')
        plt.savefig(plot_path)
        print(f"\033[96m[INFO]\033[0m Basic stats mean plot saved to: {plot_path}")
        plt.close()
        open_last_plot_in_browser(plot_path)
        print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")

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

def visualize_descriptive_stats(df, desc_stats, file_name="descriptive_stats"):
    """Create visualizations for descriptive statistics."""
    plots_dir = ensure_plots_directory()

    # Only process numeric columns
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_cols:
        return

    # Select first few columns to visualize (up to 5)
    cols_to_plot = numeric_cols[:min(5, len(numeric_cols))]

    # 1. Create boxplot of key numeric columns
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(data=df[cols_to_plot])
    plt.title("Boxplot of Key Numeric Features", fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot
    box_plot_path = os.path.join(plots_dir, f"{file_name}_boxplot.png")
    plt.savefig(box_plot_path)
    print(f"\n\033[96mBoxplot saved to: {box_plot_path}\033[0m")
    plt.close()

    # 2. Create a pairplot for selected numeric columns if there are at least 2
    if len(cols_to_plot) >= 2:
        plt.figure(figsize=(10, 8))
        scatter_plot = sns.pairplot(
            df[cols_to_plot],
            diag_kind='kde',
            plot_kws={'alpha': 0.6, 's': 30, 'edgecolor': 'k'}
        )
        plt.suptitle("Pairwise Relationships Between Features", y=1.02, fontsize=16)

        # Save plot
        pairplot_path = os.path.join(plots_dir, f"{file_name}_pairplot.png")
        scatter_plot.savefig(pairplot_path)
        print(f"\033[96mPairplot saved to: {pairplot_path}\033[0m")
        plt.close()

    # 3. Create correlation heatmap
    if len(cols_to_plot) >= 2:
        plt.figure(figsize=(10, 8))
        corr = df[cols_to_plot].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        heatmap = sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap='coolwarm',
            square=True,
            linewidths=.5,
            cbar_kws={"shrink": .8}
        )
        plt.title("Correlation Heatmap", fontsize=14)
        plt.tight_layout()

        # Save plot
        heatmap_path = os.path.join(plots_dir, f"{file_name}_correlation_heatmap.png")
        plt.savefig(heatmap_path)
        print(f"\033[96mCorrelation heatmap saved to: {heatmap_path}\033[0m")
        plt.close()

def visualize_distribution_analysis(df, dist_stats, file_name="distribution_analysis"):
    """Create visualizations for distribution analysis."""
    plots_dir = ensure_plots_directory()

    # Only process numeric columns
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_cols:
        return

    # Select columns with different distribution characteristics for visualization (up to 4)
    normal_cols = [col for col in numeric_cols if col in dist_stats and
                  'is_normal' in dist_stats[col] and dist_stats[col]['is_normal'] == 'Yes']
    highly_skewed_cols = [col for col in numeric_cols if col in dist_stats and
                         'skewness' in dist_stats[col] and abs(dist_stats[col]['skewness']) > 1]

    # Select a mix of normal and skewed columns for better visualization variety
    cols_to_plot = []
    if normal_cols:
        cols_to_plot.extend(normal_cols[:2])
    if highly_skewed_cols:
        cols_to_plot.extend(highly_skewed_cols[:2])

    # If we still don't have enough columns, add other numeric columns
    remaining_cols = [col for col in numeric_cols if col not in cols_to_plot]
    cols_to_plot.extend(remaining_cols[:4 - len(cols_to_plot)])

    # Limit to 4 columns for better visualization
    cols_to_plot = cols_to_plot[:4]

    if not cols_to_plot:
        return

    # 1. Create histograms with density plots for selected columns
    fig, axes = plt.subplots(len(cols_to_plot), 1, figsize=(10, 3 * len(cols_to_plot)), constrained_layout=True)
    if len(cols_to_plot) == 1:
        axes = [axes]

    for i, col in enumerate(cols_to_plot):
        # Get distribution statistics
        if col in dist_stats and 'error' not in dist_stats[col]:
            skew = dist_stats[col].get('skewness', 'N/A')
            kurt = dist_stats[col].get('kurtosis', 'N/A')
            is_normal = dist_stats[col].get('is_normal', 'Unknown')

            # Plot histogram with KDE
            sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color='skyblue', edgecolor='black')

            # Add distribution information as title
            axes[i].set_title(f'{col} (Skew: {skew:.2f}, Kurt: {kurt:.2f}, Normal: {is_normal})')
            axes[i].set_ylabel('Frequency')

            # Add a vertical line for mean and median
            mean_val = df[col].mean()
            median_val = df[col].median()
            axes[i].axvline(mean_val, color='r', linestyle='-', linewidth=1, label=f'Mean: {mean_val:.2f}')
            axes[i].axvline(median_val, color='g', linestyle='--', linewidth=1, label=f'Median: {median_val:.2f}')
            axes[i].legend()
        else:
            axes[i].text(0.5, 0.5, f"No valid data for {col}", horizontalalignment='center',
                        verticalalignment='center', transform=axes[i].transAxes)

    fig.suptitle("Distribution Analysis: Histograms with Density Curves", fontsize=16)

    # Save the plot
    hist_path = os.path.join(plots_dir, f"{file_name}_histograms.png")
    plt.savefig(hist_path)
    print(f"\n\033[96mDistribution histograms saved to: {hist_path}\033[0m")
    plt.close()

    # 2. Create QQ plots for normality check
    fig, axes = plt.subplots(len(cols_to_plot), 1, figsize=(10, 3 * len(cols_to_plot)), constrained_layout=True)
    if len(cols_to_plot) == 1:
        axes = [axes]

    for i, col in enumerate(cols_to_plot):
        # Get distribution statistics
        if col in dist_stats and 'error' not in dist_stats[col]:
            # Create QQ plot
            from scipy import stats as scipy_stats
            col_data = df[col].dropna()
            if len(col_data) > 0:
                qq = scipy_stats.probplot(col_data, dist="norm", plot=axes[i])
                is_normal = dist_stats[col].get('is_normal', 'Unknown')
                axes[i].set_title(f'QQ Plot for {col} (Normal: {is_normal})')
            else:
                axes[i].text(0.5, 0.5, f"No valid data for {col}", horizontalalignment='center',
                            verticalalignment='center', transform=axes[i].transAxes)
        else:
            axes[i].text(0.5, 0.5, f"No valid data for {col}", horizontalalignment='center',
                        verticalalignment='center', transform=axes[i].transAxes)

    fig.suptitle("Distribution Analysis: QQ Plots for Normality Check", fontsize=16)

    # Save the plot
    qq_path = os.path.join(plots_dir, f"{file_name}_qqplots.png")
    plt.savefig(qq_path)
    print(f"\033[96mQQ plots saved to: {qq_path}\033[0m")
    plt.close()

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

    # First try to identify pre-existing datetime columns
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]

    # Common timestamp column names to check if we don't find datetime columns
    common_date_cols = ['date', 'time', 'timestamp', 'datetime', 'dt', 'created_at', 'updated_at',
                        'date_time', 'trade_date', 'effective_date', 'execution_date']

    # If no datetime columns found, try to convert potential date columns based on column names
    if not datetime_cols:
        df_copy = df.copy()  # Create a copy to avoid modifying the original dataframe

        # Try common date column names first
        for col in df.columns:
            col_lower = col.lower()
            if any(date_name in col_lower for date_name in common_date_cols):
                try:
                    df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                    if not df_copy[col].isna().all():  # If not all values became NaN
                        datetime_cols.append(col)
                except:
                    continue

        # If still no datetime columns, try any string/object columns
        if not datetime_cols:
            for col in df.columns:
                if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                    try:
                        # Check if first few non-null values look like dates
                        sample_values = df[col].dropna().iloc[:5].tolist()
                        if not sample_values:
                            continue

                        # Try to convert sample values to see if they look like dates
                        converted = pd.to_datetime(sample_values, errors='coerce')
                        if not converted.isna().all():  # If at least one converted successfully
                            # Convert the whole column
                            df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                            if not df_copy[col].isna().all() and df_copy[col].notna().sum() > len(df) * 0.5:  # If >50% converted
                                datetime_cols.append(col)
                    except:
                        continue

        # If we found datetime columns, use the copy with converted dates
        if datetime_cols:
            df = df_copy

    # Try to identify OHLCV columns
    ohlc_patterns = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col]) and
        any(pat in col.lower() for pat in ['open', 'high', 'low', 'close', 'volume'])
    ]

    # If we don't have OHLCV columns, try to identify any numeric columns for analysis
    if not ohlc_patterns:
        numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        # For non-OHLCV data, we'll still do some analysis if we have numeric columns
        if numeric_cols:
            ohlc_patterns = numeric_cols[:min(5, len(numeric_cols))]  # Use up to 5 numeric columns
            ts_stats['warning'] = 'No OHLCV columns detected, using available numeric columns for limited analysis.'

    # If we don't have datetime columns, try to create a synthetic time index
    if not datetime_cols and len(df) > 1:
        ts_stats['warning'] = 'No datetime columns found. Creating a synthetic time index for analysis.'
        # Create a time index spanning the length of the DataFrame
        df = df.copy()  # Create a copy to avoid modifying the original
        synthetic_index = pd.date_range(start='2000-01-01', periods=len(df), freq='D')
        df['synthetic_datetime'] = synthetic_index
        datetime_cols = ['synthetic_datetime']

    # If we still don't have datetime or numeric columns, return with a message
    if not datetime_cols:
        ts_stats['error'] = 'No datetime columns found and unable to create synthetic index.'
        return ts_stats

    if not ohlc_patterns:
        ts_stats['error'] = 'No numeric columns found for time series analysis.'
        return ts_stats

    # Use the first datetime column as the index
    date_col = datetime_cols[0]
    df_ts = df.copy()
    df_ts.set_index(date_col, inplace=True)

    # Calculate derived features if we have appropriate data
    # If we have both high and low columns, calculate daily range
    high_cols = [col for col in ohlc_patterns if 'high' in col.lower()]
    low_cols = [col for col in ohlc_patterns if 'low' in col.lower()]
    if high_cols and low_cols:
        high_col = high_cols[0]
        low_col = low_cols[0]
        ts_stats['features']['price_range'] = {
            'mean': (df_ts[high_col] - df_ts[low_col]).mean(),
            'median': (df_ts[high_col] - df_ts[low_col]).median(),
            'std': (df_ts[high_col] - df_ts[low_col]).std()
        }

    # If we have both open and close columns, calculate daily change
    open_cols = [col for col in ohlc_patterns if 'open' in col.lower()]
    close_cols = [col for col in ohlc_patterns if 'close' in col.lower()]
    if open_cols and close_cols:
        open_col = open_cols[0]
        close_col = close_cols[0]
        ts_stats['features']['price_change'] = {
            'mean': (df_ts[close_col] - df_ts[open_col]).mean(),
            'median': (df_ts[close_col] - df_ts[open_col]).median(),
            'std': (df_ts[close_col] - df_ts[open_col]).std()
        }

    # For each numeric column, calculate some time series features
    for col in ohlc_patterns:
        if df_ts[col].count() > 10:  # Need sufficient data points
            # Calculate rolling statistics
            try:
                ts_stats['features'][f'{col}_trends'] = {
                    'rolling_mean_7': df_ts[col].rolling(7).mean().iloc[-1] if len(df_ts) >= 7 else None,
                    'rolling_std_7': df_ts[col].rolling(7).std().iloc[-1] if len(df_ts) >= 7 else None,
                    'pct_change_mean': df_ts[col].pct_change().mean(),
                    'pct_change_std': df_ts[col].pct_change().std()
                }
            except:
                pass

            # Stationarity test (ADF)
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
        try:
            # For OHLCV data, prefer using close price for seasonality
            if close_cols:
                col = close_cols[0]
            else:
                col = ohlc_patterns[0]  # Use first numeric column

            # Calculate mean value by day of week
            day_means = df_ts.groupby(df_ts.index.dayofweek)[col].mean()
            ts_stats['seasonality']['day_of_week'] = {day: mean for day, mean in enumerate(day_means)}

            # Check if there's any monthly seasonality
            if hasattr(df_ts.index, 'month') and len(df_ts) >= 60:  # Need enough data for monthly patterns
                try:
                    month_means = df_ts.groupby(df_ts.index.month)[col].mean()
                    ts_stats['seasonality']['month'] = {month: mean for month, mean in enumerate(month_means, 1)}
                except:
                    pass
        except:
            ts_stats['seasonality']['error'] = 'Seasonality analysis failed'

    return ts_stats

def print_descriptive_stats(desc_stats):
    """Print descriptive statistics in a readable format with columns in row for better space efficiency."""
    print("\n\033[1m\033[94mDescriptive Statistics:\033[0m")

    # Group columns with similar patterns (OHLCV, etc.)
    column_groups = {}
    for col in desc_stats.keys():
        # Try to detect column type using common patterns
        if 'open' in col.lower():
            group = 'price_ohlc'
        elif 'high' in col.lower():
            group = 'price_ohlc'
        elif 'low' in col.lower():
            group = 'price_ohlc'
        elif 'close' in col.lower():
            group = 'price_ohlc'
        elif 'volume' in col.lower():
            group = 'volume'
        elif 'pressure' in col.lower():
            group = 'pressure'
        else:
            group = 'other'

        if group not in column_groups:
            column_groups[group] = []
        column_groups[group].append(col)

    # Print statistics for each group
    for group, columns in column_groups.items():
        if group == 'price_ohlc':
            print(f"\n\033[96mPrice Data (OHLC):\033[0m")
        elif group == 'volume':
            print(f"\n\033[96mVolume Data:\033[0m")
        elif group == 'pressure':
            print(f"\n\033[96mPressure Indicators:\033[0m")
        else:
            print(f"\n\033[96mOther Data:\033[0m")

        # Print all columns in rows for common metrics
        for metric in ['mean', 'median', 'min', 'max', 'std', 'var', '25%', '50%', '75%']:
            values = []
            for col in columns:
                stats = desc_stats[col]
                if 'error' not in stats and metric in stats:
                    val = stats[metric]
                    if isinstance(val, float):
                        values.append(f"{col}: {val:.4f}")
                    else:
                        values.append(f"{col}: {val}")

            if values:
                print(f"  {metric.capitalize()}: {' | '.join(values)}")

        # Print remaining metrics separately for each column
        for col in columns:
            stats = desc_stats[col]
            if 'error' in stats:
                print(f"  {col} Error: {stats['error']}")
            else:
                other_metrics = [k for k in stats.keys() if k not in ['mean', 'median', 'min', 'max', 'std', 'var', '25%', '50%', '75%']]
                if other_metrics:
                    values = []
                    for key in other_metrics:
                        value = stats[key]
                        if isinstance(value, float):
                            values.append(f"{key}: {value:.4f}")
                        else:
                            values.append(f"{key}: {value}")
                    if values:
                        print(f"  {col} other metrics: {' | '.join(values)}")

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print("  • Statistical measures provide insights into data characteristics and quality")
    print("  • High variance may indicate the need for data normalization before modeling")
    print("  • Significant difference between mean and median suggests distribution asymmetry")
    print("  • If IQR (Q3-Q1) is wide, the data has high spread and may contain outliers")
    print("  • Next steps: Check distributions and detect anomalies using --distribution-analysis and --outlier-analysis")

    # Visualization for descriptive stats
    plots_dir = ensure_plots_directory()
    numeric_cols = [col for col, s in desc_stats.items() if 'mean' in s and 'std' in s and 'error' not in s]
    if numeric_cols:
        plt.figure(figsize=(10, 6))
        data = {col: [desc_stats[col]['mean'], desc_stats[col]['std'], desc_stats[col]['min'], desc_stats[col]['max']] for col in numeric_cols}
        df_plot = pd.DataFrame(data, index=['mean', 'std', 'min', 'max']).T
        df_plot.plot(kind='bar', figsize=(12, 6))
        plt.title('Descriptive Stats: Mean, Std, Min, Max')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'descriptive_stats_summary.png')
        plt.savefig(plot_path)
        print(f"\033[96m[INFO]\033[0m Descriptive stats summary plot saved to: {plot_path}")
        plt.close()
        open_last_plot_in_browser(plot_path)
        print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")

def print_distribution_analysis(dist_stats):
    """Print distribution analysis in a readable format."""
    print("\n\033[1m\033[94mDistribution Analysis:\033[0m")

    # Group columns by normality for summary
    normal_cols = []
    skewed_cols = []
    highly_skewed_cols = []
    heavy_tailed_cols = []
    light_tailed_cols = []

    for col, stats in dist_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            skew = stats['skewness']
            kurt = stats['kurtosis']

            # Track for summary
            if stats['is_normal'] == 'Yes':
                normal_cols.append(col)
            if abs(skew) > 1:
                highly_skewed_cols.append((col, skew))
            elif abs(skew) > 0.5:
                skewed_cols.append((col, skew))
            if kurt > 3:
                heavy_tailed_cols.append((col, kurt))
            elif kurt < 3:
                light_tailed_cols.append((col, kurt))

            # Print individual stats in a row
            skew_desc = 'Positive (right-skewed)' if skew > 0 else 'Negative (left-skewed)' if skew < 0 else 'None'
            kurt_desc = 'Heavy-tailed' if kurt > 3 else 'Light-tailed' if kurt < 3 else 'Normal'
            print(f"  Skewness: {skew:.4f} ({skew_desc}) | Kurtosis: {kurt:.4f} ({kurt_desc})")

            if stats['normality_test'] is not None:
                print(f"  Normality test p-value: {stats['normality_test'][1]:.4f} | Distribution appears normal: {stats['is_normal']}")
            else:
                print("  Normality test: Not enough data points")

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print(f"  • Found {len(normal_cols)} columns with normal distribution: {', '.join(normal_cols) if normal_cols else 'none'}")

    if highly_skewed_cols:
        print(f"  • Detected columns with strong skewness (skewness > 1): {', '.join([f'{col} ({skew:.2f})' for col, skew in highly_skewed_cols])}")
        print("  • Recommendation: Consider applying transformations (log, sqrt, Box-Cox) to normalize these variables")

    if skewed_cols:
        print(f"  • Detected columns with moderate skewness (skewness 0.5-1): {', '.join([f'{col} ({skew:.2f})' for col, skew in skewed_cols])}")

    if heavy_tailed_cols:
        print(f"  • Detected columns with heavy tails (kurtosis > 3): {', '.join([f'{col} ({kurt:.2f})' for col, kurt in heavy_tailed_cols])}")
        print("  • Recommendation: Watch for outliers and use robust statistical methods for these variables")

    if light_tailed_cols:
        print(f"  • Detected columns with light tails (kurtosis < 3): {', '.join([f'{col}' for col, _ in light_tailed_cols])}")

    print("  • Non-normal distributions may require special treatment in modeling")
    print("  • Next steps: Run outlier analysis with --outlier-analysis to identify anomalous values")

    # Visualization for distribution analysis
    plots_dir = ensure_plots_directory()
    numeric_cols = [col for col, s in dist_stats.items() if 'skewness' in s and 'error' not in s]
    if numeric_cols:
        plt.figure(figsize=(10, 6))
        skews = [dist_stats[col]['skewness'] for col in numeric_cols]
        kurts = [dist_stats[col]['kurtosis'] for col in numeric_cols]
        sns.barplot(x=numeric_cols, y=skews, color='orange', edgecolor='black')
        plt.xticks(rotation=45)
        plt.ylabel('Skewness')
        plt.title('Skewness of Numeric Columns')
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'distribution_skewness.png')
        plt.savefig(plot_path)
        print(f"\033[96m[INFO]\033[0m Distribution skewness plot saved to: {plot_path}")
        plt.close()
        open_last_plot_in_browser(plot_path)
        print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")

def print_outlier_analysis(outlier_stats):
    """Print outlier analysis in a readable format."""
    print("\n\033[1m\033[94mOutlier Analysis:\033[0m")

    # Track columns with significant outliers for summary
    high_outlier_cols = []
    moderate_outlier_cols = []

    for col, stats in outlier_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            # Print IQR method results
            iqr_pct = stats['iqr_method']['outlier_percentage']
            # Print Z-Score method results
            z_pct = stats['z_score_method']['outlier_percentage']

            # Print results in compact format
            print(f"  IQR Method: Bounds [{stats['iqr_method']['lower_bound']:.4f}, {stats['iqr_method']['upper_bound']:.4f}] | {stats['iqr_method']['outlier_count']} outliers ({iqr_pct}%)")
            print(f"  Z-Score Method (|z| > 3): {stats['z_score_method']['outlier_count']} outliers ({z_pct}%)")

            # Show sample outlier indices only if they exist
            if stats['iqr_method']['outlier_indices']:
                print(f"  Sample outlier indices (IQR): {', '.join(map(str, stats['iqr_method']['outlier_indices']))}")

            # Track for summary
            if max(iqr_pct, z_pct) > 5:  # If more than 5% are outliers
                high_outlier_cols.append((col, max(iqr_pct, z_pct)))
            elif max(iqr_pct, z_pct) > 1:  # If 1-5% are outliers
                moderate_outlier_cols.append((col, max(iqr_pct, z_pct)))

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    if high_outlier_cols:
        print(f"  • Detected {len(high_outlier_cols)} columns with significant outliers (>5%):")
        for col, pct in high_outlier_cols:
            print(f"    - {col}: {pct:.2f}% outliers")
        print("  • Recommendations for handling outliers:")
        print("    1. Investigate outlier sources: measurement errors vs. genuine extreme values")
        print("    2. For error outliers: correct or remove them")
        print("    3. For genuine outliers: apply winsorization, trimming, or robust statistics")
        print("    4. For ML models: use algorithms resistant to outliers (RandomForest, Gradient Boosting)")
    elif moderate_outlier_cols:
        print(f"  • Detected {len(moderate_outlier_cols)} columns with moderate outliers (1-5%):")
        for col, pct in moderate_outlier_cols:
            print(f"    - {col}: {pct:.2f}% outliers")
        print("  • Consider using robust methods for these variables")
    else:
        print("  • No significant outlier presence detected (>1%)")

    print("  • The presence of outliers can significantly impact statistical analyses and modeling")
    print("  • Next steps: Run time series analysis with --time-series-analysis to investigate temporal patterns")

    # Visualization for outlier analysis
    plots_dir = ensure_plots_directory()
    numeric_cols = [col for col, s in outlier_stats.items() if 'iqr_method' in s and 'error' not in s]
    if numeric_cols:
        plt.figure(figsize=(10, 6))
        outlier_pcts = [outlier_stats[col]['iqr_method']['outlier_percentage'] for col in numeric_cols]
        sns.barplot(x=numeric_cols, y=outlier_pcts, color='red', edgecolor='black')
        plt.xticks(rotation=45)
        plt.ylabel('Outlier Percentage (IQR)')
        plt.title('Outlier Percentage by Column (IQR Method)')
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'outlier_percentages.png')
        plt.savefig(plot_path)
        print(f"\033[96m[INFO]\033[0m Outlier percentage plot saved to: {plot_path}")
        plt.close()
        open_last_plot_in_browser(plot_path)
        print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")

def print_time_series_analysis(ts_stats):
    """Print time series analysis in a readable format."""
    print("\n\033[1m\033[94mTime Series Analysis:\033[0m")

    if 'error' in ts_stats:
        print(f"  Error: {ts_stats['error']}")
        return

    # Track information for summary
    has_features = False
    non_stationary_cols = []
    stationary_cols = []
    has_seasonality = False

    # Print derived features
    if 'features' in ts_stats and ts_stats['features']:
        has_features = True
        print("\n\033[96mDerived Features:\033[0m")

        # Group feature stats for more compact display
        for feature, stats in ts_stats['features'].items():
            feature_name = feature.replace('_', ' ').title()
            stats_str = " | ".join([f"{stat.title()}: {value:.4f}" for stat, value in stats.items()])
            print(f"  {feature_name}: {stats_str}")

    # Print stationarity test results
    if 'stationarity' in ts_stats and ts_stats['stationarity']:
        print("\n\033[96mStationarity Tests (ADF):\033[0m")
        for col, result in ts_stats['stationarity'].items():
            if 'error' in result:
                print(f"  {col}: Error: {result['error']}")
            else:
                is_stationary = result['is_stationary']
                status = "Stationary" if is_stationary else "Non-stationary"
                print(f"  {col}: Test statistic: {result['test_statistic']:.4f} | p-value: {result['p_value']:.4f} | Status: {status}")

                # Track for summary
                if is_stationary:
                    stationary_cols.append(col)
                else:
                    non_stationary_cols.append(col)

    # Print seasonality analysis
    if 'seasonality' in ts_stats and ts_stats['seasonality']:
        print("\n\033[96mSeasonality Analysis:\033[0m")
        if 'day_of_week' in ts_stats['seasonality']:
            has_seasonality = True
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_stats = ts_stats['seasonality']['day_of_week']

            if 'error' in dow_stats:
                print(f"  Day of Week: {dow_stats['error']}")
            else:
                # Print all days in one line
                day_values = [f"{day_names[day_num]}: {mean_value:.4f}" for day_num, mean_value in dow_stats.items()]
                print("  Average by Day of Week: " + " | ".join(day_values))

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    if has_features:
        print("  • Successfully derived time series features from price data")

    # Stationarity advice
    if non_stationary_cols:
        print(f"  • Detected non-stationary time series: {', '.join(non_stationary_cols)}")
        print("  • Recommendations for non-stationary series:")
        print("    1. Apply differencing (diff() method) to remove trends")
        print("    2. Consider logarithmic or other transformations for variance stabilization")
        print("    3. For ML models: Add trend features and use relative changes")
        print("    4. Non-stationarity often indicates predictable patterns that can be leveraged")

    if stationary_cols:
        print(f"  • Detected stationary time series: {', '.join(stationary_cols)}")
        print("  • Stationary series are well-suited for ARIMA, GARCH and other statistical methods")

    if has_seasonality:
        print("  • Weekly seasonal patterns detected")
        print("  • Recommendations for working with seasonality:")
        print("    1. Add categorical features (day of week, month, etc.)")
        print("    2. For statistical models: Use seasonal differencing or SARIMA")
        print("    3. For deep learning: Consider architectures with attention mechanisms")
        print("    4. Seasonal patterns can be strong predictors in financial data")

    print("  • Time series properties directly impact forecasting strategy and model selection")
    print("  • Next steps: Perform correlation analysis with --correlation-analysis to identify relationships")

    # Visualization for time series analysis
    plots_dir = ensure_plots_directory()
    if 'features' in ts_stats and ts_stats['features']:
        for feature, stats in ts_stats['features'].items():
            if isinstance(stats, dict) and all(isinstance(v, (int, float)) for v in stats.values()):
                plt.figure(figsize=(8, 4))
                plt.bar(list(stats.keys()), list(stats.values()), color='purple', edgecolor='black')
                plt.title(f"Time Series Feature: {feature}")
                plt.ylabel('Value')
                plt.tight_layout()
                plot_path = os.path.join(plots_dir, f'ts_feature_{feature}.png')
                plt.savefig(plot_path)
                print(f"\033[96m[INFO]\033[0m Time series feature plot saved to: {plot_path}")
                plt.close()
                open_last_plot_in_browser(plot_path)
    print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")
