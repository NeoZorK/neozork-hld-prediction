# run_analysis.py

"""
Main entry point for the NeoZorK HLD analysis tool.
Parses arguments, manages workflow execution based on selected mode (analysis or show cache).
All comments are in English.
"""

import time
import sys
import traceback
import pandas as pd # Import pandas for type hinting

# Use relative imports for consistency within the package structure
from src.cli import parse_arguments
from src.workflow import run_workflow, display_summary # Import display_summary
from src.common import logger
from src.common.constants import TradingRule # Import TradingRule for mapping
# --- Import cache manager functions ---
from src.cache_manager.cache_manager import find_cached_files, display_cached_files_info, load_cached_file

# Helper function to map rule aliases
def map_rule_alias(rule_input: str) -> TradingRule:
    """Maps rule name or alias string to TradingRule enum member."""
    rule_aliases_map = {'PHLD': 'Predict_High_Low_Direction', 'PV': 'Pressure_Vector', 'SR': 'Support_Resistants'}
    rule_name = rule_aliases_map.get(rule_input, rule_input) # Get full name if alias, else keep original
    try:
        return TradingRule[rule_name]
    except KeyError:
        logger.print_error(f"Invalid trading rule specified: '{rule_input}'. Using default.")
        # Return a default or raise an error depending on desired strictness
        return TradingRule.Predict_High_Low_Direction # Default fallback

# --- Main Execution Function ---
def main():
    """
    Parses arguments and executes the main workflow or cache management.
    """
    start_time = time.time()
    logger.print_info(f"Shcherbyna Pressure Vector Indicator - Version: {__import__('src').__version__}") # Get version dynamically

    # Parse command line arguments
    args = parse_arguments()

    # Normalize mode 'yf' to 'yfinance'
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # --- Handle 'show' mode ---
    if effective_mode == 'show':
        logger.print_info(f"--- Cache Management Mode (Source: {args.source}) ---")
        if not args.source:
             logger.print_error("Source must be specified for 'show' mode. Use --source [yf|polygon|binance|csv].")
             sys.exit(1)

        # Find matching cached files
        found_files = find_cached_files(args.source, args.search)

        if not found_files:
            # find_cached_files already prints warnings/info
            sys.exit(0) # Exit cleanly if no files found

        # Decide whether to list files or attempt to load and plot one
        load_and_plot = False
        selected_file_info = None

        if len(found_files) == 1 and args.search:
            # If search terms were provided and exactly one file matches,
            # consider loading and plotting it.
            selected_file_info = found_files[0]
            logger.print_info(f"Found unique matching file: {selected_file_info['filename']}")
            # Check if point size is provided, as it's needed for plotting
            if args.point is not None:
                 logger.print_info(f"Point size provided ({args.point}). Will attempt to load and plot.")
                 load_and_plot = True
            else:
                 logger.print_warning("Unique file found, but --point size is required for plotting from cache.")
                 logger.print_info("Displaying file information instead.")
                 # Fall through to display info

        if load_and_plot and selected_file_info:
            # Attempt to load the selected file
            loaded_df = load_cached_file(selected_file_info['path'])

            if loaded_df is not None:
                # Map rule alias if needed
                selected_rule = map_rule_alias(args.rule)

                # Prepare data_info dictionary for workflow
                # Extract info from filename or use defaults
                data_info = {
                    'mode': 'cache', # Indicate data is from cache
                    'data_source_label': selected_file_info.get('filename', 'Cached File'),
                    'interval': selected_file_info.get('interval', args.interval), # Use parsed interval or default
                    'ticker': selected_file_info.get('ticker', 'Unknown'),
                    'point_size': args.point, # Use the provided point size
                    'estimated_point': False, # Point size must be provided for cache plotting
                    'dataframe': loaded_df # Pass the loaded dataframe
                }

                # Run the workflow with the loaded data
                logger.print_info("--- Running Analysis on Cached Data ---")
                workflow_result_df, workflow_data_info, exec_times = run_workflow(args, selected_rule, preloaded_data_info=data_info)

                # Display summary (if workflow ran)
                if exec_times:
                     display_summary(workflow_data_info, selected_rule, exec_times)
                else:
                     logger.print_warning("Workflow did not return execution times.")

            else:
                logger.print_error(f"Failed to load data from {selected_file_info['filename']}. Cannot proceed with plotting.")
                # Optionally display info for the failed file
                display_cached_files_info([selected_file_info])

        else:
            # List all found files if not plotting a single one
            display_cached_files_info(found_files)

        logger.print_info("--- Cache Management Finished ---")


    # --- Handle Analysis modes (demo, yfinance, csv, polygon, binance) ---
    else:
        logger.print_info(f"--- Analysis Mode ({effective_mode}) ---")
        # Map rule alias if needed
        selected_rule = map_rule_alias(args.rule)

        # Run the standard workflow (which includes data acquisition)
        result_df, data_info, exec_times = run_workflow(args, selected_rule)

        # Display summary (if workflow ran)
        if exec_times:
             display_summary(data_info, selected_rule, exec_times)
        else:
             logger.print_warning("Workflow did not return execution times.")


    # --- Final Timing ---
    end_time = time.time()
    total_duration = end_time - start_time
    logger.print_info(f"Total script execution time: {total_duration:.3f} seconds.")
    logger.print_success("Workflow finished successfully.")


# --- Script Entry Point ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.print_warning("\nExecution interrupted by user (Ctrl+C).")
        sys.exit(1)
    except Exception as e:
        logger.print_error(f"An unexpected error occurred: {type(e).__name__}: {e}")
        # Print detailed traceback for debugging
        logger.print_error("Traceback:")
        print(traceback.format_exc(), file=sys.stderr) # Print traceback to stderr
        sys.exit(1)

