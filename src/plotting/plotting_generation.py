# src/plotting/plotting_generation.py (Removed tqdm wrapper for plotting)

"""
Workflow step for generating plots based on indicator results.
All comments are in English.
"""
import pandas as pd
# Removed: from tqdm import tqdm
import traceback

# Relative imports
from ..common import logger
from ..common.constants import TradingRule
from .plotting import plot_indicator_results

# Definition of generate_plot function
def generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point):
    """
    Generates and potentially saves a plot based on calculation results.

    Args:
        args (argparse.Namespace): Command-line arguments.
        data_info (dict): Dictionary containing data source information.
        result_df (pd.DataFrame | None): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | None): The specific trading rule enum member used.
        point_size (float | None): The point size used for calculations.
        estimated_point (bool): Flag indicating if point_size was estimated.
    """
    if result_df is None or result_df.empty:
        logger.print_info("Skipping plotting as no valid calculation results are available.")
        return
    if selected_rule is None:
         logger.print_warning("No valid rule selected, cannot generate plot accurately.")
         return

    # Construct plot title
    title_parts = [
        data_info.get('data_source_label', 'Unknown Source'),
        str(args.interval)
    ]
    if point_size is not None:
         try:
              precision = 8 if abs(point_size) < 0.001 else 4 if abs(point_size) < 0.1 else 2
              point_str = f"{point_size:.{precision}f}"
              title_parts.append(f"Point: {point_str}{' (Est.)' if estimated_point else ''}")
         except TypeError:
              logger.print_warning(f"Could not format point size for title: {point_size}")

    title = " | ".join(title_parts)

    try:
        logger.print_info("Generating plot...") # Log start

        # --- Call plotting function directly without tqdm wrapper ---
        plot_indicator_results(
            result_df,
            selected_rule,
            title
        )
        # --- End of direct call ---

        logger.print_success("Plot generation finished successfully.")

    except Exception as e:
        logger.print_error(f"An error occurred during plotting: {type(e).__name__}: {e}")
        logger.print_debug(f"Traceback:\n{traceback.format_exc()}")