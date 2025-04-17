# src/point_size_determination.py

"""
Workflow Step 2: Determines the point size to use.
All comments are in English.
"""

# Use relative imports within the src package
from . import logger
from .utils import determine_point_size # Import the core estimation function

def get_point_size(args, data_info: dict):
    """
    Determines point size based on args or estimation using data_info.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        data_info (dict): Dictionary containing info from the data acquisition step,
                          including 'ohlcv_df', 'effective_mode', 'yf_ticker'.

    Returns:
        tuple: (point_size, estimated_point) or raises ValueError on failure.
    """
    logger.print_info("--- Step 2: Determining Point Size ---")
    point_size = None
    estimated_point = False
    ohlcv_df = data_info.get("ohlcv_df")
    effective_mode = data_info.get("effective_mode")
    yf_ticker = data_info.get("yf_ticker")

    if effective_mode == 'demo':
        point_size = 0.00001 # Fixed for demo
        estimated_point = False
        logger.print_info(f"Using fixed point size for demo: {point_size}")
    elif effective_mode == 'yfinance':
        if ohlcv_df is None or ohlcv_df.empty:
             raise ValueError("Cannot determine point size without valid data.")

        if args.point is not None:
            if args.point <= 0:
                raise ValueError("Provided point size (--point) must be positive.")
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size: {point_size}")
        else:
            logger.print_info("Attempting to estimate point size automatically...")
            # Pass ticker from data_info to the utility function
            point_size = determine_point_size(yf_ticker)
            if point_size is None:
                raise ValueError(f"Automatic point size estimation failed for {yf_ticker}. Use --point.")
            estimated_point = True
            logger.print_warning(f"Est. point size: {point_size:.8f}. ESTIMATE ONLY. Use --point.")

    if point_size is None: # Safeguard
         raise ValueError("Failed to determine point size.")

    logger.print_debug(f"Point size determined: {point_size} (Estimated: {estimated_point})")
    return point_size, estimated_point