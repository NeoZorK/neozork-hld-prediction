# src/core/show_mode.py

import os
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd # We might need pandas later for date parsing if reading rows
import sys
import traceback

# To avoid circular imports when workflow.py imports this
# This way we'll be importing generate_plot only when we actually call it
def import_generate_plot():
    from ..plotting.plotting_generation import generate_plot
    return generate_plot

# Define the directories to search
SEARCH_DIRS = [
    Path("data/raw_parquet"),
    Path("data/cache/csv_converted")
]

def get_parquet_metadata(file_path: Path) -> dict:
    """
    Reads metadata (row count, columns, first/last row dates if possible) from a Parquet file.

    Args:
        file_path: Path to the Parquet file.

    Returns:
        A dictionary containing metadata: 'num_rows', 'columns', 'first_date', 'last_date'.
        Returns default values (e.g., -1 or None) if metadata cannot be read.
    """
    metadata = {'num_rows': -1, 'columns': [], 'first_date': None, 'last_date': None}
    try:
        parquet_file = pq.ParquetFile(file_path)
        metadata['num_rows'] = parquet_file.metadata.num_rows
        metadata['columns'] = parquet_file.schema.names

        # Try to read first and last row efficiently for dates (assuming a 'Date' or index)
        # This might be slow for very large files, consider optimizing if needed.
        # Reading only specific columns ('Date' if it exists) might be better.
        # For now, we try reading the head and tail.
        if metadata['num_rows'] > 0:
            df_head = pd.read_parquet(file_path, columns=metadata['columns'][:1]) # Read first column of first row
            if not df_head.empty:
                 # Try getting the first index value (often a date)
                 metadata['first_date'] = df_head.index[0] if isinstance(df_head.index, pd.DatetimeIndex) else df_head.iloc[0, 0]

            # To get the last date efficiently without reading the whole file,
            # we might need to rely on row group statistics if available and sorted,
            # or read just the last row group, or read the tail. Reading tail is simpler for now.
            if metadata['num_rows'] > 1:
                 # This reads the necessary row groups to get the tail.
                 df_tail = pd.read_parquet(file_path, columns=metadata['columns'][:1]) # Read first column of last row
                 if not df_tail.empty:
                      metadata['last_date'] = df_tail.index[-1] if isinstance(df_tail.index, pd.DatetimeIndex) else df_tail.iloc[-1, 0]
            elif metadata['num_rows'] == 1: # If only one row, first and last date are the same
                 metadata['last_date'] = metadata['first_date']


    except Exception as e:
        print(f"Warning: Could not read metadata for {file_path.name}. Error: {e}", file=sys.stderr) # Use sys.stderr
    return metadata


def handle_show_mode(args):
    """
    Handles the 'show' mode logic: finds files, displays info, and potentially triggers plot.

    Args:
        args: The parsed command-line arguments from argparse.
    """
    print(f"Searching for '{args.source}' files with keywords: {args.keywords}...")

    # Normalize source 'yf' to 'yfinance' for matching filenames like 'yfinance_...'
    search_prefix = 'yfinance' if args.source == 'yf' else args.source
    search_keywords = [k.lower() for k in args.keywords]

    found_files = []
    for search_dir in SEARCH_DIRS:
        if not search_dir.is_dir():
            print(f"Warning: Directory not found: {search_dir}")
            continue

        for item in search_dir.iterdir():
            # Check if it's a file, ends with .parquet, and starts with the source prefix
            if item.is_file() and item.suffix == '.parquet' and item.name.lower().startswith(search_prefix + '_'):
                # Check if all keywords are present in the filename (case-insensitive)
                filename_lower = item.name.lower()
                if all(keyword in filename_lower for keyword in search_keywords):
                    try:
                        file_size_bytes = item.stat().st_size
                        file_size_mb = file_size_bytes / (1024 * 1024)
                        found_files.append({
                            'path': item,
                            'name': item.name,
                            'size_mb': file_size_mb
                        })
                    except OSError as e:
                         print(f"Warning: Could not get stats for file {item.name}. Error: {e}", file=sys.stderr)


    print(f"Found {len(found_files)} file(s).")

    if not found_files:
        return # Exit if no files found

    # Sort files by name for consistent listing
    found_files.sort(key=lambda x: x['name'])

    # Get metadata and print list
    print("-" * 40) # Separator
    for idx, file_info in enumerate(found_files):
        metadata = get_parquet_metadata(file_info['path'])
        file_info.update(metadata) # Add metadata to the dict
        print(f"[{idx}] {file_info['name']}")
        print(f"    Size: {file_info['size_mb']:.3f} MB")
        if metadata['num_rows'] != -1:
            print(f"    Rows: {file_info['num_rows']:,}") # Formatted number
        else:
            print(f"    Rows: Could not determine")

        # Print extra info only if exactly one file is found
        if len(found_files) == 1:
             print(f"    Columns ({len(file_info['columns'])}): {', '.join(file_info['columns'])}")
             # Format dates nicely if they are pandas Timestamps
             first_date_str = str(file_info['first_date'])
             last_date_str = str(file_info['last_date'])
             if isinstance(file_info['first_date'], pd.Timestamp):
                 first_date_str = file_info['first_date'].strftime('%Y-%m-%d %H:%M:%S') if file_info['first_date'] else "N/A"
             if isinstance(file_info['last_date'], pd.Timestamp):
                 last_date_str = file_info['last_date'].strftime('%Y-%m-%d %H:%M:%S') if file_info['last_date'] else "N/A"

             print(f"    First Entry Date: {first_date_str}")
             print(f"    Last Entry Date: {last_date_str}")

    print("-" * 40) # Separator

    # Print hint or trigger plot
    if len(found_files) > 1:
        print("To display a chart, re-run the command specifying the file index or full name:")
        print(f"Example: python run_analysis.py <plot_mode> --file <filename_or_index> ...") # Adjust this command structure later
    elif len(found_files) == 1:
        print(f"Found one file. Triggering plot with method: '{args.draw}'...")
        # Call the plotting function for the found file
        print(f"Loading file data and triggering plot with method: '{args.draw}'...")
        
        try:
            # Read the parquet file into a dataframe
            df = pd.read_parquet(found_files[0]['path'])
            
            # Create a minimal data_info dict for generate_plot
            data_info = {
                "ohlcv_df": df,
                "data_source_label": f"Parquet file: {found_files[0]['name']}",
                "rows_count": len(df),
                "columns_count": len(df.columns),
                "data_size_mb": found_files[0]['size_mb'],
                "first_date": found_files[0]['first_date'],
                "last_date": found_files[0]['last_date'],
                "parquet_cache_used": True,
                "parquet_cache_file": str(found_files[0]['path'])
            }
            
            # Try to extract point size from filename if possible
            point_size = None
            if 'point' in found_files[0]['name'].lower():
                try:
                    # Extract the point size value if filename contains pattern like "point_0.01"
                    name_parts = found_files[0]['name'].lower().split('point_')
                    if len(name_parts) > 1:
                        possible_point = name_parts[1].split('_')[0]
                        point_size = float(possible_point)
                except (ValueError, IndexError):
                    pass
            
            # Default point size if we couldn't extract it
            if point_size is None:
                # Common defaults based on asset types
                if 'forex' in found_files[0]['name'].lower() or 'fx' in found_files[0]['name'].lower():
                    point_size = 0.00001  # Common for forex
                elif 'btc' in found_files[0]['name'].lower() or 'crypto' in found_files[0]['name'].lower():
                    point_size = 0.01  # Common for crypto
                else:
                    point_size = 0.01  # Default for stocks and other assets
                
                print(f"Point size not found in filename, using default: {point_size}")
            
            # Import here to avoid circular imports
            generate_plot = import_generate_plot()
            
            # No result_df, we're just plotting the raw data
            result_df = None
            selected_rule = args.rule if hasattr(args, 'rule') else 'Predict_High_Low_Direction'
            estimated_point = True
            
            # Call generate_plot with the necessary parameters
            generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
            
            print(f"Successfully plotted data from '{found_files[0]['name']}'")
            
        except Exception as e:
            print(f"Error plotting file: {e}")
            traceback.print_exc()


# Все необходимые импорты уже выполнены вверху файла