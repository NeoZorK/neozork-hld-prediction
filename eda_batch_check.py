# -*- coding: utf-8 -*-
# eda_batch_check.py

import os
import warnings
import subprocess
import argparse
from typing import List, Dict, Union
from tqdm import tqdm
import glob
import shutil
import logging
from pathlib import Path
import sys
import time

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

def setup_logger(log_file: str = None) -> logging.Logger:
    """
    Set up a logger to write info and errors to a file in 'logs' directory.
    No console output to keep terminal clean for progress bar.
    
    Args:
        log_file: Path to the log file (default: "logs/eda_batch_check.log")
    
    Returns:
        Logger instance with file handler only
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True, parents=True)
    
    # Set default log file path if not provided
    if log_file is None:
        log_file = logs_dir / "eda_batch_check.log"
    else:
        # Ensure the log file is in the logs directory
        log_path = Path(log_file)
        if not log_path.is_absolute():
            if not str(log_path).startswith("logs/"):
                log_file = logs_dir / log_path.name
    
    logger = logging.getLogger("eda_batch_check")
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()  # Properly close the handler
    
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Add file handler only
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Console handler removed - to keep progress bar visible alone

    logger.propagate = False
    return logger

def sort_files_by_type(base_dir: str, parquet_dir: str, csv_dir: str) -> None:
    """
    Sort files in the base directory into parquet and csv directories.
    """
    # Create directories if they don't exist
    os.makedirs(parquet_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)
    
    # Search for all files in the base directory
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        
        # Process only files, not directories
        if os.path.isfile(file_path):
            # Determine the file type and move it to the appropriate directory
            if file.lower().endswith('.parquet'):
                target_path = os.path.join(parquet_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Moved paquet file: {file} -> {target_path}")
            elif file.lower().endswith('.csv'):
                target_path = os.path.join(csv_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Move CSV File: {file} -> {target_path}")

def find_data_files(folder_path: Union[str, List[str]], extensions: List[str] = [".parquet", ".csv"], exclude_paths: List[str] = None) -> List[str]:
    """
    Find all data files in the specified folder(s) with given extensions.
    """
    data_files = []
    
    # Transform folder_path to a list if it's a string
    if isinstance(folder_path, str):
        folder_path = [folder_path]
    
    # Transform exclude_paths to absolute paths if provided
    exclude_abs_paths = []
    if exclude_paths:
        exclude_abs_paths = [os.path.abspath(p) for p in exclude_paths]
    
    for folder in folder_path:
        if not os.path.exists(folder):
            continue
            
        for root, dirs, files in os.walk(folder):
            # Check if the current directory is in the exclude paths
            current_abs_path = os.path.abspath(root)
            
            if exclude_abs_paths and any(current_abs_path.startswith(p) for p in exclude_abs_paths):
                continue
                
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    data_files.append(file_path)
    
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
    
    try:
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            return
            
        if not os.path.isdir(folder_path):
            logger.error(f"Path is not a directory: {folder_path}")
            return
            
        data_files = find_data_files(folder_path)
        logger.info(f"Found {len(data_files)} data files in '{folder_path}'.")
        
        for file_path in data_files:
            check_file(file_path, logger)
            progress_bar.update(1)
    except Exception as e:
        error_msg = f"Error processing folder {folder_path}: {str(e)}"
        logger.error(error_msg)

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
    args = parser.parse_args()

    suppress_warnings()

    target_folders = args.target_folders

    # Define logger variable in the outer scope first
    logger = None
    
    def run_eda_check(folders_to_check):
        """Inner function to run EDA check on specified folders"""
        nonlocal logger
        
        # Reset if logger already exists
        if logger is not None:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
        
        logger = setup_logger(args.log_file)
        
        all_data_files: Dict[str, List[str]] = {}
        total_files = 0
    
        for folder in folders_to_check:
            if not os.path.exists(folder):
                error_msg = f"Warning: Folder not found: {folder}"
                tqdm.write(error_msg)
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
        log_path = Path(args.log_file)
        if not log_path.is_absolute():
            log_path = Path("logs") / log_path.name if not str(log_path).startswith("logs/") else log_path
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
        # Clear previous line
        print("\033[K", end="\r")
        
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
            initial_log_report = log_analyze.analyze_log(args.log_file)
            
            # Save the analysis results in a global variable for later comparison
            initial_data_analysis = initial_log_report
            
            # Print analysis statistics
            print("\033[K", end="\r")  # Clear line
            tqdm.write("\n=== Log Analysis Summary ===")
            for category, stats in initial_log_report.items():
                tqdm.write(f"{category}: {stats}")
            tqdm.write("==========================\n")
        except Exception as e:
            print("\033[K", end="\r")  # Clear line
            tqdm.write(f"\nLog analysis failed: {e}")
    else:
        tqdm.write("Log analysis script not found.")
    
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
            # Minimal output with progress bar
            try:
                # Ensure the log file goes to logs directory
                logs_dir = Path("logs")
                logs_dir.mkdir(exist_ok=True, parents=True)
                cleaner_log_file = logs_dir / "data_cleaner_run.log"
                
                # Create the output directory if it doesn't exist
                # Use args.output_dir but ensure it's prefixed with "data/" if not already
                if args.output_dir.startswith("data/"):
                    base_output_dir = args.output_dir
                else:
                    base_output_dir = os.path.join("data", args.output_dir)
                raw_parquet_dir = os.path.join(base_output_dir, "raw_parquet")
                csv_converted_dir = os.path.join(base_output_dir, "cache", "csv_converted")
                
                # Create directories for cleaned data
                try:
                    os.makedirs(raw_parquet_dir, exist_ok=True)
                    os.makedirs(csv_converted_dir, exist_ok=True)
                except Exception as e:
                    print(f"Error creating directories: {str(e)}")
                
                # Find all files in the specified folders
                all_files = []
                for folder in target_folders:
                    if os.path.exists(folder):
                        folder_files = find_data_files(folder)
                        all_files.extend(folder_files)
                
                # Group files by type
                parquet_files = [f for f in all_files if f.lower().endswith('.parquet')]
                csv_files = [f for f in all_files if f.lower().endswith('.csv')]
                
                # Files have been collected
                
                # Run data cleaner
                cmds = []
                
                # Create logs directory if it doesn't exist
                os.makedirs("logs", exist_ok=True)
                
                # File to log data cleaner run
                with open(cleaner_log_file, "w", encoding="utf-8") as f:
                    f.write("# Data cleaner log file\n")
                
                # Create output directories if they don't exist
                os.makedirs(raw_parquet_dir, exist_ok=True)
                os.makedirs(csv_converted_dir, exist_ok=True)
                        
                # Get unique directories for parquet and csv files
                parquet_dirs = set(os.path.dirname(f) for f in parquet_files)
                csv_dirs = set(os.path.dirname(f) for f in csv_files)
                
                # Process directories
                if parquet_files:
                    for parquet_dir in parquet_dirs:
                        if not parquet_dir:  # Skip empty directories
                            continue
                        
                        # Create command for parquet files
                        cmd_parquet = [
                            "python", data_cleaner_script,
                            "-i", parquet_dir,
                            "-o", base_output_dir,
                            "--handle-duplicates", "remove",
                            "--handle-nan", args.handle_nan,
                            "--csv-delimiter", args.csv_delimiter,
                            "--csv-header", args.csv_header,
                            "--log-file", str(cleaner_log_file),
                            "--verbose"
                        ]
                        cmds.append(('parquet', cmd_parquet))
                                        
                # Check if any CSV files were found
                if csv_files:
                    for csv_dir in csv_dirs:
                        if not csv_dir:  # Skip empty directories
                            continue
                        
                        # Count CSV files in this directory
                        dir_csv_files = [f for f in csv_files if os.path.dirname(f) == csv_dir]
                        
                        # Prepare for command generation
                        
                        cmd_csv = [
                            "python", data_cleaner_script,
                            "-i", csv_dir,
                            "-o", base_output_dir,
                            "--handle-duplicates", "remove",
                            "--handle-nan", args.handle_nan,
                            "--csv-delimiter", args.csv_delimiter,
                            "--csv-header", args.csv_header,
                            "--log-file", str(cleaner_log_file),
                            "--verbose"
                        ]
                        cmds.append(('csv', cmd_csv))
                
                if not cmds:
                    tqdm.write("Не найдено CSV или Parquet файлов для обработки.")
                    return
                # Process data cleaning without progress bar 
                all_success = True
                total_processed_files = 0
                
                for file_type, cmd in cmds:
                    # Run subprocess with minimal output
                    print(f"Processing {file_type} files...")
                    
                    # Save the command to cleaner_log_file
                    with open(cleaner_log_file, "a", encoding="utf-8") as f:
                        f.write(f"\nRunning command: {' '.join(cmd)}\n")
                    
                    # Debug log files with prefix debug_cleaner_parquet_ have been removed by request
                    
                    # Run the command
                    start_time = time.time()
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    elapsed_time = time.time() - start_time
                    
                    # Analyze the output
                    stdout_lines = result.stdout.splitlines()
                    stderr_lines = result.stderr.splitlines()
                    
                    # Search for specific messages in the output
                    processed_count = 0
                    processed_msg = None
                    for line in stdout_lines:
                        if "Processing file:" in line:
                            processed_count += 1
                        if "Successfully processed" in line:
                            processed_msg = line.strip()
                    
                    # Debug logging to debug_cleaner files has been removed by request
                    
                    # Check if process succeeded
                    if result.returncode != 0:
                        # Only show error message without full command details
                        print(f"Data cleaning for {file_type} files failed with exit code {result.returncode}")
                        
                        # Save error output to log file
                        with open(cleaner_log_file, "a", encoding="utf-8") as f:
                            f.write(f"\nError output:\n{result.stderr}\n")
                        
                        # Show error message
                        if result.stderr:
                            print(f"Error: {result.stderr.splitlines()[0]}")
                            # Show first 3 lines of stderr
                            print(f"Command: {' '.join(cmd)}")
                
                        print(f"Check log file: {cleaner_log_file}")
                        all_success = False
                    else:
                        # Save success output to log file
                        with open(cleaner_log_file, "a", encoding="utf-8") as f:
                            f.write(f"\nOutput:\n{result.stdout}\n")
                
                        processed_files = result.stdout.count("Processing file:")
                        total_processed_files += processed_files
                        print(f"Successfully processed {processed_files} {file_type} files")
                
                # Show minimal success message
                if all_success:
                    print(f"Data cleaning completed. Files saved to: {base_output_dir}")
                else:
                    print(f"Data cleaning completed with some errors. Check log file: {cleaner_log_file}")
                
                # Display progress bar right before verification prompt
                with tqdm(total=1, desc="CLEANING DATA", unit="process", position=0, leave=True) as progress_bar:
                    progress_bar.update(1)

                # Ask user if they want to verify cleaned files
                if not args.skip_verification:
                    # Clear any leftovers from progress bar
                    print("\033[K", end="\r")
                    verification = input("\nVerify cleaned files with another EDA check? (Y/n): ")
                    if verification.lower() != 'n':
                        # Ensure output directory exists to avoid warning message
                        # Since files are saved to base_output_dir, we need to check that path
                        if os.path.exists(base_output_dir):
                            run_eda_check([base_output_dir])

                            # Analyze data_cleaner_run.log
                            cleaner_log_file = Path("logs") / "data_cleaner_run.log"
                            try:
                                if os.path.exists(cleaner_log_file):
                                    # Analyze the cleaning log with minimal output
                                    with tqdm(total=1, desc="ANALYZING CLEANING RESULTS", unit="log", position=0, leave=True) as progress_bar:
                                        with open(cleaner_log_file, "r", encoding="utf-8") as f:
                                            log_content = f.read()

                                        # Extract statistics from log
                                        total_files = log_content.count("Processing file:")
                                        files_with_nan = log_content.count("NaN values detected")
                                        files_with_duplicates = log_content.count("Duplicates removed")

                                        # Calculate total rows removed
                                        total_rows_removed = 0
                                        for line in log_content.split("\n"):
                                            if "Duplicates removed:" in line:
                                                try:
                                                    removed = int(line.split(":")[1].split(".")[0].strip())
                                                    total_rows_removed += removed
                                                except (ValueError, IndexError):
                                                    continue

                                        # Get final summary
                                        final_summary = None
                                        for line in reversed(log_content.split("\n")):
                                            if "Successfully processed/saved:" in line:
                                                final_summary = line
                                                break

                                        progress_bar.update(1)

                                        # Display summary directly on the screen
                                        tqdm.write("\n" + "-" * 50)
                                        tqdm.write("Data Cleaning Results:")
                                        tqdm.write(f"Total files processed: {total_files}")
                                        tqdm.write(f"Files with NaN values: {files_with_nan}")
                                        tqdm.write(f"Files with duplicates: {files_with_duplicates}")
                                        tqdm.write(f"Total rows removed: {total_rows_removed}")
                                        if final_summary:
                                            tqdm.write(f"\nFinal Summary: {final_summary}")
                                        tqdm.write("-" * 50)
                                else:
                                    tqdm.write(f"Data cleaning log file not found at: {cleaner_log_file}")
                            except Exception as e:
                                tqdm.write(f"Error analyzing cleaning log: {e}")
                        else:
                            tqdm.write(f"Output directory {args.output_dir} not found. No files to verify.")
                    else:
                        tqdm.write(f"\nSkipping verification. Run manually with: python eda_batch_check.py --target-folders {base_output_dir}")
            except Exception as e:
                print(f"Error during data cleaning: {str(e).split(':')[0]}")
                print("Check logs directory for details.")
                
                # Try to provide guidance about the issue
                if "unrecognized arguments" in str(e):
                    print("\nNOTE: There may be a mismatch between the arguments expected by data_cleaner_v2.py")
                    print("and those being passed. Check the script documentation for correct usage.")
        else:
            print(f"Data cleaner script not found at: {data_cleaner_script}")
            print("Please create scripts/data_processing/data_cleaner_v2.py first.")

if __name__ == "__main__":
    main()