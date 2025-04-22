# File: src/data/fetchers/csv_fetcher.py
# -*- coding: utf-8 -*-

import pandas as pd
import os
from pathlib import Path
from typing import Optional, Dict
import traceback  # Import traceback for exception details

# Use relative import for print functions from the custom logger
from ...common.logger import print_info, print_warning, print_error, print_debug

# --- Define Cache Directory ---
try:
    # Assumes the script runs from the project root directory ('NeoZorK HLD')
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
        skiprows: int = 0,
        separator: str = ',',
) -> pd.DataFrame:
    """
    Fetches data from a CSV file, handling various formats and standardizing column names.
    Includes Parquet caching logic: reads from Parquet if available, otherwise reads CSV and saves to Parquet.
    Uses custom print functions for logging.

    Args:
        file_path (str): The path to the CSV file.
        ohlc_columns (Optional[dict[str, str]]): Mapping from standard names ('Open', 'High', 'Low', 'Close', 'Volume')
                                                to actual column names in the CSV. Defaults used if None.
        date_column (Optional[str]): Name of the date column if date and time are separate.
        time_column (Optional[str]): Name of the time column if date and time are separate.
        datetime_column (Optional[str]): Name of the single datetime column.
        date_format (Optional[str]): The strptime format string for parsing dates/datetimes. Auto-detection if None.
        skiprows (int): Number of rows to skip at the beginning of the file.
        separator (str): The delimiter used in the CSV file.

    Returns:
        pd.DataFrame: DataFrame with standardized columns ('Open', 'High', 'Low', 'Close', 'Volume')
                      and a DatetimeIndex named 'Timestamp'. Returns an empty DataFrame on error.
    """
    default_ohlc_columns = {
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume'  # Adjust if your MT5 exports 'Tick Volume' or 'Real Volume'
    }
    column_mapping = {**(ohlc_columns or default_ohlc_columns)}
    # Ensure Volume is included, even if default (can be 'Volume', 'Tick Volume', etc.)
    volume_keys_to_check = ['Volume', 'Tick Volume', 'Real Volume']
    mapped_volume_key = 'Volume'  # The standard key we want internally

    provided_volume_source = None
    for std_key, csv_key in column_mapping.items():
        if std_key == mapped_volume_key:
            provided_volume_source = csv_key
            break

    if provided_volume_source is None:
        for vol_key in volume_keys_to_check:
            if vol_key in default_ohlc_columns.values():
                provided_volume_source = vol_key
                column_mapping[mapped_volume_key] = vol_key  # Add mapping explicitly
                break
        if provided_volume_source is None:
            provided_volume_source = 'Volume'
            column_mapping[mapped_volume_key] = 'Volume'

    required_std_cols = {'Open', 'High', 'Low', 'Close'}

    try:
        input_path = Path(file_path).resolve()  # Use resolved absolute path
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
            # Continue without caching if directory creation fails

        if parquet_path.is_file():
            try:
                print_info(f"Attempting to load cached CSV data from Parquet: {parquet_path}")
                df = pd.read_parquet(parquet_path)
                # Basic validation after loading cache
                if not required_std_cols.issubset(df.columns):
                    raise ValueError(
                        f"Cached Parquet missing required OHLC columns: {required_std_cols - set(df.columns)}")
                if mapped_volume_key not in df.columns:
                    print_warning(f"Cached Parquet missing '{mapped_volume_key}' column.")
                if not isinstance(df.index, pd.DatetimeIndex) or df.index.name != 'Timestamp':
                    raise ValueError("Cached Parquet does not have a valid DatetimeIndex named 'Timestamp'.")

                print_info(f"Successfully loaded {len(df)} rows from Parquet cache: {parquet_path}")
                return df
            except Exception as e:
                print_warning(
                    f"Failed to load or validate Parquet cache {parquet_path}: {e}. Will read CSV and attempt to overwrite cache.")
                try:
                    os.remove(parquet_path)
                    print_info(f"Removed potentially corrupted cache file: {parquet_path}")
                except OSError as rm_err:
                    print_warning(f"Could not remove potentially corrupted cache file {parquet_path}: {rm_err}")
        # --- End Parquet Cache Check ---

        # --- CSV Reading Logic ---
        print_info(f"Reading CSV data from: {file_path}")

        csv_cols_to_read = list(column_mapping.values())
        datetime_source_cols = []
        if datetime_column and datetime_column not in csv_cols_to_read:
            datetime_source_cols.append(datetime_column)
        if date_column and date_column not in csv_cols_to_read:
            datetime_source_cols.append(date_column)
        if time_column and time_column not in csv_cols_to_read:
            datetime_source_cols.append(time_column)

        csv_use_cols = list(set(csv_cols_to_read + datetime_source_cols))
        print_debug(f"Reading columns from CSV: {csv_use_cols}")

        df = pd.read_csv(
            file_path,
            skiprows=skiprows,
            sep=separator,
            usecols=csv_use_cols,
            low_memory=False
        )
        print_debug(f"Read {len(df)} rows from CSV initially.")

        # --- Timestamp Processing ---
        timestamp_col_data = None
        if datetime_column:
            if datetime_column not in df.columns:
                raise ValueError(f"Specified datetime_column '{datetime_column}' not found in CSV.")
            timestamp_col_data = df[datetime_column]
            print_debug(f"Using single datetime column: {datetime_column}")
        elif date_column and time_column:
            if date_column not in df.columns or time_column not in df.columns:
                raise ValueError(f"Specified date_column '{date_column}' or time_column '{time_column}' not found.")
            timestamp_col_data = df[date_column].astype(str) + ' ' + df[time_column].astype(str)
            print_debug(f"Combining date '{date_column}' and time '{time_column}' columns.")
        elif date_column:  # Handle date only if time is missing
            if date_column not in df.columns:
                raise ValueError(f"Specified date_column '{date_column}' not found in CSV.")
            timestamp_col_data = df[date_column]
            print_debug(f"Using date column only: {date_column}")
        else:
            common_dt_cols = ['Timestamp', 'Date', 'time', 'date']
            found_dt_col = None
            for col in common_dt_cols:
                if col in df.columns:
                    found_dt_col = col
                    print_warning(f"No date/time column specified, auto-detected '{found_dt_col}'.")
                    break
            if found_dt_col:
                timestamp_col_data = df[found_dt_col]
            else:
                raise ValueError(
                    "Must specify 'datetime_column' or ('date_column' and 'time_column'), or have a standard 'Timestamp'/'Date' column.")

        try:
            parsed_timestamps = pd.to_datetime(timestamp_col_data, format=date_format, errors='coerce')
            if parsed_timestamps.isnull().sum() > 0.5 * len(df):
                print_error(
                    f"High number of timestamp parsing errors ({parsed_timestamps.isnull().sum()}/{len(df)}). Check date format and data.")
                print_error("Sample values that might be causing issues:")
                print_error(str(timestamp_col_data[parsed_timestamps.isnull()].head()))  # Use str() for safety
                # raise ValueError("Timestamp parsing failed for too many rows.")
            elif parsed_timestamps.isnull().sum() > 0:
                print_warning(
                    f"{parsed_timestamps.isnull().sum()} rows had timestamp parsing errors and were set to NaT.")

            df['Timestamp'] = parsed_timestamps
            df = df.dropna(subset=['Timestamp'])
            df = df.set_index('Timestamp')
            print_debug("Timestamp index created successfully.")

        except Exception as e:
            print_error(f"Error parsing timestamp data: {e}")
            print_error("Sample values being parsed:")
            try:
                print_error(str(timestamp_col_data.head()))  # Use str() for safety
            except AttributeError:
                print_error("Could not display sample timestamp data.")
            raise

            # --- Column Renaming and Selection ---
        rename_map = {v: k for k, v in column_mapping.items() if v in df.columns}
        df = df.rename(columns=rename_map)

        current_cols = set(df.columns)
        missing_std_cols = required_std_cols - current_cols
        if missing_std_cols:
            raise ValueError(
                f"Missing required standard columns after mapping/renaming: {missing_std_cols}. Available columns: {list(current_cols)}. Check source CSV and 'ohlc_columns' mapping.")

        final_columns = list(required_std_cols)
        if mapped_volume_key in df.columns:
            final_columns.append(mapped_volume_key)
        else:
            print_warning(
                f"Standard volume column '{mapped_volume_key}' not found after processing CSV. Volume data will be missing.")

        df = df[final_columns]
        print_debug(f"Selected final columns: {final_columns}")

        # --- Data Type Conversion and Cleaning ---
        for col in required_std_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if mapped_volume_key in df.columns:
            df[mapped_volume_key] = pd.to_numeric(df[mapped_volume_key], errors='coerce').astype('Int64')

        initial_rows = len(df)
        df = df.dropna(subset=list(required_std_cols))
        dropped_rows = initial_rows - len(df)
        if dropped_rows > 0:
            print_warning(
                f"Dropped {dropped_rows} rows due to NaN values in required OHLC columns after numeric conversion.")

        df = df.sort_index()
        if not df.index.is_monotonic_increasing:
            print_warning(
                "Timestamp index is not monotonically increasing after sorting. Check for duplicate timestamps.")

        print_info(f"Successfully processed {len(df)} rows from CSV: {file_path}")
        # --- End CSV Reading Logic ---

        # --- Save Processed DataFrame to Parquet Cache ---
        if len(df) > 0:
            try:
                print_info(f"Saving processed data to Parquet cache: {parquet_path}")
                df.to_parquet(parquet_path, index=True)
                print_debug(f"Data successfully saved to {parquet_path}")
            except Exception as e:
                print_error(f"CRITICAL: Failed to save data to Parquet cache {parquet_path}: {e}")
                print_error("The data is processed in memory but will not be cached for the next run.")
                # Print traceback for save error
                print_error("Traceback for Parquet save error:")
                traceback.print_exc()
        else:
            print_warning("Processed DataFrame is empty. Skipping Parquet cache saving.")

        # --- Return the Processed DataFrame ---
        return df

    # --- Exception Handling for the entire function ---
    except FileNotFoundError:
        print_error(f"File Not Found Error: {file_path}")
        return pd.DataFrame()
    except ValueError as ve:
        print_error(f"Data Validation or Configuration Error processing CSV {file_path}: {ve}")
        return pd.DataFrame()
    except KeyError as ke:
        print_error(
            f"Column Not Found Error (KeyError) processing CSV {file_path}: {ke}. Check column names and mappings.")
        return pd.DataFrame()
    except ImportError as ie:
        print_error(f"ImportError: Missing dependency required for Parquet Caching: {ie}")
        print_error("Please install 'pyarrow' or 'fastparquet': pip install pyarrow")
        raise ie  # Re-raise to halt execution
    except Exception as e:
        print_error(f"An unexpected error occurred while processing CSV {file_path}: {e}")
        # Print traceback for unexpected errors
        print_error("Traceback for unexpected error:")
        traceback.print_exc()
        return pd.DataFrame()