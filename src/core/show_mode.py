# src/core/show_mode.py

import os
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd # We might need pandas later for date parsing if reading rows
import sys
import webbrowser
import traceback
from ..common import logger  # Import the logger module for consistent output
from ..indicator.indicator import calculate_indicator  # Import indicator calculator
from ..common.constants import TradingRule

def show_help():
    """Displays help for the 'show' mode."""
    logger.print_info("\n=== SHOW MODE HELP ===")
    logger.print_info("The 'show' mode allows you to list and inspect cached data files.")
    logger.print_info("Usage: python run_analysis.py show <source> [keywords...]")
    logger.print_info("\nAvailable sources:")
    logger.print_info("  - csv: Converted CSV data files")
    logger.print_info("  - yfinance/yf: Yahoo Finance data files")
    logger.print_info("  - polygon: Polygon.io data files")
    logger.print_info("  - binance: Binance data files")
    logger.print_info("\nWhen a single file is found with the filters, you can calculate the indicator:")
    logger.print_info("  python run_analysis.py show binance d1 eth")


def calculate_and_display_indicator(file_path, args, point_size=0.01):
    """
    Calculates the indicator for a single file and displays the results.
    
    Args:
        file_path: Path to the Parquet file
        args: Command-line arguments
        point_size: Point size for the instrument (default 0.01)
    
    Returns:
        DataFrame with the calculated indicator data
    """
    logger.print_info(f"Calculating indicator for: {os.path.basename(file_path)}")
    
    try:
        # Load data from Parquet file
        df = pq.read_table(file_path).to_pandas()
        logger.print_info(f"Loaded {len(df)} rows of data")
        
        # Ensure OHLCV columns are present and correctly named
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in df.columns:
                logger.print_error(f"Missing required column: {col}")
                return None
                
        # Determine which trading rule to use
        rule = None
        if hasattr(args, 'show_rule') and args.show_rule:
            # Convert rule name or alias to actual TradingRule enum value
            rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
            rule_name = rule_aliases_map.get(args.show_rule, args.show_rule)
            rule = TradingRule[rule_name]
        else:
            # Use default rule
            rule = TradingRule.Predict_High_Low_Direction
        
        logger.print_info(f"Using trading rule: {rule.name}")
        
        # Calculate the indicator
        result_df = calculate_indicator(
            df.copy(), 
            point_size=point_size,
            rule=rule
        )
        
        if result_df is None:
            logger.print_error("Failed to calculate indicator")
            return None
            
        # Display basic statistics about the calculated indicator
        logger.print_success(f"Successfully calculated indicator with {len(result_df)} rows")
        
        # Display indicator columns (those added during calculation)
        ohlcv_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
        indicator_cols = [col for col in result_df.columns if col not in ohlcv_cols]
        
        logger.print_info("Indicator columns:")
        for col in indicator_cols:
            logger.print_info(f"  - {col}")
        
        # Display a sample of the data with indicator values
        logger.print_info("\nSample data with indicator values:")
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.width', 1000)        # Wider display
        sample_cols = ['Date', 'Open', 'High', 'Low', 'Close'] + indicator_cols
        display_cols = [col for col in sample_cols if col in result_df.columns]
        logger.print_info(result_df[display_cols].head(10).to_string())
        
        return result_df
        
    except Exception as e:
        logger.print_error(f"Error calculating indicator: {str(e)}")
        traceback.print_exc()
        return None
    logger.print_info("  - polygon: Polygon.io API data files")
    logger.print_info("  - binance: Binance API data files")
    logger.print_info("\nExamples:")
    logger.print_info("  python run_analysis.py show                  # Show statistics for all sources")
    logger.print_info("  python run_analysis.py show yf               # List all Yahoo Finance files")
    logger.print_info("  python run_analysis.py show yf aapl          # List YF files containing 'aapl'")
    logger.print_info("  python run_analysis.py show binance btc MN1  # List Binance files with 'btc' and timeframe 'MN1'")

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

def count_files_by_source():
    """
    Counts Parquet files by their source prefix (yfinance, csv, polygon, binance).
    
    Returns:
        Dictionary with counts for each source type and additional stats.
    """
    source_counts = {
        'yfinance': 0,
        'csv': 0,
        'polygon': 0,
        'binance': 0,
        'other': 0,
        'csv_converted_count': 0  # Special counter for files in csv_converted folder
    }
    
    for search_dir in SEARCH_DIRS:
        if not search_dir.is_dir():
            continue
            
        for item in search_dir.iterdir():
            if item.is_file() and item.suffix == '.parquet':
                filename_lower = item.name.lower()
                
                # Check source prefix
                if filename_lower.startswith('yfinance_'):
                    source_counts['yfinance'] += 1
                elif filename_lower.startswith('csv_'):
                    source_counts['csv'] += 1
                    # Special counting of files in csv_converted folder
                    if 'csv_converted' in str(search_dir).lower():
                        source_counts['csv_converted_count'] += 1
                # Все файлы в папке csv_converted считаются CSV файлами независимо от их имени
                elif 'csv_converted' in str(search_dir).lower():
                    source_counts['csv'] += 1
                    source_counts['csv_converted_count'] += 1
                elif filename_lower.startswith('polygon_'):
                    source_counts['polygon'] += 1
                elif filename_lower.startswith('binance_'):
                    source_counts['binance'] += 1
                else:
                    source_counts['other'] += 1
                    
    return source_counts

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
        logger.print_warning(f"Could not read metadata for {file_path.name}. Error: {e}")
        # Don't print full traceback to reduce console output noise
    return metadata


def handle_show_mode(args):
    """
    Handles the 'show' mode logic: finds files, displays info, and potentially triggers plot.

    Args:
        args: The parsed command-line arguments from argparse.
    """
    # Show help and file statistics if no source is specified
    if not args.source or args.source == 'help':
        show_help()
        
        # Display stats about available files
        source_counts = count_files_by_source()
        
        logger.print_info("\n=== AVAILABLE DATA FILES ===")
        
        total_files = sum([count for source, count in source_counts.items() 
                          if source not in ['csv_converted_count']])
        
        if total_files == 0:
            logger.print_warning("No data files found. Use other modes to download or import data first.")
            logger.print_info("\nTo convert a CSV file, use the 'csv' mode:")
            logger.print_info("  python run_analysis.py csv --csv-file path/to/data.csv --point 0.01")
            return
            
        logger.print_info(f"Total cached data files: {total_files}")
        for source, count in source_counts.items():
            # Skip service counters output
            if source in ['csv_converted_count']:
                continue
                
            if count > 0:
                if source == 'csv':
                    csv_converted = source_counts.get('csv_converted_count', 0)
                    logger.print_info(f"  - {source.capitalize()}: {count} file(s) (including {csv_converted} converted from CSV)")
                elif source == 'other':
                    logger.print_info(f"  - Converted from CSV: {count} file(s)")
                else:
                    if source == 'other':
                        logger.print_info(f"  - Converted from CSV: {count} file(s)")
                    else:
                        logger.print_info(f"  - {source.capitalize()}: {count} file(s)")
                
        logger.print_info("\nTo view specific files, use: python run_analysis.py show <source> [keywords...]")
        return
        
    logger.print_info(f"Searching for '{args.source}' files with keywords: {args.keywords}...")

    # Normalize source 'yf' to 'yfinance' for matching filenames like 'yfinance_...'
    search_prefix = 'yfinance' if args.source == 'yf' else args.source
    search_keywords = [k.lower() for k in args.keywords]

    found_files = []
    for search_dir in SEARCH_DIRS:
        if not search_dir.is_dir():
            logger.print_warning(f"Directory not found: {search_dir}")
            continue
    
        for item in search_dir.iterdir():
            # Check if it's a file and ends with .parquet
            if item.is_file() and item.suffix == '.parquet':
                filename_lower = item.name.lower()
                
                # Special logic for CSV mode
                if search_prefix.lower() == 'csv':
                    # Show files that either start with 'csv_' or are located in the csv_converted folder
                    is_match = (filename_lower.startswith('csv_') or 
                               'csv_converted' in str(search_dir).lower())
                else:
                    # For other sources, check the prefix as usual
                    is_match = filename_lower.startswith(search_prefix.lower() + '_')
                
                # Check for match with search pattern and keywords
                if is_match and all(keyword in filename_lower for keyword in search_keywords):
                    try:
                        file_size_bytes = item.stat().st_size
                        file_size_mb = file_size_bytes / (1024 * 1024)
                        found_files.append({
                            'path': item,
                            'name': item.name,
                            'size_mb': file_size_mb
                        })
                    except OSError as e:
                         logger.print_warning(f"Could not get stats for file {item.name}. Error: {e}")
    
    
    logger.print_info(f"Found {len(found_files)} file(s).")
    
    if not found_files:
        return # Exit if no files found
    elif len(found_files) == 1:
        logger.print_success("Single CSV file found. Will automatically open chart in browser.")

    # Sort files by name for consistent listing
    found_files.sort(key=lambda x: x['name'])

    # Get metadata and print list
    logger.print_info("-" * 40) # Separator
    for idx, file_info in enumerate(found_files):
        metadata = get_parquet_metadata(file_info['path'])
        file_info.update(metadata) # Add metadata to the dict
        logger.print_info(f"[{idx}] {file_info['name']}")
        logger.print_info(f"    Size: {file_info['size_mb']:.3f} MB")
        if metadata['num_rows'] != -1:
            logger.print_info(f"    Rows: {file_info['num_rows']:,}") # Formatted number
        else:
            logger.print_info(f"    Rows: Could not determine")
    
        # Print extra info only if exactly one file is found
        if len(found_files) == 1:
            logger.print_info(f"    Columns ({len(file_info['columns'])}): {', '.join(file_info['columns'])}")
            
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
                logger.print_info(f"    Date Range: {first_date} → {last_date}")
            elif first_date:
                logger.print_info(f"    Date: {first_date}")
            
            # Display first row in a compact format
            if file_info['first_row'] is not None:
                first_row_str = "    First Row: "
                # If it's a Series object, display it nicely in a single line
                if isinstance(file_info['first_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['first_row'].items():
                        # Format timestamps nicely
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    first_row_str += " | ".join(values)
                else:
                    first_row_str += f"{file_info['first_row']}"
                logger.print_info(first_row_str)
            
            # Display last row in a compact format (if different from first)
            if file_info['last_row'] is not None and file_info['num_rows'] > 1:
                last_row_str = "    Last Row:  "
                # If it's a Series object, display it nicely in a single line
                if isinstance(file_info['last_row'], pd.Series):
                    values = []
                    for col_name, value in file_info['last_row'].items():
                        # Format timestamps nicely
                        if isinstance(value, pd.Timestamp):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(f"{col_name}={value}")
                    last_row_str += " | ".join(values)
                else:
                    last_row_str += f"{file_info['last_row']}"
                logger.print_info(last_row_str)
    
    logger.print_info("-" * 40) # Separator

    # Print hint or trigger plot
    if len(found_files) > 1:
        logger.print_info("To display a chart, re-run the command with more specific keywords:")
        logger.print_info(f"Example: python run_analysis.py show {args.source} <additional_keywords>")
    elif len(found_files) == 1:
        # Set default draw mode to 'fastest' if not explicitly specified
        if not hasattr(args, 'draw') or not args.draw:
            args.draw = 'fastest'
        logger.print_info(f"Found one file. Triggering plot with method: '{args.draw}'...")
        logger.print_info(f"Loading file data and triggering plot with method: '{args.draw}'...")
        
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
                
                logger.print_warning(f"Point size not found in filename, using default: {point_size}")
            
            # Import here to avoid circular imports
            generate_plot = import_generate_plot()
            
            # No result_df, we're just plotting the raw data
            result_df = None
            selected_rule = args.rule if hasattr(args, 'rule') else 'Predict_High_Low_Direction'
            estimated_point = True
            
            # Ensure 'draw' parameter is set to 'fastest' for optimal chart display
            if not hasattr(args, 'draw') or not args.draw:
                args.draw = 'fastest'
                
            # Call generate_plot with the necessary parameters
            generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
            
            logger.print_success(f"Successfully plotted data from '{found_files[0]['name']}' using '{args.draw}' mode")
            
        except Exception as e:
            logger.print_error(f"Error plotting file: {e}")
            traceback.print_exc()
