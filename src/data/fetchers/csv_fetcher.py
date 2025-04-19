# src/data/fetchers/csv_fetcher.py

"""
Contains the function to fetch and process data from a CSV file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from ...common import logger # Relative import from parent's sibling


# Definition of the fetch_csv_data function
def fetch_csv_data(filepath: str) -> pd.DataFrame | None:
    """
    Reads historical OHLCV and indicator data from a specified CSV file.
    Performs cleaning: strips column names, handles datetimes, converts numerics, replaces inf.
    """
    logger.print_debug(f"Attempting to read CSV file: {filepath}")
    file_path_obj = Path(filepath)
    if not file_path_obj.is_file():
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None

    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False)
        if df.empty:
            logger.print_warning(f"CSV file is empty: {filepath}")
            return None

        # --- Data Cleaning ---
        original_columns = df.columns.tolist()
        # Clean column names: remove leading/trailing whitespace and trailing commas
        cleaned_columns = [str(col).strip().rstrip(',') for col in original_columns]
        df.columns = cleaned_columns

        # Drop unnamed columns that might appear
        unnamed_cols = [col for col in df.columns if col == '' or 'Unnamed' in col]
        if unnamed_cols:
            logger.print_debug(f"Dropping unnamed/empty columns: {unnamed_cols}")
            df.drop(columns=unnamed_cols, inplace=True, errors='ignore')

        # Parse 'DateTime' column
        if 'DateTime' not in df.columns:
            logger.print_error("Mandatory 'DateTime' column not found in CSV.")
            return None
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
        rows_before_dropna = len(df)
        df.dropna(subset=['DateTime'], inplace=True) # Remove rows with invalid dates
        rows_after_dropna = len(df)
        if rows_before_dropna > rows_after_dropna:
            logger.print_warning(f"Dropped {rows_before_dropna - rows_after_dropna} rows with invalid DateTime format.")
        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with invalid dates.")
            return None
        df.set_index('DateTime', inplace=True)

        # Rename TickVolume to Volume for consistency
        df.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')

        # Convert all columns to numeric where possible, coercing errors
        for col in df.columns:
            # Only attempt conversion if column is not already numeric (or datetime index)
            if col not in df.select_dtypes(include=[np.number]).columns:
                 try:
                     df[col] = pd.to_numeric(df[col], errors='coerce')
                     logger.print_debug(f"Coerced column '{col}' to numeric.")
                 except Exception as e:
                      logger.print_warning(f"Could not coerce column '{col}' to numeric: {e}")


        # Replace infinite values with NaN
        inf_mask = np.isinf(df.select_dtypes(include=[np.number]))
        if inf_mask.any().any():
            logger.print_warning("Replacing infinite values (inf, -inf) with NaN.")
            df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Check for required OHLCV columns after processing
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_error(f"CSV data is missing required columns after processing: {missing_cols}")
            logger.print_error(f"Available columns: {list(df.columns)}")
            return None

        logger.print_info(f"Successfully read and processed {len(df)} rows from {filepath}")
        return df

    except FileNotFoundError: logger.print_error(f"CSV file not found at path: {file_path_obj}"); return None
    except pd.errors.EmptyDataError: logger.print_error(f"CSV file is empty: {filepath}"); return None
    except pd.errors.ParserError as e: logger.print_error(f"Failed to parse CSV file: {filepath} - Error: {e}"); return None
    except KeyError as e: logger.print_error(f"Missing expected column during processing: {e} in file {filepath}"); return None
    # noinspection PyBroadException
    except Exception as e: logger.print_error(f"An unexpected error occurred while processing CSV {filepath}: {type(e).__name__}: {e}"); return None