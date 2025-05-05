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

# This script is designed to perform exploratory data analysis (EDA) on CSV and Parquet files
from src.eda.eda_file_utils import find_data_files, sort_files_by_type
from src.eda.eda_logging import setup_logger, suppress_warnings, log_file_info
from src.eda.eda_batch_processor import check_file, process_folder
from src.eda.eda_file_utils import find_data_files, sort_files_by_type
from src.eda.eda_log_analysis import analyze_log
from src.eda.eda_argparse import get_eda_args

def main():
    """
    Main function to check all data files in specified folders with a single progress bar and per-folder output.
    Suppresses all warnings and errors from libraries to keep tqdm progress bar clean.
    At the end, runs log analysis script and optionally runs data cleaner.
    """
    # Declare global variable at the beginning of the function
    global initial_data_analysis
    initial_data_analysis = None

    args = get_eda_args()

    suppress_warnings()

    # Truncate the log file at the start of each run
    with open(args.log_file, "w", encoding="utf-8") as f:
        f.write("")

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

    # Analyze the log file and store the results for later comparison
    initial_log_report = analyze_log(args.log_file)
    if initial_log_report:
        tqdm.write("\n=== Log Analysis Summary ===")
        for category, value in initial_log_report.items():
            tqdm.write(f"{category}: {value}")
        tqdm.write("==========================\n")

    
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
                
                # Make sure we include both data/raw_parquet and data/cache/csv_converted
                # This ensures we process all 63 files (19 from raw_parquet + 44 from csv_converted)
                required_folders = ["data/raw_parquet", "data/cache/csv_converted"]
                for folder in required_folders:
                    if folder not in target_folders and os.path.exists(folder):
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
                        
                # Collect all unique directories containing data files
                all_dirs = set()
                
                # Add directories containing parquet files
                if parquet_files:
                    parquet_dirs = set(os.path.dirname(f) for f in parquet_files)
                    all_dirs.update([d for d in parquet_dirs if d])  # Skip empty strings
                
                # Add directories containing CSV files
                if csv_files:
                    csv_dirs = set(os.path.dirname(f) for f in csv_files)
                    all_dirs.update([d for d in csv_dirs if d])  # Skip empty strings
                
                # Make sure both required directories are included
                if "data/raw_parquet" not in all_dirs and os.path.exists("data/raw_parquet"):
                    all_dirs.add("data/raw_parquet")
                    
                if "data/cache/csv_converted" not in all_dirs and os.path.exists("data/cache/csv_converted"):
                    all_dirs.add("data/cache/csv_converted")
                
                # Convert set to list
                all_dirs_list = list(all_dirs)
                
                if all_dirs_list:
                    # Create a single command for all directories
                    cmd = [
                        "python", data_cleaner_script,
                        "-i"
                    ]
                    
                    # Add all directories to the command
                    cmd.extend(all_dirs_list)
                    
                    # Add the rest of the arguments
                    cmd.extend([
                        "-o", base_output_dir,
                        "--handle-duplicates", "remove",
                        "--handle-nan", args.handle_nan,
                        "--csv-delimiter", args.csv_delimiter,
                        "--csv-header", args.csv_header,
                        "--log-file", str(cleaner_log_file),
                        "--verbose"
                    ])
                    
                    # Add the command to the list
                    cmds.append(('all', cmd))
                
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
                            # Clear the EDA log file before verification run
                            with open(args.log_file, "w", encoding="utf-8") as f:
                                f.write("")  # Truncate the log file

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
                                        
                                        # Process log to extract file-specific information
                                        tqdm.write("\nDetailed Changes Summary:")
                                        
                                        # Extract and organize file changes
                                        file_changes = {}
                                        current_file = None
                                        log_lines = log_content.split("\n")
                                        
                                        for i, line in enumerate(log_lines):
                                            # Identify the file being processed
                                            if "Processing file:" in line:
                                                file_path = line.split("Processing file:")[1].strip()
                                                current_file = os.path.basename(file_path)
                                                file_changes[current_file] = {
                                                    "original_size": None,
                                                    "duplicates_removed": 0,
                                                    "nan_values": 0,
                                                    "nan_strategy": "none",
                                                    "final_size": None,
                                                    "output_path": None
                                                }
                                            
                                            # Skip if no current file being processed
                                            if not current_file:
                                                continue
                                                
                                            # Extract original size
                                            if "Original size:" in line and current_file in file_changes:
                                                try:
                                                    size_str = line.split("Original size:")[1].strip()
                                                    file_changes[current_file]["original_size"] = size_str
                                                except (IndexError, ValueError):
                                                    pass
                                                    
                                            # Extract duplicates info
                                            if "Duplicates removed:" in line and current_file in file_changes:
                                                try:
                                                    duplicates_str = line.split("Duplicates removed:")[1].split(".")[0].strip()
                                                    file_changes[current_file]["duplicates_removed"] = int(duplicates_str)
                                                except (IndexError, ValueError):
                                                    pass
                                                    
                                            # Extract NaN values info
                                            if "NaN values detected:" in line and current_file in file_changes:
                                                try:
                                                    nan_str = line.split("NaN values detected:")[1].strip()
                                                    file_changes[current_file]["nan_values"] = int(nan_str)
                                                except (IndexError, ValueError):
                                                    pass
                                                    
                                            # Extract NaN strategy
                                            if "Applied NaN strategy:" in line and current_file in file_changes:
                                                try:
                                                    strategy = line.split("Applied NaN strategy:")[1].split(".")[0].strip()
                                                    file_changes[current_file]["nan_strategy"] = strategy.strip("'")
                                                except (IndexError, ValueError):
                                                    pass
                                                    
                                            # Extract final size after NaN handling
                                            if "Size after NaN handling:" in line and current_file in file_changes:
                                                try:
                                                    size_str = line.split("Size after NaN handling:")[1].strip()
                                                    file_changes[current_file]["final_size"] = size_str
                                                except (IndexError, ValueError):
                                                    pass
                                                    
                                            # Extract output path
                                            if "Saving cleaned file to:" in line and current_file in file_changes:
                                                try:
                                                    output_path = line.split("Saving cleaned file to:")[1].strip()
                                                    file_changes[current_file]["output_path"] = output_path
                                                except (IndexError, ValueError):
                                                    pass
                                        
                                        # Display detailed file changes
                                        files_with_changes = []
                                        files_just_copied = []
                                        
                                        for filename, changes in file_changes.items():
                                            # If file had duplicates removed or NaN values fixed
                                            if changes["duplicates_removed"] > 0 or changes["nan_values"] > 0:
                                                files_with_changes.append(filename)
                                                tqdm.write(f"\n► File: {filename}")
                                                if changes["original_size"]:
                                                    tqdm.write(f"  - Original size: {changes['original_size']}")
                                                if changes["duplicates_removed"] > 0:
                                                    tqdm.write(f"  - Duplicates removed: {changes['duplicates_removed']}")
                                                if changes["nan_values"] > 0:
                                                    tqdm.write(f"  - NaN values fixed: {changes['nan_values']} using strategy '{changes['nan_strategy']}'")
                                                if changes["final_size"]:
                                                    tqdm.write(f"  - Final size: {changes['final_size']}")
                                                if changes["output_path"]:
                                                    output_dir = os.path.dirname(changes["output_path"])
                                                    tqdm.write(f"  - Saved to: {output_dir}")
                                            else:
                                                files_just_copied.append(filename)
                                        
                                        # Show summary counts of different file types
                                        tqdm.write(f"\nSummary of changes:")
                                        tqdm.write(f"  - Files with changes (duplicates/NaN fixed): {len(files_with_changes)}")
                                        tqdm.write(f"  - Files copied unchanged: {len(files_just_copied)}")
                                        
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