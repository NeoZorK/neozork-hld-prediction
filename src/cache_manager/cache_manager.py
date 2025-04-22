# src/cache_manager/cache_manager.py

"""
Manages cached data files (Parquet format) for different data sources.
Provides functions to find, list, and load cached data.
"""

import pandas as pd
from pathlib import Path
import traceback
from typing import List, Dict, Optional, Tuple

# Use relative imports for logger and constants
from ..common import logger
from ..common.constants import VALID_DATA_SOURCES # yf, polygon, binance

# Define base directories for cache
# Assuming script is run from the root directory containing 'src'
BASE_DIR = Path(__file__).resolve().parent.parent.parent # Should point to NeoZorK HLD root
CSV_CACHE_DIR = BASE_DIR / "data" / "cache" / "csv_converted"
API_CACHE_DIR = BASE_DIR / "data" / "raw_parquet"

# Define expected source types for API cache directory structure
API_SOURCE_FOLDERS = {
    'yfinance': API_CACHE_DIR / 'yfinance',
    'polygon': API_CACHE_DIR / 'polygon',
    'binance': API_CACHE_DIR / 'binance',
}

# Function to safely get file size and modification time
def get_file_metadata(file_path: Path) -> Tuple[Optional[float], Optional[pd.Timestamp]]:
    """Gets file size in MB and last modified time."""
    try:
        size_bytes = file_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        mtime_ts = pd.to_datetime(file_path.stat().st_mtime_ns, unit='ns')
        return size_mb, mtime_ts
    except OSError as e:
        logger.print_warning(f"Could not get metadata for {file_path}: {e}")
        return None, None

# Function to parse filename for metadata (example implementation)
def parse_filename(filename: str, source_type: str) -> Dict[str, str]:
    """
    Attempts to parse metadata (ticker, interval, etc.) from a filename.
    This needs refinement based on actual filename conventions.
    """
    parts = filename.replace('.parquet', '').split('_')
    metadata = {'filename': filename, 'source': source_type}
    # Very basic parsing - needs improvement based on real filenames
    if source_type == 'csv':
        # Example: CSVExport_XAUUSD_PERIOD_MN1_pt0.01_1000rows.parquet
        if len(parts) > 2:
            metadata['original_csv'] = parts[0] + "_" + parts[1] # Reconstruct original name part
            metadata['ticker'] = parts[1] if len(parts) > 1 else 'Unknown'
            metadata['interval'] = parts[3] if len(parts) > 3 else 'Unknown' # Assuming PERIOD_ is always there
            # Try to find point size if included
            for part in parts:
                 if part.startswith('pt'):
                      metadata['point_size'] = part.replace('pt','')
    elif source_type in API_SOURCE_FOLDERS:
         # Example: yfinance_AAPL_D1.parquet or polygon_EURUSD_M1.parquet
         if len(parts) >= 3:
              metadata['ticker'] = parts[1]
              metadata['interval'] = parts[2]
         elif len(parts) == 2: # Maybe just ticker?
              metadata['ticker'] = parts[1]
              metadata['interval'] = 'Unknown'

    return metadata


# Function to find cached files
def find_cached_files(source_type: str, search_terms: Optional[List[str]] = None) -> List[Dict[str, any]]:
    """
    Finds cached Parquet files for a given source, optionally filtering by search terms.

    Args:
        source_type (str): The data source ('csv', 'yfinance', 'polygon', 'binance').
        search_terms (Optional[List[str]]): A list of terms to filter filenames by.
                                             All terms must be present in the filename.

    Returns:
        List[Dict[str, any]]: A list of dictionaries, each containing metadata
                               about a found file (path, size, mtime, parsed info).
                               Returns an empty list if the directory doesn't exist or no files match.
    """
    found_files_info = []
    cache_dir = None

    if source_type == 'csv':
        cache_dir = CSV_CACHE_DIR
    elif source_type in API_SOURCE_FOLDERS:
        cache_dir = API_SOURCE_FOLDERS.get(source_type)
    else:
        logger.print_error(f"Invalid source type '{source_type}' for cache search.")
        return found_files_info # Return empty list

    if not cache_dir or not cache_dir.exists() or not cache_dir.is_dir():
        logger.print_warning(f"Cache directory for '{source_type}' not found or is not a directory: {cache_dir}")
        return found_files_info # Return empty list

    logger.print_info(f"Searching for '{source_type}' cache files in: {cache_dir}")
    if search_terms:
         logger.print_info(f"Filtering by terms: {search_terms}")

    # Use rglob to find all .parquet files recursively (might be needed for API cache)
    # If structure is flat, glob('*.parquet') is enough. Assuming flat for now.
    # Use glob for potentially better performance if dirs are known to be flat
    file_pattern = "*.parquet"
    cached_files = list(cache_dir.glob(file_pattern))

    if not cached_files:
         logger.print_warning(f"No Parquet files found in {cache_dir}")
         return found_files_info

    for file_path in cached_files:
        filename = file_path.name
        # Apply search terms filter
        if search_terms:
            # Check if all search terms are in the filename (case-insensitive)
            if not all(term.lower() in filename.lower() for term in search_terms):
                continue # Skip this file if not all terms match

        # Get metadata
        size_mb, mtime = get_file_metadata(file_path)
        parsed_info = parse_filename(filename, source_type)

        file_info = {
            'path': file_path,
            'filename': filename,
            'size_mb': size_mb,
            'modified_time': mtime,
            **parsed_info # Add parsed metadata
        }
        found_files_info.append(file_info)

    logger.print_info(f"Found {len(found_files_info)} matching file(s).")
    return found_files_info


# Function to load a specific cached file
def load_cached_file(file_path: Path) -> Optional[pd.DataFrame]:
    """
    Loads data from a specific Parquet cache file.

    Args:
        file_path (Path): The absolute path to the Parquet file.

    Returns:
        Optional[pd.DataFrame]: Loaded DataFrame, or None if loading fails.
    """
    if not file_path.exists() or not file_path.is_file():
        logger.print_error(f"Cache file not found or is not a file: {file_path}")
        return None

    logger.print_info(f"Loading data from cached file: {file_path.name}")
    try:
        df = pd.read_parquet(file_path)
        logger.print_success(f"Successfully loaded {len(df)} rows from {file_path.name}")
        # Basic validation (ensure datetime index if expected)
        if not isinstance(df.index, pd.DatetimeIndex):
             logger.print_warning("Loaded DataFrame does not have a DatetimeIndex.")
             # Attempt conversion? Or rely on downstream code?
             try:
                  df.index = pd.to_datetime(df.index)
                  logger.print_info("Converted index to DatetimeIndex.")
             except Exception as e:
                  logger.print_error(f"Failed to convert index to DatetimeIndex: {e}")
        return df
    except Exception as e:
        logger.print_error(f"Failed to load Parquet file {file_path}: {type(e).__name__}: {e}")
        logger.print_debug(f"Traceback (load cache):\n{traceback.format_exc()}")
        return None


# Function to display cached file info using Rich table
def display_cached_files_info(files_info: List[Dict[str, any]]):
    """
    Displays information about found cached files in a formatted table.

    Args:
        files_info (List[Dict[str, any]]): List of file metadata dictionaries
                                            from find_cached_files.
    """
    if not files_info:
        logger.print_info("No cached files to display.")
        return

    try:
        from rich.table import Table
        from rich.console import Console
    except ImportError:
        logger.print_warning("'rich' library not installed. Displaying basic list.")
        logger.print_info("Install with: pip install rich")
        for i, info in enumerate(files_info):
            print(f"{i+1}. {info.get('filename', 'N/A')} "
                  f"(Size: {info.get('size_mb', '?'):.2f} MB, "
                  f"Modified: {info.get('modified_time', 'N/A')})")
        return

    console = Console()
    table = Table(title="Cached Data Files", show_header=True, header_style="bold magenta")

    # Define columns dynamically based on available keys, prioritizing common ones
    # Get all unique keys from all file info dicts, except 'path'
    all_keys = set(key for info in files_info for key in info if key != 'path')
    # Define preferred order
    preferred_order = ['filename', 'ticker', 'interval', 'source', 'size_mb', 'modified_time', 'point_size', 'original_csv']
    # Create ordered columns based on preference and availability
    columns = [key for key in preferred_order if key in all_keys] + sorted([key for key in all_keys if key not in preferred_order])

    table.add_column("#", style="dim", width=4, justify="right")
    for key in columns:
        # Customize column headers and styles
        header = key.replace('_', ' ').title()
        style = "dim" if key in ['filename', 'original_csv'] else None
        justify = "right" if key == 'size_mb' else "left"
        no_wrap = False # key not in ['filename', 'original_csv'] # Avoid wrapping for most
        table.add_column(header, style=style, justify=justify, no_wrap=no_wrap)


    # Add rows
    for idx, info in enumerate(files_info):
        row_data = [str(idx + 1)]
        for key in columns:
            value = info.get(key)
            # Format specific columns
            if key == 'size_mb' and value is not None:
                formatted_value = f"{value:.2f} MB"
            elif key == 'modified_time' and value is not None and isinstance(value, pd.Timestamp):
                 # Format timestamp for readability
                 formatted_value = value.strftime('%Y-%m-%d %H:%M')
            elif value is None:
                 formatted_value = "-" # Display hyphen for missing values
            else:
                 formatted_value = str(value)
            row_data.append(formatted_value)
        table.add_row(*row_data)

    console.print(table)

