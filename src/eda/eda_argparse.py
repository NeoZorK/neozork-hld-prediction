# src/eda/eda_argparse.py

import argparse

def get_eda_args():
    parser = argparse.ArgumentParser(
        description="""Perform EDA checks on data files and optionally clean the data.

This script performs exploratory data analysis (EDA) on CSV and Parquet files in specified directories.
It checks for missing values, duplicates, data types, and provides statistical summaries.
Optionally, it can run the data cleaner to fix identified issues.

Example usage:
    # Basic EDA check
    python eda_batch_check.py

    # Run EDA check and clean data
    python eda_batch_check.py --clean

    # Specify custom output directory and NaN handling
    python eda_batch_check.py --clean --output-dir data/cleaned --handle-nan ffill
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Run data cleaner after log analysis to fix issues"
    )
    parser.add_argument(
        "--output-dir",
        default="cleaned",
        help="Output directory for cleaned data (default: 'cleaned')"
    )
    parser.add_argument(
        "--csv-delimiter",
        default="\t",
        help="Delimiter for CSV files (default is tab which works for mql5_feed)"
    )
    parser.add_argument(
        "--csv-header",
        default="0",
        help="CSV header row (0 = first row, or 'infer')"
    )
    parser.add_argument(
        "--handle-nan",
        default="ffill",
        choices=['ffill', 'dropna_rows', 'none'],
        help="Strategy for handling NaN values: 'ffill' (forward fill), 'dropna_rows' (remove rows with NaN), 'none' (don't process)"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip asking to verify cleaned files with another EDA check"
    )
    parser.add_argument(
        "--log-file",
        default="logs/eda_batch_check.log",
        help="Log file name for recording the EDA process (will be created in logs directory)"
    )
    parser.add_argument(
        "--target-folders",
        nargs="+",
        default=["data/cache/csv_converted", "data/raw_parquet"],
        help="List of folders to check (default: data/cache/csv_converted data/raw_parquet)"
    )
    return parser.parse_args()