# src/eda/eda_batch_processor.py

import os
import warnings
from tqdm import tqdm
import logging
from src.eda.eda_file_utils import find_data_files
from src.eda.eda_logging import log_file_info
from src.eda.data_overview import load_data

# This module provides functions to process data files in a folder, perform EDA checks, and log the results.
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

# This function processes all data files in a folder and logs the results with a progress bar.
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