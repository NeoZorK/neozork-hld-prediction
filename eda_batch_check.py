# -*- coding: utf-8 -*-
# eda_batch_check.py

import os
import warnings
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

    Args:
        folder_path (str): Path to the folder.
        extensions (List[str]): List of file extensions to include.

    Returns:
        List[str]: List of found file paths.
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

    Args:
        df (pd.DataFrame): Dataframe to log.
        file_path (str): File path for context.
        logger (logging.Logger): Logger instance.
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

    Args:
        file_path (str): Path to the file.
        logger (logging.Logger): Logger instance.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    file_type = "parquet" if ext == ".parquet" else "csv"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = load_data(file_path, file_type=file_type)
            log_file_info(df, file_path, logger)
    except Exception as e:
        # Only print errors to console, all other info goes to log
        tqdm.write(f"ERROR processing {file_path}: {e}")
        logger.error(f"ERROR processing {file_path}: {e}")

def process_folder(folder_path: str, logger: logging.Logger, progress_bar: tqdm) -> None:
    """
    Process all data files in a folder with progress bar.

    Args:
        folder_path (str): Path to the folder.
        logger (logging.Logger): Logger instance.
        progress_bar (tqdm): Shared tqdm instance.
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
    """
    suppress_warnings()

    target_folders = [
        "data/cache/csv_converted",
        "data/raw_parquet",
        "mql5_feed"
    ]

    logger = setup_logger()
    all_data_files: Dict[str, List[str]] = {}
    total_files = 0

    # Find all files and count total for progress bar
    for folder in target_folders:
        files = find_data_files(folder)
        all_data_files[folder] = files
        total_files += len(files)

    if total_files == 0:
        tqdm.write("No files found for checking in the specified folders.")
        logger.info("No files found for checking.")
        return

    with tqdm(total=total_files, desc="EDA CHECK", unit="file", position=0, leave=True) as progress_bar:
        for folder in target_folders:
            process_folder(folder, logger, progress_bar)

    tqdm.write(f"\nLog file: eda_batch_check.log")
    logger.info("EDA batch check completed.")

if __name__ == "__main__":
    main()