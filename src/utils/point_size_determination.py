# src/utils/point_size_determination.py # MODIFIED

"""
Workflow Step 2: Determines the point size to use.
All comments are in English.
"""
# Use relative imports within the src package
from ..common import logger
from .utils import determine_point_size

# Definition of the get_point_size function
def get_point_size(args, data_info: dict):
    """
    Determines point size based on args or estimation using data_info.
    Handles 'demo', 'csv', 'polygon', and 'yfinance' modes.

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

    # Handle 'demo' mode: fixed point size
    if effective_mode == 'demo':
        point_size = 0.00001 # Fixed point size for demonstration data
        estimated_point = False # Point size is not estimated in demo mode
        logger.print_info(f"Using fixed point size for demo: {point_size}")

    # Handle 'csv' mode: require user-provided point size
    elif effective_mode == 'csv':
        logger.print_info("Checking for user-provided point size (required for CSV mode)...")
        if args.point is None:
            raise ValueError("Point size (--point) must be provided when using csv mode.")
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        else:
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size for CSV: {point_size}")

    # Handle 'polygon' mode: require user-provided point size --- ADDED BLOCK ---
    elif effective_mode == 'polygon':
        logger.print_info("Checking for user-provided point size (required for Polygon mode)...")
        # Checks if the --point argument was provided by the user.
        if args.point is None:
            # If --point is missing for Polygon mode, raise an error.
            raise ValueError("Point size (--point) must be provided when using polygon mode.")
        # Checks if the provided point size is positive.
        elif args.point <= 0:
            raise ValueError("Provided point size (--point) must be positive.")
        # If point size is provided and valid, use it.
        else:
            point_size = args.point
            estimated_point = False # Point size is provided by user, not estimated
            logger.print_info(f"Using user-provided point size for Polygon: {point_size}")

    # Handle 'yfinance' mode: use provided or estimate
    elif effective_mode == 'yfinance':
        if ohlcv_df is None or ohlcv_df.empty:
             raise ValueError("Cannot determine point size without valid data (yfinance fetch failed?).")
        if args.point is not None:
            if args.point <= 0:
                raise ValueError("Provided point size (--point) must be positive.")
            point_size = args.point
            estimated_point = False
            logger.print_info(f"Using user-provided point size: {point_size}")
        else:
            logger.print_info(f"Attempting to estimate point size automatically for {yf_ticker}...")
            point_size = determine_point_size(yf_ticker) # Calls the estimation utility
            if point_size is None:
                raise ValueError(f"Automatic point size estimation failed for {yf_ticker}. Use --point argument.")
            estimated_point = True
            logger.print_warning(f"Using estimated point size: {point_size:.8f}. Note: This is an ESTIMATE. Use --point for accuracy.")

    # Final safeguard check
    if point_size is None: # This should not be reached if all modes are handled
         raise ValueError(f"Failed to determine point size for mode '{effective_mode}'.")

    logger.print_debug(f"Point size determined: {point_size} (Estimated: {estimated_point})")
    return point_size, estimated_point