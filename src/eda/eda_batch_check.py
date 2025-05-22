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

    # Combine analysis with fixing
    python eda_batch_check.py --data-quality-checks --fix-files --fix-all
"""
import argparse
from tqdm import tqdm
import os
import glob
import sys
import colorama
from colorama import Fore, Style

# Initialize colorama for colored output
colorama.init(autoreset=True)

# Add the parent directory to the system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import necessary modules
from src.eda import file_info, folder_stats, data_quality, fix_files, basic_stats, correlation_analysis, feature_importance


def print_nan_check(df, nan_summary):
    # Deprecated: moved to data_quality.py
    pass


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
  {Fore.GREEN}--distribution-analysis{Style.RESET_ALL}    Analyze distributions (skewness, kurtosis)
  {Fore.GREEN}--outlier-analysis{Style.RESET_ALL}         Detect outliers using IQR and Z-score methods
  {Fore.GREEN}--time-series-analysis{Style.RESET_ALL}     Basic time series analysis (trends, seasonality)
  {Fore.GREEN}--all-stats{Style.RESET_ALL}                Run all statistical analyses
  {Fore.GREEN}--correlation-analysis{Style.RESET_ALL}     Correlation analysis between numeric features
  {Fore.GREEN}--feature-importance{Style.RESET_ALL}       Feature importance analysis

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
    args = parser.parse_args()

    # Check if at least one flag is provided
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data')
    parquet_files = [y for x in os.walk(data_dir) for y in glob.glob(os.path.join(x[0], '*.parquet'))]

    # Check if there are any parquet files in the directory
    with tqdm(total=len(parquet_files), desc="Processing files", position=0, leave=True, ncols=100, bar_format='{desc} [{n_fmt}/{total_fmt}] {bar} {percentage:3.0f}%') as pbar:
        nan_summary_all = []
        dupe_summary_all = []
        gap_summary_all = []
        zero_summary_all = []
        negative_summary_all = []
        inf_summary_all = []
        for idx, file in enumerate(parquet_files, 1):
            info = file_info.get_file_info(file)
            if (
                args.data_quality_checks or args.nan_check or args.duplicate_check or args.gap_check or
                args.zero_check or args.negative_check or args.inf_check or
                args.descriptive_stats or args.distribution_analysis or args.outlier_analysis or
                args.time_series_analysis or args.all_stats or args.basic_stats
            ):
                if 'error' in info:
                    print(f"\n{Fore.CYAN}[{idx}] File: {info.get('file_path')}{Style.RESET_ALL}")
                    print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {info['error']}")
                    pbar.update(1)
                    continue
                df = None
                try:
                    import pandas as pd
                    df = pd.read_parquet(file)
                except Exception as e:
                    print(f"\n{Fore.CYAN}[{idx}] File: {info.get('file_path')}{Style.RESET_ALL}")
                    print(f"  {Fore.RED} Error reading file for checking NaN:{Style.RESET_ALL} {e}")
                if df is not None:
                    print(f"\n{Fore.CYAN}[{idx}] File: {info.get('file_path')}{Style.RESET_ALL}")
                    # Individual checks
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
                        basic_stats_result = basic_stats.compute_basic_stats(df)
                        for col, stats in basic_stats_result.items():
                            print(f"  {Fore.CYAN}{col}:{Style.RESET_ALL}")
                            for stat, val in stats.items():
                                if isinstance(val, float):
                                    print(f"    {stat}: {val:.4f}")
                                else:
                                    print(f"    {stat}: {val}")

                    if args.all_stats or args.descriptive_stats:
                        desc_stats_result = basic_stats.descriptive_stats(df)
                        basic_stats.print_descriptive_stats(desc_stats_result)

                    if args.all_stats or args.distribution_analysis:
                        dist_analysis_result = basic_stats.distribution_analysis(df)
                        basic_stats.print_distribution_analysis(dist_analysis_result)

                    if args.all_stats or args.outlier_analysis:
                        outlier_analysis_result = basic_stats.outlier_analysis(df)
                        basic_stats.print_outlier_analysis(outlier_analysis_result)

                    if args.all_stats or args.time_series_analysis:
                        ts_analysis_result = basic_stats.time_series_analysis(df)
                        basic_stats.print_time_series_analysis(ts_analysis_result)

                pbar.update(1)
                continue
            print(f"\n{Fore.CYAN}[{idx}] File: {info.get('file_path')}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Name:{Style.RESET_ALL} {info.get('file_name')}")
            print(f"  {Fore.YELLOW}Size:{Style.RESET_ALL} {info.get('file_size_mb')} MB")
            if 'error' in info:
                print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {info['error']}")
                pbar.update(1)
                continue
            print(f"  {Fore.YELLOW}Rows:{Style.RESET_ALL} {info.get('n_rows')}, {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('n_cols')}")
            print(f"  {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('columns')}")
            dtypes_dict = info.get('dtypes')
            if dtypes_dict:
                print(f"  {Fore.YELLOW}Dtypes:{Style.RESET_ALL}")
                max_col_len = max(len(str(col)) for col in dtypes_dict.keys()) if dtypes_dict else 0
                for col, dtype in dtypes_dict.items():
                    print(f"    {col.ljust(max_col_len)} : {dtype}")
            print(f"  {Fore.MAGENTA}DateTime/Timestamp fields (schema):{Style.RESET_ALL} {info.get('datetime_or_timestamp_fields')}")
            try:
                import pandas as pd
                df = pd.read_parquet(file)
                print(f"  {Fore.GREEN}First 5 rows:{Style.RESET_ALL}\n", df.head(5).to_string())
                print(f"  {Fore.GREEN}First 25 rows:{Style.RESET_ALL}\n", df.head(25).to_string())
                print(f"  {Fore.GREEN}Last 5 rows:{Style.RESET_ALL}\n", df.tail(5).to_string())
            except Exception as e:
                print(f"  {Fore.RED}Error reading rows:{Style.RESET_ALL} {e}")
            pbar.update(1)
    # Print summaries
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
        with tqdm(total=len(parquet_files), desc="Fixing files", position=0, leave=True, ncols=100, bar_format='{desc} [{n_fmt}/{total_fmt}] {bar} {percentage:3.0f}%') as pbar:
            fixed_count = 0
            total_count = 0

            for file in parquet_files:
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
                        fixed_count += 1
                    total_count += 1
                except Exception as e:
                    print(f"\n{Fore.RED}Error fixing file {file}: {str(e)}{Style.RESET_ALL}")

                pbar.update(1)

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
