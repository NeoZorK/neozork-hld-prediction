# src/data_utils.py

"""
Utility functions for fetching and preparing data (demo or yfinance).
All comments are in English.
"""
import pandas as pd
import yfinance as yf
import time
from datetime import date, timedelta
from pathlib import Path # Added for fetch_csv_data
import numpy as np     # Added for fetch_csv_data

# Assuming logger is imported if used
# Use relative import for the logger within the src package
from ..common import logger


# Added Function: Reads data from a CSV file (expected format from MQL5)
def fetch_csv_data(filepath: str) -> pd.DataFrame | None:
    """
    Reads historical OHLCV and indicator data from a specified CSV file.

    Expected format:
    - First row might be informational and skipped (header=1).
    - Comma-separated.
    - Columns like DateTime, TickVolume, Open, High, Low, Close, and potentially indicator columns.
    - DateTime format like 'YYYY.MM.DD HH:MM'.
    - Last column name might have a trailing comma.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame | None: A DataFrame containing the data with a DatetimeIndex
                             and standardized columns ('Open', 'High', 'Low', 'Close', 'Volume'),
                             plus any other numeric columns found. Returns None if reading fails.
    """
    logger.print_debug(f"Attempting to read CSV file: {filepath}")
    file_path_obj = Path(filepath)

    # Check if the file exists
    # Checks if the specified file actually exists.
    if not file_path_obj.is_file():
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None

    try:
        # Read the CSV file using pandas
        # sep=',': Specifies the delimiter is a comma.
        # header=1: Indicates that the header row is the second row (index 1), skipping the first info line.
        # skipinitialspace=True: Handles potential extra spaces around column names or values.
        # low_memory=False: Can sometimes help with parsing complex files or mixed types.
        df = pd.read_csv(file_path_obj, sep=',', header=1, skipinitialspace=True, low_memory=False)

        if df.empty:
            logger.print_warning(f"CSV file is empty: {filepath}")
            return None

        # --- Data Cleaning ---
        # 1. Clean column names: remove leading/trailing whitespace and trailing commas
        # Creates a list of cleaned column names by stripping whitespace and trailing commas.
        original_columns = df.columns.tolist()
        cleaned_columns = [str(col).strip().rstrip(',') for col in original_columns]
        # Assigns the cleaned names back to the DataFrame.
        df.columns = cleaned_columns
        logger.print_debug(f"Original CSV columns: {original_columns}")
        logger.print_debug(f"Cleaned CSV columns: {cleaned_columns}")

        # 2. Identify and drop potential unnamed column from trailing comma
        # Finds columns named '', typically resulting from trailing commas in the header.
        unnamed_cols = [col for col in df.columns if col == '' or 'Unnamed' in col] # Check for empty string and 'Unnamed' pattern
        if unnamed_cols:
            logger.print_debug(f"Dropping unnamed/empty columns: {unnamed_cols}")
            # Drops the identified unnamed columns. errors='ignore' prevents errors if columns don't exist.
            df.drop(columns=unnamed_cols, inplace=True, errors='ignore')

        # 3. Parse 'DateTime' column and set as index
        # Checks if the 'DateTime' column exists after cleaning.
        if 'DateTime' not in df.columns:
            logger.print_error("Mandatory 'DateTime' column not found in CSV.")
            return None

        # Converts the 'DateTime' column to datetime objects using the specified format.
        # errors='coerce' turns unparseable dates into NaT.
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
        # Stores the number of rows before dropping NaT dates.
        rows_before_dropna = len(df)
        # Drops rows where 'DateTime' parsing failed (became NaT).
        df.dropna(subset=['DateTime'], inplace=True)
        rows_after_dropna = len(df)
        # Logs how many rows were dropped due to invalid dates.
        if rows_before_dropna > rows_after_dropna:
            logger.print_warning(f"Dropped {rows_before_dropna - rows_after_dropna} rows with invalid DateTime format.")

        # Checks if the DataFrame is empty after dropping invalid date rows.
        if df.empty:
            logger.print_warning("DataFrame became empty after removing rows with invalid dates.")
            return None
        # Sets the 'DateTime' column as the DataFrame index.
        df.set_index('DateTime', inplace=True)

        # 4. Rename 'TickVolume' to 'Volume' for consistency
        # Renames the 'TickVolume' column to 'Volume'. errors='ignore' prevents error if 'TickVolume' doesn't exist.
        df.rename(columns={'TickVolume': 'Volume'}, inplace=True, errors='ignore')

        # 5. Convert all remaining columns to numeric if possible, replace inf
        # Iterates through all columns remaining after cleaning and indexing.
        for col in df.columns:
             # Skips the Volume column if it should remain integer (adjust if float volume needed)
             # if col == 'Volume':
             #     df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64') # Use nullable Int
             # else:
             # Converts column to numeric. errors='coerce' makes non-numeric values NaN.
             df[col] = pd.to_numeric(df[col], errors='coerce')

        # Replace infinite values with NaN, as they can cause issues in calculations
        # Finds infinite values (inf, -inf) across the DataFrame.
        inf_mask = np.isinf(df.select_dtypes(include=[np.number]))
        # Checks if any infinite values were found.
        if inf_mask.any().any():
            logger.print_warning("Replacing infinite values (inf, -inf) with NaN.")
            # Replaces all infinite values with NaN (Not a Number).
            df.replace([np.inf, -np.inf], np.nan, inplace=True)


        # 6. Check for essential OHLCV columns
        # Defines the minimum required columns for downstream processing.
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        # Finds which required columns are missing from the DataFrame.
        missing_cols = [col for col in required_cols if col not in df.columns]
        # Checks if any required columns are missing.
        if missing_cols:
            logger.print_error(f"CSV data is missing required columns after processing: {missing_cols}")
            logger.print_error(f"Available columns: {df.columns.tolist()}") # type: ignore
            return None # Cannot proceed without essential columns

        logger.print_info(f"Successfully read and processed {len(df)} rows from {filepath}")
        return df

    # Handles specific errors during file reading or processing.
    except FileNotFoundError:
        logger.print_error(f"CSV file not found at path: {file_path_obj}")
        return None
    except pd.errors.EmptyDataError:
        logger.print_error(f"CSV file is empty: {filepath}")
        return None
    except pd.errors.ParserError as e:
        logger.print_error(f"Failed to parse CSV file: {filepath} - Error: {e}")
        return None
    except KeyError as e:
         logger.print_error(f"Missing expected column during processing: {e} in file {filepath}")
         return None
    except Exception as e:
        logger.print_error(f"An unexpected error occurred while processing CSV {filepath}: {type(e).__name__}: {e}")
        # Optionally log traceback for unexpected errors
        # import traceback
        # logger.print_error(f"Traceback:\n{traceback.format_exc()}")
        return None


# Existing function
def get_demo_data() -> pd.DataFrame:
    """Returns the demonstration DataFrame."""
    # Use logger instead of print
    logger.print_info("Generating demo data...")
    # Simulate a short delay for "loading"
    time.sleep(0.5)
    # Demo data definition (same as before)
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138,
                 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150,
                 1.152, 1.155, 1.153, 1.158, 1.160, 1.157, 1.162, 1.165, 1.163, 1.160],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142,
                 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155,
                 1.156, 1.159, 1.158, 1.161, 1.163, 1.160, 1.165, 1.168, 1.166, 1.164],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136,
                1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148,
                1.150, 1.152, 1.151, 1.155, 1.157, 1.154, 1.159, 1.161, 1.160, 1.158],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14,
                  1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149,
                  1.155, 1.154, 1.157, 1.160, 1.159, 1.158, 1.163, 1.164, 1.161, 1.159],
        'Volume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650,
                   1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200,
                   2150, 2250, 2100, 2300, 2400, 2350, 2450, 2500, 2400, 2300]
    }
    # Creates a date range for the index, ending today.
    start_date_idx = date.today() - timedelta(days=len(data['Open'])-1)
    # Generates a DatetimeIndex with daily frequency.
    index = pd.date_range(start=start_date_idx, periods=len(data['Open']), freq='D')
    # Creates the DataFrame with the generated index.
    df = pd.DataFrame(data, index=index)

    # Rename columns for mplfinance compatibility - already correct in definition
    # df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df


# Existing function
def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    # Converts input timeframe to uppercase for case-insensitive matching.
    tf_input_upper = tf_input.upper()

    # Mapping from user input (like M1, D1) to yfinance interval (like 1m, 1d)
    # Defines a dictionary mapping common timeframe notations to yfinance interval strings.
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h",
        "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk",
        "MN1": "1mo", "MN": "1mo", "MO": "1mo"
    }
    # Valid intervals directly accepted by yfinance
    # Defines a list of interval strings directly supported by yfinance.
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

    # Checks if the uppercase input exists as a key in the mapping dictionary.
    if tf_input_upper in mapping:
        # Returns the corresponding yfinance interval from the mapping.
        return mapping[tf_input_upper]
    # Checks if the lowercase input is directly a valid yfinance interval.
    elif tf_input.lower() in valid_yf_intervals:
         # Allow direct use of yfinance intervals
         # Returns the lowercase input as it's already a valid yfinance interval.
         return tf_input.lower()
    # If the input doesn't match any mapping or valid interval, raise an error.
    else:
        raise ValueError(f"Invalid timeframe input: '{tf_input}'. Use formats like 'M1', 'H1', 'D1', 'W1', 'MN1' or yfinance intervals like '1m', '1h', '1d', '1wk', '1mo'.")


# Existing function
def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns."""
    # Converts the input ticker to uppercase.
    ticker = ticker_input.upper()

    # Example: Add '=X' for 6-char currency pairs without a suffix
    # Checks if the ticker has 6 characters and doesn't contain '=' or '-'.
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker:
         # Checks if all characters in the ticker are alphabetic.
         is_likely_forex = all(c.isalpha() for c in ticker)
         # If it's likely a Forex pair, log an info message and append '=X'.
         if is_likely_forex:
             logger.print_info(f"Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
             return f"{ticker}=X"

    # Return the ticker as is if no rules matched or it wasn't modified.
    return ticker


# Existing function
def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """Downloads data from Yahoo Finance, handles MultiIndex columns, and validates."""
    # Logs the attempt to fetch data with specific parameters.
    logger.print_info(f"Attempting to fetch data for ticker: {ticker} | interval: {interval}")
    try:
        # Calls yfinance.download to get the data.
        # progress=True shows a progress bar.
        # auto_adjust=False prevents automatic adjustment for splits/dividends (we might want raw data).
        # actions=False excludes dividend and stock split data.
        df = yf.download(
            tickers=ticker, # Single ticker string
            period=period,
            interval=interval,
            start=start_date,
            end=end_date,
            progress=True,
            auto_adjust=False,
            actions=False,
            # group_by='ticker' # Often forces MultiIndex, good practice for consistency
        )

        # Checks if yfinance returned None or an empty DataFrame.
        if df is None or df.empty:
            logger.print_warning(f"No data returned for ticker '{ticker}' with specified parameters.")
            return None

        # --- Handle Potential MultiIndex Columns ---
        # Check if columns are MultiIndex (returned when downloading single ticker sometimes)
        # Checks if the DataFrame columns have a MultiIndex structure.
        if isinstance(df.columns, pd.MultiIndex):
            logger.print_debug("Detected MultiIndex columns. Simplifying by dropping ticker level...")
            # Assuming the structure is (ValueType, Ticker) like ('Open', 'GOOG')
            # Drop the second level (Ticker) to get simple column names ('Open', 'High', ...)
            # Check number of levels first to be safe
            # Checks if there are multiple levels in the MultiIndex.
            if df.columns.nlevels > 1:
                 # Stores the original MultiIndex columns for debugging if needed.
                 original_cols = df.columns # Keep original for potential debug messages
                 try:
                     # Drops the second level (level 1, typically the ticker) of the MultiIndex.
                     df.columns = df.columns.droplevel(1) # Drop the ticker level (level 1)
                     logger.print_debug(f"Simplified columns: {df.columns.tolist()}")
                 # Catches errors during the droplevel operation.
                 except Exception as multi_index_error:
                     logger.print_error(f"Failed to simplify MultiIndex columns: {multi_index_error}")
                     logger.print_error(f"Original MultiIndex columns were: {original_cols}")
                     return None # Cannot proceed if columns aren't simplified
            # Handles unlikely case of a single-level MultiIndex.
            else:
                 # Handle cases where it's MultiIndex but only one level? Unlikely but possible.
                 logger.print_warning("MultiIndex detected but only one level found. Attempting basic flatten.")
                 try:
                    # Attempts to flatten the columns by joining levels with underscores.
                    df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
                 except Exception as flatten_error:
                    logger.print_error(f"Failed to flatten unusual MultiIndex: {flatten_error}")
                    return None

        # --- Validate Columns and Data (using potentially simplified column names) ---
        # Defines the essential columns required for downstream processing.
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        # Finds which required columns are missing from the DataFrame columns.
        missing_cols = [col for col in required_cols if col not in df.columns]
        # Checks if any required columns are missing.
        if missing_cols:
            logger.print_warning(f"Downloaded data for '{ticker}' is missing required columns: {missing_cols}. Available columns after potential simplification: {df.columns.tolist()}")
            return None # Return None if essential columns are missing

        # --- Drop Rows with NaNs in essential price columns ---
        # Now this should work because columns are simple strings
        # Stores the number of rows before dropping NaNs.
        initial_rows = len(df)
        try:
            # Use standard OHLC column names here
            # Drops rows where ALL specified OHLC columns are NaN.
            df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all', inplace=True)
        except KeyError as ke:
            # This shouldn't happen if the check above passed, but as a safeguard
            # Catches potential errors if column names weren't simplified correctly.
            logger.print_error(f"KeyError during dropna, columns might not be simplified correctly: {ke}")
            logger.print_error(f"Columns at time of dropna: {df.columns.tolist()}")
            return None

        # Calculates the number of rows dropped.
        rows_dropped = initial_rows - len(df)
        # Logs if any rows were dropped due to NaNs in OHLC.
        if rows_dropped > 0:
             logger.print_debug(f"Dropped {rows_dropped} rows with NaNs in OHLC columns.")

        # Checks if the DataFrame became empty after dropping rows.
        if df.empty:
            logger.print_warning(f"Data for '{ticker}' became empty after removing NaN rows.")
            return None

        logger.print_success(f"Successfully fetched and validated {len(df)} rows.")
        # Returns the processed DataFrame.
        return df

    # Catches any unexpected exceptions during the download or processing.
    except Exception as e:
        # General exception handler
        logger.print_error(f"\n--- ERROR DOWNLOADING/PROCESSING ---")
        logger.print_error(f"An unexpected error occurred for ticker '{ticker}': {type(e).__name__}: {e}")
        import traceback
        # Print traceback with error color using the logger's color constants if available
        # Gets the formatted traceback string.
        tb_str = traceback.format_exc()
        # Tries to print the traceback using error color from the logger. Falls back to default print if needed.
        try:
             print(f"{logger.ERROR_COLOR}Traceback:\n{tb_str}{logger.RESET_ALL}")
        except AttributeError: # Fallback if logger colors aren't set up as expected
             print(f"Traceback:\n{tb_str}")

        logger.print_error(f"--- END ERROR ---")
        return None