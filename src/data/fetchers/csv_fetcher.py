# src/data/fetchers/csv_fetcher.py # Re-verified Cleaning Sequence

"""
Contains the function to fetch and process data from a CSV file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from ...common import logger # Relative import from parent's sibling
import traceback # Import traceback for detailed error logging


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
        # 1. Read the CSV file using pandas
        df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False)
        if df.empty:
            logger.print_warning(f"CSV file is empty: {filepath}")
            return None # Return None if DataFrame is empty after read

        # 2. Clean column names
        original_columns = df.columns.tolist()
        cleaned_columns = [str(col).strip().rstrip(',') for col in original_columns]
        df.columns = cleaned_columns
        unnamed_cols = [col for col in df.columns if col == '' or 'Unnamed' in col]
        if unnamed_cols:
            logger.print_debug(f"Dropping unnamed/empty columns: {unnamed_cols}")
            df.drop(columns=unnamed_cols, inplace=True, errors='ignore')

        # 3. Parse and set DateTime index
        if 'DateTime' not in df.columns:
            logger.print_error("Mandatory 'DateTime' column not found in CSV.")
            return None
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
        rows_before_dropna_dt = len(df)
        df.dropna(subset=['DateTime'], inplace=True)
        rows_after_dropna_dt = len(df)
        if rows_before_dropna_dt > rows_after_dropna_dt:
            logger.print_warning(f"Dropped {rows_before_dropna_dt - rows_after_dropna_dt} rows with invalid DateTime format.")
        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with invalid dates.")
            return None
        df.set_index('DateTime', inplace=True)

        # 4. Rename TickVolume to Volume for consistency
        df.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')

        # 5. Convert potentially numeric columns to numeric (coerce errors)
        potential_numeric_cols = df.columns
        for col in potential_numeric_cols:
            if col not in df.select_dtypes(include=[np.number]).columns:
                 try:
                     df[col] = pd.to_numeric(df[col], errors='coerce')
                 except Exception as e:
                      logger.print_warning(f"Could not coerce column '{col}' to numeric during general conversion: {e}")

        # 6. Replace infinite values with NaN in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            inf_mask = np.isinf(df[numeric_cols])
            if inf_mask.any().any():
                logger.print_warning("Replacing infinite values (inf, -inf) with NaN.")
                df.replace([np.inf, -np.inf], np.nan, inplace=True)
        else:
            logger.print_warning("No numeric columns found after coercion to replace inf values.")


        # 7. Check for required OHLCV columns AFTER cleaning and type coercion
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.print_error(f"CSV data is missing required columns after processing: {missing_cols}")
            logger.print_error(f"Available columns: {list(df.columns)}")
            return None

        # 8. Drop rows if *any* of the required OHLCV columns have NaN AFTER conversion
        initial_rows_after_dt = len(df)
        df.dropna(subset=required_cols, how='any', inplace=True)
        rows_dropped_nan = initial_rows_after_dt - len(df)
        if rows_dropped_nan > 0:
            logger.print_debug(f"Dropped {rows_dropped_nan} rows with NaN in required OHLCV columns after conversion/inf handling.")

        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with NaN in required columns.")
            return None

        logger.print_info(f"Successfully read and processed {len(df)} rows from {filepath}")
        return df

    except FileNotFoundError: logger.print_error(f"CSV file not found at path: {file_path_obj}"); return None
    except pd.errors.EmptyDataError: logger.print_error(f"CSV file is empty: {filepath}"); return None
    except pd.errors.ParserError as e: logger.print_error(f"Failed to parse CSV file: {filepath} - Error: {e}"); return None
    except KeyError as e: logger.print_error(f"Missing expected column during processing: {e} in file {filepath}"); return None
    except Exception as e: logger.print_error(f"An unexpected error occurred while processing CSV {filepath}: {type(e).__name__}: {e}"); traceback.print_exc(); return None