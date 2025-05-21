"""
EDA Batch Check Script

Usage:
    python eda_batch_check.py [--data-quality-checks] [--fix-files] [--basic-stats] [--correlation-analysis] [--feature-importance]

Flags:
    --data-quality-checks    Run data quality checks (missing, duplicates, unique values)
    --fix-files              Fix data in original .parquet files
    --basic-stats            Compute basic statistics
    --correlation-analysis   Compute correlations between numerical features
    --feature-importance     Perform feature importance analysis

Examples:
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
    parser = argparse.ArgumentParser(description="Batch EDA and Data Quality Checks on Parquet Files")
    parser.add_argument('-dqc', '--data-quality-checks', action='store_true', help='Perform data quality checks (NaN, duplicates, unique values, etc.)')
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
        for idx, file in enumerate(parquet_files, 1):
            info = file_info.get_file_info(file)
            if args.data_quality_checks:
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
                    data_quality.data_quality_checks(df, nan_summary_all, Fore, Style)
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
    # NaN summary after all files
    if args.data_quality_checks:
        data_quality.print_nan_summary(nan_summary_all, Fore, Style)

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
