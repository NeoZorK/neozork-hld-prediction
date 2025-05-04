# -*- coding: utf-8 -*-
# eda_batch_check.py

import os
import warnings
import subprocess
import argparse
from typing import List, Dict
from tqdm import tqdm
import logging

from src.eda.data_overview import (
    load_data,
    show_basic_info,
    show_head,
    check_missing_values,
    check_duplicates,
    get_column_types,
    get_nan_columns,
    get_summary
)

def setup_logger(log_file: str = "eda_batch_check.log") -> logging.Logger:
    """
    Set up a logger to write info and errors to a file.
    """
    logger = logging.getLogger("eda_batch_check")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger

def find_data_files(folder_path: str, extensions: List[str] = [".parquet", ".csv"]) -> List[str]:
    """
    Recursively find all files with given extensions in the folder and its subfolders.
    """
    data_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                data_files.append(os.path.join(root, file))
    return data_files

def log_file_info(df, file_path, logger):
    """
    Log detailed information about the dataframe to the logger.
    """
    logger.info(f"CHECKING: {file_path}")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"First 3 rows:\n{df.head(3).to_string()}")
    missing = df.isnull().sum()
    logger.info(f"Missing values:\n{missing[missing > 0]}")
    num_dup = df.duplicated().sum()
    logger.info(f"Number of duplicate rows: {num_dup}")
    logger.info(f"Column types:\n{df.dtypes}")
    nan_cols = df.columns[df.isnull().any()].tolist()
    logger.info(f"Columns with NaN values: {nan_cols}")
    logger.info(f"Statistical summary:\n{df.describe()}")

def suppress_warnings():
    """
    Suppress all warnings from being printed to stderr, to keep tqdm progress bar clear.
    """
    warnings.filterwarnings("ignore")

def check_file(file_path: str, logger: logging.Logger) -> None:
    """
    Perform EDA-check on a single file, log all outputs.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    file_type = "parquet" if ext == ".parquet" else "csv"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = load_data(file_path, file_type=file_type)
            log_file_info(df, file_path, logger)
    except Exception as e:
        tqdm.write(f"ERROR processing {file_path}: {e}")
        logger.error(f"ERROR processing {file_path}: {e}")

def process_folder(folder_path: str, logger: logging.Logger, progress_bar: tqdm) -> None:
    """
    Process all data files in a folder with progress bar.
    """
    logger.info(f"Processing folder: {folder_path}")
    data_files = find_data_files(folder_path)
    logger.info(f"Found {len(data_files)} data files in '{folder_path}'.")
    for file_path in data_files:
        check_file(file_path, logger)
        progress_bar.update(1)

def main():
    """
    Main function to check all data files in specified folders with a single progress bar and per-folder output.
    Suppresses all warnings and errors from libraries to keep tqdm progress bar clean.
    At the end, runs log analysis script and optionally runs data cleaner.
    """
    # Declare global variable at the beginning of the function
    global initial_data_analysis
    initial_data_analysis = None

    parser = argparse.ArgumentParser(
        description="Perform EDA checks on data files and optionally clean the data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--clean", 
        action="store_true",
        help="Run data cleaner after log analysis to fix issues"
    )
    parser.add_argument(
        "--output-dir", 
        default="data/cleaned",
        help="Output directory for cleaned data files"
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
        help="Strategy for handling NaN values"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip asking to verify cleaned files with another EDA check"
    )
    args = parser.parse_args()

    suppress_warnings()

    target_folders = [
        "data/cache/csv_converted",
        "data/raw_parquet",
        "mql5_feed"
    ]

    # Define logger variable in the outer scope first
    logger = None
    
    def run_eda_check(folders_to_check):
        """Inner function to run EDA check on specified folders"""
        nonlocal logger
        
        # Reset if logger already exists
        if logger is not None:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
        
        logger = setup_logger()
        all_data_files: Dict[str, List[str]] = {}
        total_files = 0

        for folder in folders_to_check:
            if not os.path.exists(folder):
                tqdm.write(f"Warning: Folder not found: {folder}")
                continue
            files = find_data_files(folder)
            all_data_files[folder] = files
            total_files += len(files)

        if total_files == 0:
            tqdm.write("No files found for checking in the specified folders.")
            logger.info("No files found for checking.")
            return False

        with tqdm(total=total_files, desc="EDA CHECK", unit="file", position=0, leave=True) as progress_bar:
            for folder in folders_to_check:
                if os.path.exists(folder):
                    process_folder(folder, logger, progress_bar)

        # Clear line to prevent overlap with future output
        print("\033[K", end="\r")
        tqdm.write(f"\nLog file: eda_batch_check.log")
        logger.info("EDA batch check completed.")
        return True

    # Run initial EDA check on original folders
    initial_check_success = run_eda_check(target_folders)
    
    if not initial_check_success:
        return

    # Automatically analyze log after main process
    log_analyze_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "scripts", "log_analysis", "log_analyze.py"
    )
    if os.path.exists(log_analyze_script):
        print("\n--- Running log analysis on initial data ---\n")
        try:
            # Import the module directly instead of using subprocess for better integration
            import importlib.util
            spec = importlib.util.spec_from_file_location("log_analyze", log_analyze_script)
            log_analyze = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(log_analyze)
            
            # Use the global variable if available
            if initial_data_analysis:
                eda_log_report = initial_data_analysis
            
            # Analyze the log file and store the results for later comparison
            initial_log_report = log_analyze.analyze_log("eda_batch_check.log")
            
            # Save the analysis results in a global variable for later comparison
            initial_data_analysis = initial_log_report
        except Exception as e:
            print(f"Log analysis failed: {e}")
    else:
        print("Log analysis script not found.")
    
    # Run data cleaner if requested
    if args.clean:
        data_cleaner_script_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "scripts", "data_processing"
        )
        
        data_cleaner_script = os.path.join(
            data_cleaner_script_dir, "data_cleaner_v2.py"
        )
        
        # Ensure the directory exists
        os.makedirs(data_cleaner_script_dir, exist_ok=True)
        
        if os.path.exists(data_cleaner_script):
            print("\n--- Running data cleaner ---\n")
            try:
                # Build the command with all necessary arguments
                cmd = [
                    "python", data_cleaner_script,
                    "--input-dirs"] + target_folders + [
                    "--output-dir", args.output_dir,
                    "--handle-duplicates", "remove",
                    "--handle-nan", args.handle_nan,
                    "--csv-delimiter", args.csv_delimiter,
                    "--csv-header", args.csv_header,
                    "--log-file", "data_cleaner_run.log"
                ]
                print(f"Running: {' '.join(cmd)}")
                subprocess.run(cmd, check=True)
                print(f"\nCleaned data saved to: {args.output_dir}")
                
                # Ask user if they want to verify cleaned files
                if not args.skip_verification:
                    # Clear any leftovers from progress bar
                    print("\033[K", end="\r")
                    verification = input("\nWould you like to verify the cleaned files with another EDA check? (Y/n): ")
                    if verification.lower() != 'n':
                        print(f"\n--- Running EDA check on cleaned data in '{args.output_dir}' ---\n")
                        # Ensure output directory exists to avoid warning message
                        if os.path.exists(args.output_dir):
                            run_eda_check([args.output_dir])
                            print("\nVerification complete. Check the log file for results.")
                        else:
                            print(f"Output directory {args.output_dir} not found or not created yet. No files to verify.")
                    else:
                        print("\nSkipping verification. You can run verification manually with:")
                        print(f"python eda_batch_check.py # after modifying target_folders in code")
            except Exception as e:
                print(f"Data cleaning failed: {e}")
        else:
            print(f"Data cleaner script not found at: {data_cleaner_script}")
            print("Please create scripts/data_processing/data_cleaner_v2.py first.")

if __name__ == "__main__":
    main()