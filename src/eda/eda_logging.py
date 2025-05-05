# src/eda/eda_logging.py

import logging
import warnings
from pathlib import Path

# This module provides utility functions for logging and suppressing warnings.
def setup_logger(log_file: str = None) -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True, parents=True)
    if log_file is None:
        log_file = logs_dir / "eda_batch_check.log"
    else:
        log_path = Path(log_file)
        if not log_path.is_absolute():
            if not str(log_path).startswith("logs/"):
                log_file = logs_dir / log_path.name
    logger = logging.getLogger("eda_batch_check")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger

# This function suppresses all warnings.
def suppress_warnings():
    warnings.filterwarnings("ignore")

# This function logs the information of a DataFrame, including its shape, columns, first 3 rows, missing values, duplicate rows, column types, and statistical summary.
def log_file_info(df, file_path, logger):
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