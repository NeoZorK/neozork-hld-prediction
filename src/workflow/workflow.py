# src/workflow/workflow.py

"""
Main workflow execution logic for the indicator analysis.
Orchestrates calls to different step modules.
All comments are in English.
"""
import time
import traceback # Keep traceback
import pandas as pd

# Use relative imports within the src package
from src.common import logger
from src.data.data_acquisition_core import acquire_data
from src.utils.point_size_determination import get_point_size
from src.calculation.indicator_calculation import calculate_indicator
from src.plotting.plotting_generation import generate_plot
from src.cli.core.cli_show_mode import handle_show_mode
# Import the export functions
from src.export.parquet_export import export_indicator_to_parquet
from src.export.csv_export import export_indicator_to_csv
from src.export.json_export import export_indicator_to_json
# Import interactive mode
from src.interactive.core.interactive_system import InteractiveSystem
# from src.calculation.universal_trading_metrics import display_universal_trading_metrics

try:
    from src.calculation.universal_trading_metrics import display_universal_trading_metrics
except ImportError as e:
    print(f'universal_trading_metrics import failed: {e}')
    print(f'traceback: {traceback.format_exc()}')
    display_universal_trading_metrics = None

def run_indicator_workflow(args):
    """
    Orchestrates the main steps by calling functions from specific step modules.
    Data saving is now handled within acquire_data.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary containing results and metrics of the workflow.
    """
    # Special case: handle interactive mode
    if hasattr(args, 'interactive') and args.interactive:
        try:
            logger.print_info("Starting interactive mode...")
            system = InteractiveSystem()
            system.run()
            return {
                "success": True,
                "effective_mode": "interactive",
                "data_source_label": "Interactive mode",
                "error_message": None,
                "error_traceback": None,
                "data_fetch_duration": 0,
                "calc_duration": 0,
                "plot_duration": 0,
                "rows_count": 0,
                "columns_count": 0,
                "data_size_mb": 0,
                "data_size_bytes": 0
            }
        except Exception as e:
            traceback_str = traceback.format_exc()
            logger.print_error(f"Interactive mode failed: {e}")
            return {
                "success": False,
                "effective_mode": "interactive",
                "data_source_label": "Interactive mode",
                "error_message": str(e),
                "error_traceback": traceback_str,
                "data_fetch_duration": 0,
                "calc_duration": 0,
                "plot_duration": 0,
                "rows_count": 0,
                "columns_count": 0,
                "data_size_mb": 0,
                "data_size_bytes": 0
            }
    
    # Special case: handle 'show' mode differently
    if args.mode == 'show':
        try:
            # Track timing for show mode operations
            t_show_start = time.perf_counter()
            
            # Call the show mode handler with timing tracking
            show_results = handle_show_mode(args)
            
            t_show_end = time.perf_counter()
            show_duration = t_show_end - t_show_start
            
            # Prepare results with real timing and metrics
            results = {
                "success": True,
                "effective_mode": "show",
                "data_source_label": f"Show mode (source: {args.source if hasattr(args, 'source') else 'N/A'})",
                "error_message": None,
                "error_traceback": None,
                "data_fetch_duration": show_results.get("data_fetch_duration", 0) if show_results else 0,
                "calc_duration": show_results.get("calc_duration", 0) if show_results else 0,
                "plot_duration": show_results.get("plot_duration", 0) if show_results else 0,
                "rows_count": show_results.get("rows_count", 0) if show_results else 0,
                "columns_count": show_results.get("columns_count", 0) if show_results else 0,
                "data_size_mb": show_results.get("data_size_mb", 0) if show_results else 0,
                "data_size_bytes": show_results.get("data_size_bytes", 0) if show_results else 0,
                "file_size_bytes": show_results.get("file_size_bytes") if show_results else None,
                "point_size": show_results.get("point_size") if show_results else None,
                "estimated_point": show_results.get("estimated_point", False) if show_results else False
            }
            
            # If no detailed results were returned, set basic timing
            if not show_results:
                results["data_fetch_duration"] = show_duration
            
            return results
            
        except Exception as e:
            # traceback already imported at module level
            traceback_str = traceback.format_exc()
            # Return error information
            return {
                "success": False,
                "effective_mode": "show",
                "data_source_label": f"Show mode (source: {args.source if hasattr(args, 'source') else 'N/A'})",
                "error_message": str(e),
                "error_traceback": traceback_str,
                "data_fetch_duration": 0,
                "calc_duration": 0,
                "plot_duration": 0,
                "rows_count": 0,
                "columns_count": 0,
                "data_size_mb": 0,
                "data_size_bytes": 0
            }
    
    t_start_workflow = time.perf_counter()
    
    # Initialize results dictionary with defaults
    workflow_results = {
        "success": False, "data_fetch_duration": 0,
        "calc_duration": 0, "plot_duration": 0, "point_size": None, "estimated_point": False,
        "selected_rule": None, "error_message": None, "error_traceback": None,
        # Keep fields populated by acquire_data
        "data_source_label": "N/A", "effective_mode": args.mode, # effective_mode updated by acquire_data
        "parquet_cache_used": False, "parquet_cache_file": None,
        "data_metrics": {},
        "steps_duration": {}
    }
    
    # For show mode, set success=True by default to avoid errors
    if hasattr(args, 'mode') and args.mode == 'show':
        workflow_results["success"] = True
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

        # --- Special handling for CSV folder processing ---
        if (args.mode == 'csv' and hasattr(args, 'csv_folder') and args.csv_folder and 
            data_info.get("folder_processing_results")):
            
            # For folder processing, we already have results from the processor
            folder_results = data_info.get("folder_processing_results", {})
            
            # Update workflow results with folder processing info
            workflow_results.update({
                "success": folder_results.get('success', False),
                "files_processed": folder_results.get('files_processed', 0),
                "files_failed": folder_results.get('files_failed', 0),
                "total_processing_time": folder_results.get('total_time', 0),
                "total_size_mb": folder_results.get('total_size_mb', 0),
                "failed_files": folder_results.get('failed_files', []),
                "folder_processing_results": folder_results
            })
            
            # For folder processing, we skip the normal workflow steps
            # since each file was processed individually in the folder processor
            logger.print_success(f"CSV folder processing completed: {folder_results.get('files_processed', 0)} files processed, {folder_results.get('files_failed', 0)} failed")
            
            return workflow_results

        # --- Critical Check for single file processing ---
        if ohlcv_df is None or ohlcv_df.empty:
            error_msg_from_data = data_info.get("error_message") or "Data acquisition returned None or empty DataFrame."
            raise ValueError(error_msg_from_data)

        # Validate that ohlcv_df has a DatetimeIndex
        if not isinstance(ohlcv_df.index, pd.DatetimeIndex):
            raise ValueError("The DataFrame does not have a valid DatetimeIndex. Ensure the datetime column is correctly parsed.")

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

        # --- Step 3b: Display Universal Trading Metrics ---
        # Use args.lot_size, args.risk_reward_ratio, args.fee_per_trade if present, else defaults
        lot_size = getattr(args, 'lot_size', 1.0)
        risk_reward_ratio = getattr(args, 'risk_reward_ratio', 2.0)
        fee_per_trade = getattr(args, 'fee_per_trade', 0.07)
        
        logger.print_info("--- Step 3b: Displaying Universal Trading Metrics ---")
        
        try:
            display_universal_trading_metrics(
                result_df,
                selected_rule,
                lot_size=lot_size,
                risk_reward_ratio=risk_reward_ratio,
                fee_per_trade=fee_per_trade
            )
            logger.print_success("Universal trading metrics displayed successfully")
        except Exception as e:
            logger.print_error(f"Error displaying universal trading metrics: {e}")
            logger.print_error(f"Traceback: {traceback.format_exc()}")

        # --- Step 4: Generate Plot ---
        # Check if plot generation should be suppressed
        suppress_plots = getattr(args, 'suppress_plots', False)
        
        if not suppress_plots:
            logger.print_info("--- Step 4: Generating Plot ---")
            t_plot_start = time.perf_counter()
            # Pass data_info, result_df (which might be None/empty), selected_rule etc.
            generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point)
            t_plot_end = time.perf_counter()
            workflow_results["plot_duration"] = t_plot_end - t_plot_start
            workflow_results["steps_duration"]["plot"] = workflow_results["plot_duration"]
        else:
            logger.print_info("--- Step 4: Plot generation suppressed for folder processing ---")
            workflow_results["plot_duration"] = 0
            workflow_results["steps_duration"]["plot"] = 0

        # --- Step 5: Export Indicator Data (if requested) ---
        export_results = {}
        
        # Export to Parquet
        if hasattr(args, 'export_parquet') and args.export_parquet:
            logger.print_info("--- Step 5a: Exporting Indicator Data to Parquet ---")
            t_export_start = time.perf_counter()
            export_info = export_indicator_to_parquet(result_df, data_info, selected_rule, args)
            t_export_end = time.perf_counter()
            export_results["parquet"] = export_info
            workflow_results["export_parquet_duration"] = t_export_end - t_export_start
        
        # Export to CSV
        if hasattr(args, 'export_csv') and args.export_csv:
            logger.print_info("--- Step 5b: Exporting Indicator Data to CSV ---")
            t_export_start = time.perf_counter()
            export_info = export_indicator_to_csv(result_df, data_info, selected_rule, args)
            t_export_end = time.perf_counter()
            export_results["csv"] = export_info
            workflow_results["export_csv_duration"] = t_export_end - t_export_start
        
        # Export to JSON
        if hasattr(args, 'export_json') and args.export_json:
            logger.print_info("--- Step 5c: Exporting Indicator Data to JSON ---")
            t_export_start = time.perf_counter()
            export_info = export_indicator_to_json(result_df, data_info, selected_rule, args)
            t_export_end = time.perf_counter()
            export_results["json"] = export_info
            workflow_results["export_json_duration"] = t_export_end - t_export_start
        
        # Store export results if any exports were performed
        if export_results:
            total_export_duration = sum([
                workflow_results.get("export_parquet_duration", 0),
                workflow_results.get("export_csv_duration", 0),
                workflow_results.get("export_json_duration", 0)
            ])
            workflow_results["export_duration"] = total_export_duration
            workflow_results["steps_duration"]["export"] = total_export_duration
            workflow_results["export_results"] = export_results

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

        # Use the error message if already set (e.g., from ValueError raised above), otherwise format exception
        error_msg = workflow_results.get("error_message") or f"{type(e).__name__}: {e}"
        logger.print_error(f"Workflow failed: {error_msg}")
        traceback_str = traceback.format_exc()
        logger.print_error("Traceback:")
        try: print(f"{logger.ERROR_COLOR}{traceback_str}{logger.RESET_ALL}")
        except AttributeError: print(traceback_str)
        # Store the primary error message and traceback
        workflow_results["error_message"] = str(e) # Store the original exception string if not already set
        workflow_results["error_traceback"] = traceback_str

    # Add overall duration to results
    workflow_results["total_duration_sec"] = time.perf_counter() - t_start_workflow
    return workflow_results

