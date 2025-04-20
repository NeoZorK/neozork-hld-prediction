# src/workflow/workflow.py

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
import os # Import os for path operations
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
    Also handles saving downloaded API data to Parquet.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing results and metrics of the workflow.
    """
    # Initialize results dictionary with defaults
    workflow_results = {
        "success": False, "data_fetch_duration": 0,
        "data_size_mb": 0, "data_size_bytes": 0,
        "rows_count": 0, "columns_count": 0,
        "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False,
        "data_source_label": "N/A", "yf_ticker": None, "yf_interval": None, "current_period": None,
        "current_start": None, "current_end": None, "selected_rule": None, "error_message": None,
        "effective_mode": args.mode,
        # Metrics added previously
        "file_size_bytes": None, "api_latency_sec": None,
        # NEW: Placeholder for Parquet path
        "parquet_save_path": None
    }

    try:
        # --- Step 1: Acquire Data ---
        s_time = time.perf_counter()
        data_info = acquire_data(args)
        # Update results with all info returned by acquire_data (incl. metrics)
        workflow_results.update(data_info)
        ohlcv_df = data_info.get("ohlcv_df")
        workflow_results["data_fetch_duration"] = time.perf_counter() - s_time

        # --- Calculate DataFrame metrics AFTER successful acquisition ---
        if ohlcv_df is None or ohlcv_df.empty:
            logger.print_warning("Data acquisition failed or returned empty DataFrame.")
            # Keep default 0 values for counts and size
        else:
            # Calculate and store metrics only if df is valid
            workflow_results["rows_count"] = len(ohlcv_df)
            workflow_results["columns_count"] = len(ohlcv_df.columns)
            workflow_results["data_size_bytes"] = ohlcv_df.memory_usage(deep=True).sum()
            workflow_results["data_size_mb"] = workflow_results["data_size_bytes"] / (1024 * 1024)
            logger.print_debug(f"DataFrame Metrics: Rows={workflow_results['rows_count']}, Cols={workflow_results['columns_count']}, Memory={workflow_results['data_size_mb']:.3f} MB")

        # Check again if data is unusable before proceeding
        if ohlcv_df is None or ohlcv_df.empty:
            raise ValueError("Cannot proceed without valid data.")

        # --- NEW: Save DataFrame to Parquet for API modes ---
        effective_mode = workflow_results.get("effective_mode") # Get mode from results
        if effective_mode in ['yfinance', 'polygon', 'binance']:
            logger.print_info(f"Attempting to save raw data from '{effective_mode}' to Parquet...")
            parquet_dir = "data/raw_parquet" # Define target directory
            try:
                os.makedirs(parquet_dir, exist_ok=True) # Create directory if it doesn't exist

                # Construct filename safely
                ticker_label = args.ticker.replace('/', '_').replace('-', '_') # Sanitize ticker
                interval_label = args.interval
                start_label = workflow_results.get('current_start') or 'nodate'
                end_label = workflow_results.get('current_end') or 'nodate'
                period_label = workflow_results.get('current_period') or ''
                # Use period if start/end are not available
                date_part = f"{start_label}_{end_label}" if start_label != 'nodate' else period_label

                filename = f"{effective_mode}_{ticker_label}_{interval_label}_{date_part}.parquet"
                filepath = os.path.join(parquet_dir, filename)

                logger.print_info(f"Saving downloaded data to: {filepath}")
                # Ensure the library (pyarrow or fastparquet) is installed via requirements.txt
                ohlcv_df.to_parquet(filepath, index=True, engine='pyarrow') # Specify engine for clarity
                workflow_results["parquet_save_path"] = filepath # Store path on success
                logger.print_success(f"Successfully saved data to Parquet.")

            except ImportError as imp_err:
                 logger.print_error(f"Failed to save to Parquet: Missing required library. {imp_err}")
                 logger.print_error("Please ensure 'pyarrow' is installed (pip install pyarrow) and listed in requirements.txt.")
                 workflow_results["parquet_save_path"] = None
            except Exception as e:
                logger.print_error(f"Failed to save data to Parquet: {type(e).__name__}: {e}")
                workflow_results["parquet_save_path"] = None
        # --- End Parquet Saving ---


        # --- Step 2: Get Point Size ---
        point_size, estimated_point = get_point_size(args, data_info) # Pass data_info which contains df reference if needed
        workflow_results["point_size"] = point_size
        workflow_results["estimated_point"] = estimated_point

        # --- Step 3: Calculate Indicator ---
        s_time = time.perf_counter()
        result_df, selected_rule = calculate_indicator(args, ohlcv_df, point_size)
        workflow_results["selected_rule"] = selected_rule
        workflow_results["calc_duration"] = time.perf_counter() - s_time
        if result_df is None or result_df.empty:
            logger.print_warning("Indicator calculation returned empty results.")

        # --- Step 4: Generate Plot ---
        s_time = time.perf_counter()
        generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
        workflow_results["plot_duration"] = time.perf_counter() - s_time

        workflow_results["success"] = True

    except Exception as e:
        error_msg = f"Workflow failed: {type(e).__name__}: {e}"
        logger.print_error(error_msg)
        import traceback
        logger.print_error("Traceback:")
        try: print(f"{logger.ERROR_COLOR}{traceback.format_exc()}{logger.RESET_ALL}")
        except AttributeError: print(traceback.format_exc())
        workflow_results["error_message"] = str(e)

    return workflow_results