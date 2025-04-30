import pandas as pd
import sys

# Check if pyarrow is installed (it should be if saving worked)
try:
    import pyarrow
    print(f"Using pyarrow version: {pyarrow.__version__}")
except ImportError:
    print("Error: pyarrow library is not installed. Cannot read Parquet.")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python debug_check_parquet.py <path_to_parquet_file>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    print(f"Attempting to read: {file_path}")
    df = pd.read_parquet(file_path)

    print("\n--- File Info ---")
    print(f"Shape: {df.shape}")
    print("\n--- Columns and Dtypes ---")
    print(df.info()) # Provides index type, columns, non-null counts, dtypes, memory usage
    print("\n--- Head ---")
    print(df.head())
    print("\n--- Tail ---")
    print(df.tail())
    print("\n--- Index Check ---")
    print(f"Index Type: {type(df.index)}")
    print(f"Is Index Unique: {df.index.is_unique}")
    print(f"Is Index Monotonic Increasing: {df.index.is_monotonic_increasing}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except Exception as e:
    print(f"Error reading or inspecting Parquet file: {type(e).__name__}: {e}")