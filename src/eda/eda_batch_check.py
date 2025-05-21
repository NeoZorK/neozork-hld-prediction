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
    --fix-files                Fix data in original parquet files
    --basic-stats              Show basic statistics for files
    --correlation-analysis     Correlation analysis between numeric features
    --feature-importance       Feature importance analysis

Examples:
    python eda_batch_check.py --nan-check --duplicate-check
    python eda_batch_check.py --data-quality-checks --basic-stats
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

{Fore.YELLOW}Other Flags:{Style.RESET_ALL}
  {Fore.GREEN}--fix-files{Style.RESET_ALL}                Fix data in original parquet files
  {Fore.GREEN}--basic-stats{Style.RESET_ALL}              Show basic statistics for files
  {Fore.GREEN}--correlation-analysis{Style.RESET_ALL}     Correlation analysis between numeric features
  {Fore.GREEN}--feature-importance{Style.RESET_ALL}       Feature importance analysis

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  python eda_batch_check.py --nan-check --duplicate-check
  python eda_batch_check.py --data-quality-checks --basic-stats
  python eda_batch_check.py -dqc --basic-stats
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
    # Other features
    parser.add_argument('--fix-files', action='store_true')
    parser.add_argument('--basic-stats', action='store_true')
    parser.add_argument('--correlation-analysis', action='store_true')
    parser.add_argument('--feature-importance', action='store_true')
    args = parser.parse_args()

    # Check if at least one flag is provided
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data')
    parquet_files = [y for x in os.walk(data_dir) for y in glob.glob(os.path.join(x[0], '*.parquet'))]

    # Check if there are any parquet files in the directory
    with tqdm(total=len(parquet_files), desc="Processing files", position=0, leave=True) as pbar:
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
                args.zero_check or args.negative_check or args.inf_check
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

    # Placeholder for flag-based operations

if __name__ == "__main__":
    main()
