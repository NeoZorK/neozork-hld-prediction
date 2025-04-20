# src/workflow/workflow.py

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
# Use relative imports within the src package
from ..common import logger
# Import functions from the specific step modules using relative paths
from ..data.data_acquisition import acquire_data
from ..utils.point_size_determination import get_point_size
from ..calculation.indicator_calculation import calculate_indicator
from ..plotting.plotting_generation import generate_plot

# --- Main Workflow Orchestrator ---

# Definition of the run_indicator_workflow function
def run_indicator_workflow(args):
    """
    Orchestrates the main steps by calling functions from specific step modules.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing results and metrics of the workflow.
    """
    # Initialize results dictionary with defaults for new metrics
    workflow_results = {
        "success": False, "data_fetch_duration": 0,
        "data_size_mb": 0, "data_size_bytes": 0, # Existing memory usage
        "rows_count": 0, "columns_count": 0, # NEW: row/column counts
        "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False,
        "data_source_label": "N/A", "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": None, "current_end": None, "selected_rule": None, "error_message": None,
        "effective_mode": args.mode
        # Add placeholders for future metrics if needed (e.g., "latency_sec": None, "parquet_save_path": None)
    }

    # --- Variables to pass between steps ---
    # data_info = None # No longer needed to store whole dict outside try
    # point_size = None
    # estimated_point = False
    # result_df = None
    # selected_rule = None

    try:
        # --- Step 1: Acquire Data ---
        s_time = time.perf_counter()
        data_info = acquire_data(args)
        workflow_results.update(data_info) # Store acquired metadata (includes fetcher metrics later)
        ohlcv_df = data_info.get("ohlcv_df") # Use .get() for safety
        workflow_results["data_fetch_duration"] = time.perf_counter() - s_time

        # --- Calculate DataFrame metrics AFTER successful acquisition ---
        if ohlcv_df is None or ohlcv_df.empty:
            logger.print_warning("Data acquisition failed or returned empty DataFrame.")
            # Keep default 0 values for counts and size
            # Optionally raise error here if empty data is critical failure
            # raise ValueError("Data acquisition failed or returned empty DataFrame.") # Uncomment if needed
        else:
            # Calculate and store metrics only if df is valid
            workflow_results["rows_count"] = len(ohlcv_df) # Or ohlcv_df.shape[0]
            workflow_results["columns_count"] = len(ohlcv_df.columns) # Or ohlcv_df.shape[1]
            workflow_results["data_size_bytes"] = ohlcv_df.memory_usage(deep=True).sum()
            workflow_results["data_size_mb"] = workflow_results["data_size_bytes"] / (1024 * 1024)
            logger.print_debug(f"DataFrame Metrics: Rows={workflow_results['rows_count']}, Cols={workflow_results['columns_count']}, Memory={workflow_results['data_size_mb']:.3f} MB")

        # Check again if data is unusable before proceeding (if not raising error above)
        if ohlcv_df is None or ohlcv_df.empty:
            # If we decided not to raise an error earlier, we must stop here
            # otherwise subsequent steps will fail.
            raise ValueError("Cannot proceed without valid data.")

        # --- Step 2: Get Point Size ---
        # Timing included in calc setup time
        point_size, estimated_point = get_point_size(args, data_info)
        workflow_results["point_size"] = point_size
        workflow_results["estimated_point"] = estimated_point

        # --- Step 3: Calculate Indicator ---
        s_time = time.perf_counter()
        # Pass the confirmed valid ohlcv_df
        result_df, selected_rule = calculate_indicator(args, ohlcv_df, point_size)
        workflow_results["selected_rule"] = selected_rule
        workflow_results["calc_duration"] = time.perf_counter() - s_time
        if result_df is None or result_df.empty:
            # Treat empty result df from calculation as warning, not error stopping plotting
            logger.print_warning("Indicator calculation returned empty results.")
            # Don't raise error, allow plotting (which will then skip)

        # --- Step 4: Generate Plot ---
        s_time = time.perf_counter()
        generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
        workflow_results["plot_duration"] = time.perf_counter() - s_time

        # Mark overall success if we reached here without critical errors
        workflow_results["success"] = True

    except Exception as e:
        # Catch errors from any step
        error_msg = f"Workflow failed: {type(e).__name__}: {e}"
        logger.print_error(error_msg)
        # Add traceback print for better debugging during development
        import traceback
        logger.print_error("Traceback:")
        try:
            # Use colorama styles if logger has them
            print(f"{logger.ERROR_COLOR}{traceback.format_exc()}{logger.RESET_ALL}")
        except AttributeError:
            # Fallback to basic print if logger doesn't have color constants
            print(traceback.format_exc())
        # Store error message
        workflow_results["error_message"] = str(e)
        # Keep partial timing/info results if available (already done by initializing dict first)

    return workflow_results