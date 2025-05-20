# -*- coding: utf-8 -*-
# scripts/data_processing/data_cleaner_v2.py

import os
import argparse
import logging
from typing import List, Tuple, Optional, Union
import pandas as pd
from tqdm import tqdm
import sys # For exiting on critical errors

# Global logger
logger = None

# --- Logging Configuration ---
def setup_logger(log_file: str, verbose: bool = False) -> logging.Logger:
    """Set up logging to both file and console.
    
    Args:
        log_file (str): Path to log file.
        verbose (bool, optional): Enable verbose (DEBUG level) logging. Defaults to False.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    global logger
    if logger is not None:
        return logger

    logger = logging.getLogger('data_cleaner')
    
    # Set logger level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()
    
    # File handler always logs at DEBUG level
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler level depends on verbose flag
    if verbose:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    if verbose:
        logger.debug("Verbose logging enabled")

    return logger

# --- File Processing Functions ---
def find_data_files(base_folders: List[str]) -> List[Tuple[str, str]]:
    """Find all CSV and Parquet files in the base folders."""
    global logger
    if logger is None:
        raise RuntimeError("Logger not initialized. Call setup_logger first.")

    result = []
    for base_folder in base_folders:
        abs_base_folder = os.path.abspath(base_folder)
        logger.info(f"Searching files in: {abs_base_folder}")
        
        for root, _, files in os.walk(abs_base_folder):
            # Skip output directories
            if os.path.basename(root) == "output":
                continue
            
            for file in files:
                if file.endswith(('.csv', '.parquet')) and file != "empty.csv":
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, abs_base_folder)
                    result.append((abs_path, rel_path))
                    logger.info(f"Found file: {rel_path}")
    
    return result

def clean_file(
    input_path: str,
    input_base_dir: str,
    output_base_dir: str,
    handle_duplicates: str = "remove",
    handle_nan: str = "ffill",
    csv_delimiter: str = ",",
    csv_header: Union[int, str, None] = 0
) -> bool:
    """Clean a single data file."""
    global logger
    if logger is None:
        raise RuntimeError("Logger not initialized. Call setup_logger first.")

    logger.info(f"Processing file: {input_path}")
    file_type = None

    try:
        # Determine file type
        if input_path.lower().endswith('.csv'):
            file_type = 'csv'
            try:
                df = pd.read_csv(input_path, delimiter=csv_delimiter, header=csv_header)
                logger.info(f"  Successfully loaded CSV: delimiter='{csv_delimiter}', header={csv_header}")
            except pd.errors.EmptyDataError:
                logger.info("  Empty DataFrame detected, skipping processing")
                return True
        elif input_path.lower().endswith('.parquet'):
            file_type = 'parquet'
            df = pd.read_parquet(input_path)
            logger.info("  Successfully loaded Parquet.")
        else:
            logger.error(f"Unsupported file type (logic error): {input_path}")
            return False

        # Log original size
        logger.info(f"  Original size: {df.shape}")

        # Handle empty DataFrame
        if df.empty:
            logger.info("  Empty DataFrame detected, skipping processing")
            return True

        # Handle duplicates first
        if handle_duplicates == "remove":
            original_len = len(df)
            df = df.drop_duplicates()  # By default, considers all columns and keeps first occurrence
            duplicates_removed = original_len - len(df)
            logger.info(f"  Duplicates removed: {duplicates_removed}. Size after: {df.shape}")

        # Handle NaN values
        nan_count = df.isna().sum().sum()
        if nan_count > 0:
            logger.info(f"  NaN values detected: {nan_count}")
            if handle_nan == "ffill":
                df = df.ffill().bfill()  # Use non-deprecated methods
                logger.info("  Applied NaN strategy: 'ffill' (with subsequent 'bfill'). NaN after: 0")
                # Remove any duplicates that might have been created by NaN handling
                if handle_duplicates == "remove":
                    original_len = len(df)
                    df = df.drop_duplicates()
                    duplicates_removed = original_len - len(df)
                    if duplicates_removed > 0:
                        logger.info(f"  Additional duplicates removed after NaN handling: {duplicates_removed}. Size after: {df.shape}")
            elif handle_nan == "dropna_rows":
                original_len = len(df)
                df = df.dropna()
                rows_removed = original_len - len(df)
                logger.info(f"  Applied NaN strategy: 'dropna_rows'. Rows removed: {rows_removed}. NaN after: 0")
            else:
                logger.info("  NaN handling skipped (as per --handle-nan=none).")
        logger.info(f"  Size after NaN handling: {df.shape}")

        # --- Ensure date column is preserved and set as DatetimeIndex ---
        date_col_candidates = [col for col in df.columns if col.lower() in ['timestamp', 'datetime', 'date', 'datetime_']]
        if not date_col_candidates:
            # If index is DatetimeIndex, reset it to a column
            if isinstance(df.index, pd.DatetimeIndex):
                df = df.reset_index()
                date_col_candidates = [col for col in df.columns if col.lower() in ['timestamp', 'datetime', 'date', 'datetime_']]
        # Always keep the first found date column at the front and set as DatetimeIndex
        if date_col_candidates:
            date_col = date_col_candidates[0]
            # Move date column to front if not already
            cols = list(df.columns)
            if cols[0] != date_col:
                cols.insert(0, cols.pop(cols.index(date_col)))
                df = df[cols]
            # Convert to datetime and set as index if not already
            if not isinstance(df.index, pd.DatetimeIndex) or df.index.name != date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.set_index(date_col)
                # Do NOT drop the date_col from columns after set_index, so it will be preserved in output

        # Create output path based on file type
        output_filename = os.path.basename(input_path)
        
        # Handle file path differently depending on file type and filename pattern
        if file_type == 'csv':
            # For CSV files, check if they came from csv_converted directory
            if "csv_converted" in input_path:
                # Save to output_base_dir/cache/csv_converted
                output_dir = os.path.join(output_base_dir, "cache", "csv_converted")
            else:
                # Other CSV files save to raw_parquet
                output_dir = os.path.join(output_base_dir, "raw_parquet")
        else:  # parquet
            # For Parquet files with CSVExport_ prefix, save to cache/csv_converted
            if output_filename.startswith("CSVExport_"):
                output_dir = os.path.join(output_base_dir, "cache", "csv_converted")
                logger.info(f"  CSVExport parquet file detected, saving to csv_converted directory")
            else:
                # For other Parquet files - save to output_base_dir/raw_parquet
                output_dir = os.path.join(output_base_dir, "raw_parquet")
        
        output_path = os.path.join(output_dir, output_filename)
        
        # Create output directory structure if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)  # Create subdirectory
        
        logger.debug(f"Saving to output directory: {output_dir}")
        logger.debug(f"Full output path: {output_path}")

        # Save cleaned file
        logger.info(f"  Saving cleaned file to: {output_path}")
        try:
            if file_type == 'csv':
                df.to_csv(output_path, index=False)
                logger.debug(f"Successfully wrote CSV file with shape {df.shape}")
            else:  # parquet
                df.to_parquet(output_path, index=False)
                logger.debug(f"Successfully wrote Parquet file with shape {df.shape}")
            
            logger.info(f"  File successfully saved to {output_dir}")
            
            # Verify file exists after saving
            if os.path.exists(output_path):
                logger.debug(f"Verified file exists at: {output_path}")
            else:
                logger.error(f"File was not created at: {output_path}")
        except Exception as e:
            logger.error(f"Error saving file to {output_path}: {str(e)}")
            return False

        return True

    except Exception as e:
        logger.error(f"  Error loading {file_type} file {input_path} with delimiter='{csv_delimiter}' header={csv_header}: {str(e)}")
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
        "--verbose",
        action="store_true",
        help="Enable verbose output"
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
    logger = setup_logger(args.log_file, verbose=args.verbose)
    
    logger.info("--- Starting data cleaner script v2 ---")
    logger.info(f"Source directories: {args.input_dirs}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Files will be saved to: {os.path.join(args.output_dir, 'raw_parquet')} (most parquet files + standard csv files)")
    logger.info(f"                      : {os.path.join(args.output_dir, 'cache/csv_converted')} (csv files from csv_converted + CSVExport_*.parquet files)")
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
