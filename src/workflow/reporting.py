# src/reporting.py

"""
Functions for reporting results and summaries.
All comments are in English.
"""
from ..common import logger

def print_summary(results: dict, total_duration: float, args):
    """
    Prints the execution summary based on the results dictionary.

    Args:
        results (dict): The dictionary returned by the workflow function.
        total_duration (float): The total script execution time.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    logger.print_info("\n--- Execution Summary ---")

    # Safely get values from results dict using .get() with defaults
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
    data_fetch_duration = results.get("data_fetch_duration", 0)
    calc_duration = results.get("calc_duration", 0)
    plot_duration = results.get("plot_duration", 0)


    logger.print_info(logger.format_summary_line("Data Source:", data_source_label if effective_mode != 'demo' else 'Demo'))
    # Display rule requested by user
    logger.print_info(logger.format_summary_line("Rule Applied:", args.rule))

    if effective_mode == 'yfinance':
        logger.print_warning("--- YFinance Data Note: Volume might be zero/missing for Forex/Indices ---")
        logger.print_info(logger.format_summary_line("Ticker:", yf_ticker if yf_ticker else 'N/A'))
        logger.print_info(logger.format_summary_line("Interval Requested:", f"{args.interval} (mapped to {yf_interval_mapped if yf_interval_mapped else 'N/A'})"))
        if current_start and current_end:
            logger.print_info(logger.format_summary_line("Date Range:", f"{current_start} to {current_end}"))
        else:
            logger.print_info(logger.format_summary_line("Period:", current_period if current_period else 'N/A'))

    if point_size is not None:
        point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
        size_str = f"{point_size:{point_format}}{' (Estimated)' if estimated_point else ''}"
        logger.print_info(logger.format_summary_line("Point Size Used:", size_str ))
    else:
         reason = "(Data load failed)" if results.get("error_message") else "(Not applicable)"
         logger.print_info(logger.format_summary_line("Point Size Used:", f"N/A {reason}"))

    separator = "-" * (25 + 1 + 20) # Adjust width as needed based on format_summary_line
    logger.print_info(separator)
    logger.print_info(logger.format_summary_line("Data Size:", f"{data_size_mb:.3f} MB ({data_size_bytes:,} bytes)"))
    logger.print_info(logger.format_summary_line("Data Fetch/Load Time:", f"{data_fetch_duration:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Indicator Calc Time:", f"{calc_duration:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Plotting Time:", f"{plot_duration:.3f} seconds"))
    logger.print_info(separator)
    logger.print_info(logger.format_summary_line("Total Execution Time:", f"{total_duration:.3f} seconds"))
    logger.print_info("--- End Summary ---")

    # Optionally print error message if workflow failed
    if not results.get("success", False) and results.get("error_message"):
        logger.print_error(f"Workflow failed: {results['error_message']}")