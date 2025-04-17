# src/workflow.py

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
# Use relative imports within the src package
from . import logger
# Import functions from the new step modules
from .data_acquisition import acquire_data
from .point_size_determination import get_point_size
from .indicator_calculation import calculate_indicator
from .plotting_generation import generate_plot

# --- Main Workflow Orchestrator ---
def run_indicator_workflow(args):
    """
    Orchestrates the main steps by calling functions from specific step modules.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing results and metrics of the workflow.
    """
    # Initialize results dictionary
    workflow_results = {
        "success": False, "data_fetch_duration": 0, "data_size_mb": 0, "data_size_bytes": 0,
        "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False,
        "data_source_label": "N/A", "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": None, "current_end": None, "selected_rule": None, "error_message": None,
        "effective_mode": args.mode
    }

    # --- Variables to pass between steps ---
    # data_info = None
    # point_size = None
    # estimated_point = False
    # result_df = None
    # selected_rule = None

    try:
        # --- Step 1: Acquire Data ---
        s_time = time.perf_counter()
        data_info = acquire_data(args)
        workflow_results.update(data_info) # Store acquired metadata
        ohlcv_df = data_info["ohlcv_df"] # Extract dataframe
        workflow_results["data_fetch_duration"] = time.perf_counter() - s_time
        if ohlcv_df is None or ohlcv_df.empty:
            raise ValueError("Data acquisition failed or returned empty DataFrame.")
        workflow_results["data_size_bytes"] = ohlcv_df.memory_usage(deep=True).sum()
        workflow_results["data_size_mb"] = workflow_results["data_size_bytes"] / (1024 * 1024)

        # --- Step 2: Get Point Size ---
        # Timing included in calc setup time
        point_size, estimated_point = get_point_size(args, data_info)
        workflow_results["point_size"] = point_size
        workflow_results["estimated_point"] = estimated_point

        # --- Step 3: Calculate Indicator ---
        s_time = time.perf_counter()
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
        workflow_results["error_message"] = str(e)
        # Keep partial timing/info results if available

    return workflow_results