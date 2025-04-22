# src/utils/point_size_determination.py

"""
Workflow step responsible for determining the instrument's point size.
Uses provided arguments or attempts estimation for specific modes like yfinance.
All comments are in English.
"""

import pandas as pd
from typing import Tuple, Dict, Optional

# Use relative imports for logger and potentially the estimation utility
from ..common import logger
# Assuming the actual estimation logic is in utils.py
from .utils import determine_point_size as estimate_point_size_from_yf

# Definition of the workflow step function
def determine_point_size(args, df: Optional[pd.DataFrame], data_info: Dict) -> Tuple[Optional[float], bool]:
    """
    Determines the point size based on mode and arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        df (Optional[pd.DataFrame]): The raw data DataFrame (needed for yfinance estimation).
        data_info (Dict): Dictionary containing data source information (like mode).

    Returns:
        Tuple[Optional[float], bool]:
            - The determined point size (float) or None if not determinable.
            - A boolean flag indicating if the point size was estimated (True) or provided/fixed (False).
    """
    point_size: Optional[float] = None
    estimated: bool = False
    effective_mode = data_info.get('mode', 'unknown') # Get mode from data_info

    # 1. Check if point size was explicitly provided via CLI argument
    if args.point is not None:
        logger.print_info(f"Using explicitly provided point size: {args.point}")
        point_size = args.point
        estimated = False
        return point_size, estimated

    # 2. Handle modes where point size is fixed or required
    if effective_mode == 'demo':
        # Use a fixed default point size for demo data
        point_size = 1e-5 # Example default for demo EURUSD-like data
        estimated = False
        logger.print_info(f"Using fixed point size for demo: {point_size}")
        return point_size, estimated

    if effective_mode in ['csv', 'polygon', 'binance']:
        # For these modes, --point should have been required by CLI validation.
        # If we reach here and args.point is None, it's an unexpected state.
        logger.print_error(f"Point size (--point) was required but not provided or found for mode '{effective_mode}'.")
        return None, False # Cannot determine point size

    # 3. Handle yfinance mode (potential estimation)
    if effective_mode == 'yfinance':
        logger.print_info("Attempting to determine point size for yfinance...")
        # Check if the estimation function exists and df is available
        if df is not None and not df.empty:
            try:
                # Call the actual estimation function (renamed import)
                estimated_value = estimate_point_size_from_yf(df)
                if estimated_value is not None:
                    point_size = estimated_value
                    estimated = True
                    logger.print_success(f"Estimated point size using yfinance data: {point_size}")
                else:
                    logger.print_warning("Could not estimate point size from yfinance data.")
            except Exception as e:
                logger.print_error(f"Error during yfinance point size estimation: {e}")
        else:
            logger.print_warning("DataFrame is empty or None, cannot estimate point size for yfinance.")

        if point_size is None:
             logger.print_error("Failed to determine point size for yfinance. Please provide it using --point.")
             return None, estimated # Return None, estimation status might be True if tried

        return point_size, estimated

    # 4. Fallback for unknown modes or unhandled cases
    logger.print_error(f"Could not determine point size for mode '{effective_mode}'.")
    return None, False

