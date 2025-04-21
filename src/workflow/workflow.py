# src/workflow/workflow.py (Removed Parquet saving block)

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
import os # Keep os import if needed elsewhere
import pandas as pd
import traceback # Keep traceback

# Use relative imports within the src package
from ..common import logger
from ..data.data_acquisition import acquire_data
from ..utils.point_size_determination import get_point_size
from ..calculation.indicator_calculation import calculate_indicator
from ..plotting.plotting_generation import generate_plot

# Definition of the run_indicator_workflow function
def run_indicator_workflow(args):
    """
    Orchestrates the main steps by calling functions from specific step modules.
    Data saving is now handled within acquire_data.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing results and metrics of the workflow.
    """
    t_start_workflow = time.perf_counter()
    # Initialize results dictionary with defaults
    workflow_results = {
        "success": False, "data_fetch_duration": 0,
        "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False,
        "selected_rule": None, "error_message": None, "error_traceback": None,
        # Keep fields populated by acquire_data
        "data_source_label": "N/A", "effective_mode": args.mode,
        "parquet_cache_used": False, "parquet_cache_file": None,
        "data_metrics": {},
        "steps_duration": {}
    }
    result_df = None # Initialize result_df

    try:
        # --- Step 1: Acquire Data (Handles Caching Internally) ---
        t_acq_start = time.perf_counter()
        data_info = acquire_data(args)
        t_acq_end = time.perf_counter()
        workflow_results.update(data_info) # Merge all info from acquire_data
        workflow_results["data_fetch_duration"] = t_acq_end - t_acq_start
        workflow_results["steps_duration"]["acquire"] = workflow_results["data_fetch_duration"]

        ohlcv_df = data_info.get("ohlcv_df") # Get DataFrame

        # --- Critical Check ---
        if ohlcv_df is None or ohlcv_df.empty:
            # Error message should already be in data_info from acquire_data
            raise ValueError(data_info.get("error_message", "Cannot proceed without valid data."))

        # Log DataFrame Metrics (info now comes from data_info)
        logger.print_debug(f"DataFrame Metrics: Rows={data_info.get('rows_count', 0)}, Cols={data_info.get('columns_count', 0)}, Memory={data_info.get('data_size_mb', 0):.3f} MB")


        # --- Step 2: Get Point Size ---
        logger.print_info("--- Step 2: Determining Point Size ---")
        t_point_start = time.perf_counter()
        # Pass data_info which now contains all necessary details
        point_size, estimated_point = get_point_size(args, data_info)
        t_point_end = time.perf_counter()
        workflow_results["point_size"] = point_size
        workflow_results["estimated_point"] = estimated_point
        workflow_results["steps_duration"]["point_size"] = t_point_end - t_point_start


        # --- Step 3: Calculate Indicator ---
        logger.print_info(f"--- Step 3: Calculating Indicator (Rule: {args.rule}) ---")
        t_calc_start = time.perf_counter()
        # Pass the DataFrame obtained from data_info
        result_df, selected_rule = calculate_indicator(args, ohlcv_df.copy(), point_size)
        t_calc_end = time.perf_counter()
        workflow_results["selected_rule"] = selected_rule
        workflow_results["calc_duration"] = t_calc_end - t_calc_start
        workflow_results["steps_duration"]["calculate"] = workflow_results["calc_duration"]

        if result_df is None or result_df.empty:
            logger.print_warning("Indicator calculation returned empty results.")


        # --- Step 4: Generate Plot ---
        logger.print_info("--- Step 4: Generating Plot ---")
        t_plot_start = time.perf_counter()
        # Pass data_info, result_df (which might be None/empty), selected_rule etc.
        generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
        t_plot_end = time.perf_counter()
        workflow_results["plot_duration"] = t_plot_end - t_plot_start
        workflow_results["steps_duration"]["plot"] = workflow_results["plot_duration"]

        workflow_results["success"] = True
        logger.print_success("Workflow completed successfully.")

    except Exception as e:
        t_except = time.perf_counter() # Time of exception
        # Try to capture duration of step that failed
        if 't_plot_start' in locals() and 'plot' not in workflow_results['steps_duration']:
            workflow_results["plot_duration"] = t_except - t_plot_start
            workflow_results["steps_duration"]["plot"] = workflow_results["plot_duration"]
        elif 't_calc_start' in locals() and 'calculate' not in workflow_results['steps_duration']:
            workflow_results["calc_duration"] = t_except - t_calc_start
            workflow_results["steps_duration"]["calculate"] = workflow_results["calc_duration"]
        elif 't_point_start' in locals() and 'point_size' not in workflow_results['steps_duration']:
             workflow_results["steps_duration"]["point_size"] = t_except - t_point_start
        # No need to time acquire step here as it's always first

        error_msg = f"{type(e).__name__}: {e}"
        logger.print_error(f"Workflow failed: {error_msg}")
        traceback_str = traceback.format_exc()
        logger.print_error("Traceback:")
        try: print(f"{logger.ERROR_COLOR}{traceback_str}{logger.RESET_ALL}")
        except AttributeError: print(traceback_str)
        workflow_results["error_message"] = str(e)
        workflow_results["error_traceback"] = traceback_str

    # Add overall duration to results
    workflow_results["total_duration_sec"] = time.perf_counter() - t_start_workflow

    return workflow_results