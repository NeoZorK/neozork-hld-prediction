# File: src/data/fetchers/csv_fetcher.py
# -*- coding: utf-8 -*-

import pandas as pd
import os
from pathlib import Path
from typing import Optional, Dict
import traceback
import numpy as np # Import numpy for np.nan

# Use absolute import for print functions from the custom logger
from src.common.logger import print_info, print_warning, print_error, print_debug

# --- Define Cache Directory ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
except NameError:
    PROJECT_ROOT = Path('.').resolve()

CSV_CACHE_DIR = PROJECT_ROOT / "data" / "cache" / "csv_converted"
# --- End Cache Directory Definition ---


# Function to fetch data from CSV with Parquet caching enhancement
def fetch_csv_data(
    file_path: str,
    ohlc_columns: Optional[Dict[str, str]] = None,
    date_column: Optional[str] = None,
    time_column: Optional[str] = None,
    datetime_column: Optional[str] = None,
    date_format: Optional[str] = None,
    skiprows: int = 0, # Default to 0, but will use header=1 in read_csv
    separator: str = ',', # Default separator
) -> pd.DataFrame:
    """
    Fetches data from a CSV file, handling various formats and standardizing column names.
    Includes Parquet caching logic. Reads all columns initially, then cleans and selects.
    Uses header=1 for standard MT5 export format.

    Args:
        file_path (str): The path to the CSV file.
        ohlc_columns (Optional[dict[str, str]]): Mapping from standard names ('Open', 'High', 'Low', 'Close', 'Volume')
                                                to actual column names IN THE CSV (e.g., 'Open,', 'TickVolume,').
        date_column (Optional[str]): Not typically needed if datetime_column is correct.
        time_column (Optional[str]): Not typically needed if datetime_column is correct.
        datetime_column (Optional[str]): Name of the single datetime column IN THE CSV (e.g., 'DateTime,').
        date_format (Optional[str]): The strptime format string. Defaults to '%Y.%m.%d %H:%M'.
        skiprows (int): *NOTE: Parameter kept for signature, but header=1 is used internally.*
        separator (str): The delimiter used in the CSV file.

    Returns:
        pd.DataFrame: DataFrame with standardized columns ('Open', 'High', 'Low', 'Close', 'Volume')
                      and a DatetimeIndex named 'Timestamp'. Returns an empty DataFrame on error.
    """
    default_ohlc_columns = {
        'Open': 'Open,', 'High': 'High,', 'Low': 'Low,', 'Close': 'Close,',
        'Volume': 'TickVolume,'
    }
    input_column_mapping_std_to_csv = {**(ohlc_columns or default_ohlc_columns)}
    input_datetime_col_csv = datetime_column or 'DateTime,'

    mapped_volume_key = 'Volume'
    required_std_cols = {'Open', 'High', 'Low', 'Close'}

    try:
        input_path = Path(file_path).resolve()
        if not input_path.is_file():
            print_error(f"CSV file not found: {file_path} (Resolved: {input_path})")
            return pd.DataFrame()

        # --- Parquet Cache Logic ---
        parquet_filename = input_path.stem + ".parquet"
        parquet_path = CSV_CACHE_DIR / parquet_filename
        try:
             CSV_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
             print_error(f"Could not create cache directory {CSV_CACHE_DIR}: {e}")

        if parquet_path.is_file():
            try:
                df = pd.read_parquet(parquet_path)
                if not required_std_cols.issubset(df.columns):
                    raise ValueError("Cached Parquet missing required OHLC columns.")
                if not isinstance(df.index, pd.DatetimeIndex) or df.index.name != 'Timestamp':
                     raise ValueError("Cached Parquet needs DatetimeIndex named 'Timestamp'.")
                return df
            except Exception as e:
                try: os.remove(parquet_path)
                except OSError: pass
        # --- End Parquet Cache Check ---

        # --- CSV Reading Logic ---
        df = pd.read_csv(
            file_path,
            header=1,
            sep=separator,
            low_memory=False
        )

        # --- Clean Actual Column Names ---
        original_columns = df.columns.tolist()
        cleaned_columns = [str(col).strip().rstrip(',') for col in original_columns]
        df.columns = cleaned_columns

        unnamed_cols_to_drop = [col for col in df.columns if col.startswith('Unnamed:') or col == '']
        if unnamed_cols_to_drop:
            df = df.drop(columns=unnamed_cols_to_drop)

        # --- Renaming Logic ---
        rename_map = {}
        expected_csv_to_std_map = {str(v).strip().rstrip(','): k for k, v in input_column_mapping_std_to_csv.items()}
        cleaned_datetime_col_csv = str(input_datetime_col_csv).strip().rstrip(',')

        if cleaned_datetime_col_csv not in df.columns:
             raise ValueError(f"Expected datetime column '{cleaned_datetime_col_csv}' not found after cleaning: {list(df.columns)}")
        if cleaned_datetime_col_csv != 'Timestamp':
             rename_map[cleaned_datetime_col_csv] = 'Timestamp'

        for csv_col_cleaned, std_col in expected_csv_to_std_map.items():
             if csv_col_cleaned in df.columns:
                 if csv_col_cleaned != std_col:
                     rename_map[csv_col_cleaned] = std_col
             else:
                 if std_col in required_std_cols:
                     raise ValueError(f"Required source column '{csv_col_cleaned}' (mapped to '{std_col}') not found in cleaned columns: {list(df.columns)}")
                 else:
                     print_warning(f"Optional volume source column '{csv_col_cleaned}' (mapped to '{std_col}') not found.")

        df = df.rename(columns=rename_map)

        # --- Timestamp Processing ---
        if 'Timestamp' not in df.columns:
            print_error(f"FATAL: 'Timestamp' column confirmed missing right before access. Columns: {list(df.columns)}")
            raise ValueError("'Timestamp' column unexpectedly missing before processing.")

        timestamp_col_data = df['Timestamp']
        try:
            parse_format = date_format or '%Y.%m.%d %H:%M'
            parsed_timestamps = pd.to_datetime(timestamp_col_data, format=parse_format, errors='coerce')

            df.index = parsed_timestamps

            if 'Timestamp' in df.columns:
                 df = df.drop(columns=['Timestamp'])

            df.index.name = 'Timestamp'

            df = df[df.index.notna()]

        except Exception as e:
            raise ValueError(f"Timestamp processing failed: {e}") from e

        # --- Final Column Selection & Type Conversion ---
        current_cols = set(df.columns)
        missing_std_cols = required_std_cols - current_cols
        if missing_std_cols:
            raise ValueError(f"Missing required standard columns after processing: {missing_std_cols}. Available: {list(current_cols)}.")

        final_columns = list(required_std_cols)
        if mapped_volume_key in df.columns:
            final_columns.append(mapped_volume_key)
        else:
            print_warning(f"Standard volume column '{mapped_volume_key}' not found. Volume data will be missing.")

        all_final_columns = final_columns + [col for col in df.columns if col not in final_columns]
        df = df[all_final_columns]

        # Convert types
        for col in required_std_cols:
            if col in df.columns:
                if df[col].dtype == object:
                     df[col] = df[col].replace(['inf', '-inf'], [np.nan, np.nan]) # Use np.nan for float
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float) # Ensure float for OHLC

        if mapped_volume_key in df.columns:
            if df[mapped_volume_key].dtype == object:
                 # --- CHANGE HERE ---
                 # Replace 'inf', '-inf' with NaN for float conversion
                 df[mapped_volume_key] = df[mapped_volume_key].replace(['inf', '-inf'], [np.nan, np.nan])
            # --- CHANGE HERE ---
            # Convert to float, coercing errors to NaN
            df[mapped_volume_key] = pd.to_numeric(df[mapped_volume_key], errors='coerce').astype(float)

        potential_numeric_cols = ['predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
        for col in potential_numeric_cols:
             if col in df.columns:
                 if df[col].dtype == object:
                      df[col] = df[col].replace(['inf', '-inf'], [np.nan, np.nan]) # Use np.nan for float
                 df[col] = pd.to_numeric(df[col], errors='coerce').astype(float) # Ensure float

        # Drop rows if OHLC values are NaN (Volume NaN is often acceptable)
        df = df.dropna(subset=list(required_std_cols))

        df = df.sort_index()

        # --- Save Processed DataFrame to Parquet Cache ---
        if len(df) > 0:
             try:
                 df.to_parquet(parquet_path, index=True)
             except Exception as e:
                 print_error(f"CRITICAL: Failed to save data to Parquet cache {parquet_path}: {e}")
                 traceback.print_exc()

        return df

    # --- Exception Handling ---
    except FileNotFoundError:
        print_error(f"File Not Found Error: {file_path}")
        return pd.DataFrame()
    except ValueError as ve:
        print_error(f"Data Validation or Configuration Error processing CSV {file_path}: {ve}")
        return pd.DataFrame()
    except KeyError as ke:
        print_error(f"Column Not Found Error (KeyError) processing CSV {file_path}: {ke}. Check column names and mappings.")
        return pd.DataFrame()
    except ImportError as ie:
         print_error(f"ImportError: Missing dependency required for Parquet Caching: {ie}")
         print_error("Please install 'pyarrow' or 'fastparquet': pip install pyarrow")
         raise ie
    except Exception as e:
        print_error(f"An unexpected error occurred while processing CSV {file_path}: {e}")
        print_error("Traceback for unexpected error:")
        traceback.print_exc()
        return pd.DataFrame()