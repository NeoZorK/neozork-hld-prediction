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
    Reads metadata (row count, columns, first/last row with all fields) from a Parquet file.

    Args:
        file_path: Path to the Parquet file.

    Returns:
        A dictionary containing metadata: 'num_rows', 'columns', 'first_row', 'last_row'.
        Returns default values (e.g., -1 or None) if metadata cannot be read.
    """
    metadata = {'num_rows': -1, 'columns': [], 'first_row': None, 'last_row': None, 'first_date': None, 'last_date': None}
    try:
        parquet_file = pq.ParquetFile(file_path)
        metadata['num_rows'] = parquet_file.metadata.num_rows
        metadata['columns'] = parquet_file.schema.names

        # Read first and last row with all fields
        if metadata['num_rows'] > 0:
            # Read the first row with all columns
            # Note: pd.read_parquet doesn't support nrows, so we use head(1)
            df_head = pd.read_parquet(file_path).head(1)
            if not df_head.empty:
                metadata['first_row'] = df_head.iloc[0]
                # Keep first_date for backward compatibility
                metadata['first_date'] = df_head.index[0] if isinstance(df_head.index, pd.DatetimeIndex) else df_head.iloc[0, 0]
            
            # Read the last row if there's more than one row
            if metadata['num_rows'] > 1:
                # For the last row, we'll read the whole file but only take the last row
                # This is not very efficient for large files, but it's a simple approach
                df_tail = pd.read_parquet(file_path).tail(1)
                if not df_tail.empty:
                    metadata['last_row'] = df_tail.iloc[0]
                    # Keep last_date for backward compatibility
                    metadata['last_date'] = df_tail.index[0] if isinstance(df_tail.index, pd.DatetimeIndex) else df_tail.iloc[0, 0]
            elif metadata['num_rows'] == 1:  # If only one row, first and last are the same
                metadata['last_row'] = metadata['first_row']
                metadata['last_date'] = metadata['first_date']

    except Exception as e:
        print(f"Warning: Could not read metadata for {file_path.name}. Error: {e}", file=sys.stderr)
        # Don't print full traceback to reduce console output noise
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
            
            # Extract and format dates from first and last rows
            first_date = None
            last_date = None
            
            # Format first date/time if available
            if file_info['first_date'] is not None:
                if isinstance(file_info['first_date'], pd.Timestamp):
                    first_date = file_info['first_date'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    first_date = str(file_info['first_date'])
                
            # Format last date/time if available
            if file_info['last_date'] is not None:
                if isinstance(file_info['last_date'], pd.Timestamp):
                    last_date = file_info['last_date'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    last_date = str(file_info['last_date'])
            
            # Print date range summary
            if first_date and last_date and first_date != last_date:
                print(f"    Date Range: {first_date} → {last_date}")
            elif first_date:
                print(f"    Date: {first_date}")
            
            # Display first row in a compact format
            if file_info['first_row'] is not None:
                print(f"    First Row: ", end="")
                # If it's a Series object, display it nicely in a single line
                if isinstance(file_info['first_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['first_row'].items():
                        # Format timestamps nicely
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    print(" | ".join(values))
                else:
                    print(f"{file_info['first_row']}")
            
            # Display last row in a compact format (if different from first)
            if file_info['last_row'] is not None and file_info['num_rows'] > 1:
                print(f"    Last Row:  ", end="")
                # If it's a Series object, display it nicely in a single line
                if isinstance(file_info['last_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['last_row'].items():
                        # Format timestamps nicely
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    print(" | ".join(values))
                else:
                    print(f"{file_info['last_row']}")

    print("-" * 40) # Separator

    # Print hint or trigger plot
    if len(found_files) > 1:
        print("To display a chart, re-run the command with more specific keywords:")
        print(f"Example: python run_analysis.py show {args.source} <additional_keywords>")
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