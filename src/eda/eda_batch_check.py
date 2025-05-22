"""
Batch EDA Batch Check Script

Usage:
    python eda_batch_check.py [flags]

Flags:
    --nan-check                Check for missing values (NaN) in columns
    --duplicate-check          Find fully duplicated rows and duplicated values in string columns
    --gap-check                Find gaps in time series (abnormally large intervals in datetime columns)
    --zero-check               Find zero values in numeric columns (with anomaly heuristics)
    --negative-check           Find negative values in OHLCV and datetime columns
    --inf-check                Find +inf and -inf values in numeric columns
    --data-quality-checks      Run all data quality checks (NaN, duplicates, gaps, zeros, negatives, inf)

    --fix-nan                  Fix NaN values in columns
    --fix-duplicates           Fix fully duplicated rows
    --fix-gaps                 Fix gaps in time series
    --fix-zeros                Fix zero values in numeric columns
    --fix-negatives            Fix negative values in OHLCV columns
    --fix-infs                 Fix infinity values in numeric columns
    --fix-all                  Fix all detected problems
    --fix-files                General flag for fixing (must be used with specific fix flags)
    --restore-backups          Restore original files from .bak backups

    --basic-stats              Show basic statistics for files
    --descriptive-stats        Detailed descriptive statistics for numeric columns
    --distribution-analysis    Analyze distributions of numeric columns (skewness, kurtosis)
    --outlier-analysis         Detect outliers in numeric columns using IQR and Z-score methods
    --time-series-analysis     Basic time series analysis (trends, seasonality, stationarity)
    --all-stats                Run all statistical analyses
    --correlation-analysis     Correlation analysis between numeric features
    --feature-importance       Feature importance analysis

    --clean-stats-logs         Remove all statistics log files
    --clean-reports            Remove all HTML report directories for all analyses

Examples:
    # Check data quality issues
    python eda_batch_check.py --nan-check --duplicate-check
    python eda_batch_check.py --data-quality-checks

    # Fix specific issues
    python eda_batch_check.py --fix-files --fix-nan --fix-duplicates
    python eda_batch_check.py --fix-files --fix-zeros --fix-negatives

    # Fix all detected issues
    python eda_batch_check.py --fix-files --fix-all

    # Restore original files from backups
    python eda_batch_check.py --restore-backups

    # Run statistical analyses
    python eda_batch_check.py --descriptive-stats
    python eda_batch_check.py --all-stats

    # Clean statistics logs and reports
    python eda_batch_check.py --clean-stats-logs
    python eda_batch_check.py --clean-reports

    # Combine analysis with fixing
    python eda_batch_check.py --data-quality-checks --fix-files --fix-all
"""
import argparse
import os
import glob
import sys
import colorama
from colorama import Fore, Style
import json
import datetime
from tqdm import tqdm  # Import tqdm for progress bars

# Initialize colorama for colored output
colorama.init(autoreset=True)

# Add the parent directory to the system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import necessary modules
from src.eda import file_info, folder_stats, data_quality, fix_files, basic_stats, correlation_analysis, feature_importance, stats_logger


def print_nan_check(df, nan_summary):
    # Deprecated: moved to data_quality.py
    pass


# Statistics collection for global summary
class StatsCollector:
    def __init__(self):
        self.descriptive_summary = {
            'files_analyzed': 0,
            'total_columns': 0,
            'high_variance_cols': [],
            'skewed_cols': []
        }
        self.distribution_summary = {
            'normal_cols': [],
            'highly_skewed_cols': [],
            'heavy_tailed_cols': []
        }
        self.outlier_summary = {
            'high_outlier_cols': [],  # Columns with >5% outliers
            'moderate_outlier_cols': []  # Columns with 1-5% outliers
        }
        self.time_series_summary = {
            'stationary_cols': [],
            'non_stationary_cols': [],
            'has_seasonality': 0,
            'files_with_datetime': 0
        }

    def update_descriptive_stats(self, file_path, desc_stats):
        self.descriptive_summary['files_analyzed'] += 1
        self.descriptive_summary['total_columns'] += len(desc_stats)

        # Identify high variance columns
        for col, stats in desc_stats.items():
            if 'error' not in stats and 'std' in stats and 'mean' in stats and stats['mean'] != 0:
                # Calculate coefficient of variation
                cv = abs(stats['std'] / stats['mean']) if stats['mean'] != 0 else 0
                if cv > 1.0:  # High variance threshold
                    self.descriptive_summary['high_variance_cols'].append((file_path, col, cv))

    def update_distribution_stats(self, file_path, dist_stats):
        for col, stats in dist_stats.items():
            if 'error' not in stats:
                if stats['is_normal'] == 'Yes':
                    self.distribution_summary['normal_cols'].append((file_path, col))

                skew = stats['skewness']
                kurt = stats['kurtosis']

                if abs(skew) > 1:
                    self.distribution_summary['highly_skewed_cols'].append((file_path, col, skew))

                if kurt > 3:
                    self.distribution_summary['heavy_tailed_cols'].append((file_path, col, kurt))

    def update_outlier_stats(self, file_path, outlier_stats):
        for col, stats in outlier_stats.items():
            if 'error' not in stats:
                iqr_pct = stats['iqr_method']['outlier_percentage']
                z_pct = stats['z_score_method']['outlier_percentage']
                max_pct = max(iqr_pct, z_pct)

                if max_pct > 5:
                    self.outlier_summary['high_outlier_cols'].append((file_path, col, max_pct))
                elif max_pct > 1:
                    self.outlier_summary['moderate_outlier_cols'].append((file_path, col, max_pct))

    def update_time_series_stats(self, file_path, ts_stats):
        if 'error' in ts_stats:
            return

        self.time_series_summary['files_with_datetime'] += 1

        if 'stationarity' in ts_stats:
            for col, result in ts_stats['stationarity'].items():
                if 'error' not in result:
                    if result['is_stationary']:
                        self.time_series_summary['stationary_cols'].append((file_path, col))
                    else:
                        self.time_series_summary['non_stationary_cols'].append((file_path, col))

        if 'seasonality' in ts_stats and 'day_of_week' in ts_stats['seasonality'] and 'error' not in ts_stats['seasonality']['day_of_week']:
            self.time_series_summary['has_seasonality'] += 1

    def print_global_summary(self, args):
        print("\n" + "="*80)
        print(f"{Fore.BLUE + Style.BRIGHT}GLOBAL STATISTICAL ANALYSIS SUMMARY{Style.RESET_ALL}")
        print("="*80)

        print(f"\n{Fore.CYAN}Overall Statistics:{Style.RESET_ALL}")
        print(f"  • Files analyzed: {self.descriptive_summary['files_analyzed']}")
        print(f"  • Total columns examined: {self.descriptive_summary['total_columns']}")

        if args.descriptive_stats or args.all_stats:
            print(f"\n{Fore.CYAN}Descriptive Statistics Summary:{Style.RESET_ALL}")
            if self.descriptive_summary['high_variance_cols']:
                print(f"  • Found {len(self.descriptive_summary['high_variance_cols'])} columns with high variance (CV > 1):")
                for file_path, col, cv in self.descriptive_summary['high_variance_cols'][:10]:  # Show top 10
                    print(f"    - {os.path.basename(file_path)}: {col} (CV={cv:.2f})")
                if len(self.descriptive_summary['high_variance_cols']) > 10:
                    print(f"    - ... and {len(self.descriptive_summary['high_variance_cols']) - 10} more columns")
                print("  • Recommendation: Consider normalizing high-variance columns before modeling")
            else:
                print("  • No columns with notably high variance were detected")

        if args.distribution_analysis or args.all_stats:
            print(f"\n{Fore.CYAN}Distribution Analysis Summary:{Style.RESET_ALL}")
            normal_pct = len(self.distribution_summary['normal_cols']) / self.descriptive_summary['total_columns'] * 100 if self.descriptive_summary['total_columns'] > 0 else 0
            print(f"  • {len(self.distribution_summary['normal_cols'])} columns follow normal distribution ({normal_pct:.1f}% of total)")
            print(f"  • {len(self.distribution_summary['highly_skewed_cols'])} columns have strong skewness (skewness > 1)")
            print(f"  • {len(self.distribution_summary['heavy_tailed_cols'])} columns have heavy tails (kurtosis > 3)")
            print("  • Recommendations:")
            print("    - Apply log, sqrt, or Box-Cox transformations to normalize skewed data")
            print("    - Watch for outliers in heavy-tailed distributions")

        if args.outlier_analysis or args.all_stats:
            print(f"\n{Fore.CYAN}Outlier Analysis Summary:{Style.RESET_ALL}")
            print(f"  • {len(self.outlier_summary['high_outlier_cols'])} columns have significant outliers (>5%)")
            print(f"  • {len(self.outlier_summary['moderate_outlier_cols'])} columns have moderate outliers (1-5%)")
            if self.outlier_summary['high_outlier_cols']:
                print("  • Top columns with the most outliers:")
                sorted_outliers = sorted(self.outlier_summary['high_outlier_cols'], key=lambda x: x[2], reverse=True)
                for file_path, col, pct in sorted_outliers[:5]:  # Show top 5
                    print(f"    - {os.path.basename(file_path)}: {col} ({pct:.1f}% outliers)")

        if args.time_series_analysis or args.all_stats:
            print(f"\n{Fore.CYAN}Time Series Analysis Summary:{Style.RESET_ALL}")
            print(f"  • {self.time_series_summary['files_with_datetime']} files contained datetime columns")
            print(f"  • {len(self.time_series_summary['stationary_cols'])} stationary time series detected")
            print(f"  • {len(self.time_series_summary['non_stationary_cols'])} non-stationary time series detected")
            print(f"  • {self.time_series_summary['has_seasonality']} files showed clear weekly seasonality")
            print("  • Recommendations for time series modeling:")
            if self.time_series_summary['non_stationary_cols']:
                print("    - Apply differencing to non-stationary series before modeling")
            if self.time_series_summary['has_seasonality'] > 0:
                print("    - Include day-of-week features in your models to capture seasonality")

        print("\n" + "="*80)
        print(f"{Fore.BLUE + Style.BRIGHT}KEY FINDINGS AND RECOMMENDATIONS{Style.RESET_ALL}")
        print("="*80)
        print("1. Data Quality:")
        if self.outlier_summary['high_outlier_cols']:
            print("   - Address outliers in the data, particularly in price and volume columns")

        print("2. Data Preparation:")
        if self.distribution_summary['highly_skewed_cols']:
            print("   - Apply appropriate transformations to normalize skewed distributions")
        if self.descriptive_summary['high_variance_cols']:
            print("   - Consider standardizing high-variance features")

        print("3. Modeling Strategy:")
        if self.time_series_summary['non_stationary_cols']:
            print("   - Use differencing for non-stationary time series")
        if self.time_series_summary['has_seasonality'] > 0:
            print("   - Incorporate seasonality features (day of week, month) in your models")

        print("4. Next Steps:")
        print("   - Run correlation analysis (--correlation-analysis) to identify relationships")
        print("   - Perform feature importance analysis (--feature-importance) to identify key predictors")
        print("   - Consider developing specialized features based on domain knowledge")


# Main function to handle command line arguments and execute the appropriate functions
def main():
    """Main function to handle command line arguments and execute the appropriate functions."""
    # Colorful help message
    help_header = f"""
{Fore.CYAN + Style.BRIGHT}Batch EDA and Data Quality Checks on Parquet Files{Style.RESET_ALL}

{Fore.YELLOW}Usage:{Style.RESET_ALL}
  python eda_batch_check.py [flags]

{Fore.YELLOW}Data Quality Flags:{Style.RESET_ALL}
  {Fore.GREEN}--nan-check{Style.RESET_ALL}                Check for missing values (NaN) in columns
  {Fore.GREEN}--duplicate-check{Style.RESET_ALL}          Find fully duplicated rows and duplicated values in string columns
  {Fore.GREEN}--gap-check{Style.RESET_ALL}                Find gaps in time series (abnormally large intervals in datetime columns)
  {Fore.GREEN}--zero-check{Style.RESET_ALL}               Find zero values in numeric columns (with anomaly heuristics)
  {Fore.GREEN}--negative-check{Style.RESET_ALL}           Find negative values in OHLCV and datetime columns
  {Fore.GREEN}--inf-check{Style.RESET_ALL}                Find +inf and -inf values in numeric columns
  {Fore.GREEN}--data-quality-checks, -dqc{Style.RESET_ALL} Run all data quality checks (NaN, duplicates, gaps, zeros, negatives, inf)

{Fore.YELLOW}Fix Flags:{Style.RESET_ALL}
  {Fore.GREEN}--fix-nan{Style.RESET_ALL}                  Fix NaN values in columns
  {Fore.GREEN}--fix-duplicates{Style.RESET_ALL}           Fix fully duplicated rows
  {Fore.GREEN}--fix-gaps{Style.RESET_ALL}                 Fix gaps in time series
  {Fore.GREEN}--fix-zeros{Style.RESET_ALL}                Fix zero values in numeric columns
  {Fore.GREEN}--fix-negatives{Style.RESET_ALL}            Fix negative values in OHLCV columns
  {Fore.GREEN}--fix-infs{Style.RESET_ALL}                 Fix infinity values in numeric columns
  {Fore.GREEN}--fix-all{Style.RESET_ALL}                  Fix all detected problems
  {Fore.GREEN}--fix-files{Style.RESET_ALL}                General flag for fixing (must be used with specific fix flags)
  {Fore.GREEN}--restore-backups{Style.RESET_ALL}          Restore original files from .bak backups

{Fore.YELLOW}Statistical Analysis Flags:{Style.RESET_ALL}
  {Fore.GREEN}--basic-stats{Style.RESET_ALL}              Show basic statistics for files
  {Fore.GREEN}--descriptive-stats{Style.RESET_ALL}        Detailed descriptive statistics for numeric columns
  {Fore.GREEN}--distribution-analysis{Style.RESET_ALL}    Analyze distributions of numeric columns (skewness, kurtosis)
  {Fore.GREEN}--outlier-analysis{Style.RESET_ALL}         Detect outliers in numeric columns using IQR and Z-score methods
  {Fore.GREEN}--time-series-analysis{Style.RESET_ALL}     Basic time series analysis (trends, seasonality, stationarity)
  {Fore.GREEN}--all-stats{Style.RESET_ALL}                Run all statistical analyses
  {Fore.GREEN}--correlation-analysis{Style.RESET_ALL}     Correlation analysis between numeric features
  {Fore.GREEN}--feature-importance{Style.RESET_ALL}       Feature importance analysis
  {Fore.GREEN}--clean-stats-logs{Style.RESET_ALL}         Remove all statistics log files
  {Fore.GREEN}--clean-reports{Style.RESET_ALL}            Remove all HTML report directories for all analyses

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  # Check data quality issues
  python eda_batch_check.py --nan-check --duplicate-check
  python eda_batch_check.py --data-quality-checks
  
  # Fix specific issues
  python eda_batch_check.py --fix-files --fix-nan --fix-duplicates
  python eda_batch_check.py --fix-files --fix-zeros --fix-negatives
  
  # Fix all detected issues
  python eda_batch_check.py --fix-files --fix-all
  
  # Restore original files from backups
  python eda_batch_check.py --restore-backups
  
  # Run statistical analyses
  python eda_batch_check.py --descriptive-stats
  python eda_batch_check.py --all-stats
  
  # Clean statistics logs and reports
  python eda_batch_check.py --clean-stats-logs
  python eda_batch_check.py --clean-reports
  
  # Combine analysis with fixing
  python eda_batch_check.py --data-quality-checks --fix-files --fix-all
"""
    parser = argparse.ArgumentParser(
        description=help_header,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True
    )
    # Individual checks
    parser.add_argument('--nan-check', action='store_true', help='Check for missing values (NaN) in columns')
    parser.add_argument('--duplicate-check', action='store_true', help='Find fully duplicated rows and duplicated values in string columns')
    parser.add_argument('--gap-check', action='store_true', help='Find gaps in time series (abnormally large intervals in datetime columns)')
    parser.add_argument('--zero-check', action='store_true', help='Find zero values in numeric columns (with anomaly heuristics)')
    parser.add_argument('--negative-check', action='store_true', help='Find negative values in OHLCV and datetime columns')
    parser.add_argument('--inf-check', action='store_true', help='Find +inf and -inf values in numeric columns')
    # Grouped data quality checks (with short flag)
    parser.add_argument('--data-quality-checks', '-dqc', action='store_true', help='Run all data quality checks (NaN, duplicates, gaps, zeros, negatives, inf)')
    # Fix flags
    parser.add_argument('--fix-nan', action='store_true', help='Fix NaN values in columns')
    parser.add_argument('--fix-duplicates', action='store_true', help='Fix fully duplicated rows')
    parser.add_argument('--fix-gaps', action='store_true', help='Fix gaps in time series')
    parser.add_argument('--fix-zeros', action='store_true', help='Fix zero values in numeric columns')
    parser.add_argument('--fix-negatives', action='store_true', help='Fix negative values in OHLCV columns')
    parser.add_argument('--fix-infs', action='store_true', help='Fix infinity values in numeric columns')
    parser.add_argument('--fix-all', action='store_true', help='Fix all detected problems')
    parser.add_argument('--fix-files', action='store_true', help='General flag for fixing (must be used with specific fix flags)')
    parser.add_argument('--restore-backups', action='store_true', help='Restore original files from .bak backups')
    # Statistical analysis flags
    parser.add_argument('--basic-stats', action='store_true', help='Show basic statistics for files')
    parser.add_argument('--descriptive-stats', action='store_true', help='Detailed descriptive statistics for numeric columns')
    parser.add_argument('--distribution-analysis', action='store_true', help='Analyze distributions of numeric columns (skewness, kurtosis)')
    parser.add_argument('--outlier-analysis', action='store_true', help='Detect outliers in numeric columns using IQR and Z-score methods')
    parser.add_argument('--time-series-analysis', action='store_true', help='Basic time series analysis (trends, seasonality, stationarity)')
    parser.add_argument('--all-stats', action='store_true', help='Run all statistical analyses')
    parser.add_argument('--correlation-analysis', action='store_true', help='Correlation analysis between numeric features')
    parser.add_argument('--feature-importance', action='store_true', help='Feature importance analysis')
    parser.add_argument('--clean-stats-logs', action='store_true', help='Remove all statistics log files')
    parser.add_argument('--clean-reports', action='store_true', help='Remove all HTML report directories for all analyses')
    args = parser.parse_args()

    # Handle the clean logs request if specified
    if args.clean_stats_logs:
        count = stats_logger.clean_stats_logs()
        print(f"{Fore.GREEN}Cleaned {count} statistics log files{Style.RESET_ALL}")
        if not any(getattr(args, arg) for arg in vars(args) if arg != 'clean_stats_logs' and arg != 'clean_reports'):
            return  # Exit if no other flags are specified (except possibly clean_reports)

    # Handle the clean reports request if specified
    if args.clean_reports:
        from src.eda.html_report_generator import clean_all_reports
        success, message = clean_all_reports()
        if success:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        if not any(getattr(args, arg) for arg in vars(args) if arg != 'clean_reports' and arg != 'clean_stats_logs'):
            return  # Exit if no other flags are specified (except possibly clean_stats_logs)

    # Check if at least one flag is provided
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data')
    parquet_files = [y for x in os.walk(data_dir) for y in glob.glob(os.path.join(x[0], '*.parquet'))]

    # Create lists to store summary data
    nan_summary_all = []
    dupe_summary_all = []
    gap_summary_all = []
    zero_summary_all = []
    negative_summary_all = []
    inf_summary_all = []

    # Lists to store results for logging
    basic_stats_results = []
    desc_stats_results = []
    dist_analysis_results = []
    outlier_analysis_results = []
    ts_analysis_results = []
    processed_file_paths = []

    # Initialize stats collector for global summaries
    stats_collector = StatsCollector()

    # Process each file
    total_files = len(parquet_files)
    print(f"{Fore.CYAN}Processing {total_files} files...{Style.RESET_ALL}")

    for idx, file in enumerate(tqdm(parquet_files, desc="Processing files"), 1):  # Add progress bar
        info = file_info.get_file_info(file)

        # Data quality or statistical analysis modes
        if (
            args.data_quality_checks or args.nan_check or args.duplicate_check or args.gap_check or
            args.zero_check or args.negative_check or args.inf_check or
            args.descriptive_stats or args.distribution_analysis or args.outlier_analysis or
            args.time_series_analysis or args.all_stats or args.basic_stats
        ):
            if 'error' in info:
                print(f"\n\n{Fore.CYAN}[{idx}/{total_files}] File: {info.get('file_path')}{Style.RESET_ALL}")
                print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {info['error']}")
                continue

            # Read the DataFrame
            df = None
            try:
                import pandas as pd
                df = pd.read_parquet(file)
            except Exception as e:
                print(f"\n\n{Fore.CYAN}[{idx}/{total_files}] File: {info.get('file_path')}{Style.RESET_ALL}")
                print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {e}")
                continue

            if df is not None:
                # Track this file for logging
                processed_file_paths.append(file)

                # Print file header with extra newlines for better separation
                print(f"\n\n{Fore.CYAN}[{idx}/{total_files}] File: {info.get('file_path')}{Style.RESET_ALL}")

                # Data quality checks
                if args.data_quality_checks or args.nan_check:
                    data_quality.nan_check(df, nan_summary_all, Fore, Style)
                if args.data_quality_checks or args.duplicate_check:
                    data_quality.duplicate_check(df, dupe_summary_all, Fore, Style)
                if args.data_quality_checks or args.gap_check:
                    data_quality.gap_check(df, gap_summary_all, Fore, Style, schema_datetime_fields=info.get('datetime_or_timestamp_fields'), file_name=info.get('file_path'))
                if args.data_quality_checks or args.zero_check:
                    data_quality.zero_check(df, zero_summary_all, Fore, Style, file_name=info.get('file_path'))
                if args.data_quality_checks or args.negative_check:
                    data_quality.negative_check(df, negative_summary_all, Fore, Style, file_name=info.get('file_path'))
                if args.data_quality_checks or args.inf_check:
                    data_quality.inf_check(df, inf_summary_all, Fore, Style, file_name=info.get('file_path'))

                # Statistical analysis
                if args.all_stats or args.basic_stats:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}Basic Statistics for {info.get('file_path')}:{Style.RESET_ALL}")
                    # Add progress bar for column processing
                    columns = df.columns
                    with tqdm(total=len(columns), desc=f"Basic stats analysis", leave=False) as pbar:
                        basic_stats_result = basic_stats.compute_basic_stats(df)
                        pbar.update(len(columns))  # Update progress bar after computation

                    basic_stats_results.append(basic_stats_result)

                    # Group columns by type (similar to print_descriptive_stats)
                    column_groups = {}
                    for col in basic_stats_result.keys():
                        # Group by OHLCV pattern
                        if 'open' in col.lower() or 'high' in col.lower() or 'low' in col.lower() or 'close' in col.lower():
                            group = 'price_ohlc'
                        elif 'volume' in col.lower():
                            group = 'volume'
                        else:
                            group = 'other'

                        if group not in column_groups:
                            column_groups[group] = []
                        column_groups[group].append(col)

                    # Print each group
                    for group, columns in column_groups.items():
                        if group == 'price_ohlc':
                            print(f"\n\033[96mPrice Data (OHLC):\033[0m")
                        elif group == 'volume':
                            print(f"\n\033[96mVolume Data:\033[0m")
                        else:
                            print(f"\n\033[96mOther Data:\033[0m")

                        # Print common metrics in rows for each column group
                        metrics_to_show = ['mean', 'median', 'std', 'min', 'max', 'missing']
                        for metric in metrics_to_show:
                            values = []
                            for col in columns:
                                stats = basic_stats_result[col]
                                if metric in stats:
                                    val = stats[metric]
                                    if isinstance(val, float):
                                        values.append(f"{col}: {val:.4f}")
                                    else:
                                        values.append(f"{col}: {val}")

                            if values:
                                print(f"  {metric.capitalize()}: {' | '.join(values)}")
                        print()  # Extra line for readability

                    # Print basic stats summary
                    basic_stats.print_basic_stats_summary(basic_stats_result)

                # Run more detailed statistical analyses
                if args.all_stats or args.descriptive_stats:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}Descriptive Statistics for {info.get('file_path')}:{Style.RESET_ALL}")
                    columns = df.select_dtypes(include=['number']).columns
                    with tqdm(total=len(columns), desc=f"Descriptive stats analysis", leave=False) as pbar:
                        desc_stats_result = basic_stats.descriptive_stats(df)
                        pbar.update(len(columns))  # Update progress bar after computation

                    desc_stats_results.append(desc_stats_result)
                    basic_stats.print_descriptive_stats(desc_stats_result)
                    # Update global stats
                    stats_collector.update_descriptive_stats(file, desc_stats_result)

                if args.all_stats or args.distribution_analysis:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}Distribution Analysis for {info.get('file_path')}:{Style.RESET_ALL}")
                    columns = df.select_dtypes(include=['number']).columns
                    with tqdm(total=len(columns), desc=f"Distribution analysis", leave=False) as pbar:
                        dist_analysis_result = basic_stats.distribution_analysis(df)
                        pbar.update(len(columns))  # Update progress bar after computation

                    dist_analysis_results.append(dist_analysis_result)
                    basic_stats.print_distribution_analysis(dist_analysis_result)
                    # Update global stats
                    stats_collector.update_distribution_stats(file, dist_analysis_result)

                if args.all_stats or args.outlier_analysis:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}Outlier Analysis for {info.get('file_path')}:{Style.RESET_ALL}")
                    columns = df.select_dtypes(include=['number']).columns
                    with tqdm(total=len(columns), desc=f"Outlier detection", leave=False) as pbar:
                        outlier_analysis_result = basic_stats.outlier_analysis(df)
                        pbar.update(len(columns))  # Update progress bar after computation

                    outlier_analysis_results.append(outlier_analysis_result)
                    basic_stats.print_outlier_analysis(outlier_analysis_result)
                    # Update global stats
                    stats_collector.update_outlier_stats(file, outlier_analysis_result)

                if args.all_stats or args.time_series_analysis:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}Time Series Analysis for {info.get('file_path')}:{Style.RESET_ALL}")
                    with tqdm(total=1, desc=f"Time series analysis", leave=False) as pbar:
                        ts_analysis_result = basic_stats.time_series_analysis(df)
                        pbar.update(1)  # Update progress bar after computation

                    ts_analysis_results.append(ts_analysis_result)
                    basic_stats.print_time_series_analysis(ts_analysis_result)
                    # Update global stats
                    stats_collector.update_time_series_stats(file, ts_analysis_result)

                # Add a file-specific summary at the end of each file analysis
                if (args.all_stats or args.descriptive_stats or args.distribution_analysis or
                    args.outlier_analysis or args.time_series_analysis):
                    print(f"\n{Fore.YELLOW + Style.BRIGHT}File-Specific Summary for {os.path.basename(file)}:{Style.RESET_ALL}")
                    print("  • This file contains data with the following characteristics:")
                    # Print key metrics
                    try:
                        print(f"    - {df.shape[0]} rows and {df.shape[1]} columns")
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        print(f"    - {len(numeric_cols)} numeric columns that can be used for modeling")
                        # Check for datetime columns
                        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
                        if datetime_cols:
                            print(f"    - Contains datetime column(s): {', '.join(datetime_cols)}")
                            # Show date range if available
                            for dt_col in datetime_cols:
                                try:
                                    min_date = df[dt_col].min()
                                    max_date = df[dt_col].max()
                                    print(f"    - Date range: {min_date} to {max_date}")
                                except:
                                    pass
                    except Exception as e:
                        print(f"    - Error generating file summary: {e}")

            # Add extra space after each file
            print("\n")
            continue

        # Default mode - just print file info
        print(f"\n\n{Fore.CYAN}[{idx}/{total_files}] File: {info.get('file_path')}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Name:{Style.RESET_ALL} {info.get('file_name')}")
        print(f"  {Fore.YELLOW}Size:{Style.RESET_ALL} {info.get('file_size_mb')} MB")
        if 'error' in info:
            print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {info['error']}")
            continue
        print(f"  {Fore.YELLOW}Rows:{Style.RESET_ALL} {info.get('n_rows')}, {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('n_cols')}")
        print(f"  {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('columns')}")

        # Print dtype information
        dtypes_dict = info.get('dtypes')
        if dtypes_dict:
            print(f"  {Fore.YELLOW}Dtypes:{Style.RESET_ALL}")
            max_col_len = max(len(str(col)) for col in dtypes_dict.keys()) if dtypes_dict else 0
            for col, dtype in dtypes_dict.items():
                print(f"    {col.ljust(max_col_len)} : {dtype}")
        print(f"  {Fore.MAGENTA}DateTime/Timestamp fields (schema):{Style.RESET_ALL} {info.get('datetime_or_timestamp_fields')}")

        # Print sample rows
        try:
            import pandas as pd
            df = pd.read_parquet(file)
            print(f"  {Fore.GREEN}First 5 rows:{Style.RESET_ALL}\n", df.head(5).to_string())
            print(f"  {Fore.GREEN}Last 5 rows:{Style.RESET_ALL}\n", df.tail(5).to_string())
        except Exception as e:
            print(f"  {Fore.RED}Error reading rows:{Style.RESET_ALL} {e}")

        # Add extra space
        print("\n")

    # Print summaries for quality checks
    print("\n\n")  # Extra space
    if args.data_quality_checks or args.nan_check:
        data_quality.print_nan_summary(nan_summary_all, Fore, Style)
    if args.data_quality_checks or args.duplicate_check:
        data_quality.print_duplicate_summary(dupe_summary_all, Fore, Style)
    if args.data_quality_checks or args.gap_check:
        data_quality.print_gap_summary(gap_summary_all, Fore, Style)
    if args.data_quality_checks or args.zero_check:
        data_quality.print_zero_summary(zero_summary_all, Fore, Style)
    if args.data_quality_checks or args.negative_check:
        data_quality.print_negative_summary(negative_summary_all, Fore, Style)
    if args.data_quality_checks or args.inf_check:
        data_quality.print_inf_summary(inf_summary_all, Fore, Style)

    # Print global statistical summary if any statistical analysis was performed
    if (args.all_stats or args.descriptive_stats or args.distribution_analysis or
        args.outlier_analysis or args.time_series_analysis):
        stats_collector.print_global_summary(args)

        # Log global statistics summary
        global_log_path = stats_logger.log_global_stats_summary(stats_collector)
        print(f"\n{Fore.GREEN}Global statistics summary logged to: {global_log_path}{Style.RESET_ALL}")

    # Log individual statistics if they were computed
    if processed_file_paths:
        if args.basic_stats or args.all_stats:
            log_path = stats_logger.log_basic_stats(basic_stats_results, processed_file_paths)
            print(f"{Fore.GREEN}Basic statistics logged to: {log_path}{Style.RESET_ALL}")

        if args.descriptive_stats or args.all_stats:
            log_path = stats_logger.log_descriptive_stats(desc_stats_results, processed_file_paths)
            print(f"{Fore.GREEN}Descriptive statistics logged to: {log_path}{Style.RESET_ALL}")

        if args.distribution_analysis or args.all_stats:
            log_path = stats_logger.log_distribution_analysis(dist_analysis_results, processed_file_paths)
            print(f"{Fore.GREEN}Distribution analysis logged to: {log_path}{Style.RESET_ALL}")

        if args.outlier_analysis or args.all_stats:
            log_path = stats_logger.log_outlier_analysis(outlier_analysis_results, processed_file_paths)
            print(f"{Fore.GREEN}Outlier analysis logged to: {log_path}{Style.RESET_ALL}")

        if args.time_series_analysis or args.all_stats:
            log_path = stats_logger.log_time_series_analysis(ts_analysis_results, processed_file_paths)
            print(f"{Fore.GREEN}Time series analysis logged to: {log_path}{Style.RESET_ALL}")

    # Print folder statistics
    print("\n" + Fore.BLUE + Style.BRIGHT + "Folder statistics:" + Style.RESET_ALL)

    # Collect folder statistics
    shown_folders = set()

    # Get folder statistics for each directory
    for root, dirs, _ in os.walk(data_dir):
        for d in dirs:
            folder_path = os.path.join(root, d)

            # Skip cache folders
            if folder_path.endswith('/cache') or folder_path.endswith('\\cache'):
                continue

            # Skip already shown folders
            if folder_path in shown_folders:
                continue

            # Check if the folder is already shown
            shown_folders.add(folder_path)
            stats = folder_stats.get_folder_stats(folder_path)
            print(f"  {Fore.CYAN}Folder:{Style.RESET_ALL} {stats['folder']}")
            print(f"    {Fore.YELLOW}Total size:{Style.RESET_ALL} {stats['total_size_mb']} MB")
            print(f"    {Fore.YELLOW}File count:{Style.RESET_ALL} {stats['file_count']}")

    # Handle fix operations if requested
    if args.fix_files and (args.fix_nan or args.fix_duplicates or args.fix_gaps or
                          args.fix_zeros or args.fix_negatives or args.fix_infs or args.fix_all):
        print(f"\n{Fore.BLUE + Style.BRIGHT}Starting data fix operations:{Style.RESET_ALL}")

        # Check which fix operations to perform
        fix_nan = args.fix_nan or args.fix_all
        fix_duplicates = args.fix_duplicates or args.fix_all
        fix_gaps = args.fix_gaps or args.fix_all
        fix_zeros = args.fix_zeros or args.fix_all
        fix_negatives = args.fix_negatives or args.fix_all
        fix_infs = args.fix_infs or args.fix_all

        # Process each parquet file
        fixed_count = 0
        total_count = 0
        print(f"{Fore.CYAN}Fixing files...{Style.RESET_ALL}")

        for file_idx, file in enumerate(tqdm(parquet_files, desc="Fixing files"), 1):  # Add progress bar
            try:
                was_fixed = fix_files.fix_file(
                    file,
                    fix_nan_flag=fix_nan,
                    fix_duplicates_flag=fix_duplicates,
                    fix_gaps_flag=fix_gaps,
                    fix_zeros_flag=fix_zeros,
                    fix_negatives_flag=fix_negatives,
                    fix_infs_flag=fix_infs
                )
                if was_fixed:
                    print(f"  {Fore.GREEN}Fixed:{Style.RESET_ALL} {file} ({file_idx}/{len(parquet_files)})")
                    fixed_count += 1
                else:
                    print(f"  {Fore.YELLOW}No fixes needed:{Style.RESET_ALL} {file} ({file_idx}/{len(parquet_files)})")
                total_count += 1
            except Exception as e:
                print(f"  {Fore.RED}Error fixing file {file}: {str(e)}{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}Fixed {fixed_count} out of {total_count} files{Style.RESET_ALL}")

        if fixed_count > 0:
            print(f"\n{Fore.YELLOW}Note: Original files were backed up with .bak extension{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}To restore them, use: mv file.parquet.bak file.parquet{Style.RESET_ALL}")

    # Restore backups if requested
    if args.restore_backups:
        print(f"\n{Fore.BLUE + Style.BRIGHT}Restoring original files from backups:{Style.RESET_ALL}")
        restored_count = 0
        for file in parquet_files:
            backup_file = f"{file}.bak"
            if os.path.exists(backup_file):
                try:
                    os.rename(backup_file, file)
                    restored_count += 1
                    print(f"{Fore.GREEN}Restored:{Style.RESET_ALL} {file}")
                except Exception as e:
                    print(f"{Fore.RED}Error restoring file {file}: {str(e)}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Restored {restored_count} files{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
