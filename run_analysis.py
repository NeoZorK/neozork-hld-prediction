# /run_analysis.py (in NeoZorK HLD/ root folder)

# Standard library imports
import sys
import time
from datetime import date
#import pandas as pd

# Imports from the src package
from src import __version__ # Import version for display
from src.cli import parse_arguments # Import argument parsing function
from src.data_utils import get_demo_data, map_interval, map_ticker, fetch_yfinance_data # Import data functions
from src.utils import determine_point_size # Import point size estimation
from src.constants import TradingRule # Keep direct import for type hinting if needed later
from src.indicator import calculate_pressure_vector
from src.plotting import plot_indicator_results
from src import logger

# --- Main Execution Function ---
def main():
    """Main function to run the analysis."""

    # Print version information
    logger.print_info(f"Shcherbyna Pressure Vector Indicator - Version: {__version__}")

    # Start overall timer
    start_time_total = time.perf_counter()

    # Get command line arguments
    args = parse_arguments()

    # --- Data Acquisition ---
    start_time_data = time.perf_counter()
    ohlcv_df = None
    # Initialize point_size and estimated_point here
    point_size = None
    estimated_point = False
    data_source_label = ""
    yf_ticker = None # Store mapped ticker if applicable
    yf_interval = None # Store mapped interval if applicable
    current_period = None # Store effective period
    current_start = None # Store effective start date
    current_end = None # Store effective end date

    # Handle mode selection ('yf' alias)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    if effective_mode == 'demo':
        logger.print_info("--- Mode: Demo ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data() # get_demo_data itself logs info
        # --- SET point_size EXPLICITLY FOR DEMO ---
        point_size = 0.00001 # Use fixed value
        estimated_point = False # Not estimated
        logger.print_info(f"Using built-in demo data. Point size set to: {point_size}")
        # Point size logic is handled below, no estimation needed for demo

    elif effective_mode == 'yfinance':
        logger.print_info("--- Mode: Yahoo Finance ---")
        # Validate required arguments for yfinance mode
        if not args.ticker:
             logger.print_error("Ticker (--ticker) is required for yfinance mode.")
             sys.exit(1)

        data_source_label = args.ticker # Use ticker for plot title

        # Map and validate interval
        try:
            yf_interval = map_interval(args.interval)
        except ValueError as e:
            logger.print_error(str(e)) # Log the error message
            sys.exit(1)

        # Map ticker (optional enhancement)
        yf_ticker = map_ticker(args.ticker) # yf_ticker gets assigned value here

        # Determine history parameters
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end

        # Handle date logic (using your previous logic with default start)
        if args.start and not args.end:
            end_arg = date.today().strftime('%Y-%m-%d')
            logger.print_info(f"End date not specified, using today: {end_arg}")
        elif args.end and not args.start:
            # Using your default start date logic
            start_arg = "2000-01-01"
            logger.print_info(f"Start date not specified, using default: {start_arg}")

        # Determine effective period/dates for download
        if start_arg and end_arg:
            current_start = start_arg
            current_end = end_arg
            logger.print_info(f"Fetching data for interval '{yf_interval}' from {current_start} to {current_end}")
        else:
            current_period = period_arg
            logger.print_info(f"Fetching data for interval '{yf_interval}' for period '{current_period}'")

        # Fetch data using the function from data_utils
        ohlcv_df = fetch_yfinance_data(
            ticker=yf_ticker,
            interval=yf_interval,
            period=current_period,
            start_date=current_start,
            end_date=current_end
        )

        # --- Point Size Determination/Override (with estimation fallback) ---
        if ohlcv_df is not None and not ohlcv_df.empty:
            logger.print_debug(f"Columns returned by fetch_yfinance_data: {ohlcv_df.columns.tolist()}")
            if args.point is not None:
                # User provided point size
                if args.point <= 0:
                    logger.print_error("Provided point size (--point) must be positive.")
                    sys.exit(1)
                point_size = args.point
                estimated_point = False
                logger.print_info(f"Using user-provided point size: {point_size}")
            else:
                # --- Attempt automatic estimation ---
                logger.print_info("Attempting to estimate point size automatically...")
                point_size = determine_point_size(yf_ticker)  # Call estimation
                if point_size is not None:
                    # Estimation succeeded (though might be inaccurate)
                    estimated_point = True
                    logger.print_warning(f"Automatically estimated point size: {point_size:.8f}. "
                                         f"This is an ESTIMATE and might be inaccurate. "
                                         f"Use the --point argument for calculations requiring precision.")
                else:
                    # Estimation failed (function returned None)
                    logger.print_error(f"Automatic point size estimation failed for {yf_ticker}. "
                                       f"Please provide the correct value using the --point argument.")
                    # Exit if point size is crucial and couldn't be estimated
                    sys.exit(1)
                    # Alternatively, fallback to a default like 0.01 with a strong warning,
                    # but exiting is safer if calculations depend heavily on it.
                    # point_size = 0.01
                    # logger.print_warning("Falling back to default point size 0.01, calculations may be incorrect!")
        # --- END Point Size Logic ---

    # Record data acquisition time and size
    end_time_data = time.perf_counter()
    data_fetch_duration = end_time_data - start_time_data
    data_size_bytes = 0
    data_size_mb = 0

    # Calculate size only if df exists
    if ohlcv_df is not None:
        data_size_bytes = ohlcv_df.memory_usage(deep=True).sum()
        data_size_mb = data_size_bytes / (1024 * 1024)


    # --- Indicator Calculation ---
    result_df = None
    calc_duration = 0
    selected_rule = None # Define here for use in summary
    # Check if we have data AND a valid point size before proceeding
    if ohlcv_df is not None and not ohlcv_df.empty:
        # Crucial check: Ensure point_size was determined
        if point_size is not None:
            point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
            # Add '(Estimated)' tag to summary if it was estimated
            size_str = f"{point_size:{point_format}}{' (Estimated)' if estimated_point else ''}"
            logger.print_info(logger.format_summary_line("Point Size Used:", size_str))
        else:
            reason = "(Data load failed)" if ohlcv_df is None else "(Estimation failed)"
            logger.print_info(logger.format_summary_line("Point Size Used:", f"N/A {reason}"))

        # --- Continue with calculation ---
        logger.print_info(f"\nCalculating indicator using rule: {args.rule}...")
        start_time_calc = time.perf_counter()

        # Map rule string to enum
        try:
             selected_rule = TradingRule[args.rule]
        except KeyError:
             logger.print_error(f"Invalid rule name '{args.rule}'. Use one of {list(TradingRule.__members__.keys())}")
             sys.exit(1)

        # Check required columns and rename Volume->TickVolume
        required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in ohlcv_df.columns for col in required_cols_indicator):
            logger.print_error(f"DataFrame is missing required columns for calculation: {required_cols_indicator}. Available: {ohlcv_df.columns.tolist()}")
            sys.exit(1)
        # Rename just before passing, operate on a copy
        ohlcv_df_renamed = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')

        try:
            # Call the simplified calculation function
            # Pass the enum member directly - corrected from TradingRule(selected_rule) in your provided code
            result_df = calculate_pressure_vector(
                df=ohlcv_df_renamed.copy(),
                point=point_size,
                tr_num=TradingRule(selected_rule),
            )

            # --- DEBUGGING PRINT (Keep if needed, uses logger.print_debug) ---
            # This debug print shows the tail of the result df
            logger.print_debug(f"\n--- DEBUG: Result DF Tail for Rule: {selected_rule.name} ---")
            cols_to_debug = ['Open', 'PPrice1', 'PPrice2', 'Direction', 'PColor1', 'PColor2']
            existing_cols_to_debug = [col for col in cols_to_debug if col in result_df.columns]
            if existing_cols_to_debug:
                 debug_tail_str = result_df[existing_cols_to_debug].tail().to_string()
                 logger.print_debug(debug_tail_str)
            else:
                 logger.print_debug("No differentiating columns found to print.")
            logger.print_debug(f"--- END DEBUG ---")
            # --- END DEBUGGING PRINT ---

        except Exception as e:
             logger.print_error(f"An error occurred during indicator calculation:{e}")
             # Print traceback if needed
             import traceback
             print(traceback.format_exc())
             sys.exit(1)

        end_time_calc = time.perf_counter()
        calc_duration = end_time_calc - start_time_calc

    # Handle cases where data was not loaded or empty after fetch
    elif ohlcv_df is None:
         logger.print_error("No data loaded, cannot calculate indicator.")
         # Allow script to continue to print summary
    else: # DataFrame exists but is empty
         logger.print_warning("Loaded DataFrame is empty, skipping calculation.")


    # --- Plotting Results ---
    plot_duration = 0
    # Check if calculation was successful before plotting
    if result_df is not None and not result_df.empty:

        # # --- added check for columns ---
        # logger.print_debug(f"Columns BEFORE plotting: {result_df.columns.tolist()}")
        # # --- end of added check ---
        #
        # # --- volume check ---
        # if 'Volume' in result_df.columns:
        #     logger.print_debug(f"Volume data stats:\n{result_df['Volume'].describe().to_string()}")
        #     logger.print_debug(f"Volume data tail:\n{result_df['Volume'].tail().to_string()}")
        # else:
        #     logger.print_debug("Volume column not found in result_df for value check.")
        # # --- end of volume check ---

        logger.print_info("\nPlotting results...") # Log plotting start AFTER check
        start_time_plot = time.perf_counter()

        # Construct title (ensure selected_rule is not None)
        chart_title = f"{data_source_label} | {args.interval} | Rule: {selected_rule.name if selected_rule else 'N/A'}"
        if estimated_point and point_size is not None: # Add point size only if estimated
            point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
            chart_title += f" | Est. Point: {point_size:{point_format}}"

        try:
            # Pass the result_df and the selected rule (enum member)
            if selected_rule is not None:
                # Pass the enum member directly - corrected from TradingRule(selected_rule) in your provided code
                plot_indicator_results(result_df, TradingRule(selected_rule), title=chart_title)
            else:
                 logger.print_error("No valid trading rule determined. Skipping plotting.")

            logger.print_info("\nPlot displayed. Close the plot window to continue/exit.")
        except Exception as e:
             logger.print_error(f"An error occurred during plotting:{e}")
             import traceback
             print(traceback.format_exc())
        finally:
             end_time_plot = time.perf_counter()
             plot_duration = end_time_plot - start_time_plot

    # Handle cases where calculation didn't run or produced no results
    elif ohlcv_df is not None: # Data was loaded but calculation failed/skipped
        logger.print_info("Skipping plotting as indicator calculation did not produce results.")
    # else: # No data was loaded initially - handled above


    # --- Timing and Size Summary ---
    # ... (Summary code remains the same) ...
    end_time_total = time.perf_counter()
    total_duration = end_time_total - start_time_total

    # Print summary using logger and formatting function
    logger.print_info("\n--- Execution Summary ---")
    logger.print_info(logger.format_summary_line("Data Source:", data_source_label if effective_mode != 'demo' else 'Demo'))
    if effective_mode == 'yfinance':
        logger.print_info(logger.format_summary_line("Ticker:", yf_ticker if yf_ticker else 'N/A'))
        logger.print_info(logger.format_summary_line("Interval Requested:", f"{args.interval} (mapped to {yf_interval if yf_interval else 'N/A'})"))
        if current_start and current_end:
            logger.print_info(logger.format_summary_line("Date Range:", f"{current_start} to {current_end}"))
        else:
            logger.print_info(logger.format_summary_line("Period:", current_period if current_period else 'N/A'))

    if point_size is not None:
        point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
        logger.print_info(logger.format_summary_line("Point Size Used:", f"{point_size:{point_format}}{' (Estimated)' if estimated_point else ''}"))
    else:
         reason = "(Data load failed)" if ohlcv_df is None else "(Not applicable)" # Simplified reason
         logger.print_info(logger.format_summary_line("Point Size Used:", f"N/A {reason}"))

    # Use args.rule for display as selected_rule might be None if calc failed early
    logger.print_info(logger.format_summary_line("Rule Applied:", args.rule))
    logger.print_info("-" * (25 + 1 + 20)) # Adjust separator width based on format_summary_line
    logger.print_info(logger.format_summary_line("Data Size:", f"{data_size_mb:.3f} MB ({data_size_bytes:,} bytes)"))
    logger.print_info(logger.format_summary_line("Data Fetch/Load Time:", f"{data_fetch_duration:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Indicator Calc Time:", f"{calc_duration:.3f} seconds"))
    logger.print_info(logger.format_summary_line("Plotting Time:", f"{plot_duration:.3f} seconds"))
    logger.print_info("-" * (25 + 1 + 20))
    logger.print_info(logger.format_summary_line("Total Execution Time:", f"{total_duration:.3f} seconds"))
    logger.print_info("--- End Summary ---")


if __name__ == "__main__":
    main()