# src/workflow/workflow.py

"""
Defines the main data processing and analysis workflow.
Orchestrates data acquisition, calculation, plotting, and reporting steps.
All comments are in English.
"""

import time
import traceback

import pandas as pd
from typing import Dict, Tuple, Optional # Import Optional

# Use relative imports for workflow steps and common modules
from ..data import acquire_data
from ..calculation import calculate_indicator
from ..plotting import generate_plot
from ..utils import determine_point_size
from ..common import logger
from ..common.constants import TradingRule

# Definition of the main workflow function
def run_workflow(args, selected_rule: TradingRule, preloaded_data_info: Optional[Dict] = None) -> Tuple[Optional[pd.DataFrame], Optional[Dict], Optional[Dict]]:
    """
    Executes the main analysis workflow steps.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        selected_rule (TradingRule): The trading rule enum member to use.
        preloaded_data_info (Optional[Dict]): If provided, contains pre-loaded data
                                               (from cache) and skips acquisition.
                                               Expected keys: 'dataframe', 'mode'='cache',
                                               'data_source_label', 'interval', 'ticker',
                                               'point_size', 'estimated_point'.

    Returns:
        Tuple[Optional[pd.DataFrame], Optional[Dict], Optional[Dict]]:
            - The final DataFrame with results (or None on failure).
            - A dictionary containing information about the data source and parameters.
            - A dictionary containing execution times for each step.
    """
    exec_times = {} # Dictionary to store execution times
    data_info = {} # Dictionary to store data source info
    result_df = None # Initialize result DataFrame

    try:
        # --- Step 1: Data Acquisition (or use preloaded) ---
        step_start_time = time.time()
        raw_df = None
        if preloaded_data_info and preloaded_data_info.get('mode') == 'cache':
            logger.print_info("--- Step 1: Using Preloaded Data from Cache ---")
            data_info = preloaded_data_info # Use provided info
            raw_df = data_info.get('dataframe')
            if raw_df is None:
                 logger.print_error("Preloaded data info provided, but DataFrame is missing.")
                 return None, data_info, exec_times # Cannot proceed
            # Ensure point size is present in data_info for cached data
            if 'point_size' not in data_info or data_info['point_size'] is None:
                 logger.print_error("Point size (--point) must be provided when plotting from cache.")
                 return None, data_info, exec_times
            logger.print_success(f"Using cached data: {data_info.get('data_source_label', 'N/A')}")
        else:
            logger.print_info("--- Step 1: Acquiring Data ---")
            # Call the data acquisition module if not using cache
            raw_df, data_info = acquire_data(args)

        exec_times['data_acquisition'] = time.time() - step_start_time

        if raw_df is None or raw_df.empty:
            logger.print_warning("No data acquired or loaded. Workflow cannot continue.")
            # data_info might still contain partial info (like mode)
            return None, data_info, exec_times

        # --- Step 2: Determine Point Size (if not already set, e.g., from cache) ---
        step_start_time = time.time()
        logger.print_info("--- Step 2: Determining Point Size ---")
        # If point size is already in data_info (e.g., from cache or required args), use it
        if 'point_size' in data_info and data_info['point_size'] is not None:
             point_size = data_info['point_size']
             estimated_point = data_info.get('estimated_point', False) # Get flag if exists
             logger.print_info(f"Using specified/cached point size: {point_size}")
        else:
             # Otherwise, determine it (primarily for yfinance or if not provided)
             point_size, estimated_point = determine_point_size(args, raw_df, data_info)
             # Store determined point size back into data_info
             data_info['point_size'] = point_size
             data_info['estimated_point'] = estimated_point

        exec_times['point_determination'] = time.time() - step_start_time

        if point_size is None:
            logger.print_error("Could not determine point size. Workflow cannot continue.")
            return raw_df, data_info, exec_times # Return raw_df as result_df is None

        # --- Step 3: Calculate Indicator ---
        step_start_time = time.time()
        logger.print_info(f"--- Step 3: Calculating Indicator (Rule: {selected_rule.name}) ---")
        result_df = calculate_indicator(raw_df, selected_rule, point_size, data_info)
        exec_times['indicator_calculation'] = time.time() - step_start_time

        if result_df is None or result_df.empty:
             logger.print_warning("Indicator calculation failed or returned empty DataFrame.")
             # Return raw_df as result_df is None, data_info might be useful
             return raw_df, data_info, exec_times

        # --- Step 4: Generate Plot ---
        step_start_time = time.time()
        logger.print_info("--- Step 4: Generating Plot ---")
        generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
        exec_times['plotting'] = time.time() - step_start_time

        logger.print_success("Workflow completed successfully.")
        return result_df, data_info, exec_times

    except Exception as e:
        logger.print_error(f"An error occurred during the workflow: {type(e).__name__}: {e}")
        logger.print_debug(f"Traceback (workflow):\n{traceback.format_exc()}")
        # Return current state even on error for potential partial results/info
        return result_df, data_info, exec_times

# Function to display the execution summary
def display_summary(data_info: Optional[Dict], selected_rule: Optional[TradingRule], exec_times: Optional[Dict]):
     """Displays a summary of the execution."""
     if not data_info or not selected_rule or not exec_times:
          logger.print_warning("Cannot display summary due to missing information.")
          return

     logger.print_info("\n--- Execution Summary ---")
     source_label = data_info.get('data_source_label', 'N/A')
     mode = data_info.get('mode', 'N/A')
     rule_name = selected_rule.name
     point_size = data_info.get('point_size')
     estimated = data_info.get('estimated_point', False)
     point_str = f"{point_size:.8f}" if point_size is not None else "N/A"

     print(f"Data Source::         {source_label} (Mode: {mode})")
     print(f"Rule Applied::        {rule_name}")
     print(f"Point Size Used::     {point_str}{' (Estimated)' if estimated else ''}")
     print("-" * 45) # Separator line
     # Memory usage might be harder to track accurately per step without specific tools
     # print(f"Memory Usage::        {data_info.get('memory_usage_mb', 'N/A'):.3f} MB")
     print(f"Data Fetch/Load Time:: {exec_times.get('data_acquisition', 0):.3f} seconds")
     if 'point_determination' in exec_times: # Only show if step ran
          print(f"Point Determ. Time::  {exec_times.get('point_determination', 0):.3f} seconds")
     print(f"Indicator Calc Time:: {exec_times.get('indicator_calculation', 0):.3f} seconds")
     print(f"Plotting Time::       {exec_times.get('plotting', 0):.3f} seconds")
     print("-" * 45) # Separator line
     total_workflow_time = sum(exec_times.values())
     print(f"Total Workflow Time:: {total_workflow_time:.3f} seconds") # Sum of tracked steps
     logger.print_info("--- End Summary ---")

