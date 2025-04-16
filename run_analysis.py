# /run_analysis.py (in NeoZorK HLD/ root folder)

# Standard library imports
import sys
import time
from datetime import date

# Imports from the src package
from src.cli import parse_arguments # Import argument parsing function
from src.data_utils import get_demo_data, map_interval, map_ticker, fetch_yfinance_data # Import data functions
from src.utils import determine_point_size # Import point size estimation
from src.constants import TradingRule # Keep direct import for type hinting if needed later
from src.indicator import calculate_pressure_vector
from src.plotting import plot_indicator_results

# --- Main Execution Function ---
def main():
    """Main function to run the analysis."""
    # Start overall timer
    start_time_total = time.perf_counter()

    # Get command line arguments
    args = parse_arguments()

    # --- Data Acquisition ---
    start_time_data = time.perf_counter()
    ohlcv_df = None
    point_size = None
    data_source_label = ""
    estimated_point = False # Flag to track if point size was estimated
    yf_ticker = None # Store mapped ticker if applicable
    yf_interval = None # Store mapped interval if applicable
    current_period = None # Store effective period
    current_start = None # Store effective start date
    current_end = None # Store effective end date

    # Handle mode selection ('yf' alias)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    if effective_mode == 'demo':
        print("--- Mode: Demo ---")
        data_source_label = "Demo Data"
        ohlcv_df = get_demo_data()
        # Use a fixed point size for demo data
        point_size = 0.00001
        print(f"[Info] Using built-in demo data. Point size set to: {point_size}")

    elif effective_mode == 'yfinance':
        print("--- Mode: Yahoo Finance ---")
        # Validate required arguments for yfinance mode
        if not args.ticker:
             print("[Error] Ticker (--ticker) is required for yfinance mode.")
             sys.exit(1)
        # Point size is optional now

        data_source_label = args.ticker # Use ticker for plot title

        # Map and validate interval
        try:
            yf_interval = map_interval(args.interval)
        except ValueError as e:
            print(f"[Error] {e}")
            sys.exit(1)

        # Map ticker (optional enhancement)
        yf_ticker = map_ticker(args.ticker)

        # Determine history parameters
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end

        # Handle date logic
        if args.start and not args.end:
            end_arg = date.today().strftime('%Y-%m-%d')
            print(f"[Info] End date not specified, using today: {end_arg}")
        elif args.end and not args.start:
            print("[Error] Start date (--start) must be specified if end date (--end) is used.")
            sys.exit(1)

        # Determine effective period/dates for download
        if start_arg and end_arg:
            current_start = start_arg
            current_end = end_arg
            print(f"[Info] Fetching data for interval '{yf_interval}' from {current_start} to {current_end}")
        else:
            current_period = period_arg
            print(f"[Info] Fetching data for interval '{yf_interval}' for period '{current_period}'")

        # Fetch data using the function from data_utils
        ohlcv_df = fetch_yfinance_data(
            ticker=yf_ticker,
            interval=yf_interval,
            period=current_period,
            start_date=current_start,
            end_date=current_end
        )

        if ohlcv_df is None or ohlcv_df.empty:
            print("[Error] Could not fetch valid data from Yahoo Finance. Exiting.")
            sys.exit(1)

        # --- Point Size Determination/Override ---
        if args.point is not None:
             # User provided point size - override estimation
             if args.point <= 0:
                  print("[Error] Provided point size (--point) must be positive.")
                  sys.exit(1)
             point_size = args.point
             print(f"[Info] Using user-provided point size: {point_size}")
        else:
             # Estimate point size using the function from utils
             point_size = determine_point_size(yf_ticker, ohlcv_df)
             estimated_point = True
             print(f"[Warning] Automatically estimated point size: {point_size:.8f}. "
                   f"This is an estimate and might be inaccurate. "
                   f"Use the --point argument to specify it accurately for reliable calculations.")


    # Record data acquisition time and size
    end_time_data = time.perf_counter()
    data_fetch_duration = end_time_data - start_time_data
    data_size_bytes = 0
    data_size_mb = 0
    if ohlcv_df is not None:
        data_size_bytes = ohlcv_df.memory_usage(deep=True).sum()
        data_size_mb = data_size_bytes / (1024 * 1024)


    # --- Indicator Calculation ---
    result_df = None
    calc_duration = 0
    selected_rule = None # Define here for use in summary
    if ohlcv_df is not None and not ohlcv_df.empty:
        print(f"\nCalculating indicator using rule: {args.rule}...")
        start_time_calc = time.perf_counter()

        # Map rule string to enum
        try:
             selected_rule = TradingRule[args.rule]
        except KeyError:
             print(f"[Error] Invalid rule name '{args.rule}'. Use one of {list(TradingRule.__members__.keys())}")
             sys.exit(1)

        # Check for required columns and rename Volume->TickVolume before passing
        required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in ohlcv_df.columns for col in required_cols_indicator):
            print(f"[Error] DataFrame is missing required columns for calculation: {required_cols_indicator}. Available: {ohlcv_df.columns.tolist()}")
            sys.exit(1)
        ohlcv_df_renamed = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')

        try:
            result_df = calculate_pressure_vector(
                df=ohlcv_df_renamed.copy(), # Pass copy
                point=point_size,
            )
        except Exception as e:
             print(f"An error occurred during indicator calculation:",e)
             sys.exit(1)

        end_time_calc = time.perf_counter()
        calc_duration = end_time_calc - start_time_calc
    elif ohlcv_df is None:
         print("[Error] No data loaded, cannot calculate indicator.")
         sys.exit(1)
    else: # DataFrame exists but is empty
         print("[Warning] Loaded DataFrame is empty, skipping calculation.")


    # --- Plotting Results ---
    plot_duration = 0
    if result_df is not None and not result_df.empty:
        print("\nPlotting results...")
        start_time_plot = time.perf_counter()
        chart_title = f"{data_source_label} | {args.interval} | Rule: {selected_rule.name}"
        if estimated_point:
            chart_title += f" | Est. Point: {point_size:.8f}"

        try:
            # Pass the result_df which should have 'Volume'
            plot_indicator_results(result_df, TradingRule(rule=selected_rule), title=chart_title)
            print("\nPlot displayed. Close the plot window to continue/exit.")
        except Exception as e:
             print(f"An error occurred during plotting:",e)
        finally:
             end_time_plot = time.perf_counter()
             plot_duration = end_time_plot - start_time_plot

    elif result_df is None and ohlcv_df is not None:
        print("Skipping plotting as indicator calculation did not produce results.")
    else:
        print("Skipping plotting as no data was loaded.")


    # --- Timing and Size Summary ---
    end_time_total = time.perf_counter()
    total_duration = end_time_total - start_time_total

    print("\n--- Execution Summary ---")
    print(f"Data Source:          {data_source_label if effective_mode != 'demo' else 'Demo'}")
    if effective_mode == 'yfinance':
        print(f"Ticker:               {yf_ticker}")
        # Use args.interval for display as it's the user input
        print(f"Interval Requested:   {args.interval} (mapped to {yf_interval})")
        if current_start and current_end:
             print(f"Date Range:           {current_start} to {current_end}")
        else:
             print(f"Period:               {current_period}")
    # Format point size nicely
    point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
    print(f"Point Size Used:      {point_size:{point_format}}{' (Estimated)' if estimated_point else ''}")
    print("-" * 25)
    print(f"Data Size:            {data_size_mb:.3f} MB ({data_size_bytes:,} bytes)") # Add comma separator for bytes
    print(f"Data Fetch/Load Time: {data_fetch_duration:.3f} seconds")
    print(f"Indicator Calc Time:  {calc_duration:.3f} seconds")
    print(f"Plotting Time:        {plot_duration:.3f} seconds")
    print("-" * 25)
    print(f"Total Execution Time: {total_duration:.3f} seconds")
    print("--- End Summary ---")


if __name__ == "__main__":
    main()