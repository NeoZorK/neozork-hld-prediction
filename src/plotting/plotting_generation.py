# src/plotting_generation.py

"""
Workflow Step 4: Generates and displays the plot.
All comments are in English.
"""
import pandas as pd
import traceback
# Use relative imports within the src package
from ..common import logger
from ..common.constants import TradingRule
# Import from sibling module plotting.py
from .plotting import plot_indicator_results

def generate_plot(args, data_info: dict, result_df: pd.DataFrame | None, selected_rule: TradingRule | None, point_size: float | None, estimated_point: bool):
    """
    Generates and displays the plot if results are available.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        data_info (dict): Dictionary with info from data acquisition step.
        result_df (pd.DataFrame | None): The DataFrame with indicator results.
        selected_rule (TradingRule | None): The enum member for the rule used.
        point_size (float | None): The point size used.
        estimated_point (bool): Flag indicating if point size was estimated.
    """
    if result_df is None or result_df.empty:
        logger.print_info("Skipping plotting as no valid calculation results are available.")
        return # Exit plotting function

    logger.print_debug(f"Columns BEFORE plotting: {result_df.columns.tolist()}")
    logger.print_info("\n--- Step 4: Plotting Results ---")

    # Construct title
    data_source_label = data_info.get('data_source_label','N/A')
    chart_title = f"{data_source_label} | {args.interval} | Rule: {selected_rule.name if selected_rule else 'N/A'}"
    if data_info.get("effective_mode") == 'yfinance' and estimated_point and point_size is not None:
        point_format = ".8f" if point_size < 0.001 else ".5f" if point_size < 0.1 else ".2f"
        chart_title += f" | Est. Point: {point_size:{point_format}}"

    try:
        if selected_rule is None:
            logger.print_warning("No valid rule selected, cannot generate plot accurately.")
            return

        # Call the actual plotting function from plotting.py
        plot_indicator_results(result_df, selected_rule, title=chart_title)
        logger.print_info("\nPlot displayed. Close the plot window to continue/exit.")

    except Exception as e:
         logger.print_error(f"An error occurred during plotting:{e}")
         print(traceback.format_exc()) # Keep traceback for plotting errors
         # Log error but don't necessarily stop the whole workflow here