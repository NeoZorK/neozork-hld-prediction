# -*- coding: utf-8 -*-
# scripts/data_processing/data_cleaner_v2.py

import os
import argparse
import logging
from typing import List, Tuple, Optional
import pandas as pd
from tqdm import tqdm
import sys # For exiting on critical errors

# Global logger instance
logger = None

# --- Logging Configuration ---
def setup_logger(log_file: str) -> logging.Logger:
    """Configure logger for file and console output."""
    # Use a local name for clarity
    log_instance = logging.getLogger("data_cleaner_v2")
    log_instance.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Remove existing handlers if any
    if log_instance.handlers:
        for handler in log_instance.handlers[:]:
            log_instance.removeHandler(handler)
            
    # Add new handlers
    # File handler (overwrite mode)
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    log_instance.addHandler(file_handler)

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO) # Output INFO and above to console
    log_instance.addHandler(stream_handler)

    log_instance.propagate = False
    return log_instance

# --- File Processing Functions ---
def find_data_files(folder_paths: List[str], extensions: List[str] = [".parquet", ".csv"]) -> List[Tuple[str, str]]:
    """
    Recursively search for files with the given extensions in a list of folders.
    Returns a list of tuples (file_path, base_input_folder).
    """
    data_files = []
    for base_folder in folder_paths:
        abs_base_folder = os.path.abspath(base_folder)
        if not os.path.isdir(abs_base_folder):
            logger.warning(f"Directory not found, skipping: {abs_base_folder}")
            continue
        logger.info(f"Searching files in: {abs_base_folder}")
        for root, dirs, files in os.walk(abs_base_folder):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    data_files.append((full_path, abs_base_folder)) # Using abs_base_folder for correct relpath
    return data_files

def clean_file(
    input_path: str,
    input_base_dir: str,
    output_base_dir: str,
    handle_duplicates: str,
    handle_nan: str,
    csv_delimiter: str,
    csv_header: Optional[int] # Header can be int or None (we'll use 'infer' in read_csv)
    ) -> bool:
    """
    Loads, cleans (duplicates, NaN) and saves data file according to settings.
    Returns True on success, False on error.
    """
    logger.info(f"Processing file: {input_path}")
    file_type = None
    if input_path.lower().endswith(".csv"):
        file_type = "csv"
    elif input_path.lower().endswith(".parquet"):
        file_type = "parquet"
    else:
        # This check is redundant, since find_data_files already filters, but keeping for safety
        logger.error(f"Unsupported file type (logic error): {input_path}")
        return False

    # --- Creating output path ---
    try:
        relative_path = os.path.relpath(input_path, input_base_dir)
        output_path = os.path.join(output_base_dir, relative_path)
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True) # Create subdirectories if they don't exist
    except Exception as e:
        logger.error(f"Error creating output path for {input_path} (base: {input_base_dir}): {e}")
        return False

    try:
        # --- Loading data ---
        df = None
        load_successful = False
        if file_type == "csv":
            try:
                # Use provided CSV parsing parameters
                header_arg = 'infer' if csv_header is None else csv_header
                df = pd.read_csv(input_path, delimiter=csv_delimiter, header=header_arg, low_memory=False)
                logger.info(f"  Successfully loaded CSV: delimiter='{csv_delimiter}', header={header_arg}")
                load_successful = True
            except Exception as load_err:
                logger.error(f"  Error loading CSV file {input_path} with delimiter='{csv_delimiter}' header={header_arg}: {load_err}")
                # Could try with other parameters, but for now just report the error
                return False # Consider it an error if loading fails
        else: # parquet
            try:
                df = pd.read_parquet(input_path)
                logger.info(f"  Successfully loaded Parquet.")
                load_successful = True
            except Exception as load_err:
                logger.error(f"  Error loading Parquet file {input_path}: {load_err}")
                return False
        
        if not load_successful or df is None: # Additional check
            logger.error(f"  DataFrame was not loaded for file: {input_path}")
            return False
        
        # Check for strange parsing (one column with \t in name) - as a signal of a problem
        if file_type == "csv" and df.shape[1] == 1 and '\t' in str(df.columns[0]):
            logger.warning(f"  Detected only one column with name '{df.columns[0]}'. "
                          f"Likely incorrect CSV delimiter specified (delimiter='{csv_delimiter}'). "
                          f"Try running with --csv-delimiter '\\t'.")
            # Could decide to abort processing this file or continue as is
            # return False # Uncomment if we want to stop processing such files
        
        if df.empty:
            logger.warning(f"  File is empty or became empty after loading, skipping cleaning: {input_path}")
            # Decide whether to save empty files. For now, don't save them.
            # If you need to save empty files, create an empty file at output_path
            # open(output_path, 'w').close() # Example for CSV
            return True # Consider it a "success" since there's nothing to process
        
        original_shape = df.shape
        logger.info(f"  Original size: {original_shape}")

        # --- Step 1: Duplicate handling ---
        if handle_duplicates == 'remove':
            rows_before_drop = df.shape[0]
            df.drop_duplicates(inplace=True)
            duplicates_removed = rows_before_drop - df.shape[0]
            if duplicates_removed > 0:
                logger.info(f"  Duplicates removed: {duplicates_removed}. Size after: {df.shape}")
            else:
                logger.info(f"  No duplicates found.")
        elif handle_duplicates == 'none':
            logger.info(f"  Duplicate handling skipped (as per --handle-duplicates=none).")
        else:
            logger.warning(f"  Unknown action for duplicates: {handle_duplicates}")
        
        
        if df.empty:
            logger.warning(f"  DataFrame became empty after removing duplicates. NOT saving: {output_path}")
            return True

        # --- Step 2: NaN handling ---
        nan_before = df.isnull().sum().sum()
        if nan_before > 0:
            logger.info(f"  NaN values detected: {nan_before}")
            if handle_nan == 'ffill':
                df.fillna(method='ffill', inplace=True)
                # After ffill, NaN values may remain at the beginning. Fill them backward.
                nan_after_ffill = df.isnull().sum().sum()
                if nan_after_ffill > 0:
                    logger.info(f"    NaN after ffill: {nan_after_ffill}. Applying bfill...")
                    df.fillna(method='bfill', inplace=True)
                nan_after_bfill = df.isnull().sum().sum()
                logger.info(f"  Applied NaN strategy: 'ffill' (with subsequent 'bfill'). NaN after: {nan_after_bfill}")
            elif handle_nan == 'dropna_rows':
                rows_before_dropna = df.shape[0]
                df.dropna(axis=0, inplace=True)
                rows_removed = rows_before_dropna - df.shape[0]
                logger.info(f"  Applied NaN strategy: 'dropna_rows'. Rows removed: {rows_removed}. NaN after: {df.isnull().sum().sum()}")
            elif handle_nan == 'none':
                logger.info(f"  NaN handling skipped (as per --handle-nan=none).")
            else:
                logger.warning(f"  Unknown NaN handling strategy: '{handle_nan}'. NaN values NOT processed.")
            logger.info(f"  Size after NaN handling: {df.shape}")
        else:
            logger.info(f"  No missing values (NaN) found.")

        # --- Saving results ---
        if df.empty:
            logger.warning(f"  DataFrame became empty after full cleaning. NOT saving: {output_path}")
            return True # Consider it successful, as cleaning is complete
        
        logger.info(f"  Saving cleaned file to: {output_path}")
        if file_type == "csv":
            # Save CSV with the same delimiter as read? Or always comma?
            # For now, save with comma as standard. Specify index=False
            df.to_csv(output_path, index=False, sep=',')
        else: # parquet
            df.to_parquet(output_path, index=False)
        
        logger.info(f"  File successfully saved.")
        return True
        
    except Exception as e:
        logger.error(f"Critical error processing file {input_path}: {e}", exc_info=True) # exc_info for traceback
        return False

# --- Helper function for header parsing ---
def parse_header(value: str) -> Optional[int]:
    if value.lower() == 'infer' or value.lower() == 'none':
        return None
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Value for --csv-header must be an integer or 'infer'. Received: '{value}'")

# --- Main function ---
def main():
    parser = argparse.ArgumentParser(
        description="Clean CSV and Parquet data: remove duplicates and handle NaN with customizable CSV parsing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Shows default values in --help
    )
    parser.add_argument(
        "-i", "--input-dirs",
        nargs='+',
        required=True, # Input directories are required
        help="List of SOURCE directories for recursive search of .csv and .parquet files."
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=True, # Output directory is required
        help="Base OUTPUT directory for saving cleaned files (preserves subfolder structure)."
    )
    parser.add_argument(
        "--handle-duplicates",
        default="remove",
        choices=['remove', 'none'],
        help="Action for complete row duplicates."
    )
    parser.add_argument(
        "--handle-nan",
        default="ffill",
        choices=['ffill', 'dropna_rows', 'none'],
        help="NaN handling strategy: 'ffill' (forward+backward fill), 'dropna_rows' (remove rows with NaN), 'none' (don't process)."
    )
    parser.add_argument(
        "--csv-delimiter",
        default=",",
        help="Delimiter for reading CSV files. Use '\\t' for tab."
    )
    parser.add_argument(
        "--csv-header",
        default='infer',
        type=str, # Read as string, then convert
        help="Header row in CSV files (0-based index) or 'infer' for auto-detection."
    )
    parser.add_argument(
        "--log-file",
        default="data_cleaner_v2.log",
        help="Log file name for recording the cleaning process."
    )
    # parser.add_argument( # Overwrite option - removed for now, overwriting by default in output_dir
    #     "--overwrite",
    #     action='store_true',
    #     help="Allow overwriting files in the output directory if they already exist."
    # )

    args = parser.parse_args()

    # Decode special characters in the delimiter (e.g., '\t')
    try:
        args.csv_delimiter = args.csv_delimiter.encode().decode('unicode_escape')
    except Exception as e:
        print(f"Error decoding CSV delimiter '{args.csv_delimiter}': {e}")
        sys.exit(1)
    
    
    # Convert csv_header argument
    try:
        parsed_header = parse_header(args.csv_header)
    except argparse.ArgumentTypeError as e:
        print(e)
        sys.exit(1)
    
    
    # Set up the logger
    global logger
    logger = setup_logger(args.log_file)
    
    logger.info("--- Starting data cleaner script v2 ---")
    logger.info(f"Source directories: {args.input_dirs}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Handling duplicates: {args.handle_duplicates}")
    logger.info(f"Handling NaN: {args.handle_nan}")
    logger.info(f"CSV delimiter: '{args.csv_delimiter}'")
    logger.info(f"CSV header: {parsed_header} (from '{args.csv_header}')")
    logger.info(f"Log file: {args.log_file}")

    # Check if output directory exists (don't create it here, clean_file will create subfolders)
    # But it's useful to check if it's not a file
    if os.path.exists(args.output_dir) and not os.path.isdir(args.output_dir):
        logger.error(f"Output directory path '{args.output_dir}' exists but is not a directory!")
        print(f"Error: Output directory path '{args.output_dir}' exists but is not a directory!")
        sys.exit(1)
    
    data_files = find_data_files(args.input_dirs)
    
    if not data_files:
        logger.warning("No .csv or .parquet files found for processing in the specified directories.")
        print("No files found for processing.")
        return
    
    logger.info(f"Found files for processing: {len(data_files)}")
    
    success_count = 0
    error_count = 0
    
    # Clear any previous output
    print("\033[K", end="\r")
    
    with tqdm(total=len(data_files), desc="Cleaning files", unit="file", position=0, leave=True) as pbar:
        for file_path, input_base in data_files:
            # Clear line before status update to avoid overlapping text
            print("\033[K", end="\r")
            
            if clean_file(
                input_path=file_path,
                input_base_dir=input_base,
                output_base_dir=args.output_dir,
                handle_duplicates=args.handle_duplicates,
                handle_nan=args.handle_nan,
                csv_delimiter=args.csv_delimiter,
                csv_header=parsed_header
            ):
                success_count += 1
            else:
                error_count += 1
            pbar.update(1)
    
    logger.info("--- Data cleaner script v2 completed ---")
    logger.info(f"Successfully processed/saved: {success_count}")
    logger.info(f"Errors during processing: {error_count}")
    
    # Clear line to ensure clean output after progress bar
    print("\033[K", end="\r")
    print(f"\nCleaning completed. Success: {success_count}, Errors: {error_count}. Log: {args.log_file}")
    if error_count > 0:
        print("Warning: Errors occurred during processing. Check the log for details.")

if __name__ == "__main__":
    main()
