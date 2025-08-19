# src/workflow/reporting.py

"""
Functions for reporting results and summaries.
All comments are in English.
"""
from src.common import logger

# Definition of the print_summary function
def print_summary(results: dict, total_duration: float, args):
    """
    Prints the execution summary based on the results dictionary.

    Args:
        results (dict): The dictionary returned by the workflow function.
        total_duration (float): The total script execution time.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    logger.print_info("\n--- Execution Summary ---")

    # Safely get values from results dict
    effective_mode = results.get("effective_mode", args.mode)
    data_source_label = results.get("data_source_label", "N/A")
    yf_ticker = results.get("yf_ticker")
    yf_interval_mapped = results.get("yf_interval")
    current_start = results.get("current_start")
    current_end = results.get("current_end")
    current_period = results.get("current_period")
    point_size = results.get("point_size")
    estimated_point = results.get("estimated_point", False)
    data_size_mb = results.get("data_size_mb", 0)
    data_size_bytes = results.get("data_size_bytes", 0)
    rows_count = results.get("rows_count", 0)
    columns_count = results.get("columns_count", 0)
    file_size_bytes = results.get("file_size_bytes")
    api_latency_sec = results.get("api_latency_sec")
    # NEW: Get Parquet save path
    parquet_save_path = results.get("parquet_save_path")
    # ---
    data_fetch_duration = results.get("data_fetch_duration", 0)
    calc_duration = results.get("calc_duration", 0)
    plot_duration = results.get("plot_duration", 0)

    # --- Print Basic Info ---
    logger.print_info(logger.format_summary_line("Data Source:", data_source_label if effective_mode != 'demo' else 'Demo'))
    logger.print_info(logger.format_summary_line("Rule Applied:", args.rule))

    # --- YFinance Specific Output ---
    if effective_mode == 'yfinance':
        logger.print_warning("--- YFinance Data Note: Volume might be zero/missing for Forex/Indices ---")
        logger.print_info(logger.format_summary_line("Ticker:", yf_ticker if yf_ticker else 'N/A'))
        logger.print_info(logger.format_summary_line("Interval Requested:", f"{args.interval} (mapped to {yf_interval_mapped if yf_interval_mapped else 'N/A'})"))
        if current_start and current_end:
            logger.print_info(logger.format_summary_line("Date Range:", f"{current_start} to {current_end}"))
        else:
            logger.print_info(logger.format_summary_line("Period:", current_period if current_period else 'N/A'))

    # --- Point Size ---
    if point_size is not None:
        point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
        size_str = f"{point_size:{point_format}}{' (Estimated)' if estimated_point else ''}"
        logger.print_info(logger.format_summary_line("Point Size Used:", size_str ))
    else:
         reason = "(Data load failed)" if results.get("error_message") else "(Not applicable)"
         logger.print_info(logger.format_summary_line("Point Size Used:", f"N/A {reason}"))

    # --- Separator and Data Metrics ---
    separator = "-" * (25 + 1 + 20) # Adjust width as needed based on format_summary_line
    logger.print_info(separator)
    if effective_mode == 'csv' and file_size_bytes is not None and file_size_bytes > 0:
        file_size_mb = file_size_bytes / (1024 * 1024)
        logger.print_info(logger.format_summary_line("Input File Size:", f"{file_size_mb:.3f} MB ({file_size_bytes:,} bytes)"))
    if rows_count > 0 or columns_count > 0:
        logger.print_info(logger.format_summary_line("DataFrame Shape:", f"{rows_count} rows, {columns_count} columns"))
    logger.print_info(logger.format_summary_line("Memory Usage:", f"{data_size_mb:.3f} MB ({data_size_bytes:,} bytes)"))
    # NEW: Print Parquet save path if available
    if parquet_save_path:
        logger.print_info(logger.format_summary_line("Saved Raw Data:", parquet_save_path))
    # ---

    # --- Timing Metrics ---
    logger.print_info(logger.format_summary_line("Data Fetch/Load Time:", f"{data_fetch_duration:.3f} seconds"))
    if api_latency_sec is not None and effective_mode in ['yfinance', 'polygon', 'binance']:
        latency_label = "API Request Latency:"
        if effective_mode == 'yfinance': latency_label = "yf.download Latency:"
        elif effective_mode in ['polygon', 'binance']: latency_label = "API Chunks Total Latency:"
        logger.print_info(logger.format_summary_line(latency_label, f"{api_latency_sec:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Indicator Calc Time:", f"{calc_duration:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Plotting Time:", f"{plot_duration:.3f} seconds"))
    logger.print_info(separator)
    logger.print_info(logger.format_summary_line("Total Execution Time:", f"{total_duration:.3f} seconds"))
    logger.print_info("--- End Summary ---")

    # Optionally print error message if workflow failed
    if not results.get("success", False) and results.get("error_message"):
        logger.print_error(f"Workflow failed: {results['error_message']}")