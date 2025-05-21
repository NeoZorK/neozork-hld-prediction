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

colorama.init(autoreset=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.eda import file_info, folder_stats, data_quality, fix_files, basic_stats, correlation_analysis, feature_importance

def main():
    parser = argparse.ArgumentParser(description="Batch EDA and Data Quality Checks on Parquet Files")
    parser.add_argument('--data-quality-checks', action='store_true')
    parser.add_argument('--fix-files', action='store_true')
    parser.add_argument('--basic-stats', action='store_true')
    parser.add_argument('--correlation-analysis', action='store_true')
    parser.add_argument('--feature-importance', action='store_true')
    args = parser.parse_args()

    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data')
    parquet_files = [y for x in os.walk(data_dir) for y in glob.glob(os.path.join(x[0], '*.parquet'))]

    for idx, file in enumerate(tqdm(parquet_files, desc="Processing files", total=len(parquet_files), position=0, leave=True), 1):
        info = file_info.get_file_info(file)
        print(f"\n{Fore.CYAN}[{idx}] File: {info.get('file_path')}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Name:{Style.RESET_ALL} {info.get('file_name')}")
        print(f"  {Fore.YELLOW}Size:{Style.RESET_ALL} {info.get('file_size_mb')} MB")
        if 'error' in info:
            print(f"  {Fore.RED}Error reading file:{Style.RESET_ALL} {info['error']}")
            continue
        print(f"  {Fore.YELLOW}Rows:{Style.RESET_ALL} {info.get('n_rows')}, {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('n_cols')}")
        print(f"  {Fore.YELLOW}Columns:{Style.RESET_ALL} {info.get('columns')}")
        print(f"  {Fore.YELLOW}Dtypes:{Style.RESET_ALL} {info.get('dtypes')}")
        print(f"  {Fore.MAGENTA}DateTime/Timestamp fields (schema):{Style.RESET_ALL} {info.get('datetime_or_timestamp_fields')}")
        try:
            import pandas as pd
            df = pd.read_parquet(file)
            print(f"  {Fore.GREEN}First 5 rows:{Style.RESET_ALL}\n", df.head(5).to_string())
            print(f"  {Fore.GREEN}First 100 rows:{Style.RESET_ALL}\n", df.head(100).to_string())
            print(f"  {Fore.GREEN}Last 5 rows:{Style.RESET_ALL}\n", df.tail(5).to_string())
        except Exception as e:
            print(f"  {Fore.RED}Error reading rows:{Style.RESET_ALL} {e}")

    print("\n" + Fore.BLUE + Style.BRIGHT + "Folder statistics:" + Style.RESET_ALL)
    shown_folders = set()
    for root, dirs, _ in os.walk(data_dir):
        for d in dirs:
            folder_path = os.path.join(root, d)
            if folder_path in shown_folders:
                continue
            shown_folders.add(folder_path)
            stats = folder_stats.get_folder_stats(folder_path)
            print(f"  {Fore.CYAN}Folder:{Style.RESET_ALL} {stats['folder']}")
            print(f"    {Fore.YELLOW}Total size:{Style.RESET_ALL} {stats['total_size_mb']} MB")
            print(f"    {Fore.YELLOW}File count:{Style.RESET_ALL} {stats['file_count']}")

    # Placeholder for flag-based operations

if __name__ == "__main__":
    main()
