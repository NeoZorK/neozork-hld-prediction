# NeoZorK HLD/src/workflow/workflow.py (CORRECTED - Moved Check Earlier)

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
import os # Import os for path operations
import pandas as pd # Import pandas for type hinting and checks
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
        "file_size_bytes": None, "api_latency_sec": None,
        "parquet_save_path": None, # Use consistent key
        "data_metrics": {}, # Initialize data_metrics
        "steps_duration": {} # Initialize steps_duration
    }
    ohlcv_df = None # Initialize ohlcv_df to None

    try:
        # --- Step 1: Acquire Data ---
        s_time = time.perf_counter()
        data_info = acquire_data(args)
        # Update results with all info returned by acquire_data (incl. metrics)
        workflow_results.update(data_info)
        ohlcv_df = data_info.get("ohlcv_df") # Get DataFrame from data_info
        data_fetch_duration = time.perf_counter() - s_time
        workflow_results["data_fetch_duration"] = data_fetch_duration
        workflow_results["steps_duration"]["acquire"] = data_fetch_duration # Record step duration

        # --- ** CRITICAL CHECK MOVED EARLIER ** ---
        # Exit immediately if data acquisition failed or returned unusable data
        if ohlcv_df is None or ohlcv_df.empty:
            logger.print_warning("Data acquisition failed or returned empty DataFrame. Cannot proceed.")
            # Set relevant metrics to 0 or default before raising
            workflow_results["rows_count"] = 0
            workflow_results["columns_count"] = 0
            workflow_results["data_size_bytes"] = 0
            workflow_results["data_size_mb"] = 0
            # Raise the specific error expected by the test
            raise ValueError("Cannot proceed without valid data.")

        # --- Calculate DataFrame Metrics (only if df is valid) ---
        workflow_results["rows_count"] = len(ohlcv_df)
        workflow_results["columns_count"] = len(ohlcv_df.columns)
        workflow_results["data_size_bytes"] = ohlcv_df.memory_usage(deep=True).sum()
        workflow_results["data_size_mb"] = workflow_results["data_size_bytes"] / (1024 * 1024)
        # Update data_metrics within results
        workflow_results["data_metrics"].update({
            "rows": workflow_results["rows_count"],
            "cols": workflow_results["columns_count"],
            "memory_bytes": workflow_results["data_size_bytes"],
            "memory_mb": workflow_results["data_size_mb"],
            # Try to get start/end from df index if available
            "start": str(ohlcv_df.index.min()) if isinstance(ohlcv_df.index, pd.DatetimeIndex) else None,
            "end": str(ohlcv_df.index.max()) if isinstance(ohlcv_df.index, pd.DatetimeIndex) else None,
            "source": data_info.get('data_source_label', 'N/A') # Add source info
        })
        logger.print_debug(f"DataFrame Metrics: Rows={workflow_results['rows_count']}, Cols={workflow_results['columns_count']}, Memory={workflow_results['data_size_mb']:.3f} MB")


        # --- NEW: Save DataFrame to Parquet for API modes ---
        effective_mode = workflow_results.get("effective_mode") # Get mode from results
        if effective_mode in ['yfinance', 'polygon', 'binance']:
            logger.print_info(f"Attempting to save raw data from '{effective_mode}' to Parquet...")
            parquet_dir = "data/raw_parquet"
            try:
                os.makedirs(parquet_dir, exist_ok=True)
                ticker_label = str(args.ticker).replace('/', '_').replace('-', '_')
                interval_label = str(args.interval)
                start_label = workflow_results.get('current_start') or 'nodate'
                end_label = workflow_results.get('current_end') or 'nodate'
                period_label = workflow_results.get('current_period') or ''
                date_part = f"{start_label}_{end_label}" if start_label != 'nodate' else period_label
                filename = f"{effective_mode}_{ticker_label}_{interval_label}_{date_part}.parquet"
                filepath = os.path.join(parquet_dir, filename)

                logger.print_info(f"Saving downloaded data to: {filepath}")
                ohlcv_df.to_parquet(filepath, index=True, engine='pyarrow')
                workflow_results["parquet_save_path"] = filepath # Use consistent key
                logger.print_success(f"Successfully saved data to Parquet.")
            except ImportError as imp_err:
                 logger.print_error(f"Failed to save to Parquet: Missing required library. {imp_err}")
                 logger.print_error("Please ensure 'pyarrow' is installed (pip install pyarrow) and listed in requirements.txt.")
                 workflow_results["parquet_save_path"] = None
            except Exception as e:
                logger.print_error(f"Failed to save data to Parquet: {type(e).__name__}: {e}")
                workflow_results["parquet_save_path"] = None

        # --- Step 2: Get Point Size ---
        s_time = time.perf_counter()
        # Pass data_info which should contain necessary details even if df is used directly
        point_size, estimated_point = get_point_size(args, data_info)
        point_size_duration = time.perf_counter() - s_time
        workflow_results["point_size"] = point_size
        workflow_results["estimated_point"] = estimated_point
        workflow_results["steps_duration"]["point_size"] = point_size_duration # Record step duration

        # --- Step 3: Calculate Indicator ---
        s_time = time.perf_counter()
        # Pass the original ohlcv_df here, as calculate_indicator handles renaming Volume->TickVolume internally if needed
        result_df, selected_rule = calculate_indicator(args, ohlcv_df.copy(), point_size) # Pass a copy just in case
        calc_duration = time.perf_counter() - s_time
        workflow_results["selected_rule"] = selected_rule
        workflow_results["calc_duration"] = calc_duration
        workflow_results["steps_duration"]["calculate"] = calc_duration # Record step duration
        if result_df is None or result_df.empty:
            logger.print_warning("Indicator calculation returned empty results.")
            # Maybe don't proceed to plot if calculation failed? Or let generate_plot handle None.
            # For now, we continue and let generate_plot check.

        # --- Step 4: Generate Plot ---
        s_time = time.perf_counter()
        generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
        plot_duration = time.perf_counter() - s_time
        workflow_results["plot_duration"] = plot_duration
        workflow_results["steps_duration"]["plot"] = plot_duration # Record step duration

        workflow_results["success"] = True

    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        logger.print_error(f"Workflow failed: {error_msg}")
        import traceback
        traceback_str = traceback.format_exc()
        logger.print_error("Traceback:")
        # Use logger's color capabilities if possible
        try: print(f"{logger.ERROR_COLOR}{traceback_str}{logger.RESET_ALL}")
        except AttributeError: print(traceback_str) # Fallback if logger colors aren't set up right
        workflow_results["error_message"] = str(e) # Store just the exception message string
        workflow_results["error_traceback"] = traceback_str # Store full traceback

    # --- Final Step: Consolidate Metrics ---
    # Update the main results dict with calculated durations and metrics
    # This is already done within the try block, but double-check structure.

    return workflow_results