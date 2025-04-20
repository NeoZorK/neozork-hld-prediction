# src/data/fetchers/csv_fetcher.py # Re-verified Cleaning Sequence

"""
Contains the function to fetch and process data from a CSV file.
"""
import os # Import os to get file size, or use pathlib more
import pandas as pd
import numpy as np
from pathlib import Path
from ...common import logger # Relative import from parent's sibling
import traceback # Import traceback for detailed error logging


# Definition of the fetch_csv_data function
# MODIFIED: Return type is now tuple[pd.DataFrame | None, dict]
def fetch_csv_data(filepath: str) -> tuple[pd.DataFrame | None, dict]:
    """
    Reads historical OHLCV and indicator data from a specified CSV file.
    Performs cleaning: strips column names, handles datetimes, converts numerics, replaces inf.
    Returns a tuple: (DataFrame or None, metrics dictionary).
    """
    logger.print_debug(f"Attempting to read CSV file: {filepath}")
    file_path_obj = Path(filepath)
    metrics = {"file_size_bytes": None} # Initialize metrics dict

    if not file_path_obj.is_file():
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None, metrics # Return None df and basic metrics

    try:
        # Get file size BEFORE reading
        metrics["file_size_bytes"] = file_path_obj.stat().st_size
        logger.print_debug(f"File size: {metrics['file_size_bytes']} bytes")

        # 1. Read the CSV file using pandas
        # Pass explicit types to potentially reduce memory and handle specific columns better
        # Example: Specify types for known numeric columns if possible
        # dtype_spec = {'Open': float, 'High': float, 'Low': float, 'Close': float, 'TickVolume': float}
        # df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False, dtype=dtype_spec)
        # Or read as default first:
        df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False)

        if df.empty:
            logger.print_warning(f"CSV file is empty: {filepath}")
            # Return empty DataFrame and metrics if needed, or None
            return None, metrics # Return None df if file is empty

        # 2. Clean column names (rest of the logic remains the same)
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
            return None, metrics
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
        rows_before_dropna_dt = len(df)
        df.dropna(subset=['DateTime'], inplace=True)
        rows_after_dropna_dt = len(df)
        if rows_before_dropna_dt > rows_after_dropna_dt:
            logger.print_warning(f"Dropped {rows_before_dropna_dt - rows_after_dropna_dt} rows with invalid DateTime format.")
        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with invalid dates.")
            return None, metrics
        df.set_index('DateTime', inplace=True)

        # 4. Rename TickVolume to Volume for consistency
        df.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')

        # 5. Convert potentially numeric columns to numeric (coerce errors)
        potential_numeric_cols = df.columns
        for col in potential_numeric_cols:
            # Check if the column is not already numeric before trying conversion
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                 try:
                     # Attempt conversion
                     converted_col = pd.to_numeric(df[col], errors='coerce')
                     # Check if conversion actually changed the type (it might coerce object to object if all fail)
                     if pd.api.types.is_numeric_dtype(converted_col):
                          df[col] = converted_col
                          logger.print_debug(f"Coerced column '{col}' to numeric.")
                     # else: # Optional: Log if coercion didn't result in numeric
                     #    logger.print_debug(f"Column '{col}' could not be fully coerced to numeric (remains {df[col].dtype}).")
                 except ValueError: # Catch errors during to_numeric if needed, though 'coerce' handles most
                      logger.print_warning(f"Could not coerce column '{col}' to numeric during general conversion due to ValueError.")
                 except Exception as e:
                      logger.print_warning(f"Could not coerce column '{col}' to numeric during general conversion: {type(e).__name__}")


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
            return None, metrics

        # 8. Drop rows if *any* of the required OHLCV columns have NaN AFTER conversion
        initial_rows_after_dt = len(df)
        df.dropna(subset=required_cols, how='any', inplace=True)
        rows_dropped_nan = initial_rows_after_dt - len(df)
        if rows_dropped_nan > 0:
            logger.print_debug(f"Dropped {rows_dropped_nan} rows with NaN in required OHLCV columns after conversion/inf handling.")

        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with NaN in required columns.")
            return None, metrics

        logger.print_info(f"Successfully read and processed {len(df)} rows from {filepath}")
        # Return DataFrame and metrics dict
        return df, metrics

    except FileNotFoundError:
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None, metrics
    except pd.errors.EmptyDataError:
        logger.print_error(f"CSV file is empty: {filepath}")
        return None, metrics
    except pd.errors.ParserError as e:
        logger.print_error(f"Failed to parse CSV file: {filepath} - Error: {e}")
        return None, metrics
    except KeyError as e:
        logger.print_error(f"Missing expected column during processing: {e} in file {filepath}")
        return None, metrics
    except Exception as e:
        logger.print_error(f"An unexpected error occurred while processing CSV {filepath}: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None, metrics