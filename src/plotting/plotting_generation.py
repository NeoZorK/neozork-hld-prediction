# -*- coding: utf-8 -*-
# src/plotting/plotting_generation.py

from .mplfinance_plot import plot_indicator_results_mplfinance
from .plotly_plot import plot_indicator_results_plotly
from .fast_plot import plot_indicator_results_fast
from .seaborn_plot import plot_indicator_results_seaborn

"""
Workflow step for generating plots based on indicator results using the selected library (Plotly, mplfinance, fast, seaborn).
Saves Plotly plots as HTML and attempts to open them, displays mplfinance and seaborn plots.
"""
import pandas as pd
import traceback
from pathlib import Path
import webbrowser
import os

from ..common import logger
from ..common.constants import TradingRule

def generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point):
    """
    Generates and potentially saves/displays a plot based on calculation results
    using the library specified in args.draw. Attempts to open saved HTML plots.

    Args:
        args (argparse.Namespace): Command-line arguments (must contain 'draw').
        data_info (dict): Dictionary containing data source information.
        result_df (pd.DataFrame | None): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | None): The specific trading rule enum member used.
        point_size (float | None): The point size used for calculations.
        estimated_point (bool): Flag indicating if point_size was estimated.
    """
    # --- Basic Validation ---
    if result_df is None or result_df.empty:
        logger.print_info("Skipping plotting as no valid calculation results are available.")
        return
    if selected_rule is None:
        logger.print_warning("No valid rule selected, cannot generate plot accurately.")
        return

    # --- Check for AUTO mode ---
    is_auto_mode = False
    if hasattr(args, 'auto_display_mode') and args.auto_display_mode:
        is_auto_mode = True
        # Ensure selected_rule is properly set for AUTO mode
        if isinstance(selected_rule, str):
            if selected_rule not in ['AUTO', 'Auto_Display_All']:
                selected_rule = 'Auto_Display_All'
        else:
            selected_rule = 'Auto_Display_All'
        logger.print_info("AUTO display mode detected, will display all available columns")

    # Use 'fastest' as default drawing method if draw is not specified
    if not hasattr(args, 'draw') or args.draw is None:
        logger.print_info("Drawing method not specified, using 'fastest' by default.")
        args.draw = 'fastest'

    # --- DEBUG: Print DataFrame info before plotting ---
    logger.print_debug("--- DataFrame before plotting ---")
    logger.print_debug(f"Columns: {result_df.columns.tolist()}")
    logger.print_debug(f"Index type: {type(result_df.index)}")
    logger.print_debug(f"Shape: {result_df.shape}")
    logger.print_debug("First 5 rows:")
    with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
        logger.print_debug(f"\n{result_df.head().to_string()}")
    logger.print_debug("--- End DataFrame info ---")

    # --- Construct Title ---
    title_parts = []
    data_label = data_info.get('data_source_label', 'Unknown Source')
    if isinstance(data_label, str) and ('/' in data_label or '\\' in data_label):
        data_label = Path(data_label).stem
    title_parts.append(data_label)

    # Extract interval from data_info or args
    if 'data_source_label' in data_info and isinstance(data_info['data_source_label'], str):
        # Try to extract interval from data_source_label
        source_label = data_info['data_source_label']
        if 'PERIOD_' in source_label:
            try:
                interval_str = source_label.split('PERIOD_')[1].split('_')[0].split('.')[0]
            except (IndexError, ValueError):
                # If extraction fails, fallback to args or data_info
                interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')
        else:
            interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')
    else:
        interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')

    title_parts.append(interval_str)
    if point_size is not None:
        try:
            precision = 8 if abs(point_size) < 0.001 else 5 if abs(point_size) < 0.1 else 2
            point_str = f"{point_size:.{precision}f}"
            title_parts.append(f"Pt:{point_str}{'~' if estimated_point else ''}")
        except (TypeError, ValueError):
            logger.print_warning(f"Could not format point size for title: {point_size}")
    plot_title = " | ".join(filter(None, title_parts))

    # --- Choose Plotting Function based on args.draw ---
    draw_mode = getattr(args, 'draw', 'fastest').lower()
    use_mplfinance = draw_mode in ['mplfinance', 'mpl']
    use_seaborn = draw_mode in ['seaborn', 'sb']

    try:
        if use_mplfinance:
            logger.print_info("Generating plot using mplfinance...")
            plot_indicator_results_mplfinance(
                result_df,
                selected_rule,
                plot_title
            )
            logger.print_success("Mplfinance plot generation finished (should display).")
        elif use_seaborn:
            logger.print_info("Generating plot using seaborn...")
            plot_indicator_results_seaborn(
                result_df,
                selected_rule,
                plot_title
            )
            logger.print_success("Seaborn plot generation finished (should display).")
        elif draw_mode == 'fast':
            logger.print_info("Generating plot using Dask+Datashader+Bokeh (fast)...")
            plot_indicator_results_fast(
                result_df,
                selected_rule,
                plot_title
            )
        else:
            logger.print_info("Generating plot using Plotly...")
            fig = plot_indicator_results_plotly(
                result_df,
                selected_rule,
                plot_title
            )
            if fig is None:
                logger.print_warning("Plotly generation returned None. Skipping save.")
                return
            # --- Save Plotly Plot as HTML ---
            output_dir = Path("results/plots")
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.print_error(f"Could not create plot output directory {output_dir}: {e}")
                return
            # Construct filename
            filename_parts = [
                data_label.replace(':', '_').replace('/', '_').replace('\\\\', '_'),
                interval_str
            ]

            # Add point size if available
            if hasattr(selected_rule, 'name'):
                rule_shortname = selected_rule.name.replace("_", "")
            else:
                rule_shortname = str(selected_rule).replace("_", "")

            filename_parts.append(rule_shortname)
            filename_parts.append("plotly")

            filename = "_".join(filter(None, filename_parts)) + ".html"
            filepath = output_dir / filename
            try:
                fig.write_html(str(filepath), include_plotlyjs='cdn')
                logger.print_success(f"Interactive Plotly plot saved successfully to: {filepath}")
                try:
                    # Check if we are running in a Docker container
                    in_docker = os.path.exists('/.dockerenv') or os.environ.get('RUNNING_IN_DOCKER') == 'true'

                    if not in_docker:
                        # Only open in browser if not in Docker
                        absolute_filepath = filepath.resolve()
                        file_uri = absolute_filepath.as_uri()
                        webbrowser.open(file_uri)
                        logger.print_info(f"Attempting to open {filepath} in default browser...")
                    else:
                        logger.print_info(f"Running in Docker container - opening in lynx browser...")
                        # Full path for lynx
                        absolute_filepath = filepath.resolve()
                        # Use subprocess to open in lynx
                        import subprocess
                        try:
                            # Check if lynx is installed
                            lynx_check = subprocess.run(['which', 'lynx'], capture_output=True, text=True)
                            if lynx_check.returncode == 0:
                                # Open the HTML file in lynx browser
                                subprocess.Popen(['lynx', '-localhost', '-force_html', str(absolute_filepath)],
                                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                                logger.print_success(f"HTML file opened in lynx browser")
                            else:
                                logger.print_warning("Lynx browser not found. Install with: apt-get install lynx")
                        except Exception as lynx_error:
                            logger.print_warning(f"Failed to open in lynx: {lynx_error}")

                        # Display the file path in the console
                        logger.print_info(f"You can also access this plot at: http://localhost:8080/plots/{filename}")
                except Exception as e_open:
                    logger.print_warning(
                        f"Could not automatically open the plot in browser: {type(e_open).__name__}: {e_open}")
                    logger.print_debug(f"Traceback (open plot):\n{traceback.format_exc()}")
            except Exception as e_save:
                logger.print_error(f"Failed to save Plotly plot to {filepath}: {type(e_save).__name__}: {e_save}")
                logger.print_debug(f"Traceback (save plot):\n{traceback.format_exc()}")
    except Exception as e_gen:
        logger.print_error(f"An error occurred during plot generation: {type(e_gen).__name__}: {e_gen}")
        logger.print_debug(f"Traceback (generate plot):\n{traceback.format_exc()}")

