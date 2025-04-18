# NeoZorK HLD/debug_csv_reader.py

import pandas as pd
import argparse
import sys
from pathlib import Path
import numpy as np # Import numpy to check for inf values later if needed

# Setup argument parser to accept a file path
# Sets up an argument parser to accept command-line arguments.
parser = argparse.ArgumentParser(
    description="Read and display basic info from an MQL5 exported CSV file."
)
# Adds an argument '--file' which expects the path to the CSV file.
# Default value is set to the sample file provided.
parser.add_argument(
    "--file",
    type=str,
    default="mql5_feed/CSVExport_XAUUSD_PERIOD_MN1.csv",
    help="Path to the CSV file to read.",
)
# Parses the arguments provided when running the script.
args = parser.parse_args()

# Get the absolute path to the file
# Constructs the full path to the CSV file based on the script's location and the provided argument.
# resolve() makes the path absolute.
file_path = Path(__file__).parent / args.file

print(f"--- Testing CSV Reader ---")
print(f"Attempting to read: {file_path}")

# Check if the file exists before trying to read
# Checks if the specified file actually exists.
if not file_path.is_file():
    print(f"\n[Error] File not found at path: {file_path}")
    sys.exit(1) # Exit if file not found

try:
    # Read the CSV file using pandas
    # Reads the CSV file into a pandas DataFrame.
    # sep=',': Specifies the delimiter is a comma.
    # header=1: Indicates that the header row is the second row (index 1), skipping the first info line.
    # skipinitialspace=True: Handles potential extra spaces around column names or values.
    # low_memory=False: Can sometimes help with parsing complex files or mixed types, though might use more memory.
    df = pd.read_csv(file_path, sep=',', header=1, skipinitialspace=True, low_memory=False)

    # --- Data Cleaning ---
    # 1. Clean column names: remove leading/trailing whitespace and trailing commas
    # Creates a list of cleaned column names.
    # str.strip() removes leading/trailing whitespace.
    # str.rstrip(',') removes trailing commas specifically.
    cleaned_columns = [col.strip().rstrip(',') for col in df.columns]
    # Assigns the cleaned names back to the DataFrame.
    df.columns = cleaned_columns

    # 2. Parse 'DateTime' column and set as index
    # Converts the 'DateTime' column to datetime objects.
    # format='%Y.%m.%d %H:%M': Explicitly tells pandas the format of the date string.
    # errors='coerce': If a date cannot be parsed, it will be replaced with NaT (Not a Time).
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y.%m.%d %H:%M', errors='coerce')
    # Drops rows where DateTime could not be parsed (resulting in NaT).
    df.dropna(subset=['DateTime'], inplace=True)
    # Sets the 'DateTime' column as the index of the DataFrame.
    df.set_index('DateTime', inplace=True)

    # 3. Convert relevant columns to numeric, coercing errors
    # Defines the columns expected to contain numerical data (OHLCV + indicator outputs).
    numeric_cols = ['TickVolume', 'Open', 'High', 'Low', 'Close',
                    'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
    # Iterates through the expected numeric columns.
    for col in numeric_cols:
        # Checks if the column exists in the DataFrame.
        if col in df.columns:
             # Converts the column to numeric type.
             # errors='coerce': If a value cannot be converted to numeric, it becomes NaN (Not a Number).
             df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            # Prints a warning if an expected numeric column is missing.
            print(f"[Warning] Expected numeric column '{col}' not found in the CSV.")

    # --- Display Information ---
    print("\n[Success] CSV file read successfully.")
    print(f"\nShape: {df.shape}") # (rows, columns)

    print("\nColumns:")
    # Prints the list of final column names.
    print(list(df.columns))

    print("\nData Types:")
    # Prints the data type of each column.
    print(df.dtypes)

    print("\nIndex Info:")
    # Prints information about the DataFrame's index (should be DatetimeIndex).
    print(df.index)

    print("\nHead (First 5 rows):")
    # Prints the first 5 rows of the DataFrame.
    print(df.head())

    print("\nTail (Last 5 rows):")
    # Prints the last 5 rows of the DataFrame.
    print(df.tail())

    # Optional: Check for infinity values introduced by calculations if needed
    # Checks if any infinite values exist in the DataFrame.
    # np.isinf(df).any().any() checks across all rows and columns.
    if np.isinf(df.select_dtypes(include=[np.number])).any().any():
        print("\n[Warning] Infinite values (inf, -inf) detected in the DataFrame.")

except FileNotFoundError:
    # Handles the specific error if the file path is correct but the file doesn't exist.
    print(f"\n[Error] File not found at path: {file_path}")
    sys.exit(1)
except pd.errors.EmptyDataError:
    # Handles the error if the CSV file is empty.
    print(f"\n[Error] The file is empty: {file_path}")
    sys.exit(1)
except Exception as e:
    # Catches any other unexpected errors during file reading or processing.
    print(f"\n[Error] An unexpected error occurred: {type(e).__name__}: {e}")
    # Prints the full traceback for debugging.
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n--- End of CSV Test ---")