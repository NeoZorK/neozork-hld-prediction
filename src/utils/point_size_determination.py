# src/utils/point_size_determination.py # Re-verified

"""
Workflow Step 2: Determines the point size to use.
All comments are in English.
"""
# Use relative imports within the src package
from ..common import logger
from .utils import determine_point_size # For yfinance estimation

# Definition of the get_point_size function
def get_point_size(args, data_info: dict):
    """
    Determines point size based on args or estimation using data_info.
    Handles 'demo', 'csv', 'polygon', 'yfinance', 'binance', and 'exrate' modes.

    Args:
        args (argparse.Namespace): Parsed command-line arguments. Must contain 'point'.
        data_info (dict): Dictionary containing info from the data acquisition step,
                          including 'ohlcv_df', 'effective_mode', 'yf_ticker'.

    Returns:
        tuple: (point_size, estimated_point) or raises ValueError on failure.
    """
    logger.print_info("--- Step 2: Determining Point Size ---")
    # Initialize variables
    point_size = None
    estimated_point = False
    # Extract needed info from the data_info dictionary
    ohlcv_df = data_info.get("ohlcv_df")
    effective_mode = data_info.get("effective_mode")
    yf_ticker = data_info.get("yf_ticker") # Used only in yfinance mode

    # --- Handle point size based on mode ---

    # Demo Mode
    if effective_mode == 'demo':
        point_size = 0.00001 # Fixed point size for demonstration data
        estimated_point = False
        logger.print_info(f"Using fixed point size for demo: {point_size}")

    # CSV Mode
    elif effective_mode == 'csv':
        logger.print_info("Checking for user-provided point size (required for CSV mode)...")
        if args.point is None:
            # Error should be raised by CLI parser, but double-check
            raise ValueError("Point size (--point) must be provided when using csv mode.")
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        else:
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size for CSV: {point_size}")

    # Polygon Mode
    elif effective_mode == 'polygon':
        logger.print_info("Checking for user-provided point size (required for Polygon mode)...")
        if args.point is None:
            raise ValueError("Point size (--point) must be provided when using polygon mode.")
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        else:
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size for Polygon: {point_size}")

    # Binance Mode - CORRECTED Block (logic was ok, ensure flow)
    elif effective_mode == 'binance':
        logger.print_info("Checking for user-provided point size (required for Binance mode)...")
        if args.point is None:
            raise ValueError("Point size (--point) must be provided when using binance mode (estimation not reliable).")
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        else:
            point_size = args.point # Assign point size here
            estimated_point = False # Point size is provided by user
            logger.print_info(f"Using user-provided point size for Binance: {point_size}")

    # Exchange Rate API Mode
    elif effective_mode == 'exrate':
        logger.print_info("Checking for user-provided point size (required for Exchange Rate API mode)...")
        if args.point is None:
            raise ValueError("Point size (--point) must be provided when using exrate mode.")
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        else:
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size for Exchange Rate API: {point_size}")

    # YFinance Mode
    elif effective_mode == 'yfinance':
        if ohlcv_df is None or ohlcv_df.empty:
             raise ValueError("Cannot determine point size without valid data (yfinance fetch failed?).")
        # Use provided point if available
        if args.point is not None:
            if args.point <= 0:
                raise ValueError("Provided point size (--point) must be positive.")
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size: {point_size}")
        # Otherwise, attempt estimation
        else:
            logger.print_info(f"Attempting to estimate point size automatically for {yf_ticker}...")
            point_size = determine_point_size(yf_ticker) # Calls the estimation utility
            if point_size is None:
                raise ValueError(f"Automatic point size estimation failed for {yf_ticker}. Use --point argument.")
            estimated_point = True
            logger.print_warning(f"Using estimated point size: {point_size:.8f}. Note: This is an ESTIMATE. Use --point for accuracy.")

    # Final fallback check
    if point_size is None:
        # This should ideally not be reached if all modes and validation work correctly
         raise ValueError(f"Internal Error: Failed to determine point size for mode '{effective_mode}'. Logic might be flawed.")

    logger.print_debug(f"Point size determined: {point_size} (Estimated: {estimated_point})")
    return point_size, estimated_point