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
from src.eda.eda_data_cleaner import run_data_cleaner

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
        run_data_cleaner(args, target_folders)

if __name__ == "__main__":
    main()